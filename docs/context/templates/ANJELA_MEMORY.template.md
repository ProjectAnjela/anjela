# ANJELA_MEMORY

## Purpose

This file stores safe, durable memory that can live in a public repository.

## Allowed entries

- `[identity]` stable public identity facts
- `[project]` repository-confirmed project facts
- `[workflow]` durable operating rules
- `[preference]` safe user preferences
- `[archive]` approved archive pointers

## Entry format

```text
- [category] key: value
```

## Safety rules

- Do not store secrets
- Do not store raw conversation logs
- Do not store private personal data
- Keep volatile runtime state out of Git

## Maintenance

- Keep facts short
- Remove anything that stops being public-safe
- Update the file only when the new information is confirmed
