---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-27
CREATED_BY: Claude Chat (Blueprint Builder) — overnight session, Will asleep
PURPOSE: Paper trial of a RESEARCH task hitting the engine while workflow3 does NOT exist. Pins down what
  ACTUALLY happens (vs what docs/memory claim) and whether "RESEARCH fails silently" is accurate.
RUNS_AGAINST: 05_AI_LAYER/RESEARCH_ROUTE_SPEC.md + live WF1 (vOH1CsPYvD27sUxx) "Non-Ollama Handler" node
  (code read directly from the workflow JSON this session).
---

# PAPER TRIAL — RESEARCH TASK WITH NO WORKFLOW3

## SCENARIO (invented, realistic)
Will runs a Perplexity query about Zenfolio Advanced-plan upload concurrency (one of the real open
EVENTS verification items), saves the structured output to QUEUE/ as a RESEARCH task per the spec:
```json
{
  "task_id": "20260628-RES-001",
  "task_type": "RESEARCH",
  "topic": "Zenfolio Advanced concurrency",
  "prompt": "[Perplexity summary text...]",
  "priority": "NORMAL",
  "status": "PENDING",
  "source": "PERPLEXITY_MANUAL",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260628-RES-001_RESEARCH.md"
}
```
Two variants are walked: (A) the task as above, and (B) the same task with `"auto_research": true` added.

---

## WALKTHROUGH (against the ACTUAL live WF1 code, not just the spec)

