# Anjela Memory

This file is for sanitized durable memory that the project can safely keep in Git.

## Keep here

- Stable user preferences that are safe to publish
- Long-lived project facts confirmed by repository content
- Durable workflow rules that help future maintenance

## Do not keep here

- Secrets
- Raw conversation logs
- Personal data that should stay private
- Runtime database contents

## Suggested format

```text
- [category] key: value
```

## Example categories

- `identity`
- `workflow`
- `project`
- `preference`
- `archive`

## Maintenance rule

If a fact changes often, it probably does not belong in this file unless it is stored as a short-lived note with a clear review date.
