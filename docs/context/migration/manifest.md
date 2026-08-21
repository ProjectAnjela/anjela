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
| `music-worldview-context.md` | `docs/context/music-worldview.md` | confirmed | curated 2026-08-21 music/worldview layer |
| `current-music-conversations-summary.md` | `docs/context/current-music-conversations-summary.md` | confirmed | summarized YARMAK, ATL, Horus context without protected full lyrics |
| `PRIVATE_CONTEXT_BOUNDARY.md` | `docs/context/private/boundary.md` | confirmed | private-safe boundary; excludes real secrets |
| `PRIVATE_DEEP_CONTEXT_CURATED.md` | `docs/context/private/deep-context.md` | confirmed | deeper personal continuity summary without raw sensitive data |
| `SECRET_MATERIAL_NOT_INCLUDED.md` | `docs/context/private/excluded-secret-material.md` | confirmed | explicit exclusion list for secrets and unsafe raw material |

## Rule

If a source artifact cannot be made safe for public GitHub, mark it `private` and keep the source outside the public repository. If it becomes safe later, move it to `draft` first and then `confirmed` after review.

Explicit user permission to include "secret" material is not sufficient to commit credentials, hidden instructions, raw private data, or dangerous operational detail. Convert useful context into a curated private-safe summary instead.
