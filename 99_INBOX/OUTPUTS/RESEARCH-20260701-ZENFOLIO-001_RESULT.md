# RESULT -- RESEARCH-20260701-ZENFOLIO-001

- Executor: claude_code
- Status: complete
- Dispatched: 2026-07-01 01:46:41

---

Done. Wrote findings to `C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\research_zenfolio_verification.md` (new file; nothing else touched). Summary of what the research found:

**1. Storage/bandwidth (Advanced tier)** — Unlimited photo storage + 150 GB video (4K, 30 GB max file). **Bandwidth cap: UNCONFIRMED** — Zenfolio markets photographer-grade bandwidth but publishes no hard numeric transfer cap.

**2. Pricing** — Advanced = **$40/mo**, discounted annually. The exact annual rate is inconsistent across sources (~$20 vs ~$16/mo), so I flagged it UNCONFIRMED.

**3. QR gallery delivery — YES, but Advanced-only.** Two documented features: per-gallery unique QR codes (download as **PNG**, auto-redirect if the link changes) and a bulk "QR Code Workflow" for volume/event shoots (CSV import, auto-sorting by scanned QR card). This is a genuine primary-source-confirmed capability.

**4. Multiple devices / concurrent logins** — This is the shakiest area, so I split it deliberately:
- **Confirmed:** Advanced supports **multiple named user accounts** under one subscription (legacy docs cite up to 30) — so parallel work via *separate* sub-user logins is supported.
- **UNCONFIRMED:** whether *one identical credential* can be logged in on several laptops at once for concurrent uploads, and any session limit. My recommendation: architect around per-laptop sub-users, not a shared login, and confirm with Zenfolio.

**5. QR business-card printing** — VistaPrint (budget, any stock) and MOO (higher quality, Printfinity = 50 unique designs/pack, closest to a per-gallery card workflow). No special paper needed.

**6. QR export formats** — Industry norm is SVG/EPS (vector) best for print, PNG at ≥300 DPI acceptable, never JPEG. Caveat: **Zenfolio only exports PNG** — vector master would need a separate generator.

A couple of caveats worth calling out: two Zenfolio *Classic* support pages (the multi-user-accounts and login/logout articles) returned **HTTP 403** to automated fetching, so those specifics (the "30 users" figure, session behavior) are cited from search summaries and flagged for browser verification. The file ends with a consolidated list of all 7 UNCONFIRMED items needing direct verification. Every claim is cited with source URLs, and Adobe/Google MCP connectors weren't relevant here so I didn't touch them.
