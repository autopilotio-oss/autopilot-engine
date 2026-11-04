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
 ("Bookkeeping Sorter", "10", "bookkeeping-sorter", "books", "Upload a statement. Each expense sorted with totals; it asks when unsure.", "sort"),
 ("Invoice Chaser", "10", "invoice-chaser", "invoice", "Invoices from job notes, and a kind reminder for anyone late.", "chase Dave"),
 ("Review Desk", "10", "review-desk", "reviews", "Warm replies to good reviews, calm ones to angry reviews.", "reply"),
 ("Content Week", "10", "content-week", "content", "5 questions on Sunday. 7 posts for the week.", "week"),
]
def tool_cards():
    return "".join(f'<div class="card prod"><img src="/store/{im}-cover.png" alt="{e(n)}" loading="lazy" style="width:100%;border-radius:14px;margin-bottom:6px"><div class="nm">{e(n)}</div><p>{e(d)}</p><div class="cmd">You type <b>{e(cmd)}</b></div><div class="go"><a class="btn dark buy" href="{GR}{perm}">Get it · ${p}</a></div></div>' for n, p, perm, im, d, cmd in TOOLS)
HSTYLE = """<style>.phn{max-width:360px;margin:0 auto;background:#0d0d0d;border:1px solid var(--line);border-radius:36px;padding:22px 18px;box-shadow:0 50px 120px rgba(0,0,0,.6),0 0 120px rgba(212,255,58,.06)}
.phn .t{font:600 11.5px/1 var(--T);letter-spacing:.18em;color:var(--mut);display:flex;justify-content:space-between;gap:12px;margin-bottom:16px}
.phn .me{margin-left:auto;max-width:80%;background:#262626;border-radius:18px 18px 4px 18px;padding:10px 14px;font-size:15px;margin-bottom:12px;width:max-content}
.phn .ai{background:rgba(212,255,58,.08);border:1px solid rgba(212,255,58,.45);border-radius:18px 18px 18px 4px;padding:12px 14px;font-size:14.5px;line-height:1.5}
.phn .ai b{display:block;font:600 11px/1 var(--T);letter-spacing:.16em;color:var(--l);margin-bottom:8px}
.phn .r{display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.07);padding:5px 0}
.hgrid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(320px,.8fr);gap:48px;align-items:center}.hgrid h1{font-size:clamp(34px,5.4vw,72px)}@media(max-width:900px){.hgrid h1{font-size:clamp(34px,8.6vw,72px)}}@media(max-width:900px){.hgrid{grid-template-columns:1fr}}
.kit{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}@media(max-width:820px){.kit{grid-template-columns:1fr}}</style>"""
WORDS = ["sort", "chase", "reply", "week", "quote", "sort", "chase", "reply", "week", "quote"]
def home():
    band = "".join(f"<span>{w}</span>" for w in WORDS * 2)
    return head("AUTOPILOT.OI · AI helpers for busy business owners. No tech skills.", "Simple AI helpers for owners who have never used AI: bookkeeping, invoices, reviews, posts and customer replies. Copy one message, answer a few questions. From $10.", "/", "toolkit-cover.png") + nav("") + f"""
{HSTYLE}
<div class="wrap hero hgrid"><div><div class="k"><b>●</b> AI helpers for business owners</div>
<h1 style="margin:22px 0 24px">No more paperwork <em>at midnight.</em></h1>
<p class="lead">Copy one message into the free Claude app. Type one word. It drafts the busywork; you check it and send it. From $10.</p>
<div class="row" style="margin-top:32px"><a class="btn buy" href="#tools">See the tools</a><a class="btn ghost" href="#free">Try one free</a></div></div>
<div class="phn"><div class="t"><span>BOOKKEEPING</span><span>EXAMPLE</span></div><div class="me">sort 📎 october.pdf</div>
<div class="ai"><b>OCTOBER · SORTED</b><div class="r"><span>Supplies</span><span>$612</span></div><div class="r"><span>Gas and car</span><span>$388</span></div><div class="r"><span>Software</span><span>$74</span></div><div class="r"><span>Advertising</span><span>$150</span></div><div class="r"><span>Personal</span><span>$219</span></div>
<div style="margin-top:10px">1 question: Home Depot $64 on Oct 12, work or home?</div></div></div></div>
<div class="band" aria-hidden="true"><div class="tr">{band}</div></div>
<div class="sec paper" id="tools"><div class="wrap"><div class="head"><div><div class="k" style="margin-bottom:16px">The tools</div><h2>One job. <em>$10.</em></h2></div><p class="lead" style="max-width:380px">Pick the paperwork you hate most. One time price, 30 day refund.</p></div>
<div class="grid4">{tool_cards()}</div>
<div class="kit"><div class="card prod" style="background:var(--ink);color:var(--tx);border-color:var(--ink)"><span class="tagline live" style="border-color:#333;color:#cfcfc8">Best value</span><div class="nm" style="font-size:clamp(24px,3vw,34px)">Owner Toolkit</div><div class="price" style="color:var(--l)">$24<small style="color:#a2a39a">all 4 · $40 separately</small></div><p style="color:#bdbdb6">Bookkeeping, invoices, reviews and posts.</p><div class="go"><a class="btn buy" href="{GR}owner-toolkit">Get all 4 · $24</a></div></div>
<div class="card prod"><span class="tagline live">For businesses that text all day</span><div class="nm" style="font-size:clamp(24px,3vw,34px)">Front Desk Kit</div><div class="price">$39<small>one time</small></div><p>Customer replies, quotes and follow ups, drafted from your real prices.</p><div class="go row"><a class="btn dark buy" style="flex:1" href="{GR}autopilot">Get it · $39</a><a class="btn ghost" href="/front-desk/">Details</a></div></div></div></div></div>
<div class="sec" id="how"><div class="wrap"><div class="k" style="margin-bottom:16px">Never used AI? Good.</div><h2 style="margin-bottom:44px">Three steps. <em>On your phone.</em></h2>
<div class="steps"><div><h3>Get the free Claude app</h3><p style="color:var(--mut)">The free plan works.</p></div>
<div><h3>Paste one message</h3><p style="color:var(--mut)">It asks you a few easy questions about your business.</p></div>
<div><h3>Type one word</h3><p style="color:var(--mut)">sort, chase, reply, week. Read the draft. Send it yourself.</p></div></div></div></div>
<div class="sec" id="free"><div class="wrap grid2" style="align-items:center;gap:44px"><div><div class="k" style="margin-bottom:16px">Free · 60 seconds</div><h2>Try it <em>right now.</em></h2><p class="lead" style="margin-top:18px">Paste this into Claude with a real review of your business.</p>
<button class="btn" style="margin-top:26px" onclick="navigator.clipboard.writeText(document.getElementById('fp').innerText);this.textContent='Copied'">Copy the message</button></div>
<div class="cp" id="fp">Here is a review of my business. Write a short reply I can post.
My business: [name and what you do]
My name: [your first name]
The review: [paste it]
Keep it warm and real, 2 to 3 sentences. Don't make up any details.</div></div></div>
<div class="sec"><div class="wrap grid2" style="gap:44px"><div><h2>Questions</h2><p class="lead" style="margin-top:18px">Stuck? Reply to your receipt email and we help.</p><a class="btn ghost" style="margin-top:24px" href="/brain/">Get the free starter</a></div><div>
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
<div class="wrap hero"><div class="k"><b>●</b> Marketplace</div><h1 style="margin:22px 0 24px">Simple AI tools. <em>No tech skills.</em></h1>
<p class="lead">Each kit sets up your own Claude account for one job. It drafts; you send. One time price, 30 day refund.</p></div>
<div class="sec paper"><div class="wrap"><div class="grid3">{cards}</div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Next</div><h2 style="margin-bottom:36px">Coming <em>soon.</em></h2><div class="grid3">{soon}</div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development</span><h2 style="margin:20px 0 18px">Runs <em>without opening Claude.</em></h2><p class="lead">Workspace, our software, will catch the lead while you're on a job and have the reply waiting for your tap.</p><a class="btn" style="margin-top:28px" href="/workspace/">See Workspace</a></div>{INBOX}</div></div>""" + FOOT

