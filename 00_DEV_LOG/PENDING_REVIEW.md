---
STATUS: FOR HUMAN REVIEW
LAST_UPDATED: 2026-05-29
SCANNED_BY: Claude Code (claude-sonnet-4-6)
NOTE: Scan-only. Nothing was modified. Will reviews and decides.
---

# PENDING REVIEW — VAULT UNCONFIRMED & FOR HUMAN REVIEW ITEMS

Scanned: 2026-05-29
Method: grep across all .md files, noise-filtered (rule defs, path references, and system files excluded)

---

## SECTION 1: WHOLE FILES — STATUS: UNCONFIRMED
These files cannot be built from until Will confirms them.

| File | Notes |
|------|-------|
| 03_INFRASTRUCTURE/METADATA_SYSTEM.md | Supabase schema not yet designed |
| 04_WORKFLOWS/CULLING.md | Full file unconfirmed |
| 04_WORKFLOWS/DELIVERY.md | Platform, notification method all TBD |
| 04_WORKFLOWS/EXPORT.md | Export specs awaiting Will confirmation |
| 04_WORKFLOWS/ARCHIVE.md | Full file unconfirmed |
| 05_AI_LAYER/QUALITY_CONTROL.md | Full file unconfirmed |
| 06_TOOLS/INTEGRATIONS.md | SFV_EVENTS status, scheduling tool, Tailscale all TBD |
| 08_TESTS/FAILURE_TESTS.md | Full file unconfirmed |
| 08_TESTS/EDGE_CASES.md | Full file unconfirmed |
| 08_TESTS/BUILD_READINESS_CHECKLIST.md | Full file unconfirmed |
| 09_PROMPTS/RESEARCH_PROMPTS.md | Full file unconfirmed |
| 02_BRANCHES/SFV_UGC.md | Handle and pricing unconfirmed |
| 12_DATABANKS/DATABANK_ARCHITECTURE.md | Full file unconfirmed |
| 12_DATABANKS/BRAND_BANKS.md | Caption style TBD |
| 12_DATABANKS/TASTE_BANKS.md | Full file unconfirmed |
| 12_DATABANKS/CLIENT_BANKS.md | Full file unconfirmed |
| 12_DATABANKS/RESEARCH_BANKS.md | Full file unconfirmed |
| 12_DATABANKS/CONTENT_BANKS.md | Full file unconfirmed |
| 12_DATABANKS/TRAINING_DATA.md | Full file unconfirmed |

---

## SECTION 2: WHOLE FILES — STATUS: FOR HUMAN REVIEW
These files need Will's explicit decision before any action is taken.

| File | Notes |
|------|-------|
| 04_WORKFLOWS/N8N_BLUEPRINT.md | Entire n8n workflow blueprint awaiting approval |
| 99_INBOX/OUTPUTS/20260525-002_INGEST_WASTE_AUDIT.md | Ingest audit with several FOR HUMAN REVIEW recommendations |
| 00_DEV_LOG/ORPHANS.md | Orphaned items awaiting categorization |

---

## SECTION 3: SPECIFIC ITEMS — BUSINESS / CREATIVE (Will decides)
These are within otherwise active files. Touch nothing — Will answers.

### HARDWARE_CONTEXT.md
- L18: Three-monitor setup — confirmed or still planned?
- L57: Future bottlenecks section — content TBD

### 02_BRANCHES/SFV_404.md
- L16: Own IG account confirmed? Or different platform?
- L23: Content scope — photography + graphic/mixed media — confirm

### 02_BRANCHES/SFV_EVENTS.md
- L33: Final pricing scheme — UNCONFIRMED
- L35–37: Delivery method — Pixieset (like Studio) or different?

### 02_BRANCHES/SFV_UGC.md
- L20: Handle — `SFV_UGC` or alternative?
- L40: Package pricing — UNCONFIRMED

### 06_TOOLS/TOOLBOX.md
- L49: IG scheduling tool — Later vs Buffer — not chosen yet
- L50: Buffer as alternative — UNCONFIRMED
- L53: Canva API for Level 6+ accounts — UNCONFIRMED

### 11_VERSIONS/UPGRADE_CHECKPOINTS.md
- L53: UPS installation — FOR HUMAN REVIEW

### 06_TOOLS/TOOL_STACK.md
- L48: OpenClaw (R&D terminal agent) — FOR HUMAN REVIEW

### 03_INFRASTRUCTURE/STACK_INTEGRATION_PLAN.md
- L264: Antigravity role in Cowork-specific SFV tasks — INFERENCE, FOR HUMAN REVIEW

---

## SECTION 4: SPECIFIC ITEMS — TECHNICAL (Will or Claude can decide)
These are technical decisions that do not require creative/business input but were flagged for confirmation.

### 03_INFRASTRUCTURE/METADATA_SYSTEM.md
- L32: DATABASE IDs structure — Supabase schema not yet designed
- L39: METADATA STORAGE location — UNCONFIRMED

### 05_AI_LAYER/LOCAL_MODELS.md
- L19: Model selection for R&D Terminal — install and test before locking
- L36: Electricity management strategy — FOR HUMAN REVIEW
- L42: Connection to Engine Body — UNCONFIRMED

### 05_AI_LAYER/RATE_LIMITS.md
- L10: Rate limit numbers are INFERENCE from training data — need verification
- L70: Gemini 2.5 Pro RPD (~25/day) — INFERENCE, verify against current Gemini docs
- L89: Queries/day (~50/notebook) — INFERENCE, verify

### 06_TOOLS/TOOL_STATUS.md
- L54: Docker — UNCONFIRMED, currently evaluating

### 02_BRANCHES/MYTHOLOGY.md
- L33–38: CATCH LOGIC — auto-detection logic for Mythology branch is UNCONFIRMED

### 10_REFERENCES/TOOL_RESEARCH.md
- L24: Status RESEARCHING — FOR HUMAN REVIEW (check if research is complete)

### 99_INBOX/OUTPUTS/20260525-002_INGEST_WASTE_AUDIT.md (key items)
- L69: Should Ollama be added as post-ingest branch classifier for unknown files?
- L78: Is cross-branch dedup a real requirement for Will's workflow?
- L92–93: n8n for file watcher trigger + notify step — flagged as easy wins, FOR HUMAN REVIEW
- L95: Branch auto-detection gap — Ollama post-ingest classifier?

---

## SECTION 5: FOR_HUMAN_REVIEW/PROPOSALS.md
Active Claude proposals waiting for Will's yes/no. Review separately.
Path: C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\PROPOSALS.md

---

## COUNTS
- Whole files UNCONFIRMED: 19
- Whole files FOR HUMAN REVIEW: 3
- Specific business items: ~14
- Specific technical items: ~14
- Total actionable items: ~50

## CONNECTED FILES
- [[00_DEV_LOG/DECISIONS|DECISIONS]]
- [[03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT|AI_STACK_ARCHITECTURE_BLUEPRINT]]
- [[04_WORKFLOWS/INGEST|INGEST]]
- [[06_TOOLS/INTEGRATIONS|INTEGRATIONS]]
- [[12_DATABANKS/DATABANK_ARCHITECTURE|DATABANK_ARCHITECTURE]]
- [[05_AI_LAYER/QUALITY_CONTROL|QUALITY_CONTROL]]
- [[02_BRANCHES/SFV_UGC|SFV_UGC]]
- [[09_PROMPTS/RESEARCH_PROMPTS|RESEARCH_PROMPTS]]
