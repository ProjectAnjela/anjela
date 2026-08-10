# Anjela Memory

This file stores sanitized durable memory that the project can safely keep in Git.

## Confirmed project memory

```text
- [project] repo: ProjectAnjela/anjela
- [project] default_branch: main
- [project] public_context_root: docs/context
- [project] stack: Python, GitHub Actions, SQLite, OpenAI Responses API adapter
- [project] current_stage: MVP 0.2, with durable memory foundation
- [workflow] source_of_truth: current repository state, not stale chat history
- [workflow] safety_rule: do not store secrets, raw transcripts, or runtime databases in public Git
- [workflow] change_policy: keep workflow files stable unless a change is needed
- [archive] migration_thread: 6a79f2b8-5b88-83eb-9017-5c6acdefc4da | Migrate Anjela into GitHub context
```

## Keep here

- Stable project facts confirmed by repository content
- Durable workflow rules that help future maintenance
- Short archive pointers that do not expose sensitive content

## Do not keep here

- Secrets
- Raw conversation logs
- Personal data that should stay private
- Runtime database contents

## Maintenance rule

If a fact changes often, it probably does not belong in this file unless it is stored as a short-lived note with a clear review date.
