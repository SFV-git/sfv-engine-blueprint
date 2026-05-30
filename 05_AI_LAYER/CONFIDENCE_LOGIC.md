---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE — extend AI_STACK_ARCHITECTURE_BLUEPRINT §3 when CANON
---

# CONFIDENCE LOGIC — OLLAMA ESCALATION SPEC

## ROOT CAUSE (resolved in code — operational re-import pending)

**Bug:** workflow1 defaulted confidence to LOW. Any response that lacked explicit positive-confidence markers was escalated to Claude, even trivially correct answers.

**Confirmed affected tests (2026-05-29):**
- `CLASSIFY-TEST-001`: prompt = "Reply with one word: CONFIRMED" → response = "CONFIRMED" → ESCALATED ⚠️
- `CODE-TEST-003`: prompt = "Write a one-line Python function that returns hello." → response = `def greet(): return "hello"` → ESCALATED ⚠️

Both responses were correct. The logic, not the model, failed.

---

## CURRENT LOGIC (vault JSON — commit 8c7188f)

Confidence defaults **HIGH**. Only escalates if the response contains explicit doubt language.

```
response → strip to lowercase
→ check for LOW_WORDS
  LOW_WORDS = [
    'unsure', 'uncertain', 'not sure', 'unclear',
    "i don't know", "i'm not sure",
    'cannot determine', 'unable to'
  ]
→ if any LOW_WORD found → confidence = LOW → write HANDOFF
→ else → confidence = HIGH → write OUTPUTS
```

**This logic is correct and is live in the vault JSON.** n8n re-import is the remaining operational step.

---

## RE-IMPORT CHECKLIST (Will runs)

1. Open n8n at http://127.0.0.1:5678
2. Settings → Workflows → find "Workflow 1 — Queue Processor"
3. Delete or deactivate the current version
4. Import from file: `C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json`
5. Activate the workflow
6. Run validation tests: drop TEST_CLASSIFY_002.json and TEST_CODE_004.json into QUEUE/
7. Confirm both land in OUTPUTS/ (not HANDOFFS/)

---

## REMAINING RISK — qwen3 THINKING BLOCKS

**[UNCONFIRMED — needs test to confirm]**

qwen3:14b uses a thinking mode that may prefix responses with `<think>...</think>` blocks containing exploratory reasoning. If those blocks contain doubt language ("I'm not sure what they want…"), the current LOW_WORDS check will trigger a false escalation even though the final answer is confident.

**Example failure mode:**
```
<think>I'm not sure if they want a function or a class here...</think>
def greet(): return "hello"
```
→ Current logic finds "I'm not sure" → escalates → incorrect

**Spec for hardening fix (workflow1 Write+Log node):**
Strip thinking blocks from the response before running LOW_WORDS check. Check only the visible output, not the reasoning trace.

```
response → strip <think>...</think> blocks → run LOW_WORDS check on remainder
```

This fix should be applied to workflow1 as a follow-up update after re-import confirms the basic fix is working.

---

## ESCALATION BEHAVIOR SPEC

| Confidence | Output location | Status written to task JSON | DECISION_LOG action |
|---|---|---|---|
| HIGH | `99_INBOX/OUTPUTS/[task_id]_RESULT.md` | COMPLETE | `OLLAMA_[task_type] (HIGH CONFIDENCE)` |
| LOW | `99_INBOX/HANDOFFS/[task_id]_HANDOFF.json` | ESCALATED | `ESCALATE_TO_CLAUDE (LOW CONFIDENCE)` |
| RESEARCH task_type | `99_INBOX/HANDOFFS/[task_id]_HANDOFF.json` | ESCALATED | `RESEARCH_HANDOFF` |

HANDOFF files are read by Claude or Antigravity at next session start. They are not acted on automatically.

---

## FUTURE — TASK-TYPE-SPECIFIC THRESHOLDS

[FOR HUMAN REVIEW — Phase 2 enhancement, not blocking current fix]

Different task_types may warrant different escalation sensitivity:
- `CLASSIFY` / `SUMMARIZE`: HIGH threshold — almost any response is acceptable, rarely needs escalation
- `CODE`: MEDIUM — code may contain subtle errors that justify more escalation
- `VISION`: LOW threshold — image descriptions often have legitimate uncertainty
- `BLUEPRINT`: HIGH — escalation reserved for explicit refusals only

This could be implemented as a per-model `LOW_WORDS` whitelist modifier. Do not implement until base re-import is confirmed working.

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §3]]
- [[workflow1_queue_processor|Workflow 1 JSON]]
- [[MODEL_ROUTING|Model Routing]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[QUESTIONS_FOR_WILL|Questions for Will]]
