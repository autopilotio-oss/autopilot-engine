# Approvals queue
Items here are built but not public. Seb approves or rejects. Workers release only items marked APPROVED.

## 2026-10-31 · lower-agent · Lower Bills Agent ($10 prompt kit)
What: compares internet, phone and insurance offers like for like, writes call scripts, drafts bank fee refund requests. Replaced the retired Credit Agent.
Gate score (honest): demand 1 (common need, no linked evidence yet) · fit 2 · value 2 (free guide works without paying) · better than free results 1 · safe 2 · measurable 1 (no target set yet) = 9/12, below the 10 bar.
Already inside the $39 All 6 bundle (file swapped in on Oct 31). Standalone listing held as a draft.
Status: REJECTED by Seb Oct 31 ("drop it"). Removed from bundle, guide and keywords.

## 2026-10-31 · refund-v2 · Improved REFUND free guide (fix to a live seller's guide, no new product)
What: rewrite of /g/refund/ so the card dispute step actually protects the reader: written billing error letter to the billing inquiries address, 60 days from the first statement, certified mail, 30/90 day issuer deadlines, hold the disputed amount; new copyable FCBA letter prompt that also computes the deadline; flight step now lists every DOT "significant change" trigger and the automatic refund; debit card 60 day warning; removed the unsourced "gets results far more often" line.
Why now: the refund-dd Threads post (Nov 3 12:30 ET) sends people to this guide, and the live version only says "dispute with your card issuer within 60 days", which misses the written notice that federal rights depend on (FTC, CFPB).
QA: all pass, see config/qa/2026-10-31-refund-v2.md (sources opened, no dashes, no promises, reader reviews and sends everything, 5 prompts tested on a synthetic case, disclaimer present). Kit PDF unchanged.
Preview: docs/g/refund-v2/index.html (noindex, not linked, not in sitemap) · cover: none (no new product, live refund cover unchanged).
On APPROVED: copy G["refund-v2"] fields over G["refund"] in tools/guides/guides.py (drop draft/base), delete the refund-v2 entry and docs/g/refund-v2/, rebuild.
Status: APPROVED by Seb Oct 31, RELEASED Oct 31 (live at /g/refund/)

## 2026-10-31 · lead-followup-pro · Lead Follow-Up Pro ($99 Claude Skill test) · IDEA GATE ONLY, nothing built
What: installable Claude Skill that sorts a business's leads by urgency, drafts follow-ups for the owner to approve, and keeps a tracker.
Evidence:
- Problem is real: 36% of customers say they wouldn't rehire a small business because it was slow or hard to reach (HoneyBook + Harris Poll, 503 owners and 1,002 customers, released May 2026) https://news.honeybook.com/news/honeybook-research-poor-communication-top-reason-customers-leave-small-businesses
- Owners on the job can't reply fast ("the plumber is under a sink when the lead comes in", r/Entrepreneur, Mar 2026)
- But free and cheap versions already exist: free follow-up skills (e.g. humanizerai follow-up skill, 204 installs) https://claudemarketplaces.com/skills/humanizerai/agent-skills/follow-up ; Anthropic's free Sales plugin; Gumroad follow-up kits at $5 to $19 (e.g. https://workdash.gumroad.com/l/plug-and-ping-email-prompts , https://munemomark.gumroad.com/l/pwpmkg)
Score: demand 2 · fit 1 (our audience is mostly consumers; The Workspace $49 already includes a Follow up agent, so this would compete with our own product) · free value 1 · better than free 0 · safe 2 · measurable 2 = 8/12 with a zero.
Result: FAILS the gate. Not recommended. Better move: sell the follow-up job through The Workspace we already have.
Status: NOT PITCHED FOR BUILD


## 2026-10-31 Deposit Agent (deposit-agent)
Problem: landlords keep part of security deposits; renters need to sort deductions and ask in writing.
Gate: 11/12 {"real_problem": 2, "honest_claim": 2, "easy_to_run": 2, "fits_brand": 2, "sellable": 2, "not_done_before": 1}
Evidence: NY AG recoveries (2022, 2023), Gothamist Dec 2024 (nearly 5,000 NY complaints), California Courts self help guide.
QA: PASS (scripts/revenue/quality.py). Kit PDF, cover, guide and demo video checked by eye.
Preview: docs/g/deposit/ (noindex draft), docs/store/deposit-cover.png, docs/media/demo/deposit-agent.mp4
Note: built under the Oct 31 "fully automatic" decision, then put back to draft by Revenue Engine 2.0 (paid publication needs approval). Posts for it are scheduled Nov 1 (TikTok + IG 10:30 ET, X 11:30 ET) and Nov 2 (Threads 11:00 ET); they point to the free guide only.
Approve: python3 scripts/revenue/release.py deposit-agent --approved-by "Seb, <date>"
Status: APPROVED (Seb (Oct 31 chat: finish everything yourself)), RELEASED 2026-10-31
