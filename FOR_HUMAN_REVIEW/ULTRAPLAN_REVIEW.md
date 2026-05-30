---
STATUS: FOR HUMAN REVIEW
REVIEWER: Antigravity (Claude Opus 4.6)
DATE: 2026-05-29
---

# ULTRAPLAN REVIEW — 19 New Blueprint Docs

Audit of all 19 FOR HUMAN REVIEW docs against the 5 CANON docs:
SESSION_STATE.md, AI_STACK_ARCHITECTURE_BLUEPRINT.md, AI_USE_CASE_PROFILE.md,
ANTIGRAVITY_RULES.md, ENGINE_COMMUNICATION_MODEL.md.

---

## CONTRADICTION — 05_AI_LAYER/CONFIDENCE_LOGIC.md
What: CONFIDENCE_LOGIC.md replaces the CANON numeric confidence threshold (< 0.75) with a keyword-matching approach (default HIGH, only LOW if doubt words found) — these are fundamentally different escalation mechanisms.
Location: "CURRENT LOGIC" section vs AI_STACK_ARCHITECTURE_BLUEPRINT.md §3 line 139: "confidence score evaluates to < 0.75"
Recommendation: Will must decide which approach is authoritative — if the keyword approach is correct (and the JSON fix confirms it is the live implementation), then AI_STACK_ARCHITECTURE_BLUEPRINT §3 must be updated to retire the 0.75 threshold. One of the two must change.

## CONTRADICTION — 05_AI_LAYER/VECTOR_LAYER_PLAN.md
What: Proposes storing Qdrant data on D:\ (Seagate) instead of C:\ (SSD), directly contradicting AI_STACK_ARCHITECTURE_BLUEPRINT.md §2 File Allocation table which assigns "Qdrant vector DB | A | C:\ | Vector search latency demands SSD."
Location: "QDRANT DEPLOYMENT" section, docker run command and "Storage rationale correction" paragraph
Recommendation: Remove the "rationale correction" and align with the CANON C:\ decision. If Will wants to change it, update the Blueprint first.

