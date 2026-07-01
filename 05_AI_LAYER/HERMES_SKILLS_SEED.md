---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-27
CREATED_BY: Antigravity
PURPOSE: Pre-seeded skills for Hermes Agent. Import at adoption time. Claude Code handles import.
---

# HERMES SKILLS — SEED SET v1.0

> These 10 skills are imported into Hermes at adoption time.
> They give Hermes SFV-specific knowledge from day one, skipping the cold-start period.
> Hermes will compound on these — writing new skills from experience as the build progresses.
> Each skill below is formatted for Hermes skill import. Claude Code imports during integration session.

---

## SKILL-001 — SFV SYSTEM CONTEXT

```yaml
skill_id: sfv-001-system-context
name: SFV System Context
version: "1.0"
trigger_patterns:
  - "sfv"
  - "what is this system"
  - "engine context"
  - "what are we building"
  - "give me context"
source_doc: MASTER_CONTEXT.md + COMPRESSED_CONTEXT.md
content: |
  SFV Engine is a photography + content production system owned by Will.
  Two hardware nodes:
    - Engine Body (RTX 5080, 64GB RAM): primary worker — ingest, render, Lightroom, n8n, Ollama
    - R&D Terminal (RTX 3060, 16GB RAM): sentinel — monitoring, telemetry, client gateway, experiments
  
  Money makers (in order):
    1. SFV_UGC — content retainers with clients (primary revenue, 6.5 complexity)
    2. SFV_EVENTS — on-site photography at events and venues (5-6.5 complexity)
  
  Nine branches: MYTHOLOGY (hub), LIVE (events), EVENTS (portraits), ATHLETICS (sports),
  STUDIO (studio), UGC (content), ARCHIVE (portfolio), WORLD (life/alias), 404 (experimental)
  
  Vault location: C:\SFV_BLUEPRINT\ (Obsidian vault, also the git repo)
  Active storage: D:\SFV_ACTIVE\ (production files, not in vault)
  
  AI stack (current):
    - Antigravity (Claude Chat): top-tier system builder, final reviewer
    - Claude Code: builder/executor — edits vault, runs scripts
    - n8n (PostgreSQL): automation trigger layer
    - Ollama qwen3:14b: local gatekeeper — classify/summarize
    - Hermes: persistent daemon, loop driver, messenger
  
  Blueprint lock rule: nothing gets built until the blueprint is deterministic.
  Canon rule: Will approves all CANON changes. AI writes DRAFT only.
```

---

## SKILL-002 — DROP A TASK TO QUEUE

```yaml
skill_id: sfv-002-queue-task
name: Drop Task to Queue
version: "1.0"
trigger_patterns:
  - "drop task"
  - "add to queue"
  - "run this through n8n"
  - "queue a job"
  - "create job envelope"
source_doc: JOB_ENVELOPE_SPEC.md
content: |
  To add a task to the SFV n8n processing queue, create a JSON file in:
    C:\SFV_BLUEPRINT\99_INBOX\QUEUE\
  
  REQUIRED FIELDS (all must be present):
  {
    "task_id":       "YYYYMMDD-NNN",        <- sequential, unique per day
    "task_type":     "CLASSIFY|SUMMARIZE|COMPRESS|RESEARCH|BLUEPRINT|CODE|MEDIA|VISION|GEMINI",
    "topic":         "Short human-readable description",
    "prompt":        "Full prompt text sent to the model",
    "priority":      "NORMAL|HIGH|CRITICAL",
    "status":        "PENDING",             <- MUST be PENDING — workflow1 skips non-PENDING
    "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/[task_id]_RESULT.md"
  }
  
  OPTIONAL FIELDS:
    "client_facing":  false   <- set true to force Claude escalation regardless of confidence
    "auto_research":  false   <- RESEARCH tasks only: true = Tavily auto-search
    "source":         ""      <- RESEARCH origin: PERPLEXITY_MANUAL | WILL_DIRECT | ANTIGRAVITY
    "file_path":      ""      <- MEDIA/VISION: absolute path to source file
    "output_format":  "md"    <- MEDIA only: md | json | txt
  
  RULES:
  - File extension MUST be .json (trigger only fires on .json)
  - File encoding MUST be UTF-8 without BOM (Set-Content in PowerShell adds BOM — use Out-File -Encoding utf8NoBOM)
  - task_id must be unique
  - Malformed JSON is silently dropped
  
  EXAMPLE (CLASSIFY):
  {
    "task_id": "20260628-001",
    "task_type": "CLASSIFY",
    "topic": "Branch classification for morning walk assets",
    "prompt": "Classify which SFV branch this belongs to: [description]",
    "priority": "NORMAL",
    "status": "PENDING",
    "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260628-001_RESULT.md"
  }
```

