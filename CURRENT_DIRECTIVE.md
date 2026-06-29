---
STATUS: ACTIVE
DIRECTIVE_ID: DIR-20260628-OVERNIGHT-001
CREATED: 2026-06-28
CREATED_BY: Will (via Claude Chat)
PURPOSE: First full end-to-end test of the Hermes autonomous loop. Evaluate system effectiveness.
---

# OVERNIGHT DIRECTIVE — SYSTEM TEST RUN

## OBJECTIVE
Execute four tasks against the live vault. Produce clean outputs. Ping Will on completion or if blocked.
This is a test of the loop — not just the outputs. Note anything that feels broken, slow, or uncertain.

## ALLOWED
- Read any vault file
- Write to 99_INBOX/OUTPUTS/
- Write to 00_DEV_LOG/HANDOFF_2026-06-28_OVERNIGHT.md
- Edit QUESTIONS_FOR_WILL.md (draft answers only, no deletions)
- Edit TOOL_STATUS.md (update statuses to reflect current reality)
- Create files in 99_INBOX/OUTPUTS/
- Spawn Claude Code for multi-file vault work
- Send Telegram messages to Will

## NOT ALLOWED
- Promote anything to CANON
- Touch n8n workflows or any live running service
- Delete any existing vault file
- Spend more than $8.00 Claude API
- Make any architectural decisions without a HANDOFF

## MAX_TURNS: 80
## MAX_BUDGET_USD: 8.00

## CONTEXT FILES TO READ FIRST
- SESSION_STATE.md
- COMPRESSED_CONTEXT.md
- DASHBOARD.md
- 00_DEV_LOG/QUESTIONS_FOR_WILL.md

## TASKS (in order)

### TASK 1 — FOR_HUMAN_REVIEW Audit
Read every file in FOR_HUMAN_REVIEW/.
Write: 99_INBOX/OUTPUTS/OVERNIGHT_001_FHR_AUDIT.md
Content: one table — doc name, what decision Will needs to make, recommended action, urgency (HIGH/MED/LOW).

### TASK 2 — WF3 Research Handler Blueprint
Write a full blueprint for the missing WF3 RESEARCH n8n workflow.
Model it on how WF1 works (read 03_INFRASTRUCTURE/n8n_workflows/ for reference).
Write: 99_INBOX/OUTPUTS/OVERNIGHT_002_WF3_BLUEPRINT.md
Status: FOR HUMAN REVIEW. No building — blueprint only.

### TASK 3 — TOOL_STATUS.md Update
Read TOOL_STATUS.md. Compare against actual known state from SESSION_STATE.md and HERMES_EVAL.md.
Update statuses in-file to reflect reality as of 2026-06-28.
(e.g. Hermes → ACTIVE, Ollama qwen3:14b → ACTIVE, Tailscale → ACTIVE, n8n → ACTIVE, etc.)
Label your changes with [UPDATED 2026-06-28] inline.

### TASK 4 — QUESTIONS_FOR_WILL Draft Answers
Read 00_DEV_LOG/QUESTIONS_FOR_WILL.md.
For each open question: draft a recommended answer based on vault context.
Append drafts below each question as > DRAFT ANSWER: [answer] (FOR HUMAN REVIEW).
Do not delete or modify the original questions.

## SUCCESS CRITERIA
- [ ] OVERNIGHT_001_FHR_AUDIT.md exists in OUTPUTS with at least one table row per FHR doc
- [ ] OVERNIGHT_002_WF3_BLUEPRINT.md exists in OUTPUTS with a complete workflow spec
- [ ] TOOL_STATUS.md updated with [UPDATED 2026-06-28] tags on changed rows
- [ ] QUESTIONS_FOR_WILL.md has DRAFT ANSWER blocks appended to open questions
- [ ] Telegram ping sent to Will on completion

## HUMAN_GATE_TRIGGERS
- Any task requires touching a live service
- Any task requires an architectural decision not answerable from vault context
- Claude API spend approaches $6.00
- Any success criterion looks impossible to meet cleanly

## COMPLETION
When all four tasks done, write:
99_INBOX/OUTPUTS/OVERNIGHT_001_COMPLETE.md
Content: what was done, what was skipped and why, anything Will should look at first, honest assessment of where the loop felt smooth vs rough.
Then ping Will on Telegram: "Overnight test run complete. Check OUTPUTS. Summary in OVERNIGHT_001_COMPLETE.md"
