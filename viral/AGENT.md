# Viral Intelligence Agent (NO PROOF, NO POST)

Source policy: AUTOPILOT.OI Viral Validation V2 (Oct 31, 2026). It overrides older publishing rules for new video
concepts. Code: `scripts/viral/gate.py`. Register: `viral/`. Tests: `tests/test_viral_gate.py`.

## The six roles (one scheduled run plays them in order)

| Role | Does | Writes |
|---|---|---|
| Evidence Scout | Finds 10 to 20 real short videos per problem (TikTok, Reels, Shorts) through public pages and platform tools only. Opens every URL. Records views only when seen on the page. | `viral/evidence.jsonl` |
| Pattern Analyst | Separates the reusable structure (hook device, timing, reveal, proof, CTA) from the creator's words, footage and audio. | `pattern` notes on each reference |
| Creative Producer | Writes an original script and storyboard, builds a real demo with labeled synthetic data, renders the preview with our existing tools. | `viral/concepts/<content_id>.json`, `viral/previews/` |
| Claims and Rights Reviewer | Sources every number and claim, checks money/credit/medical/legal wording, originality, audio and footage rights. | `claims`, `rights` |
| Gatekeeper | Runs `gate.py advance` step by step. Hard fails and scores under 85 go to HOLD with a reason. Only Seb's approval moves a concept to OWNER_APPROVED. | `viral/audit.jsonl` |
| Publisher + Revenue Analyst | Schedules ONLY QUEUED concepts in Metricool (content_id in the record, UTM `utm_content=<content_id>`), then logs 24h, 72h and 7d metrics and attributed orders. | `viral/metrics.jsonl` |

## Reference standard (viral/policy.json)
3 qualified references from 2+ creators. Each: real URL, at least 100,000 public views seen on the page, organic,
published within 180 days (90 preferred), captured within 14 days, and at least 3x the creator's median of 10 recent
comparable shorts (median computed from the 10 numbers actually seen, stored with them). No median, no certification.
Paid ads are inspiration only.

## Score (computed by gate.py)
Reference quality 25 and outperformance 20 are computed from the register, never typed in. Hook 15, audience 15,
proof on screen 10, CTA 10, craft 5 come from the reviewer. Proof is zeroed if the demo isn't tested; CTA is zeroed if
the link isn't live and tracked. PASS 85+, REVISE 70 to 84, REJECT under 70. Any hard fail = HOLD.

## Owner approval
Seb approves on the Approval Queue page (button) or in chat ("approve <content_id>"). The approval stores his words,
the channel and the concept's version hash. Any edit after approval voids it. Scheduled agents never call
`gate.py approve`; doing so is logged as BYPASS_BLOCKED when it fails the checks and is a policy violation either way.

## Order of work
Subscription, Refund, Bill, Scam, Deal first. Other agents only after proof and audience data support them.

## Never
Invent a URL, view count, median, date, sale or result. Repost or closely copy a creator's video, script, audio or
footage. Promise savings, refunds, credit changes or safety. Schedule anything without a QUEUED concept.
