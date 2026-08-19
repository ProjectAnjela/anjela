# Anjela

Personal AI assistant project.

Anjela is being built as a modular assistant with a small, testable core and clear boundaries for memory, tools, providers, interfaces, and project context.

## Current stage

**MVP 0.2 - first real AI provider + durable memory foundation**

- Python project layout
- Core assistant loop
- Provider interface
- Local in-memory conversation state
- Durable SQLite-backed long-term memory
- OpenAI Responses API adapter
- Automatic local fallback when no API key is configured
- CLI entry point
- Unit tests
- GitHub Actions CI
- Sanitized context index for migration materials

## Project structure

```text
anjela/
├── docs/
│   └── context/
│       ├── README.md
│       ├── boot.md
│       ├── personality.md
│       ├── memory.md
│       ├── project-history.md
│       ├── archive-index.md
│       ├── migration.md
│       └── migration/
│           ├── pack.md
│           └── manifest.md
├── .github/workflows/main.yml
├── src/anjela/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py
│   ├── facts.py
│   ├── long_term_memory.py
│   ├── memory.py
│   ├── providers.py
│   ├── spotify_listener.py
│   └── sqlite_memory.py
├── tests/
│   ├── test_core.py
│   └── test_providers.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Context layout

The canonical place for sanitized migration context is [`docs/context/README.md`](docs/context/README.md).

The migration map lives in [`docs/context/migration.md`](docs/context/migration.md).

## Run locally

Install the project with OpenAI support:

```bash
pip install -e '.[openai]'
```

Set your API key in the environment:

```bash
export OPENAI_API_KEY='your_api_key_here'
```

Then start Anjela:

```bash
python -m anjela
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = 'your_api_key_here'
python -m anjela
```

Optional model override:

```bash
export ANJELA_MODEL='gpt-5.5'
```

Without `OPENAI_API_KEY`, Anjela stays in local Echo mode, so the project can still be tested without an API connection.

For development:

```bash
pip install -e '.[dev]'
pytest
```

## Spotify listening log

Anjela can save Spotify listening history into the same SQLite database used for local memory. The listener uses Spotify's Web API `GET /me/player/recently-played` endpoint with the `user-read-recently-played` scope.

Create a Spotify app in the Spotify Developer Dashboard, set its redirect URI to:

```text
http://127.0.0.1:8765/callback
```

Then run:

```powershell
$env:SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
anjela-spotify-listener --once
```

For continuous polling:

```powershell
anjela-spotify-listener --interval 60
```

The listener stores OAuth tokens under `~/.anjela/spotify-token.json` by default and stores deduplicated plays in the `spotify_listens` table. Spotify only exposes recent play history through this endpoint, so keep the listener running if you want a fuller ongoing archive.

## Architecture

The assistant core knows only about the `Provider` interface. The current OpenAI adapter uses the official Python SDK and the Responses API. Local conversation history and durable facts are stored separately through SQLite-backed memory classes, while public context docs stay sanitized and versioned.

API keys are never stored in the repository. `.env` is ignored by Git; use `.env.example` as the template for local configuration.

## Roadmap

1. Stable core and tests
2. Real LLM provider adapter and durable memory **← current**
3. Tool/plugin system
4. API service
5. Web/mobile interface
6. Deployment

The project deliberately grows in small, testable steps instead of turning into one giant script.
