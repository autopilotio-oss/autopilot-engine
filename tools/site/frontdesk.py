"""Hero funnel: /front-desk/ (Front Desk Kit). Reads config/offers.json so price, plan and refund copy can't drift.
Imported by tools/site/build.py."""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
e = html.escape
O = {o["id"]: o for o in json.load(open(f"{ROOT}/config/offers.json"))["offers"]}["front_desk_kit"]
PRICE = f"${O['price_cents'] // 100}"
# Sample outputs written with the kit's reply rules (real price from the example Business Brain, two time options,
# sign off, [CHECK] when the Brain lacks a fact). Example businesses only; labelled as such on the page.
SAMPLES = {
 "detailing": {"label": "Mobile detailing", "biz": "Northside Detail (example)", "items": {
   "price": ("How much for a full detail on an SUV? Free Saturday?", "Hi! A full SUV detail is $250 and takes about 3 hours. We come to you, no water or power needed. I have Saturday at 9 AM or 1 PM. Want me to lock one in? Mike, Northside Detail"),
   "late": ("Sorry it's late, can someone come tomorrow for an interior clean? Dog hair everywhere lol", "No problem at all! An interior detail is $150, plus $30 for pet hair, about 2 hours. Tomorrow I have 10 AM or 2 PM. Which works? Mike, Northside Detail"),
   "chase": ("(Quote sent Tuesday: full detail + ceramic, $490. No reply.)", "Hi Dave, just checking in on the full detail and ceramic coating ($490). Saturday 9 AM is still open, and a $50 deposit holds it. Want me to save it for you? Mike")}},
 "cleaning": {"label": "House cleaning", "biz": "Bright Home Cleaning (example)", "items": {
   "price": ("How much for a deep clean, 3 bed 2 bath?", "Hi! A deep clean for a 3 bed, 2 bath home is $280 and takes about 5 hours with a team of two. I can do Thursday at 9 AM or Friday at 1 PM. Would one of those work? Ana, Bright Home"),
   "late": ("Hi, any chance you can do a move out clean this weekend?", "Hi! Yes, we do move out cleans. For the price I need the size of the home: how many bedrooms and bathrooms? [CHECK: weekend availability] Ana, Bright Home"),
   "chase": ("(Quote sent last week: biweekly cleaning, $140 a visit. No reply.)", "Hi Laura, following up on the biweekly cleaning at $140 a visit. I still have Thursday mornings open. Want me to put you on the schedule starting next week? Ana")}},
 "lawn": {"label": "Lawn care", "biz": "GreenLine Lawn (example)", "items": {
   "price": ("What do you charge to mow a quarter acre every week?", "Hi! Weekly mowing for a quarter acre is $45 a visit, including edging and blowing the walks. I can start this Wednesday or Friday. Which day is better for you? Chris, GreenLine"),
   "late": ("Can you do a fall cleanup before the 15th? Lots of leaves.", "Hi! Yes. Fall cleanups start at $220 for a typical yard, and I'd confirm the price after a quick look or a few photos. I have the 9th or the 12th open. Could you send 2 photos of the yard? Chris, GreenLine"),
   "chase": ("(Quote sent 4 days ago: spring aeration and seeding, $180. No reply.)", "Hi Tom, checking in on the aeration and seeding quote ($180). Early spring is the best window and I have a few spots left next week. Want one? Chris")}},
 "handyman": {"label": "Handyman", "biz": "Ridge Handyman (example)", "items": {
   "price": ("Do you mount TVs? 65 inch on drywall.", "Hi! Yes. Mounting a 65 inch TV on drywall is $149 with your mount, cables hidden in a cord cover. I have Tuesday at 10 AM or Wednesday at 3 PM. Want one of those? Sam, Ridge Handyman"),
   "late": ("Toilet keeps running all night, can you come early tomorrow?", "Hi! That's usually a quick fix: a toilet repair visit is $95 plus parts. Tomorrow I can be there at 8 AM or 11 AM. Which works? Sam, Ridge Handyman"),
   "chase": ("(Quote sent Friday: replace 3 interior doors, $620. No reply.)", "Hi Jen, following up on the 3 interior doors ($620 installed). I can order the doors this week so we're set for next Tuesday. Should I go ahead? Sam")}},
}
TYPES = [("price", "A price question"), ("late", "A late night request"), ("chase", "A quote that went quiet")]

