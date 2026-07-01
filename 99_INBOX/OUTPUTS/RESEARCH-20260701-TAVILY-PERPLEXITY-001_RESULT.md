# RESULT -- RESEARCH-20260701-TAVILY-PERPLEXITY-001

- Executor: claude_code
- Status: complete
- Dispatched: 2026-07-01 01:54:55

---

Done. Wrote findings to `C:\SFV_BLUEPRINT\FOR_HUMAN_REVIEW\research_tavily_perplexity_refresh.md` (new file only — no other file, and no n8n/Docker/git/keys touched).

## Key findings

**Tavily Search API**
- **Free tier: 1,000 credits/month, indefinite, no credit card.** Basic search = 1 credit, advanced = 2. Credits don't roll over.
- Paid plans (from Tavily's own docs): Project 4,000/$30, Bootstrap 15,000/$100, Startup 38,000/$220, Growth 100,000/$500. PAYG $0.008/credit.
- Rate limits: **100 RPM dev**, 1,000 RPM production.

**Perplexity (Sonar) API**
- **No permanent free tier** — must add a payment method to get a key. Possible one-time ~$25–50 trial credit (secondary sources).
- Cheapest model `sonar`: **$1/$1 per 1M tokens** + a **$5–$12 per 1,000 requests** search fee (by context depth). Sonar Pro is $3/$15 per 1M.
- Tier 0 rate limit: **50 RPM** (`sonar`/`sonar-pro`), 5 RPM deep research. Tiers advance by cumulative spend.

**Recent 2026 changes noted**
- Perplexity **ended the Pro-subscriber ~$5/mo API credit perk in Feb 2026**.
- Perplexity **stopped billing citation tokens** for standard Sonar/Sonar Pro (lowers effective cost).
- No major Tavily pricing/API break surfaced, but plan names/prices vary between vendor docs and aggregators — flagged inline.

**Bearing on the plan (informational only):** For a genuinely low-volume/occasional route, Tavily's free tier means ~$0/month, versus Perplexity's small but unavoidable per-call floor plus required billing. Nothing here contradicts the existing Tavily-based `RESEARCH_ROUTE_SPEC.md`. The real trade beyond price is output shape — Perplexity returns a synthesized cited answer; Tavily returns search results. Watch-items: 1,000-credit non-rollover cap under bursty use, and re-verifying Tavily plan prices at build time. Human review decides.

A caveat worth stating plainly: vendor pricing shifts often and some numbers (trial credits, exact plan tiers) came from aggregators where docs were silent — I flagged those. Re-check the official pages before committing.

Sources: [Tavily pricing](https://www.tavily.com/pricing), [Tavily credits docs](https://docs.tavily.com/documentation/api-credits), [Tavily rate limits](https://docs.tavily.com/documentation/rate-limits), [Perplexity pricing](https://docs.perplexity.ai/docs/getting-started/pricing), [Perplexity rate limits & tiers](https://docs.perplexity.ai/docs/admin/rate-limits-usage-tiers).
