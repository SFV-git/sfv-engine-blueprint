---
STATUS: FOR HUMAN REVIEW
SOURCE: Perplexity (manual, pasted by Will 2026-07-01)
TASK_ID: 20260701-001
VERIFIED_BY: Claude Chat -- spot-checked Devstral Small 2 claims only, rest UNCONFIRMED
---

# CLAUDE CODE EXECUTOR ALTERNATIVE -- RESEARCH RESULT

## VERIFICATION NOTE (added by Claude, not part of Perplexity output)
Web-search spot-check confirms the core claim: **Devstral Small 2 (24B, Apache 2.0) is real**,
released by Mistral (Devstral 2 family, Dec 2025), **68.0% SWE-bench Verified is the correct
figure** per Mistral's own announcement and independently corroborated by Ollama/HuggingFace/
DigitalOcean/Cline coverage. Fits single consumer GPU (Mistral says RTX 4090/32GB Mac class;
DigitalOcean puts the 24B at ~25GB unquantized RAM/VRAM -- Perplexity's ~14-15GB Q4_K_M figure
for the RTX 5080 is a quantized estimate, NOT independently verified by me, but is directionally
consistent with a 24B model at Q4). Devstral 2 (123B) needs data-center GPUs -- correctly ruled
out for this hardware.

**NOT independently verified this session (flag before acting on):**
- Terminal-Bench 2.0 22.5% figure
- "~46.8% via OpenHands harness" -- the harness-adjusted score. This number has no source link
  in the Perplexity output and reads like an extrapolation, not a cited benchmark. Treat as
  UNCONFIRMED / possible fabrication until sourced.
- DeepSeek-Coder-V2-Lite specs/VRAM for the R&D Terminal 3060
- OpenHands headless/`--json` flag behavior and the exact CLI syntax shown
- DeepSeek V4 Flash pricing ($0.14/$0.28 per MTok) and its SWE-bench score -- DeepSeek V4 is a
  newer release than what's in my training; plausible given DeepSeek's pricing history, not
  independently confirmed
- Qwen3-Coder 14B / Qwen3.6-35B-A3B specs
- All "Ollama pull" command names (`devstral-small-2`, `deepseek-coder-v2:lite`) -- confirm the
  exact tag exists before scripting against it; Ollama library naming isn't always 1:1 with
  Perplexity's shorthand

## RAW PERPLEXITY OUTPUT

Bottom line first: **Devstral Small 2 + OpenHands headless** is the stack that most faithfully
replicates Claude Code's agentic loop at zero per-token cost on your 5080.

### Best Model for 16GB VRAM (RTX 5080)
**Primary Pick: Devstral Small 2 (24B)** -- 24B dense, SWE-bench Verified 68.0%, Terminal-Bench 2.0
22.5% [UNCONFIRMED], 256K context, ~14-15GB VRAM at Q4_K_M, `ollama pull devstral-small-2`,
Apache 2.0, ~35-45 tok/s on RTX 5080 [UNCONFIRMED].
Fine-tuned specifically for agentic harnesses (OpenHands is the reference framework).

**Alternate: Qwen3-Coder 14B** -- ~9.5GB at Q4_K_M, ~89% HumanEval [UNCONFIRMED], no agentic
fine-tuning, good as an Ollama-tier fast path for mechanical rewrites.

**Doesn't fit:** Devstral 2 (123B, needs multi-GPU/H100), Qwen3-Coder 32B Q4_K_M (~20.5GB,
overflows 16GB), Qwen3-Coder-Next 80B MoE (~48GB combined, 3-8 tok/s with CPU offload -- painful),
Codestral 22B (fits at ~14.1GB but is FIM/autocomplete, not agentic).

### Best Model for 12GB VRAM (RTX 3060 / R&D Terminal)
**Pick: DeepSeek-Coder-V2-Lite (16B MoE, 2.4B active)** -- ~81-90% HumanEval [UNCONFIRMED], 128K
context, ~8.9GB at Q4_K_M, `ollama pull deepseek-coder-v2:lite`, ~20-30 tok/s on RTX 3060.
Fallback: Qwen3-Coder 14B Q4_K_M (9.5GB, cleaner tool-call formatting).

