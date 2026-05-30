---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: LOCAL_MODELS.md when CANON
---

# MODEL LIFECYCLE POLICY

Policy for locking, evaluating, swapping, and recovering Ollama models on the SFV Engine stack.

---

## 1. VERSION LOCKFILE

A single file tracks the exact model versions in production:

**Location:** `C:\SFV_BLUEPRINT\05_AI_LAYER\OLLAMA_PROMPTS\MODEL_LOCK.md`

### Current locked models

| Model | Route | Locked since |
|---|---|---|
| qwen3:14b | CLASSIFY / SUMMARIZE | 2026-05-27 |
| qwen2.5-coder:7b | CODE | 2026-05-29 |
| minicpm-v:8b | VISION | 2026-05-29 |
| nomic-embed-text | EMBED (FUTURE) | not yet locked |

**Rule:** Never swap a model in production without updating MODEL_LOCK.md first and obtaining Will's explicit approval. No unilateral swaps under any circumstances.

---

## 2. EVALUATION CRITERIA FOR MODEL SWAPS

All five criteria must pass before a model is promoted to production.

### 2a. HIGH_CONF rate
- New model must match or exceed the current model's HIGH_CONF rate on the same canonical test tasks
- Measure via DECISION_LOG — count HIGH_CONF responses / total responses over a comparable task set
- Threshold: do not swap if new model's HIGH_CONF rate is lower than current model's rate

### 2b. Inference speed
- New model must not be more than 20% slower on average task latency
- Measure via timestamp deltas in DECISION_LOG (task submitted → response returned)
- Test on the same hardware (Engine Body, RTX 5080) under same load conditions

### 2c. VRAM footprint
- Confirm new model fits within Engine Body VRAM budget (see Section 6)
- Do not load the new model simultaneously with all other active models without verifying it fits
- If new model exceeds VRAM budget, evaluate whether a route can be unloaded during operation

### 2d. Context quality — canonical task suite
Run all five task types with equivalent inputs and compare outputs side-by-side:
1. CLASSIFY — photo or video file classification task
2. SUMMARIZE — session notes or metadata summarization
3. CODE — script generation or debugging task
4. VISION — image description or metadata extraction
5. HANDOFF — handoff document generation

Record outputs in `00_DEV_LOG/MODEL_EVAL_[date].md` for Will's review.

### 2e. All criteria must pass
A model that passes four of five criteria does not qualify. All five must pass before Will approves the swap.

---

## 3. SWAP PROCEDURE

Execute in this order, no steps skipped.

1. **Will approves the swap** — document approval in `00_DEV_LOG/DECISIONS.md` (CANON CONTROL applies)
2. **Pull new model** on Engine Body: `ollama pull [new-model-name]`
3. **Run canonical task suite** against new model using workflow1 task files
4. **Record eval results** in `00_DEV_LOG/MODEL_EVAL_[date].md`
5. **Will reviews eval results** and gives final go/no-go
6. **If passing:** update workflow1 routing node to reference new model name
7. **Update MODEL_LOCK.md** — add new model, mark old model as superseded with date
8. **Retention window:** keep old model on disk for 2 weeks before removing — rollback window
9. **Commit vault** with message: `feat: swap [old-model] → [new-model] on [route] route`

If any step fails, stop and report to Will. Do not proceed to the next step.

---

## 4. qwen3:14b ROADMAP

### Trigger conditions for evaluation
- Quarterly review cycle: evaluate qwen3:14b replacement at most once per quarter
- Do not chase every new Ollama release
- Early evaluation trigger: if HIGH_CONF rate on routine tasks falls below 85% as measured in DECISION_LOG, evaluate sooner

### Target upgrade path
- When qwen4 or equivalent becomes available on Ollama with comparable VRAM footprint (~9–10 GB) and demonstrably higher output quality: run full eval per Section 2
- Priority: quality on CLASSIFY and SUMMARIZE routes — these are the highest-volume routes
- [FOR HUMAN REVIEW]: Should quarterly reviews be documented in a recurring DEV_LOG entry, or is an informal check sufficient?

---

## 5. SPECIALIST MODEL SWAP CRITERIA

### qwen2.5-coder:7b (CODE route)
- Swap candidate: any model marketed as a code specialist, fits within ~5 GB VRAM, available on Ollama
- Swap trigger: if CODE route produces repeated low-confidence or incorrect outputs on SFV task patterns
- D:\ space must allow for parallel install during evaluation window

### minicpm-v:8b (VISION route)
- Swap candidate: any vision-language model on Ollama with stronger image-to-text quality at comparable VRAM
- Swap trigger: if VISION route produces structurally incorrect metadata descriptions or repeated LOW_CONF responses
- [INFERENCE]: minicpm-v:8b is currently the best-available compact vision model on Ollama — verify before assuming an upgrade exists

### nomic-embed-text (EMBED route — FUTURE)
- Swap only if embedding quality degrades for SFV vault content (e.g., semantic search returns wrong results)
- This model is not yet active — lock date will be set when the vector layer is enabled
- Low VRAM footprint means it does not compete with inference models

---

## 6. VRAM BUDGET TABLE — ENGINE BODY (RTX 5080)

[INFERENCE — verify actual VRAM allocations at runtime before treating these as authoritative. Use `nvidia-smi` during live inference to confirm.]

| Model | Estimated VRAM | Loaded when |
|---|---|---|
| qwen3:14b | ~9–10 GB | CLASSIFY / SUMMARIZE tasks |
| qwen2.5-coder:7b | ~5 GB | CODE tasks |
| minicpm-v:8b | ~6 GB | VISION tasks |
| nomic-embed-text | ~0.3 GB | Embedding runs (FUTURE) |

**RTX 5080 total VRAM: 16 GB**

**Rule:** Do not load more than two large models simultaneously. Models are loaded on-demand by Ollama and unloaded after keep-alive timeout — this is not a static allocation. However, concurrent requests from workflow1 could cause two models to be resident at once.

[FOR HUMAN REVIEW]: Should workflow1 enforce single-model-at-a-time loading via a queue, or is the current keep-alive/timeout approach sufficient given the RTX 5080's 16 GB headroom?

---

## 7. ROLLBACK PROCEDURE

If a newly swapped model fails in production:

1. Identify the old model name from MODEL_LOCK.md (it remains on disk for 2 weeks)
2. Update workflow1 routing node to reference old model name
3. Update MODEL_LOCK.md — restore old model as active, mark new model as REJECTED
4. Record the failure in `00_DEV_LOG/MODEL_EVAL_[date].md` with root cause
5. Commit vault

After 2 weeks without rollback need, the old model may be removed: `ollama rm [old-model]`

---

## CONNECTED FILES
- [[LOCAL_MODELS]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT]]
- [[CONFIDENCE_LOGIC]]
- [[PROMPT_VERSIONING]]
- [[MODEL_ROUTING]]
