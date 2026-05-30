---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# MEDIA PIPELINE — WHISPER TRANSCRIPTION BRANCH

> Specifies how MEDIA tasks are routed, serialized, processed by Whisper on Node B, and output
> as transcripts. Covers the current Execute Command path, FFmpeg pre-processing, and the
> faster-whisper migration path.

---

## OVERVIEW

Branch D of the n8n routing tree handles all MEDIA tasks. The branch exists in the current
workflow1_queue_processor as an Execute Command node that calls a Whisper HTTP endpoint on Node B.

No concrete serial queue rules, port spec, or migration path existed before this document.
This spec fills those gaps.

---

## SECTION 1 — WHAT TRIGGERS A MEDIA TASK

### Entry Points

1. **File drop to QUEUE folder** — Will drops a video file (or a job envelope JSON referencing
   a video file) into `C:\SFV_BLUEPRINT\99_INBOX\QUEUE\`. The n8n Local File Trigger detects the
   new file and reads the envelope.

2. **n8n webhook** — An upstream workflow or Antigravity POSTs a job envelope directly to the
   n8n webhook endpoint on Node A (port 5678). The envelope's `task_type` field is set to `MEDIA`.

3. **Programmatic queue drop** — A Python script or another n8n workflow writes a job envelope
   JSON to the QUEUE folder. Same detection path as #1.

### Supported File Types

The following source video containers are in scope for the Whisper transcription pipeline:

| Extension | Notes |
|-----------|-------|
| `.mp4` | Primary ingest format |
| `.mov` | SFV Studio / camera native |
| `.mxf` | [INFERENCE] — confirm whether MXF ingest is in scope |
| `.mkv` | [INFERENCE] — confirm whether MKV is required |

Audio-only files (`.mp3`, `.wav`, `.m4a`) are also valid inputs — FFmpeg pre-processing is skipped
when the source is already audio.

[FOR HUMAN REVIEW]: Confirm which file types are in scope for transcription. The list above is
based on typical SFV production formats.

---

## SECTION 2 — JOB ENVELOPE FOR MEDIA TASKS

The standard job envelope (from AI_STACK_ARCHITECTURE_BLUEPRINT) is extended with two required
fields for MEDIA tasks:

```json
{
  "task_id": "YYYYMMDD-###",
  "task_type": "MEDIA",
  "topic": "string — short description of the video content",
  "prompt": "string — optional context hint for Whisper (e.g. speaker names, domain vocabulary)",
  "priority": "NORMAL | HIGH | CRITICAL",
  "status": "PENDING",
  "output_target": "C:\\SFV_BLUEPRINT\\99_INBOX\\OUTPUTS\\YYYYMMDD-###_transcript.md",
  "file_path": "D:\\SFV_ACTIVE\\[branch]\\[filename].mp4",
  "output_format": "md"
}
```

### Extended Fields

| Field | Required | Description |
|-------|----------|-------------|
| `file_path` | YES | Absolute path to the source video or audio file on Node A |
| `output_format` | YES | Format for the output transcript. Default: `md`. Options: `md`, `json`, `txt` |

See JOB_ENVELOPE_SPEC.md for the canonical schema. MEDIA tasks use optional fields: `file_path`, `output_format`.

[FOR HUMAN REVIEW]: Confirm whether `output_format` should default to `md` or whether `json`
(with timestamps) is preferred for downstream processing.

---

## SECTION 3 — SERIAL QUEUE RULES

### Why Serial Only

The RTX 3060 on Node B (R&D Terminal) has 12GB VRAM. Running two Whisper jobs concurrently
will exhaust VRAM and trigger an OOM crash, killing both jobs and potentially crashing the
Whisper service. This is documented as a confirmed gap in AI_STACK_ARCHITECTURE_BLUEPRINT §6.

**Rule: Only one Whisper job may run at a time on Node B.**

### How Serialization Is Enforced

The n8n workflow enforces this via a status gate before dispatching to Node B:

```
Job arrives at Branch D (MEDIA)
  ↓
Check DECISION_LOG.md for any entry with status IN_PROGRESS and task_type MEDIA
  → If found: set status to DEFERRED, write back to QUEUE, exit branch
  → If not found: proceed to dispatch
  ↓
Write IN_PROGRESS entry to DECISION_LOG.md (lock record)
  ↓
Dispatch to Whisper (see Section 5)
  ↓
