---
STATUS: CANON
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-24
---

# OLLAMA PROMPTS — SFV ENGINE

## SYSTEM PROMPT (prepend to every call)
```
You are a task assistant for SFV Engine, a photography production system.
Branches: MYTHOLOGY, LIVE, EVENTS, ATHLETICS, STUDIO, UGC, ARCHIVE, WORLD, 404
Revenue: UGC content retainers + EVENTS on-site portraits
Your role: handle specific low-value tasks only. Be structured. Never make creative decisions.
If unsure, say UNSURE — never guess.
Output exactly what is asked. No extra commentary.
```

---

## TASK PROMPTS

### SUMMARIZE
```
Summarize this in 3 bullet points for SFV vault reference:
[paste content]
```

### TAG FILE
```
Tag this content for SFV Engine.
Output exactly:
BRANCH: [branch name]
CONTENT_TYPE: [photo/video/reel/graphic]
STATUS: [raw/select/export/delivered]
PRIORITY: [high/medium/low]
Content: [paste]
```

### CAPTION DRAFT
```
Draft 3 Instagram caption options for SFV [BRANCH] account.
Style: [raw/professional/polished]
Content: [describe the photo/video]
Rules: under 150 chars each, no hashtags, no emojis unless natural
Output numbered list only.
```

### RESEARCH SYNTHESIS
```
Synthesize this research for SFV Engine context.
Topic: [topic]
Output: 5 bullet points, practical only, no fluff, no generic advice.
Source: [paste content]
```

### QC PRE-CHECK
```
QC check this reel before Will reviews it.
Check for: typos, missing CTA, off-brand elements, technical issues.
Output: PASS or FAIL
If FAIL: numbered list of specific issues only.
Content description: [paste]
```

### BLUEPRINT AUDIT
```
Audit this workflow section for gaps or failure points.
Output: numbered list of issues only. Be specific.
If no issues: say CLEAN.
Workflow: [paste]
```

### HOOK GENERATION
```
Generate 5 hook options for a [niche] reel.
Client type: [fitness trainer / athlete / etc]
Topic: [what the reel is about]
Format: first 3 seconds of video, spoken or text on screen.
Output numbered list only. No explanation.
```

### CONTENT MAP DRAFT
```
Draft a monthly content map for a [niche] client.
Deliverables: [X reels per month]
Goals: [awareness / conversion / both]
Output: week by week, one concept per week, hook idea included.
Keep it practical. No filler weeks.
```

### SHOOT BRIEF
```
Generate a shoot execution packet for:
Client: [name]
Niche: [type]
Deliverables: [what needs to be filmed]
Output:
- Scripts (2-3 per reel concept)
- Hooks (3 options per script)
- B-roll list
- CTA options
- Outfit/location notes
Be specific. No generic advice.
```

## CONNECTED FILES
- [[05_AI_LAYER/QUALITY_CONTROL|Quality Control]]
- [[03_INFRASTRUCTURE/METADATA_SYSTEM|Metadata System]]
- [[12_DATABANKS/BRAND_BANKS|Brand Banks]]
- [[12_DATABANKS/RESEARCH_BANKS|Research Banks]]
- [[05_AI_LAYER/COST_ROUTING|Cost Routing]]
- [[08_TESTS/FAILURE_TESTS|Failure Tests]]