def workspace():
    return head("Workspace · every lead answered · AUTOPILOT.OI", "Software for owner operated service businesses: every new lead answered within a minute, replies and quotes drafted, quiet quotes followed up. In development; founding spots open.", "/workspace/", "workspace-founding-cover.png") + nav("w") + f"""
<div class="wrap hero grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development · founding spots open</span>
<h1 class="s" style="margin:22px 0 24px">Every lead answered. <em>Every quote followed up.</em></h1>
<p class="lead">Software we're building for service businesses. New leads get your acknowledgment within a minute; the reply and quote are drafted from your prices. You approve from your phone.</p>
<div class="row" style="margin-top:30px"><a class="btn buy" href="{GR}workspace-founding">Hold a founding spot · $49</a><a class="btn ghost" href="#list">Join the free list</a></div>
<p class="label" style="margin-top:14px">Deposit fully refundable · credited to your first month · $99 a month planned</p></div>{INBOX}</div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">How it will work</div><h2 style="margin-bottom:44px">Set up <em>on your phone.</em></h2>
<div class="steps"><div><h3>Connect your line</h3><p style="color:var(--mut)">Phone line and form email. Quo (formerly OpenPhone) first.</p></div>
<div><h3>Teach it your business</h3><p style="color:var(--mut)">A 15 question interview. You write the one acknowledgment it may send.</p></div>
<div><h3>Approve with a tap</h3><p style="color:var(--mut)">Reply and quote drafted. Approve, edit or skip.</p></div></div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Permissions</div><h2 style="margin-bottom:36px">You decide what it can <em>touch.</em></h2>
<div class="perm"><div class="card"><h3>It reads</h3><ul><li>New calls and texts on the line you connect</li><li>Lead emails you forward</li><li>Your calendar's free times (read only)</li></ul></div>
<div class="card"><h3>It sends on its own</h3><ul><li>Only your acknowledgment, written and approved by you</li><li>Nothing else</li></ul></div>
<div class="card"><h3>It always waits for you</h3><ul><li>Replies, quotes and follow ups</li><li>Anything with a price or a promise</li><li>Every message is logged where you can see it</li></ul></div></div></div></div>
<div class="sec paper"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Founding members</div><h2>Hold your spot for <em>$49.</em></h2><p class="lead" style="margin-top:14px">Fully refundable, and credited to your first month.</p></div>
<div class="card"><div class="prod"><ul><li>$49 credited to your first paid month</li><li>First access to the beta, in the order you joined</li><li>$99 a month locked for your first 12 months</li><li>A say in what gets built first</li><li>Refund anytime before your first paid month; full refund if it's not open to founding members by Feb 28, 2027</li></ul><a class="btn dark buy" style="margin-top:18px" href="{GR}workspace-founding">Hold a founding spot · $49</a></div></div></div></div>
<div class="sec" id="list"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Free list</div><h2>Not ready to put money down?</h2><p class="lead" style="margin-top:14px">Join the list. Three quick questions tell us what to build first.</p></div>
<form class="form" id="wl"><input type="email" name="email_address" required placeholder="Your email" autocomplete="email">
<select name="fields[trade]" required><option value="">What kind of business?</option><option>Auto detailing</option><option>Cleaning</option><option>Landscaping or lawn</option><option>Handyman or home repair</option><option>HVAC, plumbing or electrical</option><option>Pressure washing</option><option>Other service business</option></select>
<select name="fields[leads_per_week]" required><option value="">New leads per week?</option><option>Under 5</option><option>5 to 15</option><option>16 to 40</option><option>More than 40</option></select>
<select name="fields[phone_system]" required><option value="">Business phone?</option><option>My cell phone</option><option>Quo (OpenPhone)</option><option>Google Voice</option><option>RingCentral or other VoIP</option><option>Other</option></select>
<button class="btn" type="submit">Join the list</button><p class="label" id="wlm">No spam. Unsubscribe anytime.</p></form></div></div>
<div class="sec"><div class="wrap grid2" style="gap:44px"><div><h2>Questions</h2></div><div>
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
