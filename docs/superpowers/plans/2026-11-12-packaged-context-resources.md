# Packaged Context Resources Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Anjela's public-safe default context load successfully from a normally installed wheel while preserving `ANJELA_CONTEXT_DIR` overrides.

**Architecture:** Store the five runtime Markdown files in the `anjela.context` package and include them as setuptools package data. `context_loader` will use the common read-only `Traversable` interface for both `pathlib.Path` overrides and `importlib.resources` defaults, keeping validation identical across both sources.

**Tech Stack:** Python 3.11+, setuptools, `importlib.resources`, pytest, pip wheel

**Spec:** `docs/superpowers/specs/2026-11-12-packaged-context-resources-design.md`

## Global Constraints

- Do not add production dependencies.
- Preserve Python `>=3.11`.
- Preserve `ANJELA_CONTEXT_DIR` as the highest-priority context source.
- Package only the five public-safe runtime files named in the spec.
- Do not change or merge `main`; commit and push only `feat/mvp-0.3-context-loader`.
- Tests must not make paid OpenAI API requests.

## Review Focus

- A wheel missing any one required persona resource must fail the packaging test.
- Loading from an extracted wheel must not fall back to the source checkout.
- An explicit filesystem override must still win over bundled resources.
- Missing or empty required files in an override must still raise the existing errors.
- Optional bundled reference files must remain user-level reference data rather than privileged instructions.

---

### Task 1: Package and load runtime context resources

**Files:**
- Create: `src/anjela/context/__init__.py`
- Move: `docs/context/boot.md` -> `src/anjela/context/boot.md`
- Move: `docs/context/personality.md` -> `src/anjela/context/personality.md`
- Move: `docs/context/memory.md` -> `src/anjela/context/memory.md`
- Move: `docs/context/project-history.md` -> `src/anjela/context/project-history.md`
- Move: `docs/context/archive-index.md` -> `src/anjela/context/archive-index.md`
- Modify: `src/anjela/context_loader.py`
- Modify: `pyproject.toml`
- Create: `tests/test_packaging.py`
- Test: `tests/test_context_loader.py`

**Interfaces:**
- Consumes: `load_context(directory: str | Path | None = None) -> ContextBundle`
- Produces: `default_context_dir() -> importlib.resources.abc.Traversable`; bundled package `anjela.context`; unchanged `ContextBundle` and override API

- [ ] **Step 1: Write the failing wheel integration test**

Create `test_wheel_contains_context_and_loads_default`. Build with `python -m pip wheel . --no-deps --wheel-dir <tmp>`, assert the wheel contains `anjela/context/{boot,personality,memory,project-history,archive-index}.md`, extract it, then run a subprocess from the extracted directory that imports `load_context()` and asserts persona plus reference content are non-empty.

- [ ] **Step 2: Run the wheel integration test to verify it fails**

Run: `.venv\Scripts\python.exe -m pytest tests\test_packaging.py::test_wheel_contains_context_and_loads_default -vv`

Expected: FAIL because the wheel contains no `anjela/context/*.md` resources.

- [ ] **Step 3: Move the five runtime files into `src/anjela/context` and mark it as a package**

Use `git mv` for the Markdown files so history is preserved. Add a minimal `__init__.py` that documents the package as read-only public-safe runtime context.

- [ ] **Step 4: Configure setuptools package data**

Add `[tool.setuptools.package-data]` in `pyproject.toml` with `"anjela.context" = ["*.md"]`.

- [ ] **Step 5: Load bundled defaults through `importlib.resources`**

Change `default_context_dir()` to return `files("anjela.context")`. Update the internal reader to accept `Path | Traversable`, read bytes once, preserve the byte and character limits, decode UTF-8, and keep the existing missing/empty error behavior. Keep explicit directories converted to `Path`.

- [ ] **Step 6: Run targeted unit and packaging tests**

Run: `.venv\Scripts\python.exe -m pytest tests\test_context_loader.py tests\test_packaging.py -vv`

Expected: all targeted tests PASS, including the external override tests and wheel smoke test.

- [ ] **Step 7: Commit the runtime packaging change**

```powershell
git add pyproject.toml src/anjela/context src/anjela/context_loader.py tests/test_packaging.py tests/test_context_loader.py
git commit -m "feat: package default Anjela context"
```

### Task 2: Align documentation and verify the distribution

**Files:**
- Modify: `README.md`
- Modify: `docs/context/README.md`
- Modify: `docs/context/migration.md`
- Modify: `docs/context/migration/manifest.md`
- Modify: `docs/context/migration/README.md`
- Modify: `docs/context/device-migration-2026-10-24.md`
- Modify: any remaining documentation reference that identifies one of the five moved files under `docs/context`

**Interfaces:**
- Consumes: canonical runtime resource path `src/anjela/context/`
- Produces: documentation with no stale canonical path for the five runtime files

- [ ] **Step 1: Update documentation paths and ownership wording**

Document `src/anjela/context/` as the canonical location for distributable public-safe runtime context. Keep migration maps, templates, and archive catalogs under `docs/context/` and update their links to the moved files.

- [ ] **Step 2: Check for stale runtime paths**

Run: `rg -n "docs/context/(boot|personality|memory|project-history|archive-index)\.md" README.md docs src tests`

Expected: no stale references to the old runtime file locations.

- [ ] **Step 3: Run complete local verification**

Run:

```powershell
.venv\Scripts\python.exe -m compileall -q src tests
uv pip check --python .venv\Scripts\python.exe
.venv\Scripts\python.exe -m pytest -ra -vv
```

Expected: compilation succeeds, all installed packages are compatible, and the full pytest suite passes.

- [ ] **Step 4: Build and smoke-test a fresh wheel outside the repository**

Build the wheel into a temporary directory, install it into a clean Python 3.11 environment, change the working directory outside the repository, call `load_context()`, and confirm both instructions and reference context load without setting `ANJELA_CONTEXT_DIR`.

- [ ] **Step 5: Commit documentation and push the feature branch**

```powershell
git add README.md docs/context
git commit -m "docs: document packaged context resources"
git push origin feat/mvp-0.3-context-loader
```

- [ ] **Step 6: Update PR #10 without merging**

Add the wheel verification result, test count, and packaged resource behavior to the PR description. Keep the PR as a draft while GitHub checks are blocked by billing.

