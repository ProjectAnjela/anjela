# Anjela

Personal AI assistant project.

Anjela is being built as a modular assistant with a small, testable core and clear boundaries for memory, tools, providers, interfaces, and project context.

## Current stage

**MVP 0.3 - project context loader + durable memory foundation**

- Python project layout
- Core assistant loop
- Provider interface
- Local in-memory conversation state
- Durable SQLite-backed long-term memory
- Sanitized docs/context loader for project identity and history
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
│   ├── context_loader.py
│   ├── core.py
│   ├── facts.py
│   ├── long_term_memory.py
│   ├── memory.py
│   ├── providers.py
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

At runtime, the CLI loads the selected top-level files from `docs/context` and sends them to providers as system context before conversation history. Durable user facts from SQLite are still injected separately, after project context and before user messages.

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

## Architecture

The assistant core knows only about the `Provider` interface. The current OpenAI adapter uses the official Python SDK and the Responses API. Local conversation history and durable facts are stored separately through SQLite-backed memory classes, while public context docs stay sanitized, versioned, and loaded through `ProjectContextLoader`.

API keys are never stored in the repository. `.env` is ignored by Git; use `.env.example` as the template for local configuration.

## Roadmap

1. Stable core and tests
2. Real LLM provider adapter and durable memory
3. Project context loader **← current**
4. Tool/plugin system
5. API service
6. Web/mobile interface
7. Deployment

The project deliberately grows in small, testable steps instead of turning into one giant script.
