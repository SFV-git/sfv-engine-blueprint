---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Chat
HANDOFF_TO: Claude Code
---

# ULTRAPLAN BRIEF — AI STACK COMPLETION

> Claude Code reads this at session start. This is the complete brief for finishing the AI stack blueprint.
> All gap analysis and phase sequencing was done in Claude Chat 2026-05-29.
> Will is final authority. No canon writes without approval.

---

## MISSION

Finish planning the AI stack. Every gap below needs a blueprint doc written or an existing doc updated.
No dev work. No code. Planning documents only.
Phase 0 decisions need Will's input before writing.

---

## VAULT READS — DO FIRST

Before writing anything, read these in full:

- C:\SFV_BLUEPRINT\SESSION_STATE.md
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\AI_STACK_ARCHITECTURE_BLUEPRINT.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\AI_USE_CASE_PROFILE.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\MODEL_ROUTING.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\COST_ROUTING.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\RATE_LIMITS.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\RD_TERMINAL_ARCHITECTURE.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\ANTIGRAVITY_RULES.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\LOCAL_MODELS.md
- C:\SFV_BLUEPRINT\05_AI_LAYER\QUALITY_CONTROL.md
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\ENGINE_COMMUNICATION_MODEL.md
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\STACK_INTEGRATION_PLAN.md
- C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\MULTI_AGENT_WORKFLOW.md
- C:\SFV_BLUEPRINT\00_DEV_LOG\QUESTIONS_FOR_WILL.md

Also check: C:\SFV_BLUEPRINT\99_INBOX\HANDOFFS\ for any Claude Code diagnosis output on the confidence escalation issue.

---

## WHAT IS ALREADY CANON — DO NOT REBUILD

| Area | Doc | Status |
|---|---|---|
| Tier hierarchy (Antigravity→n8n→Ollama→Cloud) | AI_USE_CASE_PROFILE | ✅ CANON |
| Connection map + IPs + ports | AI_STACK_ARCHITECTURE_BLUEPRINT §1 | ✅ CANON |
| Routing decision tree (local/cheap/premium) | AI_STACK_ARCHITECTURE_BLUEPRINT §3 | ✅ CANON |
| Job envelope schema | AI_STACK_ARCHITECTURE_BLUEPRINT §4 | ✅ CANON |
| File-based comms (QUEUE/OUTPUTS/HANDOFFS) | ENGINE_COMMUNICATION_MODEL | ✅ CANON |
| Rate limits per tool | RATE_LIMITS | ✅ CANON (numbers INFERENCE) |
| Sentinel roles (4 sub-roles) | RD_TERMINAL_ARCHITECTURE | ✅ CANON APPROVED |
| Antigravity boundaries | ANTIGRAVITY_RULES | ✅ CANON |
| Storage allocation per drive | AI_STACK_ARCHITECTURE_BLUEPRINT §2 | ✅ CANON |
| Specialist model assignments | SESSION_STATE (workflow1 routing) | ✅ CANON |

---

## GAP INVENTORY

### 🔴 PHASE 0 — BLOCKERS (Will decides before writing)

**Gap 1 — Confidence escalation logic (BLOCKER)**
- 2/3 false escalations on trivial prompts (CLASSIFY + CODE routes)
- Claude Code sent diagnosis prompt at end of 2026-05-29 session
- Read HANDOFFS/ for output before proposing a fix
- DO NOT auto-patch. Present fix proposal to Will first.
- Target doc: extend AI_STACK_ARCHITECTURE_BLUEPRINT §3 OR new 05_AI_LAYER/CONFIDENCE_LOGIC.md

**Gap 2 — PostgreSQL migration (BLOCKER)**
- Flagged Critical in AI_STACK_ARCHITECTURE_BLUEPRINT §6 but no step-by-step plan
- Needs: backup procedure, migration script, rollback plan, validation checks
- Target doc: new 03_INFRASTRUCTURE/POSTGRES_MIGRATION.md

**Gap 3 — Docker install**
- Blocks Open WebUI, n8n-MCP, queue mode
- Will does the install (requires restart)
- Target doc: update existing docker references to CONFIRMED once done

---

### 🟠 PHASE 1 — RESILIENCE (write after Phase 0 decisions)

**Gap 4 — Failover model**
- Engine Body Ollama dies → R&D fallback mentioned but not wired in any doc
- n8n process crash recovery not documented
- Watchdog process not defined
- Target doc: new 03_INFRASTRUCTURE/FAILOVER_MODEL.md

