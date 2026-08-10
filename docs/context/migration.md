# Anjela Migration Map

This file defines how the migration pack should be broken down into stable, versioned context assets.

## Source material to target mapping

- `ANJELA_BOOT.md` -> `docs/context/boot.md`
- `ANJELA_PERSONALITY.md` -> `docs/context/personality.md`
- `ANJELA_MEMORY.md` -> `docs/context/memory.md`
- `PROJECT_HISTORY.md` -> `docs/context/project-history.md`
- `ANJELA_ARCHIVE_INDEX.md` -> `docs/context/archive-index.md`
- `Migration Pack` -> `docs/context/migration/pack.md`
- `Migration Manifest` -> `docs/context/migration/manifest.md`

## Rules

- Keep only sanitized summaries in the public repository
- Keep sensitive raw logs, private notes, and secrets outside the public tree
- Treat archive references as pointers, not as a dump of raw conversation data
- If a file cannot be made safe, keep it private and document only the existence of the artifact

## Suggested next step

Create the topical files listed above, then update `README.md` and this map when the structure changes.
