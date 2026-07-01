# RESULT -- DEV-20260701-BOM-STRIP-FIX-001

- Executor: codex
- Status: complete
- Dispatched: 2026-07-01 02:01:43

---

Updated only:

- `workflow1_queue_processor.json`: strips UTF-8 BOM before `JSON.parse`.
- `CHANGELOG.md`: notes the fix is not yet live.

Workflow JSON validation passed. No live n8n, Docker, import, restart, or git operations performed.
