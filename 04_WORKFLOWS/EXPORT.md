---
STATUS: UNCONFIRMED
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# EXPORT WORKFLOW

## PURPOSE
Produce final deliverable files in correct specs per branch and platform.

## EXPORT SPECS [UNCONFIRMED — awaiting Will confirmation]

### Photo exports
| Spec | Use case |
|------|---------|
| FULLRES | Client delivery, archive |
| 1080SQ | Instagram feed (1:1) |
| 1080x1350 | Instagram portrait (4:5) |
| 1920x1080 | Landscape/story |

### Video/Reel exports [UNCONFIRMED]
| Spec | Use case |
|------|---------|
| 1080x1920 | Instagram Reels (9:16) |
| 1080x1080 | Square video |
| [TBD] | Platform-specific |

## PER-BRANCH EXPORT NOTES

SFV_STUDIO: Lightroom Classic batch export with sync presets
SFV_LIVE: Minimal processing, square format, basically untouched
SFV_EVENTS: Full res for Pixieset + social specs for IG
SFV_UGC: Reel format, per client spec
SFV_ARCHIVE: Full res + social specs

## TOOLS
- Lightroom Classic: photo batch export (Studio, Events, Archive)
- FFmpeg: video export and format conversion
- n8n: orchestrate export triggers [FUTURE]

## CONNECTED FILES
- [[N8N_BLUEPRINT|N8N Blueprint]]
- [[BRANCH_OUTPUTS|Branch Outputs]]
- [[SFV_EVENTS|SFV_EVENTS]]
- [[TOOLBOX|Toolbox]]
