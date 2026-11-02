"""AUTOPILOT.OI site v2: home, /marketplace, /workspace (software), redirects. python3 tools/site/build.py
Product pages (/store/<slug>, /office-autopilot) stay where they are; this only builds the top level pages."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); D = f"{ROOT}/docs"
e = html.escape; GR = "https://autopilotoi.gumroad.com/l/"
def head(title, desc, path):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="https://autopilotoi.app{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://autopilotoi.app/store/workspace-founding-cover.png">
<meta name="theme-color" content="#050605"><link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,500;14..32,600;14..32,700;14..32,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=3"></head><body>"""
def nav(on):
    a = lambda href, t, k: f'<a href="{href}"{" class=\"on\"" if k == on else ""}>{t}</a>'
    return f'<div class="nav"><div class="wrap"><a class="brand" href="/"><span class="eyes"><i></i><i></i></span>AUTOPILOT.OI</a><div class="links">{a("/marketplace/", "Marketplace", "m")}{a("/workspace/", "Workspace", "w")}{a("/brain/", "Free check", "c")}</div></div></div>'
FOOT = """<div class="foot"><div class="wrap"><div>AUTOPILOT.OI · AI for the front office<br>Independent. Not affiliated with Anthropic. Claude is a product of Anthropic.</div>
<div style="display:flex;gap:18px;flex-wrap:wrap"><a href="/marketplace/">Marketplace</a><a href="/workspace/">Workspace</a><a href="/brain/">Free check</a><a href="/library/">Library</a><a href="https://www.instagram.com/autopilot.oi/">Instagram</a></div></div></div>
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

def home():
    return head("AUTOPILOT.OI · AI for the front office", "Setup kits you install in your own Claude account, and Workspace, the software we're building to answer every lead for you.", "/") + nav("") + f"""
<div class="wrap hero"><div class="k"><b>AUTOPILOT.OI</b> · AI for the front office</div>
<h1 style="margin:18px 0 22px">Your front office,<br><em>handled.</em> You stay in control.</h1>
<p class="lead">Setup kits that install AI into your business today, and Workspace, the software we're building to answer every lead while you work.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px"><a class="btn" href="/marketplace/">Browse the Marketplace</a><a class="btn ghost" href="/workspace/">See Workspace</a></div></div>
<div class="wrap" style="padding-bottom:84px"><div class="grid2">
<a class="card door" href="/marketplace/"><span class="tagline live">Available now</span><h2 style="font-size:34px">Marketplace</h2><p>Guided setup kits for your own Claude account: a front desk that drafts replies and quotes, an office of scheduled agents, a week of content. One time price, 30 day refund.</p><span class="label">SETUP KITS · FROM $10</span><span class="go">Browse kits →</span></a>
<a class="card door" href="/workspace/"><span class="tagline dev">In development · founding spots open</span><h2 style="font-size:34px">Workspace</h2><p>Software that catches every new lead, answers within a minute, drafts the reply and quote, and chases quiet quotes. One inbox you approve from your phone.</p><span class="label">SOFTWARE · $99 A MONTH PLANNED</span><span class="go">See Workspace →</span></a></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:14px">How we work</div><h2 style="margin-bottom:30px">Built to be <em>trusted</em> with real customers.</h2>
<div class="grid3"><div class="card"><h3>You approve what goes out</h3><p style="margin-top:10px">Our kits draft. Workspace drafts too, and only sends the one acknowledgment you write yourself.</p></div>
<div class="card"><h3>Clear labels</h3><p style="margin-top:10px">Every product says what it is: a setup kit that runs in your Claude account, or software we run. Nothing pretends to be more.</p></div>
<div class="card"><h3>Your prices, your rules</h3><p style="margin-top:10px">Everything starts from a short interview about your business. When information is missing it asks, instead of guessing.</p></div></div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center"><div><div class="k" style="margin-bottom:14px">Free · 2 minutes</div><h2>Where are your leads <em>leaking?</em></h2><p class="lead" style="margin-top:14px">Answer 10 questions and get your own AI front desk prompt, free.</p><a class="btn" style="margin-top:24px" href="/brain/">Start the free check</a></div>{INBOX}</div></div>""" + FOOT

