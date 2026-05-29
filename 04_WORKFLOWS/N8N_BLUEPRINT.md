---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
DATE: 2026-05-26
SOURCE: PERPLEXITY PRO RESEARCH
CANON_APPROVAL_REQUIRED: WILL
---

# SFV Engine — Blueprint Stage Workflow Architecture

***

## 1. Wikilink Failures — Root Cause & Fix

### Root Cause

**A — Git case sensitivity mismatch.** NTFS is case-insensitive, Git on Windows defaults to `core.ignorecase=true`. File renames with only a case change (e.g. `SFV_Studio.md` → `SFV_STUDIO.md`) are not registered by Git, leaving ghost files in the index that Obsidian resolves to broken links.

**B — Smart Connections races against Git sync.** Smart Connections indexes on vault open. When Git pulls mid-write, the plugin processes incomplete files, creating broken embedding references that surface as wikilink failures.

**C — Dataview renders virtual content, not physical files.** Links resolved through Dataview queries instead of physical files appear broken to any tool reading the vault as a file tree (n8n, Antigravity, Python scripts). Not a wikilink bug — a Dataview/Smart Connections architectural incompatibility.

### Fix Steps

1. Force Git to recognize case renames:
```powershell
cd C:\SFV_BLUEPRINT
git config core.ignorecase false
git rm -r --cached .
git add .
git commit -m "fix: force case-sensitive tracking"
```

2. Rename Twice for any case-mismatched file in Obsidian:
   - Rename `SFV_Studio.md` → `SFV_STUDIOx.md` → `SFV_STUDIO.md`
   - Requires: Settings > Files & Links > Automatically update internal links = ON

3. Set consistent link format:
   - Settings > Files & Links > New link format → Shortest path that uniquely identifies file
   - Use [[Wikilinks]] → ON. Do NOT switch to Markdown links.

4. Fix Smart Connections race:
   - Disable "Auto-import on startup"
   - After each Git pull: manually trigger Smart Connections > Refresh All (prune + import) > Force Refresh All
   - Long-term: PowerShell script delays Smart Connections indexing 10s after Git pull

5. Freeze Dataview-dependent links:
   - Use `dv.queryMarkdown()` for any note Smart Connections or external scripts must read
   - Add to Templater template for files in `05_AI_LAYER/` and `04_WORKFLOWS/`

**Build first:** Git case fix + Rename Twice pass. **Defer:** Dataview freezing.

***

## 2. Ollama ↔ Claude Handoff Loop

### Folder Structure
```
C:\SFV_BLUEPRINT\99_INBOX\
  QUEUE\       ← Will or n8n drops task JSON here
  HANDOFFS\    ← Ollama writes compressed handoff files here
  OUTPUTS\     ← Final outputs land here
```

### Handoff File Format

