---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# QUALITY CONTROL SYSTEM

## PURPOSE
Ensure SFV_UGC deliverables meet quality standards before client delivery.
AI audits. Will reviews. Feedback trains the system.

## SCOPE
Primary branch: SFV_UGC
Secondary: SFV_EVENTS, SFV_STUDIO (technical QC only)

## QC CHECKS (per reel batch)
- Brand alignment: does it match client's established style?
- No typos in text overlays or captions
- No misplaced overlays or transitions
- Audio sync correct
- Correct export specs for platform
- Hook strength (lightweight check only)
- CTA present and correct

## FLOW
```
Reel batch exported
→ local model pre-audit (R&D terminal)
→ issues flagged
→ auto-fix if possible
→ if not fixable → flagged for human rework
→ Claude API final audit layer (if needed)
→ Will reviews before posting
→ Will approves or rejects
→ approved → delivered to client
→ rejected → reworked, re-audited
→ both outcomes logged to TRAINING_DATA
```

## TRAINING LOOP
Approved reels → QC_APPROVED/ folder
Rejected reels → QC_REJECTED/ folder
Over time: system learns what quality looks like for each client.
Client-specific QC improves with each batch.

## NOTES
QC is a technical system. It does not replace Will's creative judgment.
Will reviews every deliverable before client sees it.
