"""Product pages for the store: docs/store/<slug>/index.html.
One page per product people are most likely to buy. Each page: who it's for, a sample output from a test run on
made-up data (labelled), what it does and doesn't do, what you need, FAQ, one checkout button.
Run: python3 tools/store/pages.py"""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
e = html.escape
GR = "https://autopilotoi.gumroad.com/l/"

FAQ_COMMON = [
    ("Is this an app?", "No. It's a PDF prompt kit. You paste the master prompt into a Claude Project once, then run it whenever you need it."),
    ("Do I need a paid Claude plan?", "No. Claude's free plan works and lets you create up to 5 Projects. A paid plan gives you more usage."),
    ("Can it log into my accounts or send things for me?", "No. It reads what you upload and drafts. You check it, decide and send."),
    ("What about my private info?", "Black out full account, card and member numbers before you upload. Claude only needs merchant names, dates and amounts."),
]

P = {
 "subs": dict(
  name="Subscription Agent", price="$10", buy="subs-agent", kw="SUBS", guide="subs",
  title="Find every subscription you pay for",
  lead="Upload 2 to 3 months of statements. Claude lists every recurring charge, helps you sort keep and cut, and drafts the cancel messages. Do a sweep once a month and new charges don't slip by.",
  who=["You pay for apps, streaming or trials you've lost track of", "You want one clear list with the yearly cost of each", "You'd rather not write cancel emails yourself"],
  sample_note="Sample output from a test run on made-up statements. Your results depend on your statements.",
  sample_head=["Merchant", "Amount", "Every", "Yearly"],
  sample_rows=[["NETFLIX.COM", "$17.99", "Month", "$215.88"], ["SPOTIFY USA", "$11.99", "Month", "$143.88"],
               ["ADOBE PHOTO", "$19.99", "Month", "$239.88"], ["PLANET FIT", "$15.00", "Month", "$180.00"],
               ["APPLE.COM/BILL", "$6.99", "Month", "$83.88"], ["APPLE.COM/BILL", "$2.99", "Month", "$35.88"],
               ["AMZN PRIME", "$139.00", "Year", "$139.00"]],
  sample_after=["Total: $74.95 a month plus $139 a year, about $1,038 a year.", "Flags: two Apple charges (check Settings, then Subscriptions) and the photo plan went up in month 3. Then it asks which ones you still use.",
                "Cancel draft: \"Please cancel my Photography plan under this email, effective today, stop all future charges and confirm in writing.\""],
  does=["Finds recurring charges, even with odd merchant names", "Builds your keep and cut list with yearly costs", "Drafts cancel and refund messages", "Flags new charges and price changes when you upload new statements"],
  doesnt=["Cancel anything for you", "See your bank account", "Guarantee a refund"],
  need=["2 to 3 months of bank and card statements (PDF or CSV)", "A Claude account (free works)", "About 15 minutes"],
  faq=[("How is this different from the free guide?", "The free guide gives you the prompts to do one sweep. The kit adds a deeper master prompt, 5 starter prompts (cancel, still charged, cheaper plan, free trial guard, monthly sweep) and a tracker, set up once in a Claude Project.")],
 ),
 "bill": dict(
  name="Bill Agent", price="$10", buy="bill-agent", kw="BILL", guide="bill",
  title="Check a medical bill before you pay it",
  lead="Upload your itemized bill and your insurer's explanation of benefits. Claude lines them up, points out what doesn't match, and writes your call script so you know exactly what to ask.",
  who=["You got a medical or dental bill and aren't sure it's right", "The bill doesn't match what your insurance says you owe", "You want a script before you call the billing office"],
  sample_note="Sample output from a test run on a made-up bill and EOB. Your results depend on your documents.",
  sample_head=["Line", "Billed", "EOB says", "Ask"],
  sample_rows=[["Office visit", "$310.00", "You owe $40 copay", "Why am I billed more than my copay?"], ["Lab panel, twice same day", "$96 x2", "Listed once", "Is this a duplicate charge?"],
               ["Facility fee", "$185.00", "Not listed", "Was this sent to my insurance?"], ["Total due", "$687.00", "Your share $63.40", "Can you rebill to match the EOB?"]],
  sample_after=["Call script opener: \"Hi, I'm calling about my bill from [date]. Before I pay, I'd like to review a few lines that don't match my insurance statement.\"",
                "It also reminds you to ask whether the hospital has a financial assistance policy, and to get any agreement in writing."],
  does=["Compares your bill to your EOB line by line", "Lists questions and possible errors in a table", "Writes your call script and follow up email", "Keeps a log of every bill until it's settled"],
  doesnt=["Call anyone for you", "Give medical or legal advice", "Guarantee a lower bill"],
  need=["Your itemized bill (ask the billing office for it)", "The EOB from your insurer for that visit", "A Claude account (free works)"],
  faq=[("What if I don't have an itemized bill?", "Call the billing office and ask for one with every charge and its billing code. The kit includes the exact words to use.")],
 ),
 "money": dict(
  name="All 5 Money Agents", price="$39", buy="all-money-agents", kw=None, guide=None,
  title="All 5 Money Agents",
  lead="Five Claude prompt kits for the money jobs most people put off: medical bills, card debt, subscriptions, refunds and raises. $50 separately, $39 together.",
  who=["You want one place to handle bills, debt and refunds with Claude", "You'll use at least 3 of the 5", "You like having the exact prompt ready when something comes up"],
  sample_note="Sample output from the Subscription Agent, from a test run on made-up statements.",
  sample_head=["Merchant", "Amount", "Every", "Yearly"],
  sample_rows=[["NETFLIX.COM", "$17.99", "Month", "$215.88"], ["ADOBE PHOTO", "$19.99", "Month", "$239.88"], ["PLANET FIT", "$15.00", "Month", "$180.00"], ["AMZN PRIME", "$139.00", "Year", "$139.00"]],
  sample_after=["Then it asks which ones you still use and drafts the cancel messages for the rest."],
  does=["Bill Agent: checks a medical bill against your insurance", "Debt Agent: payoff plan and the script to ask for a lower rate", "Subscription Agent: lists every recurring charge, drafts cancel messages", "Refund Agent: drafts refund requests that name your rights", "Raise Agent: pay data, your number and a practice run"],
  doesnt=["Log into your accounts", "Send messages or make calls for you", "Give financial or legal advice or guarantee results"],
  need=["A Claude account (the free plan's 5 Projects fit all 5)", "The documents for whichever job you're doing", "About 10 minutes to set up each one"],
  faq=[("Can I start with one?", "Yes. Every kit is $10 on its own, and every one has a free guide you can try first.")],
 ),
}

