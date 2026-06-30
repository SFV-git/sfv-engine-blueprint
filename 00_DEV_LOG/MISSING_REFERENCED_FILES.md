---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple, Prompt A)
---

# MISSING / REFERENCED-BUT-ABSENT — SFV_BLUEPRINT SNAPSHOT

Four categories per the runbook quality bar.

---

## 1. REFERENCED BUT ABSENT (files other docs point at; not in snapshot)

| Missing item | Referenced by | Impact |
|---|---|---|
| `00_DEV_LOG/ORPHANS.md` | PENDING_REVIEW §2 ("awaiting categorization"), canon-control rule CONNECTED FILES, find_orphans.py output target, SESSION_STATE 05-25 | Dead reference. Either run find_orphans.py and commit, or strip references. |
| `workflow3` (n8n JSON) | RESEARCH_ROUTE_SPEC (confirmed dedicated handler), SESSION_STATE next-actions, N8N_MCP exposure table | By design — not yet built. RESEARCH tasks currently dead-end into HANDOFFS (correct interim behavior, confirmed in workflow1 Non-Ollama Handler). |
| `06_APPS/ugc_preproduction/` (+ data/*.json) | UGC_PRE_PRODUCTION.md (CANON) file-location spec | By design — Blueprint Lock. Build target only. |
| `prometheus_alert_writer.ps1` | MONITORING_STACK §6 | Dev-phase build item. |
| `COMPRESSED_CONTEXT_DRAFT.md` | N8N_BLUEPRINT Workflow 5 spec | workflow5 not built; fine. |
| `00_DEV_LOG/MODEL_EVAL_[date].md` | MODEL_LIFECYCLE_POLICY swap procedure | Procedural — none generated yet; expected. |
| Telemetry JSON logs (`D:\SFV_ACTIVE\LOGS\TELEMETRY\`) + emission code in ingest.py | RD_TERMINAL_ARCHITECTURE Roles 1 & 3 | Sentinel Roles 1/3 have no data source until ingest.py emits telemetry. Unblocked dependency, undocumented as a gap anywhere. |
| Scheduled Task for backup_n8n.ps1 | DISASTER_RECOVERY §4, A2 | Script exists; schedule doesn't. **The n8n DB backup gap is still open.** |
| GitHub remote + last-push state | DISASTER_RECOVERY assumes GitHub IS the off-site; UNCONFIRMED.md flags verification | [UNVERIFIABLE FROM SNAPSHOT — .git excluded from extraction]. Verify `git remote -v` + push freshness on Engine Body. |
| Robocopy nightly task definition | AI_STACK §2, DR §2/§4 reference it as "already configured and running" | No script/task file in vault. If it lives only in Task Scheduler, it's machine-local intelligence — violates Rule 12 spirit. Export the task XML to vault. |
| `SFV_N8N.vbs` + vault_watcher VBS launcher | SESSION_STATE 05-29 (auto-start on login) | Startup-folder artifacts not in vault. Same Rule 12 concern as above. |
| Zenfolio QR card stock / export format / per-day event template | Memory + UNCONFIRMED.md resolution line, MYTHOS prompt Scenario A | See §3 — the whole locked system is undocumented. |

## 2. EMPTY STUBS (exist, zero content)

| File | Referenced by | Action |
|---|---|---|
| `99_INBOX/DATABASE_ARCHITECTURE.md` (0 bytes) | — (orphan stub) | Delete or write; currently noise that also violates "never create files without a status tag." |
| `99_INBOX/OLLAMA_STAGING/AI_BRIDGE_BUILD_PLAN.md` (0 bytes) | Wikilinked from N8N_BLUEPRINT CONNECTED FILES | Dead-content link. Delete + strip link, or write the plan. |
| `99_INBOX/OLLAMA_STAGING/` generally | — | Single empty file inside; folder purpose undefined anywhere. |

## 3. IMPLIED SYSTEMS NOT YET FORMALIZED (decided/locked in conversation, no vault doc)

| Implied spec | Evidence it's decided | Gap |
|---|---|---|
| **SFV_EVENTS Zenfolio QR delivery workflow** — the entire locked multi-day event system (QR cards, Golden Rule, per-day events, Cam1_/Cam2_/Cam3_ prefixes, 3 laptops/1 account, same-day model, instant-delivery-as-upsell, face-rec rejected) | UNCONFIRMED.md resolved line: "Zenfolio Sports & Events (QR workflow) for multi-day events"; MYTHOS_FORWARD_PROMPT Scenario A walks it | **No 04_WORKFLOWS doc exists.** This is a LOCKED operational system for a primary money branch living only in chat history + memory. Highest-priority formalization candidate — it's exactly the kind of thing Blueprint Lock exists to capture. Also: Zenfolio Advanced caps/pricing/QR export format flagged for verification. |
| **Theory Runs protocol** | Approved methodology per memory; scenarios A/B/C embedded in MYTHOS_FORWARD_PROMPT | No standalone protocol doc (08_TESTS is the natural home). MYTHOS prompt holds the only spec. |
| **Pixieset same-day Lightroom workflow** (Adaptive Portrait preset + AI masking sync, Generative Remove, sRGB q80–85 2560px export) | Executed for Morning Walk/Shamar per memory; EXPORT.md remains UNCONFIRMED with TBD specs | The proven export recipe exists in practice but EXPORT.md still says specs await confirmation. Battle-tested numbers should be promoted into EXPORT.md. |
| **workflow5** identity | N8N_BLUEPRINT defines workflow5 = Blueprint Sync; OUTPUT_VALIDATION proposes workflow5 = nightly validation | Two different systems claim the same name. Neither built. Resolve naming before either is. |
| **client_facing flag wiring** | Blueprint §3 + CONFIDENCE_LOGIC reference it; JOB_ENVELOPE_SPEC defines the field | workflow1 JSON does NOT check `client_facing` — defined but unenforced. Either wire it into workflow1 or mark deferred. |
| **Decision-record consolidation** | DECISIONS.md stops 05-24; later locks scatter across QUESTIONS_FOR_WILL resolved blocks, PROPOSALS, SESSION_STATE LOCKED lists | "Single source of truth" (Rule 06) for decisions is currently four files. Needs a designated ledger or an explicit rule about which file owns decision records. |

## 4. AMBIGUOUS NAMES / ALIASES (same thing, multiple names — or one name, multiple things)

| Term | Collision |
|---|---|
| `%SFV_ROOT%` | ENVIRONMENT_CONFIG: `C:\SFV_BLUEPRINT` (the vault). STORAGE_ARCHITECTURE + RULES Rule 04 + HARDWARE_CONTEXT: used as "current drive root" for active storage trees. Two CANON meanings. → Contradiction C1. |
| `workflow2` | Deployed: Model Pre-Warm cron. N8N_BLUEPRINT (FHR): File Watcher/Ingest trigger. → C2. |
| `workflow5` | N8N_BLUEPRINT: Blueprint Sync. OUTPUT_VALIDATION: nightly validation pass. → C2. |
| "queue" | `99_INBOX\QUEUE\*.json` (live, n8n) vs `TASK_QUEUE.md` (LEGACY, daemon). Now labeled, but 4 stale PENDING tasks still sit in TASK_QUEUE.md inviting daemon re-runs. |
| Workflow IDs | Vault JSON ids (static UUIDs: 7a8b9c…, 4a1b2c…) vs n8n-runtime ids (LJH60a1N…/Eb78T9Fn…/GBzP0Qam…/oUw9qPMw…/6OtCtcsw…). SESSION_STATE 06-03 block and later state disagree on which runtime IDs are live. → C4 / A6. |
| "Sentinel" monitoring home | RD_TERMINAL_ARCHITECTURE (CANON): dashboards/Prometheus concept on Node B. MONITORING_STACK (FHR, decision D-B): Prometheus+Grafana on Node A. → C5. |
| R&D Terminal model roster | LOCAL_MODELS (CANON, post-Perplexity): qwen3:8b + qwen3:14b, drop coder. TWO_TERMINAL plan B2 (DRAFT): qwen3:8b + qwen2.5-coder:7b. FAILOVER_MODEL: 14b-only fallback. → C8 / open Q17. |
| "SFV Studio" vs "SFV_STUDIO" | Locked: underscore caps. Snapshot is clean on this — no violations found. (Recorded so it stays checked.) |

## CONNECTED FILES
- [[SESSION_STATE|Session State]]
- [[DASHBOARD|Dashboard]]
