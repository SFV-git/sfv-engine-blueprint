---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple, Prompt A)
---

# BLUEPRINT MANIFEST — SFV_BLUEPRINT SNAPSHOT 2026-06-10

Every meaningful file in the snapshot. Columns:
**Status** = STATUS tag in the file. **Stage** = NOW / P1 / P2 / FUTURE / SHARED (see README_FIRST).
**Conf** = authority confidence: HIGH (canon, consistent), MED (canon, minor drift found),
STALE (canon, confirmed drift — see audit), LOW (FHR/UNCONFIRMED/RESEARCH).
**Depends-on/Dependents** = key downstream files that break if this changes.

---

## ROOT — CONTROL & CONTEXT

| File | Purpose | Status | Stage | Conf | Key dependents |
|---|---|---|---|---|---|
| SESSION_STATE.md | Session continuity + standing orders + locked decisions | CANON v0.6.0 | SHARED | STALE | Every session start; self-flags post-06-03 write-back gap |
| DASHBOARD.md | At-a-glance attention list (Dataview) | CANON | SHARED | HIGH | Session protocol |
| MASTER_CONTEXT.md | What SFV is, two nodes, money makers, Claude role | CANON | SHARED | STALE | COMPRESSED_CONTEXT; near-term targets + R&D model list outdated |
| COMPRESSED_CONTEXT.md | Cheap-call context (rewritten v0.3.0 in 06-09 audit) | CANON v0.3.0 | SHARED | HIGH | All model calls; pending PROPOSAL 008 ratification |
| CLAUDE.md | Claude Code session context + rules | (no tag) | SHARED | MED | Claude Code; "WHAT TO BUILD FIRST" references May 28 — stale |
| ANTIGRAVITY.md | Antigravity session context + rules | (no tag) | SHARED | HIGH | Antigravity sessions; "MAY 28 DEADLINE" line stale |
| HARDWARE_CONTEXT.md | Node specs, drive inventory, electricity constraint | CANON | SHARED | MED | STORAGE_ARCHITECTURE, UPGRADE_CHECKPOINTS; monitor-count [UNCONFIRMED] inline despite Q002 resolved |
| README.md | Vault usage + folder map | CANON | SHARED | HIGH | — |
| index.md | Quartz/nav index | (title only) | SHARED | HIGH | serve_vault.ps1 |
| CHANGELOG.md | Change history (last entry 05-29 ultraplan) | CANON | SHARED | MED | file-editing rule requires entries; post-05-29 changes missing |
| USAGE_OPTIMIZATION.md | Token/usage strategy (OPT 01–06) | CANON | SHARED | HIGH | COST_ROUTING |
| .claude/rules/*.md (5) | blueprint-only, canon-control, file-editing, human-approval, no-assumptions | CANON | SHARED | HIGH | Every Claude Code session |
| .claude*/settings.local.json | Claude Code allow-list (32 rules) | — | NOW | HIGH | Claude Code; contains command allow-list, no secrets, but machine-specific |
| .gitignore / gitignore_for_sfv.txt | Excludes n8n_env.ps1, .obsidian, .smart-env | — | SHARED | HIGH | Secrets policy |

## 01_CANON_RULES

| File | Purpose | Status | Stage | Conf |
|---|---|---|---|---|
| RULES.md | Rules 01–12 governing the build | CANON | SHARED | HIGH |

## 02_BRANCHES

| File | Purpose | Status | Stage | Conf | Notes |
|---|---|---|---|---|---|
| BRANCH_OUTPUTS.md | Engine-level scale, branch summary table, repost groups, cross-branch rules, per-branch naming | CANON | SHARED | HIGH | Hub reference for all branches |
| MYTHOLOGY.md | Hub account def (SFV_abbass, Level 1) | CANON | NOW | HIGH | Catch logic [UNCONFIRMED] |
| SFV_LIVE.md | Event coverage def (Level 3.5) | CANON | NOW | HIGH | — |
| SFV_EVENTS.md | On-site portraits def (Level 5–6.5, money maker) | CANON | NOW | MED | Delivery [UNCONFIRMED] in file but resolved in UNCONFIRMED.md (Pixieset + Zenfolio QR) — file not updated; pricing open |
| SFV_ATHLETICS.md | Sports coverage def (3.5) | CANON | NOW | HIGH | — |
| SFV_STUDIO.md | Studio production def (5.5, growth) | CANON | NOW | HIGH | Morning Walk section now historical |
| SFV_UGC.md | Primary money engine def (6.5, growth) | **UNCONFIRMED** | NOW | LOW | Handle + pricing open; primary revenue branch is the only UNCONFIRMED branch |
| SFV_ARCHIVE.md | Portfolio def (3.5) | CANON | NOW | HIGH | Human-taste protection clause |
| SFV_WORLD.md | Alias/life def (2.5) | CANON | NOW | HIGH | are.na overflow (Proposal 005 approved) |
| SFV_404.md | Experimental def (2.5) | CANON | NOW | MED | IG-account [UNCONFIRMED] inline despite Q001 resolved 05-27 |

