"""AUTOPILOT.OI site v2: home, /marketplace, /workspace (software), redirects. python3 tools/site/build.py
Product pages (/store/<slug>, /office-autopilot) stay where they are; this only builds the top level pages."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); D = f"{ROOT}/docs"
e = html.escape; GR = "https://autopilotoi.gumroad.com/l/"
def head(title, desc, path, img="autopilot-cover.png"):  # share image: the product the page sells
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="https://autopilotoi.app{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://autopilotoi.app/store/{img}">
<meta name="theme-color" content="#0a0a0a"><link rel="icon" href="/logo-128.png">
<link rel="preload" href="/assets/fonts/APWide-Black.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=4"></head><body>"""
def nav(on):
    a = lambda href, t, k, c="": f'<a href="{href}" class="{c}{" on" if k == on else ""}">{t}</a>'
    return f'<div class="nav"><div class="wrap"><a class="brand" href="/"><span class="eyes"><i></i><i></i></span>AUTOPILOT.OI</a><div class="links">{a("/front-desk/", "Front Desk", "f", "hm")}{a("/brain/", "Free starter", "c")}{a("/#tools", "Tools", "m", "cta")}</div></div></div>'
FOOT = """<div class="foot"><div class="wrap"><div class="big">AUTOPILOT<span>.</span>OI</div>
<div><div>Simple AI helpers for business owners.<br>Independent. Not affiliated with Anthropic. Claude is a product of Anthropic.</div>
<div style="display:flex;gap:18px;flex-wrap:wrap"><a href="/marketplace/">Marketplace</a><a href="/front-desk/">Front Desk</a><a href="/workspace/">Workspace</a><a href="/brain/">Free starter</a><a href="/library/">Library</a><a href="https://www.instagram.com/autopilot.oi/">Instagram</a></div></div></div></div>
<script src="/assets/ap.js" defer></script></body></html>"""
def redirect(path, to):
    os.makedirs(f"{D}{path}", exist_ok=True)
    open(f"{D}{path}index.html", "w").write(f'<!DOCTYPE html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="https://autopilotoi.app{to}"><meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}"+location.search)</script><a href="{to}">Continue</a>')
def write(path, s): os.makedirs(f"{D}{path}", exist_ok=True); open(f"{D}{path}index.html", "w").write(s)

INBOX = """<div class="ui"><div class="bar"><span>Leads · today</span><span>Product preview</span></div>
<div class="row"><div class="av">DR</div><div class="t"><b>Dana R.</b><span>How much for a full detail on an SUV? Free Saturday?</span></div><span class="st g">REPLIED 0:48</span></div>
<div class="row"><div class="av">MT</div><div class="t"><b>Mark T.</b><span>Ceramic coating, 2022 Tacoma</span></div><span class="st g">QUOTE READY</span></div>
<div class="row"><div class="av">PS</div><div class="t"><b>Priya S.</b><span>Quote sent Tuesday, no reply</span></div><span class="st">FOLLOW UP · DAY 2</span></div>
<div class="draft"><div class="label" style="margin-bottom:10px">DRAFT FOR DANA · WAITING FOR YOU</div><div class="msg">How much for a full detail on an SUV? Free Saturday?</div>
<div class="dr">A full SUV detail is $250, about 3 hours, and we come to you. I have Saturday at 9 or 1. Want me to hold one?</div><div class="acts"><span>Edit</span><span class="ok">Approve & send</span></div></div>
<div class="label" style="margin-top:12px;text-align:center">Example business. Workspace is in development.</div></div>"""

