---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# BRANCH OUTPUTS

Central reference for what every branch produces.

---

## ENGINE INVOLVEMENT SCALE

| Level | What the Engine Does |
|-------|---------------------|
| 1 | Catches relevant files and stores them |
| 2 | Organizes posts |
| 3 | Rough edit, still gets Will's creative touch |
| 4 | Fully edits and posts |
| 5 | Fully edits, posts, and basically runs the account |
| 6 | Adds advertising content (graphics, Canva ads, etc.) |
| +.5 | Also schedules automatically |

---

## BRANCH SUMMARY TABLE

| Branch | Level | Growth | Reels | Stories | Main Content |
|--------|-------|--------|-------|---------|-------------|
| abbass | 1 | NO | YES* | manual | Myth-building, cinematic raw |
| SFV_LIVE | 3.5 | NO | YES | manual | Raw event coverage, square |
| SFV_EVENTS | 5-6.5 | NO | implied | engine | Professional portraits, service clear |
| SFV_ATHLETICS | 3.5 | NO | implied | manual | Sports coverage, non-traditional |
| SFV_STUDIO | 5.5 | YES | maybe | engine | Portraits, comp cards, headshots |
| SFV_UGC | 6.5 | YES | YES | engine | Polished content, ads, clear offers |
| SFV_ARCHIVE | 3.5 | NO | YES | manual | Music videos, brand shoots, creative |
| SFV_WORLD | 2.5 | NO | implied | manual | Life dumps, vlog style, light edits |
| SFV_404 | 2.5 | NO | implied | manual | Experimental, graphic, over the top |

*abbass reels: Engine catches files, Will builds these himself

---

## REPOST ECOSYSTEM

Accounts support each other within logical groupings:

```
GROUP A — Creative/Talent: ARCHIVE + 404 + ATHLETICS
GROUP B — Service:         STUDIO + UGC + EVENTS
GROUP C — Lifestyle:       WORLD + abbass
GROUP D — Hub:             abbass receives support from all groups
```

---

## CROSS-BRANCH FILING RULES

When a file could belong to multiple branches:
1. Engine flags it FOR HUMAN REVIEW
2. Will makes the final call
3. Decision gets logged in 00_DEV_LOG/DECISIONS.md

Basic logic (not exhaustive):
- Will in photo → consider abbass catch
- Backdrop + paid session → SFV_EVENTS
- Event, no backdrop → SFV_LIVE
- Controlled studio lighting → SFV_STUDIO
- Non-traditional sports → SFV_ATHLETICS
- Best creative work → SFV_ARCHIVE
- Too experimental for Archive → SFV_404

---

## NAMING BY BRANCH

```
MYTHOLOGY_[YYYYMMDD]_[PROJECT]_[####]_[STATUS]
LIVE_[YYYYMMDD]_[EVENT]_[####]_[STATUS]
EVENTS_[YYYYMMDD]_[CLIENT]_[####]_[STATUS]
ATHLETICS_[YYYYMMDD]_[EVENT]_[####]_[STATUS]
STUDIO_[YYYYMMDD]_[CLIENT]_[####]_[STATUS]
UGC_[YYYYMMDD]_[CLIENT]_[####]_[STATUS]
ARCHIVE_[YYYYMMDD]_[PROJECT]_[####]_[STATUS]
WORLD_[YYYYMMDD]_[####]_[STATUS]
SFV404_[YYYYMMDD]_[PROJECT]_[####]_[STATUS]
```

## CONNECTED FILES
- [[00_DEV_LOG/DECISIONS|DECISIONS]]
- [[TOOLBOX|TOOLBOX]]
- [[CONTENT_BANKS|CONTENT BANKS]]
- [[CURRENT_DIRECTIVE|CURRENT DIRECTIVE]]
- [[TOOL_STATUS|TOOL STATUS]]
