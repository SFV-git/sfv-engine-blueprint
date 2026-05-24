# TASK QUEUE
Claude or Will adds tasks here. Daemon picks them up every 30 seconds.
Separate tasks with ---
Completed tasks get moved to OLLAMA_RESULTS.md automatically.

---
AUDIT: Read COMPRESSED_CONTEXT.md and SESSION_STATE.md. List the top 5 gaps in the current blueprint based on what's UNCONFIRMED. Output numbered list only.
---
REVIEW: Read 04_WORKFLOWS/INGEST.md. Find any missing steps or failure points. Output: numbered list of issues. If none, say CLEAN.
---
REVIEW: Read 02_BRANCHES/BRANCH_OUTPUTS.md. Check every branch has ENGINE_LEVEL, CONTENT_TYPES, INGEST_PATH, OUTPUT_PATH defined. List any missing fields.
---
