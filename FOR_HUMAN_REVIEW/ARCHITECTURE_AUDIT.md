---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-10
CREATED_BY: Claude Fable 5 (Session Maple, Prompt B)
SCOPE: Full snapshot read — all 220 files including workflow JSONs, scripts, logs
SEVERITY: 🔴 critical · 🟠 high · 🟡 medium · 🟢 low
ACTION: FIX NOW · DEFER · VERIFY-AT-IMPL
---

# ARCHITECTURE AUDIT — SFV ENGINE BLUEPRINT (SNAPSHOT 2026-06-10)

## STRENGTHS (short, then we get to work)

The status-tag discipline (CANON/UNCONFIRMED/FHR) is real and mostly honored — rare for a
solo vault. The file-based communication model is genuinely good architecture: decoupled,
restart-safe, inspectable, and it survived the confidence-bug incident exactly as designed
(bad escalations left evidence in HANDOFFS/). The 05-29 ultraplan + Antigravity Opus review
+ 06-09 MYTHOS audit form a working self-correction loop; most of the Opus review's findings
were actually fixed. CONFIDENCE_LOGIC default-HIGH was validated end-to-end with named test
artifacts. The single biggest structural asset: nearly every gap below is ALREADY KNOWN to
the vault somewhere — the failures are write-back and ratification lag, not blindness.

---

## S — SECURITY

**S1 🔴 Live secrets traveled in the snapshot.** `03_INFRASTRUCTURE/n8n_env.ps1` (13 env
assignments including the live Tavily key) is inside the zip that went SSD → MacBook → upload.
SECRETS_POLICY: "n8n_env.ps1 is the only place API keys live" and rotation trigger is
"on suspected exposure." This is a suspected-exposure event by the policy's own standard.
Source: SECRETS_POLICY.md (storage rules, rotation table); the file itself in snapshot.
ACTION — FIX NOW: (1) rotate Tavily key at tavily.ai → update n8n_env.ps1 → restart n8n →
log "KEY ROTATED" row to DECISIONS.md per policy; (2) add `n8n_env.ps1` and
`.claude*/settings.local.json` to every snapshot/zip exclusion list; (3) delete the zip copy
from the MacBook when tonight's sessions end. Perplexity key is marked "web-only/NOT_USED"
in the template — verify the live file matches before deciding whether it also rotates.

**S2 🟠 Secrets off-site backup still unconfirmed.** Bitwarden DECIDED, entry unconfirmed —
DISASTER_RECOVERY §3: "ACTION STILL PENDING: Will confirms the keys have actually been
entered." If Engine Body dies today, keys are gone (and after S1 rotation, the NEW key needs
the Bitwarden entry immediately). Source: DISASTER_RECOVERY.md §3, SECRETS_POLICY.md, A3.
ACTION — FIX NOW (5 min, pairs with S1 rotation).

**S3 🟢 Ollama bound 0.0.0.0 is fine today, watch it later.** Firewall-scoped to /24 per
AI_STACK §1; acceptable. Becomes a review item the day Tailscale subnet ideas or any
internet exposure appear — SECRETS_POLICY already flags this. ACTION — DEFER (tracked).

## D — DATA INTEGRITY / BACKUP

**D1 🔴 n8n database still has zero scheduled backup.** DR calls it "the most critical
unaddressed gap"; DASHBOARD lists it; backup_n8n.ps1 exists but A2 confirms it is NOT
scheduled. One SQLite corruption (which AI_STACK §6 says is exactly what SQLite does under
parallel hits) loses all workflow definitions + history. Source: DISASTER_RECOVERY.md §4,
QUESTIONS A2, DASHBOARD.md. ACTION — FIX NOW: the 5-minute Task Scheduler entry in A2.
This is the cheapest insurance in the whole system.

