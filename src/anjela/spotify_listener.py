"""Spotify listening history capture for Anjela."""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.server
import json
import os
import secrets
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
RECENTLY_PLAYED_URL = "https://api.spotify.com/v1/me/player/recently-played"
SCOPES = ("user-read-recently-played",)


@dataclass(frozen=True)
class SpotifyListen:
    played_at: str
    played_at_ms: int
    track_id: str
    track_name: str
    artists: str
    album: str
    spotify_url: str


class SpotifyListeningStore:
    def __init__(self, database: Path | str) -> None:
        self.database = Path(database)
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database)

    def _init(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS spotify_listens (
                    played_at TEXT NOT NULL,
                    played_at_ms INTEGER NOT NULL,
                    track_id TEXT NOT NULL,
                    track_name TEXT NOT NULL,
                    artists TEXT NOT NULL,
                    album TEXT NOT NULL,
                    spotify_url TEXT NOT NULL,
                    inserted_at INTEGER NOT NULL,
                    PRIMARY KEY (played_at, track_id)
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS spotify_sync_state (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )

    def add_many(self, listens: list[SpotifyListen]) -> int:
        if not listens:
            return 0

        with self._connect() as connection:
            before = connection.total_changes
            connection.executemany(
                """
                INSERT OR IGNORE INTO spotify_listens (
                    played_at,
                    played_at_ms,
                    track_id,
                    track_name,
                    artists,
                    album,
                    spotify_url,
                    inserted_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        listen.played_at,
                        listen.played_at_ms,
                        listen.track_id,
                        listen.track_name,
                        listen.artists,
                        listen.album,
                        listen.spotify_url,
                        int(time.time()),
                    )
                    for listen in listens
                ],
            )
            newest = max(listen.played_at_ms for listen in listens)
            connection.execute(
                """
                INSERT INTO spotify_sync_state (key, value)
                VALUES ('recently_played_after_ms', ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (str(newest),),
            )
            return connection.total_changes - before - 1

    def last_after_ms(self) -> int | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT value FROM spotify_sync_state WHERE key = 'recently_played_after_ms'"
            ).fetchone()
        if row is None:
            return None
        return int(row[0])


def parse_recently_played_item(item: dict[str, Any]) -> SpotifyListen | None:
    track = item.get("track")
    if not isinstance(track, dict) or track.get("type") != "track":
        return None

    played_at = item.get("played_at")
    track_id = track.get("id")
    name = track.get("name")
    if not all(isinstance(value, str) and value for value in (played_at, track_id, name)):
        return None

    artists = ", ".join(
        artist["name"]
        for artist in track.get("artists", [])
        if isinstance(artist, dict) and isinstance(artist.get("name"), str)
    )
    album = track.get("album", {}).get("name", "") if isinstance(track.get("album"), dict) else ""
    external_urls = track.get("external_urls", {})
    spotify_url = external_urls.get("spotify", "") if isinstance(external_urls, dict) else ""

    return SpotifyListen(
        played_at=played_at,
        played_at_ms=spotify_timestamp_ms(played_at),
        track_id=track_id,
        track_name=name,
        artists=artists,
        album=album,
        spotify_url=spotify_url,
    )


def spotify_timestamp_ms(value: str) -> int:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return int(parsed.timestamp() * 1000)


def load_token(token_file: Path) -> dict[str, Any] | None:
    if not token_file.is_file():
        return None
    return json.loads(token_file.read_text(encoding="utf-8"))


def save_token(token_file: Path, token: dict[str, Any]) -> None:
    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text(json.dumps(token, indent=2), encoding="utf-8")


def api_request(url: str, token: str, params: dict[str, str | int] | None = None) -> dict[str, Any]:
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def token_request(data: dict[str, str]) -> dict[str, Any]:
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(TOKEN_URL, data=encoded, method="POST")
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def refresh_token(client_id: str, token: dict[str, Any]) -> dict[str, Any]:
    refreshed = token_request(
        {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
        }
    )
    refreshed["refresh_token"] = refreshed.get("refresh_token", token["refresh_token"])
    refreshed["expires_at"] = int(time.time()) + int(refreshed["expires_in"])
    return refreshed


def authorize(client_id: str, redirect_uri: str) -> dict[str, Any]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(16)
    parsed_redirect = urllib.parse.urlparse(redirect_uri)

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        code: str | None = None
        error: str | None = None

        def do_GET(self) -> None:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if query.get("state", [""])[0] != state:
                self.__class__.error = "OAuth state mismatch"
            else:
                self.__class__.code = query.get("code", [None])[0]
                self.__class__.error = query.get("error", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Spotify authorization complete. You can close this tab.")

        def log_message(self, format: str, *args: Any) -> None:
            return

    server = http.server.HTTPServer((parsed_redirect.hostname or "127.0.0.1", parsed_redirect.port or 8765), CallbackHandler)
    params = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(SCOPES),
            "code_challenge_method": "S256",
            "code_challenge": challenge,
            "state": state,
        }
    )
    webbrowser.open(f"{AUTH_URL}?{params}")
    server.handle_request()

    if CallbackHandler.error:
        raise RuntimeError(f"Spotify authorization failed: {CallbackHandler.error}")
    if not CallbackHandler.code:
        raise RuntimeError("Spotify authorization did not return a code")

    token = token_request(
        {
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": CallbackHandler.code,
            "redirect_uri": redirect_uri,
            "code_verifier": verifier,
        }
    )
    token["expires_at"] = int(time.time()) + int(token["expires_in"])
    return token


def get_access_token(client_id: str, redirect_uri: str, token_file: Path) -> str:
    token = load_token(token_file)
    if token is None:
        token = authorize(client_id, redirect_uri)
        save_token(token_file, token)
    elif int(token.get("expires_at", 0)) <= int(time.time()) + 60:
        token = refresh_token(client_id, token)
        save_token(token_file, token)
    return token["access_token"]


def fetch_recently_played(access_token: str, after_ms: int | None, limit: int) -> list[SpotifyListen]:
    params: dict[str, str | int] = {"limit": limit}
    if after_ms is not None:
        params["after"] = after_ms

    try:
        payload = api_request(RECENTLY_PLAYED_URL, access_token, params)
    except urllib.error.HTTPError as exc:
        if exc.code == 204:
            return []
        raise

    listens = [parse_recently_played_item(item) for item in payload.get("items", [])]
    return [listen for listen in listens if listen is not None]


def run_once(client_id: str, redirect_uri: str, token_file: Path, store: SpotifyListeningStore, limit: int) -> int:
    token = get_access_token(client_id, redirect_uri, token_file)
    listens = fetch_recently_played(token, store.last_after_ms(), limit)
    inserted = store.add_many(listens)
    print(f"Saved {inserted} new Spotify listens.")
    for listen in listens:
        print(f"- {listen.track_name} - {listen.artists}")
    return inserted


def main() -> None:
    parser = argparse.ArgumentParser(description="Save Spotify listening history into Anjela's SQLite database.")
    parser.add_argument("--client-id", default=os.getenv("SPOTIFY_CLIENT_ID"), help="Spotify app client ID.")
    parser.add_argument("--redirect-uri", default=os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8765/callback"))
    parser.add_argument("--token-file", type=Path, default=Path(os.getenv("ANJELA_SPOTIFY_TOKEN", "~/.anjela/spotify-token.json")).expanduser())
    parser.add_argument("--db", type=Path, default=Path(os.getenv("ANJELA_DB", "anjela.db")))
    parser.add_argument("--interval", type=int, default=60, help="Polling interval in seconds.")
    parser.add_argument("--limit", type=int, default=50, choices=range(1, 51), metavar="[1-50]")
    parser.add_argument("--once", action="store_true", help="Fetch once and exit.")
    args = parser.parse_args()

    if not args.client_id:
        raise SystemExit("Set SPOTIFY_CLIENT_ID or pass --client-id.")

    store = SpotifyListeningStore(args.db)
    while True:
        run_once(args.client_id, args.redirect_uri, args.token_file, store, args.limit)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