### Harness Comparison
| Harness | Headless | Local Ollama | Multi-file | Git | JSONL | Notes |
|---|---|---|---|---|---|---|
| OpenHands | Yes (`--headless`) | Yes | Yes, full R/W+shell | Yes | Yes | Best Claude Code analog |
| Aider | Yes (`--yes --message`) | Yes | Yes, git diff | Yes, auto-commit | No | One-shot per invocation |
| Open Codex CLI | Yes (`--approval-mode full-auto`) | Yes | Yes | Yes | Yes | Fork of OpenAI Codex CLI |
| SWE-agent | Yes, Docker batch | Yes | Yes | Yes | Yes | Overkill for production |
| Cline (Continue) | No -- VS Code ext only | Yes | Yes | Yes | No | Not scriptable headless |

**Winner: OpenHands** -- only harness running a full read-write-shell-observe-iterate loop in
one headless call. `--json` streams events parseable from n8n.

### Cheap API Fallbacks [ALL PRICING/SCORES UNCONFIRMED THIS SESSION]
| Provider | In $/MTok | Out $/MTok | Context | SWE-bench |
|---|---|---|---|---|
| DeepSeek V4 Flash | $0.14 | $0.28 | 1M | ~78% |
| DeepSeek V4 Pro | $0.435 | $0.87 | 1M | ~78-80% |
| Qwen3-Coder-Next API | ~$0.15 | ~$0.60 | 262K | 70.6% |
| Qwen3 235B-A22B | ~$0.09 | ~$0.10 | 262K | -- |
| GLM-5-Code | $1.20 | $5.00 | 200K | 62.8% -- not recommended |

Recommended fallback: DeepSeek V4 Flash.

### Recommended Stack (Perplexity's proposal)
```
Tier 0 (free): Ollama local -- Qwen3-Coder 14B Q4_K_M -- mechanical generation, stubs, doc rewrites
Tier 1 (free): OpenHands --headless + Devstral Small 2 via Ollama -- multi-file agentic sessions
Tier 2 (cheap API ~$0.14/MTok): DeepSeek V4 Flash -- fallback when local VRAM/context saturated
Tier 3 (last resort, retired): Claude Code -- only tasks that fail all three above
```

### Capability Gaps vs Claude Code
| Dimension | Claude Code | Devstral Small 2 + OpenHands | Gap |
|---|---|---|---|
| SWE-bench Verified | ~79.6% (Sonnet 4.6) | 68.0% model-only, ~46.8% via harness [UNCONFIRMED] | Real |
| Multi-file coherence | Excellent | Good, degrades past 32K at Q4 | Moderate |
| Tool call reliability | Very high | High (tuned for it) | Slight |
| Iterative shell loops | Native | Matches via `--headless` | Minimal |
| Context window | 200K | 256K | None |
| Speed | Cloud-limited | 35-45 tok/s local | Local often faster |
| Subtle bug detection | Strong | Weaker on logic errors | Notable |
| Novel architecture reasoning | Strong | Weaker | Notable |

### Integration Pattern
n8n Execute Command node (self-hosted only, re-enable in n8n 2.0+):
```json
{"command": "openhands --headless --json -t \"{{ $json.task_description }}\" 2>&1"}
```
Python subprocess pattern for the SFV orchestrator:
```python
import subprocess, json, os
def run_coding_agent(task: str, cwd: str) -> dict:
    env = {**os.environ, "LLM_MODEL": "ollama/devstral-small-2", "LLM_BASE_URL": "http://localhost:11434"}
    result = subprocess.run(["openhands", "--headless", "--json", "-t", task],
        cwd=cwd, capture_output=True, text=True, env=env)
    events = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    return {"events": events, "exit_code": result.returncode}
```
OpenHands config (`~/.openhands/config.toml` or env):
```toml
[llm]
model = "ollama/devstral-small-2"
base_url = "http://localhost:11434"
```

## CONNECTED FILES
- [[LOCAL_MODELS|Local Models]]
- [[MODEL_LIFECYCLE_POLICY|Model Lifecycle Policy]]
- [[TOOL_STACK|Tool Stack]]
- [[CRITICAL_PATH|Critical Path]]
