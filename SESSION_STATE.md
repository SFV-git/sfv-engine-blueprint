---
STATUS: CANON
VERSION: v0.6.2
OWNER: WILL
LAST_UPDATED: 2026-06-27
---

# SESSION STATE

Read this first every session. Report in 3 lines. Wait for Will.

---

## STANDING ORDERS — DO NOT OVERRIDE WITHOUT WILL'S EXPLICIT INSTRUCTION
1. NO dev work until blueprint is fully planned and Will approves build order
2. NO deadlines drive decisions — long term correctness over short term delivery
3. Every feature must be planned to its full scaled form before any code is written
4. Plan what gets built, by which tool, in what order — FIRST. Always.
5. Physical node scaling must be accounted for in every architectural decision

## CURRENT PHASE
v0.x — Blueprint Lock COMPLETE. All 20 AI stack gaps blueprinted. Confidence fix validated.
Queue processor + Output Monitor + Pre-Warm all LIVE and ACTIVE (verified 06-25, see below).
Audit layer added (Maple package 06-22) + Quartz vault website (06-10). M1 is the next target
state — see 00_DEV_LOG/CRITICAL_PATH.md. Gate: PROPOSAL 008 ratify/revert still OPEN.
**Hermes adoption RATIFIED (Will, 2026-06-28) — gateway LIVE: Ollama qwen3:14b brain + Telegram connected.**

---

## SESSION — 2026-06-28 (HERMES BROUGHT LIVE — CLAUDE CHAT, OPUS 4.8, WILL PRESENT)

