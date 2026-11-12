# Packaged Context Resources Design

## Intent

Anjela must load its public-safe default personality and reference context after a normal wheel installation, not only from a source checkout. This closes the packaging gap identified in MVP 0.3 while preserving `ANJELA_CONTEXT_DIR` as an explicit deployment override.

## Goals

- Ship `boot.md`, `personality.md`, `memory.md`, `project-history.md`, and `archive-index.md` inside the Python distribution.
- Load bundled defaults through `importlib.resources`, which works independently of the repository layout.
- Preserve the existing filesystem override and its validation behavior.
- Prove the result by building a wheel, importing it from an isolated location, and loading the bundled context.
- Keep only public-safe, versioned context in the distributable package.

## Non-goals

- Do not package raw transcripts, private repositories, databases, tokens, or secrets.
- Do not add FastAPI, PWA, deployment, or synchronization work in this change.
- Do not make paid OpenAI API calls.
- Do not merge the pull request or modify `main`.

## Constraints

- Python remains `>=3.11`.
- No new production dependency is required; use the standard-library `importlib.resources` API.
- `ANJELA_CONTEXT_DIR` continues to override bundled resources.
- The five runtime context files have one canonical copy inside the Python package; migration-only documentation remains under `docs/context`.
- Existing per-file size and required-file checks remain in force for both packaged and external context.

## Approaches considered

1. **Package resources inside `anjela` — selected.** Move the five public runtime context files into `src/anjela/context`, include them with setuptools package data, and read them with `importlib.resources`. This is portable and avoids relying on repository-relative paths.
2. **Copy `docs/context` during the build.** This preserves the old tree but adds a custom synchronization step and creates two source locations that can drift.
3. **Require `ANJELA_CONTEXT_DIR`.** This avoids packaging work but leaves normal wheel installations incomplete and was rejected by the product requirement.

## Resulting structure

- `src/anjela/context/`: canonical distributable runtime context and package marker.
- `docs/context/`: migration maps, templates, archive catalogs, and documentation pointing to the runtime resource location.
- `src/anjela/context_loader.py`: loads an explicit filesystem directory when supplied, otherwise loads `anjela.context` resources.
- `tests/test_packaging.py`: builds a wheel, confirms all five Markdown resources are included, and verifies default loading from the extracted wheel.

## Acceptance criteria

- The wheel contains all five runtime Markdown files.
- Code imported from the built wheel loads required persona and optional reference context without `ANJELA_CONTEXT_DIR`.
- An explicit external context directory still takes precedence.
- Unit tests, wheel integration test, compilation, and dependency checks pass locally.

