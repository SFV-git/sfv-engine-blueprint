---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE — AI_STACK_ARCHITECTURE_BLUEPRINT §4 references this file
---

# JOB ENVELOPE SPEC — CANONICAL SCHEMA

> Single source of truth for the n8n job envelope JSON format.
> All docs that reference the job envelope schema should link here, not re-define it.

---

## REQUIRED FIELDS

All job envelope files must include these fields:

```json
{
  "task_id":      "YYYYMMDD-###",
  "task_type":    "CLASSIFY | SUMMARIZE | COMPRESS | RESEARCH | BLUEPRINT | CODE | MEDIA | VISION | GEMINI",
  "topic":        "Short human-readable description of the task",
  "prompt":       "Full prompt text sent to the model",
  "priority":     "NORMAL | HIGH | CRITICAL",
  "status":       "PENDING",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/[task_id]_RESULT.md"
}
```

**Rules:**
- `status` must be `"PENDING"` on creation — workflow1 skips non-PENDING files
- `task_id` must be unique — use `YYYYMMDD-NNN` format with sequential number
- File must be valid JSON — malformed files are silently dropped by workflow1
- File extension must be `.json` — the Local File Trigger only fires on `.json` files
- File must land in `C:\SFV_BLUEPRINT\99_INBOX\QUEUE\` to be processed

---

## OPTIONAL FIELDS

Include only when relevant to the task_type:

```json
{
  "client_facing":  false,
  "auto_research":  false,
  "source":         "",
  "file_path":      "",
  "output_format":  "md"
}
```

### `client_facing` (boolean — default: false)
Set `true` to force escalation to Claude regardless of Ollama confidence.
Use for: deliverables that go directly to clients (captions, briefs, final copy).
See: CONFIDENCE_LOGIC.md for full escalation rules.

### `auto_research` (boolean — default: false)
RESEARCH tasks only. Set `true` to attempt Tavily automated web search before Claude escalation.
Set `false` (or omit) to send directly to Claude HANDOFF.
See: RESEARCH_ROUTE_SPEC.md and workflow3 spec.

### `source` (string)
RESEARCH tasks only. Identifies where the research request originated.
Values: `"PERPLEXITY_MANUAL"` | `"WILL_DIRECT"` | `"ANTIGRAVITY"` | `"N8N_INTERNAL"`

### `file_path` (string — absolute path)
MEDIA and VISION tasks. Absolute path to the source file to process.
Example: `"C:/SFV_ACTIVE/SFV_STUDIO/RAW/2026-05-28_morning_walk.mp4"`
Required for MEDIA tasks. Optional for VISION (prompt may contain image data instead).

### `output_format` (string — default: "md")
MEDIA tasks only. Format for the transcript output.
Values: `"md"` (default markdown) | `"json"` (structured with timestamps) | `"txt"` (plain text)

---

## STATUS VALUES (unified — confirmed 2026-05-29)

| Status | Set by | Meaning |
|---|---|---|
| `PENDING` | Task creator | In queue, not picked up yet |
| `IN_PROGRESS` | workflow1 on pickup | Currently being processed — prevents duplicate runs |
| `COMPLETE` | workflow1 Write+Log | Processed successfully, output in OUTPUTS/ |
| `ESCALATED` | workflow1 Write+Log | Sent to HANDOFFS/ — requires Claude or Antigravity |
| `DEFERRED` | Will or agent | Intentionally postponed — do not process |
| `BLOCKED` | Will or agent | Cannot proceed — question logged in QUESTIONS_FOR_WILL.md |
| `DRAFT` | Any agent | Output written, not yet reviewed by Will |

---

## FULL EXAMPLE — CLASSIFY TASK

```json
{
  "task_id": "20260529-001",
  "task_type": "CLASSIFY",
  "topic": "Branch classification for morning walk assets",
  "prompt": "Classify which SFV branch this file belongs to based on the filename and description. Output: branch name, confidence level, one-sentence reason.\n\nFilename: IMG_8432_morning_walk_model_studio.jpg\nContext: Portrait shoot, indoor studio setting, professional model.",
  "priority": "NORMAL",
  "status": "PENDING",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260529-001_RESULT.md"
}
```

## FULL EXAMPLE — MEDIA TASK

```json
{
  "task_id": "20260529-002",
  "task_type": "MEDIA",
  "topic": "Transcribe UGC client briefing video",
  "prompt": "Transcribe this video. Output timestamped transcript. Flag any section where the speaker mentions deliverables or deadlines.",
  "priority": "HIGH",
  "status": "PENDING",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260529-002_TRANSCRIPT.md",
  "file_path": "D:/SFV_ACTIVE/SFV_UGC/BRIEFS/client_briefing_2026-05-29.mp4",
  "output_format": "md"
}
```

## FULL EXAMPLE — RESEARCH TASK (auto)

```json
{
  "task_id": "20260529-003",
  "task_type": "RESEARCH",
  "topic": "Current Instagram Reels algorithm best practices",
  "prompt": "What are the current best practices for Instagram Reels algorithm optimization as of 2026? Focus on: hook timing, caption strategy, hashtag use, posting frequency.",
  "priority": "NORMAL",
  "status": "PENDING",
  "output_target": "C:/SFV_BLUEPRINT/99_INBOX/OUTPUTS/20260529-003_RESEARCH.md",
  "auto_research": true,
  "source": "WILL_DIRECT"
}
```

---

## WHERE THIS SCHEMA IS USED

| File | Usage |
|---|---|
| `03_INFRASTRUCTURE/AI_STACK_ARCHITECTURE_BLUEPRINT.md` §4 | References this file for base schema |
| `05_AI_LAYER/ANTIGRAVITY_N8N_TRIGGER.md` | Antigravity file-drop format |
| `05_AI_LAYER/RESEARCH_ROUTE_SPEC.md` | RESEARCH task extensions |
| `04_WORKFLOWS/MEDIA_PIPELINE.md` | MEDIA task extensions |
| `03_INFRASTRUCTURE/n8n_workflows/workflow1_queue_processor.json` | Reads and validates this schema |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT|AI Stack Architecture §4]]
- [[ANTIGRAVITY_N8N_TRIGGER|Antigravity → n8n Trigger]]
- [[RESEARCH_ROUTE_SPEC|Research Route Spec]]
- [[MEDIA_PIPELINE|Media Pipeline]]
- [[CONFIDENCE_LOGIC|Confidence Logic]]
- [[ENGINE_COMMUNICATION_MODEL|Engine Communication Model]]