TOOLS = [
 ("Bookkeeping Sorter", "10", "bookkeeping-sorter", "Upload your bank statement. Every charge goes into a category, with monthly totals. It asks when it isn't sure.", "sort", "Messy receipts"),
 ("Invoice Chaser", "10", "invoice-chaser", "Writes the invoice from your job notes, and a polite reminder for anyone who hasn't paid.", "chase Dave", "Unpaid invoices"),
 ("Review Desk", "10", "review-desk", "Writes a reply to every review in your voice, including the angry ones.", "reply", "Ignored reviews"),
 ("Content Week", "10", "content-week", "Answer 5 questions on Sunday. Get 7 posts for the week, captions included.", "week", "Nothing to post"),
]
def tool_cards():
    return "".join(f'<div class="tc"><div class="tc-top"><span>0{i}</span><span>${p}</span></div><h3 class="tc-pb">{e(pb)}</h3><div class="tc-nm">{e(n)}</div><p class="tc-d">{e(d)}</p><div class="cmd">You type <b>{e(cmd)}</b></div><a class="btn dark buy" href="{GR}{perm}">Get it · ${p}</a></div>' for i, (n, p, perm, d, cmd, pb) in enumerate(TOOLS, 1))
FACTS = [("$10", "one payment per tool"), ("$0", "monthly fees"), ("Free", "Claude plan works"), ("30 days", "money back")]
HSTYLE = """<style>.phn{max-width:360px;margin-left:auto;width:100%;background:#111;border:1px solid var(--line);border-radius:28px;padding:22px 18px}
.phn .t{font:600 11px/1 var(--T);letter-spacing:.16em;color:var(--mut);display:flex;justify-content:space-between;gap:12px;margin-bottom:16px;text-transform:uppercase}
.phn .me{margin-left:auto;max-width:80%;background:#242424;border-radius:16px 16px 4px 16px;padding:9px 14px;font-size:15px;margin-bottom:12px;width:max-content}
.phn .ai{background:#171717;border:1px solid #2c2c2c;border-radius:16px 16px 16px 4px;padding:14px;font-size:14.5px;line-height:1.5}
.phn .ai b{display:block;font:600 11px/1 var(--T);letter-spacing:.16em;color:var(--mut);margin-bottom:10px}
.phn .r{display:flex;justify-content:space-between;border-bottom:1px solid #262626;padding:6px 0;font-variant-numeric:tabular-nums}
.phn .q{margin-top:12px;padding:10px 12px;border-radius:10px;background:rgba(212,255,58,.1);color:#e9ffc2;font-size:14px}
.hgrid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(300px,.75fr);gap:64px;align-items:center}.hgrid h1{font-size:clamp(36px,5.2vw,70px)}
@media(max-width:900px){.hgrid{grid-template-columns:1fr;gap:44px}.hgrid h1{font-size:clamp(36px,10vw,76px)}.phn{margin:0 auto}}
.facts{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.facts div{padding:30px 20px;border-left:1px solid var(--line)}.facts div:first-child{border-left:0;padding-left:0}
.facts b{display:block;font:400 clamp(26px,3.2vw,40px)/1 var(--W);letter-spacing:-.02em;color:var(--tx)}.facts span{display:block;margin-top:10px;font:500 14px var(--T);color:var(--mut)}
@media(max-width:820px){.facts{grid-template-columns:1fr 1fr}.facts div{padding:22px 0 22px 18px}.facts div:nth-child(odd){border-left:0;padding-left:0}.facts div:nth-child(n+3){border-top:1px solid var(--line)}}
.tools{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.tc{display:grid;grid-row:span 6;grid-template-rows:subgrid;row-gap:0;background:#fff;border:1px solid #dcdcd5;border-radius:20px;padding:24px}
.tc-top{display:flex;justify-content:space-between;font:600 13px var(--T);color:#77776f;padding-bottom:18px;margin-bottom:22px;border-bottom:1px solid #e6e6e0;font-variant-numeric:tabular-nums}
.tc-pb{font:400 clamp(20px,1.9vw,26px)/1.02 var(--W);text-transform:uppercase;letter-spacing:-.02em}
.tc-nm{font:600 13px var(--T);letter-spacing:.1em;text-transform:uppercase;color:#77776f;margin:12px 0 14px}
.tc-d{font-size:15px;color:#3b3b36;line-height:1.5}
.tc .cmd{margin:18px 0 22px;color:#77776f}.tc .btn{width:100%;align-self:end}
@media(max-width:1000px){.tools{grid-template-columns:1fr 1fr}}@media(max-width:560px){.tools{grid-template-columns:1fr}}
.kit{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.kit>*{min-width:0}@media(max-width:820px){.kit{grid-template-columns:1fr}}
.kc{display:flex;flex-direction:column;border-radius:20px;padding:28px;border:1px solid #dcdcd5;background:#fff}.kc.dk{background:var(--ink);border-color:var(--ink);color:var(--tx)}
.kc .k{margin-bottom:14px}.kc h3{font:400 clamp(24px,2.6vw,32px)/1 var(--W);text-transform:uppercase;letter-spacing:-.02em}
.kc p{margin:14px 0 24px;font-size:15px;color:#3b3b36;max-width:460px}.kc.dk p{color:#b9b9b2}.kc .row{margin-top:auto}.kc .row .btn{flex:1}.kc .row .btn.ghost{flex:none}</style>"""
def home():
    facts = "".join(f"<div><b>{e(v)}</b><span>{e(t)}</span></div>" for v, t in FACTS)
    return head("AUTOPILOT.OI · $10 AI tools for the paperwork you put off", "Four simple tools for small business owners: bookkeeping, invoices, reviews and posts. They run in the free Claude app and draft the work; you check and send. $10 each, one payment, 30 day refund.", "/", "toolkit-cover.png") + nav("") + f"""
{HSTYLE}
<div class="wrap hero hgrid"><div><div class="k">For small business owners</div>
<h1 style="margin:22px 0 26px">Hate paperwork? <em>$10 fixes it.</em></h1>
<p class="lead">Four simple tools for the jobs you put off: receipts, invoices, reviews and posts. They run in the free Claude app. You check every draft and send it yourself.</p>
<div class="row" style="margin-top:34px"><a class="btn buy" href="#tools">See the tools</a><a class="btn ghost" href="#free">Try one free</a></div></div>
<div class="phn"><div class="t"><span>Bookkeeping Sorter</span><span>Example</span></div><div class="me">sort · october.pdf</div>
<div class="ai"><b>October, sorted</b><div class="r"><span>Supplies</span><span>$612</span></div><div class="r"><span>Gas and car</span><span>$388</span></div><div class="r"><span>Software</span><span>$74</span></div><div class="r"><span>Advertising</span><span>$150</span></div><div class="r"><span>Personal</span><span>$219</span></div>
<div class="q">Home Depot, $64 on Oct 12: work or home?</div></div></div></div>
<div class="wrap"><div class="facts">{facts}</div></div>
<div class="sec paper" id="tools" style="margin-top:96px"><div class="wrap"><div class="head"><div><div class="k" style="margin-bottom:16px">The tools</div><h2>Four problems. <em>Four $10 fixes.</em></h2></div><p class="lead" style="max-width:340px">Pay once and keep it. No subscription, no setup fee.</p></div>
<div class="tools">{tool_cards()}</div>
<div class="kit"><div class="kc dk"><div class="k">Best value</div><h3>All four for <em style="font-style:normal;color:var(--l)">$24</em></h3><p>Bookkeeping, invoices, reviews and posts. That's $6 a tool instead of $40.</p><div class="row"><a class="btn buy" href="{GR}owner-toolkit">Get all four · $24</a></div></div>
<div class="kc"><div class="k">For businesses that text all day</div><h3>Front Desk Kit · $39</h3><p>Drafts replies, quotes and follow ups to customer texts from your real prices.</p><div class="row"><a class="btn dark buy" href="{GR}autopilot">Get it · $39</a><a class="btn ghost" href="/front-desk/">Details</a></div></div></div></div></div>
<div class="sec" id="how"><div class="wrap"><div class="k" style="margin-bottom:16px">Setup</div><h2 style="margin-bottom:48px">Ready in about <em>15 minutes.</em></h2>
<div class="steps"><div><h3>Open Claude</h3><p style="color:var(--mut)">Free app or claude.ai. The free plan works.</p></div>
<div><h3>Paste one message</h3><p style="color:var(--mut)">It asks a few questions about your business.</p></div>
<div><h3>Type one word</h3><p style="color:var(--mut)">Read the draft. Send it yourself.</p></div></div></div></div>
<div class="sec" id="free"><div class="wrap grid2" style="align-items:center;gap:64px"><div><div class="k" style="margin-bottom:16px">Free · 60 seconds</div><h2>Try one <em>free.</em></h2><p class="lead" style="margin-top:20px">Paste this into Claude with a real review of your business. It writes the reply.</p>
<button class="btn" style="margin-top:28px" onclick="navigator.clipboard.writeText(document.getElementById('fp').innerText);this.textContent='Copied'">Copy the message</button></div>
<div class="cp" id="fp">Here is a review of my business. Write a short reply I can post.
My business: [name and what you do]
My name: [your first name]
The review: [paste it]
Keep it warm and real, 2 to 3 sentences. Don't make up any details.</div></div></div>
<div class="sec"><div class="wrap grid2" style="gap:64px"><div><h2>Before you <em>buy.</em></h2><p class="lead" style="margin-top:20px">Stuck after you buy? Reply to your receipt and we help.</p></div><div>
<details><summary>What is Claude?</summary><p>An AI assistant made by Anthropic. You text it and it writes back. Our tools set it up to do one job for your business.</p></details>
<details><summary>Do I have to pay for Claude?</summary><p>No. Every tool works on the free plan.</p></details>
<details><summary>Does it send or post for me?</summary><p>No. Everything is a draft. You send it yourself.</p></details>
<details><summary>Is my information safe?</summary><p>Never paste card numbers, account numbers or passwords into any AI. Your chats stay in your own Claude account.</p></details>
<details><summary>What if it doesn't work for me?</summary><p>30 day refund. Reply to your Gumroad receipt.</p></details></div></div></div>""" + FOOT

