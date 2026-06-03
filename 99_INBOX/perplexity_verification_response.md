# ANTIGRAVITY RESPONSE — Perplexity Verification Report (Step 3 of 4)

**Status:** ALL FLAGS RESOLVED — 4 corrections accepted with vault-specific notes, 2 flags answered below.

---

## Vault Cross-Reference — Corrections

### CORRECTION 1 — qwen3:8b vs qwen3:14b (R&D Terminal model roster)

**Accepted with modifications.**

Current vault state: [OLLAMA_SETUP.md](file:///c:/SFV_BLUEPRINT/05_AI_LAYER/OLLAMA_SETUP.md) specifies `qwen3:14b` for Engine Body (RTX 5080). [LOCAL_MODELS.md](file:///c:/SFV_BLUEPRINT/05_AI_LAYER/LOCAL_MODELS.md) has outdated model list (DeepSeek, Llama 3.1 — both stale).

**For R&D Terminal (RTX 3060 12GB):**

| Model | Role | VRAM | Action |
|---|---|---|---|
| `qwen3:8b` | Primary: classify, summarize, route | ~5.2 GB | `ollama pull qwen3:8b` |
| `qwen3:14b` Q4_K_M | Secondary: code, complex reasoning | ~10 GB | `ollama pull qwen3:14b` |

> [!IMPORTANT]
> **Never load both simultaneously.** The R&D Terminal has 12GB VRAM. Loading 8b (~5.2GB) + 14b (~10GB) = OOM. Ollama must fully unload the current model before loading the next. Set `OLLAMA_NUM_PARALLEL=1` on the R&D Terminal and ensure `OLLAMA_KEEP_ALIVE` is short (e.g. `2m`) to avoid stale model hogging VRAM.

**Drop `qwen2.5-coder:7b` from R&D Terminal.** It's already installed on Engine Body ([SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L151) — confirmed 4.7GB pull). R&D Terminal should not duplicate it — `qwen3:14b` covers code tasks at higher quality.

**Vault docs to update:**
- [LOCAL_MODELS.md](file:///c:/SFV_BLUEPRINT/05_AI_LAYER/LOCAL_MODELS.md) — Replace stale model list with qwen3:8b + qwen3:14b
- [ENVIRONMENT_CONFIG.md](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/ENVIRONMENT_CONFIG.md#L61) — `RND_MODEL` should become `RND_MODEL_FAST=qwen3:8b` + `RND_MODEL_HEAVY=qwen3:14b`

---

### CORRECTION 2 — n8n Local File Trigger env var

**Already mitigated in the vault.** 

[start_n8n.ps1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/start_n8n.ps1#L3-L7) already sets `$env:NODES_EXCLUDE = "[]"` which re-enables `localFileTrigger`. This is the canonical n8n v2.0+ workaround.

> [!WARNING]
> However, Perplexity's report mentions `N8N_ENABLE_LOCAL_FILE_NODE`. This is a **different env var** introduced in even newer n8n versions. Our current approach (`NODES_EXCLUDE=[]`) works on **n8n v2.22.5** (confirmed live in [SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L31)). If n8n is upgraded beyond v2.22.x, test that `localFileTrigger` still activates. If it doesn't, add `$env:N8N_ENABLE_LOCAL_FILE_NODE = "true"` to `start_n8n.ps1`.

**No action needed now.** Add to [start_n8n.ps1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/start_n8n.ps1) as a defensive measure:
```powershell
$env:N8N_ENABLE_LOCAL_FILE_NODE = "true"  # Belt-and-suspenders for future n8n upgrades
```

---

### CORRECTION 3 — Syncthing `fsWatcherDelayS` = 10s default

**Accepted.** This is a real latency multiplier for tight loops.

Current vault state: [AI_STACK_ARCHITECTURE_BLUEPRINT.md §2](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md#L102-L105) mentions Syncthing for vault sync but does not specify watcher tuning.

**Action:** After Syncthing is configured on R&D Terminal, edit `%APPDATA%\Syncthing\config.xml`:
```xml
<folder id="sfv-vault" label="SFV_BLUEPRINT" path="C:\SFV_BLUEPRINT" ...>
  <fsWatcherDelayS>1</fsWatcherDelayS>
</folder>
```

Only set this on the **sending node** (whichever node originates the file change). Restart Syncthing after saving.

**Vault doc to update:** Add `fsWatcherDelayS=1` requirement to [AI_STACK_ARCHITECTURE_BLUEPRINT.md §2](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md#L102-L105) under Sync Strategy.

---

### CORRECTION 4 — Ollama `OLLAMA_HOST` for remote access

**Already done.** [SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L174) confirms:
> `✅ OLLAMA_HOST=0.0.0.0:11434` — set at Machine scope on Engine Body (2026-05-27 session)

[AI_STACK_ARCHITECTURE_BLUEPRINT.md §1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md#L72) also documents this:
> `Set OLLAMA_HOST=0.0.0.0:11434 as a system environment variable on Node A.`

Cross-node confirmed live at `http://192.168.137.1:11434` from R&D Terminal ([SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L285)).

**No action needed.**

---

## FLAG A — Syncthing → n8n Race Condition (RESOLVED)

### Question: Does n8n's chokidar-based watcher correctly see only the final move event, or also fire on `.syncthing.*.tmp` files?

### Answer: **It fires on both — but the architecture prevents the problem.**

**How chokidar works in n8n's `localFileTrigger`:**

n8n uses [chokidar](https://github.com/paulmillr/chokidar) v3.x for file watching. On Windows, chokidar uses the `ReadDirectoryChangesW` Win32 API (not inotify — that's Linux). It fires on:
- `add` — new file appears in watched directory
- `change` — existing file content modified
- `unlink` — file removed

**How Syncthing writes files:**

Syncthing writes to `.syncthing.filename.tmp` in the **same directory** as the target file, then performs an atomic rename (`MoveFileEx` on Windows) to the final filename. This generates two events in chokidar:
1. `add` event for `.syncthing.filename.tmp` (the temp file)
2. `add` event for `filename.json` (the final atomic rename)
3. `unlink` event for `.syncthing.filename.tmp` (cleanup)

**The risk:** n8n's `localFileTrigger` will fire on event #1 (the `.tmp` file), attempting to read and parse an incomplete temporary file. This causes either:
- A JSON parse error (workflow crashes on that execution)
- A partial read (corrupted task processing)

### Mitigation (two-layer defense):

**Layer 1 — n8n file pattern filter:**

In n8n's `localFileTrigger` node config, set the **"Watch Specific Files"** glob pattern to:
```
*.json
```
This makes chokidar only fire on files matching `*.json`. The `.syncthing.*.tmp` files won't match, so event #1 is ignored entirely. The `add` event for the final `.json` file (event #2) fires normally.

**Layer 2 — Syncthing ignore pattern (defense in depth):**

Add to `.stignore` on both nodes:
```
// Already standard Syncthing ignores:
(?d).syncthing.*.tmp
```
This is actually already Syncthing's default behavior — it never *syncs* `.tmp` files between nodes. But the important point is the **local** `.tmp` file still appears on disk during the write process, which is what chokidar sees.

**Layer 1 is the fix. Layer 2 is already in place by default.**

> [!TIP]
> All four workflows in [N8N_BLUEPRINT.md](file:///c:/SFV_BLUEPRINT/04_WORKFLOWS/N8N_BLUEPRINT.md) that use `localFileTrigger` (Workflows 1, 2, 4, 5) should have their file pattern filters set to match only the expected file extensions (`.json`, `.md`, `.jpg`, etc.). This prevents accidental triggering on any temp files from any source — not just Syncthing.

### Additional debounce for Workflow 5 (Blueprint Sync):

[N8N_BLUEPRINT.md](file:///c:/SFV_BLUEPRINT/04_WORKFLOWS/N8N_BLUEPRINT.md#L231) already specifies:
> *Add debounce: Wait node (5 min) + check if workflow already running before Ollama call.*

This Wait node also absorbs any Syncthing race condition naturally. No further changes needed for Workflow 5.

---

## FLAG B — Two Claude Code Instances, Same Account (RESOLVED)

### Question: Can Engine Body and R&D Terminal both run Claude Code sessions without cross-contamination?

### Answer: **Yes — with `CLAUDE_CONFIG_DIR` isolation. Perplexity's finding is correct and the workaround is sound.**

**The problem in detail:**

Claude Code stores its state in `~/.claude/` by default:
- `.credentials.json` — API auth tokens
- `settings.json` / `settings.local.json` — per-project settings
- Internal state files — conversation history, session context

When two Claude Code instances share the same `~/.claude/`, they share:
1. **Auth state** — one session logout/rate-limit affects the other
2. **Settings** — permission changes propagate unexpectedly
3. **Session context** — chat history bleeds across sessions

Working in **different directories** (`C:\SFV_BLUEPRINT` on Engine Body vs a different working dir on R&D Terminal) prevents some contamination, but not auth/settings conflicts.

**The fix — `CLAUDE_CONFIG_DIR` per node:**

```powershell
# On R&D Terminal, add to your PowerShell profile or startup script:
$env:CLAUDE_CONFIG_DIR = "C:\SFV_BLUEPRINT\.claude-rnd"

# Then launch Claude Code:
claude --dangerously-skip-permissions
```

```powershell
# On Engine Body, leave default (~/.claude/) or explicitly set:
$env:CLAUDE_CONFIG_DIR = "C:\SFV_BLUEPRINT\.claude-engine"
```

This gives each node its own:
- Credential store (independent rate limiting)
- Settings file (independent permission grants)
- Session state (no history bleed)

> [!WARNING]
> **Both directories must be git-ignored.** The existing [.gitignore](file:///c:/SFV_BLUEPRINT/.gitignore) excludes `.obsidian/` and `.smart-env/` but does NOT currently exclude `.claude-rnd/` or `.claude-engine/`. Add these before creating the directories.

**For the `--dangerously-skip-permissions` bug:**

Per Perplexity's finding, add to **each** node's config directory:
```json
// .claude-engine/settings.json (Engine Body)
// .claude-rnd/settings.json (R&D Terminal)
{
  "defaultMode": "bypassPermissions"
}
```

This ensures the `Edit` tool doesn't re-prompt during unattended loops.

> [!IMPORTANT]
> The existing [.claude/settings.local.json](file:///c:/SFV_BLUEPRINT/.claude/settings.local.json) contains project-scoped permission rules (git, curl, PowerShell, etc.). When migrating to per-node config dirs, **copy this file** into both `.claude-engine/` and `.claude-rnd/` so the permission allowlist isn't lost.

---

## Vault Update Checklist (Priority Order)

All corrections and flag resolutions produce these required vault changes:

| # | File | Change | Priority |
|---|---|---|---|
| 1 | [start_n8n.ps1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/start_n8n.ps1) | Add `$env:N8N_ENABLE_LOCAL_FILE_NODE = "true"` (defensive) | 🟠 High |
| 2 | [n8n_env.ps1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/n8n_env.ps1) | Add `$env:NODES_EXCLUDE = "[]"` to match start_n8n.ps1 | 🟠 High |
| 3 | [.gitignore](file:///c:/SFV_BLUEPRINT/.gitignore) | Add `.claude-rnd/` and `.claude-engine/` entries | 🟠 High |
| 4 | [LOCAL_MODELS.md](file:///c:/SFV_BLUEPRINT/05_AI_LAYER/LOCAL_MODELS.md) | Replace stale model list with `qwen3:8b` + `qwen3:14b` for R&D Terminal | 🟡 Medium |
| 5 | [ENVIRONMENT_CONFIG.md](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/ENVIRONMENT_CONFIG.md) | Split `RND_MODEL` into `RND_MODEL_FAST` + `RND_MODEL_HEAVY` | 🟡 Medium |
| 6 | [AI_STACK_ARCHITECTURE_BLUEPRINT.md §2](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md) | Add `fsWatcherDelayS=1` to Syncthing sync config | 🟡 Medium |
| 7 | [N8N_BLUEPRINT.md](file:///c:/SFV_BLUEPRINT/04_WORKFLOWS/N8N_BLUEPRINT.md) | Add `*.json` file pattern filter note to all `localFileTrigger` workflows | 🟡 Medium |
| 8 | [AI_STACK_ARCHITECTURE_BLUEPRINT.md §7](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md) | Drop `qwen3.6-coder` from Phase 1 action item #212, replace with `qwen3:14b` for R&D Terminal | 🟡 Medium |

---

## Items Already Handled in Vault (No Action Needed)

| Item | Where | Status |
|---|---|---|
| `OLLAMA_HOST=0.0.0.0` on Engine Body | Set at Machine scope, confirmed [SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L174) | ✅ Done |
| `NODES_EXCLUDE=[]` in n8n launcher | [start_n8n.ps1](file:///c:/SFV_BLUEPRINT/03_INFRASTRUCTURE/start_n8n.ps1#L7) | ✅ Done |
| `winget install Ollama.Ollama` | Ollama installed on both nodes ([SESSION_STATE.md](file:///c:/SFV_BLUEPRINT/SESSION_STATE.md#L274)) | ✅ Done |
| `qwen3:14b` model tag | Live on Engine Body (`ollama list` confirmed) | ✅ Done |

---

**Step 3 complete. All flags resolved. Ready for Step 4 — vault updates on your approval.**