PRODUCTS = [
 ("Front Desk Kit", "39", "/store/autopilot/", GR + "autopilot", "Customer replies, quotes and follow ups, drafted in your voice from your real prices.", ["15 question business interview", "Reply, quote, chase, review, FAQ, plan week", "3 extra systems built for your business", "Free Claude plan works"]),
 ("Office Autopilot", "79", "/office-autopilot/", GR + "workspace", "Seven scheduled Claude agents on your Gmail and Calendar: inbox, brief, bookings, follow ups.", ["Morning brief and inbox drafts", "Booking, follow up, invoice, review agents", "50 phone commands", "Needs a paid Claude plan"]),
 ("Video Agent", "10", "/store/video/", GR + "video-agent", "One idea into a week of short videos: hooks, scripts and a cut by cut edit plan.", ["5 hooks per idea", "Scripts in your voice", "CapCut edit plans", "Weekly numbers review"]),
]
SOON = [("Review Engine", "Review requests, replies to every review and Google Business Profile posts."), ("Local Content Week", "A week of videos and posts made for a local service business."), ("Owner's Bundle", "The core kits in one Project with one setup.")]
def marketplace():
    cards = "".join(f'<div class="card prod"><span class="tagline live">Setup kit</span><h3 style="font-size:23px">{e(n)}</h3><div class="price">${p}<small>one time</small></div><p>{e(d)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in li)}</ul><div style="display:flex;gap:10px;margin-top:auto;padding-top:10px"><a class="btn buy" style="flex:1;height:48px" href="{g}">Get it · ${p}</a><a class="btn ghost" style="height:48px" href="{u}">Details</a></div></div>' for n, p, u, g, d, li in PRODUCTS)
    soon = "".join(f'<div class="card"><span class="tagline dev">Coming soon</span><h3 style="margin:14px 0 8px">{e(n)}</h3><p>{e(d)}</p></div>' for n, d in SOON)
    return head("Marketplace · AI setup kits for small businesses · AUTOPILOT.OI", "Guided setup kits that install AI into your own Claude account. They draft; you decide and send. One time price, 30 day refund.", "/marketplace/") + nav("m") + f"""
<div class="wrap hero"><div class="k"><b>Marketplace</b> · setup kits</div><h1 style="margin:18px 0 22px">Install AI into your business,<br><em>in one evening.</em></h1>
<p class="lead">Each kit is a guided setup for your own Claude account, built around a short interview about your business. It drafts; you decide and send. One time price. Not working for you within 30 days? Reply to your receipt for a full refund.</p></div>
<div class="wrap" style="padding-bottom:70px"><div class="grid3">{cards}</div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:14px">Next in the Marketplace</div><div class="grid3">{soon}</div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center"><div><span class="tagline dev">In development</span><h2 style="margin:16px 0 14px">Want it to run <em>without opening Claude?</em></h2><p class="lead">Kits draft when you ask. Workspace, our software, will catch the lead while you're on a job and have the reply waiting. Kit buyers get their purchase credited to the first month.</p><a class="btn" style="margin-top:24px" href="/workspace/">See Workspace</a></div>{INBOX}</div></div>""" + FOOT

