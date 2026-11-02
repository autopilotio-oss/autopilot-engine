# Front Desk Kit: owner usability test (Workstream B)

Goal: 3 independent service business owners go from receipt to a first useful draft **without help**. This is a free product test, kept separate from paid sales; testers are never counted as customers or revenue.

## Who qualifies
Owner operated service business (detailing, cleaning, lawn, handyman, trades) that answers customer messages themselves and sends quotes. Not a friend of the brand who will be polite; someone with real messages to answer this week.

## How they get the kit (no self purchase)
Seb creates a 100% off Gumroad offer code limited to 3 uses (Gumroad → Products → Front Desk Kit → Offer codes), or uses Gumroad's test purchase. These orders are $0 and the ledger excludes them from revenue.

## The test (30 to 45 minutes, owner on their own phone or computer)
1. Open the receipt email and download the PDF.
2. Follow page 2 exactly. Do not explain steps unless they are stuck for more than 3 minutes; note where.
3. Finish the interview and setup.
4. Paste one real customer message from this week and type `reply`.
5. Owner rates the draft: would you send it as is / with small edits / no.

## Record one row per tester in `sales/activations.csv`
`date, offer_id=front_desk_kit, order_ref=test-01, source=usability_test, activated=yes|no, minutes_to_first_draft, stuck_at, note`

## Pass bar (before any paid traffic)
- 3 of 3 reach a valid draft from a real message
- Setup time measured (replaces the "about 30 minutes" estimate on the page)
- Every place someone got stuck is fixed in the PDF and re-tested

## Ask each tester (optional, with consent)
- May we screen record the reply step for the product page? (Real recording replaces nothing fake; nothing is published without their OK.)
- Would you have paid $39 for this? Why or why not? (Log the answer as the objection.)
