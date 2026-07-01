# TWO-TERMINAL ATTACK PLAN — TONIGHT
## SFV Engine: Engine Body + R&D Terminal → Self-Developing Loop

---

## AGENT LOOP CONTEXT — READ FIRST

This plan moves through a verification chain. Every agent must know its position:

```
[1] CLAUDE (chat)      → AUTHORED this plan. Reasoning + architecture layer.
                          Defines WHAT to build and WHY.
        ↓
[2] PERPLEXITY PRO     → VERIFIES technical accuracy. Research layer.
                          Checks: Are commands current? Do these flags exist?
                          Is the install order correct for Windows 11 / these versions?
                          Flags anything outdated, deprecated, or wrong.
        ↓
[3] ANTIGRAVITY 2.0    → VALIDATES executability. Orchestration layer.
                          Checks: Can these steps actually run on this hardware?
                          Are paths correct? Will the network config work?
                          Simulates/dry-runs where possible. Flags real blockers.
        ↓
[4] CLAUDE (chat)      → RECONCILES feedback. Final plan author.
                          Integrates Perplexity + Antigravity corrections.
                          Produces final run-ready prompts.
```

**To Perplexity:** You are step [2]. Do not rewrite the architecture — verify the technical facts. Your output goes to Antigravity next, so flag anything it needs to know.

**To Antigravity:** You are step [3]. Perplexity has already checked technical accuracy. You check whether it RUNS on this specific hardware and network. Your output returns to Claude for final reconciliation.

---

## HARDWARE GROUND TRUTH

| Node | Spec | Role | State |
|------|------|------|-------|
| Engine Body | Ryzen 9 9900X, RTX 5080, 32→64GB RAM | Production / primary processor | Ollama + n8n + Claude Code LIVE |
| R&D Terminal | RTX 3060, 16GB RAM, 24/7 | Sentinel / overnight reasoning | NOT SET UP |

Vault: `C:\SFV_BLUEPRINT` (must be identical on both nodes via Syncthing)

---

## THE GOAL STATE

By end of tonight:
- Both terminals running Ollama + Claude Code
- Vault synced live between them (Syncthing)
- Engine Body: processes QUEUE tasks via n8n + Ollama
- R&D Terminal: runs overnight Claude Code loop, generates tasks, writes to shared QUEUE
- Watchdog running on Engine Body
- One full autonomous loop confirmed before sleep

---

# PHASE A — ENGINE BODY (already mostly done)

**Precondition:** the /goal prompt sent to Claude Code finished successfully.

## A1. Confirm optimization pass landed
Verify in this order:
- workflow1 has system prompt in Call Ollama node
- workflow1 has Phase 1 validation in Write + Log node
- workflow1 active in n8n (new ID)
- watchdog.ps1 exists at C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\
- OVERNIGHT_DIRECTIVE.md exists at C:\SFV_BLUEPRINT\99_INBOX\
- TEST_VALIDATION_001 landed in OUTPUTS tagged VALIDATED

## A2. Fix Workflow 4 (manual, UI required)
The API can't fix it — the trigger node is missing triggerOn.
1. Open http://127.0.0.1:5678
2. Open "Workflow 4 — Output Monitor"
3. Click the "Watch 99_INBOX" trigger node
4. Set triggerOn = folder
5. Set path = C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS
6. Set events = add
7. Save, then activate (toggle top-right)

## A3. Start the watchdog
Open a NEW dedicated PowerShell window (leave it open):
```powershell
cd C:\SFV_BLUEPRINT\03_INFRASTRUCTURE
.\watchdog.ps1
```
Confirm first line appears in WATCHDOG_LOG.md.

## A4. Install Syncthing on Engine Body
```powershell
winget install Syncthing.Syncthing
```
After install:
1. Launch Syncthing — opens http://127.0.0.1:8384
2. Add folder: C:\SFV_BLUEPRINT — Folder ID: sfv-vault
3. Leave it — we connect R&D Terminal to it in Phase B
4. Note the Engine Body Device ID (Actions → Show ID) — write it down

---

# PHASE B — R&D TERMINAL (full setup from zero)

Do these AT the R&D Terminal machine.

## B1. Install Node.js (required for Claude Code)
```powershell
winget install OpenJS.NodeJS.LTS
```
Close and reopen PowerShell after. Verify:
```powershell
node --version
npm --version
```
Need v18+. If older, update before continuing.

