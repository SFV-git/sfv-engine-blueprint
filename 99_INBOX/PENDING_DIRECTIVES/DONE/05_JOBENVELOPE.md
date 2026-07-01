---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-JOBENVELOPE-001
EXECUTOR: ollama
---

You are revising 05_AI_LAYER/JOB_ENVELOPE_SPEC.md for SFV Engine. Scored 3/5: good foundation, needs
detailed definitions and examples. A "job envelope" is the standard structured wrapper every task in
the system carries as it moves through the Hermes loop and n8n.

Context: the Hermes loop reads a directive with frontmatter STATUS / DIRECTIVE_ID / EXECUTOR and a body,
routes to an executor, writes {DIRECTIVE_ID}_RESULT.md, logs a row to DECISION_LOG.md.

Write a complete spec defining the job envelope schema covering: (1) every field a job carries
(id, type, executor, priority, status, created_at, source, payload/body, output_target, confidence,
review_required_by, canon_approval_required_by), (2) the field definitions with types and allowed values,
(3) the lifecycle states a job moves through (pending -> active -> complete/error -> reviewed -> ratified),
(4) TWO concrete worked examples of a filled envelope (one ollama mechanical task, one claude judgment task)
shown as JSON or frontmatter, (5) how the envelope maps onto the existing Hermes directive frontmatter.
Do not invent fields that contradict the Hermes loop contract above. Output only finished markdown.
