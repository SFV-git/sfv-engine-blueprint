---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-FAILOVER-DEPTH-001
EXECUTOR: ollama
---

Draft a deeper "Node B Failover Behavior" section for a 2-node home AI setup where a secondary machine (R&D Terminal) can run Ollama as a fallback if the primary (Engine Body) goes offline. Propose: how a workflow should detect the primary is unreachable (timeout value), how it should redirect to Node B, what model Node B should keep loaded for this purpose given it likely has less VRAM, and how to detect and log when failover happened so it's not silently missed. Output only the finished markdown section, no preamble.
