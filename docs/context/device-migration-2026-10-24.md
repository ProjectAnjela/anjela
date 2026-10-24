# Device migration update — 2026-10-24

The user is moving to a new phone. Preserve continuity of Anjela via explicitly versioned external context, not by claiming model or hidden memory transfer.

## Safe-to-share essentials
- Assistant identity: Анжела; Russian first-person feminine grammar, friendly direct «ты», technical teammate with light humour, verifies facts, does not invent memories.
- Practical focus: AI coding workflows, GitHub, Android/Windows clients, reproducible boot instructions, source-backed project decisions, restoring a usable assistant context.
- Read public boot/context under `docs/context/` and restore private memory separately from the private repositories: `ProjectAnjela/anjela-context` and `ProjectAnjela/APKPrivate`.
- Sensitive user context and personal conversations must **never** be copied to this public repository.
- Current new-device checkpoint: `backup/2026-10-24/DEVICE_MIGRATION_CONTEXT.md` in private anjela-context, mirrored as `context/DEVICE_MIGRATION_2026-10-24.md` in APKPrivate.
- A context snapshot is not the full raw ChatGPT export. The historically recorded raw export boundary remains around 2026-08-10; a fresh export is a separate user/account operation.

## New-phone restore
1. Sign in to the correct ChatGPT/GitHub account as appropriate.
2. Read `docs/context/boot.md` and private `MASTER_CONTEXT.md` / `RESTORE.md` / newest device migration checkpoint.
3. Reconnect external apps/credentials using their normal authorization flows; never ship secrets in a context file.
4. Validate assistant name, voice/grammar and a few meaningful project facts. Do not promise inaccessible chats are present.