## 03_INFRASTRUCTURE

| File | Purpose | Status | Stage | Conf | Notes |
|---|---|---|---|---|---|
| AI_STACK_ARCHITECTURE_BLUEPRINT.md | Master architecture: hub-and-spoke, connection map, endpoint registry, storage alloc, routing tree, gaps, action sequence | CANON v1.1 | SHARED | HIGH | IPs fixed to .246 (P008); §3 defers to CONFIDENCE_LOGIC — 0.75 contradiction resolved |
| ENGINE_COMMUNICATION_MODEL.md | File-based comms: QUEUE/OUTPUTS/HANDOFFS, status tags (unified), routing rules, cost order | CANON | SHARED | HIGH | TASK_QUEUE marked LEGACY (P008) |
| STORAGE_ARCHITECTURE.md | Drive roles, tiers, per-branch folder tree, redundancy | CANON | SHARED | **STALE** | Uses `%SFV_ROOT%\ACTIVE_STORAGE` — contradicts ENVIRONMENT_CONFIG's SFV_ROOT=C:\SFV_BLUEPRINT. See contradiction C1 |
| NAMING_CONVENTIONS.md | All file/folder/caption naming templates | CANON | SHARED | HIGH | ingest.py, all workflows |
| ENVIRONMENT_CONFIG.md | The path variable registry (locked drive map) | CANON v0.2.0 | SHARED | HIGH | Every script; C1 partner doc |
| METADATA_SYSTEM.md | EXIF + engine metadata, DB IDs, sidecar plan | UNCONFIRMED | P2 | LOW | Supabase schema TBD |
| STACK_INTEGRATION_PLAN.md | Full-stack setup V1/V2, Claude routing, daily workflow | CANON | SHARED | MED | Some sections historical (plugin installs etc.) |
| MULTI_AGENT_WORKFLOW.md | Tool interaction map, session phases, delivery example, Google-tools verdicts | CANON | SHARED | HIGH | — |
| CONCURRENCY_QUEUE_SPEC.md | PRIORITY enforcement, max-concurrent by task_type, Redis future | CANON | P1/P2 | HIGH | MERGE_INTO Blueprint §4 pending; values [INFERENCE] |
| DISASTER_RECOVERY.md | Backup state, gaps, recovery runbooks | FOR HUMAN REVIEW | SHARED | LOW | Bitwarden decision recorded; n8n backup gap is P1 of the whole system |
| DOCKER_INSTALL_CHECKLIST.md | Install steps + what unlocks | CANON | P1 | HIGH | Blocks Open WebUI, n8n-MCP, Redis, Qdrant |
| FAILOVER_MODEL.md | Ollama Node B fallback spec + watchdog reality reconciliation | FOR HUMAN REVIEW | P1 | LOW | Fallback DEAD until R&D Ollama reinstalled (self-flagged) |
| MONITORING_STACK.md | Prometheus/Grafana on Node A (D-B), windows_exporter, thresholds | FOR HUMAN REVIEW v0.2 | P2 | LOW | Conflicts with RD_TERMINAL Role 1 location — C5 |
| N8N_MCP_SPEC.md | czlonkowski/n8n-mcp deploy, exposure policy, auth | CANON | P1 | MED | Will's own A1 verdict: hold at FHR until prereqs CANON — status says CANON. C-note in matrix |
| OPEN_WEBUI_SPEC.md | Unified inference endpoint, auth, workflow1 migration question | FOR HUMAN REVIEW | P1 | LOW | Open Q19 |
| POSTGRES_MIGRATION.md | Backup → install → migrate → validate → rollback | FOR HUMAN REVIEW | NOW→P1 gate | LOW | THE gating doc; Option A (native) leans CANON per Ultraplan Review |
| SECRETS_POLICY.md | Key inventory, storage rules, rotation, Bitwarden | CANON | SHARED | HIGH | Violated by this snapshot's contents — audit S1 |
| n8n_env.ps1 | **LIVE SECRETS** (13 vars incl. Tavily key) | gitignored | NOW | — | **SHOULD NOT BE IN SNAPSHOTS** — audit S1 |
| n8n_env.template.ps1 | Safe placeholder twin | — | SHARED | HIGH | — |
| start_n8n.ps1 | n8n launcher (NODES_EXCLUDE, OLLAMA vars, ALLOW_BUILTIN=fs,path,os) | — | NOW | MED | Does NOT source n8n_env.ps1 → split-brain env. C14 |
| watchdog.ps1 | n8n+Ollama health check / auto-restart, 5-min loop | — | NOW | HIGH | Manual window only — A5 pending |
| serve_vault.ps1 | Quartz build + serve vault site :8080 | — | NOW | HIGH | Requires C:\SFV_QUARTZ |
| n8n_workflows/workflow1_queue_processor.json | THE queue processor (route by task_type, confidence, validation) | — | NOW | MED | Has UTF-8 BOM + mojibake; already contains think-strip + Phase-1 validation. Audit F4/F5 |
| n8n_workflows/workflow2_model_prewarm.json | 5-min pre-warm cron, pings 3 models | — | NOW | HIGH | Clean UTF-8, no id field |
| n8n_workflows/workflow4_output_monitor.json | OUTPUTS watcher → ESCALATED items log | — | NOW | MED | BOM + mojibake; vault JSON has triggerOn fix history unclear — A6 |