Ollama writes to `HANDOFFS\` using this schema:

```json
{
  "handoff_id": "20260526-003",
  "task_type": "BLUEPRINT_REVIEW | COMPLEX_CODE | REASONING",
  "priority": "HIGH | NORMAL",
  "source_task": "QUEUE/20260526-003_TASK.json",
  "context_budget_tokens": 1500,
  "summary": "2-3 sentence plain-English description",
  "key_findings": ["Finding 1", "Finding 2"],
  "unresolved": ["Exact question or decision needed from Claude"],
  "relevant_files": ["C:\\SFV_BLUEPRINT\\04_WORKFLOWS\\INGEST.md"],
  "do_not_include": ["Files Ollama already read — Claude should not re-read"],
  "ollama_confidence": "LOW | MEDIUM | HIGH",
  "escalation_reason": "Why Ollama is handing off instead of completing"
}
```

**Token ceiling:** Handoff JSON + relevant file content combined must stay under 8,000 tokens. Ollama enforces this. Exceeding budget → Ollama writes compressed excerpt and flags it.

### Trigger Logic

n8n watches `HANDOFFS\` via Local File Trigger. On new file:
- `BLUEPRINT_REVIEW | COMPLEX_CODE | REASONING` → Claude (HTTP webhook or manual notification)
- `LOW_CONFIDENCE` on classifiable task → re-queue with different Ollama prompt
- `HIGH_CONFIDENCE` on classifiable task → write directly to OUTPUTS, skip Claude

### Ollama Compression Prompt Template

Store at `05_AI_LAYER/OLLAMA_PROMPTS/handoff_generator.txt`:

```
You are a context compression agent. Read the attached task file.
Your output is a JSON handoff for Claude. Rules:
- summary: max 3 sentences, plain English, no jargon
- key_findings: max 5 bullets, each under 20 words
- unresolved: only list what genuinely requires high reasoning
- context_budget_tokens: estimate your JSON output token count, keep under 1500
- If you can complete the task fully: do so. Write to OUTPUTS. Do NOT create a handoff.
- Only create a handoff if: (1) task needs web data, (2) task needs canon editing, (3) ollama_confidence = LOW
Output valid JSON only. No commentary.
```

**Build first:** Handoff format + n8n trigger. **Defer:** Confidence scoring calibration — start with all handoffs going to Claude, tune after 10+ real tasks.

***

## 3. N8N Core Workflows

### CRITICAL — Local File Trigger on Windows

Run n8n via npm (`npx n8n`), NOT Docker. Docker on Windows does not reliably propagate host-side inotify file events through the filesystem layer. This is a hard constraint.

Windows path fix for all file nodes: `{{ $json.path.replace(/\\/g, '\\\\') }}`

***

### Workflow 1 — Queue Processor

**Trigger:** Local File Trigger
- Folder: `{{ $env["VAULT_PATH"] }}\99_INBOX\QUEUE`
- Watch for: Files added

**Nodes:**
1. Local File Trigger → file path
2. Code node → fix Windows backslash
3. Read/Write Files from Disk → Read JSON file
4. Code node → `JSON.parse()` → extract `task_type`, `requires_web`, `priority`
5. Switch node:
   - `CLASSIFY | SUMMARIZE | COMPRESS` → Branch A: Ollama
   - `RESEARCH` → Branch B: Tavily (Workflow 3)
   - `BLUEPRINT | CODE` → Branch C: write handoff for Claude
6. Branch A — HTTP Request (Ollama):
   - POST `{{ $env["OLLAMA_URL"] }}/api/generate`
   - Body: `{ "model": "{{ $env["OLLAMA_MODEL"] }}", "prompt": "[task content]", "stream": false }`
7. Code node → extract `response` → format as markdown
8. Read/Write Files from Disk → Write to `OUTPUTS\[task_id]_RESULT.md`
9. Code node → append to `DECISION_LOG.md`

***

### Workflow 2 — File Watcher / Ingest Trigger

**Trigger:** Local File Trigger
- Folder: `{{ $env["FIELD_INGEST_PATH"] }}`
- Watch for: Files added
- Ignore: `**/*.tmp`, `**/*.lrcat`, `**/*.DS_Store`
- Max Folder Depth: 2

**Nodes:**
1. Local File Trigger → file path
2. Code node → extract extension → filter for `.jpg .jpeg .cr3 .mp4 .mov`
3. Switch node → Photo branch / Video branch
4. Execute Command node:
```
python {{ $env["VAULT_PATH"] }}\99_INBOX\ingest.py --branch {{ detected_branch }} --tag {{ detected_tag }} --source {{ $json.path }}
```
5. Code node → parse ingest.py stdout
6. Read/Write Files from Disk → append to DECISION_LOG

**Defer:** Auto branch/tag detection. For May 28 hardcode `--branch SFV_STUDIO --tag MORNINGWALK`.

***

### Workflow 3 — Research Layer (Tavily)

**Tavily is correct for this use case.** Native n8n node, AI-ready structured results, 1,000 free credits/month, 1 credit per basic search call.

| Tool | Free Tier | n8n Native | Verdict |
|------|-----------|------------|---------|
| Tavily | 1,000/mo | Yes | USE |
| Brave Search | 2,000/mo | HTTP only | Backup |
| Serper | 100/mo | HTTP only | Skip |
| Exa | Limited | HTTP only | Skip |

**Trigger:** Called as subworkflow from Queue Processor Branch B

**Nodes:**
1. Receive task payload (query, task_id)
2. Tavily node → Search, basic depth, max 5 results
3. Code node → format as structured markdown
4. Read/Write Files from Disk → Write to `OUTPUTS\[task_id]_RESEARCH.md`
5. Code node → check `requires_synthesis` flag:
   - YES → write handoff to `HANDOFFS\`
   - NO → write to OUTPUTS, log to DECISION_LOG

***

### Workflow 4 — Output Monitor

**Trigger:** Local File Trigger
- Folder: `{{ $env["VAULT_PATH"] }}\99_INBOX\OUTPUTS`
- Watch for: Files added

**Nodes:**
1. Local File Trigger → file path
2. Code node → extract task_id from filename (regex: `^\d{8}-\d{3}`)
3. Read/Write Files from Disk → Read file → extract first 3 lines
4. Code node → build log table row: `| timestamp | task_id | filename | summary | AUTO |`
5. Read/Write Files from Disk → Read DECISION_LOG → append row → Write back

**Note:** DECISION_LOG.md must be markdown table format before activating this. Convert it first.

***

### Workflow 5 — Blueprint Sync (COMPRESSED_CONTEXT Auto-Update)

**Trigger:** Local File Trigger
- Folder: `{{ $env["VAULT_PATH"] }}`
- Watch for: Files changed
- Match: `SESSION_STATE.md`, `MASTER_CONTEXT.md`, `AI_USE_CASE_PROFILE.md`

**Nodes:**
1. Local File Trigger → changed file path
2. Switch node → confirm it's one of the three source files
3. Read/Write Files from Disk → Read all three
4. HTTP Request → Ollama: compress to COMPRESSED_CONTEXT schema
5. Code node → prepend YAML frontmatter with updated `LAST_UPDATED`
6. Read/Write Files from Disk → Write to `COMPRESSED_CONTEXT_DRAFT.md` (NOT canon file directly)
7. Log to DECISION_LOG

**RISK FLAG:** Ollama must write to `COMPRESSED_CONTEXT_DRAFT.md`. Will reviews and renames. Do NOT auto-overwrite the CANON `COMPRESSED_CONTEXT.md`.

**Add debounce:** Wait node (5 min) + check if workflow already running before Ollama call.

***

## 4. Model Linking — Config Approach

Create `C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_env.ps1`:

```powershell
$env:OLLAMA_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "qwen3:14b"
$env:OLLAMA_MODEL_FAST = "qwen3:14b"
$env:VAULT_PATH = "C:\SFV_BLUEPRINT"
$env:ACTIVE_STORAGE = "D:\SFV_ACTIVE"
$env:FIELD_INGEST_PATH = "E:\"
$env:TAVILY_API_KEY = "tvly-YOUR_KEY_HERE"
$env:DECISION_LOG = "C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md"

npx n8n
```

Reference in n8n nodes: `{{ $env["OLLAMA_MODEL"] }}`

Add optional `model_override` field to task JSON — Queue Processor uses it if present, overrides global env var.

***

## 5. Token Optimization

**Claude hard ceiling: 8,000 tokens per call.**
- Handoff JSON: ~500 tokens
- Relevant file excerpts: ~5,000 tokens
- Task instruction: ~500 tokens
- Buffer: ~2,000 tokens

Beyond 8,000 → decompose further or route to Google AI Studio (1M context, free).

### Routing Matrix

| Task Type | First Router | Escalate If | Never Claude |
|-----------|-------------|-------------|--------------|
| Branch classification | Ollama | Confidence < 70% | Direct classification |
| File summarization | Ollama | >500 token summary needed | Short summaries |
| Web research | Tavily → Ollama format | Synthesis needed | Raw search |
| Blueprint writing | Claude | — | Simple templating |
| Code generation (canon) | Claude | — | Non-canon scripts |
| System audit | Antigravity | — | Single-file review |
| Massive context read | Google AI Studio | — | Files > 50k tokens |
| Overnight batch | Ollama daemon | — | Batch processing |

### Ollama Compression Rules Before Handoff

Strip: YAML frontmatter, `---` dividers, Obsidian syntax (`[[links]]`, `#tags`, callouts), repeated headers, sections already processed in previous tasks.

Target: **60-70% compression.** 5,000-token file → 1,500-token structured handoff.

**Rule:** If `ollama_confidence: HIGH` → never escalate to Claude regardless of task type. Calibrate over first 30 tasks, then set threshold.

***

## 6. Blueprint Stage Tooling

### Build in n8n UI — not Claude Code JSON import.

n8n JSON schema changes between versions. Import failures are opaque. Build manually in UI — it is the correct tool.

### Build Order (this stage)

| Step | Task | Owner | When |
|------|------|-------|------|
| 1 | `git config core.ignorecase false` + commit | Will + Antigravity | Tonight |
| 2 | Write and test `n8n_env.ps1` | Antigravity | Tonight |
| 3 | Run `ingest.py --dry-run` for May 28 | Will | May 27 |
| 4 | Extend `ollama_queue_test.py` to simulate Queue Processor | Ollama / Claude Code | May 27 |
| 5 | Install n8n via npm, verify localhost:5678 | Will + Antigravity | May 27 |
| 6 | Build Workflow 4 (Output Monitor) in n8n UI | Will | May 27 |
| 7 | Build Workflow 1 (Queue Processor, Ollama branch) | Will | May 27 |
| 8 | Morning Walk pipeline end-to-end test | Will | May 28 |
| 9 | Build Workflow 3 (Tavily research) | Will | After May 28 |
| 10 | Build Workflow 2 (File Watcher / Ingest) | Will | After May 28 |
| 11 | Build Workflow 5 (Blueprint Sync) | Will | After June 6 |

***

## Flags and Contradictions vs Vault

- **CONTRADICTION:** `COMPRESSED_CONTEXT.md` lists n8n as FUTURE. Clarify: is n8n being installed before May 28? ingest.py runs without it. If May 28 is hard deadline, skip n8n for Morning Walk entirely and build after.
- **GAP:** `ENGINE_COMMUNICATION_MODEL.md` does not specify DECISION_LOG format (table vs freeform). Standardize before building Workflow 4.
- **RISK:** Workflow 5 must write to `COMPRESSED_CONTEXT_DRAFT.md` not the CANON file. Ollama cannot auto-overwrite CANON.
- **MONITOR:** Tavily free tier = 1,000 credits/month. Watch usage once automated workflows are live.
- **CONFIRMED:** `ollama_queue_test.py` already exists and tested. Extend it — do not rebuild.

## CONNECTED FILES
- [[03_INFRASTRUCTURE/ENVIRONMENT_CONFIG|Environment Config]]
- [[03_INFRASTRUCTURE/NAMING_CONVENTIONS|Naming Conventions]]
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
