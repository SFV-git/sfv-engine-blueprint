---
STATUS: ACTIVE
DIRECTIVE_ID: DEV-20260701-ORPHAN-DETECTOR-V2-001
EXECUTOR: codex
---

Read C:\SFV_BLUEPRINT\99_INBOX\find_orphans.py for reference (do not modify it). Write a NEW script C:\SFV_BLUEPRINT\99_INBOX\find_orphans_v2.py that improves on it: in addition to finding vault .md files with zero inbound wikilinks, also flag files whose frontmatter STATUS is missing entirely, and files that reference a wikilink target that doesn't exist anywhere in the vault (broken links). Write results to C:\SFV_BLUEPRINT\00_DEV_LOG\ORPHANS_V2.md. Run it once to generate output. Do not modify find_orphans.py or ORPHANS.md. Do not touch n8n, Docker, git push, or any live service.