## 04_WORKFLOWS

| File | Purpose | Status | Stage | Conf | Notes |
|---|---|---|---|---|---|
| INGEST.md | Bulletproof ingest flow, Morning Walk case, script spec, failure behavior | CANON v0.2.0 | NOW | HIGH | Morning Walk sections historical |
| CULLING.md | Technical-cull flow (AI) + creative cull (Will) | UNCONFIRMED | P2 | LOW | — |
| DELIVERY.md | Per-branch delivery; scheduling = 8+ accounts | UNCONFIRMED | NOW | **STALE** | Scheduling [UNCONFIRMED] inline but Later chosen 05-26; SFV_EVENTS line predates Zenfolio decision |
| EXPORT.md | Export specs per branch (photo/video) | UNCONFIRMED | NOW | LOW | Specs await Will (Q13) |
| ARCHIVE.md | ACTIVE→WARM→COLD tiering | UNCONFIRMED | P2 | LOW | Porsche SSD blocked |
| MEDIA_PIPELINE.md | Whisper branch: serial lock, FFmpeg, faster-whisper path | FOR HUMAN REVIEW | P2 | LOW | Whisper port [INFERENCE] — blocks build (A4) |
| N8N_BLUEPRINT.md | Perplexity-sourced n8n architecture: 5 workflows, wikilink fixes, token rules | FOR HUMAN REVIEW | SHARED | LOW | **Workflow numbering conflicts with deployed reality** — C2; UI-build-not-API-import guidance partially superseded |
| OUTPUTS_RETENTION.md | Retention rules + 13-file cleanup list | FOR HUMAN REVIEW | NOW | LOW | Cleanup awaiting approval |
| UGC_PRE_PRODUCTION.md | Pre-production manager full spec (entities, intake, PDFs, build order) | CANON | P1 | HIGH | Build target 06_APPS/ does not exist yet (by design) |

## 05_AI_LAYER

