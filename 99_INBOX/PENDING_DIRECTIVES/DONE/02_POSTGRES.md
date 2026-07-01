---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-POSTGRES-001
EXECUTOR: ollama
---

You are revising 03_INFRASTRUCTURE/POSTGRES_MIGRATION.md for SFV Engine. It scored 3/5: right
direction, missing implementation detail. Context: n8n currently runs on SQLite and must migrate to
PostgreSQL before queue-mode / concurrency. Runs on Engine Body (Ryzen 9 9900X, RTX 5080, Windows 11,
Docker installed). n8n is Postgres-backed once migrated.

Write a complete, ordered migration runbook covering: (1) prerequisites (Docker running, backup of
current SQLite n8n data), (2) standing up a PostgreSQL container with a persistent named volume,
(3) the n8n environment variables that switch it from SQLite to Postgres (DB_TYPE, DB_POSTGRESDB_*),
(4) exporting existing n8n workflows/credentials before the switch and re-importing after, (5) verification
steps (n8n health 200, workflows present, a test execution), (6) rollback procedure if it fails.

Be specific with actual env var names and docker concepts. Mark anything you are not certain about as
[UNCONFIRMED — verify against current n8n docs]. Do not invent version numbers. Output only finished markdown.
