# Anjela Context Index

This directory is the canonical index for sanitized migration records, templates, and archive catalogs that help the project stay coherent over time. Distributable runtime context lives in `src/anjela/context/` so a normal wheel installation can load it without a source checkout.

## What belongs here

- Migration notes, manifests, and templates
- Archive catalogs and pointers to older conversations
- Device migration notes

The short boot context, personality rules, sanitized memory summary, project history, and runtime archive index belong in `src/anjela/context/`.

## What does not belong here

- API keys, tokens, cookies, or session state
- Raw private transcripts that should not be public
- Live local databases such as `anjela.db`
- Anything that would expose a private source, user data, or deployment secret

## Recommended structure

```text
src/anjela/context/
├── boot.md
├── personality.md
├── memory.md
├── project-history.md
└── archive-index.md

docs/context/
├── README.md
├── archive/
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
5. The runtime files under `src/anjela/context/` for the actual working context
6. The migration subfolder for source-to-target tracking

## Status

The packaged runtime context and this migration index are populated with real public-safe content, not placeholders.

## Operating rule

If a fact is not confirmed by repository content or an approved archive, keep it out of the public repo or mark it as a placeholder.