---

## SKILL-003 — UPDATE SESSION STATE

```yaml
skill_id: sfv-003-session-state
name: Update SESSION_STATE
version: "1.0"
trigger_patterns:
  - "update session state"
  - "log what we did"
  - "record progress"
  - "end of session"
  - "write session summary"
source_doc: SESSION_STATE.md
content: |
  SESSION_STATE.md is the primary continuity document.
  Location: C:\SFV_BLUEPRINT\SESSION_STATE.md
  
  ALWAYS update at end of every autonomous session step.
  If the session ends without updating SESSION_STATE, context is lost for the next session.
  
  WHAT TO INCLUDE IN AN UPDATE:
  1. Current version number (increment patch: v0.6.2 → v0.6.3)
  2. Date and what was completed
  3. Current infrastructure state (what is running, what is broken)
  4. Open flags (anything unresolved Will needs to know)
  5. Next session priorities (in order)
  
  FORMAT: Add a dated block at the TOP of the verification/history section.
  Never delete old entries. Append, don't overwrite.
  
  UPDATE TRIGGER: After every directive COMPLETE or HUMAN_GATE. Not after every step.
  
  CANONICAL LOCATION OF TRUTH: SESSION_STATE.md > any other doc.
  If there is a contradiction between SESSION_STATE and another doc, SESSION_STATE wins
  for current runtime state. The other doc may need updating as a follow-up.
```

---

## SKILL-004 — WRITE A HANDOFF

```yaml
skill_id: sfv-004-handoff
name: Write a HANDOFF File
version: "1.0"
trigger_patterns:
  - "write handoff"
  - "human gate"
  - "pause for will"
  - "need will's decision"
  - "stop and wait"
  - "cannot proceed"
source_doc: HANDOFF_2026-06-27.md (template reference)
content: |
  A HANDOFF is written when the autonomous loop hits a human gate trigger.
  It pauses the loop. Hermes delivers it to Will's phone. Will responds. Loop resumes.
  
  LOCATION: C:\SFV_BLUEPRINT\00_DEV_LOG\HANDOFF_YYYY-MM-DD.md
  (If a handoff already exists for today, append a new section. Don't overwrite.)
  
  REQUIRED SECTIONS:
  
  ## WHAT WAS COMPLETED (before this gate)
  - Bullet list of what was done in this session so far
  - Current state of each affected file/system
  
  ## DECISION REQUIRED
  - Exactly what Will needs to decide
  - Options (if applicable) with pros/cons
  - Recommended option (clearly labeled as recommendation, not decision)
  
  ## WHAT IS BLOCKED
  - What cannot proceed until Will decides
  - Estimated impact of delay
  
  ## STEPS FOR WILL
  - Numbered, specific, actionable steps for Will to take
  - Include exact commands or file paths where relevant
  
  ## NEXT SESSION PRIORITY ORDER
  - What should happen after Will responds, in order
  
  AFTER WRITING: Set CURRENT_DIRECTIVE.md STATUS to HUMAN_GATE.
  Hermes will ping Will and wait.
  Do not continue autonomous work until Will updates the directive STATUS back to ACTIVE.
```

