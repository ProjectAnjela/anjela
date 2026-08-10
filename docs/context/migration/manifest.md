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
| verified repository state | `docs/context/boot.md` | confirmed | startup context populated from the live repo state |
| verified repository state | `docs/context/personality.md` | confirmed | public-facing style populated from current project guidance |
| verified repository state | `docs/context/memory.md` | confirmed | durable project memory populated with safe facts |
| verified repository state | `docs/context/project-history.md` | confirmed | milestones recorded from current repository content |
| migration thread archive | `docs/context/archive-index.md` | confirmed | archive pointer recorded without raw transcript data |
| public-safe context pack | `docs/context/migration/pack.md` | confirmed | package contents documented |
| public-safe migration guide | `docs/context/migration/README.md` | confirmed | folder usage documented |

## Rule

If a source artifact cannot be made safe for public GitHub, mark it `private` and keep the source outside the public repository. If it becomes safe later, move it to `draft` first and then `confirmed` after review.
