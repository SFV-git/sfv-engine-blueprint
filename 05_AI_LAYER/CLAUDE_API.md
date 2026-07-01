---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# CLAUDE API USAGE

## PRINCIPLE
Claude API is reserved for high-value tasks only.
Never use Claude for tasks a local model can handle.

## APPROVED USE CASES
- Caption and copy writing (final polish)
- Creative strategy decisions
- Art direction guidance
- Complex reasoning and planning
- Blueprint development (this vault)
- QC audit final layer (after local model pre-check)
- Client brief generation
- Monthly content map generation

## NEVER USE CLAUDE API FOR
- File sorting
- Tagging
- Transcript cleanup
- Repetitive organization
- Rough summaries
- Blur or duplicate detection
- Any task a local model handles

## COST MANAGEMENT
- Use Sonnet for most tasks (5x cheaper than Opus)
- Use Opus only for complex reasoning
- API key mode for automation (not subscription)
- Set spend cap in Anthropic Console
- Context compression: always use MASTER_CONTEXT.md reference
  instead of re-explaining SFV in every call

## CONTEXT COMPRESSION
Never feed raw unstructured context to Claude.
Always:
1. Local model processes and summarizes first
2. Claude receives condensed high-value context only
Example:
BAD: "Here are 400 photos, analyze them"
GOOD: "Best 18 selects from LIVE shoot. Sequence for carousel."

## CONNECTED FILES
- [[05_AI_LAYER/COST_CEILING_POLICY|Cost Ceiling Policy]]
- [[MASTER_CONTEXT|Master Context]]
- [[05_AI_LAYER/OUTPUT_VALIDATION|Output Validation]]