PRODUCTS = [
 ("Front Desk Kit", "39", "/front-desk/", GR + "autopilot", "Customer replies, quotes and follow ups, drafted in your voice from your real prices.", ["15 question business interview", "Reply, quote, chase, review, FAQ, plan week", "3 extra systems built for your business", "Free Claude plan works"]),
 ("Bookkeeping Sorter", "10", "/#tools", GR + "bookkeeping-sorter", "Upload a statement, type sort. Each expense sorted into a category, with totals.", ["Setup helper, tap by tap", "Monthly and yearly totals", "Asks when it isn't sure", "Free Claude plan works"]),
 ("Invoice Chaser", "10", "/#tools", GR + "invoice-chaser", "Invoices from job notes and the right reminder for every late customer.", ["Setup helper, tap by tap", "Owed list", "Friendly to firm reminders", "Free Claude plan works"]),
 ("Review Desk", "10", "/#tools", GR + "review-desk", "Replies to every review in your voice, and the text that asks for new ones.", ["Setup helper, tap by tap", "Calm replies to bad reviews", "Never fake reviews", "Free Claude plan works"]),
 ("Content Week", "10", "/#tools", GR + "content-week", "5 questions on Sunday, 7 posts for the week.", ["Setup helper, tap by tap", "What to shoot, captions, hashtags", "Replies to comments", "Free Claude plan works"]),
 ("Owner Toolkit", "24", "/#tools", GR + "owner-toolkit", "All 4 tools: bookkeeping, invoices, reviews and posts. $40 separately.", ["4 setup helpers", "Works in the free Claude app", "You send everything", "30 day refund"]),
]
SOON = [("Done for you setup", "We set up your tools with your real prices and test them on your real messages."), ("Workspace", "Software that answers new leads while you are on a job. In development."), ("More tools", "Tell us the job you hate most. Reply to any receipt.")]
def marketplace():
    cards = "".join(f'<div class="card prod"><div class="nm">{e(n)}</div><div class="price">${p}<small>one time</small></div><p>{e(d)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in li[:3])}</ul><div class="go row"><a class="btn dark buy" style="flex:1" href="{g}">Get it · ${p}</a><a class="btn ghost" href="{u}">Details</a></div></div>' for n, p, u, g, d, li in PRODUCTS)
    soon = "".join(f'<div class="card"><span class="tagline dev">Coming soon</span><h3 style="margin:16px 0 8px">{e(n)}</h3><p>{e(d)}</p></div>' for n, d in SOON)
    return head("Marketplace · AI setup kits for small businesses · AUTOPILOT.OI", "Guided setup kits that install AI into your own Claude account. They draft; you decide and send. One time price, 30 day refund.", "/marketplace/") + nav("m") + f"""
<div class="wrap hero"><div class="k">Marketplace</div><h1 style="margin:22px 0 24px">Every tool. <em>From $10.</em></h1>
<p class="lead">Setup kits for your own Claude account. It drafts; you send. 30 day refund.</p></div>
<div class="sec paper"><div class="wrap"><div class="grid3">{cards}</div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Next</div><h2 style="margin-bottom:36px">Coming <em>soon.</em></h2><div class="grid3">{soon}</div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development</span><h2 style="margin:20px 0 18px;font-size:clamp(28px,3.9vw,50px)">Answers leads <em>while you work.</em></h2><p class="lead">Workspace, our software, in development. It catches new leads and has the reply ready for your tap.</p><a class="btn" style="margin-top:28px" href="/workspace/">See Workspace</a></div>{INBOX}</div></div>""" + FOOT

