---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-27
CREATED_BY: Antigravity
MERGE_INTO: STANDALONE — referenced by HERMES_INTEGRATION.md and autonomous loop docs
---

# DIRECTIVE TEMPLATE — CURRENT_DIRECTIVE.md SCHEMA

> This document defines the canonical schema for `CURRENT_DIRECTIVE.md`.
> That file is the single input Will writes to drive autonomous build sessions.
> Hermes reads it, spawns `claude -p`, and manages the loop until the directive is complete.
> Will writes one directive per phase. That is the full extent of Will's input per session.

---

## HOW TO USE THIS

1. Copy the FULL TEMPLATE below
2. Save it as `C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md` (overwriting the previous one)
3. Hermes detects the file change and fires the first `claude -p` automatically
4. You are done until a HANDOFF or PHASE_COMPLETE notification arrives

---

## FULL TEMPLATE

```markdown
---
DIRECTIVE_ID: DIR-YYYYMMDD-NNN
CREATED: YYYY-MM-DDTHH:MM:SS
CREATED_BY: WILL
STATUS: ACTIVE
VERSION: v1.0
---

# CURRENT DIRECTIVE

## OBJECTIVE
<!-- One paragraph. What should exist at the end of this directive that doesn't exist now?
     Be concrete. Bad: "improve the system". Good: "WF4 process.env bug is fixed, re-imported,
     tested with TEST_CLASSIFY_002, result confirmed in OUTPUTS/." -->


## SCOPE BOUNDS
<!-- What Claude Code IS allowed to touch during this directive. Be explicit. -->
ALLOWED:
- [ ] Edit files in: [list specific directories or files]
- [ ] Run commands: [list specific commands allowed]
- [ ] Create new files in: [list directories]

NOT ALLOWED (do not touch):
- [ ] [list explicitly forbidden files/directories]
- [ ] Do not promote anything to STATUS: CANON — DRAFT only
- [ ] Do not push to Git — Will pushes manually

## SUCCESS CRITERIA
<!-- How will we know this directive is DONE? Must be testable.
     Claude Code writes STEP_RESULTS/DIR-YYYYMMDD-NNN_COMPLETE.md when all criteria pass. -->
- [ ] [Criterion 1 — specific, checkable]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] SESSION_STATE.md updated with what was done
- [ ] CHANGELOG.md entry added

## HUMAN GATE TRIGGERS
<!-- If any of these are encountered, STOP immediately.
     Write HANDOFFS/DIR-YYYYMMDD-NNN_GATE_NNN.md and wait for Will.
     Do not guess or proceed. -->
- Any decision that requires Will's taste or creative judgment
- Any conflict with CANON docs that isn't clearly resolvable
- API cost alert in COST_ALERTS.md
- Unexpected file not in scope bounds
- Any action that would delete or overwrite more than 3 files
- [Add directive-specific gates here]

## CONTEXT FILES TO READ FIRST
<!-- Claude Code reads these before doing anything else. -->
- C:\SFV_BLUEPRINT\SESSION_STATE.md
- C:\SFV_BLUEPRINT\COMPRESSED_CONTEXT.md
- C:\SFV_BLUEPRINT\00_DEV_LOG\CRITICAL_PATH.md
- C:\SFV_BLUEPRINT\99_INBOX\COST_ALERTS.md
- [Add directive-specific context files here]

## MAX TURNS
<!-- Hard cap on claude -p --max-turns. Prevents runaway sessions.
     Most directives: 20-40 turns. Complex multi-step builds: up to 60. -->
MAX_TURNS: 30

## MAX BUDGET
<!-- Hard cap on claude -p --max-budget-usd. Prevents runaway spend. -->
MAX_BUDGET_USD: 2.00

## OUTPUT LOCATION
<!-- Where Claude Code writes its primary output for this directive. -->
STEP_RESULTS: C:\SFV_BLUEPRINT\STEP_RESULTS\DIR-YYYYMMDD-NNN\
COMPLETION_FILE: C:\SFV_BLUEPRINT\STEP_RESULTS\DIR-YYYYMMDD-NNN_COMPLETE.md

## NOTES FOR CLAUDE CODE
<!-- Anything Claude Code should know that isn't in the scope or criteria.
     Relevant history, known pitfalls, order of operations, etc. -->

```

---

## FIELD REFERENCE

### DIRECTIVE_ID
Format: `DIR-YYYYMMDD-NNN` where NNN is a sequential number per day.
Example: `DIR-20260627-001`
Used as the key that Hermes and Claude Code use to track this session across turns.

### STATUS values
| Status | Set by | Meaning |
|--------|--------|---------|
| `ACTIVE` | Will | Hermes fires on this status |
| `IN_PROGRESS` | Hermes | Loop is running — do not overwrite |
| `COMPLETE` | Hermes/Claude Code | All success criteria passed |
| `HUMAN_GATE` | Claude Code | Waiting for Will input |
| `PAUSED` | Will | Deliberately paused mid-run |
| `REJECTED` | Will | Directive cancelled — write reason |

### SCOPE BOUNDS — why this exists
Claude Code is powerful and will try to be helpful beyond its instructions.
A tight SCOPE_BOUNDS list prevents:
- Touching docs in a build phase that should only be touched in a design phase
- Resolving ambiguity by making a decision that should be Will's
- Creating new docs that dilute the vault

**Rule:** If it's not explicitly in ALLOWED, Claude Code must write a HANDOFF and wait.

