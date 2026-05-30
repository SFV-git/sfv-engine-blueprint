---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# RESEARCH ROUTE SPEC

> Defines how RESEARCH task_type is handled, the role split between Tavily and Perplexity,
> and the spec for workflow3 (pending D3 decision).

---

## CONFIRMED ROLE SPLIT (D7 — confirmed 2026-05-29)

| Tool | Role | Entry point |
|---|---|---|
| **Tavily** | Automated web search inside n8n — called by workflow nodes when a task needs live web data | n8n HTTP Request node → Tavily API |
| **Perplexity** | Manual research intake — Will runs a Perplexity query, outputs structured file to QUEUE/ | Will → Perplexity → file drop to QUEUE/ |

These are complementary, not redundant. Tavily is machine-triggered. Perplexity is human-triggered.

---

## CURRENT RESEARCH ROUTE BEHAVIOR (workflow1)

Tasks with `task_type: "RESEARCH"` bypass Ollama entirely. workflow1 writes them directly to `HANDOFFS/` for Claude:

```
QUEUE/[task_id].json (task_type=RESEARCH)
  ↓ workflow1 "Non-Ollama Handler" node
  ↓ writes HANDOFFS/[task_id]_HANDOFF.json
  ↓ sets task status = ESCALATED
→ Claude or Antigravity reads HANDOFF at next session
```

This is correct for research tasks that need judgment — they should go to Claude. But it means no automated web search runs. Tavily integration must be added to handle automated research without human escalation.

---

## TAVILY INTEGRATION SPEC (Gap 8 — Phase 2)

Add a Tavily branch to workflow1 for RESEARCH tasks that can be auto-resolved:

```
RESEARCH task arrives
  ↓ Does task have field "auto_research": true?
    YES → Call Tavily API
           POST https://api.tavily.com/search
           Body: { query: task.prompt, search_depth: "basic", max_results: 5 }
           → write results to OUTPUTS/[task_id]_RESEARCH.md
           → set status = COMPLETE
    NO → Direct HANDOFF to Claude (current behavior)
```

**Tavily API key:** Already in `n8n_env.ps1` as active credential. Add to n8n credential store per SECRETS_POLICY.md Phase 2 plan.

**New field on job envelope:** `"auto_research": true | false` — allows caller to specify whether Tavily should attempt auto-resolution before escalating to Claude.

---

## PERPLEXITY INTAKE FLOW

Will runs a Perplexity query manually. Output is saved as structured JSON to QUEUE/:

```json
{
  "task_id": "YYYYMMDD-###",
  "task_type": "RESEARCH",
  "topic": "[research topic]",
  "prompt": "[Perplexity response or summary]",
  "priority": "NORMAL",
  "status": "PENDING",
  "source": "PERPLEXITY_MANUAL",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/[task_id]_RESEARCH.md"
}
```

See JOB_ENVELOPE_SPEC.md for the full canonical schema. RESEARCH tasks may add optional fields: `auto_research`, `source`.

workflow1 picks this up and routes it to Claude HANDOFF (unless `auto_research: true`).

This is the canonical path for research findings entering the Engine from Perplexity.

---

## WORKFLOW3 — CONFIRMED: DEDICATED RESEARCH HANDLER

**Decision confirmed 2026-05-29 (D3 = C2).**

workflow3 is a dedicated RESEARCH handler. It is not yet built or imported into n8n.

**Purpose:** Keep workflow1 Ollama-only (clean decision layer). workflow3 owns all RESEARCH task_type logic — Tavily automated search, Perplexity intake, result formatting, source tagging, and retry logic.

**Trigger:** workflow3 fires when workflow1 routes a task with `task_type = "RESEARCH"` to the Non-Ollama Handler node. The Non-Ollama Handler writes a HANDOFF file and sets status = ESCALATED. workflow3 should watch HANDOFFS/ for RESEARCH-type handoffs and pick them up automatically (or workflow1 can be updated to call workflow3 directly via webhook).

**workflow3 scope:**
- Receive RESEARCH task from QUEUE/ or HANDOFFS/
- If `auto_research: true` → call Tavily API → write structured result to OUTPUTS/
- If `auto_research: false` or Tavily fails → write HANDOFF for Claude
- Log all routing decisions to DECISION_LOG.md
- Output format: standard RESEARCH output format (see below)

**Build prerequisite:** Tavily API key active in n8n_env.ps1 (already confirmed). No Docker required.

---

## RESEARCH OUTPUT FORMAT

Whether handled by Tavily, Perplexity, or Claude, RESEARCH outputs should follow this structure:

```markdown
---
TASK_ID: [id]
SOURCE: TAVILY | PERPLEXITY | CLAUDE
DATE: [timestamp]
STATUS: DRAFT
REVIEW_REQUIRED: YES
---

# RESEARCH OUTPUT — [topic]

## Summary
[2-3 sentence summary]

## Findings
[numbered list of findings]

## Sources
[URLs or references]

## Unresolved
[anything that needs follow-up]
```

---

## CONNECTED FILES
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §3]]
- [[ANTIGRAVITY_N8N_TRIGGER|Antigravity → n8n Trigger]]
- [[SECRETS_POLICY|Secrets Policy]]
- [[workflow1_queue_processor|Workflow 1 JSON]]
- [[QUESTIONS_FOR_WILL|Questions for Will]]
