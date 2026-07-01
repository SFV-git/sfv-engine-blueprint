---
STATUS: FOR HUMAN REVIEW
VERSION: v0.1.0
OWNER: WILL
LAST_UPDATED: 2026-05-29
CREATED_BY: Claude Code
MERGE_INTO: STANDALONE
---

# COST CEILING POLICY — SFV AI STACK

> Documents the alert thresholds, tracking mechanism, and escalation rules for cloud AI spend.
> No automatic kill-switch is implemented. Will reviews alerts and acts manually.

---

## SECTION 1 — POLICY STATEMENT

**Decision (CONFIRMED 2026-05-29):** Alert-only. No automatic kill-switch.

The SFV Engine stack does not shut down services or abort running jobs when a spend threshold is crossed. Instead, it writes a structured alert entry to `C:\SFV_BLUEPRINT\99_INBOX\COST_ALERTS.md` for Will to review at session start or session end.

Will is the only authority who can act on a cost alert. No automation may pause, throttle, or reroute cloud calls based on spend thresholds alone.

**Rationale:** Hard kill-switches interrupt live workflows and could corrupt partial outputs. An alert-only policy keeps the system running while surfacing the signal.

---

## SECTION 2 — PER-TOOL BUDGET THRESHOLDS

### 2.1 Claude Code (Anthropic API — API key mode)

| Threshold | Value | Action |
|---|---|---|
| Hard cap | $25.00 | Already set in Anthropic console — enforced by Anthropic, not by SFV Engine |
| Alert threshold | $20.00 (80% of cap) [INFERENCE] | Write COST_ALERTS.md entry |
| Escalation threshold | $23.00 [INFERENCE] | Pause session, report to Will before continuing |

> [INFERENCE] — $20 and $23 alert levels are proposed defaults. Will sets exact numbers.

**Notes:**
- The $25 hard cap at the Anthropic console is the only enforced ceiling. Once hit, all API calls fail.
- The $20 alert exists so Will has runway to finish a session or raise the cap before hitting the wall.
- If spend reaches $23+ mid-session: stop, append alert row, report to Will before executing further tool calls.

---

### 2.2 Tavily API (subscription — fixed monthly cost)

| Threshold | Value | Action |
|---|---|---|
| Cost alert | N/A | Fixed subscription — no usage-based billing |
| Anomaly alert | >200 calls/day | Write COST_ALERTS.md entry — unexpected volume may indicate a loop |

> No cost monitoring needed. Volume monitoring only. Flag if n8n workflow triggers Tavily >200 times in a 24-hour window — this signals a runaway workflow, not normal usage.

---

### 2.3 Gemini Flash (Google AI — free tier / AI Ultra post-preview)

| Threshold | Value | Action |
|---|---|---|
| RPD alert | 1500 requests/day (INFERENCE) | Free tier daily limit — write COST_ALERTS.md entry |
| Alert trigger | Approaching 1500 RPD | Flag: risk of service interruption if limit is hit |
| Post-preview billing | [FOR HUMAN REVIEW] | If Google ends free preview, RPD may convert to billable — reassess thresholds |

> [INFERENCE] — 1500 RPD is the current free tier limit sourced from RATE_LIMITS.md. Check Google AI Studio docs if behavior changes.
> [FOR HUMAN REVIEW] — If Gemini Flash moves to paid billing, this policy section must be updated before the next session.

---

### 2.4 Ollama (local — Engine Body)

No monitoring needed. Zero cost, no rate limits, no daily cap. See RATE_LIMITS.md for context window constraints.

---

### 2.5 Perplexity (subscription — fixed monthly cost)

Fixed cost. No usage-based billing. No alert threshold needed.

---

## SECTION 3 — ALERT MECHANISM

### How alerts are written

Alert entries are appended to `C:\SFV_BLUEPRINT\99_INBOX\COST_ALERTS.md`.

- Append-only. Never delete or overwrite rows.
- Claude Code or Antigravity may write alert rows.
- No tool may silently suppress an alert condition.

### When to check

At the start of every Claude Code session: read COST_ALERTS.md before beginning work. If an open alert is present (no [RESOLVED] tag), report it to Will.

---

## SECTION 4 — COST_ALERTS.MD FORMAT

File location: `C:\SFV_BLUEPRINT\99_INBOX\COST_ALERTS.md`

### Row format

```
| DATE | TOOL | USAGE / LIMIT | STATUS |
```

### Example rows

```
| 2026-05-29 | Claude Code | $18.50 / $25.00 | 74% — approaching cap |
| 2026-05-29 | Gemini Flash | 1200/1500 RPD | 80% — monitor |
| 2026-05-29 | Claude Code | $23.10 / $25.00 | 92% — PAUSED, waiting for Will |
| 2026-05-29 | Tavily | 247 calls today | ANOMALY — check n8n workflow for loop |
```

### Resolved row format

Add `[RESOLVED]` and the resolution note to the status column when Will acts:

```
| 2026-05-29 | Claude Code | $23.10 / $25.00 | 92% — [RESOLVED] Cap raised to $50 |
```

---

## SECTION 5 — DAILY TRACKING

At session end, Claude Code or Antigravity appends a cost summary row to COST_ALERTS.md with:
- Date
- Tool
- Estimated token spend for the session (input + output tokens × rate, or best estimate)
- Running total for the billing period if known

This is a manual tracking mechanism, not automated telemetry. Accuracy is best-effort.

---

## SECTION 6 — ESCALATION TO ACTION

| Condition | Required action |
|---|---|
| Claude Code reaches $20 | Append alert row to COST_ALERTS.md. Continue session. |
| Claude Code reaches $23+ mid-session | Stop immediately. Append alert row. Report to Will. Do not continue until Will responds. |
| Anthropic $25 hard cap hit | All Claude API calls will fail. Will must raise cap in Anthropic console before resuming. |
| Gemini RPD at 80%+ (1200+ calls) | Append alert row. Switch remaining tasks to Ollama if possible. |
| Tavily >200 calls/day | Append anomaly row. Inspect n8n workflow for unintended loop. Report to Will. |

---

## SECTION 7 — FUTURE PHASE 3 INTEGRATION

> [FOR HUMAN REVIEW] — Phase 3 item. Do not implement until Prometheus is live.

Connect to Prometheus alerting when MONITORING_STACK is deployed:
- Trigger alert rule when DECISION_LOG shows >50 Gemini Flash calls within any 1-hour rolling window
- Surface Prometheus alert in Grafana dashboard (if deployed)
- Alert rule should write to COST_ALERTS.md via a Prometheus Alertmanager webhook hitting n8n

Pre-requisite: MONITORING_STACK.md must reach STATUS: CANON and be deployed before this can be built.

---

## CONNECTED FILES
- [[COST_ALERTS|Cost Alerts]]
- [[CLAUDE|Claude Integration]]
- [[RATE_LIMITS|Rate Limits Policy]]
- [[INTEGRATIONS|Tool Integrations]]
- [[CURRENT_DIRECTIVE|Current Directive Rules]]
