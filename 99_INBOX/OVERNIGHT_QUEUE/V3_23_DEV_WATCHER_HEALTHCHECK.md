---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-WATCHER-HEALTHCHECK-001
EXECUTOR: codex
---

Read C:\Users\willa\AppData\Local\hermes\sfv_loop\persistence_selftest.py for reference (do not modify it). Write a NEW lightweight script C:\Users\willa\AppData\Local\hermes\sfv_loop\watcher_healthcheck.py that just checks (without dispatching a real directive): is watcher.lock present and does its PID correspond to a running process, and what is the last line of watcher.log with its timestamp (to show how recently it was active). Print a simple HEALTHY / STALE / DEAD verdict based on whether the lock PID is alive. Run it once and report the result. Do not modify watcher.py, router.py, watcher.lock, or watcher.log. Do not touch n8n, Docker, git push, or any live service.