On COMPLETE or FAILED: clear IN_PROGRESS lock in DECISION_LOG.md
```

[INFERENCE]: The lock mechanism above uses DECISION_LOG.md as a simple mutex. A more robust
approach (Redis lock or n8n's own execution queue mode) is available after the Redis deployment
in Phase 2. This serial-by-file-check approach is the Phase 1 spec.

[FOR HUMAN REVIEW]: Confirm whether DEFERRED tasks should re-queue automatically (n8n retry
on schedule) or require Will to manually resubmit. Recommend: auto-retry after 5 minutes.

---

## SECTION 4 — FFMPEG PRE-PROCESSING

### Role

FFmpeg runs on Node A via an n8n Execute Command node before the job is sent to Node B.
Its job is to extract the audio track from the source video and convert it to a Whisper-compatible
format (16 kHz mono WAV).

### Why FFmpeg Is Needed

Whisper's native support for video containers is inconsistent. Pre-extracting audio:
- Reduces the payload size sent to Node B
- Eliminates format compatibility errors in Whisper
- Speeds up Node B processing (no demux overhead on RTX 3060)

### FFmpeg Command Spec

```bash
ffmpeg -i "[file_path]" -ar 16000 -ac 1 -c:a pcm_s16le "C:\SFV_BLUEPRINT\99_INBOX\QUEUE\[task_id]_audio.wav"
```

Parameters:
- `-ar 16000` — resample to 16 kHz (Whisper optimal)
- `-ac 1` — downmix to mono
- `-c:a pcm_s16le` — uncompressed WAV (fast decode in Whisper)

Output audio file lands in the QUEUE folder and is referenced in the dispatch payload to Node B.

[INFERENCE]: FFmpeg is assumed to be installed on Node A at a system PATH location.
Confirm `ffmpeg --version` before implementing this branch.

[FOR HUMAN REVIEW]: If the source file is already a WAV or MP3, FFmpeg may still be run for
format normalization (resample to 16 kHz). Confirm whether this passthrough step is acceptable
for audio-only inputs.

---

## SECTION 5 — CURRENT WHISPER PATH (EXECUTE COMMAND → HTTP)

### Architecture

```
Node A (Engine Body)
  n8n workflow1 — Branch D
    ↓
  Execute Command node
    → FFmpeg audio extraction (Section 4)
    ↓
  HTTP Request node
    → POST http://192.168.137.239:[PORT]/transcribe
    → Body: { "audio_path": "...", "task_id": "...", "prompt": "..." }
    ↓
  Node B (R&D Terminal)
    → Whisper HTTP service receives request
    → Loads audio file from shared path (SMB VaultShare) or receives audio as payload
    → Returns transcript JSON
```

### Whisper Endpoint on Node B

- Host: `http://192.168.137.239`
- Port: [INFERENCE — port not confirmed in existing docs. Common values: 9000, 8000, 8080.
  Will must confirm the actual port and update this doc.]
- Endpoint: `/transcribe` [INFERENCE — confirm actual route]
- Method: POST
- Expected response: JSON with `text` field containing the transcript

[FOR HUMAN REVIEW]: Confirm the Whisper service port and endpoint route on Node B. This is
the minimum required to implement Branch D.

### Audio File Transfer

Two options for getting the audio file to Node B:

| Option | Method | Notes |
|--------|--------|-------|
| A (current) | SMB shared path — Node B reads from `\\192.168.137.1\VaultShare\99_INBOX\QUEUE\` | Requires SMB share is mounted on Node B. No file transfer overhead. |
| B (alternative) | HTTP multipart upload — audio bytes sent in POST body | No SMB dependency, but larger request. [FOR HUMAN REVIEW] |

Recommend Option A as it uses the already-confirmed SMB VaultShare link.

---

## SECTION 6 — OUTPUT FORMAT

Transcripts are written to `C:\SFV_BLUEPRINT\99_INBOX\OUTPUTS\` as Markdown files.

### Output File Naming

```
YYYYMMDD-###_[topic-slug]_TRANSCRIPT.md
```

Example: `20260529-001_morning-walk-broll_TRANSCRIPT.md`

### Output File Format

```markdown
---
task_id: YYYYMMDD-###
source_file: [original file_path]
model: whisper-[model-size]
processed_by: Node B (R&D Terminal)
timestamp: ISO8601
status: COMPLETE
---

# Transcript — [topic]

[full transcript text]
```

Raw JSON from Whisper (with word-level timestamps if available) is also preserved as a
sidecar file: `YYYYMMDD-###_[topic-slug]_TRANSCRIPT_RAW.json`

---

## SECTION 7 — STATUS FLOW

```
PENDING       → job envelope written to QUEUE, status field = PENDING
IN_PROGRESS   → lock written to DECISION_LOG.md, FFmpeg and Whisper dispatched
COMPLETE      → transcript written to OUTPUTS\, lock cleared, DECISION_LOG updated
FAILED        → error logged (see Section 8), lock cleared, status = FAILED in DECISION_LOG
DEFERRED      → serial lock was active, job re-queued for retry
```

All status transitions are written to `C:\SFV_BLUEPRINT\99_INBOX\DECISION_LOG.md` with:
- task_id
- task_type: MEDIA
- timestamp
- status
- model used
- error message (if FAILED)

---

## SECTION 8 — ERROR HANDLING

### Scenario A — Whisper Timeout

Cause: Node B is slow (large file, model cold start, or VRAM pressure from another task).

Response:
1. n8n Execute Command / HTTP Request node receives timeout error
2. Write FAILED entry to DECISION_LOG.md with error tag `WHISPER_TIMEOUT`
3. Clear IN_PROGRESS serial lock
4. Write failed job back to QUEUE with status FAILED and retry count incremented
5. If retry count < 3: requeue as PENDING (auto-retry)
6. If retry count >= 3: mark BLOCKED, log to `99_INBOX/FAILOVER_LOG.md`, surface to Will

