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

## Current mapping

| Source | Target | Status | Notes |
| --- | --- | --- | --- |
| `ANJELA_BOOT.md` | `docs/context/boot.md` | confirmed | imported from the migration pack |
| `ANJELA_PERSONALITY.md` | `docs/context/personality.md` | confirmed | imported from the migration pack |
| `ANJELA_MEMORY.md` | `docs/context/memory.md` | confirmed | imported from the migration pack |
| `PROJECT_HISTORY.md` | `docs/context/project-history.md` | confirmed | imported from the migration pack |
| `ANJELA_ARCHIVE_INDEX.md` | `docs/context/archive-index.md` | confirmed | imported from the migration pack |
| `MIGRATION_MANIFEST.md` | `docs/context/migration/manifest.md` | confirmed | this manifest documents the imported pack |
| `ANJELA_MIGRATION_PACK.md` | `docs/context/migration/pack.md` | confirmed | imported package overview |

## Rule

If a source artifact cannot be made safe for public GitHub, mark it `private` and keep the source outside the public repository. If it becomes safe later, move it to `draft` first and then `confirmed` after review.
