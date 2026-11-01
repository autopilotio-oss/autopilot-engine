# Next actions (handoff between runs)

- Daily Pulse writes run-history/<date>-daily.md; the Weekly Sprint reads the last 7.
- Viral Lab: Subscription first (viral/demos/subscription has the tested synthetic demo). Need 3 qualified references before a concept can pass. BLOCKER (Oct 31 + Nov 1 runs): from the cloud runner, YouTube serves a bot-protection shell (no views, wrong metadata on watch?v=) and TikTok/IG are robots-blocked, so no reference can be certified. Needs Seb's call: a source that shows public view counts (e.g. YouTube Data API key, or Seb captures URL + views + creator's last 10 from his phone).
- Publisher: nothing QUEUED yet; `python3 scripts/growthos/publish.py plan` is empty until Seb approves a concept.
- Decided Oct 31: caps $30/month, keep legacy posts, GitHub alerts confirmed, Seb connecting Gmail for support drafts.

## Inbox alerts (first scan 2026-10-31, Gmail)
- Oct 30: Metricool could not publish one Instagram post: "The Instagram account is restricted." Later Instagram posts published fine on Oct 31, so it looks lifted; watch for repeats.
- Oct 30: Meta rejected the boosted credit report post (Discriminatory Practices policy). Credit is a special ad category on Meta; the paid Credit Agent is retired. Do not boost credit posts.
- Oct 31 11:32 ART: TikTok new login alert from Safari, Buenos Aires (Seb's own setup; informational).
- Support agent run Oct 31 19:10 UTC: incidents recorded inc:email:1a18dab9 (SEV-2 Metricool/IG restricted post), inc:email:1a18e451 + inc:email:1a18e44f (SEV-2 credit ad rejected). Oct 30-31 logins (Google, Kit, Metricool, Porkbun, Meta password change) all iOS/Argentina during setup: SEV-3 informational, not recorded.
## Support this week
- 0 buyer emails (no orders yet). Oct 31 run: 0 cases, 0 drafted, 0 escalated.

## Daily Pulse 2026-11-01 (08:20 ART)
- Health: 0 failing checks, all 12 checkouts ok. Open incidents: the 3 Oct 30 email SEV-2s above (known). inc:page:home:2026-10-31 resolved by probe but its alert line stays sent:false (never messaged, resolved, no action).
- Metricool: 0 unapproved pending posts (all post cutoff pending posts are in the approved set). 2 Threads ERRORs on the Binance news carousel (00:52, 00:59 ART), reposted fine at 07:40.
- ONE CHANGE: refresh.yml now skips the Threads key refresh while config/threads.json says paused (the Sunday job failed red with 'Cannot parse access token' because get_token() returns None when paused). Test added.
- For the operator: tests/test_revenue_engine.py::test_guide_pages_build_reproducibly fails on main (before this run): the site builder would swap the /g/subs and /g/refund topcard videos to subs-leak.mp4 / refund-fighter.mp4 and touch sitemap.xml. Either rebuild and commit the guide pages (campaign approval covers site pushes) or pin the builder to the current videos. Daily Pulse did not touch live pages.
- support_agent heartbeat is late (16.1h vs 16h limit, SEV-3).
