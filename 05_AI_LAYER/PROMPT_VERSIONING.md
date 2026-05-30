---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# PROMPT VERSIONING

## Purpose

This document defines version control discipline for all prompt files used by the SFV Engine AI stack. Prompts are the primary lever for output quality. Without versioning, prompt changes are invisible, regressions are untraceable, and A/B comparisons are impossible.

This spec governs the OLLAMA_PROMPTS/ folder inside 05_AI_LAYER/ and applies to all prompt files that drive Ollama model calls.

---

## Current State

OLLAMA_PROMPTS/ currently contains one file:

```
OLLAMA_PROMPTS/
  handoff_generator.txt
```

No versioning. No naming convention. No change history. Prompts are edited in-place. If a prompt change degrades output quality, there is no prior version to roll back to.

This document defines the discipline to fix that going forward.

---

## Version Naming Convention

```
OLLAMA_PROMPTS/
  [prompt_name]_v[N].txt        ← versioned, immutable after creation
  [prompt_name]_CURRENT.txt     ← active version (copy of latest vN)
  PROMPT_CHANGELOG.md           ← append-only version log
```

Example for handoff_generator after two revisions:

```
OLLAMA_PROMPTS/
  handoff_generator_v1.txt
  handoff_generator_v2.txt
  handoff_generator_CURRENT.txt   (copy of v2, this is what workflow1 reads)
  PROMPT_CHANGELOG.md
```

**Rules:**
- workflow1 reads only the CURRENT file — never a versioned file directly
- Versioned files (v1, v2, ...) are never overwritten or deleted after creation
- CURRENT is a plain copy, not a symlink — simpler on Windows, no OS dependency
- Version numbers are integers, no decimals: v1, v2, v3, not v1.1

---

## When to Create a New Version

Create a new version when any of the following change:
- Prompt structure (reordered sections, added/removed instructions)
- Output format specification (e.g., field names, expected length)
- Task framing or imperative wording
- Model-specific tuning (e.g., added qwen3 think-mode off tag)

Do NOT create a new version for:
- Whitespace or punctuation fixes that do not change meaning
- Fixing a typo that does not alter the instruction

When in doubt: bump the version. Storage cost is negligible. Version history is permanent value.

**Append-only rule:** Never overwrite an existing versioned file. If v3 exists and needs a change, create v4. v3 stays.

---

## Version Log — PROMPT_CHANGELOG.md

Every new version must be logged by appending a row to `OLLAMA_PROMPTS/PROMPT_CHANGELOG.md`.

Format:

```
| Version | Date | Prompt Name | Change Summary |
|---|---|---|---|
| v1 | 2026-05-29 | handoff_generator | Initial versioned baseline from unversioned original. |
| v2 | 2026-05-29 | handoff_generator | Changed summary field to 3 sentences max. Reason: outputs were too long for context budget. |
```

The PROMPT_CHANGELOG.md file itself is append-only. Do not edit past rows.

---

## A/B Testing Model (Phase 2 — not blocking)

Phase 2 introduces a structured A/B test process for prompts that run at high volume.

**Process:**
1. Create vN and vN+1 with the single change under test
2. Route identical tasks to both versions over one week (or until 50 outputs per version)
3. Score outputs on three metrics: HIGH_CONF rate, escalation rate, median output length
4. Keep the version with the better HIGH_CONF rate and shorter outputs
5. Record the winner in PROMPT_CHANGELOG.md with the metric scores
6. Retire the losing version — it stays in the folder as history but CURRENT is updated to the winner

**Scoring example entry for PROMPT_CHANGELOG.md:**

```
| v3 | 2026-06-10 | classify_branch | A/B winner over v2. HIGH_CONF: 87% vs 79%. Escalation: 4% vs 9%. Shorter output: avg 12 tokens vs 21. |
```

[FOR HUMAN REVIEW]: A/B testing requires running each task twice during the test window, doubling inference cost for that prompt. Recommended constraint: only A/B test prompts used more than 50 times per week. Lower-volume prompts should be updated by judgment, not A/B test. Confirm acceptable cost policy before Phase 2 is built.

---

## Prompt Library Scope

All prompt files that must be under version control:

| File | Status | Notes |
|---|---|---|
| handoff_generator.txt | Existing — needs v1 baseline created | First step: copy current file to handoff_generator_v1.txt, create CURRENT copy |
| classify_branch.txt | [INFERENCE] | Will be needed when CLASSIFY task_type prompt is formalized |
| summarize.txt | [INFERENCE] | Will be needed when SUMMARIZE prompt is separated from generic instruction |
| caption.txt | [INFERENCE] | Social caption generation for SFV_UGC / SFV_EVENTS |
| vision_audit.txt | [INFERENCE] | VISION task_type prompt for minicpm-v:8b |

[INFERENCE]: Future prompt files listed above are inferred from the AI stack task_types. Add each to this table when created. Do not create them without a confirmed use case.

---

## Prompt Engineering Principles for Ollama (qwen3:14b)

These principles apply to all prompts targeting qwen3:14b. They are guidelines, not syntax rules — apply judgment.

**Keep prompts short.**
Target under 200 tokens per prompt. qwen3 has an 8K context window but shorter prompts produce faster inference and more focused outputs. Every token of instruction that is not load-bearing should be removed.

**Use direct imperative format.**
State the task in one sentence. Do not explain why. Example:
- Preferred: "Classify this file. Output only the branch name."
- Avoid: "Your job is to look at the file and try to determine which branch of the SFV Engine it belongs to, then tell me the name of that branch."

**Do not ask for explanations unless the output requires them.**
Explanations add tokens and reduce HIGH_CONF rate. If the downstream system only needs a branch name, ask only for a branch name. If reasoning is needed (e.g., for HANDOFFS/ context), ask for it explicitly and keep it to one sentence.

**End every task-type prompt with an output format specification.**
Final line format: `Output: [exact format expected]`

Examples:
- `Output: One branch name from the canonical list. Nothing else.`
- `Output: A summary of 50 to 200 words. Plain text, no headers.`
- `Output: Python function with docstring. No explanation outside the code block.`

**For qwen3 think-mode:** qwen3:14b supports a thinking tag. For tasks where chain-of-thought helps accuracy (CLASSIFY on ambiguous files, RESEARCH), the prompt can include `/think` to enable it. For high-volume low-ambiguity tasks, omit it to reduce latency.

[FOR HUMAN REVIEW]: Think-mode usage policy — should think-mode be enabled per task_type in the routing config, or left to individual prompt files? Recommend: routing config sets the default, prompt files can override. Confirm before Phase 2.

---

## CONNECTED FILES

- [[LOCAL_MODELS]]
- [[ENGINE_COMMUNICATION_MODEL]]
- [[CONFIDENCE_LOGIC]]
- [[MODEL_ROUTING]]
- [[OUTPUT_VALIDATION]]