def page(slug, p):
    rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in p["sample_rows"])
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"] + FAQ_COMMON)
    free = f'<p class="free">Not ready to buy? <a href="/g/{p["guide"]}/">Try the free guide first</a>.</p>' if p["guide"] else '<p class="free">Not ready to buy? <a href="/free/">Every kit has a free guide</a>.</p>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(p['name'])} · {p['price']} · AUTOPILOT.OI</title>
<meta name="description" content="{e(p['lead'])}">
<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['lead'])}">
<meta property="og:image" content="https://autopilotoi.app/logo.png"><link rel="canonical" href="https://autopilotoi.app/store/{slug}/">
<meta name="theme-color" content="#000000"><link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,500;14..32,600;14..32,700;14..32,900&display=swap" rel="stylesheet">
<style>
:root{{--l:#D4FF3A;--line:#1c1d1b;--mut:#8f928b;--card:#0c0d0c}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{overflow-x:hidden}}
body{{background:#000;color:#fff;font:500 16px/1.55 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}.w{{max-width:560px;margin:0 auto;padding:0 20px 60px;position:relative;z-index:1}}
.glow{{position:fixed;width:520px;height:520px;left:50%;margin-left:-260px;top:-300px;border-radius:50%;background:rgba(212,255,58,.15);filter:blur(100px);pointer-events:none}}
.hd{{display:flex;align-items:center;gap:10px;padding:20px 0}}.hd img{{width:34px;height:34px;border-radius:50%}}.hd b{{font-weight:900;letter-spacing:.04em}}.hd a.bk{{margin-left:auto;color:var(--mut);font-size:14px;text-decoration:none}}
.tag{{font:700 11px 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:var(--l)}}
h1{{font:900 clamp(34px,9vw,48px)/.98 Inter;text-transform:uppercase;letter-spacing:-.02em;margin:10px 0 14px}}
.lead{{color:rgba(255,255,255,.8);font-size:17px}}
.buy{{display:block;text-align:center;background:var(--l);color:#000;text-decoration:none;font:900 16px Inter;text-transform:uppercase;border-radius:16px;padding:18px;margin:22px 0 8px}}
.sm{{text-align:center;color:var(--mut);font-size:13px}}
h2{{font:900 13px 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);margin:34px 0 12px}}
ul{{padding-left:20px}}li{{margin:6px 0}}
.box{{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px}}
.note{{font-size:13px;color:var(--mut);margin-bottom:10px}}
.tbl{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font:400 12.5px 'Space Mono',monospace}}
th{{text-align:left;color:var(--l);font-weight:700;border-bottom:1px solid #2a2d27;padding:6px 6px 6px 0;white-space:nowrap}}td{{border-bottom:1px solid #1a1c19;padding:7px 6px 7px 0;vertical-align:top}}
.after p{{margin-top:10px;font-size:14.5px;color:rgba(255,255,255,.85)}}
.two{{display:grid;grid-template-columns:1fr;gap:12px}}.no li::marker{{content:"✕  ";color:#ff6b6b}}.yes li::marker{{content:"✓  ";color:var(--l)}}
details{{border-bottom:1px solid var(--line);padding:12px 0}}summary{{font-weight:700;cursor:pointer}}details p{{color:rgba(255,255,255,.75);margin-top:6px;font-size:15px}}
.free{{text-align:center;margin-top:14px;color:var(--mut)}}.free a{{color:var(--l)}}
.ft{{color:#5d6059;font-size:12px;text-align:center;margin-top:36px}}
</style><link rel="stylesheet" href="/assets/brand.css"></head><body><div class="glow"></div><div class="w">
<div class="hd"><a href="/"><img src="/logo.png" alt=""></a><b>AUTOPILOT.OI</b><a class="bk" href="/store/">← Store</a></div>
<div class="tag">Claude prompt kit · {p['price']}</div>
<h1>{e(p['title'])}</h1>
<p class="lead">{e(p['lead'])}</p>
<a class="buy" href="{GR}{p['buy']}">Get the {e(p['name'])} · {p['price']}</a>
<p class="sm">Instant download · works on Claude's free plan</p>
<h2>It's for you if</h2><ul>{li(p['who'])}</ul>
<h2>What it looks like</h2><div class="box"><p class="note">{e(p['sample_note'])}</p>
<div class="tbl"><table><tr>{''.join(f'<th>{e(h)}</th>' for h in p['sample_head'])}</tr>{rows}</table></div>
<div class="after">{''.join(f'<p>{e(x)}</p>' for x in p['sample_after'])}</div></div>
<h2>What it does</h2><ul class="yes">{li(p['does'])}</ul>
<h2>What it doesn't do</h2><ul class="no">{li(p['doesnt'])}</ul>
<h2>What you need</h2><ul>{li(p['need'])}</ul>
<h2>What you get</h2><p>A PDF with the master prompt, 5 starter prompts, a 10 minute setup guide and a tracker{'' if slug != 'money' else ', for each of the 5 kits'}.</p>
<h2>Questions</h2>{faq}
<a class="buy" href="{GR}{p['buy']}">Get the {e(p['name'])} · {p['price']}</a>
{free}
<div class="ft">Education only, not financial, legal or medical advice. AUTOPILOT.OI is independent and not affiliated with Anthropic. Claude is a product of Anthropic.</div>
</div><script src="/assets/ap.js" defer></script></body></html>"""

for slug, p in P.items():
    d = os.path.join(ROOT, "docs", "store", slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(page(slug, p)); print("built store/" + slug)
