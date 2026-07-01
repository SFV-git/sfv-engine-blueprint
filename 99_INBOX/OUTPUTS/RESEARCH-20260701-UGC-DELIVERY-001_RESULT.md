# RESULT -- RESEARCH-20260701-UGC-DELIVERY-001

- Executor: claude_code
- Status: complete
- Dispatched: 2026-07-01 01:50:54

---

Done. Wrote the comparison to `C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\research_ugc_delivery_comparison.md` (new file, nothing else touched — no n8n, Docker, git, or live services involved).

## What it covers

A comparison table across all four options plus per-platform tradeoffs, on the exact axes you asked for:

| | Frame.io | Dropbox | Google Drive | Pixieset |
|---|---|---|---|---|
| **Pricing** | Free → Pro $15 → Team $25/seat/mo | Free 2GB → Plus ~$10 → Business ~$10–15+/seat/mo | Free 15GB → Google One/Workspace | Free → $10 → $20 → $50/mo (storage-based) |
| **Client access** | No account (share links) | No account (links/file requests), but no true portal | No account (public links) | No account (gallery links) |
| **Revision/approval** | **Strong** — annotations, comments, approvals | None native | None native | **Favorites** proofing (photo selection, not video markup) |
| **API** | Yes (V4 REST + webhooks) | Yes (mature public API) | Yes (Drive API) | **No native API / no Zapier** — workarounds only |

## Key decision signals (no winner picked)
- **Frame.io** — the only one built for video *review/approval*; best real API, but per-seat cost and Adobe IMS auth friction.
- **Pixieset** — most polished branded *photo* delivery + light proofing, but photo-centric and **automation is the hard gap (no API)**.
- **Google Drive** — cheapest and simplest, but generic and no approval workflow.
- **Dropbox** — solid storage + API, but no native client-portal or review layer.

The biggest strategic fork for a UGC agency: **do you need programmatic/automated delivery pipelines?** If yes, Pixieset's lack of an API is a real constraint the others don't have. All sources are cited inline and in a Sources list at the bottom.

One caveat I baked into the doc: pricing/tiers shift often, so the exact numbers should be re-verified on each vendor's page before you commit.

One note for later — the **Adobe (claude.ai) MCP connector** shown in this session isn't authorized, so I couldn't pull anything from Frame.io's account directly; this was all done via web search. If you ever want live account data, you'd authorize that connector in your claude.ai connector settings.
