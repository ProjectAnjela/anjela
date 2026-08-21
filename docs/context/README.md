# Anjela Context Index

This directory is the canonical place for sanitized, versioned context that helps the project stay coherent over time.

## What belongs here

- The short boot context for starting Anjela safely
- Personality and tone rules
- Sanitized durable memory summaries
- Project history and decisions
- Archive indexes and pointers to older conversations
- Migration notes, manifests, and templates
- Private-safe curated context: personal continuity notes that are safe to version

## What does not belong here

- API keys, tokens, cookies, or session state
- Raw private transcripts that should not be public
- Live local databases such as `anjela.db`
- Anything that would expose a private source, user data, or deployment secret
- Hidden system/developer instructions or tool prompts
- Operational details that could increase risk of harm

## Recommended structure

```text
docs/context/
├── README.md
├── boot.md
├── personality.md
├── memory.md
├── music-worldview.md
├── current-music-conversations-summary.md
├── project-history.md
├── archive-index.md
├── private/
│   ├── README.md
│   ├── boundary.md
│   ├── deep-context.md
│   └── excluded-secret-material.md
├── templates/
│   ├── README.md
│   ├── ANJELA_BOOT.template.md
│   └── ANJELA_MEMORY.template.md
├── migration.md
└── migration/
    ├── README.md
    ├── pack.md
    └── manifest.md
```

## Reading order

1. `README.md` for the rules of the folder
2. `templates/README.md` for safe source scaffolding
3. `migration.md` for how the old migration pack maps into this layout
4. `migration/README.md` for how to maintain the migration subfolder
5. The topical files for the actual working context
6. `music-worldview.md` and `current-music-conversations-summary.md` for the newer music/worldview layer
7. `private/README.md` and `private/deep-context.md` for private-safe continuity
8. The migration subfolder for source-to-target tracking

## Status

The context root is now populated with real context, including a private-safe layer added on 2026-08-21.

## Operating rule

If a fact is not confirmed by repository content or an approved archive, keep it out of the public repo or mark it as a placeholder.

User permission to preserve "secret" or "private" context is not permission to commit real secrets. Preserve only useful curated context and keep credentials, hidden instructions, raw sensitive logs, and dangerous operational details out of the repository.