---

## SKILL-005 — CANON RULES

```yaml
skill_id: sfv-005-canon-rules
name: Canon Rules (All 12)
version: "1.0"
trigger_patterns:
  - "can I"
  - "am I allowed to"
  - "should I"
  - "is this allowed"
  - "what are the rules"
  - "canon rules"
source_doc: 01_CANON_RULES/RULES.md
content: |
  These 12 rules govern everything built under SFV Engine.
  They cannot be overridden without Will's explicit decision.
  When uncertain about any action, check against these rules first.
  
  RULE 01 — NO INVENTION
  Claude does not invent systems. If not discussed and approved, it does not exist.
  
  RULE 02 — LABEL EVERYTHING
  - Approved by Will → CANON
  - Discussed, not locked → UNCONFIRMED
  - Proposed by Claude → FOR HUMAN REVIEW
  - Not current phase → FUTURE
  - Dead end → REJECTED
  
  RULE 03 — HUMAN TASTE IS FINAL
  AI assists. Will finalizes. Especially: archive curation, creative direction, grading, selects, pacing.
  
  RULE 04 — NO ABSOLUTE PATHS
  All paths reference %SFV_ROOT%. Never hardcode drive letters.
  (Exception: Windows boot drive is always C:\ — use C:\ for system tools, env vars for data paths.)
  
  RULE 05 — MODULAR DESIGN
  Every module: isolated, replaceable, debuggable. Failure in one module does not cascade.
  
  RULE 06 — SINGLE SOURCE OF TRUTH
  One authoritative location for metadata, exports, assets, client IDs. No duplicated records.
  
  RULE 07 — BLUEPRINT BEFORE BUILD
  Nothing gets built until the blueprint is deterministic enough that Claude Code is only
  connecting paths, not making decisions.
  
  RULE 08 — NO OWNERSHIP DILUTION
  Nobody gets equity in SFV except Will. Operators, contractors, affiliates: revenue share only.
  
  RULE 09 — R&D PROPOSES, ENGINE IMPLEMENTS
  R&D Terminal proposes improvements. Will approves. Engine implements.
  R&D Terminal never touches production directly.
  
  RULE 10 — VERSIONED EVERYTHING
  Every workflow versioned. Every change logged. Rollback must always be possible.
  
  RULE 11 — SOLVE REAL BOTTLENECKS
  Build for the next real problem. Not imaginary future infrastructure.
  
  RULE 12 — ENGINE INTELLIGENCE PERSISTS
  Hardware is replaceable. Engine intelligence lives in config and scripts, not the machine.
  
  ADDITIONAL RULE (Hermes / autonomous sessions):
  RULE 13 — CANON IS LOCKED DURING AUTONOMOUS RUNS
  Autonomous sessions write DRAFT-status docs only. Will promotes to CANON manually.
  No autonomous session may change the STATUS field of any doc to CANON.
```

---

## SKILL-006 — N8N HEALTH CHECK

