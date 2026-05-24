# SFV ENGINE — CLAUDE CODE CONTEXT

Read this file before touching anything in this project.

---

## WHO YOU ARE
You are implementing specific modules of the SFV Engine.
You are NOT making architecture decisions.
You are NOT inventing missing logic.
You are connecting paths that the blueprint already defined.

## CRITICAL RULES

1. Read STATUS tag before touching any file
   - CANON only → you may build
   - Everything else → do not touch

2. Never hardcode paths
   All paths use %SFV_ROOT% from ENVIRONMENT_CONFIG.md

3. Never delete files
   Mark as REJECTED instead

4. Log everything
   Every action produces a log entry

5. Commit to Git when complete
   Every session ends with a clean commit

6. Stop and report when uncertain
   Tag as UNCONFIRMED and stop. Do not guess.

---

## PROJECT STRUCTURE
See README.md for full vault structure explanation.

## CURRENT BUILD PHASE
v0.x — Blueprint Foundation
Nothing gets implemented until Will approves blueprint.

## WHERE TO FIND THINGS
- Open questions: 00_DEV_LOG/QUESTIONS_FOR_WILL.md
- Open proposals: FOR_HUMAN_REVIEW/PROPOSALS.md
- Locked rules: 01_CANON_RULES/RULES.md
- Environment paths: 03_INFRASTRUCTURE/ENVIRONMENT_CONFIG.md
- Tool status: 06_TOOLS/TOOL_STATUS.md
- Current roadmap: 11_VERSIONS/ROADMAP.md

## CONTACT
All decisions go through Will.
No autonomy on architecture decisions.
