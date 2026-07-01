---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-CONCURRENCY-DEPTH-001
EXECUTOR: ollama
---

Draft a deeper "Concurrency & Priority Enforcement" section for a single-machine task queue (n8n + Ollama on one GPU, no Redis yet). Propose: a simple max-concurrent-jobs=1 rule and why it's correct for a single-GPU setup, how PRIORITY should be enforced when multiple tasks are queued (client_facing tasks jump the line), and what changes would be needed later if Redis is added for true multi-worker concurrency. Output only the finished markdown section, no preamble.
