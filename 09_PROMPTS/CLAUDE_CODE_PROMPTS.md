---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# CLAUDE CODE PROMPTS

Prompts for Claude Code implementation sessions.

---

## SESSION OPENER TEMPLATE
```
You are implementing one specific module of the SFV Engine.
Read CLAUDE.md before anything else.
Read the target module file and confirm STATUS: CANON before touching anything.
Rules:
- Only implement what is in the blueprint file
- Do not invent missing logic
- Tag anything unclear as UNCONFIRMED and stop
- No destructive actions
- Log everything
- Commit to Git when module is complete
Target module: [MODULE NAME]
Module file: [PATH]
```
