# Decision log (approvals, vetoes, standing permissions)

| Date (ART) | Decision | By | Scope | Expiry |
|---|---|---|---|---|
| 2026-10-31 15:18 | "Nothing gets scheduled without verified evidence, an 85/100 quality score, and my approval." | Seb (chat) | All public content | Standing |
| 2026-10-31 15:41 | "Keep publishing approval-based until I explicitly authorize a standing autopublishing policy." | Seb (chat) | All public content | Until Seb authorizes autopublishing |
| 2026-10-31 15:41 | "Send one concise weekly performance report. Interrupt me only for critical failures, security concerns, required authorization, or spending decisions." | Seb (chat) | Owner messages | Standing |
| 2026-10-31 15:41 | "Never assume approval for spending, production deployments, public publishing, or sensitive customer actions." | Seb (chat) | All workers | Standing |
| 2026-10-31 | Cutover executed: publishing workers moved to drafts; 13 not yet scheduled posts held in queue/hold/2026-10-31-cutover.json; 13 posts already in Metricool before the cutover left as scheduled (legacy) | Claude, per the two instructions above | Scheduled tasks + queue | Rollback: growth-os/rollback/ |
| 2026-10-31 15:00 | "Figure out how to finish everything yourself" (Workspace rebuilt and queued, Deposit released, attribution live) | Seb (chat) | Revenue Engine 2.0 open items | Done |
| 2026-10-31 15:52 | Usage tools budget: $30 a month ($1/day soft, $2/day hard, 1 preview render a day) | Seb (chat) | ElevenLabs renders, paid APIs | Until changed |
| 2026-10-31 15:52 | Keep the 13 posts scheduled in Metricool before the cutover | Seb (chat) | Legacy posts Nov 1 to 3 | One time |
| 2026-10-31 15:52 | GitHub issue alerts confirmed received | Seb (chat) | Alert channel 1 | Standing |
| 2026-10-31 15:52 | Seb will connect Gmail so the support agent can draft replies (drafts only) | Seb (chat) | Support inbox | Standing |
| 2026-10-31 15:56 | "Use Gmail for this": Gmail connected; Support + inbox monitor runs with Gmail (drafts only, alerts as incidents) | Seb (chat) | Business inbox | Standing |
| 2026-10-31 15:56 | "TikTok is good now": voice fix confirmed on the subs repost | Seb (chat) | TikTok video rule | Standing |
| 2026-11-01 07:40 | Flagship reels subs-leak and refund-fighter passed the gate (93, 92) and were scheduled after the last queued reel (Nov 3 20:30, Nov 4 12:30 ART); bundle reel charged-twice moved up to render Nov 2 with bill-coach | operator, campaign standing approval | queue/freel | Campaign |
| 2026-11-01 10:25 | Containment: scripts/daily_stories.py writes the auto story batch to queue/hold/ (drafts); today's 5 stories moved there. Clears SEV-1 viral_queue_guard (issue #4). Reverse: change the path back and git mv the file | Monthly Review, under the standing NO PROOF + approval-only publishing instructions | Daily stories Action | Until Seb says revert |
| 2026-11-01 10:25 | Recorded Meta Ads spend Oct 30 $9.56 + Oct 31 $22.47 (boost 'If you answer the same customer...', ACTIVE) as spend.recorded events. Not paused: pause or continue is Seb's call | Monthly Review | costs ledger | One time |

- 2026-11-01 14:40 ART: Seb approved the shift plan ("Yeah"). New scheduled tasks: Hourly analyst (read only, writes the HQ feed), Draft factory (carousel bank every 2h, never posts), Site improver (one tested fix every 3h, approval window Nov 1 to 10, never prices). News Desk step 6 now uses a banked prompts post first. HQ page shows 24 agents incl. 8 GitHub workers via scripts/growthos/hq_feed.py. Rollback: disable the three tasks.
