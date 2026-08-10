# Migration Manifest

This manifest records which source artifacts were migrated into the context layout.

## Status values

- `draft` - scaffold exists, content still needs confirmation
- `confirmed` - content is populated and reviewed as public-safe
- `private` - source exists but must stay outside the public repository

## Use this file to record

- source file name
- target file name
- status
- notes about sanitization

## Suggested table

| Source | Target | Status | Notes |
| --- | --- | --- | --- |
| `ANJELA_BOOT.md` | `docs/context/boot.md` | draft | sanitized public template only |
| `ANJELA_PERSONALITY.md` | `docs/context/personality.md` | draft | sanitized public template only |
| `ANJELA_MEMORY.md` | `docs/context/memory.md` | draft | sanitized public template only |
| `PROJECT_HISTORY.md` | `docs/context/project-history.md` | draft | public-safe history scaffold |
| `ANJELA_ARCHIVE_INDEX.md` | `docs/context/archive-index.md` | draft | pointer-only index scaffold |

## Rule

If a source artifact cannot be made safe for public GitHub, mark it `private` and keep the source outside the public repository. If it becomes safe later, move it to `draft` first and then `confirmed` after review.
