"""Search intent guides for service business owners (Workstream E, test 3). Each one is useful on its own and ends with the
Front Desk Kit and the free check. Imported by tools/site/build.py."""
import html
e = html.escape
U = lambda c: f"utm_source=site&utm_medium=guide&utm_campaign=front_desk&utm_content={c}"
GUIDES = [
 {"slug": "reply-to-price-inquiry", "title": "How to reply to a price inquiry (and win the job)", "k": "Replies",
  "desc": "A simple structure for answering \"how much?\" texts from customers: price, what's included, two times, one question.",
  "lead": "Most service jobs start with a text that says \"how much?\". The reply that books the job is short, gives a real number and makes the next step easy.",
  "steps": [("Give the real price first", "A range or \"it depends\" sends people to the next business. If it truly depends, give the starting price and the one question you need answered."),
            ("Say what's included and how long it takes", "One line. \"About 3 hours, we come to you\" answers the next two questions before they're asked."),
            ("Offer two specific times", "\"Saturday at 9 or 1?\" is easier to answer than \"when works for you?\"."),
            ("End with one question", "Ask for the booking, not for more questions.")],
  "ex": [("How much for a full detail on an SUV? Free Saturday?", "Hi! A full SUV detail is $250 and takes about 3 hours. We come to you. I have Saturday at 9 AM or 1 PM. Want me to lock one in?")],
  "prompt": "You write customer replies for my business. My services and prices: [paste your price list]. Reply to this message in 3 short sentences: give the real price, what's included and how long it takes, offer two times from my availability [times], and end with one question that books the job. If you don't know a price, write [CHECK] instead of guessing. Message: [paste]"},
 {"slug": "after-hours-customer-messages", "title": "Answering customer messages after hours", "k": "After hours",
  "desc": "How to handle texts and calls that come in while you're on a job or done for the day, without living on your phone.",
  "lead": "Messages that arrive at 7 or 9 PM are often the most ready to buy, and they're the easiest to lose. You don't have to answer instantly, but you do need a system.",
  "steps": [("Acknowledge fast, answer properly later", "A short note you write once (\"Thanks, I'm on a job, I'll send your price by 8 AM\") keeps the lead warm without you typing a quote at night."),
            ("Batch the real replies", "Answer everything in one sitting: first thing in the morning and after your last job."),
            ("Ask the one missing detail up front", "Size, model, address, photos. Whatever you always need before you can price it."),
            ("Never promise what you can't check", "If you're not sure a time is open, say you'll confirm it.")],
  "ex": [("Sorry it's late, can someone come tomorrow for an interior clean? Dog hair everywhere", "No problem at all! An interior detail is $150, plus $30 for pet hair, about 2 hours. Tomorrow I have 10 AM or 2 PM. Which works?")],
  "prompt": "Here are the customer messages that came in after hours: [paste all]. For each one, draft a short reply using my prices and rules: [paste]. Offer two times from tomorrow's open slots [times]. If a message is missing what I need to price it, ask for that one detail. Mark anything you're unsure of with [CHECK]."},
 {"slug": "follow-up-on-a-quote", "title": "How to follow up on a quote without sounding pushy", "k": "Follow ups",
  "desc": "When and how to follow up on quotes that went quiet, with example messages for day 2, day 5 and the last check in.",
  "lead": "A quote that gets no reply isn't always a no. People get busy. A short, friendly follow up wins back jobs that were already gone, and most owners never send one.",
  "steps": [("Day 2: make it easy to say yes", "Repeat the price and offer a time. No pressure."),
            ("Day 5: answer the likely objection", "Price, timing or trust. Give one reason it's still a good deal, or offer a smaller option."),
            ("Last check in: close the loop", "\"I'll close this out for now, just reply if you'd like to book later.\" People often answer this one."),
            ("Stop after three", "Then move on. Following up forever hurts more than it helps.")],
  "ex": [("(Quote sent Tuesday: full detail + ceramic, $490. No reply.)", "Hi Dave, just checking in on the full detail and ceramic coating ($490). Saturday 9 AM is still open, and a $50 deposit holds it. Want me to save it for you?")],
  "prompt": "I sent [name] a quote for [service] at [price] on [day] and haven't heard back. It's been [days] days. Write one short, friendly follow up in my voice (examples: [paste 2 messages you sent]). Say whether this is the 1st, 2nd or last follow up. Offer one specific next step. Don't invent discounts."},
]

def page(g, head, nav, foot):
    steps = "".join(f'<div class="card"><h3>{e(a)}</h3><p style="margin-top:8px">{e(b)}</p></div>' for a, b in g["steps"])
    ex = "".join(f'<div class="ui"><div class="bar"><span>Example</span><span>Example business</span></div><div class="msg">{e(q)}</div><div class="draft"><div class="label" style="margin-bottom:8px">REPLY</div><div class="dr">{e(a)}</div></div></div>' for q, a in g["ex"])
    return head(g["title"] + " · AUTOPILOT.OI", g["desc"], f"/guides/{g['slug']}/") + nav("") + f"""
<div class="wrap hero" style="max-width:820px"><div class="k"><b>Guide</b> · {e(g['k'])}</div><h1 style="margin:18px 0 20px;font-size:clamp(34px,5.4vw,54px)">{e(g['title'])}</h1><p class="lead">{e(g['lead'])}</p></div>
<div class="wrap" style="max-width:820px;padding-bottom:60px"><div class="steps" style="grid-template-columns:1fr 1fr">{steps}</div>
<h2 style="margin:50px 0 18px;font-size:30px">An example</h2>{ex}
<h2 style="margin:50px 0 12px;font-size:30px">Do it free with Claude</h2><p class="lead" style="font-size:17px">Paste this into Claude (the free plan works) and fill the brackets.</p>
<div class="card" style="margin-top:14px"><p style="font:500 15px/1.6 ui-monospace,Menlo,monospace;color:#e3e6dc;white-space:pre-wrap">{e(g['prompt'])}</p></div>
<div class="card" style="margin-top:40px;border-color:rgba(212,255,58,.4)"><div class="k" style="margin-bottom:10px">Set it up once</div><h3 style="font-size:22px">Don't want to paste your prices every time?</h3>
<p style="margin:10px 0 18px">The Front Desk Kit saves your prices, rules and voice in your own Claude account and drafts replies, quotes and follow ups from them. It drafts; you send. $39 one time, 30 day refund.</p>
<div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn" href="/front-desk/?{U(g['slug'])}">See the Front Desk Kit</a><a class="btn ghost" href="/brain/?{U(g['slug'])}">Try the free check</a></div></div></div>""" + foot