## B2. Install Ollama
```powershell
winget install Ollama.Ollama
```
Verify:
```powershell
ollama --version
```
Then pull the models. RTX 3060 has 12GB VRAM (NOT 16 — that's system RAM).
qwen3:14b may be tight. Pull a smaller primary for this node:
```powershell
ollama pull qwen3:8b
ollama pull qwen2.5-coder:7b
```
[CLAUDE FLAG — FOR PERPLEXITY: confirm qwen3:8b exists and is the right call for 12GB VRAM, vs running qwen3:14b quantized. R&D Terminal GPU is RTX 3060.]

## B3. Install Claude Code
```powershell
npm install -g @anthropic-ai/claude-code
claude --version
```
Authenticate when prompted (same account as Engine Body).

## B4. Install Syncthing + connect to Engine Body
```powershell
winget install Syncthing.Syncthing
```
1. Launch — http://127.0.0.1:8384
2. Add Remote Device → paste Engine Body Device ID from A4
3. Accept the shared folder sfv-vault when it appears
4. Set local path: C:\SFV_BLUEPRINT
5. Wait for initial sync — confirm files appear
6. On Engine Body Syncthing, accept the R&D Terminal device when it requests

## B5. Verify vault sync
On R&D Terminal:
```powershell
Get-ChildItem C:\SFV_BLUEPRINT\99_INBOX\QUEUE
```
Should show the same files as Engine Body. Drop a test file on Engine Body, confirm it appears on R&D Terminal within ~30s.

---

# PHASE C — WIRE THE OVERNIGHT LOOP

## C1. Decide the division of labor
- **Engine Body** = the PROCESSOR. n8n + Ollama consume QUEUE, write OUTPUTS. Stays on its current job.
- **R&D Terminal** = the GENERATOR. Claude Code reads OUTPUTS/HANDOFFS, reasons, writes NEW QUEUE tasks.

Because the vault is synced, R&D Terminal writes a task → Syncthing pushes to Engine Body → n8n trigger fires → Ollama processes → writes OUTPUT → Syncthing pushes back to R&D Terminal → Claude Code reads it next loop.

[CLAUDE FLAG — FOR ANTIGRAVITY: verify Syncthing propagation delay won't cause n8n localFileTrigger to fire on a half-synced file. May need a "settled" check — task file should include a written-complete marker or n8n should debounce. Confirm or propose fix.]

## C2. Launch the overnight loop on R&D Terminal
```powershell
cd C:\SFV_BLUEPRINT
claude --dangerously-skip-permissions
```
First message:
```
Read C:\SFV_BLUEPRINT\99_INBOX\OVERNIGHT_DIRECTIVE.md and execute it.
Do not ask questions. Begin the loop now. Run until stopped.
```

## C3. Confirm one full loop before sleep
Watch for:
1. R&D Terminal Claude Code writes a task to QUEUE/
2. File syncs to Engine Body (check Syncthing)
3. n8n fires, Ollama processes (check DECISION_LOG.md)
4. OUTPUT written, syncs back
5. R&D Terminal Claude Code reads it next loop

If all 5 happen once → the loop is real. Step away.

---

# OPEN QUESTIONS FOR THE CHAIN

These need Perplexity + Antigravity input before final lock:

1. **[PERPLEXITY]** qwen3:8b vs qwen3:14b-quantized on RTX 3060 12GB — which performs better for CLASSIFY/SUMMARIZE/CODE?
2. **[PERPLEXITY]** Is `winget install Ollama.Ollama` the current correct package ID, or has it changed?
3. **[PERPLEXITY]** Does Claude Code support `--dangerously-skip-permissions` in current version, or has the flag been renamed?
4. **[ANTIGRAVITY]** Syncthing + n8n localFileTrigger race condition — will partial-sync files trigger premature processing?
5. **[ANTIGRAVITY]** Should both nodes run Ollama, or should R&D Terminal call Engine Body's Ollama over the network to avoid double model loading?
6. **[ANTIGRAVITY]** Two Claude Code instances (one per node) — any auth/session conflict on the same account?

---

# FALLBACK IF SOMETHING BREAKS

- If Syncthing won't connect: fall back to single-node overnight on Engine Body only. The loop still works on one machine — R&D Terminal is an enhancement, not a requirement.
- If R&D Terminal Ollama can't load models: point R&D Terminal Claude Code at Engine Body's Ollama (http://[engine-body-ip]:11434) instead of local.
- If the loop stalls: watchdog logs it. Morning review shows where it died.

---

STATUS: DRAFT — awaiting Perplexity (step 2) then Antigravity (step 3) then Claude reconciliation (step 4)
AUTHORED BY: Claude (step 1)
DATE: 2026-06-03

## CONNECTED FILES
- [[OLLAMA_SETUP|Ollama Setup]]
- [[VAULT_DASHBOARD_DRAFT|Vault Dashboard Draft]]
- [[HARDWARE_CONTEXT|Hardware Context]]
- [[CURRENT_DIRECTIVE|Current Directive]]
- [[CLAUDE_CODE_PROMPTS|Claude Code Prompts]]
- [[INFRASTRUCTURE|Infrastructure]]
- [[DASHBOARD|Dashboard]]
