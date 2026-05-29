---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# DATABANK ARCHITECTURE

## PURPOSE
Maps every databank in the SFV system.
Blueprint vault documents structure. Engine holds actual data.

## TWO LAYERS
```
SFV_BLUEPRINT/12_DATABANKS/    ← architecture docs (this vault)
SFV_ENGINE/DATABANKS/           ← actual data (built in v2.x+)
```

## DATABANK TYPES

### CONTENT BANKS
Hooks, CTAs, script templates, content map templates.
Fed by: UGC production sessions, successful content analysis.
Used by: Claude API (caption generation), n8n (content map builder).

### TASTE BANKS
Visual references, grade references, edit style per branch.
Fed by: Will's selections, are.na research, R&D terminal trend research.
Used by: Archive curation support, QC audit visual baseline.

### CLIENT BANKS
Client profiles, briefs, feedback, memory per client.
Fed by: each UGC client session, QC outcomes.
Used by: monthly content map generation, brief generation.

### BRAND BANKS
SFV visual language, caption style per branch.
Fed by: Will's decisions, design sessions.
Used by: all AI calls involving SFV brand voice.

### RESEARCH BANKS
Trend research, platform insights.
Fed by: R&D terminal continuous research (24/7).
Used by: content map generation, template updates.

### TRAINING DATA
QC approved and rejected reels.
Fed by: every UGC delivery outcome.
Used by: QC system training, improving accuracy over time.

## CONNECTED FILES
- [[COMPRESSED_CONTEXT|Compressed Context]]
- [[CLAUDE_API|Claude API]]
- [[RD_TERMINAL_ARCHITECTURE|RD Terminal Architecture]]
- [[BRANCH_OUTPUTS|Branch Outputs]]
- [[QUALITY_CONTROL|Quality Control]]
- [[STORAGE_ARCHITECTURE|Storage Architecture]]
- [[DEEP_RESEARCH_FINDINGS|Deep Research Findings]]
