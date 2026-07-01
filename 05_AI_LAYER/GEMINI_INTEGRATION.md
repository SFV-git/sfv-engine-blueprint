---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE — or merge into AI_STACK_ARCHITECTURE_BLUEPRINT §3 when CANON
---

# GEMINI INTEGRATION SPEC

> Gemini Flash as Tier 4-cheap for bulk reformat/caption at scale.
> Currently only accessible via Antigravity. This doc specs the n8n→Gemini direct path.

---

## CURRENT STATE

Gemini Flash is used by Antigravity (free during preview). There is no direct n8n → Gemini API path. All Gemini-tier tasks currently require Antigravity as the intermediary.

**Gap:** For automated bulk tasks (caption generation at scale, bulk reformatting) that run via the n8n queue, Antigravity cannot be in the loop — it requires human session context. n8n needs to call Gemini Flash directly.

---

## WHEN TO USE GEMINI FLASH (not Ollama)

Route to Gemini Flash when:
- Task requires quality above Ollama but cost below Claude Sonnet
- Bulk volume: 20+ captions or reformats in a single batch
- Task requires internet context or current knowledge (Ollama has none)
- Antigravity is not in session and the task is non-blocking

Stay on Ollama when:
- Task is simple classification or summarization (Ollama handles it fine)
- Task is urgent and Gemini rate limits are a risk
- Task contains sensitive data (keep local)

---

## GEMINI FLASH API — n8n INTEGRATION SPEC

**API endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent`

**Auth:** API key via query param `?key=[GEMINI_API_KEY]`

**n8n HTTP Request node config:**
```
Method: POST
URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={{ $env.GEMINI_API_KEY }}
Headers: Content-Type: application/json
Body:
{
  "contents": [
    {
      "parts": [{ "text": "{{ $json.prompt }}" }]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 1024,
    "temperature": 0.7
  }
}
```

**Response extraction:**
```
{{ $json.candidates[0].content.parts[0].text }}
```

---

## ENV VAR REQUIRED

Add to `n8n_env.ps1`:
```powershell
$env:GEMINI_API_KEY = "[key from Google AI Studio]"
```

Add placeholder to `n8n_env.template.ps1`.
Add key to SECRETS_POLICY.md credential table.

**[FOR HUMAN REVIEW]:** Gemini API key not yet set. Get from aistudio.google.com → API Keys → Create API Key. Free tier is sufficient for Phase 1 volumes.

---

## JOB ENVELOPE EXTENSION

To route a task to Gemini Flash, add `task_type: "GEMINI"` or add a `tier` field:

Option A — new task_type:
```json
{ "task_type": "GEMINI", ... }
```

Option B — tier field on existing task_types:
```json
{ "task_type": "SUMMARIZE", "tier": "cloud_cheap", ... }
```

**Recommendation: Option A.** Keeps workflow1 routing clean. Add `GEMINI` as a named route alongside OLLAMA and RESEARCH.

workflow1 "Read Task" node routing addition:
```
if task_type === 'GEMINI' → route = 'GEMINI'
```

New branch in workflow1 Switch/IF node → Gemini HTTP Request node → Write+Log node.

---

## RATE LIMITS AND FALLBACK

See `05_AI_LAYER/RATE_LIMITS.md` for current Gemini Flash rate limit values.
Key constraint for SFV stack: if Gemini Flash returns HTTP 429, fall back to Ollama and log `GEMINI_FALLBACK` to DECISION_LOG.md.

---

## USE CASES IN SFV STACK

| Task | Volume | Why Gemini over Ollama |
|---|---|---|
| Caption generation at scale | 20–100/batch | Quality + style consistency |
| Bulk alt-text for media | 50+ files | Speed + accuracy |
| Reformat/restructure docs | 10+ files | Reliable instruction following |
| Branch strategy synthesis | 1–3/session | Internet context useful |

---

## ANTIGRAVITY GEMINI PATH (existing — no change needed)

Antigravity continues to use Gemini Flash directly via its own model selection. The n8n path is additive — it enables automated tasks to access Gemini without Antigravity being in session.

---

## CONNECTED FILES
- [[INTEGRATIONS|Integrations]]
- [[SECRETS_POLICY|Secrets Policy]]
- [[MODEL_ROUTING|Model Routing]]
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture Blueprint]]
- [[ANTIGRAVITY|Antigravity]]
- [[RATE_LIMITS|Rate Limits]]