**D2 🟠 SESSION_STATE write-back discipline broke after 06-03.** The vault's own words:
"Vault write-back discipline gap — sessions after 06-03 did not update SESSION_STATE."
Consequence: live workflow IDs/states are [UNCONFIRMED] in the canonical continuity file
(A6). The session-start protocol reads SESSION_STATE first — so every session now boots on
known-stale state. Source: SESSION_STATE.md 06-09 block. ACTION — FIX NOW: verify IDs in
n8n UI, update SESSION_STATE, and add "SESSION_STATE updated?" to a session-end checklist
(CLAUDE_CODE_PROMPTS.md already has one — it isn't being run).

**D3 🟠 Decision ledger fragmentation.** DECISIONS.md last entry 05-24; locks since then
live in QUESTIONS resolved blocks, PROPOSALS, and SESSION_STATE LOCKED lists. Rule 06
(single source of truth) is violated for the most important record type in a
human-approval system. Source: DECISIONS.md vs QUESTIONS_FOR_WILL.md vs PROPOSALS.md.
ACTION — FIX NOW (decision, not work): Will designates the ledger; one consolidation pass.

**D4 🟡 Media off-site backup unchosen.** DR §6 Options A/B both unconfigured; both nodes
same building (fire/theft = total loss of originals). Source: DISASTER_RECOVERY.md §6.
ACTION — DEFER behind D1, but it's open decision territory (cold-rotation Option B is the
cheap start).

**D5 🟡 Machine-local intelligence violates Rule 12.** Robocopy nightly task, SFV_N8N.vbs,
vault_watcher VBS launcher, and any Scheduled Tasks exist only on the machine — "Engine
intelligence lives in config and scripts, not the machine" (RULES.md Rule 12). A rebuild
from the DR runbook would silently lose them. ACTION — FIX NOW (cheap): export Task
Scheduler XMLs + copy VBS launchers into 03_INFRASTRUCTURE/.

## W — WORKFLOW / IMPLEMENTATION FINDINGS

