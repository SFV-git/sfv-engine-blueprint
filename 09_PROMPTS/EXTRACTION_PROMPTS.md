---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# EXTRACTION PROMPTS

Prompts for extracting structured information from conversations
and adding it to the vault.

---

## CHAT EXTRACT PROMPT
```
Read this conversation excerpt and extract:
1. CANON decisions (approved by Will)
2. UNCONFIRMED items (discussed but not locked)
3. FOR HUMAN REVIEW proposals (Claude suggestions)
4. QUESTIONS FOR WILL (still open)
Format as markdown lists ready to paste into the vault.
Conversation: [PASTE EXCERPT]
```

## DECISION LOG PROMPT
```
Summarize this session's decisions for DECISIONS.md.
Format:
## [DATE]
### [Decision title]
[One paragraph description]
Session content: [PASTE OR DESCRIBE]
```

## CONNECTED FILES
- [[01_CANON_RULES/RULES|Canon Rules]]
- [[00_DEV_LOG/UNCONFIRMED|Unconfirmed Items]]
- [[00_DEV_LOG/PROPOSALS|Proposals]]
- [[03_INFRASTRUCTURE/METADATA_SYSTEM|Metadata System]]
- [[04_WORKFLOWS/UGC_PRE_PRODUCTION|UGC Pre-Production]]
- [[00_DEV_LOG/QUESTIONS_FOR_WILL|Questions for Will]]
- [[03_INFRASTRUCTURE/STORAGE_ARCHITECTURE|Storage Architecture]]
