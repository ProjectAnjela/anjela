from pathlib import Path

from anjela.spotify_listener import (
    SpotifyListen,
    SpotifyListeningStore,
    parse_recently_played_item,
)


def test_parse_recently_played_track() -> None:
    listen = parse_recently_played_item(
        {
            "played_at": "2026-08-19T12:34:56.000Z",
            "track": {
                "type": "track",
                "id": "track-1",
                "name": "Song Name",
                "artists": [{"name": "Artist One"}, {"name": "Artist Two"}],
                "album": {"name": "Album Name"},
                "external_urls": {"spotify": "https://open.spotify.com/track/track-1"},
            },
        }
    )

    assert listen is not None
    assert listen.track_name == "Song Name"
    assert listen.artists == "Artist One, Artist Two"
    assert listen.album == "Album Name"
    assert listen.played_at_ms == 1787142896000


def test_parse_recently_played_ignores_non_track_items() -> None:
    listen = parse_recently_played_item(
        {"played_at": "2026-08-19T12:34:56.000Z", "track": {"type": "episode"}}
    )

    assert listen is None


def test_spotify_listening_store_deduplicates_listens(tmp_path: Path) -> None:
    store = SpotifyListeningStore(tmp_path / "anjela.db")
    listen = SpotifyListen(
        played_at="2026-08-19T12:34:56.000Z",
        played_at_ms=1787142896000,
        track_id="track-1",
        track_name="Song Name",
        artists="Artist",
        album="Album",
        spotify_url="https://open.spotify.com/track/track-1",
    )

    assert store.add_many([listen]) == 1
    assert store.add_many([listen]) == 0
    assert store.last_after_ms() == 1787142896000