Will ratified Hermes adoption (confirmed in-session). Goal: finish getting Hermes fully working per
HANDOFF_2026-06-28. Done within ratified scope (no new deps adopted beyond completing the already-
ratified Norton/truststore fix; no CANON self-promoted without Will's confirmation).

**RESOLVED — the real blocker was NOT TLS.** Norton's `truststore` injection collides with Hermes'
SSL pre-flight guard (`ctx.get_ca_certs()` → empty `NotImplementedError` → swallowed as "Failed to
initialize OpenAI client:"). Full root-cause + fix logged CANON in `00_DEV_LOG/HERMES_EVAL.md`
(TLS / Two-Venv Resolution section).

**Live now (verified 2026-06-28):**
- Chat brain = **Ollama qwen3:14b** (local/free/private). `hermes -z "PING"` → PING. ✅
- `HERMES_SKIP_SSL_GUARD=1` persisted (keepalive wrapper + User env var).
- Gateway runs from **`hermes-agent\venv`** (only venv with Telegram); truststore copied there from
  `app\.venv` (api.telegram.org IS Norton-intercepted). Keepalive repointed accordingly.
- Telegram **connected (polling mode)**, no SSL errors. `hermes send` → delivered to home channel. ✅
- `config.yaml` model block = Ollama dict form (provider:custom/base_url/api_key:ollama/qwen3:14b/64K).
  Backup: `config.yaml.bak.20260628_184304`.

**FLAGGED FOR WILL [FOR HUMAN REVIEW]:**
- **Reboot persistence NOT set** — gateway running via keepalive launched this session only. Needs
  `hermes_task.xml` registered from ELEVATED prompt (Will-only) OR a no-admin Startup-folder shortcut.
- **Inbound→reply loop untested** — message the bot to confirm a qwen3:14b reply (outbound proven).
- Telegram bot token rotation (cleartext-exposed) + Tavily key rotation — still pending, Will-only.
- Desktop Electron app (PID from 2:58 AM) holds shared handles on config.yaml/.env — fine, just noted.

**Objectives 2 (engine capability review) + 3 (sell-as-software) — NOT STARTED this session.**

---

## SESSION — 2026-06-27 (BLUEPRINT COMPLETENESS AUDIT — CLAUDE CODE, OPUS, HEADLESS)

Directive: `00_DEV_LOG/DIRECTIVE_BLUEPRINT_AUDIT_CONTENT_BANK.md`. Blueprint Lock honored — all output
FOR HUMAN REVIEW, no CANON promo, no build, no live-system change.

**STEP 1 DONE ✅** — 4 parallel read-only subagents (A production / B UGC / C R&D roles / D infra+AI),
merged into **`08_TESTS/BLUEPRINT_COVERAGE_MAP.md`** (FHR): 4 coverage tables + scorecard + 18-item ranked
MASTER GAP LIST. Headline: infra/AI is planned-but-THIN; the real MISSING holes are the craft/business
layer — no Premiere/video-edit doc, no IG scheduling doc, no Lightroom preset doc, and the whole UGC money
pipeline (lead→brief→contract→invoice→notify→report) is unblueprinted. Content Idea Bank (Role 5) = absent.

**STEP 2 NOT DONE ❌** — launched 2 research subagents (ingestion + storage/retrieval); both returned 0
tokens — hit Anthropic session limit. No TOOL_RESEARCH/CONTENT_IDEA_BANK/gap docs written. Will said end here.

**RESUME:** see `00_DEV_LOG/HANDOFF_2026-06-27_BLUEPRINT_AUDIT.md` — re-run the 2 research subagents →
TOOL_RESEARCH.md → CONTENT_IDEA_BANK.md → Role 5 note → remaining ranked gaps. STEP 1 scratch audits
(richest = AUDIT_C Role 5 stub) are in the session scratchpad dir.

---

## SESSION — 2026-06-28 (OVERNIGHT BUG-FIX + VERIFICATION — CLAUDE CHAT, WILL ASLEEP)

Autonomous overnight session. No new dependencies adopted, no CANON self-promoted, no architecture
decisions made on Will's behalf (A1/A2/A3 still await Will). Safe operational work only.

**Done:**
- **WF4 process.env bug FIXED** (live Postgres row + vault JSON). Removed env dependency entirely —
  node now uses literal locked path `C:\SFV_BLUEPRINT`, sandbox-proof. Applied via direct DB row patch
  (NOT re-import — avoided the 06-27 corruption class). Backup: 99_INBOX/BACKUP_wf4_live_20260627_032802.json.
  REMAINING: arms on next n8n restart OR run C:\Windows\Temp\sfv_wf4_reactivate.ps1. Did NOT reactivate
  overnight (non-blocking error + no observer = not worth the risk).
- **WF1 <think> strip confirmed already live** in DB — STEP 3 needed no re-import. Pure risk avoided.
- **Regression PASSED**: REGTEST_THINK_20260627 (CLASSIFY w/ forced thinking block) → clean OUTPUTS landing,
  STATUS VALIDATED, BRANCH SFV_EVENTS, no <think> bleed. Full chain verified end-to-end.

**Verified live:** n8n health 200, 3 workflows active + no duplicates, Ollama up, psql/DB-patch pattern works.

**For Will:** (1) ratify/reject A1/A2/A3, (2) restart n8n or run reactivate script to load WF4 fix,
(3) rotate Tavily key (still plaintext in n8n_env.ps1 — standing CRITICAL_PATH item).

Full detail: 00_DEV_LOG/HANDOFF_2026-06-28.md

---

## SESSION — 2026-06-27 PART 2 (ARCHITECTURE REVIEW — CLAUDE CHAT, WILL PRESENT)

Will raised core question: is the current AI stack capable of walk-away autonomous self-development?
Answer: NO as designed — but a clear path exists. Full analysis in HANDOFF_2026-06-27.md.
Key findings: Ollama is NOT the executor (Claude Code headless is). Hermes Agent (Nous Research,
MIT, 200k stars) may replace most custom loop work — persistent daemon, cron, Claude Code spawning,
skill memory, 18+ messaging platforms. Architecture decision FOR HUMAN REVIEW: adopt Hermes or build
minimal Node orchestrator. Next: Will ratifies → Claude Code evaluates Hermes on Engine Body.
Context ran out. All state saved. Start next session from HANDOFF_2026-06-27.md.

---

## SESSION — 2026-06-27 (BLOCK F — TRIGGERS FIXED END-TO-END — CLAUDE CODE, OPUS, WILL PRESENT)

Goal: fix localFileTrigger so QUEUE/ tasks fire. Will approved the operational work + (mid-session)
the workflow re-import repair. No git push (Will pushes). No Bitwarden/Postgres password entry or key
rotation. workflow3/Docker untouched.

### VERIFICATION (what Will asked to confirm)
- **Env vars in LIVE process: YES.** Read directly from the running n8n process PEB (not the file):
  `NODES_EXCLUDE=[]`, `N8N_ENABLE_LOCAL_FILE_NODE=true`, `DB_TYPE=postgresdb` all confirmed live.
- **Health: 200** at http://127.0.0.1:5678/healthz after every restart.
- **Trigger re-register: DONE** via n8n 2.x publish model (see root cause). All 3 workflows
  active=true, published (activeVersionId set), triggerCount=1, and "Activated workflow" at boot.
- **TEST-002: LANDED in OUTPUTS.** `99_INBOX/OUTPUTS/TEST-002_RESULT.md` (VALIDATED, qwen3:14b,
  ~15s Ollama run). Task JSON written back to status=COMPLETE. Full chain works:
  localFileTrigger → Read Task → Route? → Call Ollama → Write+Log → OUTPUTS.
- **Duplicate deleted: YES.** `bf6LkL91FXDBF10F` removed (exported to backup first). 3 workflows remain.

### ROOT CAUSE — was NOT env-vars-only (handoff diagnosis was incomplete)
Three compounding problems, all now fixed:
1. **Missing env vars** (real): NODES_EXCLUDE/N8N_ENABLE_LOCAL_FILE_NODE lived only in start_n8n.ps1,
   not n8n_env.ps1. Merged into n8n_env.ps1 (single source of truth); start_n8n.ps1 reduced to
   dot-source + `n8n start`.
2. **n8n 2.22.5 publish model**: workflows were active=true but UNPUBLISHED (activeVersionId=NULL).
   Boot log showed "0 published workflows" → no triggers registered. Fixed via `n8n publish:workflow`.
3. **Corrupted workflow graphs** (the real blocker): WF1 + WF4 were imported while localFileTrigger
   was disabled, so n8n silently STRIPPED the trigger node's outgoing connection. Trigger fired but
   dead-ended. Repaired by re-importing the canonical vault JSONs (id retargeted to live DB ids,
   tags stripped to dodge a tagId import bug), then re-activate + publish + restart. WF2 (schedule
   trigger) was never corrupted — it always worked.

### CHANGES MADE
- `03_INFRASTRUCTURE/n8n_env.ps1` (gitignored): added NODES_EXCLUDE=[], N8N_ENABLE_LOCAL_FILE_NODE=true;
  folded in NODE_FUNCTION_ALLOW_EXTERNAL=*, N8N_LOG_LEVEL=info (were only in start_n8n.ps1);
  NODE_FUNCTION_ALLOW_BUILTIN upgraded fs,path → fs,path,os. OLLAMA_URL LEFT as localhost (see flags).
- `03_INFRASTRUCTURE/start_n8n.ps1`: reduced to dot-source n8n_env.ps1 + `n8n start`.
- WF1 (vOH1CsPYvD27sUxx) + WF4 (nRbwsa0K62y2Fnmo): re-imported with restored connections, published.
- Backups in scratchpad: BACKUP_wf1_*.json, BACKUP_wf4_*.json, BACKUP_duplicate_bf6LkL91FXDBF10F.json.

### FLAGGED FOR WILL [FOR HUMAN REVIEW]
- **WF4 (Output Monitor) now FIRES but ERRORS**: `ReferenceError: process is not defined` in its
  "Guard — DECISION_LOG only" Code node (n8n task-runner sandbox blocks `process`). Pre-existing bug,
  never surfaced before because WF4's trigger never fired. Needs a code fix (replace process.env usage).
  Does NOT affect WF1 (the queue processor). Out of Block F scope.
- **n8n API key: NOT created.** Requires the UI/owner login (Settings → API); cannot be minted
  headlessly. `N8N_API_KEY` not added to n8n_env.ps1. Re-register/publish/delete were all done via
  n8n CLI + psql instead, so the key was not needed this block. Create it next time you're in the UI.
- **localFileTrigger has no `awaitWriteFinish` + Read Task does not strip a UTF-8 BOM.** A task file
  written with a BOM (e.g. PowerShell `Set-Content -Encoding utf8`) makes JSON.parse fail → task
  silently dropped. Tasks must be dropped as UTF-8 **no-BOM** (and ideally atomically, write-then-move).
  Consider hardening Read Task to strip a leading BOM. [INFERENCE: likely why ad-hoc drops fail.]
- **OLLAMA_URL kept as `http://localhost:11434`** (current working value). start_n8n.ps1 historically
  used 127.0.0.1 to dodge a Node IPv6-resolution bug. Left as-is to avoid changing working behavior —
  switch to 127.0.0.1 if Ollama calls ever fail on IPv6.
- backup_n8n.ps1 still backs up SQLite — needs pg_dump update (carried over from 06-26 handoff).
- Git NOT pushed (Will pushes). n8n is running (launched via merged env, health 200).

---

## SESSION — 2026-06-25 (RUNTIME VERIFICATION + WRITE-BACK + EVENTS DOC — CLAUDE CHAT, WILL AWAY)

Will granted "do whatever you can without me touching the system." Read-only verification +
additive vault docs only. No services restarted, no key touched, no workflow re-imported, no
decisions made. Local commit only (no push).

### Verified against live runtime (resolves C4 / closes A6 read-side):
- **workflow1 Queue Processor = `Eb78T9FnnKm8UKrJ` — ACTIVE.** (06-03 block's `LJH60a1NrfM2TqKf` is STALE — superseded by re-import.)
- **workflow4 Output Monitor = `GBzP0Qamy3hl0utY` — ACTIVE.** (06-03 block said activation FAILED — it later succeeded. Now confirmed active in DB.)
- **workflow2 Model Pre-Warm = `6OtCtcsw6FANtm8j` — ACTIVE.**
- **workflow3 = NOT BUILT** — only an inactive `My workflow 3` (`l9ZOkREMN0utzwAd`) placeholder exists. RESEARCH still dead-ends to HANDOFFS as designed.
- 4 inactive duplicate/test workflows present (`SsaQRDfF31dNK4m4`, `UyiHaTl8TZudv6IC`, `i1gFo6trABRwRBAL`, `asuuWNDWnHv61Lau`) — harmless, cleanup candidates.
- n8n health 200, Ollama UP. Models present: qwen3:14b, qwen2.5-coder:7b, minicpm-v:8b (CANON roster) + extras qwen2.5:1.5b, llama3.1:latest, qwen3:latest [INFERENCE — leftover/experimental, not in roster].
- **Security:** `n8n_env.ps1` is gitignored + UNTRACKED (not leaking via git). [Tavily key ROTATION still pending — Will-only, requires Tavily dashboard login. Not done.]
- **DR off-site confirmed:** remote = `github.com/SFV-git/sfv-engine-blueprint.git`; `origin/main` == local HEAD (`81e2b03`). GitHub is current.

### Written this session (all FOR HUMAN REVIEW / additive):
- **04_WORKFLOWS/EVENTS_ZENFOLIO_DELIVERY.md (NEW)** — formalizes the locked SFV_EVENTS Zenfolio QR system (Golden Rule, Cam1_/2_/3_ prefixes, filename-sort, 3 laptops/1 account, multi-day fresh-stack, failure modes, rejected face-rec). Closes the top doc hole flagged in MISSING_REFERENCED_FILES §3. Verification block (Zenfolio caps/pricing, QR card stock + export format, per-day template) left FHR.
- **04_WORKFLOWS/DELIVERY.md** — SFV_EVENTS platform line updated from `[UNCONFIRMED]` → points to the new doc.

### NOT done (needs Will / out of safe-autonomous scope):
- PROPOSAL 008 ratify/revert · A1–A6 · Tavily key rotation · n8n restart/re-import · PostgreSQL · Docker · workflow3 build · stale-PENDING + duplicate-workflow cleanup (all flagged).

### WHAT NEEDS ATTENTION NEXT (priority):
1. **PROPOSAL 008 ratify/revert** + **A1–A6** — still the decision gate (CRITICAL_PATH Step 0).
2. **Rotate Tavily key** (CRITICAL_PATH Step 1, Will-only — Tavily dashboard) → update n8n_env.ps1 → restart n8n → log to DECISIONS.md.
3. C4 now CLOSED — runtime IDs above are truth. Old 06-03 IDs are superseded.
4. PostgreSQL migration → Docker → workflow3 build (CRITICAL_PATH Steps 4–6).
5. Promote EVENTS_ZENFOLIO_DELIVERY.md to CANON once its verification block is cleared.

---

## SESSION — 2026-06-09 (FULL-VAULT AUDIT + MECHANICAL FIXES — CLAUDE CHAT)

### Completed this session:
- Full-vault audit (MYTHOS role) executed directly via Desktop Commander — 5-part findings delivered in chat
- All mechanical fixes applied under Will's "full rein" grant — full list in PROPOSALS.md → PROPOSAL 008 (RATIFY OR REVERT)
- Headlines: stale .239 IPs fixed in 4 docs | COMPRESSED_CONTEXT rewritten v0.3.0 | TASK_QUEUE.md marked LEGACY | FAILOVER_MODEL reconciled with real watchdog.ps1 | PROMPT_VERSIONING implemented (v1 + CURRENT + CHANGELOG) | Bitwarden decision recorded in DR + SECRETS_POLICY | UNCONFIRMED.md reconciled | DASHBOARD refreshed | MYTHOS_PROTOCOL.md created (FHR)
- 6 urgent questions (A1–A6) + 11 open decisions (15–25) logged to QUESTIONS_FOR_WILL.md

### [RESOLVED 2026-06-25 — verified against live n8n DB, see 06-25 block above]:
- Workflow IDs in this file's 2026-06-03 block may be superseded: later work reportedly re-imported workflow1 (Eb78T9FnnKm8UKrJ) and activated workflow4 (GBzP0Qamy3hl0utY). The 06-03 block says workflow4 activation FAILED. Verify actual IDs/states in n8n UI and update here. Vault write-back discipline gap — sessions after 06-03 did not update SESSION_STATE.
  - **RESOLUTION:** Confirmed — workflow1=`Eb78T9FnnKm8UKrJ` ACTIVE, workflow4=`GBzP0Qamy3hl0utY` ACTIVE. 06-03 IDs/FAILED-status are stale. C4 closed.

### WHAT NEEDS ATTENTION NEXT SESSION (PRIORITY ORDER):
1. **Will reviews PROPOSAL 008** — ratify or revert audit fixes (git diff shows everything)
2. **Will answers A1–A6** in QUESTIONS_FOR_WILL.md — Antigravity CANON ratification, n8n backup approval, Bitwarden confirm, Whisper port, watchdog Scheduled Task, workflow ID verify
3. **PostgreSQL migration** — unchanged, Will supervises, backup SQLite first
4. **Docker install** — unchanged, needs restart
5. **R&D Terminal reinstalls** — Ollama → Syncthing → Claude Code → windows_exporter

---

## SESSION — 2026-06-03 (CONFIDENCE FIX VALIDATED + N8N OPERATIONAL)

### Completed this session:
- n8n started clean — v2.22.5, healthy at http://127.0.0.1:5678 ✅
- workflow1_queue_processor re-imported via API (ID: LJH60a1NrfM2TqKf) ✅
- workflow1 activated — localFileTrigger live on QUEUE/ ✅
- **Confidence fix CONFIRMED end-to-end:**
  - TEST_CLASSIFY_002 → OLLAMA_CLASSIFY (HIGH CONFIDENCE) → OUTPUTS/ ✅
  - TEST_CODE_004 → OLLAMA_CODE (HIGH CONFIDENCE) → OUTPUTS/ ✅
  - Both processed in <5s of file drop. Write-back to QUEUE json confirmed. DECISION_LOG updated.
- CONFIDENCE_LOGIC.md promoted to CANON (was FOR HUMAN REVIEW) ✅
- Duplicate workflow1 (FwTeEPL7w5vlPwO7) deleted ✅
- OVERNIGHT_DIRECTIVE.md written — ready for autonomous loop ✅

### NOT completed this session:
- ❌ Workflow 4 (Output Monitor, ID: oUw9qPMw6CpHEIv8) — activation FAILED
  - Error: Node "Watch 99_INBOX" missing required parameter `triggerOn`
  - Fix: open in n8n UI → edit trigger node → set triggerOn=folder → save → activate

### WHAT NEEDS ATTENTION NEXT SESSION (PRIORITY ORDER):
1. **Fix Workflow 4 trigger node** — open n8n UI, set triggerOn=folder on "Watch 99_INBOX", activate
2. **PostgreSQL migration** — see POSTGRES_MIGRATION.md. Will supervises. Backup SQLite first.
3. **Docker install on Engine Body** — requires restart. See DOCKER_INSTALL_CHECKLIST.md (CANON).
4. **R&D Terminal installs** — in order: Ollama → Syncthing → Claude Code → windows_exporter
5. **Review 12 remaining FHR docs** — start with: POSTGRES_MIGRATION, FAILOVER_MODEL, SECRETS_POLICY
6. **workflow3 build** — RESEARCH handler. See RESEARCH_ROUTE_SPEC.md. After PostgreSQL + Docker stable.
7. **Update AI_STACK_ARCHITECTURE_BLUEPRINT.md** — R&D Terminal IP 192.168.137.239 → 192.168.137.246
8. **Secrets backup** — n8n_env.ps1 has no off-site backup (see DISASTER_RECOVERY.md §3)

---

## SESSION — 2026-05-30 (ULTRAPLAN COMPLETE + R&D TERMINAL SETUP)

### Completed this session:
- Claude Code finished all 20 AI stack gap docs (ultraplan execution complete)
- 6 docs promoted to CANON by Antigravity review:
  DOCKER_INSTALL_CHECKLIST · SECRETS_POLICY · CONCURRENCY_QUEUE_SPEC · OUTPUT_VALIDATION · PROMPT_VERSIONING · N8N_MCP_SPEC
- 13 docs remain FOR HUMAN REVIEW — Will promotes as execution begins
- ULTRAPLAN_BRIEF.md written to 00_DEV_LOG/ (Chat → Code handoff doc)
- R&D Terminal post-Win11 state confirmed (DESKTOP-JGUJOGA):
  - ✅ Git 2.54.0 | ✅ Tailscale 1.98.2 | ✅ Python
  - ❌ Ollama — needs reinstall
  - ❌ Syncthing — needs reinstall
  - ❌ Claude Code — needs install
  - ❓ windows_exporter — not checked
- R&D Terminal IP CHANGED: 192.168.137.239 → 192.168.137.246 (DHCP after Win11)
  - Firewall /24 scope still valid. AI_STACK_ARCHITECTURE_BLUEPRINT.md needs IP update.

### WHAT NEEDS ATTENTION NEXT SESSION (PRIORITY ORDER):
1. **workflow1 re-import** — drop updated JSON (commit 8c7188f) into n8n. Test with TEST_CLASSIFY_002.json + TEST_CODE_004.json in QUEUE/
2. **PostgreSQL migration** — see POSTGRES_MIGRATION.md. Will supervises. Backup SQLite first.
3. **Docker install on Engine Body** — requires restart. See DOCKER_INSTALL_CHECKLIST.md (CANON). Unlocks Open WebUI, n8n-MCP, Redis.
4. **R&D Terminal installs** — in order: Ollama → Syncthing → Claude Code → windows_exporter
5. **Review 13 FHR docs** — start with Phase 0: CONFIDENCE_LOGIC, POSTGRES_MIGRATION, FAILOVER_MODEL, SECRETS_POLICY
6. **workflow3 build** — confirmed RESEARCH handler. See RESEARCH_ROUTE_SPEC.md. After PostgreSQL + Docker stable.
7. **Update AI_STACK_ARCHITECTURE_BLUEPRINT.md** — R&D Terminal IP 192.168.137.239 → 192.168.137.246
8. **Open question** — password manager for secrets (n8n_env.ps1 has no off-site backup, see DISASTER_RECOVERY.md §3)

---

## SESSION — 2026-05-29 (ULTRAPLAN — AI STACK GAP ANALYSIS — CLAUDE CODE)

### Completed this session:
- Read all 14 vault files per ULTRAPLAN_BRIEF.md
- Diagnosed confidence escalation bug (Gap 1): fix already in vault JSON (commit 8c7188f); n8n re-import pending
- Wrote 19 new blueprint docs covering all 20 gaps (Gaps 1–20)
- Gap 9 (workflow3): flagged FOR HUMAN REVIEW — D3 not answered, see RESEARCH_ROUTE_SPEC.md
- All docs STATUS: FOR HUMAN REVIEW, all content labeled CANON/UNCONFIRMED/INFERENCE as appropriate

### New files written this session:
- 05_AI_LAYER/CONFIDENCE_LOGIC.md
- 03_INFRASTRUCTURE/POSTGRES_MIGRATION.md
- 03_INFRASTRUCTURE/DOCKER_INSTALL_CHECKLIST.md
- 03_INFRASTRUCTURE/FAILOVER_MODEL.md
- 03_INFRASTRUCTURE/SECRETS_POLICY.md
- 05_AI_LAYER/ANTIGRAVITY_N8N_TRIGGER.md
- 03_INFRASTRUCTURE/N8N_MCP_SPEC.md
- 05_AI_LAYER/RESEARCH_ROUTE_SPEC.md
- 05_AI_LAYER/GEMINI_INTEGRATION.md
- 03_INFRASTRUCTURE/OPEN_WEBUI_SPEC.md
- 05_AI_LAYER/VECTOR_LAYER_PLAN.md
- 04_WORKFLOWS/MEDIA_PIPELINE.md
- 03_INFRASTRUCTURE/MONITORING_STACK.md
- 05_AI_LAYER/COST_CEILING_POLICY.md
- 03_INFRASTRUCTURE/CONCURRENCY_QUEUE_SPEC.md
- 05_AI_LAYER/OUTPUT_VALIDATION.md
- 05_AI_LAYER/PROMPT_VERSIONING.md
- 05_AI_LAYER/MODEL_LIFECYCLE_POLICY.md
- 03_INFRASTRUCTURE/DISASTER_RECOVERY.md

### WHAT NEEDS ATTENTION NEXT SESSION:
1. **Will reviews all 19 new docs** — approve, reject, or mark CANON as ready
2. **workflow3 decision (D3)** — confirm: dedicated RESEARCH handler or keep inside workflow1?
3. **workflow1 re-import** — re-import workflow1_queue_processor.json into n8n to apply confidence fix
4. **Test confidence fix** — drop TEST_CLASSIFY_002.json and TEST_CODE_004.json into QUEUE/, confirm both land in OUTPUTS/
5. **MERGE_INTO docs** — after Will approves, merge flagged docs into their target files
6. **CONCURRENCY_QUEUE_SPEC** → AI_STACK_ARCHITECTURE_BLUEPRINT §4
7. **MODEL_LIFECYCLE_POLICY** → LOCAL_MODELS.md
8. **Remaining Phase 0 actions** — Docker install, PostgreSQL migration (see those docs)

---

## SESSION — 2026-05-29 (AI STACK PHASE 1 EXECUTION — ENGINE BODY)

### Completed this session:
- vault_watcher auto-start on boot — Startup folder VBS launcher (Task Scheduler required admin, blocked)
- Wikilinks backfilled across vault — 66 files ADDED, 12 already had, 11 skipped
- backfill_wikilinks.py written — C:\SFV_BLUEPRINT\99_INBOX\backfill_wikilinks.py
- Semantic links script written — C:\SFV_BLUEPRINT\99_INBOX\semantic_links.py (Ollama-driven per-file linking)
- n8n workflows imported and live:
  - workflow1_queue_processor → id=FwTeEPL7w5vlPwO7, active=true
  - workflow4_output_monitor → id=oUw9qPMw6CpHEIv8
  - workflow2_model_prewarm → id=6OtCtcsw6FANtm8j, active=true (fires every 5 min)
- workflow1 routing updated by task_type:
  - CODE → qwen2.5-coder:7b
  - VISION → minicpm-v:8b
  - CLASSIFY / SUMMARIZE / default → qwen3:14b
  - RESEARCH → HANDOFFS
  - keep_alive=10m on all Ollama calls
- CC-TEST-002 confirmed full queue end-to-end (file trigger → Ollama → HANDOFFS escalation)
- start_n8n.ps1 + SFV_N8N.vbs created — n8n auto-starts on login with NODES_EXCLUDE=[], OLLAMA_URL, OLLAMA_MODEL set
- OLLAMA_KEEP_ALIVE=10m set at Machine scope, Ollama restarted, responsive
- Specialist models pulled on Engine Body:
  - qwen2.5-coder:7b (4.7 GB) ✅
  - minicpm-v:8b (5.5 GB) ✅
- UGC_PRE_PRODUCTION.md blueprint written — full pre-production manager spec (04_WORKFLOWS/)
- n8n_import.py written — 99_INBOX/n8n_import.py
- localFileTrigger node enabled in n8n via NODES_EXCLUDE=[] env var
- n8n hardcoded http://127.0.0.1:11434 (localhost resolves to IPv6 in Node 18+)

### Git commits this session:
- 8b84ad4 — vault_watcher auto-start, wikilinks backfilled
- 86cf7ae — n8n workflows imported and tested
- 3a91b5f — Ollama specialist models, keep-alive, pre-warm cron, task_type routing
- da700df — VISION route confirmation

### Route test results — FLAG FOR REVIEW:
- VISION-TEST-002 → minicpm-v:8b → COMPLETE (high-conf → OUTPUTS) ✅
- CLASSIFY-TEST-001 → qwen3:14b → ESCALATED (low-conf → HANDOFFS) ⚠️
- CODE-TEST-003 → qwen2.5-coder:7b → ESCALATED (low-conf → HANDOFFS) ⚠️

**2/3 false escalations on trivial prompts.** Cost routing breaks if Ollama always escalates.
Diagnosis prompt sent to Claude Code at session end — read HANDOFF files + workflow1 confidence logic.
DO NOT auto-fix. Will reviews next session.

### Engine Body — AI Stack Phase 1 Status:
- ✅ OLLAMA_HOST=0.0.0.0:11434
- ✅ OLLAMA_KEEP_ALIVE=10m
- ✅ Pre-warm cron active (workflow2, every 5 min)
- ✅ Specialist models loaded (general, code, vision)
- ✅ task_type routing in workflow1
- ✅ n8n auto-starts on login
- ✅ vault_watcher auto-starts on login
- ❌ Confidence escalation logic — 2/3 false escalations (BLOCKER)
- ❌ Docker not installed — blocks Open WebUI + n8n-MCP
- ❌ PostgreSQL migration — n8n still on SQLite (🔴 Critical before scaling)
- ❌ Antigravity → n8n direct trigger not wired

### R&D Terminal:
- Updating to Windows 11 — paused all R&D work this session
- Sentinel Phase 1 deferred until back online

### WHAT NEEDS ATTENTION NEXT SESSION:
1. **Fix confidence escalation logic in workflow1** — read Claude Code diagnosis output first
2. **Docker install on Engine Body** — unlocks Open WebUI + n8n-MCP + n8n queue mode
3. **PostgreSQL migration for n8n** — daytime task, Will supervises
4. **Antigravity → n8n direct trigger** — wire the orchestrator into the queue
5. **R&D Terminal post-Win11 setup** — reinstall Ollama, Tailscale, Syncthing, Claude Code
6. **UGC Pre-Production app build** — blueprint ready in 04_WORKFLOWS/, Claude Code can scaffold
7. **Test RESEARCH route** — requires Perplexity API confirmation
8. **Semantic links script** — confirm it ran cleanly, audit results

---

## PRIORITY ORDER (locked until Will says otherwise)
1. AI stack — design and link Claude + Antigravity + Ollama + n8n end to end. Token optimization. Full connection map.
2. Blueprint development — every workflow, every file, every decision documented before build begins.
   Includes: ingest (with culling), delivery, AI routing, physical node scaling, multi-computer architecture.
3. Build order — who builds what, when, in what sequence. Assigned per tool capability.
4. Dev work — only begins after 1-3 are complete and Will approves.

## LAST SESSION — 2026-05-25 (MAJOR SESSION)

### Stack built and operational:
- Full tool stack live: Claude Chat + Code + Cowork + Antigravity 2.0 + Ollama daemon + Obsidian + Google AI Studio + NotebookLM
- Drive paths locked: C:\=vault | D:\=Seagate One Touch 5TB | E:\=SanDisk Extreme 1TB
- Branch folders built on D:\ (49 folders, all 9 branches)
- Ollama daemon v3 running — fixed Windows path separator bug for READ: file injection
- vault_watcher.py v2 running — auto-adds CONNECTED FILES to new .md files
- find_orphans.py written — run to generate 00_DEV_LOG/ORPHANS.md

### Antigravity confirmed:
- Role: Agentic Orchestrator (PowerShell, web access, subagents, cron scheduling)
- Capabilities confirmed by Antigravity's own session
- ANTIGRAVITY.md context file written and live in vault root
- Git: SESSION_STATE.md + STACK_INTEGRATION_PLAN.md modified by Antigravity (not committed yet)
- ANTIGRAVITY_RULES.md shows as untracked in git — needs git add

### Blueprint docs built:
- 04_WORKFLOWS/INGEST.md — fully detailed, May 28 spec complete
- 99_INBOX/ingest.py v2 — all Gemini review issues fixed (config loader, correct duplicate behavior, lazy MD5, proper naming convention, dry-run without media)
- 05_AI_LAYER/RATE_LIMITS.md — all tools documented with limits + routing strategy
- 03_INFRASTRUCTURE/MULTI_AGENT_WORKFLOW.md — full tool interaction map
- 03_INFRASTRUCTURE/STACK_INTEGRATION_PLAN.md — updated by Antigravity
- 05_AI_LAYER/RD_TERMINAL_ARCHITECTURE.md — Sentinel proposal written (FOR HUMAN REVIEW)
- FOR_HUMAN_REVIEW/PROPOSALS.md — Proposal 007 (Sentinel) added by Antigravity

### Wikilinks:
- All 9 branch files: CONNECTED FILES sections added with cross-branch links
- All paths updated from %SFV_ROOT%\ACTIVE_STORAGE to %BRANCHES_ROOT%

### Corrections noted:
- Branch name is SFV_STUDIO not "SFV Studio" — all references should use underscore caps

## WHAT NEEDS ATTENTION NEXT SESSION
1. AI stack connection map — Claude + Antigravity + Ollama + n8n. Full design, token optimization, no code yet.
2. Ingest blueprint rewrite — culling during import, storage efficiency, full flow design including long term scaling.
3. Physical node architecture — Engine Body + R&D Terminal + future nodes. How they connect, what runs where.
4. Build order document — every file, every tool, every sequence. Will approves before anything gets coded.
5. n8n workflow JSONs have bad UUIDs — DO NOT import until blueprinted and rebuilt correctly.
6. Claude Code instance — currently paused, waiting. Do not resume until blueprint work is complete.
7. Docker install + restart — end of a future session when Will is ready.

## SESSION — 2026-05-27 (ENGINE BODY + R&D TERMINAL NETWORK)

### Completed this session:
- OLLAMA_HOST=0.0.0.0:11434 set at Machine scope on Engine Body — Ollama now cross-node accessible
- Firewall rules created on Engine Body (scoped to 192.168.137.0/24): ports 11434, 5678, 9182
- File and Printer Sharing enabled on Engine Body (32 rules) and R&D Terminal
- Network Discovery enabled on Engine Body (52 rules) and R&D Terminal
- VaultShare fixed — was incorrectly pointing to C:\, corrected to C:\SFV_BLUEPRINT
- Engine Body ethernet interface changed from Public → Private profile (was blocking SMB)
- WinRM configured on Engine Body via winrm quickconfig — Node B added to TrustedHosts
- sfvshare local account created on Engine Body to work around Microsoft account/PIN blocking SMB
- V: drive mapped on R&D Terminal — \\192.168.137.1\VaultShare → V:\ persistent, confirmed working
- AI_STACK_ARCHITECTURE_BLUEPRINT.md updated with real IPs (192.168.137.x subnet, confirmed)
- RD_TERMINAL_ARCHITECTURE.md status updated to CANON (Proposal 007 approved)

### Node networking — CONFIRMED LIVE:
- Engine Body: 192.168.137.1 (ICS), 192.168.2.12 (WiFi), 100.118.181.52 (Tailscale)
- R&D Terminal: 192.168.137.239 (ICS client), internet via Engine Body ICS
- Both nodes fully linked. R&D Terminal has live read/write vault access via V:\
- Ollama on Engine Body reachable from R&D Terminal at http://192.168.137.1:11434
- Blueprint Section 1 (networking) physically implemented and confirmed

### R&D Terminal Phase 1 installs — DONE:
- Ollama ✅ | Tailscale ✅ | Python ✅ | Git ✅ | Syncthing ✅ | windows_exporter ✅
- ICS internet via Engine Body ethernet ✅ | DNS set to 8.8.8.8 ✅
- Docker/WSL2 — DEFERRED to Phase 2 (not blocking anything now)

### WHAT NEEDS ATTENTION NEXT SESSION:
1. n8n workflows — import workflow JSONs into n8n UI and test with a live queue task
2. PostgreSQL — migrate n8n off SQLite (🔴 Critical per blueprint before scaling)
3. Delete SYNC_TEST.txt from vault root
4. Git commit — all session changes uncommitted

### COMPLETED THIS SESSION (2026-05-28):
- Ollama cross-node confirmed live — 192.168.137.239 hitting Engine Body at 0.0.0.0:11434 ✅
- qwen3:14b confirmed in ollama list — daemon clear to use it ✅
- Syncthing installed on both nodes (was missing from Engine Body) ✅
- Syncthing configured — SFV_BLUEPRINT folder bidirectional sync, both nodes live ✅
- Claude Code installed on Engine Body — dangerously-skip-permissions pattern established ✅
- n8n workflow JSONs rebuilt by Claude Code with correct structure:
  - 03_INFRASTRUCTURE/n8n_workflows/workflow1_queue_processor.json ✅
  - 03_INFRASTRUCTURE/n8n_workflows/workflow4_output_monitor.json ✅
  - Routing logic: OLLAMA / RESEARCH / HANDOFF per task_type
  - PENDING status filter — skips already-processed tasks
- SYNC_TEST.txt in vault root — needs manual delete

## SESSION — 2026-05-26 (CONTINUED)
### Completed this session:
- AI_STACK_ARCHITECTURE_BLUEPRINT.md — STATUS: CANON, v1.1, 230 lines. AI stack priority item DONE.
- Full node linking, file allocation, phase sequence, all tools confirmed.
- Docker install initiated — requires restart to complete.

### FIRST TASK NEXT SESSION:
Build a lightweight terminal review system for all FOR HUMAN REVIEW and UNCONFIRMED items across the vault. No tokens — Will yes/no's them. Design + build at session start.
### Built (dev work — now paused pending blueprint completion):
- n8n_env.ps1 — API keys filled, Tavily live, Perplexity web-only
- .gitignore — n8n_env.ps1, .obsidian/, .smart-env/ excluded
- n8n_env.template.ps1 — safe placeholder for git
- ollama_queue_test.py — rewritten with Switch node routing + table log format
- workflow4_output_monitor.json — built but import failing (UUID issue)
- workflow1_queue_processor.json — built but import failing (UUID issue)
- QUESTIONS_FOR_WILL.md — 5 decisions resolved: UGC name, Later, Tailscale, Docker, Sentinel

### Decisions locked 2026-05-26:
- SFV_UGC stays as internal name
- Scheduling tool: Later
- Tailscale: approved
- Docker: approved (install end of session TBD)
- Proposal 007 Sentinel: approved
- Ingest routing: Option B fallback (C:\ if D:\ not present)
- NO MORE DEV WORK until blueprint is complete

## COMPLETED 2026-05-25 SESSION 2 — COMMUNICATION LAYER
- 00_DEV_LOG/2026-05-25_TODAY_CONTROL.md — created
- 05_AI_LAYER/AI_USE_CASE_PROFILE.md — created (Antigravity elevated to Tier 1, routing tree defined)
- 03_INFRASTRUCTURE/ENGINE_COMMUNICATION_MODEL.md — created (full comms model: queue, outputs, handoffs, decision log, routing rules)
- 99_INBOX/QUEUE/ — created. Perplexity task + Ollama test task queued.
- 99_INBOX/OUTPUTS/ — created
- 99_INBOX/HANDOFFS/ — created
- 99_INBOX/DECISION_LOG.md — created
- 99_INBOX/ollama_queue_test.py — created (reads JSON from QUEUE → Ollama → writes OUTPUTS → logs DECISION_LOG)
- 99_INBOX/OUTPUTS/20260525-002_INGEST_WASTE_AUDIT.md — ingest audited. No Claude waste. n8n trigger opps flagged FOR HUMAN REVIEW.

## OLLAMA QUEUE TEST — READY
  python C:\SFV_BLUEPRINT\99_INBOX\ollama_queue_test.py
  Test task: QUEUE/20260525-TEST-001_OLLAMA_BRANCH_CLASSIFY.json

## PERPLEXITY TASK — READY (run manually)
  Task prompt in: QUEUE/20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.json
  Save output to: OUTPUTS/20260525-001_PERPLEXITY_N8N_INGEST_RESEARCH.md

## CRITICAL DEADLINES
- MAY 28 THURSDAY — Morning Walk, 50+ models, SFV_STUDIO pipeline MUST work
- JUNE 6 — Shamar Tournament, SFV_LIVE pipeline
- THIS WEEK — Brandon Bellotti visit (first UGC client candidate)

## GIT STATUS (as of end of session 2026-05-25)
Files modified/untracked — NOT YET COMMITTED:
- M 03_INFRASTRUCTURE/STACK_INTEGRATION_PLAN.md
- M SESSION_STATE.md
- ?? 05_AI_LAYER/ANTIGRAVITY_RULES.md (untracked — needs git add)
- Multiple new files created tonight

Commit command:
  git add .
  git commit -m "feat: full stack operational — ingest v2, Sentinel proposal, wikilinks, daemon v3"

## OLLAMA DAEMON — HOW TO RUN
Ollama auto-starts. Do NOT run ollama serve (port conflict).
Run from Windows Terminal (PowerShell) — NOT inside Python interpreter.
Verify live: http://localhost:11434

  python C:\SFV_BLUEPRINT\99_INBOX\ollama_daemon.py

Results: C:\SFV_BLUEPRINT\99_INBOX\OLLAMA_RESULTS.md
Queue: C:\SFV_BLUEPRINT\99_INBOX\TASK_QUEUE.md (separate tasks with ---)

## VAULT WATCHER — HOW TO RUN
Run in dedicated terminal tab whenever doing vault work:
  python C:\SFV_BLUEPRINT\99_INBOX\vault_watcher.py
Auto-adds CONNECTED FILES to new .md files + queues Ollama for semantic links.

## LOCKED — DO NOT RE-DISCUSS
- 9 branches: MYTHOLOGY, SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO, SFV_UGC, SFV_ARCHIVE, SFV_WORLD, SFV_404
- Branch name format: SFV_STUDIO (underscore + caps) — never "SFV Studio"
- Vault path: C:\SFV_BLUEPRINT
- Naming conventions: locked (see 03_INFRASTRUCTURE/NAMING_CONVENTIONS.md)
- Storage: C:\=vault | D:\=Seagate One Touch 5TB | E:\=SanDisk Extreme 1TB
- SFV_EVENTS delivery: Pixieset
- Model routing: Sonnet default, Opus on request, Gemini Flash for Antigravity
- Windows Terminal replaces Ghostty
- All paths via ENVIRONMENT_CONFIG.md — never hardcode

## DECISIONS LOCKED 2026-05-27 (REVIEW SESSION)
- P001 OpenClaw: DEFERRED — Ollama + Antigravity cover it. Revisit post-v1.0.
- P003 UPS: DEFERRED — Will confirmed eventual yes. Buy when full stack running.
- P004 Idle Throttling: APPROVED — R&D Terminal idles by default, Will gives heads-up before shoot.
- P005 SFV World → are.na: APPROVED — rejected WORLD content queued with tag/description. Will has hard veto per piece.
- P006 Git Commit Convention: APPROVED — format locked.
- U001 Cross-branch dedup: APPROVED WITH MODIFICATION — write proxy/pointer .txt noting original location instead of blocking. Will decides routing.
- U002 Docker doc: FIXED — RD_TERMINAL_ARCHITECTURE.md updated UNCONFIRMED → APPROVED.
- FHR001 n8n file watcher: APPROVED — negligible load. System idles by default.
- FHR002 n8n notify: APPROVED.
- FHR003 Ollama classifier: APPROVED — must tag/describe unknown-branch files for Will to decide after the fact.
- FHR004 Gemini Flash: ADDED to stack, low priority.
- FHR005 Google Colab: APPROVED — add to stack.
- Q001 SFV_404: RESOLVED — own IG account.
- Q002 Three monitors: RESOLVED — 3 Engine Body, 2 R&D Terminal.
- Q003 Whisper: RESOLVED — local on R&D Terminal (free).
- Q004 Canva: REMOVED — not part of stack. Question was an unsourced inference.

## HOW TO START NEXT SESSION
1. Claude reads SESSION_STATE.md + DASHBOARD.md + QUESTIONS_FOR_WILL.md
2. Claude reads OLLAMA_RESULTS.md for overnight output
3. Reports 3 lines max
4. Waits for Will

## CONNECTED FILES
- [[ANTIGRAVITY_RULES|Antigravity Rules]]
- [[MODEL_ROUTING|Model Routing]]
- [[INGEST|Ingest Workflow]]
- [[STACK_INTEGRATION_PLAN|Stack Integration Plan]]
- [[MULTI_AGENT_WORKFLOW|Multi-Agent Workflow]]
- [[PROPOSALS|Proposals for Human Review]]
- [[RATE_LIMITS|Rate Limits Documentation]]