## CONTRADICTION — 03_INFRASTRUCTURE/DISASTER_RECOVERY.md
What: Proposes backup path `C:\SFV_ACTIVE\BACKUPS\` — but no `C:\SFV_ACTIVE` directory exists in the CANON path layout. COMPRESSED_CONTEXT.md defines active storage as `D:\SFV_ACTIVE` (Seagate One Touch 5TB).
Location: Section "4. n8n DATABASE BACKUP", pg_dump example path
Recommendation: Change all `C:\SFV_ACTIVE` references to `D:\SFV_ACTIVE`.

## CONTRADICTION — 05_AI_LAYER/COST_CEILING_POLICY.md
What: Section 2.4 is titled "Ollama (local — R&D Terminal)" — but CANON designates Ollama primary on Engine Body (Node A), not R&D Terminal (Node B). Node B runs a secondary/fallback Ollama instance only.
Location: Section 2.4 heading, line 72
Recommendation: Correct the heading to "Ollama (local — Engine Body)" to match AI_STACK_ARCHITECTURE_BLUEPRINT §1 and the Service Endpoint Registry.

---

## MISSING LINK — 05_AI_LAYER/COST_CEILING_POLICY.md
What: Defines COST_ALERTS.md at `99_INBOX/COST_ALERTS.md` as the central alert log, referenced 11 times across the doc, but this file does not exist in the vault.
Location: Sections 3, 4, 5, and 6
Recommendation: Flag as a prerequisite — COST_ALERTS.md must be created (even as an empty table header) before this policy can be enacted. Do not create it until Will promotes this doc.

## MISSING LINK — 03_INFRASTRUCTURE/FAILOVER_MODEL.md + MONITORING_STACK.md
What: Both docs write to `99_INBOX/FAILOVER_LOG.md` as a shared append-only log, but this file does not exist in the vault. MONITORING_STACK.md also writes to it via the alert script.
Location: FAILOVER_MODEL.md "FAILOVER LOG FORMAT" section; MONITORING_STACK.md Section 6
Recommendation: Same as above — create the file with headers when the first of these docs is promoted.

## MISSING LINK — 05_AI_LAYER/CONFIDENCE_LOGIC.md
What: CONFIDENCE_LOGIC.md references "client-facing" job envelope flag as an alternative escalation trigger, echoing AI_STACK_ARCHITECTURE_BLUEPRINT §3 ("or if the job envelope flags it as 'client-facing'"), but no doc defines how this flag is set or what job envelope field it maps to.
Location: Inherited from CANON (Blueprint §3 line 139), but CONFIDENCE_LOGIC should have addressed it
Recommendation: Will decides whether to add a `client_facing: true|false` field to the canonical job envelope schema or defer it.

---

## SEQUENCING ERROR — 03_INFRASTRUCTURE/MONITORING_STACK.md
What: Plans to deploy Prometheus and Grafana as Docker containers on Node B (R&D Terminal), but DOCKER_INSTALL_CHECKLIST.md only specs Docker for Node A (Engine Body). Docker on Node B was explicitly "DEFERRED to Phase 2" per SESSION_STATE.md (2026-05-27 session).
Location: Sections 3 and 4 (Docker run commands for Prometheus and Grafana)
Recommendation: Either add a Node B Docker install step to DOCKER_INSTALL_CHECKLIST.md, or restructure MONITORING_STACK.md to deploy on Node A instead. Will must approve Node B Docker before this stack can proceed.

## SEQUENCING ERROR — 03_INFRASTRUCTURE/N8N_MCP_SPEC.md
What: Lists "n8n running with PostgreSQL" as a prerequisite, but POSTGRES_MIGRATION.md is itself still FOR HUMAN REVIEW. The MCP spec cannot be acted on until PostgreSQL is migrated AND confirmed stable.
Location: "PREREQUISITES" section
Recommendation: No doc change needed — this is correctly sequenced as a dependency chain. But flag for Will: the promotion order must be PostgreSQL → Docker → N8N_MCP_SPEC. Promoting N8N_MCP_SPEC to CANON before its prerequisites are CANON creates a dead spec.

---

## INFERENCE GAP — 05_AI_LAYER/RESEARCH_ROUTE_SPEC.md
What: Frames workflow3 as an open question requiring Will's decision, but AI_STACK_ARCHITECTURE_BLUEPRINT §1 already defines "Branch E: Research" as part of the n8n Router Layer — CANON implies research routing lives inside workflow1.
Location: "WORKFLOW3 — OPEN QUESTION (Gap 9)" section
Recommendation: Flag [INFERENCE] that CANON already answers this: RESEARCH is Branch E in workflow1, not a separate workflow. Will can confirm or override, but the question is not as open as the doc implies.

## INFERENCE GAP — 03_INFRASTRUCTURE/POSTGRES_MIGRATION.md
What: Presents Docker vs native Windows install as equally open options (Option A vs Option B), but AI_STACK_ARCHITECTURE_BLUEPRINT §2 File Allocation table assigns "n8n data & Postgres DB | A | C:\ | DB read/write performance is critical for webhook speed" — implying native install on C:\, not a Docker container.
Location: "POSTGRESQL INSTALL" section, Option B
Recommendation: Resolve the [INFERENCE] tag on Option B — CANON leans toward native install (Option A). Docker option can remain documented as an alternative but should note it does not match the current CANON storage allocation.

## INFERENCE GAP — 05_AI_LAYER/GEMINI_INTEGRATION.md
What: Gemini Flash rate limits are marked [INFERENCE] (15 RPM, 1500 RPD), but 05_AI_LAYER/RATE_LIMITS.md already exists in the vault and is listed as a key context file in ANTIGRAVITY.md.
Location: "RATE LIMITS AND FALLBACK" section
Recommendation: Cross-check against RATE_LIMITS.md and promote to confirmed if the numbers match.

---

## REDUNDANCY — Job Envelope Schema (3 docs)
What: The canonical job envelope schema is defined in AI_STACK_ARCHITECTURE_BLUEPRINT §4, then re-stated in ANTIGRAVITY_N8N_TRIGGER.md (adds `prompt` field), RESEARCH_ROUTE_SPEC.md (adds `auto_research` and `source` fields), and MEDIA_PIPELINE.md (adds `file_path` and `output_format` fields). Four definitions of the same schema will inevitably drift.
Location: Blueprint §4; ANTIGRAVITY_N8N_TRIGGER "JOB ENVELOPE FORMAT"; RESEARCH_ROUTE_SPEC "PERPLEXITY INTAKE FLOW"; MEDIA_PIPELINE §2
Recommendation: Define extensions in one place. Either update the CANON schema with optional fields, or create a single JOB_ENVELOPE_SPEC.md that all docs reference. Remove inline schema re-definitions from the satellite docs.

## REDUNDANCY — Gemini Rate Limits (2 docs)
What: Gemini Flash rate limits (1500 RPD) are defined in both COST_CEILING_POLICY.md §2.3 and GEMINI_INTEGRATION.md §"RATE LIMITS AND FALLBACK". Both are marked [INFERENCE]. If one is updated and the other is not, they will conflict.
Location: COST_CEILING_POLICY §2.3; GEMINI_INTEGRATION rate limits table
Recommendation: Pick one as the authoritative source for Gemini rate limits (RATE_LIMITS.md already exists for this purpose) and have both docs reference it.

## REDUNDANCY — FAILOVER_MODEL.md + DISASTER_RECOVERY.md
What: Both docs cover "Engine Body goes offline" scenarios with overlapping recovery guidance. FAILOVER_MODEL covers operational runtime recovery; DISASTER_RECOVERY covers catastrophic loss. The boundary is reasonable but the Node B offline scenario appears in both.
Location: FAILOVER_MODEL §3, §4; DISASTER_RECOVERY §7
Recommendation: Acceptable overlap if scopes stay distinct (runtime vs catastrophic). Add a one-line cross-reference in each noting the boundary: FAILOVER_MODEL = "service is down, node is rebooting"; DISASTER_RECOVERY = "hardware is destroyed or data is corrupted beyond restart."

---

## SCOPE CREEP — 03_INFRASTRUCTURE/MONITORING_STACK.md
What: Contains a full PowerShell implementation of the prometheus_alert_writer.ps1 script (10+ lines of executable code with variable interpolation, REST calls, and file writes).
Location: Section 6 "Alert Script Spec"
Recommendation: Replace the code with a behavioral spec (inputs, outputs, trigger, log format). Build the actual script in 99_INBOX/ during the dev phase.

## SCOPE CREEP — 03_INFRASTRUCTURE/FAILOVER_MODEL.md
What: Contains pseudocode for an n8n watchdog script (loop, health check, retry, relaunch).
Location: Section "FAILURE SCENARIO 2 — n8n process crash", watchdog spec block
Recommendation: Replace with a behavioral spec. The pseudocode is close to implementation — it belongs in a build task, not a blueprint.

## SCOPE CREEP — 04_WORKFLOWS/MEDIA_PIPELINE.md
What: Contains specific FFmpeg command with precise flags (`-ar 16000 -ac 1 -c:a pcm_s16le`). This is an implementation decision that should be validated at build time, not locked in a blueprint.
Location: Section 4 "FFMPEG PRE-PROCESSING", command spec block
Recommendation: Borderline — the flags are spec-level detail. Keep for now but note that exact FFmpeg parameters should be validated during dev phase and may need adjustment for different codecs.

---

## EXISTING CANON CONFLICT (informational — not caused by new docs)
What: ENGINE_COMMUNICATION_MODEL.md (CANON) defines status tags as `PENDING | IN_PROGRESS | COMPLETE | BLOCKED | DRAFT`, while AI_STACK_ARCHITECTURE_BLUEPRINT.md (CANON) defines them as `PENDING | IN_PROGRESS | COMPLETE | ESCALATED | DEFERRED`. The two CANON docs disagree on valid status values. All 19 new docs use ESCALATED/DEFERRED (matching the Blueprint), which means they implicitly contradict ENGINE_COMMUNICATION_MODEL.md.
Location: ENGINE_COMMUNICATION_MODEL §"STATUS TAGS" vs AI_STACK_ARCHITECTURE_BLUEPRINT §4 job envelope schema
Recommendation: Will should reconcile these two CANON docs. The combined set is likely: `PENDING | IN_PROGRESS | COMPLETE | ESCALATED | DEFERRED | BLOCKED | DRAFT`. Update both CANON docs to use the unified list.

---

## READY TO PROMOTE

The following docs had no contradictions, no hard sequencing errors, and no scope creep.
They have minor [INFERENCE] items or [FOR HUMAN REVIEW] questions that are correctly labeled
and do not block promotion. Will can mark these CANON after reviewing the tagged items inline.

- **03_INFRASTRUCTURE/DOCKER_INSTALL_CHECKLIST.md** — Clean. Correct prerequisite chains. No issues.
- **03_INFRASTRUCTURE/SECRETS_POLICY.md** — Clean. Practical, well-scoped, correct cross-references.
- **03_INFRASTRUCTURE/CONCURRENCY_QUEUE_SPEC.md** — Clean. Correctly sequences Phase 1 (no Redis) and Phase 2 (Redis). SQLite warning aligns with CANON.
- **05_AI_LAYER/OUTPUT_VALIDATION.md** — Clean. Correctly references QUALITY_CONTROL.md (STATUS: UNCONFIRMED, exists in vault). Additive layer, not competing.
- **05_AI_LAYER/PROMPT_VERSIONING.md** — Clean. Introduces discipline without contradicting any CANON doc. Good vault hygiene.
- **03_INFRASTRUCTURE/N8N_MCP_SPEC.md** — Clean. Prerequisites correctly listed. Fallback to file-drop documented. Promote after Docker and PostgreSQL are confirmed.

## NOT READY TO PROMOTE

These docs have findings above that must be resolved before promotion:

| Doc | Blocking Finding |
|---|---|
| CONFIDENCE_LOGIC.md | Contradicts CANON 0.75 threshold — must reconcile |
| VECTOR_LAYER_PLAN.md | Contradicts CANON C:\ storage allocation |
| DISASTER_RECOVERY.md | Wrong path (C:\SFV_ACTIVE vs D:\SFV_ACTIVE) |
| COST_CEILING_POLICY.md | Ollama mislabeled as R&D Terminal; Gemini rate limit redundancy |
| ANTIGRAVITY_N8N_TRIGGER.md | Job envelope redundancy — needs single source of truth |
| RESEARCH_ROUTE_SPEC.md | workflow3 question is partially answered by CANON |
| MEDIA_PIPELINE.md | Job envelope redundancy; FFmpeg scope creep (minor) |
| MONITORING_STACK.md | Docker on Node B not approved; script code in blueprint |
| FAILOVER_MODEL.md | Script pseudocode in blueprint |
| POSTGRES_MIGRATION.md | Docker option conflicts with CANON storage allocation |
| GEMINI_INTEGRATION.md | Rate limit redundancy with COST_CEILING_POLICY |
| MODEL_LIFECYCLE_POLICY.md | No blocking issues but depends on resolving confidence logic contradiction |
| OPEN_WEBUI_SPEC.md | No blocking issues but workflow1 migration recommendation should be [FOR HUMAN REVIEW], not assumed |

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
- [[AI_USE_CASE_PROFILE|AI Use Case Profile]]
- [[ANTIGRAVITY_RULES|Antigravity Rules]]
- [[SESSION_STATE|Session State]]
