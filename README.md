# Anjela

Personal AI assistant project.

Anjela is being built as a modular assistant with a small, testable core and clear boundaries for memory, tools, providers, and interfaces.

## Current stage

**MVP 0.2 — first real AI provider**

- Python project layout
- Core assistant loop
- Provider interface
- Local in-memory conversation state
- OpenAI Responses API adapter
- Automatic local fallback when no API key is configured
- CLI entry point
- Unit tests
- GitHub Actions CI

## Project structure

```text
anjela/
├── .github/workflows/main.yml
├── src/anjela/
│   ├── __init__.py
│   ├── __main__.py
│   ├── core.py
│   ├── providers.py
│   └── memory.py
├── tests/
│   ├── test_core.py
│   └── test_providers.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

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

The assistant core knows only about the `Provider` interface. The current OpenAI adapter uses the official Python SDK and the Responses API. This keeps the model vendor behind one boundary, so later providers can be added without rewriting the conversation loop.

API keys are never stored in the repository. `.env` is ignored by Git; use `.env.example` as the template for local configuration.

## Roadmap

1. Stable core and tests
2. Real LLM provider adapter **← current**
3. Persistent memory
4. Tool/plugin system
5. API service
6. Web/mobile interface
7. Deployment

The project deliberately grows in small, testable steps instead of turning into one giant script.