def workspace():
    return head("Workspace · every lead answered · AUTOPILOT.OI", "Software for owner operated service businesses: every new lead answered within a minute, replies and quotes drafted, quiet quotes followed up. In development; founding spots open.", "/workspace/") + nav("w") + f"""
<div class="wrap hero grid2" style="align-items:center;gap:40px"><div><span class="tagline dev">In development · founding spots open</span>
<h1 style="margin:20px 0 22px">Every lead answered.<br><em>Every quote followed up.</em></h1>
<p class="lead">Workspace is the software we're building for owner operated service businesses. New calls, texts and form leads get your acknowledgment within a minute. The real reply and quote are drafted from your prices, and quiet quotes get chased. You approve from your phone.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn buy" href="{GR}workspace-founding">Hold a founding spot · $49</a><a class="btn ghost" href="#list">Join the free list</a></div>
<p class="label" style="margin-top:14px">Deposit fully refundable · credited to your first month · $99 a month planned</p></div>{INBOX}</div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:14px">How it will work</div><h2 style="margin-bottom:30px">Ten minutes to set up. <em>On your phone.</em></h2>
<div class="steps"><div class="card"><h3>Connect your line</h3><p style="margin-top:10px">Your business phone line and your website form email. Planned first: Quo (formerly OpenPhone).</p></div>
<div class="card"><h3>Teach it your business</h3><p style="margin-top:10px">A 15 question interview: prices, rules, hours, how you talk. You write the one acknowledgment it may send for you.</p></div>
<div class="card"><h3>Approve with a tap</h3><p style="margin-top:10px">Each lead arrives with the reply and quote drafted. Approve, edit or skip. Follow ups queue themselves.</p></div></div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:14px">Permissions</div><h2 style="margin-bottom:30px">You decide what it can <em>touch.</em></h2>
<div class="perm"><div class="card"><h3>It reads</h3><ul><li>New calls and texts on the line you connect</li><li>Lead emails you forward</li><li>Your calendar's free times (read only)</li></ul></div>
<div class="card"><h3>It sends on its own</h3><ul><li>Only your acknowledgment, written and approved by you</li><li>Nothing else</li></ul></div>
<div class="card"><h3>It always waits for you</h3><ul><li>Replies, quotes and follow ups</li><li>Anything with a price or a promise</li><li>Every message is logged where you can see it</li></ul></div></div></div></div>
<div class="sec"><div class="wrap grid2"><div><div class="k" style="margin-bottom:14px">Founding members</div><h2>Hold your spot for <em>$49.</em></h2><p class="lead" style="margin-top:14px">Fully refundable, and credited to your first month.</p></div>
<div class="card"><div class="prod"><ul><li>$49 credited to your first paid month</li><li>First access to the beta, in the order you joined</li><li>$99 a month locked for your first 12 months</li><li>A say in what gets built first</li><li>Refund anytime before your first paid month; full refund if it's not open to founding members by Feb 28, 2027</li></ul><a class="btn buy" style="margin-top:16px" href="{GR}workspace-founding">Hold a founding spot · $49</a></div></div></div></div>
<div class="sec" id="list"><div class="wrap grid2"><div><div class="k" style="margin-bottom:14px">Free list</div><h2>Not ready to put money down?</h2><p class="lead" style="margin-top:14px">Join the list. Three quick questions tell us what to build first.</p></div>
<form class="form" id="wl"><input type="email" name="email_address" required placeholder="Your email" autocomplete="email">
<select name="fields[trade]" required><option value="">What kind of business?</option><option>Auto detailing</option><option>Cleaning</option><option>Landscaping or lawn</option><option>Handyman or home repair</option><option>HVAC, plumbing or electrical</option><option>Pressure washing</option><option>Other service business</option></select>
<select name="fields[leads_per_week]" required><option value="">New leads per week?</option><option>Under 5</option><option>5 to 15</option><option>16 to 40</option><option>More than 40</option></select>
<select name="fields[phone_system]" required><option value="">Business phone?</option><option>My cell phone</option><option>Quo (OpenPhone)</option><option>Google Voice</option><option>RingCentral or other VoIP</option><option>Other</option></select>
<button class="btn" type="submit">Join the list</button><p class="label" id="wlm">No spam. Unsubscribe anytime.</p></form></div></div>
<div class="sec"><div class="wrap"><h2 style="margin-bottom:16px">Questions</h2>
<details><summary>Can I use Workspace today?</summary><p>Not yet. It's in development. Founding members get the beta first. Until then, the Front Desk Kit in our Marketplace drafts replies and quotes inside your own Claude account.</p></details>
<details><summary>What will it cost?</summary><p>$99 a month is the planned price. Founding members lock $99 for 12 months and get their $49 deposit credited to the first month.</p></details>
<details><summary>Will it text my customers on its own?</summary><p>Only the acknowledgment you write and approve during setup. Replies, quotes and follow ups always wait for your tap.</p></details>
<details><summary>Which phone systems will it work with?</summary><p>We plan to start with Quo (formerly OpenPhone). Tell us yours in the list form above; the answers decide what we connect next.</p></details>
<details><summary>How do refunds work?</summary><p>Reply to your Gumroad receipt anytime before your first paid month for the full $49. If Workspace isn't open to founding members by February 28, 2027, every deposit is refunded.</p></details></div></div>
<script>document.getElementById('wl').addEventListener('submit',function(ev){{ev.preventDefault();var f=new FormData(this);f.append('fields[source]','workspace_list');fetch('https://app.kit.com/forms/10118407/subscriptions',{{method:'POST',body:f,mode:'no-cors'}}).finally(function(){{document.getElementById('wlm').textContent="You're on the list. Check your email to confirm.";}});try{{if(window.fbq)fbq('track','Lead',{{content_name:'workspace_list'}})}}catch(e){{}};try{{if(window.goatcounter)goatcounter.count({{path:'optin/workspace-list',event:true}})}}catch(e){{}}}});</script>""" + FOOT

write("/", home()); write("/marketplace/", marketplace()); write("/workspace/", workspace())
redirect("/check/", "/brain/"); redirect("/store/", "/marketplace/")
print("site built")