| File | Purpose | Status | Stage | Conf | Notes |
|---|---|---|---|---|---|
| AI_USE_CASE_PROFILE.md | Tier hierarchy (Antigravity T1 … Ollama T5) + routing tree | CANON v0.2.0 | SHARED | HIGH | — |
| ANTIGRAVITY_N8N_TRIGGER.md | File-drop dispatch spec, webhook future | FOR HUMAN REVIEW | NOW | MED | Schema now defers to JOB_ENVELOPE_SPEC (redundancy fixed) |
| ANTIGRAVITY_RULES.md | Antigravity capabilities, banned actions, approval gate | CANON v0.2.0 | SHARED | HIGH | — |
| CLAUDE_API.md | Approved/never use-cases, cost mgmt | CANON | SHARED | HIGH | — |
| CONFIDENCE_LOGIC.md | Keyword escalation spec (default HIGH) | CANON (confirmed 06-03) | NOW | **STALE** | Doc lists think-strip as unconfirmed future fix; vault JSON ALREADY implements it. C3 |
| COST_CEILING_POLICY.md | Alert-only policy, thresholds, COST_ALERTS format | FOR HUMAN REVIEW | SHARED | MED | §2.4 heading fixed to Engine Body (P008 era) |
| COST_ROUTING.md | Model tiers + task routing + session cost rules | CANON | SHARED | HIGH | — |
| GEMINI_INTEGRATION.md | n8n→Gemini Flash direct path spec | FOR HUMAN REVIEW | P1 | LOW | Key not set (Q20) |
| JOB_ENVELOPE_SPEC.md | Canonical envelope schema, optional fields, status values | FOR HUMAN REVIEW | SHARED | HIGH | Single-source-of-truth fix from Ultraplan Review — should be promoted with priority |
| LOCAL_MODELS.md | R&D Terminal roster (8b+14b), VRAM rules, install steps | CANON | NOW | HIGH | Roster conflicts with TWO_TERMINAL plan B2 — C8 |
| MODEL_LIFECYCLE_POLICY.md | Lock/eval/swap/rollback procedure, VRAM budget | FOR HUMAN REVIEW | SHARED | MED | RTX 5080 16GB table |
| MODEL_LOCK.md | Active model registry (3 locked) | FOR HUMAN REVIEW | NOW | HIGH | DR recovery checklist |
| MODEL_ROUTING.md | Task→tool→cost table | CANON | SHARED | MED | Several rows route to "R&D terminal" for tasks now on Engine Body — pre-pivot residue |
| MYTHOS_FORWARD_PROMPT.md | 1M-context forward-planning prompt (4 deliverables) | CANON | SHARED | HIGH | Contains Syncthing Device ID; Theory Runs scenarios A/B/C |
| MYTHOS_PROTOCOL.md | Full-vault audit role, routing rule, cadence | FOR HUMAN REVIEW | SHARED | MED | Open Q25 |
| OLLAMA_PROMPTS/handoff_generator{_v1,_CURRENT,}.txt + PROMPT_CHANGELOG.md | Versioned prompt set (P008 implementation) | — | NOW | HIGH | First versioned prompt |
| OLLAMA_SETUP.md | Ollama limits, model, system prompt, Obsidian plugin | CANON | SHARED | MED | "R&D terminal" framing predates Engine-Body-primary pivot |
| OUTPUT_VALIDATION.md | Per-task_type validity criteria, 3 phases | CANON | NOW | HIGH | Phase 1 already in workflow1 JSON |
| PROMPT_VERSIONING.md | vN/_CURRENT/changelog discipline, A/B model, qwen3 principles | CANON | SHARED | HIGH | Implemented |
| QUALITY_CONTROL.md | Client-delivery QC for UGC/EVENTS | UNCONFIRMED | P1 | LOW | Additive after OUTPUT_VALIDATION |
| RATE_LIMITS.md | Per-tool limits + routing order + daily budget | CANON | SHARED | MED | All numbers [INFERENCE]; qwen3 8K-context claim likely stale |
| RD_TERMINAL_ARCHITECTURE.md | Sentinel: 4 roles (telemetry, client gateway, optimizer, trading sandbox) | CANON v0.2.0 (P007 approved) | P2/FUTURE | MED | Role 1 dashboard location conflicts with MONITORING_STACK D-B — C5 |
| RESEARCH_ROUTE_SPEC.md | Tavily/Perplexity split (D7), workflow3 confirmed dedicated | FOR HUMAN REVIEW | P1 | HIGH | workflow3 = D3=C2 confirmed 05-29 |
| VECTOR_LAYER_PLAN.md | Qdrant + nomic-embed-text: what/when/who queries | FOR HUMAN REVIEW | P2 | MED | Storage now aligned to C:\ |

## 06_TOOLS / 07_SCALING / 08_TESTS / 09_PROMPTS / 10_REFERENCES / 11_VERSIONS / 12_DATABANKS