def workspace():
    return head("Workspace · every lead answered · AUTOPILOT.OI", "Software for owner operated service businesses: every new lead answered within a minute, replies and quotes drafted, quiet quotes followed up. In development; founding spots open.", "/workspace/", "workspace-founding-cover.png") + nav("w") + f"""
<div class="wrap hero grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development · founding spots open</span>
<h1 class="s" style="margin:22px 0 24px">Answers new leads <em>while you're on a job.</em></h1>
<p class="lead">Software we're building for service businesses. New leads get your acknowledgment within a minute; the reply and quote are drafted from your prices. You approve from your phone.</p>
<div class="row" style="margin-top:30px"><a class="btn buy" href="{GR}workspace-founding">Hold a founding spot · $49</a><a class="btn ghost" href="#list">Join the free list</a></div>
<p class="label" style="margin-top:14px">Deposit fully refundable · credited to your first month · $99 a month planned</p></div>{INBOX}</div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">How it will work</div><h2 style="margin-bottom:44px">How it <em>will work.</em></h2>
<div class="steps"><div><h3>Connect your line</h3><p style="color:var(--mut)">Phone line and form email. Quo (formerly OpenPhone) first.</p></div>
<div><h3>Teach it your business</h3><p style="color:var(--mut)">A 15 question interview. You write the one acknowledgment it may send.</p></div>
<div><h3>Approve with a tap</h3><p style="color:var(--mut)">Reply and quote drafted. Approve, edit or skip.</p></div></div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Permissions</div><h2 style="margin-bottom:36px">What it can <em>and can't do.</em></h2>
<div class="perm"><div class="card"><h3>It reads</h3><ul><li>New calls and texts on the line you connect</li><li>Lead emails you forward</li><li>Your calendar's free times (read only)</li></ul></div>
<div class="card"><h3>It sends on its own</h3><ul><li>Only your acknowledgment, written and approved by you</li><li>Nothing else</li></ul></div>
<div class="card"><h3>It always waits for you</h3><ul><li>Replies, quotes and follow ups</li><li>Anything with a price or a promise</li><li>Every message is logged where you can see it</li></ul></div></div></div></div>
<div class="sec paper"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Founding members</div><h2 style="font-size:clamp(28px,3.6vw,46px)">Hold a spot. <em>$49, refundable.</em></h2><p class="lead" style="margin-top:14px">Fully refundable, and credited to your first month.</p></div>
<div class="card"><div class="prod"><ul><li>$49 credited to your first paid month</li><li>First access to the beta, in the order you joined</li><li>$99 a month locked for your first 12 months</li><li>A say in what gets built first</li><li>Refund anytime before your first paid month; full refund if it's not open to founding members by Feb 28, 2027</li></ul><a class="btn dark buy" style="margin-top:18px" href="{GR}workspace-founding">Hold a founding spot · $49</a></div></div></div></div>
<div class="sec" id="list"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Free list</div><h2>Join the <em>free list.</em></h2><p class="lead" style="margin-top:14px">Free. Three questions tell us what to build first.</p></div>
<form class="form" id="wl"><input type="email" name="email_address" required placeholder="Your email" autocomplete="email">
<select name="fields[trade]" required><option value="">What kind of business?</option><option>Auto detailing</option><option>Cleaning</option><option>Landscaping or lawn</option><option>Handyman or home repair</option><option>HVAC, plumbing or electrical</option><option>Pressure washing</option><option>Other service business</option></select>
<select name="fields[leads_per_week]" required><option value="">New leads per week?</option><option>Under 5</option><option>5 to 15</option><option>16 to 40</option><option>More than 40</option></select>
<select name="fields[phone_system]" required><option value="">Business phone?</option><option>My cell phone</option><option>Quo (OpenPhone)</option><option>Google Voice</option><option>RingCentral or other VoIP</option><option>Other</option></select>
<button class="btn" type="submit">Join the list</button><p class="label" id="wlm">No spam. Unsubscribe anytime.</p></form></div></div>
<div class="sec"><div class="wrap grid2" style="gap:44px"><div><h2>Questions<em>.</em></h2></div><div>
<details><summary>Can I use Workspace today?</summary><p>Not yet. It's in development. Founding members get the beta first. Until then, the Front Desk Kit in our Marketplace drafts replies and quotes inside your own Claude account.</p></details>
<details><summary>What will it cost?</summary><p>$99 a month is the planned price. Founding members lock $99 for 12 months and get their $49 deposit credited to the first month.</p></details>
<details><summary>Will it text my customers on its own?</summary><p>Only the acknowledgment you write and approve during setup. Replies, quotes and follow ups always wait for your tap.</p></details>
<details><summary>Which phone systems will it work with?</summary><p>We plan to start with Quo (formerly OpenPhone). Tell us yours in the list form above; the answers decide what we connect next.</p></details>
<details><summary>How do refunds work?</summary><p>Reply to your Gumroad receipt anytime before your first paid month for the full $49. If Workspace isn't open to founding members by February 28, 2027, every deposit is refunded.</p></details></div></div></div>
<script>document.getElementById('wl').addEventListener('submit',function(ev){{ev.preventDefault();var f=new FormData(this);f.append('fields[source]','workspace_list');fetch('https://app.kit.com/forms/10118407/subscriptions',{{method:'POST',body:f,mode:'no-cors'}}).finally(function(){{document.getElementById('wlm').textContent="You're on the list. Check your email to confirm.";}});try{{if(window.fbq)fbq('track','Lead',{{content_name:'workspace_list'}})}}catch(e){{}};try{{if(window.goatcounter)goatcounter.count({{path:'optin/workspace-list',event:true}})}}catch(e){{}}}});</script>""" + FOOT

write("/", home()); write("/marketplace/", marketplace()); write("/workspace/", workspace())
redirect("/check/", "/brain/"); redirect("/store/", "/library/")  # old store links (Kit money and TikTok emails) land on the full catalog
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import frontdesk
write("/front-desk/", frontdesk.page(head, nav, FOOT))
for _v in ("after-hours", "demo"): write(frontdesk.VARIANTS[_v]["path"], frontdesk.page(head, nav, FOOT, _v))
import fdguides
for _g in fdguides.GUIDES: write(f"/guides/{_g['slug']}/", fdguides.page(_g, head, nav, FOOT))
redirect("/autopilot/", "/front-desk/"); redirect("/store/autopilot/", "/front-desk/")
print("site built")
