# Anjela

Personal AI assistant project.

Anjela is being built as a modular assistant with a small, testable core and clear boundaries for memory, tools, providers, and interfaces.

## Current stage

**MVP foundation**

- Python project layout
- Core assistant loop
- Provider interface
- Local in-memory conversation state
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
│   └── test_core.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Run locally

```bash
python -m anjela
```

For development:

```bash
python -m pytest
```

## Roadmap

1. Stable core and tests
2. Real LLM provider adapter
3. Persistent memory
4. Tool/plugin system
5. API service
6. Web/mobile interface
7. Deployment

The project deliberately grows in small, testable steps instead of turning into one giant script.
