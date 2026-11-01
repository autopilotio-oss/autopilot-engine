# FIRST SALES MODE audit

## Nov 1 2026 (operator, 07:15 to 07:45 ART)

Site checked against the local docs/ folder served on localhost (autopilotoi.app is not reachable from the operator sandbox; GitHub Pages deploys after the last commits all succeeded). Playwright, Chromium, widths 390 and 1280, every docs/**/index.html (20 pages), loaded with ?utm_source=audit&utm_medium=test&utm_campaign=first_sales&utm_content=audit.

| Check | Result |
|---|---|
| JS errors | none on any page |
| Horizontal overflow at 390 px | none (scrollWidth equals viewport on all 20 pages) |
| Internal links | no broken links (relative links on /g/lower/ and /quiz/ resolve on /free/ after redirect) |
| Buy buttons | 43 Gumroad links across 17 pages; all point to products in docs/live.json; none disabled; every one rewritten to /l/<slug>/LAUNCH30 with utm_source, utm_medium, utm_campaign, utm_content (+ ft first touch) |
| Launch banner | shown on every page with a buy link |
| GoatCounter | count.js requested on every page; checkout-click/<slug>/<page>/<source> fires on buy click (17/17 pages tested); optin/<page>/<source> fires on Kit submit |
| Kit opt in | #kf form on home, /g/subs/, /g/refund/, /g/bill/ (and the other guides) POSTs to app.kit.com/forms/10118407/subscriptions (request intercepted, not sent) |
| Delivery | 10 single products have products/<slug>/file.enc and product.json version = state/products.json version; bundles all-money-agents (v5) and tiktok-agents (v1, adopted) are assembled from component sealed files plus products/_bonus/money-pro/file.enc |
| Health checks | state/health/status.json: all checkout:<slug> and page:<name> checks ok |

### Fixed
- /quiz/ and /g/lower/ redirect to /free/ with a meta refresh that dropped the query string, so any post linking there lost its utm_source/utm_content and the checkout clicks showed as direct. Now a script redirect keeps location.search (meta refresh kept as fallback). Verified: /quiz/?utm_source=instagram&utm_content=test1 lands on /free/ with the params and the buy link carries them.
- Factory reel template: the big number held at full value only about 0.2 s (gate finding on subs-leak and refund-fighter). Count now runs 0.45 s and the card starts earlier in the beat, so the final number stays on screen about 1 s or more. Applies from the next render.

### Open (not fixed today)
- /free/ (the ManyChat DM link) has no email opt in form; the guides it links to do. Candidate for the Nov 8 to 10 funnel fix if guide visits are high and opt ins low.
- End card covers in the rendered flagship reels still read "Subscription Agent" and "Refund Agent"; the product renames and new thumbnails are Nov 3 to 4 work (step b).
- bill-agent sealed file is about 0.35 MB (4 pages) vs 1.4 to 1.9 MB for the others: Nov 3 to 4 work (step a).
- "Keep the Threads key alive" workflow failed at 04:36 ART: Threads API says the stored token cannot be parsed (OAuth 190). Campaign posts go to Threads through Metricool, so reels are not affected; the direct Threads workflow may be posting nothing. Needs a new Threads token from Seb if the direct workflow matters.
- Audio: refund-fighter true peak +0.4 dBTP after single pass loudnorm (target -1.5). Audible clipping not observed; consider two pass loudnorm in make.sh final.