# Message matched variants (Master Plan p6/p11). One variable changes per variant: the promise the ad makes.
# Facts (price, refund, plan, limits) always come from config/offers.json. Variants are ad destinations only:
# canonical points at /front-desk/ and they are noindex, so search sees one page.
VARIANTS = {
 "main": {"path": "/front-desk/", "tag": "Setup kit · for service businesses", "trade": "detailing", "type": "price",
          "h1": "Stop typing the same <em>customer reply.</em>",
          "lead": "Price questions, quotes and quiet leads: it drafts the reply from your real prices, in your voice. You check each one and send it yourself.",
          "title": "Front Desk Kit · answer customer inquiries faster · AUTOPILOT.OI"},
 "after-hours": {"path": "/front-desk/after-hours/", "tag": "For detailing shops and mobile detailers", "trade": "detailing", "type": "late",
          "h1": "Still answering quotes after hours? <em>Get the reply drafted, then send it yourself.</em>",
          "lead": "Paste the message that came in while you were on a job. The kit drafts the reply with your real prices and two open times, in your voice. You read it and send it.",
          "title": "Front Desk Kit · draft after hours replies for your detailing shop · AUTOPILOT.OI"},
 "demo": {"path": "/front-desk/demo/", "tag": "See exactly how it works", "trade": "detailing", "type": "price",
          "h1": "See exactly how the Front Desk Kit works, <em>from a customer message to a draft you approve.</em>",
          "lead": "Pick a trade and a message type. The draft on the right follows the kit's reply rules for an example business. Then see the 3 steps to set it up in your own Claude account.",
          "title": "Front Desk Kit demo · how it drafts replies and quotes · AUTOPILOT.OI"},
}
FAQ_EXTRA = [
 ("Does it send texts or emails automatically?", "No. It never sends anything. It writes a draft in your Claude chat; you copy it, edit it if you want and send it from your own phone or email."),
 ("Can it draft quotes?", "Yes. Type quote with the job details and it writes the quote from your saved prices, with your deposit and cancellation rules. If a price is missing it writes [CHECK] instead of guessing."),
]

KITJS = """<script>document.querySelectorAll('form.kitform').forEach(function(f){f.addEventListener('submit',function(ev){ev.preventDefault();
var em=f.querySelector('input[type=email]').value.trim(),b=f.querySelector('button'),m=f.parentNode.querySelector('.kitmsg');
if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em)){m.textContent='Check that email and try again.';return}
b.disabled=true;b.textContent='Sending...';var fd=new FormData();fd.append('email_address',em);fd.append('fields[source]',f.dataset.source);
try{var q=new URLSearchParams(location.search);['utm_source','utm_campaign','utm_content'].forEach(function(k){var v=q.get(k)||sessionStorage.getItem('ap_'+k);if(v)fd.append('fields['+k+']',v)})}catch(x){}
fetch('https://app.kit.com/forms/10118407/subscriptions',{method:'POST',body:fd,mode:'no-cors'}).then(function(){f.style.display='none';m.innerHTML='<b>Check your inbox.</b> Kit sends a confirm link first; tap it to get the emails.';try{if(window.goatcounter)goatcounter.count({path:'optin/'+f.dataset.page,event:true})}catch(x){}}).catch(function(){b.disabled=false;b.textContent='Try again';m.textContent='Something went wrong. Try again in a moment.'})});});</script>"""

