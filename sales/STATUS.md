# Sales recovery status (statuses: live, tested, built, blocked, not started)

Updated 2026-11-02 by Claude. Source of truth for offers: `config/offers.json`.

| Item | Status | Evidence |
| --- | --- | --- |
| Offer manifest + CI rules (stale copy, forbidden claims, prices, promo expiry, keyword links) | live | tests/test_manifest.py, CI green on 95e8f44 |
| Front Desk Kit hero page /front-desk/ with sample output check | live | health check page:front_desk + landing_price pass |
| /autopilot/ and /store/autopilot/ → /front-desk/; /store/ → /library/ | live | health redirect checks pass |
| Keyword DM replies (WORKSPACE, BRAIN, AGENT(S), new FRONTDESK) | live | config/keywords.json, used hourly by daily.yml |
| /brain and /free upsell → Front Desk Kit $39 | live | pages pushed, stale copy test passes |
| Kit "Business Brain" sequence: $49 Workspace emails unpublished, 2 Front Desk Kit emails published | live | Kit sequence 2951307 (0 subscribers so far) |
| Production check: Gumroad price/name/live vs manifest, landing prices, redirects, pixel | live | hourly health.yml; last run failing only meta_pixel_configured |
| Sales dashboard (orders, refunds, fees, spend, CAC, contribution, activations, objections) | built | SALES.md, refreshed every 3h by revenue.yml |
| Meta Pixel on site and Gumroad | blocked | needs Seb: no pixel exists on the ad account |
| Gumroad → Kit purchase onboarding (sequence 2954468) | blocked | test purchase done; needs Seb: connect Gumroad in Kit + Purchase automation |
| Test checkout and delivery | tested | Nov 2: Seb bought Front Desk Kit with a one use 100% code (SEBTEST9089, deleted after); receipt and PDF delivered. $0 order, not revenue |
| 3 owner usability tests | not started | protocol: sales/usability_test.md; invites need Seb's approval |
| Qualified owner and partner outreach | not started | drafts: sales/invites.md; nothing sent |
| Paid ads | blocked by policy | $60 cap; only after tracking + 3 tests pass and Seb approves |
| Office Autopilot retest on current Claude plans | not started | advertising on hold |
| Gumroad covers (one current cover per product) | tested | cover_check workflow: diff 0.0 vs current art for all 3 |
| Gumroad thumbnails | blocked | Seb uploads the 3 thumbnail files (API can't set them) |
| 3 search intent guides (/guides/reply-to-price-inquiry, after-hours-customer-messages, follow-up-on-a-quote) | live after deploy | hourly health check covers them |
| 3 Threads demo posts (Nov 4, 5, 6, 9:30 ET) linking the guides | waiting for Seb's YES | queue/2026-11-04-frontdesk.json; approval issue opens about 1 hour before each |

## 2026-11-02 night (verified)
- All 14 Gumroad prices verified via API against config/offers.json; health checks library prices hourly.
- LAUNCH30 removed from Office Autopilot (on hold); sync log: offer_code_withdrawn workspace.
- Free offer renamed Front Desk Starter (/brain/); paid stays Front Desk Kit $39.
- Share images per page fixed; meta added to Office Autopilot, brain, free.
- Office Autopilot copy: old Workspace name gone, schedule claim accurate. Full redesign skipped while on hold.
- Health: only meta_pixel_configured failing (needs Seb's pixel ID). CI green.

## 2026-11-03 Master Plan session (verified)
- Integration audit: audit/integration_inventory.md. G0 not passed: no Meta Pixel exists (0 pixels on ad account), Kit has no Gumroad integration (0 purchases), a $0 order is invisible to the ledger, GoatCounter data unreadable.
- Ad spend corrected: $49.89 (Oct 30 to Nov 1 boost), contribution -$49.89.
- Funnel: /front-desk/after-hours/ and /front-desk/demo/ live after deploy; email capture on /brain/ (top) and all Front Desk pages.
- Daily report: growth/report_daily.md, refreshed every 3 h by revenue.yml.
