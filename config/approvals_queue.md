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
Status: AWAITING APPROVAL