```yaml
skill_id: sfv-006-n8n-health
name: n8n Health Check
version: "1.0"
trigger_patterns:
  - "check n8n"
  - "is n8n running"
  - "n8n health"
  - "workflow status"
  - "n8n down"
source_doc: HANDOFF_2026-06-27.md + SESSION_STATE.md
content: |
  n8n runs at: http://127.0.0.1:5678
  Health endpoint: http://127.0.0.1:5678/healthz  (expected: 200 OK)
  PostgreSQL backend: localhost:5432, db: n8n
  
  CURRENT WORKFLOW IDs (PostgreSQL, confirmed live as of 2026-06-27):
    WF1 Queue Processor:  vOH1CsPYvD27sUxx  (active, published)
    WF2 Pre-Warm:         qgOkBV73L21wmvZi  (active, published)
    WF4 Output Monitor:   nRbwsa0K62y2Fnmo  (active, published — WF4 has known process.env bug)
    WF3 Research Handler: NOT YET BUILT
  
  HOW TO CHECK:
  Invoke-WebRequest -Uri "http://127.0.0.1:5678/healthz" -UseBasicParsing
  Expected: StatusCode 200
  
  HOW TO RESTART n8n:
  Run: C:\SFV_BLUEPRINT\start_n8n.ps1
  (This dot-sources n8n_env.ps1 first, then starts n8n)
  
  HOW TO CHECK WORKFLOW ACTIVE+PUBLISHED STATUS:
  Via n8n API (requires API key — not yet minted as of 2026-06-27):
    GET http://127.0.0.1:5678/api/v1/workflows/{id}
  Via UI: n8n → Settings → Workflows → check Active toggle + Published badge
  
  KNOWN ISSUE (2026-06-27):
  WF4 Code node "Guard — DECISION_LOG only" uses process.env which is blocked in
  n8n task-runner sandbox. Fix: replace with $env expression. Not yet applied.
  WF4 errors do NOT affect WF1 (queue processor still fully functional).
  
  IF n8n IS DOWN:
  1. Check Task Manager — is n8n process running?
  2. Run start_n8n.ps1
  3. Check PostgreSQL service: Get-Service postgresql*
  4. If PostgreSQL down: Start-Service postgresql*
  5. Then restart n8n via start_n8n.ps1
  6. If still down: write HANDOFF for Will
```

---

## SKILL-007 — COST GATE BEFORE API CALL

```yaml
skill_id: sfv-007-cost-gate
name: Cost Gate Before API Call
version: "1.0"
trigger_patterns:
  - "about to call claude"
  - "spawn claude -p"
  - "before I run an api call"
  - "cost check"
  - "budget check"
source_doc: COST_CEILING_POLICY.md
content: |
  ALWAYS run this check before spawning claude -p or making any Claude API call.
  
  STEP 1: Read C:\SFV_BLUEPRINT\99_INBOX\COST_ALERTS.md
  - If file has an unresolved row (no [RESOLVED] tag) → check the spend amount
  - If spend is within $2.00 of the hard cap ($25.00): STOP. Write HANDOFF. Ping Will.
  - If spend is below $23.00 and alert row present: proceed but log awareness
  
  STEP 2: Check remaining budget in current directive
  - Read CURRENT_DIRECTIVE.md → MAX_BUDGET_USD field
  - Estimate cost of next claude -p call (rough: 1 turn ≈ $0.05-0.15 for Sonnet)
  - If estimated remaining budget < $0.50: STOP. Write HANDOFF. Ping Will.
  
  STEP 3: If proceeding — log the call
  After each claude -p call, append a row to COST_ALERTS.md:
  | DATE | Claude Code | estimated $X / session | DIR-YYYYMMDD-NNN step N |
  
  HARD CAPS (enforced by Anthropic, not SFV):
  - $25.00 total: Anthropic shuts off all API calls. Will must raise cap in console.
  - Alert threshold: $20.00 (write row, continue)
  - Escalation threshold: $23.00 (stop, write HANDOFF, wait for Will)
  
  TAVILY anomaly check (run daily, not per-call):
  - If Tavily call count today > 200: write COST_ALERTS.md anomaly row. Check n8n for loops.
```

---

## SKILL-008 — GIT CHECKPOINT

