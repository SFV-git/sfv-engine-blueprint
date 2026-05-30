---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# OUTPUT VALIDATION

## Purpose

This document defines general validation criteria for AI outputs across all task_types in the SFV Engine AI stack.

It establishes what constitutes a valid output that proceeds to OUTPUTS/ versus a failure that is flagged, retried, or escalated to HANDOFFS/. Validation logic lives in the workflow layer — this document is the authoritative spec that workflow nodes implement.

**Relationship to QUALITY_CONTROL.md:** QUALITY_CONTROL.md (STATUS: UNCONFIRMED) handles client-delivery QC for SFV_UGC and SFV_EVENTS specifically — post-production reel audits, brand alignment, hook strength, CTA checks. OUTPUT_VALIDATION.md covers the general AI stack layer: is the model's raw output structurally sound before it enters any downstream step? These two layers are additive, not competing. OUTPUT_VALIDATION runs first; QUALITY_CONTROL runs after, on approved content only.

---

## Output Status Tags

Every output file written to OUTPUTS/ carries one of the following status tags in its metadata or filename suffix:

| Tag | Meaning |
|---|---|
| DRAFT | Written to OUTPUTS/, not yet validated |
| VALIDATED | Passed automatic validation checks |
| FLAGGED | Failed validation — reason noted, Will reviews |
| ESCALATED | Routed to HANDOFFS/ for Claude to handle |

---

## Validation Criteria by task_type

### CLASSIFY

**Valid output:**
- Response contains exactly one known branch name from the canonical list: MYTHOLOGY, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO, SFV_UGC, SFV_ARCHIVE, SFV_WORLD, SFV_404
- Response includes a confidence level (HIGH or LOW per CONFIDENCE_LOGIC.md) and a brief reason

**Invalid output:**
- No branch name present
- Multiple branch names returned without a reasoned selection
- Response is a refusal or uncertainty statement ("I don't know", "I cannot classify")
- Branch name returned that is not in the canonical nine

**Auto-fix:** None. Invalid CLASSIFY outputs escalate directly to HANDOFFS/ for Claude review.

---

### SUMMARIZE

**Valid output:**
- Response is between 50 and 500 words
- Response contains the key topic of the source material
- Response does not contradict factual statements in the source
- No hallucinated details that are absent from the source

**Invalid output:**
- Response is fewer than 20 words (likely truncated or incomplete)
- Response is longer than the source material itself
- Response contradicts the source
- Response is a refusal or generic placeholder

**Auto-fix:**
- Too long: truncate to 500 words and tag VALIDATED with a truncation note
- Too short: retry once with a tighter prompt; if retry also fails, tag FLAGGED

---

### CODE

**Valid output:**
- Syntactically valid Python (or the language specified in the task)
- Contains at least one function or class definition
- No placeholder comments such as `# TODO: implement this` or `# fill in here`
- No imports of modules that do not exist in the standard library or the project's known dependencies

**Invalid output:**
- Response is explanation-only with no code block
- Code contains obvious syntax errors (unmatched brackets, missing colons, etc.)
- Code imports non-existent or hallucinated modules
- Response is a refusal

**Auto-fix:** None. Invalid CODE outputs escalate to HANDOFFS/ for Claude review.

---

### VISION

**Valid output:**
- Response describes visual content rather than refusing to engage
- Response includes at minimum: the primary subject, a note on composition or framing, and at least one quality observation (exposure, sharpness, color, or technical issue)
- Response is specific to the image provided — not a generic description

**Invalid output:**
- Response is a refusal ("I cannot analyze images", "I'm not able to view this")
- Response is generic with no image-specific detail
- Response is empty or shorter than one sentence

**Auto-fix:** None. Invalid VISION outputs escalate to HANDOFFS/.

---

### RESEARCH

**Valid output:**
- Response contains at least two distinct findings relevant to the query
- Response cites or references at least one source, URL, or named reference
- Response is structured enough to be actionable (not all hedges)

**Invalid output:**
- Response is entirely hedged with no concrete findings ("It depends", "There are many factors", "I'm not sure")
- Response contains only one finding with no supporting reference
- Response is a refusal

**Auto-fix:** None. Invalid RESEARCH outputs route to Claude HANDOFF for a second pass.

---

### BLUEPRINT

**Valid output:**
- Response follows SFV vault structure: includes STATUS tag, VERSION, OWNER, LAST_UPDATED in frontmatter
- Contains a CONNECTED FILES section
- Content is organized under named headings — not a single block of prose

**Invalid output:**
- No frontmatter structure
- No STATUS tag
- No CONNECTED FILES section
- Response is a single unstructured paragraph

**Auto-fix:** None. Invalid BLUEPRINT outputs escalate to Claude for structural correction.

---

### MEDIA (Transcript)

**Valid output:**
- Response is a timestamped transcript (e.g., `[00:00:14] Speaker: text`) or speaker-labeled text block
- Response covers the duration or segment of the source audio/video
- Response is not garbled or character-corrupted

**Invalid output:**
- Empty response
- Garbled, corrupted, or non-language character output
- Response that describes the media rather than transcribing it

**Auto-fix:** Retry once with the same prompt. If retry also produces invalid output, tag FLAGGED and route for manual review.

---

## Validation Implementation Phases

### Phase 1 — Inline in workflow1 (current target)

Location: workflow1 "Write + Log" node, immediately after receiving the Ollama response.

Implementation: Basic regex and length checks per task_type. Examples:
- CLASSIFY: check response against canonical branch name list
- SUMMARIZE: word count check, source-length comparison
- CODE: check for presence of `def ` or `class `, absence of known placeholder strings
- VISION/RESEARCH/BLUEPRINT: minimum length threshold + structural keyword presence

Output: tag the output record as DRAFT, VALIDATED, FLAGGED, or ESCALATED before writing to OUTPUTS/.

### Phase 2 — Standalone validation workflow (planned)

A scheduled workflow (proposed: workflow5) post-processes all OUTPUTS/ files on a defined schedule (e.g., nightly). This layer runs deeper structural checks than Phase 1 can do inline. It surfaces FLAGGED items to Will for review.

[FOR HUMAN REVIEW]: Should workflow5 be a dedicated validation workflow, or a scheduled node appended to an existing workflow? Recommend standalone for separation of concerns, but Will decides.

### Phase 3 — Claude API validation layer (existing QUALITY_CONTROL.md flow)

For client-facing outputs (SFV_UGC, SFV_EVENTS reels), the QUALITY_CONTROL.md flow applies after Phases 1 and 2 pass. Claude performs brand alignment, hook strength, and CTA checks. This phase is the most expensive and runs only on content cleared by Phases 1 and 2.

---

## Escalation Path Summary

```
Ollama response received
  → Phase 1 checks (workflow1 "Write + Log" node)
      → VALID: tag VALIDATED, write to OUTPUTS/
      → INVALID, auto-fix possible: apply fix, tag VALIDATED with note
      → INVALID, no auto-fix: tag ESCALATED, write to HANDOFFS/
  → Phase 2 checks (workflow5, scheduled)
      → Re-validate DRAFT items in OUTPUTS/
      → Tag FLAGGED if structural issues found
      → Will reviews FLAGGED queue
  → Phase 3: QUALITY_CONTROL.md flow (SFV_UGC / SFV_EVENTS only)
```

---

## CONNECTED FILES

- [[QUALITY_CONTROL]]
- [[CONFIDENCE_LOGIC]]
- [[ENGINE_COMMUNICATION_MODEL]]
- [[workflow1_queue_processor]]
- [[AI_USE_CASE_PROFILE]]