| File | Purpose | Status | Stage | Conf | Notes |
|---|---|---|---|---|---|
| 06_TOOLS/TOOLBOX.md | Every tool considered | CANON | SHARED | MED | Ghostty rows stale vs TOOL_STATUS |
| 06_TOOLS/TOOL_STACK.md | Active/confirmed tools | CANON | SHARED | STALE | n8n listed FUTURE (it's live); scheduling UNCONFIRMED (Later chosen) |
| 06_TOOLS/TOOL_STATUS.md | Status registry per tool | CANON | SHARED | **STALE** | "Last updated 05-24": Docker UNCONFIRMED (approved), n8n FUTURE (active), Later RESEARCHING (chosen), Ollama "R&D terminal" (Engine Body primary) |
| 06_TOOLS/INTEGRATIONS.md | External connections | UNCONFIRMED | SHARED | STALE | Tailscale/scheduling rows pre-date resolutions |
| 07_SCALING/BRANCH_INDEPENDENCE.md | Owns/shares per branch, add-branch steps | CANON | FUTURE | HIGH | — |
| 07_SCALING/NATIONWIDE.md | Halifax→Maritimes→Midwest, hiring phases | CANON | FUTURE | HIGH | — |
| 07_SCALING/OPERATOR_MODEL.md | ~40% rev share, remote QC, ownership rule | CANON | FUTURE | HIGH | — |
| 08_TESTS/PAPER_TRIAL_RUNS.md | Paper-trial method + Trial 01/02 | CANON | SHARED | MED | Both trials still "NOT YET RUN" though events completed — record vs reality gap |
| 08_TESTS/FAILURE_TESTS.md / EDGE_CASES.md / BUILD_READINESS_CHECKLIST.md | Failure behaviors, edge cases, pre-build gate | UNCONFIRMED | SHARED | LOW | Theory Runs protocol will supersede/feed these |
| 09_PROMPTS/* (6 files) | Prompt libraries per tool (Claude, Code, Ollama, ChatGPT, extraction, research) | CANON (RESEARCH_PROMPTS UNCONFIRMED) | SHARED | HIGH | OLLAMA_PROMPTS.md duplicates system prompt also in OLLAMA_SETUP — single-source candidate |
| 10_REFERENCES/* (4 files) | Case studies, 10 lessons, links, tool research | RESEARCH | SHARED | HIGH | Reference-only per canon-control |
| 11_VERSIONS/ROADMAP.md | v0.x→v10.x phase ladder | CANON | SHARED | STALE | v1.x dated "MAY→EARLY JUNE"; milestones passed; phase markers drifted vs live n8n reality |
| 11_VERSIONS/UPGRADE_CHECKPOINTS.md | Hardware/infra upgrade triggers | CANON | SHARED | HIGH | — |
| 11_VERSIONS/VERSION_LOG.md | What happened (only v0.1.0 entry) | CANON | SHARED | STALE | No entries since 05-24 despite major milestones |
| 12_DATABANKS/* (7 files) | Content/taste/client/brand/research/training bank architecture | UNCONFIRMED | P1/P2 | LOW | Brandon Bellotti + ProEdge profiles seeded in CLIENT_BANKS |

## 00_DEV_LOG

| File | Purpose | Status | Conf | Notes |
|---|---|---|---|---|
| QUESTIONS_FOR_WILL.md | A1–A6 urgent + open decisions 15–25 + resolved archive | CANON v0.3.0 | HIGH | The decision queue — gates everything |
| DECISIONS.md | Locked decisions (05-24 set) | CANON | MED | No entries after 05-24; later decisions live in QUESTIONS/PROPOSALS/SESSION_STATE — fragmentation |
| UNCONFIRMED.md | Open items, reconciled 06-09 | UNCONFIRMED v0.2.0 | HIGH | Zenfolio resolution recorded here ONLY — no workflow doc exists |
| PENDING_REVIEW.md | 05-29 grep sweep: 19 UNCONFIRMED files, ~50 items | FOR HUMAN REVIEW | MED | References ORPHANS.md which doesn't exist |
| REJECTED_CHANGED.md | Rejected/changed directions record | CANON | HIGH | — |
| DEV_LOG.md | Session 001 only | CANON | STALE | Dead log — superseded by SESSION_STATE in practice |
| ULTRAPLAN_BRIEF.md | The 20-gap brief (Chat→Code handoff) | FOR HUMAN REVIEW | HIGH | Historical artifact; executed |
| ANTIGRAVITY_SETUP_GUIDE.md | Step-by-step Antigravity + ingest build guide | CANON | HIGH | — |
| 2026-06-03_TWO_TERMINAL_ATTACK_PLAN.md | Verification-chain plan: both nodes + overnight loop | DRAFT | MED | B2 model list conflicts with LOCAL_MODELS — C8; open questions 1–6 partially answered by perplexity_verification_response |
| 2026-05-25_TODAY_CONTROL.md / 2026-05-27_SESSION_END.md / CLAUDE_CODE_SESSION_2026-05-29.md | Session artifacts | — | HIGH | Historical |
| SEMANTIC_LINKS_* (9 small files) | Wikilink-suggestion worker tasks/results | — | LOW | Tooling residue; candidates for archive |
| WATCHDOG_LOG.md | Watchdog event log (48 bytes — header only) | — | HIGH | Watchdog ran briefly or log rotated |

## FOR_HUMAN_REVIEW

| File | Purpose | Status | Conf | Notes |
|---|---|---|---|---|
| PROPOSALS.md | P008 (ratify-or-revert audit fixes) + approved P002/4/5/6/7 + deferred P001/P003 | CANON v0.2.0 | HIGH | **P008 is the gate on everything from 06-09** |
| ULTRAPLAN_REVIEW.md | Antigravity Opus audit of 19 docs: contradictions, ready/not-ready lists | FOR HUMAN REVIEW | HIGH | Several findings since fixed (paths, §2.4, job-envelope single-source); others still open |

## 99_INBOX

| File/Group | Purpose | Conf | Notes |
|---|---|---|---|
| QUEUE/ (10 test JSONs + DONE/ 3) | Job envelopes; TEST_* validation set | HIGH | TEST_CLASSIFY_002 + TEST_CODE_004 = the confidence-fix proof pair |
| OUTPUTS/ (21 files) | Results incl. 13 triplicates pending OUTPUTS_RETENTION approval | MED | Keep/delete list already written |
| HANDOFFS/ (4 JSONs) | Escalation records incl. CC-TEST-002 (pre-fix false escalation evidence) | HIGH | — |
| DECISION_LOG.md | Routing decision rows | HIGH | workflow1 write-back target |
| OLLAMA_RESULTS.md (30KB) | Daemon-era outputs; early UNSURE results = daemon READ: limitation | HIGH | Legacy path |
| TASK_QUEUE.md | LEGACY daemon queue (4 stale semantic-link tasks still PENDING) | HIGH | Marked LEGACY in ENGINE_COMM; stale tasks should be cleared/archived |
| OVERNIGHT_DIRECTIVE.md | Autonomous-loop permissions/prohibitions | ACTIVE | HIGH — clean boundary doc |
| COST_ALERTS.md / FAILOVER_LOG.md | Append-only logs (headers only, no rows) | CANON | Created, never fired — consistent with alert mechanisms not yet wired |
| perplexity_verification_response.md (12KB) | Step-3 verification of TWO_TERMINAL plan (model roster, NODES_EXCLUDE, Syncthing race) | HIGH | Source of the *.json glob + fsWatcherDelayS guidance |
| DATABASE_ARCHITECTURE.md | **EMPTY (0 bytes)** | — | Stub — see MISSING_REFERENCED_FILES |
| OLLAMA_STAGING/AI_BRIDGE_BUILD_PLAN.md | **EMPTY (0 bytes)** | — | Wikilinked from N8N_BLUEPRINT — dead link content |
| Scripts: ingest.py (17KB) | The ingest implementation (v2, Gemini-review-fixed) | HIGH | Spec: INGEST.md |
| Scripts: ollama_daemon.py / ollama_queue_test.py / ollama_wrapper.py / n8n_import.py / n8n_retry.py / run_session.py / review_tool.py / setup_stack.py / vault_watcher.py / backup_n8n.ps1 / backfill_wikilinks.py / find_orphans.py / fix_floating.py / fix_all_floating.py / semantic_links*.py | Automation tooling per SESSION_STATE history | MED | backup_n8n.ps1 built-not-scheduled (A2); find_orphans.py output (ORPHANS.md) never generated/committed |
| RAW_IDEAS / SCRATCHPAD / TO_REVIEW / CHAT_EXTRACTS / SFV Engine.md / TEMPLATE_DEFAULT | Inbox stubs | LOW | — |

## NESTED ARTIFACT

| Item | Note |
|---|---|
| SFV_BLUEPRINT/SFV_BLUEPRINT/Welcome.md | Accidental Obsidian vault-in-vault (a stray "open folder as vault" created it 22:41 during zip prep). Safe to delete on Engine Body. |

## CONNECTED FILES
- [[SESSION_STATE|Session Continuity & Standing Orders]]
- [[COMPRESSED_CONTEXT|Cheap-Call Context]]
- [[MASTER_CONTEXT|SFV Overview & Claude Role]]
- [[RULES|Core Build Rules 01–12]]
- [[HARDWARE_CONTEXT|Node Specs & Electricity Constraints]]
- [[STORAGE_ARCHITECTURE|Storage System Design]]
- [[UPGRADE_CHECKPOINTS|Version Upgrade Milestones]]
- [[COST_ROUTING|Token/Usage Strategy Dependencies]]