**Gap 5 — Secrets management**
- n8n_env.ps1 has live API keys (Tavily, Perplexity confirmed)
- No rotation plan, no encryption at rest policy, no access control doc
- Target doc: new 03_INFRASTRUCTURE/SECRETS_POLICY.md

---

### 🟠 PHASE 2 — ROUTING GAPS (write after Phase 1)

**Gap 6 — Antigravity → n8n trigger spec**
- SESSION_STATE flags this as unwired
- No doc on how Antigravity calls n8n (Webhook? File drop? MCP server call? Auth?)
- Target doc: new section in STACK_INTEGRATION_PLAN or new 05_AI_LAYER/ANTIGRAVITY_N8N_TRIGGER.md

**Gap 7 — n8n-MCP integration spec**
- Listed as Phase 1 in AI_STACK_ARCHITECTURE_BLUEPRINT (czlonkowski/n8n-mcp via Docker)
- Which workflows get exposed? Which agents call it? Auth model?
- Target doc: new 03_INFRASTRUCTURE/N8N_MCP_SPEC.md

**Gap 8 — RESEARCH route (Perplexity vs Tavily)**
- Route listed in workflow1 (HANDOFFS escalation) but not fully specced
- Tavily API is live in n8n_env.ps1 — relationship to Perplexity unclear
- INFERENCE: Tavily = automated web search inside n8n, Perplexity = manual research intake. Confirm.
- Target doc: new 05_AI_LAYER/RESEARCH_ROUTE_SPEC.md

**Gap 9 — workflow3 (missing)**
- Workflows 1, 2, 4 exist and are imported. No workflow3.
- INFERENCE: was intended as RESEARCH/Perplexity handler. Confirm or correct before writing.
- FOR HUMAN REVIEW: ask Will before building this doc.

**Gap 10 — Gemini Flash direct-from-n8n**
- Routing tree lists Gemini Flash as Tier 4-cheap for bulk reformat/caption at scale
- Currently only accessed via Antigravity — no n8n→Gemini API integration specced
- Target doc: new section in AI_STACK_ARCHITECTURE_BLUEPRINT or 05_AI_LAYER/GEMINI_INTEGRATION.md

---

### 🟡 PHASE 3 — NEW LAYERS (write after Phase 2)

**Gap 11 — Open WebUI deployment spec**
- Listed as Phase 1 in AI_STACK_ARCHITECTURE_BLUEPRINT
- No auth model, no access policy, no routing rules (what goes through it vs direct Ollama)
- Target doc: new 03_INFRASTRUCTURE/OPEN_WEBUI_SPEC.md

**Gap 12 — Vector layer (Qdrant + embeddings)**
- Marked FUTURE in AI_STACK_ARCHITECTURE_BLUEPRINT §8
- No plan for: what gets embedded, when embedding runs, what queries the vector store, RAG vs semantic search vs dedup use case
- FOR HUMAN REVIEW: confirm this is in scope for ultraplan or defer to v2.0
- Target doc: new 05_AI_LAYER/VECTOR_LAYER_PLAN.md

**Gap 13 — Media pipeline spec (Whisper + FFmpeg)**
- Branch D in routing tree (Execute Command node → Whisper HTTP)
- No concrete spec: serial queue rules, faster-whisper migration path, video ingest entry point
- Target doc: new 04_WORKFLOWS/MEDIA_PIPELINE.md

---

### 🟡 PHASE 4 — OBSERVABILITY + GUARDRAILS

**Gap 14 — Monitoring stack deploy doc**
- Prometheus + Grafana + windows_exporter marked FUTURE
- Sentinel role defines the concept but no concrete deploy doc
- Target doc: new 03_INFRASTRUCTURE/MONITORING_STACK.md

**Gap 15 — Cost ceiling enforcement**
- "Set spend cap" mentioned but no automatic kill switch, no daily budget tracker, no alert thresholds
- FOR HUMAN REVIEW: hard kill-switch or alert-only? Will decides.
- Target doc: new 05_AI_LAYER/COST_CEILING_POLICY.md

**Gap 16 — Concurrency and queue mode design**
- Redis queue mode marked FUTURE
- PRIORITY field in job envelope schema is unused — no enforcement logic
- Max-concurrent task limit not documented anywhere
- Target doc: new section in AI_STACK_ARCHITECTURE_BLUEPRINT §4 or standalone doc