def page(head, nav, foot, variant="main"):
    V = VARIANTS[variant]
    inc = "".join(f"<li>{e(x)}</li>" for x in O["includes"])
    data = json.dumps(SAMPLES)
    trades = "".join(f'<option value="{k}">{e(v["label"])}</option>' for k, v in SAMPLES.items())
    types = "".join(f'<option value="{k}">{e(v)}</option>' for k, v in TYPES)
    buy = f'<a class="btn buy" href="{O["checkout"]}">Get the Front Desk Kit · {PRICE}</a>'
    nots = "".join(f"<li>{e(x[0].upper() + x[1:])}</li>" for x in O["does_not"])
    faqx = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ_EXTRA)
    h = head(V["title"], "A setup kit for your own Claude account that drafts replies, quotes and follow ups from your real prices and rules. You check and send. One time price, 30 day refund.", "/front-desk/")
    if variant != "main":
        h = h.replace("</title>", '</title><meta name="robots" content="noindex,follow">', 1)
    steps = "" if variant != "demo" else """<div class="sec"><div class="wrap"><h2 style="margin-bottom:36px">The setup, step by step</h2><div class="grid3">
<div class="card"><div class="k">1 · Make a Claude Project</div><p>In claude.ai open Projects, then New project, and add the kit PDF to the project files. Free plan works.</p></div>
<div class="card"><div class="k">2 · Answer the interview</div><p>Paste the starter prompt from page 2. The setup agent asks 15 questions about your services, prices, hours and rules, then writes your Business Brain.</p></div>
<div class="card"><div class="k">3 · Paste a message, type reply</div><p>Paste any customer message and type reply, quote or chase. Read the draft, fix anything, send it yourself.</p></div>
</div><p class="label" style="margin-top:14px">A recorded walkthrough of a real setup is coming after our owner tests. Until then the demo above uses example businesses.</p></div></div>"""
    return h + nav("m") + f"""
<div class="wrap hero grid2" style="align-items:center;gap:44px"><div>
<span class="tagline live">{e(V["tag"])}</span>
<h1 class="{"" if variant == "main" else "s"}" style="margin:22px 0 24px">{V["h1"]}</h1>
<p class="lead">{e(V["lead"])}</p>
<div style="display:flex;align-items:baseline;gap:12px;margin-top:28px;flex-wrap:wrap"><span class="W" style="font-size:44px;line-height:1">{PRICE}</span><span class="label">ONE TIME · 30 DAY REFUND</span></div>
<div style="margin-top:16px">{buy}</div>
<p class="label" style="margin-top:12px;line-height:1.6">Runs in your Claude account ({e(O['claude_plan'][0].lower() + O['claude_plan'][1:]).replace('claude', 'Claude')}). It drafts; you send. Not an auto reply service.</p></div>
<div class="ui" id="fdc"><div class="bar"><span>Front Desk Check</span><span>Sample output</span></div>
<div class="fdsel"><select id="fdt" class="sel">{trades}</select><select id="fdk" class="sel">{types}</select></div>
<div class="label" id="fdb" style="margin:4px 4px 8px"></div>
<div class="msg" id="fdm"></div>
<div class="draft"><div class="label" style="margin-bottom:8px">KIT DRAFT · YOU REVIEW AND SEND</div><div class="dr" id="fdd"></div></div>
<div class="label" style="margin-top:12px;text-align:center;line-height:1.5">Written with the kit's reply rules for an example business.<br>Yours uses your own prices, rules and voice.</div></div></div>
<div class="sec paper"><div class="wrap"><h2 style="margin-bottom:36px">What you <em>get.</em></h2><div class="grid3">
<div class="card prod"><div class="k" style="margin-bottom:4px">What you get</div><ul>{inc}</ul></div>
<div class="card"><div class="k" style="margin-bottom:12px">Setup</div><p>Make a Claude Project, add the PDF, paste one starter prompt. The setup agent interviews you and builds your commands with you.</p><p class="label" style="margin-top:12px">{e(O['setup_time']).upper()}</p></div>
<div class="card"><div class="k" style="margin-bottom:12px">What it won't do</div><ul style="list-style:none;display:flex;flex-direction:column;gap:8px;color:#3b3b36;font-size:15px">{nots}<li>Guess a price it doesn't know: it writes [CHECK]</li></ul></div></div></div></div>{steps}
<div class="sec"><div class="wrap grid2" style="gap:44px"><div><h2>Questions<em>.</em></h2><div style="margin-top:28px">{buy}</div></div><div>
<details><summary>Is this an app?</summary><p>No. It's a setup kit: a PDF with a starter prompt, the setup agent and the instructions it installs in a Claude Project. Everything runs in your own Claude account.</p></details>
<details><summary>Do I need a paid Claude plan?</summary><p>No. Claude's free plan works. A paid plan gives you more usage.</p></details>
<details><summary>I've never used Claude. Can I do this?</summary><p>Yes. Make a free account at claude.ai, then follow the 3 step plan in the PDF: make a Project, paste one prompt, answer the questions.</p></details>
<details><summary>Why not just use ChatGPT?</summary><p>A blank chat starts from zero every time and will guess your prices. The kit interviews you once, saves your Business Brain in a Claude Project and drafts from it every time. When something is missing it writes [CHECK] instead of guessing.</p></details>
<details><summary>What if it doesn't work for me?</summary><p>{e(O['refund'])}. Not working for you within 30 days? You get your money back.</p></details>
{faqx}</div></div></div>
<div class="sec"><div class="wrap"><div class="card" style="max-width:640px"><div class="k" style="margin-bottom:8px">Not ready to buy?</div>
<p>Get the free Front Desk Starter and 5 short setup tips by email. Try it on a few real messages first.</p>
<form class="kitform" data-source="frontdesk" data-page="fd_{variant}" style="display:flex;gap:8px;flex-wrap:wrap;margin-top:14px"><input type="email" required placeholder="Your email" autocomplete="email" aria-label="Your email" style="flex:1;min-width:200px;height:54px;border-radius:999px;border:1px solid var(--line);background:var(--g1);color:var(--tx);padding:0 20px;font:500 16px var(--T)"><button class="btn" type="submit">Send it</button></form>
<p class="label kitmsg" style="margin-top:10px">No spam. Unsubscribe anytime. Or <a href="/brain/?utm_source=site&utm_medium=fd_{variant}&utm_campaign=front_desk" style="text-decoration:underline">use it now without email</a>.</p></div></div></div>
<style>.fdsel{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}}@media (max-width:520px){{.fdsel{{grid-template-columns:1fr}}}}.sel{{width:100%;min-width:0;height:44px;border-radius:12px;border:1px solid var(--line);background:var(--g2);color:var(--tx);padding:0 10px;font:600 14px var(--T)}}</style>
<script>(function(){{var S={data},t=document.getElementById('fdt'),k=document.getElementById('fdk');function r(){{var b=S[t.value],x=b.items[k.value];document.getElementById('fdb').textContent=b.biz.toUpperCase();document.getElementById('fdm').textContent=x[0];document.getElementById('fdd').textContent=x[1];try{{if(window.goatcounter)goatcounter.count({{path:'fdc/'+t.value+'/'+k.value,event:true}})}}catch(e){{}}}}t.value='{V["trade"]}';k.value='{V["type"]}';t.onchange=r;k.onchange=r;r();}})();</script>""" + KITJS + foot