**W1 🟠 Workflow JSON encoding defects — probable root cause of past import pain.**
workflow1 and workflow4 JSONs carry a UTF-8 BOM (strict JSON parsers reject:
"Unexpected UTF-8 BOM") and mojibake in names ("Workflow 1 â€” Queue Processor",
"Guard â€” DECISION_LOG only") — em-dashes double-encoded. The vault's learned lesson
"non-UUID formats cause silent partial imports / UI import more reliable than API" is
consistent with BOM+encoding breakage, not (only) UUID format. workflow2 (no BOM, clean
em-dash) is the healthy control sample. Source: the three JSON files; SESSION_STATE 05-26
"import failing (UUID issue)". ACTION — FIX NOW: rewrite both JSONs UTF-8-no-BOM with
clean names; keep UI import as default anyway. (I can emit cleaned JSONs on request —
it's a byte-level fix, no logic change, but per Blueprint Lock it ships as a proposal.)

**W2 🟠 CANON doc lags the validated code (CONFIDENCE_LOGIC vs workflow1 JSON).** The doc
lists `<think>`-block stripping as "[UNCONFIRMED — needs test]… follow-up after re-import,"
but the vault JSON's Write+Log node already implements it:
`response.replace(/<think>[\s\S]*?<\/think>/g, '')` — plus the Phase-1 validation from
OUTPUT_VALIDATION. So either (a) the 06-03 re-import used this JSON and the live system has
both fixes (doc stale), or (b) the live import predates it (system missing validation).
Source: CONFIDENCE_LOGIC.md "REMAINING RISK" vs workflow1_queue_processor.json Write+Log.
ACTION — VERIFY-AT-IMPL on Engine Body (open live workflow1, check for think-strip), then
update CONFIDENCE_LOGIC.md to match reality. Pairs with A6.

**W3 🟠 RESEARCH route is a planned dead-end pending workflow3 — fine — but priority is
metadata-only and `client_facing` is defined-but-unenforced.** workflow1 routes RESEARCH →
HANDOFFS (correct interim). However: ANTIGRAVITY_N8N_TRIGGER admits "priority… not
currently enforced — all tasks FIFO," and the `client_facing` force-escalation flag
(Blueprint §3 escalation trigger; JOB_ENVELOPE_SPEC optional field) does not appear in the
workflow1 JSON at all. A client-facing task would ride normal confidence logic. Source:
workflow1 JSON Read Task / Write+Log nodes; JOB_ENVELOPE_SPEC.md; AI_STACK §3.
ACTION — FIX NOW for client_facing (3-line addition to Write+Log spec; matters the day
Brandon's first deliverable enters the queue); DEFER priority enforcement to
CONCURRENCY_QUEUE_SPEC Phase 1 as already planned.

**W4 🟠 The locked SFV_EVENTS Zenfolio QR system has no vault doc.** A primary-revenue,
fully-decided operational workflow (QR cards, Golden Rule, per-day events, camera prefixes,
account-as-source-of-truth, same-day model) exists only in chat memory + one resolved line
in UNCONFIRMED.md. This is the single largest Blueprint-Lock violation in the system —
locked-but-undocumented. Source: UNCONFIRMED.md resolved list; MYTHOS_FORWARD_PROMPT
Scenario A; absence in 04_WORKFLOWS/. ACTION — FIX NOW: write
04_WORKFLOWS/EVENTS_ZENFOLIO_DELIVERY.md before the next event; fold in the open
verification items (Advanced plan caps, QR export format, same-day throughput).

**W5 🟡 workflow1 hardcodes `C:/SFV_BLUEPRINT` inside Code nodes** while start_n8n.ps1 and
n8n_env.ps1 are two different launchers setting different env sets (start_n8n.ps1 doesn't
source n8n_env.ps1; ALLOW_BUILTIN differs: `fs,path,os` vs `fs,path`). Depending on which
window launched n8n, VAULT_PATH may not even exist — which is why the hardcode "works."
Rule 04 violation + split-brain launcher. Source: workflow1 Read Task node; start_n8n.ps1;
n8n_env.ps1/template. ACTION — FIX NOW (small): start_n8n.ps1 dot-sources n8n_env.ps1;
workflow nodes read `$env.VAULT_PATH` with the hardcode as fallback only.

**W6 🟡 Stale LEGACY queue still loaded.** TASK_QUEUE.md (LEGACY) holds 4 PENDING
semantic-link tasks; any ollama_daemon.py run re-executes them. Source: TASK_QUEUE.md head.
ACTION — FIX NOW (1 min): mark them DONE/CANCELLED or archive the file body.

**W7 🟡 OUTPUTS retention cleanup approved-pending.** 13 triplicate test artifacts with an
exact keep/delete list already written. Source: OUTPUTS_RETENTION.md. ACTION — Will
approves; one delete pass.

**W8 🟢 Paper-trial record vs reality.** PAPER_TRIAL_RUNS Trials 01/02 say "NOT YET RUN"
while the events completed successfully. Harmless historically, but Theory Runs should
supersede this file's role explicitly so 08_TESTS doesn't fork into two test methodologies.
ACTION — fold into Theory Runs protocol doc when written.

## R — RELIABILITY / BOTTLENECKS

**R1 🟠 SQLite remains the production DB.** Known, flagged 🔴 in AI_STACK §7 since 05-26,
gated only on Will's supervised session. Every week on SQLite is exposure to the exact
corruption mode the architecture doc predicts, and it blocks Phase-1 concurrency, Redis,
n8n-MCP. Source: AI_STACK §6/§7; POSTGRES_MIGRATION.md. ACTION — the migration IS the
critical path head after the 5-minute fixes (see CRITICAL_PATH.md). The doc is build-ready;
Ultraplan Review's one note (Option A native install matches CANON storage alloc) stands.

**R2 🟠 Failover to Node B is documented-but-dead.** FAILOVER_MODEL's own words: "This
failover path is DEAD until the R&D Terminal install sequence completes" — and the fallback
logic isn't in workflow1 JSON either. So today: Engine Body Ollama dies → tasks fail
silently in n8n logs → watchdog restarts Ollama in ≤5 min (the real mitigation). Honest
state, just keep both halves remembered: R&D rebuild AND the workflow1 retry/fallback edit.
Source: FAILOVER_MODEL.md Scenario 1; workflow1 JSON. ACTION — VERIFY-AT-IMPL after R&D
rebuild; Theory Run Scenario B is purpose-built to validate this.

**R3 🟡 Watchdog dies with its window.** Manual PowerShell loop, not a Scheduled Task —
reboot or closed window = no watchdog, and nothing watches the watchdog. Source:
FAILOVER_MODEL Scenario 2; A5. ACTION — A5 yes (promote to Scheduled Task); trivially
cheap resilience.

**R4 🟡 Syncthing partial-sync race vs localFileTrigger.** Perplexity verification flagged
it; mitigations decided (`*.json` glob, fsWatcherDelayS=1) but the glob filter is NOT
visible in the workflow1 JSON trigger parameters and R&D-side config is pending rebuild.
Source: perplexity_verification_response.md; TWO_TERMINAL plan C1 flag; workflow1 JSON.
ACTION — VERIFY-AT-IMPL: confirm trigger glob on live instance; re-apply on R&D rebuild.
(Read Task node does skip non-.json paths in code — partial protection exists one node late;
a half-synced .json could still parse-fail safely to `return []`. Net: low actual risk,
worth closing properly.)

**R5 🟢 Pre-warm cron vs VRAM budget.** workflow2 pings all three models every 5 min with
keep_alive; MODEL_LIFECYCLE_POLICY warns "Do not load more than two large models
simultaneously" on 16GB. qwen3:14b (~10G) + coder (~5G) + minicpm (~6G) can't all be
resident; Ollama will evict — meaning pre-warm partially defeats itself and the "which
model is warm" state is nondeterministic. Source: workflow2 JSON; MODEL_LIFECYCLE §6.
ACTION — DEFER, but note for Phase-1 tuning: pre-warm the default model only, or stagger.

## C — CONSISTENCY / MAINTENANCE HOTSPOTS

**C-hot1 🟠 PROPOSAL 008 unratified = the whole 06-09 audit layer is provisional.**
COMPRESSED_CONTEXT v0.3.0, IP fixes, LEGACY marking, UNCONFIRMED reconciliation — all of it
sits in ratify-or-revert limbo, and this audit's "fixed" claims inherit that limbo.
Source: PROPOSALS.md P008. ACTION — FIX NOW: it's the first decision on the critical path.

**C-hot2 🟠 N8N_MCP_SPEC status contradicts Will's own A1 verdict.** File says STATUS:
CANON; A1 (Will-facing assessment) says "keep STATUS: FOR HUMAN REVIEW until Docker +
PostgreSQL are confirmed live." A dead-prereq CANON spec is exactly what A1 warned about.
Source: N8N_MCP_SPEC.md frontmatter vs QUESTIONS A1 table. ACTION — FIX NOW with A1
ratification: flip the tag to match whatever Will decides.

**C-hot3 🟡 Stale-tag debt across CANON docs.** TOOL_STATUS (n8n FUTURE, Docker
UNCONFIRMED, Later RESEARCHING), TOOL_STACK, INTEGRATIONS, DELIVERY (scheduling
[UNCONFIRMED]), SFV_404/HARDWARE_CONTEXT inline [UNCONFIRMED]s already resolved by Q001/Q002,
MASTER_CONTEXT near-term targets, ROADMAP/VERSION_LOG/CHANGELOG frozen in May, CLAUDE.md /
ANTIGRAVITY.md May-28 build priorities, MODEL_ROUTING/OLLAMA_SETUP "R&D terminal" framing
pre-dating the Engine-Body-primary pivot. None of these are decisions — all mechanical.
ACTION — one batch mechanical-fix pass (PROPOSAL-009 style), after P008 ratifies, so the
two don't tangle.

**C-hot4 🟡 Duplicated Ollama system prompt** (OLLAMA_SETUP.md and OLLAMA_PROMPTS.md carry
the same block) — drift-prone twin; PROMPT_VERSIONING exists precisely to own this. ACTION —
make OLLAMA_PROMPTS/ the single home, reference from elsewhere.

Full cross-doc conflict inventory: **CONTRADICTION_MATRIX.md** (14 rows, 2 already closed).

## SCALABILITY RISKS (forward-looking, no action tonight)

FIFO + no concurrency caps means one MEDIA job stalls everything (documented, Phase-1/2
plans exist). 32GB RAM with Postgres+Qdrant+Redis+models ambitions — the Blueprint's own
RAM-dependent note stands; 64GB upgrade is a real prerequisite for the P2 stack. Operator-
era scaling (multi-city ingest) has principles (BRANCH_INDEPENDENCE) but zero mechanics —
correctly FUTURE. Tavily 1000/mo free credits with automated workflow3 coming: the >200/day
anomaly alert exists on paper but nothing writes it yet.

## DEFERRABLE (confirmed safe to push to P2/FUTURE)

Vector layer (Qdrant), monitoring stack, media/Whisper pipeline (blocked on A4 anyway),
Gemini n8n route, Open WebUI migration question (Q19), Redis queue mode, faster-whisper,
trading sandbox, client review gateway, Supabase/metadata schema, all 12_DATABANKS seeding,
A/B prompt testing.

## WHAT BLOCKS THE NEXT MILESTONE

First demo already happened (queue processor live, confidence fix validated). The next
milestone that matters is **"PostgreSQL-backed n8n + workflow3 RESEARCH end-to-end +
SESSION_STATE matching runtime."** Blockers, in order: P008 ratification → A1–A6 answers →
S1/D1/S2 five-minute fixes → PostgreSQL migration (Will-supervised) → Docker restart →
workflow3 build → Theory Run Scenario C as the acceptance test. Full ordering with edges:
**CRITICAL_PATH.md** and **DEPENDENCY_GRAPH.mmd**.
