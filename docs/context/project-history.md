# PROJECT_HISTORY.md

## Current canonical repository

**ProjectAnjela/anjela**

Current GitHub repository: `ProjectAnjela/anjela`

The repository is the canonical home for the Anjela software project. The ChatGPT/GitHub connection currently has access to this repository.

## Project idea

The archive shows a recurring goal: build Anjela as more than a prompt/persona — as a real software project with a portable context, tools, memory and integrations.

Earlier discussions used concepts such as:

- AI Operating System;
- portable AI context;
- memory repository;
- core/persona/communication/principles;
- workspace/projects/roadmap/ideas;
- prompts for different AI systems;
- Git-based versioning of AI context.

## Repository direction recovered from the archive

A proposed structure included:

```text
/
├── README.md
├── AI_OPERATING_SYSTEM.md
├── core/
│   ├── persona.md
│   ├── communication.md
│   ├── coding.md
│   └── principles.md
├── workspace/
│   ├── current-projects.md
│   ├── roadmap.md
│   └── ideas.md
├── memory/
│   ├── decisions.md
│   ├── preferences.md
│   └── timeline.md
├── prompts/
│   ├── chatgpt.md
│   ├── gemini.md
│   ├── claude.md
│   └── cursor.md
└── templates/
```

This is **historical design intent**, not a claim that all of these files currently exist.

## GitHub Actions history

The archive contains a concentrated sequence of conversations on 2026-08-08 around:

- choosing an Actions trigger;
- creating a workflow file;
- checking GitHub Actions;
- debugging Actions loading errors;
- deployment workflow;
- Docker/deployment direction.

A test workflow named **Deploy Anjela** was created and manually run successfully according to the conversation history. The user was then guided toward a future pipeline:

**project files → Docker → GitHub Actions → GHCR → server**

Treat that pipeline as planned/partially established, not as a guarantee that every component is currently present. Always inspect the current repository before changing architecture.

## GitHub integration history

The archive repeatedly records a `403 Resource not accessible by integration` error when trying to write to GitHub.

This is important historical context because it explains why some earlier assistant claims about creating files/Issues may have failed.

Current state should be verified against the actual GitHub connector/repository, not assumed from old chat.

## Project principles

1. GitHub is the source of truth for the actual current code.
2. Chat history is the source of truth for why a decision was discussed.
3. Do not assume a historical workflow still exists.
4. Before changing infrastructure, inspect the repository and current Actions configuration.
5. Prefer small, verifiable changes over a giant initial rewrite.
6. Keep the AI/personality layer separated from infrastructure and model-provider code.

## Migration relevance

The project repository is intentionally separate from the ChatGPT account. Therefore it should survive an account migration unchanged.

The new ChatGPT account should reconnect to GitHub and verify access to `ProjectAnjela/anjela`.

## Historical decision notes recovered from chats

### Portable context / AI Operating System
The project was repeatedly framed as a portable AI context rather than a single provider-specific prompt. The intent was to keep persona, communication rules, coding style, principles, memory, current projects, roadmap, ideas and provider-specific prompts under version control.

### Provider portability
The archive explicitly considered separate prompt/context entry points for systems such as ChatGPT, Gemini, Claude and Cursor. Treat these as portability design discussions, not proof that every integration was implemented.

### GitHub Actions
The user was guided through:
- selecting an Actions trigger;
- creating a workflow YAML;
- manually running the workflow;
- checking the Actions UI;
- diagnosing an Actions loading problem;
- thinking through a deployment path.

A successful manual test of a `Deploy Anjela` workflow was discussed in the archive. Verify current YAML before relying on that historical state.

### Permissions / 403
Several historical GitHub operations hit:
`403 Resource not accessible by integration`

This means historical assistant attempts to create/update repository content could fail even when the repository itself was visible. Do not infer write success from an old conversational claim. Verify the current connector permissions and repository state.

### Source-of-truth rule
- Current code/config: GitHub.
- Historical intent and rationale: conversation archive.
- User's stable communication preferences: migration memory/personality docs.
