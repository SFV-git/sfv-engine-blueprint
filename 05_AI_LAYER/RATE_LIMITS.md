---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-25
---

# RATE LIMITS AND USAGE STRATEGY

> INFERENCE: Specific limit numbers sourced from training data — FOR HUMAN REVIEW.
> Limits change. Check each platform's current docs if hitting walls.
> Strategy below is accurate regardless of exact numbers.

---

## LIMITS PER TOOL

### Ollama (local — R&D Terminal)
| Limit | Value |
|-------|-------|
| Rate limit | NONE |
| Daily cap | NONE |
| Cost | $0 forever |
| Context window | ~8K (qwen3) |

**The constraint:** Context window, not rate limits. Tasks must be self-contained.
**Strategy:** Route everything possible here. It never runs out.

---

### Claude Chat (claude.ai — Pro plan)
| Limit | Value |
|-------|-------|
| Sonnet messages | ~45–50 per 5-hour window (INFERENCE) |
| Opus messages | Lower — ~20–30 per 5-hour window (INFERENCE) |
| Reset | Rolling 5-hour window |
| Cost | Subscription (fixed) |

**The constraint:** Message count, not tokens.
**Strategy:**
- One message = maximum value. Never send half a question.
- Batch all related questions into one prompt.
- Use COMPRESSED_CONTEXT.md — never paste full vault.
- Let Ollama draft → paste result into one Claude message for polish.
- Never use Opus unless Will explicitly requests it.

---

### Claude Code (Code tab — API)
| Limit | Value |
|-------|-------|
| Rate limit | Depends on API tier (INFERENCE: Tier 1 = 50 RPM) |
| Token limit | Depends on tier (INFERENCE: 40K–80K TPM) |
| Cost | Per token — Sonnet ~$3/MTok in, ~$15/MTok out |
| Hard cap | Set spend cap in Anthropic console |

**The constraint:** Cost and tokens per minute.
**Strategy:**
- `/compact` when context gets long mid-session
- `/clear` between unrelated modules — never carry dead context
- One module per Code session
- Pass file paths not file contents when possible
- Commit after each module → fresh session

---

### Google AI Studio (free tier)
| Limit | Value |
|-------|-------|
| Gemini 2.5 Pro RPD | ~25 requests/day (INFERENCE — FOR HUMAN REVIEW) |
| Gemini 2.5 Flash RPD | ~1500 requests/day (INFERENCE) |
| RPM (requests/min) | 2–15 depending on model (INFERENCE) |
| Context window | 1,000,000 tokens |
| Cost | $0 on free tier |

**The constraint:** Daily request cap on Pro model is low.
**Strategy:**
- Reserve Gemini 2.5 Pro for massive-context tasks only (full shoot logs, large doc synthesis)
- Use Flash for anything smaller and more frequent
- Never waste a Pro request on something Ollama can handle
- Batch content before sending — one big request beats five small ones

---

### NotebookLM (free tier)
| Limit | Value |
|-------|-------|
| Notebooks | ~100 (INFERENCE) |
| Queries/day | ~50 per notebook (INFERENCE — FOR HUMAN REVIEW) |
| Sources per notebook | 50 max |
| Cost | $0 on free tier |

**The constraint:** Query volume and sources per notebook.
**Strategy:**
- One notebook per SFV domain (references, competitors, case studies, tools)
- Use for research synthesis only — not repeatable tasks
- Let it index 10_REFERENCES/ content once, query many times

---

### Antigravity (local)
| Limit | Value |
|-------|-------|
| Rate limit | NONE — local executor |
| Cost | $0 |

**The constraint:** Approval gate (by design — every action needs Will's OK).
**Strategy:** Use for git audits, file inspection, vault file creation. Not for rapid iteration.

---

## PRIORITY ROUTING ORDER

```
Task comes in
    ↓
Can Ollama handle it? (bulk, repeatable, low-stakes)
    YES → TASK_QUEUE.md → Ollama → free, unlimited
    ↓ NO
Does it need file system access or code execution?
    YES → Claude Code → one module, /compact aggressively
    ↓ NO
Does it need massive context (>50K tokens of material)?
    YES → Google AI Studio Gemini 2.5 Pro → batch first, one request
    ↓ NO
Is it a planning/blueprint decision?
    YES → Claude Chat Sonnet → batch all questions, max value per message
    ↓ NO
Is it desktop file routing?
    YES → Claude Cowork
    ↓ NO
Is it a local vault operation with an approval gate?
    YES → Antigravity
```

---

## DAILY BUDGET EXAMPLE (sustainable rhythm)

| Tool | Daily use target | Buffer |
|------|-----------------|--------|
| Ollama | Unlimited — use freely | — |
| Claude Chat | 15–20 messages max | Leaves headroom for burst sessions |
| Claude Code | 3–5 sessions | One module each |
| Google AI Studio Pro | 1–2 requests | Reserve for big context only |
| Google AI Studio Flash | 20–30 requests | Lightweight tasks |
| NotebookLM | 10–15 queries | Research sessions only |

---

## WHEN YOU HIT A LIMIT

| Tool | Limit hit | Fix |
|------|-----------|-----|
| Claude Chat | Message limit | Switch to Ollama for drafts, come back next window |
| Claude Code | Token limit mid-session | Run /compact immediately |
| Claude Code | Spend cap hit | Review what ran, raise cap if justified |
| Google AI Studio Pro | Daily cap | Use Flash, or wait for reset (midnight PT) |
| Ollama | UNSURE result | Task needs file content injected — see TASK_QUEUE_GUIDE.md |

---

## OLLAMA UNSURE FIX — TASK FORMAT

Ollama cannot read vault files on its own. If a task references a file,
paste the file content into the task directly.

WRONG:
```
REVIEW: Read 04_WORKFLOWS/INGEST.md. Find missing steps.
```

RIGHT:
```
REVIEW: Find missing steps or failure points in this workflow.
Output numbered list only.

CONTENT:
[paste INGEST.md content here]
```

OR: Use the improved daemon (daemon v3) which auto-reads referenced files.
See: 99_INBOX/ollama_daemon.py — upgrade pending.
