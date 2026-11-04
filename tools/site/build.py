"""AUTOPILOT.OI site v2: home, /marketplace, /workspace (software), redirects. python3 tools/site/build.py
Product pages (/store/<slug>, /office-autopilot) stay where they are; this only builds the top level pages."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); D = f"{ROOT}/docs"
e = html.escape; GR = "https://autopilotoi.gumroad.com/l/"
def head(title, desc, path, img="autopilot-cover.png"):  # share image: the product the page sells
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="https://autopilotoi.app{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://autopilotoi.app/store/{img}">
<meta name="theme-color" content="#050605"><link rel="icon" href="/logo-128.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,500;14..32,600;14..32,700;14..32,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v=3"></head><body>"""
def nav(on):
    a = lambda href, t, k: f'<a href="{href}"{" class=\"on\"" if k == on else ""}>{t}</a>'
    return f'<div class="nav"><div class="wrap"><a class="brand" href="/"><span class="eyes"><i></i><i></i></span>AUTOPILOT.OI</a><div class="links">{a("/#tools", "Tools", "m")}{a("/front-desk/", "Front Desk", "f")}{a("/brain/", "Free starter", "c")}</div></div></div>'
FOOT = """<div class="foot"><div class="wrap"><div>AUTOPILOT.OI · simple AI helpers for business owners<br>Independent. Not affiliated with Anthropic. Claude is a product of Anthropic.</div>
<div style="display:flex;gap:18px;flex-wrap:wrap"><a href="/marketplace/">Marketplace</a><a href="/workspace/">Workspace</a><a href="/brain/">Free starter</a><a href="/library/">Library</a><a href="https://www.instagram.com/autopilot.oi/">Instagram</a></div></div></div>
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
 ("Bookkeeping Sorter", "10", "bookkeeping-sorter", "books", "Upload your bank statement, type sort. Each expense sorted into a category with totals, and a quick question when it isn't sure.", "sort", "A shoebox of receipts in April", "Totals every month, one table for your accountant"),
 ("Invoice Chaser", "10", "invoice-chaser", "invoice", "Invoices from your job notes, and the right reminder for every customer who hasn't paid.", "chase Dave", "Staring at a text you don't want to send", "A kind reminder, ready to send"),
 ("Review Desk", "10", "review-desk", "reviews", "Paste a review, type reply. Warm thank yous, calm answers to angry ones, in your voice.", "reply", "Reviews sitting unanswered for months", "Every review answered in your voice"),
 ("Content Week", "10", "content-week", "content", "Answer 5 questions on Sunday. Get 7 posts: what to shoot, the caption, the hashtags.", "week", "\"What do I even post?\"", "7 posts planned from your real week"),
]
def tool_cards():
    c = "".join(f'<div class="card prod"><img src="/store/{im}-cover.png" alt="{e(n)}" style="width:100%;border-radius:12px;margin-bottom:14px"><h3 style="font-size:23px">{e(n)}</h3><div class="price">${p}<small>one time</small></div><p>{e(d)}</p><p class="label" style="margin-top:6px">YOU TYPE: {e(cmd)}</p><div class="ba"><div class="b"><span>BEFORE</span>{e(bf)}</div><div class="a"><span>AFTER</span>{e(af)}</div></div><div style="display:flex;gap:10px;margin-top:auto;padding-top:12px"><a class="btn buy" style="flex:1;height:48px" href="{GR}{perm}">Get it · ${p}</a></div></div>' for n, p, perm, im, d, cmd, bf, af in TOOLS)
    return c
HSTYLE = """<style>.phn{max-width:360px;margin:0 auto;background:#0b0d0b;border:1px solid var(--line);border-radius:36px;padding:22px 18px;box-shadow:0 50px 120px rgba(0,0,0,.6),0 0 90px rgba(198,255,61,.07)}
.phn .t{font:600 12px/1 ui-monospace,monospace;letter-spacing:.14em;color:#8b918a;display:flex;justify-content:space-between;margin-bottom:16px}
.phn .me{margin-left:auto;max-width:80%;background:#262a24;border-radius:18px 18px 4px 18px;padding:10px 14px;font-size:15px;margin-bottom:12px;width:max-content}
.phn .ai{background:rgba(198,255,61,.09);border:1px solid rgba(198,255,61,.45);border-radius:18px 18px 18px 4px;padding:12px 14px;font-size:14.5px;line-height:1.5}
.phn .ai b{display:block;font:600 11px/1 ui-monospace,monospace;letter-spacing:.14em;color:#C6FF3D;margin-bottom:8px}
.phn .r{display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,.07);padding:5px 0}
.cp{background:#0d0f0c;border:2px dashed rgba(198,255,61,.5);border-radius:18px;padding:18px;white-space:pre-wrap;font:14px/1.6 ui-monospace,monospace;color:#e9ffd0}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}.ba div{border-radius:12px;padding:10px 12px;font-size:13.5px;line-height:1.4}.ba .b{background:#1a1514;border:1px solid #3a2a26;color:#d8b8ae}.ba .a{background:rgba(198,255,61,.07);border:1px solid rgba(198,255,61,.35)}
.ba span{display:block;font:600 10px/1 ui-monospace,monospace;letter-spacing:.14em;margin-bottom:6px;opacity:.8}</style>"""
def home():
    return head("AUTOPILOT.OI · AI helpers for busy business owners. No tech skills.", "Simple AI helpers for owners who have never used AI: bookkeeping, invoices, reviews, posts and customer replies. Copy one message, answer a few questions. From $10.", "/", "toolkit-cover.png") + nav("") + f"""
{HSTYLE}
<div class="wrap hero grid2" style="align-items:center;gap:40px"><div><div class="k"><b>AUTOPILOT.OI</b> · for owners who have never used AI</div>
<h1 style="margin:18px 0 22px">You didn't start a business<br>to do <em>paperwork at midnight.</em></h1>
<p class="lead">Simple AI helpers for the busywork that eats your week: bookkeeping, invoices, reviews, posts and customer replies. Copy one message, answer a few easy questions, then type one word. It writes. You stay in charge. From $10.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px"><a class="btn buy" href="#tools">See the tools</a><a class="btn ghost" href="#free">Try one free</a></div></div>
<div class="phn"><div class="t"><span>BOOKKEEPING</span><span>EXAMPLE</span></div><div class="me">sort 📎 october.pdf</div>
<div class="ai"><b>OCTOBER · SORTED</b><div class="r"><span>Supplies</span><span>$612</span></div><div class="r"><span>Gas and car</span><span>$388</span></div><div class="r"><span>Software</span><span>$74</span></div><div class="r"><span>Advertising</span><span>$150</span></div><div class="r"><span>Personal</span><span>$219</span></div>
<div style="margin-top:10px">1 question: Home Depot $64 on Oct 12, work or home?</div></div></div></div>
<div class="sec" id="how"><div class="wrap"><div class="k" style="margin-bottom:14px">Never used AI? Perfect.</div><h2 style="margin-bottom:30px">Three steps. <em>On your phone.</em></h2>
<div class="grid3"><div class="card"><h3>1. Get the free Claude app</h3><p style="margin-top:10px">Claude is an AI assistant, like a smart helper you text. The free plan works. Make a free account at claude.ai.</p></div>
<div class="card"><h3>2. Paste one message</h3><p style="margin-top:10px">Your tool comes with a guide. You copy one message into Claude and it asks you 7 easy questions about your business. About 15 minutes, tap by tap.</p></div>
<div class="card"><h3>3. Type one word</h3><p style="margin-top:10px">sort, chase, reply, week. It does the busywork from your real prices and rules. You read it and send it yourself.</p></div></div></div></div>
<div class="sec" id="free"><div class="wrap grid2" style="align-items:center;gap:40px"><div><div class="k" style="margin-bottom:14px">Free · 60 seconds</div><h2>Try one <em>right now.</em></h2><p class="lead" style="margin-top:14px">Open the free Claude app, tap New chat, paste this and fill in the brackets with a real review of your business. That's what using AI feels like. Our tools do this for every job, already set up with your business.</p>
<button class="btn" style="margin-top:22px" onclick="navigator.clipboard.writeText(document.getElementById('fp').innerText);this.textContent='Copied'">Copy the message</button></div>
<div class="cp" id="fp">Here is a review of my business. Write a short reply I can post.
My business: [name and what you do]
My name: [your first name]
The review: [paste it]
Keep it warm and real, 2 to 3 sentences. Don't make up any details.</div></div></div>
<div class="sec" id="tools"><div class="wrap"><div class="k" style="margin-bottom:14px">The tools</div><h2 style="margin-bottom:30px">Pick the job you hate most. <em>$10.</em></h2>
<div class="grid2">{tool_cards()}</div>
<div class="card prod" style="margin-top:22px;border-color:rgba(198,255,61,.45)"><span class="tagline live">Best value</span><h3 style="font-size:28px;margin-top:10px">The Owner Toolkit: all 4 tools</h3><div class="price">$24<small>one time · $40 separately</small></div><p>Bookkeeping Sorter, Invoice Chaser, Review Desk and Content Week. Each has its own setup helper.</p><a class="btn buy" style="margin-top:14px;height:52px" href="{GR}owner-toolkit">Get all 4 · $24</a></div>
<div class="card prod" style="margin-top:22px"><span class="tagline live">For service businesses that text all day</span><h3 style="font-size:28px;margin-top:10px">Front Desk Kit</h3><div class="price">$39<small>one time</small></div><p>Customer replies, quotes and follow ups, drafted in your voice from your real prices. Built for detailers, cleaners, landscapers and every business that answers texts all day.</p><div style="display:flex;gap:10px;margin-top:14px"><a class="btn buy" style="flex:1;height:52px" href="{GR}autopilot">Get it · $39</a><a class="btn ghost" style="height:52px" href="/front-desk/">Details</a></div></div></div></div>
<div class="sec"><div class="wrap"><h2 style="margin-bottom:16px">Questions</h2>
<details><summary>What is Claude?</summary><p>Claude is an AI assistant made by Anthropic. You type to it like a text conversation and it writes back. Our tools are guides that set Claude up to do one job for your business. We're independent and not affiliated with Anthropic.</p></details>
<details><summary>Do I have to pay for Claude?</summary><p>No. Every tool works on the free Claude plan. A paid plan gives you more room if you use it a lot.</p></details>
<details><summary>I'm not good with tech. Can I really do this?</summary><p>That's who we built these for. The guide walks you through every tap, and if you get stuck you type "I'm stuck" and describe your screen. Still stuck? Reply to your receipt email and we'll help.</p></details>
<details><summary>Does it send messages or post for me?</summary><p>No. Everything is a draft. You read it, then you send or post it yourself. Nothing goes out without you.</p></details>
<details><summary>Is my information safe?</summary><p>Never paste card numbers, bank account numbers or passwords into any AI. Black out full account numbers on statements before you upload. Your chats live in your own Claude account.</p></details>
<details><summary>What if it doesn't work for me?</summary><p>30 day refund. Reply to your Gumroad receipt and you get your money back.</p></details></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center"><div><span class="tagline dev">Coming soon</span><h2 style="margin:16px 0 14px">Want it done <em>for you?</em></h2><p class="lead">We're building a done for you setup and Workspace, software that answers new leads while you're on a job. Not on sale yet. Join the list and you hear first.</p><a class="btn ghost" style="margin-top:24px" href="/workspace/#list">Join the waitlist</a></div>
<div class="card"><div class="k" style="margin-bottom:10px">Free · 2 minutes</div><h3>Not ready to buy?</h3><p style="margin-top:10px">Get the free Front Desk Starter: one message that turns Claude into a front desk for your business.</p><a class="btn" style="margin-top:16px" href="/brain/">Get the free starter</a></div></div></div>""" + FOOT

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
    cards = "".join(f'<div class="card prod"><span class="tagline live">Setup kit</span><h3 style="font-size:23px">{e(n)}</h3><div class="price">${p}<small>one time</small></div><p>{e(d)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in li)}</ul><div style="display:flex;gap:10px;margin-top:auto;padding-top:10px"><a class="btn buy" style="flex:1;height:48px" href="{g}">Get it · ${p}</a><a class="btn ghost" style="height:48px" href="{u}">Details</a></div></div>' for n, p, u, g, d, li in PRODUCTS)
    soon = "".join(f'<div class="card"><span class="tagline dev">Coming soon</span><h3 style="margin:14px 0 8px">{e(n)}</h3><p>{e(d)}</p></div>' for n, d in SOON)
    return head("Marketplace · AI setup kits for small businesses · AUTOPILOT.OI", "Guided setup kits that install AI into your own Claude account. They draft; you decide and send. One time price, 30 day refund.", "/marketplace/") + nav("m") + f"""
<div class="wrap hero"><div class="k"><b>Marketplace</b> · setup kits</div><h1 style="margin:18px 0 22px">Simple AI tools.<br><em>No tech skills.</em></h1>
<p class="lead">Each kit is a guided setup for your own Claude account, built around a short interview about your business. It drafts; you decide and send. One time price. Not working for you within 30 days? Reply to your receipt for a full refund.</p></div>
<div class="wrap" style="padding-bottom:70px"><div class="grid3">{cards}</div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:14px">Next in the Marketplace</div><div class="grid3">{soon}</div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center"><div><span class="tagline dev">In development</span><h2 style="margin:16px 0 14px">Want it to run <em>without opening Claude?</em></h2><p class="lead">Kits draft when you ask. Workspace, our software, will catch the lead while you're on a job and have the reply waiting. Kit buyers get their purchase credited to the first month.</p><a class="btn" style="margin-top:24px" href="/workspace/">See Workspace</a></div>{INBOX}</div></div>""" + FOOT

def workspace():
    return head("Workspace · every lead answered · AUTOPILOT.OI", "Software for owner operated service businesses: every new lead answered within a minute, replies and quotes drafted, quiet quotes followed up. In development; founding spots open.", "/workspace/", "workspace-founding-cover.png") + nav("w") + f"""
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
redirect("/check/", "/brain/"); redirect("/store/", "/library/")  # old store links (Kit money and TikTok emails) land on the full catalog
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import frontdesk
write("/front-desk/", frontdesk.page(head, nav, FOOT))
for _v in ("after-hours", "demo"): write(frontdesk.VARIANTS[_v]["path"], frontdesk.page(head, nav, FOOT, _v))
import fdguides
for _g in fdguides.GUIDES: write(f"/guides/{_g['slug']}/", fdguides.page(_g, head, nav, FOOT))
redirect("/autopilot/", "/front-desk/"); redirect("/store/autopilot/", "/front-desk/")
print("site built")
