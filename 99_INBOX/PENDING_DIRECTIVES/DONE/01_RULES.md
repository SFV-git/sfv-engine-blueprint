---
STATUS: ACTIVE
DIRECTIVE_ID: REVAMP-20260701-RULES-001
EXECUTOR: ollama
---

You are revising a governance doc for SFV Engine, a solo photography/video production business.
The current 01_CANON_RULES/RULES.md scored 3/5: right framework but lacks specific, actionable guidance.

Rewrite it as a complete, specific rules doc. Keep it grounded in this reality:
- SFV is a SOLO operator (Will). No teams, no employees yet.
- Core governance is "Blueprint Lock": no dev work until a feature is fully planned and Will approves; nothing becomes CANON without Will's explicit ratification; AI sessions can draft/propose but never self-approve architecture.
- Routing rule: ollama=cheap mechanical work, claude_code=multi-file authoring, codex=narrow coding with locked specs, claude=hard one-shot judgment.
- Every AI output is labeled UNCONFIRMED / INFERENCE / FOR HUMAN REVIEW until Will ratifies.

Output a clean markdown rules doc with numbered, enforceable rules grouped under clear headings
(Governance, AI Execution, Vault Discipline, Change Control). Be specific and actionable, not vague.
Do not invent facts about the business beyond what is stated above. Output only the finished markdown.
