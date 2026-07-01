---
STATUS: ACTIVE
DIRECTIVE_ID: PLAN-20260701-PROMPT-VERSIONING-DEPTH-001
EXECUTOR: ollama
---

Draft a deeper "Prompt Versioning Workflow" section: given a system where n8n workflow nodes call Ollama with hardcoded prompts, propose a concrete versioning scheme (e.g. v1, v2 naming), a PROMPT_CHANGELOG.md entry format (date, prompt name, version, what changed, why), and a lightweight before/after A/B testing method a solo operator could actually do without extra tooling (e.g. run both versions on the same 5 saved test cases, compare outputs manually). Output only the finished markdown section, no preamble.
