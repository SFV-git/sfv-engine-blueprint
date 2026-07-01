---
STATUS: ACTIVE
DIRECTIVE_ID: FABLE-20260701-UGC-AUDIT-PLAN-001
EXECUTOR: claude
PRIORITY: HIGH
CREATED: 2026-07-01
INSTRUCTIONS_FOR_EXECUTOR: >
  This task uses the claude executor (Fable 5 / Claude Sonnet). Read every file listed in
  CONTEXT_FILES below before writing anything. Spend tokens only on thinking and producing
  the plan doc. Do not rewrite any vault file. Do not self-ratify anything. Output goes to
  OUTPUT_TARGET only. Blueprint Lock applies.
---

# DIRECTIVE: FABLE UGC AUDIT + OPTIMAL PLAN

## ROLE
You are the SFV Blueprint Builder. You have deep knowledge of the SFV Engine architecture.
This is a first-pass audit and planning session — thinking and planning only, no execution.

## OBJECTIVE
1. Read all UGC-related vault files listed below
2. Identify every gap, missing piece, and quality failure in the current UGC blueprint
3. Produce a single comprehensive plan document that local subagents can execute 1-for-1
   without needing judgment — every instruction must be specific enough that a local model
   running headless can follow it exactly
4. Include a website architecture plan: produce exact prompts that local AI would use to
   build each of the four sides (client portal, true admin, SFV subcontractor, SaaS client/admin)
5. Flag all cybersecurity considerations that must be stress-tested before launch

## CONTEXT FILES — READ ALL BEFORE WRITING
- C:\SFV_BLUEPRINT\02_BRANCHES\SFV_UGC_SEED.md          ← Will's actual business (ground truth)
- C:\SFV_BLUEPRINT\02_BRANCHES\SFV_UGC.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_PRE_PRODUCTION.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_BUSINESS_PIPELINE.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\UGC_DELIVERY.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\VIDEO_EDIT_WORKFLOW.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\QC_CHECKLIST.md
- C:\SFV_BLUEPRINT\04_WORKFLOWS\SCHEDULING_WORKFLOW.md
- C:\SFV_BLUEPRINT\12_DATABANKS\DATABANK_ARCHITECTURE.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\CONTENT_IDEA_BANK.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\CLIENT_BANKS.md           ← if exists
- C:\SFV_BLUEPRINT\13_SAAS_CONVERSION\SAAS_CONVERSION_PLAN.md
- C:\SFV_BLUEPRINT\08_TESTS\BLUEPRINT_COVERAGE_MAP.md    ← Domain B coverage table

## OUTPUT TARGET
C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\FABLE-20260701-UGC-AUDIT-PLAN-001.md

## OUTPUT STRUCTURE REQUIRED
The output doc must contain exactly these sections in order:

### 1. GAP ANALYSIS
Every missing or broken piece in the current UGC blueprint. Be specific — name the file,
name the gap, quote the failure if relevant. Reference the Perplexity audit verdicts:
VIDEO_EDIT_WORKFLOW = 1.5/5 (hallucinated Premiere features), UGC_BUSINESS_PIPELINE = 1/5
(described wrong business model entirely). Those two need full rewrites.

### 2. PRIORITY-ORDERED REWRITE LIST
Every file that needs to be rewritten or created, in execution order. For each:
- File path
- What it currently says (one sentence)
- What it must say instead (specific, based on SFV_UGC_SEED.md ground truth)
- Which executor should write it: ollama (mechanical) or perplexity (needs real-world research)

### 3. SUBAGENT EXECUTION PLAN
For every rewrite in §2: write the exact directive text that would go into CURRENT_DIRECTIVE.md
to produce that file. These must be specific enough that qwen3:14b running headless produces
an accurate, non-generic result. Include the seed facts from SFV_UGC_SEED.md inline in each
directive so the subagent has ground truth baked in.

### 4. WEBSITE ARCHITECTURE + LOCAL AI BUILD PROMPTS
Four portals:
a) Client portal — brand logs in, sees their content calendar, approves deliverables, downloads assets
b) True admin (Will) — full pipeline view, client management, operator assignment, invoicing
c) SFV subcontractor portal — field operators see assigned shoots, upload footage, track status
d) SaaS client/admin — if/when productized for other shooters to license the system

For each portal: what pages/features it needs, tech stack recommendation (given local-first/
BYO-compute constraints from SAAS_CONVERSION_PLAN.md), and the exact prompt you would give
a local AI to build it (React/Next.js spec-level detail).

### 5. CYBERSECURITY CHECKLIST (pre-launch)
List every security test that must pass before this goes to market. For each: test name,
what it checks, pass/fail criteria. Flag which can be automated vs require manual pen testing.
These become the inputs to Fable's final security stress test pass.

### 6. FABLE FINAL REVIEW GATE
After all rewrites are executed by subagents, Fable does a final pass. Describe exactly what
Fable will check in that pass — the criteria, the file list, and the output format of the
final sign-off doc.

## CONSTRAINTS
- Blueprint Lock: no CANON self-promotion, no live system changes
- Everything in output is FOR HUMAN REVIEW until Will ratifies
- Base all UGC content on SFV_UGC_SEED.md, not assumptions
- If a file listed in CONTEXT_FILES does not exist, note it as MISSING in §1
- Do not pad. Dense, specific, executable.
