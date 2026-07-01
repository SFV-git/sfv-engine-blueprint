---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-ROUTER-TESTS-001
EXECUTOR: codex
---

Read C:\Users\willa\AppData\Local\hermes\sfv_loop\router.py (do not modify it). Write a NEW pytest test file C:\Users\willa\AppData\Local\hermes\sfv_loop\test_router_parse.py that unit-tests the parse_directive() function's edge cases: missing STATUS field, missing DIRECTIVE_ID field, an invalid/unrecognized EXECUTOR value (should default to ollama), a UTF-8 BOM at the start of the file, and a STATUS value that isn't exactly "ACTIVE" (case variations like "active", "Active"). Run pytest on the new file and report the results in the RESULT. Do not modify router.py, watcher.py, or any other file in that folder. Do not touch n8n, Docker, git push, or any live service.
