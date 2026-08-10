# Anjela Context Index

This directory is the canonical place for sanitized, versioned context that helps the project stay coherent over time.

## What belongs here

- The short boot context for starting Anjela safely
- Personality and tone rules
- Sanitized durable memory summaries
- Project history and decisions
- Archive indexes and pointers to older conversations
- Migration notes, manifests, and templates

## What does not belong here

- API keys, tokens, cookies, or session state
- Raw private transcripts that should not be public
- Live local databases such as `anjela.db`
- Anything that would expose a private source, user data, or deployment secret

## Recommended structure

```text
docs/context/
├── README.md
├── boot.md
├── personality.md
├── memory.md
├── project-history.md
├── archive-index.md
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
6. The migration subfolder for source-to-target tracking

## Operating rule

If a fact is not confirmed by repository content or an approved archive, keep it out of the public repo or mark it as a placeholder.