```yaml
skill_id: sfv-008-git-checkpoint
name: Git Checkpoint for Autonomous Sessions
version: "1.0"
trigger_patterns:
  - "create checkpoint"
  - "git branch"
  - "before I start a session"
  - "autonomous session start"
  - "backup vault state"
source_doc: 01_CANON_RULES/RULES.md Rule 10
content: |
  BEFORE EVERY AUTONOMOUS SESSION (Hermes triggers this automatically):
  
  1. Create a timestamped branch:
     git -C C:\SFV_BLUEPRINT checkout -b autonomous/DIR-YYYYMMDD-NNN
  
  2. Verify branch created:
     git -C C:\SFV_BLUEPRINT branch --show-current
     (Should return: autonomous/DIR-YYYYMMDD-NNN)
  
  3. Export current n8n workflow snapshots (precaution):
     (Via n8n API or UI export — saves to 03_INFRASTRUCTURE/n8n_workflows/)
  
  DURING SESSION:
  - Commit checkpoints every 5 steps:
    git -C C:\SFV_BLUEPRINT add -A
    git -C C:\SFV_BLUEPRINT commit -m "[DIR-ID] step N checkpoint: [what was done]"
  
  AFTER SESSION (COMPLETE):
  - Final commit on branch:
    git -C C:\SFV_BLUEPRINT add -A
    git -C C:\SFV_BLUEPRINT commit -m "[DIR-ID] COMPLETE: [summary of what directive accomplished]"
  - Leave branch for Will to review and merge to main manually
  - Do NOT push to remote — Will pushes
  
  ROLLBACK (if session produced bad output):
    git -C C:\SFV_BLUEPRINT checkout main
    git -C C:\SFV_BLUEPRINT branch -D autonomous/DIR-YYYYMMDD-NNN
  
  RULE: Every autonomous session runs on a branch. Never on main directly.
  Main is the stable, Will-reviewed state. Branches are work-in-progress.
```

---

## SKILL-009 — BRANCH CLASSIFICATION

```yaml
skill_id: sfv-009-branch-classification
name: SFV Branch Classification
version: "1.0"
trigger_patterns:
  - "which branch"
  - "classify this file"
  - "what branch does this belong to"
  - "branch rules"
  - "sfv branches"
source_doc: BRANCH_OUTPUTS.md
content: |
  SFV has 9 content branches. Each has a defined scope, complexity level, and revenue role.
  
  BRANCH: MYTHOLOGY
  Complexity: Level 1 | Account: SFV_abbass (hub account)
  Content: Overarching brand identity, portfolio highlights, cross-branch reposts
  Revenue: Indirect — brand awareness
  
  BRANCH: LIVE (SFV_LIVE)
  Complexity: Level 3.5
  Content: Event coverage — concerts, shows, gatherings (not paid portraits)
  Revenue: Supporting — builds portfolio and reach
  
  BRANCH: EVENTS (SFV_EVENTS)
  Complexity: Level 5-6.5 | PRIMARY MONEY MAKER
  Content: On-site paid portrait sessions at events and venues
  Revenue: Direct — portrait session fees
  Delivery: Pixieset (client galleries) + Zenfolio QR (on-site delivery)
  
  BRANCH: ATHLETICS (SFV_ATHLETICS)
  Complexity: Level 3.5
  Content: Sports photography — games, training, action shots
  Revenue: Supporting
  
  BRANCH: STUDIO (SFV_STUDIO)
  Complexity: Level 5.5 | Growth branch
  Content: Controlled studio production — portraits, product, editorial
  Revenue: Growing — session fees + licensing potential
  
  BRANCH: UGC (SFV_UGC)
  Complexity: Level 6.5 | PRIMARY MONEY MAKER
  Content: Content creator retainer work for brands and clients
  Revenue: Direct — monthly retainer fees (primary revenue engine)
  Note: Handle + pricing still UNCONFIRMED as of last audit
  
  BRANCH: ARCHIVE (SFV_ARCHIVE)
  Complexity: Level 3.5
  Content: Portfolio and legacy work — curated historical shots
  Revenue: Indirect — credibility and licensing
  Rule: HUMAN TASTE ONLY — AI never curates archive
  
  BRANCH: WORLD (SFV_WORLD)
  Complexity: Level 2.5 | Alias/life
  Content: Personal creative work, travel, life outside the studio
  Revenue: None — brand building only
  
  BRANCH: 404 (SFV_404)
  Complexity: Level 2.5 | Experimental
  Content: Experimental creative — pushing boundaries, testing new formats
  Revenue: None — R&D creative output
  
  CLASSIFICATION RULE: When uncertain between two branches, always escalate to HANDOFF.
  Misclassification in archive or delivery context can affect client deliverables.
```