**Gap 17 — Output validation framework**
- QUALITY_CONTROL.md is UNCONFIRMED and scoped only to SFV_UGC
- No general "good output" criteria per task_type for the AI stack
- Target doc: extend QUALITY_CONTROL.md or new 05_AI_LAYER/OUTPUT_VALIDATION.md

---

### 🟢 PHASE 5 — POLISH

**Gap 18 — Prompt versioning convention**
- OLLAMA_PROMPTS/ folder exists with handoff_generator.txt
- No version control discipline, no A/B testing model
- Target doc: new section in OLLAMA_SETUP.md or new 05_AI_LAYER/PROMPT_VERSIONING.md

**Gap 19 — Model lifecycle policy**
- No plan for swapping qwen3:14b → newer model
- No eval criteria, no version lockfile
- Target doc: new section in LOCAL_MODELS.md

**Gap 20 — Disaster recovery + backup**
- n8n DB state, Ollama models, vault off-site backup
- Syncthing handles A↔B only — no off-site
- Target doc: new 03_INFRASTRUCTURE/DISASTER_RECOVERY.md

---

## DECISIONS WILL MUST MAKE BEFORE WRITING — FOR HUMAN REVIEW

Ask Will these before proceeding past Phase 0:

| # | Question | Blocks |
|---|---|---|
| D1 | Scope: all 20 gaps this session, or phase by phase? | All |
| D2 | Confidence fix: read HANDOFFS diagnosis + propose fix now, or separate session? | Gap 1 |
| D3 | workflow3: was it intentionally skipped, or should it be the RESEARCH handler? | Gap 9 |
| D4 | Vector layer: in scope for ultraplan or defer to v2.0? | Gap 12 |
| D5 | Cost ceiling: hard kill-switch or alert-only? | Gap 15 |
| D6 | New docs go in existing files (extend AI_STACK_ARCHITECTURE_BLUEPRINT) or new files per gap? | All |
| D7 | Tavily vs Perplexity: confirm INFERENCE — Tavily = automated in-n8n, Perplexity = manual intake? | Gap 8 |

---

## OUTPUT TARGETS (new files to create)

```
03_INFRASTRUCTURE/
  POSTGRES_MIGRATION.md       ← Gap 2
  FAILOVER_MODEL.md           ← Gap 4
  SECRETS_POLICY.md           ← Gap 5
  N8N_MCP_SPEC.md             ← Gap 7
  OPEN_WEBUI_SPEC.md          ← Gap 11
  MONITORING_STACK.md         ← Gap 14
  DISASTER_RECOVERY.md        ← Gap 20

04_WORKFLOWS/
  MEDIA_PIPELINE.md           ← Gap 13

05_AI_LAYER/
  CONFIDENCE_LOGIC.md         ← Gap 1
  ANTIGRAVITY_N8N_TRIGGER.md  ← Gap 6
  RESEARCH_ROUTE_SPEC.md      ← Gap 8
  GEMINI_INTEGRATION.md       ← Gap 10
  VECTOR_LAYER_PLAN.md        ← Gap 12 (if approved)
  COST_CEILING_POLICY.md      ← Gap 15
  OUTPUT_VALIDATION.md        ← Gap 17
  PROMPT_VERSIONING.md        ← Gap 18
```

Existing files to extend:
- AI_STACK_ARCHITECTURE_BLUEPRINT.md — Gap 16 (concurrency section)
- LOCAL_MODELS.md — Gap 19 (model lifecycle section)
- QUALITY_CONTROL.md — Gap 17 (or replaced by OUTPUT_VALIDATION.md)

---

## EXECUTION RULES FOR CLAUDE CODE

1. Read all vault files listed above FIRST. Do not write from memory.
2. Ask Will D1–D7 before starting Phase 1.
3. Write one doc at a time. Report to Will after each. Wait for approval before next.
4. Label all content: CANON / UNCONFIRMED / INFERENCE / FOR HUMAN REVIEW.
5. No dev work. No scripts. Blueprint docs only.
6. Git commit at end of session after Will approves all docs.
7. Update SESSION_STATE.md at session end with what was completed.

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[DATABASE_ARCHITECTURE|Database Architecture]]
- [[QUESTIONS_FOR_WILL|Questions for Will]]
- [[STACK_INTEGRATION_PLAN|Stack Integration Plan]]
- [[RATE_LIMITS|Rate Limits]]
- [[MODEL_ROUTING|Model Routing]]
