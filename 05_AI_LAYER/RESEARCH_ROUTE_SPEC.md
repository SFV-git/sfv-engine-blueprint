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

workflow1 picks this up and routes it to Claude HANDOFF (unless `auto_research: true`).

This is the canonical path for research findings entering the Engine from Perplexity.

---

## WORKFLOW3 — OPEN QUESTION (Gap 9)

**[FOR HUMAN REVIEW — D3 not answered]**

Workflows 1, 2, and 4 are imported and active. No workflow3 exists in the vault or in n8n.

**Inference:** workflow3 was intended as a dedicated RESEARCH handler, possibly calling Tavily or Perplexity API directly. This would offload research routing from workflow1 and give research tasks their own dedicated pipeline with retry logic, result formatting, and direct OUTPUTS write.

**Question for Will:**
- Was workflow3 intentionally skipped?
- Should workflow3 be a dedicated RESEARCH handler (Tavily + Perplexity integration)?
- Or should research routing stay inside workflow1 as a branch?

**Recommendation:** Build workflow3 as a dedicated RESEARCH handler. Keeps workflow1 clean (Ollama-only decisions) and allows research-specific logic (Tavily retry, result formatting, source tagging) without bloating workflow1.

**Do not build workflow3 until Will confirms direction.**

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