[FOR HUMAN REVIEW]: Confirm timeout threshold. Recommend 120 seconds for large video files.

### Scenario B — OOM Crash on Node B

Cause: Another process consumed VRAM before the serial lock check, or the serial lock failed.

Response:
1. HTTP Request node returns 500 or connection refused
2. Write FAILED entry: error tag `WHISPER_OOM`
3. Clear serial lock
4. Do NOT retry immediately — wait 60 seconds before requeue to allow Node B VRAM to clear
5. Log to `99_INBOX/FAILOVER_LOG.md`

Note: The serial queue rule in Section 3 is the primary OOM prevention. This handler is the
recovery path if OOM occurs despite serialization.

### Scenario C — FFmpeg Failure

Cause: Source file is corrupt, codec unsupported, or FFmpeg not installed.

Response:
1. Execute Command node returns non-zero exit code
2. Write FAILED entry: error tag `FFMPEG_ERROR`
3. Do not dispatch to Node B (no audio to transcribe)
4. Log error details (exit code, stderr) to DECISION_LOG.md
5. Mark job BLOCKED — requires Will's attention

### Scenario D — Node B Offline

Cause: R&D Terminal is powered off or network path `192.168.137.239` is unreachable.

Response:
1. HTTP Request node times out or returns connection refused
2. Write FAILED entry: error tag `NODE_B_OFFLINE`
3. Set status DEFERRED — do not retry until Node B is confirmed online
4. Log to `99_INBOX/FAILOVER_LOG.md`
5. No fallback: Node A's RTX 5080 can run Whisper, but this is not in Phase 1 scope

[FOR HUMAN REVIEW]: Should Node A be configured as a Whisper fallback if Node B is offline?
This would require installing Whisper on Node A. Recommend deferring to Phase 2.

---

## SECTION 9 — FASTER-WHISPER MIGRATION PATH

### What faster-whisper Is

faster-whisper is a Python reimplementation of OpenAI Whisper using CTranslate2.
It is listed as [FUTURE] in AI_STACK_ARCHITECTURE_BLUEPRINT §8.

Key improvements over standard Whisper:
- 4x faster transcription on the same hardware
- Lower peak VRAM usage (better for RTX 3060's 12GB constraint)
- Supports int8 quantization for further memory reduction
- Word-level timestamps included by default

### Migration Path

The migration is designed to be a drop-in replacement. The HTTP interface does not change.

| Item | Current (standard Whisper) | After faster-whisper |
|------|---------------------------|----------------------|
| Service | Standard OpenAI Whisper HTTP | Python Flask/FastAPI wrapping faster-whisper |
| Endpoint | `http://192.168.137.239:[PORT]/transcribe` | Same — endpoint unchanged |
| Request schema | `{ audio_path, task_id, prompt }` | Same |
| Response schema | `{ text }` | `{ text, segments }` — segments add timestamps |
| VRAM usage | Higher (float16) | Lower (int8 quantization available) |
| Processing speed | Baseline | ~4x faster |
| Serial queue rule | Required | Still required — lower risk but not eliminated |

### Migration Steps (Phase 2)

1. Install faster-whisper on Node B:
   ```
   pip install faster-whisper
   ```
2. Write a lightweight Flask/FastAPI wrapper that exposes `/transcribe` with the same
   request/response schema as the current Whisper HTTP service
3. Deploy wrapper as a Windows service or persistent background process on Node B
4. Test with one MEDIA task — confirm output parity with current Whisper output
5. Update this doc: change port/endpoint entries from [INFERENCE] to confirmed values
6. Update AI_STACK_ARCHITECTURE_BLUEPRINT §8 to remove [FUTURE] tag from faster-whisper

[FOR HUMAN REVIEW]: Confirm which faster-whisper model size to use on RTX 3060.
Options: `tiny`, `base`, `small`, `medium`, `large-v2`. Recommend `medium` for quality/speed
balance. `large-v2` may push VRAM limits on concurrent system load.

---

## IMPLEMENTATION ORDER

| Priority | Action | Phase |
|---|---|---|
| Now | Confirm Whisper port and endpoint on Node B | Pre-Phase 1 |
| Now | Confirm FFmpeg installed on Node A (`ffmpeg --version`) | Pre-Phase 1 |
| Phase 1 | Implement serial lock in workflow1 using DECISION_LOG.md | Phase 1 |
| Phase 1 | Build Branch D in n8n: FFmpeg → HTTP Request → Whisper | Phase 1 |
| Phase 1 | Define output file naming and write transcript to OUTPUTS\ | Phase 1 |
| Phase 2 | Deploy faster-whisper Flask wrapper on Node B | Phase 2 |
| Phase 2 | Evaluate Node A Whisper fallback (if Node B offline) | Phase 2 |
| Phase 3 | Replace DECISION_LOG.md serial lock with Redis lock | Phase 3 |

---

## CONNECTED FILES
- [[AI_STACK_ARCHITECTURE_BLUEPRINT]]
- [[ENGINE_COMMUNICATION_MODEL]]
- [[RD_TERMINAL_ARCHITECTURE]]
- [[workflow1_queue_processor]]