**Live fact (read from WF1 JSON this session):** WF1's "Read Task" node sets
`route = 'RESEARCH'` for task_type RESEARCH, and the "Route?" IF node sends route!=OLLAMA to the
**"Non-Ollama Handler"** node. That node:
- writes `HANDOFFS/[task_id]_HANDOFF.json` (task_type=RESEARCH, escalation_reason="task_type=RESEARCH —
  direct handoff, no Perplexity integration active"),
- sets the QUEUE task status = ESCALATED,
- appends a row to DECISION_LOG.md (action=RESEARCH_HANDOFF, handler=CLAUDE).

**Variant A walkthrough:**
1. File lands in QUEUE/ → localFileTrigger fires (add event). ✅
2. Read Task: status=PENDING ✅, task_type=RESEARCH → route=RESEARCH, model=null. ✅
3. Route? → false branch → Non-Ollama Handler. ✅
4. Non-Ollama Handler writes HANDOFF, sets ESCALATED, logs DECISION_LOG. ✅
5. End. The HANDOFF sits in HANDOFFS/ until Claude/Antigravity reads it next session.

**FINDING (corrects the "fails silently" framing):** Variant A does **NOT** fail silently. It is
handled, logged, and visible in DECISION_LOG + HANDOFFS/. The task is correctly parked for human/Claude
pickup. This is *by design* per the spec (RESEARCH needing judgment → Claude). ✅ Working as intended.

**Variant B walkthrough (`auto_research: true`):**
1–3. Same as A — Read Task routes by task_type=RESEARCH **without ever inspecting `auto_research`.**
4. Non-Ollama Handler writes the SAME HANDOFF and ignores `auto_research` entirely.
5. End.

**FINDING (the REAL gap):** The `auto_research: true` field — which the spec says should trigger Tavily
auto-resolution — is **silently ignored** by the live WF1. There is no node that reads it, because WF3
(which owns Tavily) does not exist AND WF1's Non-Ollama Handler has no auto_research branch. So a caller
who sets `auto_research: true` expecting an automated Tavily answer instead gets a Claude HANDOFF with no
indication their flag did nothing. **THIS is the silent failure — not RESEARCH generally, but the
auto_research path specifically.** A user could drop 20 auto-research tasks expecting OUTPUTS and get 20
HANDOFFS, with DECISION_LOG falsely implying the handoff was the intended route.

---

## FAILURE MODES SURFACED

| # | Trigger | What docs/memory imply | What ACTUALLY happens | Severity |
|---|---------|------------------------|-----------------------|----------|
| 1 | Plain RESEARCH task, no WF3 | "RESEARCH fails silently" | Correctly HANDOFF'd + logged (works as designed) | NONE — framing was wrong |
| 2 | RESEARCH task with auto_research:true | Tavily auto-resolves → OUTPUTS | Flag ignored → Claude HANDOFF, no notice | **MEDIUM — real silent gap** |
| 3 | Tavily key present but unused | key is "active credential" | key sits in n8n_env.ps1 plaintext, never called; also a SECURITY exposure | LOW (fn) / HIGH (sec) |
| 4 | Many auto_research tasks dropped at once | each auto-resolves | each becomes a HANDOFF; HANDOFFS/ floods, no auto-answer | MEDIUM |

---

## GAPS + RECOMMENDATIONS
1. **Correct the "RESEARCH fails silently" note** in memory/handoffs. Accurate statement: *plain RESEARCH
   is handled correctly; the `auto_research:true` path is silently ignored until WF3 exists.* Precision
   matters — the current framing would send someone debugging the wrong thing.
2. **Until WF3 is built, make the ignored flag explicit, not silent.** Cheapest interim fix: add one line
   to WF1's Non-Ollama Handler that, if `auto_research === true`, writes the HANDOFF with
   escalation_reason = "auto_research requested but WF3/Tavily not yet built — escalated to Claude". Then
   DECISION_LOG tells the truth and no one is misled. (This is a tiny, low-risk WF1 code edit — but it IS
   a WF1 edit, so it should be done deliberately with Will, given WF1's import-corruption history. Do NOT
   do it as a drive-by.)
3. **WF3 build remains the real fix** (per RESEARCH_ROUTE_SPEC). When built, it owns the auto_research
   branch + Tavily call + retry. Prereq is only the Tavily key (no Docker) — but rotate the key FIRST
   (it's been sitting plaintext in vault-snapshot range; see standing CRITICAL_PATH item).
4. **Stranded-RESEARCH variant.** Same structural gap as all queue jobs: if a RESEARCH task is already in
   QUEUE at status≠PENDING, it never re-fires. A "requeue" helper (noted in HANDOFF_2026-06-28 obs #2)
   would cover this for RESEARCH too.

## OPEN QUESTIONS FOR WILL
- Q-RES1: Until WF3 exists, do you want the interim "explicit ignored-flag" line added to WF1 (recommend
  yes — turns a silent gap into an honest log), or leave WF1 untouched until WF3 is built wholesale?
- Q-RES2: When WF3 is built, should auto_research default to true or false on the job envelope? (Default
  true = engine tries Tavily first, escalates on failure = more autonomous but more web calls / cost.)
- Q-RES3: Should WF3 watch HANDOFFS/ for RESEARCH handoffs (per spec option A) or be called directly by
  WF1 via webhook (option B)? Option B avoids the HANDOFFS/ round-trip but couples the workflows.

## VERDICT
The headline finding overturns a stated assumption: **plain RESEARCH does not fail silently — it works.**
The genuine silent failure is narrow and specific: the `auto_research:true` flag is accepted by the job
envelope but read by nothing, so it no-ops without notice. This is low-effort to make honest (one log
line) and properly fixed only by building WF3. Residual risk: LOW for plain RESEARCH, MEDIUM for anyone
relying on auto_research before WF3 ships. Plus a standing HIGH security note: the Tavily key is in
plaintext for a feature that isn't even wired up yet — rotate it regardless of WF3 timing.

## CONNECTED FILES
- [[PAPER_TRIAL_RUNS|Paper Trial Runs]]
- [[RESEARCH_ROUTE_SPEC|Research Route Spec]]
- [[workflow1_queue_processor|Workflow 1 JSON]]
- [[JOB_ENVELOPE_SPEC|Job Envelope Spec]]
