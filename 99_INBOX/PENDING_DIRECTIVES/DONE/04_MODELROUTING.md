---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-MODELROUTING-001
EXECUTOR: ollama
---

You are revising 05_AI_LAYER/MODEL_ROUTING.md for SFV Engine. Scored 3/5: clear direction, needs
specifics on implementation and evaluation. This is the doc that governs which model/executor handles
which task, by cost tier.

The LOCKED routing rule is:
- ollama (local qwen3:14b, free) -> cheap mechanical work: inventories, classification, summaries, stubs, doc drafts
- claude_code (cloud, billed) -> real multi-file blueprint authoring
- codex (ChatGPT sub) -> narrow coding tasks with locked specs, write-enabled in vault
- claude (cloud, billed) -> hard one-shot judgment only
- NEW tier under evaluation: devstral-small-2 (24B, local, free) via an agentic harness as a
  potential free replacement for the claude_code tier (still FOR HUMAN REVIEW, not adopted).

Write a complete routing policy covering: (1) the tier table above with a concrete decision rule for
each (what signals route a task to each tier — token estimate, file count, whether it needs judgment vs
mechanical execution, whether it needs web/current facts), (2) escalation path (try free local first,
escalate to paid only on failure), (3) a short worked example of routing 3 different tasks, (4) how
routing decisions get logged. Do not invent pricing. Mark unadopted items [FOR HUMAN REVIEW].
Output only finished markdown.