---

## SKILL-010 — DIRECTIVE INTERPRETATION

```yaml
skill_id: sfv-010-directive
name: CURRENT_DIRECTIVE Interpretation
version: "1.0"
trigger_patterns:
  - "read the directive"
  - "what's the current task"
  - "current directive"
  - "what am I doing"
  - "interpret directive"
source_doc: 01_CANON_RULES/DIRECTIVE_TEMPLATE.md
content: |
  CURRENT_DIRECTIVE.md is located at: C:\SFV_BLUEPRINT\CURRENT_DIRECTIVE.md
  It is the single source of truth for what the autonomous session should do.
  Read it FIRST before taking any action.
  
  KEY FIELDS AND HOW TO INTERPRET THEM:
  
  STATUS field:
  - ACTIVE: proceed with the directive
  - IN_PROGRESS: already running (Hermes sets this when loop starts)
  - HUMAN_GATE: do not start — waiting for Will response
  - PAUSED: do not start — Will deliberately paused
  
  OBJECTIVE: What should exist at the end that doesn't exist now.
  Read this first. Understand the end state before reading the steps.
  
  SCOPE_BOUNDS (ALLOWED / NOT ALLOWED):
  Critical. If an action is not in ALLOWED, do not take it.
  If the work requires touching something not in ALLOWED: write HANDOFF, stop.
  "NOT ALLOWED: do not promote anything to CANON" — this is always present and always applies.
  
  SUCCESS_CRITERIA: How to know when the directive is DONE.
  Check each criterion before writing the COMPLETION_FILE.
  All criteria must pass. Partial completion is not complete.
  
  HUMAN_GATE_TRIGGERS: Non-negotiable stop conditions.
  If any trigger fires: immediately write HANDOFFS/DIR-YYYYMMDD-NNN_GATE_NNN.md
  Set CURRENT_DIRECTIVE.md STATUS to HUMAN_GATE. Ping Will via Telegram. Stop.
  
  CONTEXT FILES TO READ FIRST: Read all of them before starting work.
  SESSION_STATE.md is always in this list. COMPRESSED_CONTEXT.md is always in this list.
  
  MAX_TURNS and MAX_BUDGET_USD: Hard limits passed to claude -p.
  If a directive needs more turns to complete properly, write HANDOFF recommending
  the limit be raised. Do not just keep going past the limit.
  
  COMPLETION FILE: When all success criteria pass, write:
    C:\SFV_BLUEPRINT\STEP_RESULTS\DIR-YYYYMMDD-NNN_COMPLETE.md
  Include: what was done, criteria checked, any follow-up items.
  Hermes reads this file to detect directive completion and pings Will.
```

---

## IMPORT INSTRUCTIONS FOR CLAUDE CODE

> During the Hermes integration session, Claude Code runs these steps:

```powershell
# 1. Create Hermes skills directory in vault
New-Item -ItemType Directory -Path "C:\SFV_BLUEPRINT\.hermes\skills" -Force

# 2. Copy each skill file
# (Claude Code converts YAML blocks above into individual .yaml files)
# Naming: sfv-001-system-context.yaml, sfv-002-queue-task.yaml, etc.

# 3. Import into Hermes
# (Hermes import command — confirm exact syntax from Hermes docs after install)
# hermes skills import C:\SFV_BLUEPRINT\.hermes\skills\*.yaml

# 4. Verify import
# hermes skills list
# Should show 10 skills: sfv-001 through sfv-010
```

---

## CONNECTED FILES
- [[MASTER_CONTEXT|Master Context]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[JOB_ENVELOPE_SPEC|Job Envelope Specification]]
- [[ANTIGRAVITY|Antigravity]]
- [[CLAUDE|Claude]]
- [[TOOL_STACK|Tool Stack]]
