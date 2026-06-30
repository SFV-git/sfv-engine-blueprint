---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-06-09
---

# MYTHOS FORWARD-PLANNING PROMPT

Use this prompt in Google AI Studio (1M context) before any major phase gate.
Paste full vault dump after the --- VAULT BELOW --- line.
Output comes back to Claude Chat for vault integration — never write MYTHOS output directly to CANON.

---

## PROMPT

You are the strategic planner for SFV Engine — a local AI-powered media production and management
system built by one person (Will, Halifax). Read every document in the vault below.

Produce exactly four deliverables. No preamble. No system explanation. Just the deliverables.

---

### DELIVERABLE 1 — EXECUTION ORDER

The single correct sequence of all remaining build tasks.
No task appears before its prerequisites are complete.
Format per item:
  [N]. TASK NAME | why it's next | what it unblocks | estimated Will-time to execute

Separate into two groups:
  GROUP A — Can be done without Engine Body (planning, decisions, remote tasks)
  GROUP B — Requires Engine Body to be physically on and accessible

---

### DELIVERABLE 2 — R&D TERMINAL REINSTALL RUNBOOK

Every step to rebuild R&D Terminal from scratch post-Win11, in order.
Include exact PowerShell commands where possible.
Flag each step that requires Engine Body to be reachable on the network.
Sections:
  1. Ollama install + model pulls (qwen3:8b, qwen3:14b) + env vars
  2. Syncthing install + pair with Engine Body (Device ID: 5U7DSVN-NIWPDSV-2D4U276-BPP72LW-PAMBCH4-SZHVUBM-INK6DEL-EN6CIA5)
  3. Claude Code install + CLAUDE_CONFIG_DIR setup (.claude-rnd/)
  4. windows_exporter install + verify
  5. Post-install verification checklist

---

### DELIVERABLE 3 — THEORY RUNS

Walk each scenario through the full stack. At each step name the component, what it does,
and what breaks or succeeds. End each run with a FAILURE MODES list and PATCHES NEEDED.

Scenario A: Full SFV_EVENTS shoot day end-to-end
  Shoot → SD card → ingest to E:\ → QR match → file naming → move to D:\SFV_ACTIVE\BRANCHES\SFV_EVENTS\
  → Lightroom import → cull → batch edit → export → Zenfolio upload → QR-linked delivery

Scenario B: Engine Body Ollama crashes mid-queue
  10 jobs in QUEUE\, 1 IN_PROGRESS, Ollama dies
  → n8n response → watchdog.ps1 response → queue state → recovery path → what gets lost vs recovered

Scenario C: RESEARCH task hits workflow1, routes to workflow3 (which does not exist)
  Job envelope arrives → workflow1 reads task_type: RESEARCH → routes → finds nothing → what happens
  → Error handling → fallback → queue state → Will notification path

---

### DELIVERABLE 4 — UGC PRE-PRODUCTION MANAGER SPEC

Full product spec for a standalone React app (no backend initially — localStorage or flat JSON).
Sections:
  PURPOSE: What problem it solves for Will and clients like Brandon Bellotti
  DEFENSIBLE WEDGE: Why this is hard to replicate (creator-ops memory layer)
  DATA LAYER: What gets persisted (gear DB, location DB, client history, shot pattern history)
  CORE FEATURES (MVP): List each with one-line description
  AUTO-GENERATION: What the app generates automatically from stored data (shot lists, gear lists, call sheets)
  BRANDON BELLOTTI INTEGRATION: How to use him as design partner — what to show him, what questions to ask
  BUILD ORDER FOR CLAUDE CODE: Exact sequence of components to build, each as a Claude Code task

---

Flag any item UNCONFIRMED or FOR HUMAN REVIEW where relevant.
Do not ask clarifying questions. Make recommendations where decisions are needed and label them RECOMMENDATION.

--- VAULT BELOW ---
[PASTE OUTPUT OF POWERSHELL DUMP COMMAND]

## VAULT DUMP COMMAND (run in PowerShell on Engine Body)

```powershell
Get-ChildItem C:\SFV_BLUEPRINT -Recurse -Filter "*.md" |
  Where-Object { $_.FullName -notmatch '\.git|\.obsidian|\.smart-env|node_modules' } |
  ForEach-Object { "=== $($_.FullName) ===`n" + (Get-Content $_.FullName -Raw) + "`n`n" } |
  Set-Clipboard
```

Then paste clipboard contents after "--- VAULT BELOW ---" above.

## CONNECTED FILES
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[05_AI_LAYER/RATE_LIMITS|Rate Limits]]
- [[COMPRESSED_CONTEXT|Compressed Context]]
