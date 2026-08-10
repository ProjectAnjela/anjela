# Migration Manifest

This manifest records which source artifacts were migrated into the context layout.

## Use this file to record

- source file name
- target file name
- status
- notes about sanitization

## Suggested table

| Source | Target | Status | Notes |
| --- | --- | --- | --- |
| `ANJELA_BOOT.md` | `docs/context/boot.md` | planned | sanitized public version |
| `ANJELA_PERSONALITY.md` | `docs/context/personality.md` | planned | sanitized public version |
| `ANJELA_MEMORY.md` | `docs/context/memory.md` | planned | sanitized public version |
| `PROJECT_HISTORY.md` | `docs/context/project-history.md` | planned | public-safe history |
| `ANJELA_ARCHIVE_INDEX.md` | `docs/context/archive-index.md` | planned | pointer-only index |

## Rule

If a source artifact cannot be made safe for public GitHub, keep the source private and note only the existence of the migration in this manifest.
