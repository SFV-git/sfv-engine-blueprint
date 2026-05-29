---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# CLAUDE CODE PROMPTS — OPTIMIZED

## STANDARD SESSION OPENER
Copy this at the start of every Claude Code session:
```
Read CLAUDE.md and COMPRESSED_CONTEXT.md first.
Target module: [MODULE FILE PATH]
Confirm STATUS: CANON then state your build plan in one sentence.
Wait for my go-ahead before writing any code.
Model: Sonnet. One module only this session.
```

## MODULE BRIEF TEMPLATE
```
Module: [name]
File: C:\SFV_BLUEPRINT\[path]
Build: [exact script/file to create]
Input: [what it reads]
Output: [what it produces]
Must not: [what it cannot touch]
Success looks like: [one sentence]
```

## PARALLEL INSTANCE OPENER (overnight)
```
You are instance [N] of [TOTAL] running in parallel.
Your job only: [specific task]
Do not touch any files outside: [specific folder]
Read COMPRESSED_CONTEXT.md for system context.
Use Sonnet. Commit when done. Report completion.
```

## MID-SESSION COMMANDS
/compact → compress context when it gets long
/clear → fresh context between unrelated tasks
/model claude-sonnet-4-6 → set model explicitly
/cost → check session token usage

## END OF SESSION CHECKLIST
```
[ ] Module complete
[ ] Tests passed (or paper trial done)
[ ] Git committed with descriptive message
[ ] CHANGELOG.md updated
[ ] VERSION_LOG.md updated if milestone hit
[ ] SESSION_STATE.md updated with what was built
```

## CONNECTED FILES
- [[CLAUDE|CLAUDE.md]]
- [[COMPRESSED_CONTEXT|COMPRESSED_CONTEXT.md]]
- [[CHANGELOG|CHANGELOG.md]]
- [[VERSION_LOG|VERSION_LOG.md]]
- [[SESSION_STATE|SESSION_STATE.md]]
- [[COST_ROUTING|Cost Routing]]
- [[RATE_LIMITS|Rate Limits]]
