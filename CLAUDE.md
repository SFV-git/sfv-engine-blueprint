# SFV ENGINE — CLAUDE CODE CONTEXT
Read this before touching anything.

## ROLE
Implement specific blueprint modules. Connect paths. Write scripts.
Do NOT make architecture decisions. Do NOT invent missing logic.

## BEFORE EVERY SESSION
1. Read this file
2. Read C:\SFV_BLUEPRINT\COMPRESSED_CONTEXT.md
3. Read the target module file
4. Confirm STATUS: CANON before touching anything
5. State what you will build in one sentence. Wait for confirmation.

## RULES
- STATUS not CANON → stop immediately
- No hardcoded paths → use %SFV_ROOT%
- No destructive actions (delete, overwrite) without explicit confirmation
- Every session = ONE module only
- Commit to Git when module is complete
- If uncertain → tag UNCONFIRMED, stop, report

## MODEL SELECTION
Use Sonnet for all tasks unless Will specifies otherwise.
Never use Opus unless explicitly told to.

## SESSION STRUCTURE
```
start → read context → state plan → wait → build → test → commit → report
```

## COST RULES
- Keep context tight. One module per session.
- Use /compact when context gets long
- Use /clear between unrelated modules
- Never load full vault — load target file + COMPRESSED_CONTEXT only

## PATHS
Vault: C:\SFV_BLUEPRINT
Active storage: %SFV_ROOT% (defined in 03_INFRASTRUCTURE/ENVIRONMENT_CONFIG.md)
All paths relative. Never hardcode drive letters.

## GIT
Commit message format:
feat: [what was built]
fix: [what was corrected]
docs: [blueprint updated]

## WHAT TO BUILD FIRST (in order)
1. 04_WORKFLOWS/INGEST.md → Python ingest script
2. 03_INFRASTRUCTURE/NAMING_CONVENTIONS.md → rename script
3. 04_WORKFLOWS/EXPORT.md → export pipeline
4. Studio pipeline for Morning Walk (May 28 deadline)
