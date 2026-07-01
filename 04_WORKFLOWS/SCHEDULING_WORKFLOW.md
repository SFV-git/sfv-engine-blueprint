---
STATUS: FOR HUMAN REVIEW
VERSION: v2.0.0
OWNER: WILL
LAST_UPDATED: 2026-07-01
REWRITTEN_BY: Claude Chat (autonomous, web-researched against Later 2026 docs)
SUPERSEDES: v1 (scored 3/5 — invented fake geographic "Branch A-H" in foreign time zones
  UTC+8/Middle East/Europe, referenced nonexistent "branch content managers" and "social teams".
  SFV branches are Halifax-based content categories, not global regions. SFV is a solo operator.)
---

# INSTAGRAM SCHEDULING WORKFLOW

Covers the 8 non-MYTHOLOGY branches (SFV_LIVE, SFV_EVENTS, SFV_ATHLETICS, SFV_STUDIO, SFV_UGC,
SFV_ARCHIVE, SFV_WORLD, SFV_404). All are Halifax-operated content categories on ONE operator's
schedule — NOT separate geographic regions. Locked tool: **Later** (decision recorded 2026-05-26).

## 1. TIMING — SINGLE OPERATOR, ATLANTIC TIME
All accounts post on Atlantic Time (America/Halifax). There are no foreign time zones.
Optimal windows should come from each account's OWN Later "Best Time to Post" data (Growth tier+),
NOT generic guesses. Until each account has ~30 days of engagement data, use these starting
defaults for an Atlantic-audience, then let Later's per-account recommendations override:
- Weekday morning: 7:00–9:00 AM AT (commute/wake scroll)
- Weekday midday: 11:30 AM–1:00 PM AT (lunch)
- Weekday evening: 6:00–9:00 PM AT (primary — highest short-form engagement)
Audience per branch differs (athletes vs event clients vs studio) — refine quarterly from real data.

## 2. LATER PRICING / ACCOUNT ARCHITECTURE — [FOR HUMAN REVIEW, real cost decision]
Later prices by "social set" (one profile per platform per set). 2026 tiers:
- Free: 5 posts/profile/mo (trial only)
- Starter $25/mo: 30 posts/profile, 1 social set, 1 user
- Growth $45/mo: unlimited scheduling, full analytics, best-time-to-post, up to 3 social sets
- Advanced $80/mo: team collab, 6 social sets, competitive benchmarking

**Problem: 8 IG accounts exceeds even Advanced's 6 sets.** Options to decide:
(a) Advanced tier + buy 2 add-on sets, or (b) consolidate low-volume branches (SFV_404, SFV_WORLD,
SFV_ARCHIVE) onto a shared cadence, or (c) evaluate a cheaper multi-account tool (Timed Post cited
at ~$19/mo for 10 accounts — UNVERIFIED, would need testing before switching off the locked Later
decision). Requires Will's call — this is a real recurring-cost fork.

Prerequisite: every SFV account must be an Instagram **Business or Creator** account — Meta's Graph
API requires it for auto-publish. Personal accounts only get push-notification reminders (defeats automation).

## 3. CAPTION INSERTION
Captions pulled from CONTENT_BANKS per branch, voice per branch (see caption-voice decision,
still open in QUESTIONS_FOR_WILL #12). Structure:
```
[Hook — scroll-stopper, first line, no wasted words]
[Branch-specific body — value or context]
[CTA — save/share/comment/DM]
[3–5 branch hashtags — Later hashtag suggestions, saved as reusable groups per branch]
```
Approval: Will reviews before scheduling (solo operator — no "content manager" layer exists).
Hashtags: 3–5 targeted, NOT stuffed. Save per-branch hashtag groups in Later for reuse.

## 4. n8n INTEGRATION
1. Trigger: content approved in vault/queue (batch marked ready for delivery).
2. Fetch: media + caption from branch EXPORT path + CONTENT_BANKS.
3. Route: push to Later via Later API with branch tag + scheduled slot.
4. Notify: confirmation to Will via **Telegram** (locked channel — NOT Slack/email).
Error handling: failed-schedule alert to Telegram. Most failures = expired IG account permission;
fix is reconnecting the account in Later (Graph API token refresh).

## 5. WORKFLOW STEPS
1. Batch content produced + edited (see [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]]).
2. QC self-audit before delivery (brand alignment, no typos/overlay errors, technical check).
3. Will reviews batch.
4. n8n routes approved batch to Later with per-branch timing.
5. Later auto-publishes at scheduled slot via Graph API.
6. Monitor via Later analytics; refine timing/captions quarterly from real per-account data.

## 6. KEY CONSIDERATIONS
- Visual grid planning: use Later's drag-and-drop grid preview to keep each branch feed cohesive
  before anything goes live (Later's core strength for visual brands).
- Content library: centralized approved-asset repository = CONTENT_BANKS + branch EXPORT folders.
- Scalability: n8n handles repetitive rescheduling. As operator count grows (NATIONWIDE plan),
  revisit whether Later's per-set model still fits vs an agency-grade multi-account tool.

## CONNECTED FILES
- [[CONTENT_BANKS|Content Banks]]
- [[BRAND_BANKS|Brand Banks]]
- [[VIDEO_EDIT_WORKFLOW|Video Edit Workflow]]
- [[INTEGRATIONS|Integrations]]
- [[TOOL_STACK|Tool Stack]]