### SUCCESS CRITERIA — format
Each criterion should be checkable by running a command or reading a file.
Bad: "the bug is fixed"
Good: "TEST_CLASSIFY_002.json dropped in QUEUE/ lands in OUTPUTS/ with status COMPLETE"

### HUMAN GATE TRIGGERS — the most important section
This is the enforcement mechanism for Rule 07 (Blueprint Before Build) and Rule 03 (Human Taste Is Final).
These are non-negotiable. Claude Code MUST stop and write a HANDOFF if any trigger fires.
Hermes delivers the HANDOFF notification to Will's phone.

### MAX_TURNS and MAX_BUDGET_USD
These are passed directly to `claude -p --max-turns N --max-budget-usd N`.
They are hard stops enforced by the Anthropic SDK — not guidelines.
If a directive needs more turns than the cap, it should be split into two directives.

---

## WORKED EXAMPLE — REAL DIRECTIVE

```markdown
---
DIRECTIVE_ID: DIR-20260628-001
CREATED: 2026-06-28T09:00:00
CREATED_BY: WILL
STATUS: ACTIVE
VERSION: v1.0
---

# CURRENT DIRECTIVE

## OBJECTIVE
Fix the WF4 process.env bug in n8n. The "Guard — DECISION_LOG only" Code node in WF4
uses `process.env` which is blocked by n8n task-runner sandbox. Replace with `$env`
expressions. Re-import the fixed workflow JSON, re-activate, publish, verify no errors.
Then update HANDOFF_2026-06-27.md to mark this item resolved.

## SCOPE BOUNDS
ALLOWED:
- [ ] Edit: C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow4_output_monitor.json
- [ ] Edit: C:\SFV_BLUEPRINT\00_DEV_LOG\HANDOFF_2026-06-27.md (mark WF4 item resolved)
- [ ] Run: n8n workflow import commands
- [ ] Create: STEP_RESULTS\DIR-20260628-001\ files

NOT ALLOWED:
- [ ] Do not touch workflow1 or workflow2
- [ ] Do not promote anything to CANON
- [ ] Do not push to Git

## SUCCESS CRITERIA
- [ ] WF4 JSON has no process.env references (grep confirms zero matches)
- [ ] WF4 re-imported into n8n, active, published
- [ ] n8n execution log for WF4 shows no ReferenceError
- [ ] HANDOFF_2026-06-27.md WF4 item marked [RESOLVED]
- [ ] SESSION_STATE.md updated
- [ ] CHANGELOG.md entry added

## HUMAN GATE TRIGGERS
- Any n8n import error that isn't clearly a UTF-8 BOM issue
- If WF4 logic change requires understanding business rules I don't have
- API cost reaches $1.50

## CONTEXT FILES TO READ FIRST
- C:\SFV_BLUEPRINT\SESSION_STATE.md
- C:\SFV_BLUEPRINT\COMPRESSED_CONTEXT.md
- C:\SFV_BLUEPRINT\00_DEV_LOG\HANDOFF_2026-06-27.md

## MAX TURNS
MAX_TURNS: 20

## MAX BUDGET
MAX_BUDGET_USD: 1.50

## OUTPUT LOCATION
STEP_RESULTS: C:\SFV_BLUEPRINT\STEP_RESULTS\DIR-20260628-001\
COMPLETION_FILE: C:\SFV_BLUEPRINT\STEP_RESULTS\DIR-20260628-001_COMPLETE.md

## NOTES FOR CLAUDE CODE
- n8n runs at http://127.0.0.1:5678
- Workflow IDs: WF4 = nRbwsa0K62y2Fnmo
- The process.env fix is simple: replace process.env.VAULT_PATH with $env.VAULT_PATH
  (n8n expression syntax, not JavaScript). Check all nodes in WF4, not just the Guard node.
- After re-import: activate + publish via n8n UI or API. Don't just import and leave unpublished
  (that was the original bug that caused WF1/WF4 to not fire).
```

---

## RULES FOR AUTONOMOUS LOOP (HERMES INTEGRATION)

These rules apply whenever a `CURRENT_DIRECTIVE.md` is ACTIVE and Hermes is running:

1. **One directive at a time.** Hermes does not process a new CURRENT_DIRECTIVE.md while STATUS is IN_PROGRESS.
2. **CANON is locked during autonomous runs.** Claude Code may write DRAFT-status docs only. Will promotes to CANON.
3. **Git branch before session.** Hermes creates a timestamped git branch before spawning the first `claude -p`. Rollback path is always available.
4. **HANDOFF is a pause, not a failure.** When Claude Code writes a HANDOFF, Hermes pauses the loop and pings Will. The session resumes after Will responds.
5. **Review every 3-5 steps.** Hermes spawns a read-only `claude -p` review pass every 3-5 steps. The review checks for drift vs. the directive and writes REVIEW_NNN.md. No changes made during review pass.
6. **Cost gate.** Before spawning any `claude -p`, Hermes checks COST_ALERTS.md. If an unresolved alert is present and the remaining budget is below $0.50, Hermes pauses and pings Will instead of firing.

---

## CONNECTED FILES
- [[CURRENT_DIRECTIVE|Current Directive]]
- [[HERMES_INTEGRATION|Hermes Integration]]
- [[SESSION_STATE|Session State]]
- [[CHANGELOG|Changelog]]
- [[CRITICAL_PATH|Critical Path]]
- [[COST_ALERTS|Cost Alerts]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
