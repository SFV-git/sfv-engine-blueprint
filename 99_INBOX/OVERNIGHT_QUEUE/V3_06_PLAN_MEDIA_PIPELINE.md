---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-MEDIA-PIPELINE-001
EXECUTOR: ollama
---

Draft a detailed "Serial Queue Processing Rules" section for a media pipeline document, for a system that processes video/photo files through FFmpeg (transcoding) and Whisper/faster-whisper (transcription) on a single GPU machine. Cover: why serial (not parallel) processing is required on limited VRAM, a proposed queue priority order (client-facing work first), how to handle a stuck/hung job (timeout + skip logic), and a simple retry policy. Output only the finished markdown section, no preamble.
