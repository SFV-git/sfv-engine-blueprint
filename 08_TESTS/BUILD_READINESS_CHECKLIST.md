---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# BUILD READINESS CHECKLIST

Before any module gets built by Claude Code,
every item on this list must be checked.

---

## BLUEPRINT READINESS
[ ] Module has STATUS: CANON
[ ] All paths use %SFV_ROOT% (no hardcoded paths)
[ ] Input path defined
[ ] Output path defined
[ ] Failure behavior defined
[ ] Paper trial run completed
[ ] No UNCONFIRMED items blocking this module
[ ] Claude Code brief written for this module specifically

## ENVIRONMENT READINESS
[ ] Python installed and working
[ ] Git initialized
[ ] %SFV_ROOT% set in environment
[ ] ENVIRONMENT_CONFIG.md has all required paths
[ ] Drive labels confirmed and drives physically labeled

## DEPENDENCY READINESS
[ ] All tools this module needs are INSTALLED in TOOL_STATUS
[ ] No module this depends on has UNCONFIRMED status
[ ] Database schema ready if module writes to database

## SAFETY CHECKS
[ ] No destructive actions (delete, overwrite) without explicit confirmation
[ ] Logs enabled for this module
[ ] Failure behavior tested on paper
[ ] Rollback possible via Git if something goes wrong

## CONNECTED FILES
- [[ENVIRONMENT_CONFIG|Environment Config]]
- [[TOOL_STATUS|Tool Status]]
- [[UNCONFIRMED|Unconfirmed Items]]
- [[DATABANK_ARCHITECTURE|Databank Architecture]]
- [[VERSION_LOG|Version Log]]
