"""The store: docs/store/index.html + one page per product at docs/store/<slug>/index.html.
Every page: the demo reel where one exists, who it's for, a labelled sample output, what it does and doesn't do,
what you need, what you get, FAQ, one checkout button. Prices are copied from Gumroad, never changed here.
Run: python3 tools/store/pages.py"""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
e = html.escape
GR = "https://autopilotoi.gumroad.com/l/"
def vid(id): return id if os.path.exists(f"{ROOT}/docs/media/freel/web/{id}.mp4") else None
def advid(id): return ("ads/" + id) if os.path.exists(f"{ROOT}/docs/media/ads/{id}.mp4") else None

FAQ_COMMON = [
    ("Is this an app?", "No. It's a prompt kit (PDF). You paste the master prompt into a Claude Project once, then run it whenever you need it."),
    ("Do I need a paid Claude plan?", "No. Claude's free plan works and lets you create up to 5 Projects. A paid plan gives you more usage."),
    ("Can it log into my accounts or send things for me?", "No. It reads what you upload and drafts. You check it, decide and send."),
    ("What about my private info?", "Black out full account, card and member numbers before you upload. Claude only needs merchant names, dates and amounts."),
    ("Refunds?", "Not working for you within 30 days? Reply to your Gumroad receipt for a full refund."),
]
HOW = [("Buy it, open the PDF", "Instant download from Gumroad."), ("Paste the master prompt into a Claude Project", "About 10 minutes, once. Free Claude plan works."), ("Upload your documents and run it", "It reads, checks and drafts. You decide and send.")]
KIT = "A PDF with the master prompt, 5 starter prompts, a 10 minute setup guide and a tracker."

P = {
 "subs": dict(cat="money", ic="✂️", name="Subscription Agent", price="$10", buy="subs-agent", kw="SUBS", guide="subs", video=vid("subs-agent"),
  title="Find every subscription you pay for", short="Lists every recurring charge, drafts the cancel messages",
  lead="Upload 2 to 3 months of statements. Claude lists every recurring charge, helps you sort keep and cut, and drafts the cancel messages. Do a sweep once a month and new charges don't slip by.",
  who=["You pay for apps, streaming or trials you've lost track of", "You want one clear list with the yearly cost of each", "You'd rather not write cancel emails yourself"],
  sample_note="Sample output from a test run on made-up statements. Your results depend on your statements.",
  sample_head=["Merchant", "Amount", "Every", "Yearly"],
  sample_rows=[["NETFLIX.COM", "$17.99", "Month", "$215.88"], ["SPOTIFY USA", "$11.99", "Month", "$143.88"], ["ADOBE PHOTO", "$19.99", "Month", "$239.88"], ["PLANET FIT", "$15.00", "Month", "$180.00"], ["APPLE.COM/BILL", "$6.99", "Month", "$83.88"], ["APPLE.COM/BILL", "$2.99", "Month", "$35.88"], ["AMZN PRIME", "$139.00", "Year", "$139.00"]],
  sample_after=["Total: $74.95 a month plus $139 a year, about $1,038 a year.", "Flags: two Apple charges (check Settings, then Subscriptions) and the photo plan went up in month 3. Then it asks which ones you still use.", "Cancel draft: \"Please cancel my Photography plan under this email, effective today, stop all future charges and confirm in writing.\""],
  does=["Finds recurring charges, even with odd merchant names", "Builds your keep and cut list with yearly costs", "Drafts cancel and refund messages", "Flags new charges and price changes when you upload new statements"],
  doesnt=["Cancel anything for you", "See your bank account", "Guarantee a refund"],
  need=["2 to 3 months of bank and card statements (PDF or CSV)", "A Claude account (free works)", "About 15 minutes"],
  faq=[("How is this different from the free guide?", "The free guide gives you the prompts to do one sweep. The kit adds a deeper master prompt, 5 starter prompts (cancel, still charged, cheaper plan, free trial guard, monthly sweep) and a tracker, set up once in a Claude Project.")]),
 "bill": dict(cat="money", ic="🧾", name="Bill Agent", price="$10", buy="bill-agent", kw="BILL", guide="bill", video=vid("bill-agent"),
  title="Check a medical bill before you pay it", short="Checks a medical bill against your insurance before you pay",
  lead="Upload your itemized bill and your insurer's explanation of benefits. Claude lines them up, points out what doesn't match, and writes your call script so you know exactly what to ask.",
  who=["You got a medical or dental bill and aren't sure it's right", "The bill doesn't match what your insurance says you owe", "You want a script before you call the billing office"],
  sample_note="Sample output from a test run on a made-up bill and EOB. Your results depend on your documents.",
  sample_head=["Line", "Billed", "EOB says", "Ask"],
  sample_rows=[["Office visit", "$310.00", "You owe $40 copay", "Why am I billed more than my copay?"], ["Lab panel, twice same day", "$96 x2", "Listed once", "Is this a duplicate charge?"], ["Facility fee", "$185.00", "Not listed", "Was this sent to my insurance?"], ["Total due", "$687.00", "Your share $63.40", "Can you rebill to match the EOB?"]],
  sample_after=["Call script opener: \"Hi, I'm calling about my bill from [date]. Before I pay, I'd like to review a few lines that don't match my insurance statement.\"", "It also reminds you to ask whether the hospital has a financial assistance policy, and to get any agreement in writing."],
  does=["Compares your bill to your EOB line by line", "Lists questions and possible errors in a table", "Writes your call script and follow up email", "Keeps a log of every bill until it's settled"],
  doesnt=["Call anyone for you", "Give medical or legal advice", "Guarantee a lower bill"],
  need=["Your itemized bill (ask the billing office for it)", "The EOB from your insurer for that visit", "A Claude account (free works)"],
  faq=[("What if I don't have an itemized bill?", "Call the billing office and ask for one with every charge and its billing code. The kit includes the exact words to use.")]),
 "debt": dict(cat="money", ic="💸", name="Debt Agent", price="$10", buy="debt-agent", kw="DEBT", guide="debt", video=vid("debt-agent"),
  title="A payoff plan and the script to ask for a lower rate", short="Payoff plan and the script to ask for a lower rate",
  lead="Give it your cards and loans: balance, rate, minimum. Claude builds a payoff order you can keep, shows what each extra dollar does, and writes the call script for asking your card company for a lower rate.",
  who=["You carry balances on more than one card or loan", "You want to know which one to hit first and why", "You'd like to ask for a lower rate but don't know what to say"],
  sample_note="Sample output from a test run on made-up balances. Your plan depends on your numbers.",
  sample_head=["Account", "Balance", "APR", "Order"],
  sample_rows=[["Store card", "$1,240", "29.9%", "1st"], ["Visa", "$3,860", "24.5%", "2nd"], ["Car loan", "$7,900", "6.9%", "minimums only"]],
  sample_after=["With $150 extra a month on the store card first, the plan shows the payoff month for each account and the interest you'd skip.", "Rate call script: \"I've been a customer since 2019 and I've paid on time. I'm seeing offers at 18%. Can you lower my rate?\" plus what to say if they say no."],
  does=["Orders your debts by what saves the most interest", "Shows the payoff month for every extra dollar you add", "Writes the lower rate call script and a hardship letter", "Tracks balances month to month"],
  doesnt=["Negotiate for you or contact lenders", "Give financial or legal advice", "Promise a lower rate"],
  need=["Your balances, rates and minimums (statements or just the numbers)", "A Claude account (free works)", "About 15 minutes"],
  faq=[("Snowball or avalanche?", "It shows you both with your real numbers and the difference in interest, then you pick the one you'll stick to.")]),
 "refund": dict(cat="money", ic="↩️", name="Refund Agent", price="$10", buy="refund-agent", kw="REFUND", guide="refund", video=vid("refund-agent"),
  title="Get your money back without the argument", short="Drafts refund requests that name your rights",
  lead="Cancelled flight, double charge, item never arrived, service still billing after you cancelled. Upload the receipt or booking. Claude checks what you can ask for, and writes the request for you to send.",
  who=["A company owes you money and the first ask went nowhere", "You're not sure what you're actually entitled to", "You want the request written properly, with the rule named"],
  sample_note="Sample output from a test run on a made-up cancelled flight. Rules depend on your country, your card and the case.",
  sample_head=["Check", "Result"],
  sample_rows=[["Flight cancelled by airline", "Yes"], ["Took the voucher or a new flight?", "No"], ["U.S. DOT refund rule applies", "Likely"], ["Ask for", "Full refund to original card"]],
  sample_after=["Draft: \"Hello, you cancelled my flight on Oct 12 (booking K7Q2PX). I did not accept the voucher or a new flight. Under U.S. DOT rules I am requesting a full refund of $412.60 to my original card.\"", "If they say no, it drafts the next step: a chargeback request to your card or a complaint to the right regulator."],
  does=["Works out what you can ask for and the deadline", "Writes the first request, the follow up and the escalation", "Drafts a chargeback letter when that's the right move", "Keeps every case in one tracker"],
  doesnt=["Send anything or contact companies for you", "Give legal advice", "Guarantee a refund"],
  need=["The receipt, booking or statement line", "Any emails or chats you already had with them", "A Claude account (free works)"],
  faq=[("Does it work outside the U.S.?", "Yes. You tell it your country and it uses the consumer rules there, and tells you plainly when it isn't sure.")]),
 "raise": dict(cat="money", ic="📈", name="Raise Agent", price="$10", buy="raise-agent", kw="RAISE", guide="raise", video=vid("raise-agent"),
  title="Build the case for your raise", short="Pay data, your number and a practice run with pushback",
  lead="Dump your messy notes from the year. Claude turns them into proof with numbers, checks public pay data for your role and area, picks a number to ask for, and practices the conversation with you, pushback included.",
  who=["You think you're underpaid but can't prove it on paper", "Reviews are coming and you want to walk in prepared", "You freeze when the manager says 'there's no budget'"],
  sample_note="Sample output from a test run on made-up notes. Pay data comes from public sources at the time you run it.",
  sample_head=["Win", "Proof"],
  sample_rows=[["Cut supplier costs", "saved $18K"], ["Trained 3 new hires", "onboarding 2 weeks faster"], ["Took over the Hill account", "+$40K a year"], ["Fixed the late invoices", "paid 12 days sooner"]],
  sample_after=["Ask: 8%, with the market range for your role in your area and the three wins that justify it.", "Then it plays your manager: \"We just don't have the budget this quarter.\" and coaches your reply."],
  does=["Turns notes into wins with numbers", "Checks public pay data (BLS and salary sites) for your role", "Writes your one page case and the opening lines", "Practices the meeting with you, including the no"],
  doesnt=["Talk to your manager for you", "Promise a raise", "Make up numbers you can't back"],
  need=["Your notes, reviews, emails, anything from the year", "Your job title, area and current pay (or skip it)", "A Claude account (free works)"],
  faq=[("What if I don't have numbers?", "It asks the questions that find them: time saved, money saved, customers kept, problems avoided. Most people have more than they think.")]),
 "deposit": dict(cat="money", ic="🏠", name="Deposit Agent", price="$10", buy="deposit-agent", kw="DEPOSIT", guide="deposit", video=None,
  title="Get your security deposit back", short="Check every deduction and draft the letter",
  lead="Upload the move out statement and your lease. Claude checks every deduction against your state's rules and normal wear, and drafts the letter that asks for the rest back, with the deadline named.",
  who=["Your landlord kept part or all of your deposit", "The deductions look like normal wear to you", "You want a firm, polite letter instead of a fight"],
  sample_note="Sample output from a test run on a made-up move out statement. Rules depend on your state and your lease.",
  sample_head=["Deduction", "Charged", "Check"],
  sample_rows=[["Repaint whole unit", "$450", "Normal wear after 3 years, usually not chargeable"], ["Carpet cleaning", "$120", "Only if the lease says so and it's dirtier than normal"], ["Lost key", "$25", "Fair"]],
  sample_after=["Draft: \"I'm requesting the return of $570 of my $1,200 deposit. Repainting after a three year tenancy is normal wear under [state] law. Please return the amount within [state deadline].\"", "If they don't reply, it drafts the small claims checklist."],
  does=["Checks each deduction against your state's deposit rules", "Separates normal wear from damage", "Writes the demand letter with the legal deadline", "Prepares the small claims steps if needed"],
  doesnt=["Give legal advice", "File anything for you", "Guarantee the money back"],
  need=["The move out statement and your lease", "Move in and move out photos if you have them", "A Claude account (free works)"],
  faq=[("Is this legal advice?", "No. It's education and drafting. For a big amount or a complicated case, a tenant's rights group or a lawyer is the right call, and the kit tells you when.")]),
 "money": dict(cat="money", ic="💰", bundle=True, name="All 5 Money Agents", price="$39", buy="all-money-agents", kw=None, guide=None, video=vid("money-agents"),
  title="All 5 Money Agents", short="Bill, Debt, Subscription, Refund and Raise, in one Claude Project",
  lead="Five Claude prompt kits for the money jobs most people put off: medical bills, card debt, subscriptions, refunds and raises. $50 separately, $39 together, plus the Money Agents Pro setup that installs all 5 in one Claude Project in about 20 minutes.",
  who=["You want one place to handle bills, debt and refunds with Claude", "You'll use at least 3 of the 5", "You like having the exact prompt ready when something comes up"],
  sample_note="Sample output from the Subscription Agent, from a test run on made-up statements.",
  sample_head=["Merchant", "Amount", "Every", "Yearly"],
  sample_rows=[["NETFLIX.COM", "$17.99", "Month", "$215.88"], ["ADOBE PHOTO", "$19.99", "Month", "$239.88"], ["PLANET FIT", "$15.00", "Month", "$180.00"], ["AMZN PRIME", "$139.00", "Year", "$139.00"]],
  sample_after=["Then it asks which ones you still use and drafts the cancel messages for the rest."],
  does=["Bill Agent: checks a medical bill against your insurance", "Debt Agent: payoff plan and the script to ask for a lower rate", "Subscription Agent: lists every recurring charge, drafts cancel messages", "Refund Agent: drafts refund requests that name your rights", "Raise Agent: pay data, your number and a practice run"],
  doesnt=["Log into your accounts", "Send messages or make calls for you", "Give financial or legal advice or guarantee results"],
  need=["A Claude account (the free plan's 5 Projects fit all 5)", "The documents for whichever job you're doing", "About 20 minutes to set up"],
  faq=[("Can I start with one?", "Yes. Every kit is $10 on its own, and every one has a free guide you can try first.")],
  items=["bill", "debt", "subs", "refund", "raise"], sep="$50"),
 "autopilot": dict(cat="business", ic="⚡", name="Autopilot", price="$19.99", buy="autopilot", kw="AUTOPILOT", guide=None, video=advid("st-demo") or advid("ap-a"),
  title="It writes.|You send.", short="Your replies, quotes and follow ups, drafted in your voice",
  lead="A 15 minute setup that turns the free Claude app into your business assistant. It learns your prices, rules and voice, then drafts your customer replies, quotes and follow ups. You read every draft and hit send.",
  inside=["Setup guide (PDF) and 1 starter prompt", "9 ready commands: reply, quote, chase, review, faq, plan week, plus 3 built for your business", "Templates, a cheat sheet and a time back tracker"],
  who=["You answer customers yourself, often at night", "Quotes go quiet and you forget to follow up", "You want help tonight, not a course or a new app to learn"],
  sample_note="Example business (a mobile car detailer) from a test run. Your drafts use your own prices, rules and voice.",
  sample_head=["You type", "Autopilot drafts"],
  sample_rows=[["reply: how much for a full detail on an SUV? Free Saturday?", "A full SUV detail is $250, about 3 hours. We come to you. Saturday at 9 AM or 1 PM?"], ["quote: Dave, SUV, ceramic, pet hair", "$250 + $240 + $30 = $520 · $50 deposit holds the slot · 24 hr notice to cancel"], ["chase: Dave, day 3", "Saturday 9 AM is still open and the $520 holds through the end of the month. Want me to lock it in?"], ["review: Maria, full detail", "Thanks for having us out today! A quick Google review would mean a lot: [your link]"]],
  sample_after=["Missing information shows up as [CHECK: ...], so it never guesses a price or a rule.", "Then type build me a system for [any task] and it builds a new command with you."],
  does=["Interviews you and writes your Business Brain", "Builds 6 core systems: reply, quote, chase, review, faq, plan week", "Builds 3 extra systems from the busy work you name", "Drafts in your voice with your real prices and rules"],
  doesnt=["Send, post or call anyone for you", "Log into your email, calendar or accounts", "Run on a schedule by itself (that's The Workspace)"],
  need=["A free Claude account (claude.ai) on your phone or computer", "Your price list and 2 real messages you've sent customers", "About 30 minutes"],
  faq=[("Why not just use ChatGPT?", "You can, but a blank chat starts from zero every time and will guess your prices. Autopilot interviews you once, saves your Business Brain in a Claude Project, and drafts from it every time. When something is missing it writes [CHECK] instead of guessing. You also get 9 ready commands, templates and a 30 minute setup plan."),
       ("Why is it called Autopilot if I press send?", "It puts the writing on autopilot: replies, quotes and follow ups come back drafted. Sending stays with you, so nothing reaches a customer that you haven't read."),
       ("I've never used Claude. Can I do this?", "Yes. Make a free account at claude.ai, then follow the 3 step plan in the PDF: make a Project, paste one prompt, answer the questions. About 30 minutes."),
       ("How is this different from The Workspace?", "Autopilot drafts when you paste something in. The Workspace connects 7 scheduled agents to your Gmail and Calendar so they work on their own, still waiting for your OK."), ("Does it work for my business?", "If you answer customers, send quotes and follow up, yes. The interview shapes everything around your business.")],
  how=[("Buy it, open the PDF", "Instant download from Gumroad."), ("Paste one prompt into a Claude Project", "Autopilot interviews you for about 15 minutes and writes your Business Brain."), ("It builds your systems with you", "Tests each one on a real example from your business until it sounds like you.")]),
 "video": dict(cat="tiktok", ic="🎬", name="Video Agent", price="$10", buy="video-agent", kw="VIDEO", guide="video", video=vid("content-machine"),
  title="One idea into a week of TikToks", short="One idea into a week of TikToks, every edit planned",
  lead="Tell it your niche, your format and one idea. Claude writes 5 hooks, scripts every video, and plans every cut, caption and on screen text as a CapCut edit plan. You film and post.",
  who=["You know what you want to talk about but posting daily is the hard part", "You want scripts that sound like you, not a template", "You edit in CapCut and want the plan done before you open it"],
  sample_note="Sample output from a test run with a made-up money tips account. Your hooks come from your niche and your voice.",
  sample_head=["Day", "Hook"],
  sample_rows=[["Mon", "3 apps I deleted to save $40"], ["Tue", "The fee your bank hopes you miss"], ["Wed", "I asked AI to audit my phone bill"], ["Thu", "Cancel this before it renews"], ["Fri", "The 10 second budget check"]],
  sample_after=["Each day comes with a 30 second script, the shot list, the text on screen and the caption with hashtags.", "After a week you paste your numbers in and it tells you which hook style to make more of."],
  does=["Writes hooks and scripts in your voice", "Plans every edit: cuts, text, captions, cover", "Builds a weekly content calendar", "Reads your results and adjusts next week"],
  doesnt=["Film, edit or post for you", "Promise views or followers", "Copy other creators' videos"],
  need=["Your handle, niche and one caption or script you wrote", "A Claude account (free works)", "CapCut or any editor"],
  faq=[("I don't want to show my face.", "Fine. Tell it your format (voiceover, hands only, screen recording) and every script and shot list is written for that.")]),
 "shop": dict(cat="tiktok", ic="🛍️", name="Shop Agent", price="$10", buy="shop-agent", kw="SHOP", guide="shop", video=vid("shop-finder"),
  title="Stop guessing what to sell on TikTok Shop", short="Find products, profit math after fees, rules check, creators",
  lead="Give it your niche and your budget. Claude finds product ideas, works out what you'd actually keep after fees and shipping, checks the category rules, and drafts your listings and creator outreach.",
  who=["You want to sell on TikTok Shop and don't know where to start", "You've been burned by a product that didn't make money after fees", "You want listings and creator messages drafted, not blank pages"],
  sample_note="Sample output from a test run with a $300 budget. Fees change, so the kit always tells you to confirm them in Seller Center.",
  sample_head=["Product", "Sells for", "You keep"],
  sample_rows=[["Posture corrector", "$24.99", "$9.40"], ["LED desk lamp", "$29.99", "$8.15"], ["Phone tripod", "$19.99", "$6.70"]],
  sample_after=["Each product comes with the cost, fee and shipping math shown, the category rules to check, and a first listing draft.", "Then it drafts the message to 10 creators who already post in your niche."],
  does=["Finds product ideas in your niche and budget", "Does the profit math after fees and shipping", "Checks category rules and what needs approval", "Drafts listings and creator outreach"],
  doesnt=["Buy stock, list or ship for you", "Promise sales", "Know today's fees without you checking Seller Center"],
  need=["Your niche, budget and country (written for the US)", "A Claude account (free works)", "A TikTok Shop seller or affiliate account when you're ready"],
  faq=[("Seller or affiliate?", "Both. The quiz asks which path you're on and the prompts change for each.")]),
 "sell": dict(cat="tiktok", ic="💬", name="Sales Agent", price="$10", buy="sell-agent", kw="SALES", guide="sell", video=None,
  title="Every DM answered in your voice", short="Every DM answered in your voice, videos, LIVE plans",
  lead="Tell it what you sell, your prices, shipping and the 5 questions buyers always ask. Claude drafts replies to comments and DMs in your voice, writes the product videos, and plans your LIVE. You read, tweak and send.",
  who=["You sell something and the DMs are eating your evenings", "You want replies that sound like you and never make a claim you can't back", "You want a LIVE plan that isn't just 'go live and talk'"],
  sample_note="Sample output from a test run with a made-up candle shop. Your replies use your real prices and policies.",
  sample_head=["Buyer asks", "Draft reply"],
  sample_rows=[["Does it ship to Canada?", "Yes! $12 flat, usually 6 to 9 days. Want me to send the link?"], ["Is it really soy wax?", "100% soy, cotton wick. Burn time is about 45 hours on the 8oz."], ["Any discount?", "Our bundle of 3 saves $9, that's the best deal we run."]],
  sample_after=["It keeps a list of the questions it couldn't answer from your info, so you add the answer once and it never guesses.", "LIVE plan: the 20 minute run of show, 3 hooks for the first minute and what to pin."],
  does=["Drafts comment and DM replies in your voice", "Writes product videos and the LIVE run of show", "Keeps an FAQ that grows with every new question", "Flags questions it shouldn't answer (refunds, claims)"],
  doesnt=["Send replies or go live for you", "Make up reviews or results", "Promise sales"],
  need=["Your product, price, shipping and return policy", "The 5 questions buyers ask most, with your answers", "A Claude account (free works)"],
  faq=[("Can I use it for Instagram or Etsy?", "Yes. It's written for TikTok Shop first, but the replies and FAQ work anywhere you sell.")]),
 "tiktok": dict(cat="tiktok", ic="🎯", bundle=True, name="TikTok Agents", price="$24", buy="tiktok-agents", kw=None, guide=None, video=vid("shop-finder"),
  title="All 3 TikTok Agents", short="Video, Shop and Sales Agent, together",
  lead="Video, Shop and Sales Agent: scripts and CapCut edit plans, product finding and profit checks, and reply drafts for comments and DMs. $30 separately, $24 together. You edit, post and reply.",
  who=["You're building a TikTok Shop and want the whole loop covered", "You'd use at least 2 of the 3", "You want them set up in one Claude Project with one Business Brain"],
  sample_note="Sample output from the Shop Agent, from a test run with a $300 budget.",
  sample_head=["Product", "Sells for", "You keep"],
  sample_rows=[["Posture corrector", "$24.99", "$9.40"], ["LED desk lamp", "$29.99", "$8.15"], ["Phone tripod", "$19.99", "$6.70"]],
  sample_after=["Then the Video Agent plans the week of videos for the winner and the Sales Agent drafts the replies when the comments come in."],
  does=["Video Agent: one idea into a week of TikToks, every edit planned", "Shop Agent: find products, profit math after fees, rules check, creators", "Sales Agent: every DM answered in your voice, videos, LIVE plans"],
  doesnt=["Film, post, list or reply for you", "Promise views or sales", "Replace reading the Seller Center rules yourself"],
  need=["A Claude account (free works)", "Your niche, budget and what you sell", "About 20 minutes to set up"],
  faq=[("Can I start with one?", "Yes. Each one is $10 on its own.")],
  items=["video", "shop", "sell"], sep="$30"),
}

CATS = [("money", "Save money", "Bills, debt, subscriptions, refunds, raises. The money jobs you keep putting off."),
        ("tiktok", "Grow on TikTok", "Scripts, products that actually make money after fees, and DMs answered in your voice."),
        ("business", "Run a business", "Agents that work your inbox, calendar and follow ups, and brief you every morning.")]

CSS = """
:root{--l:#D4FF3A;--line:#1c1d1b;--mut:#8f928b;--card:#0c0d0c}
*{box-sizing:border-box;margin:0;padding:0}html{overflow-x:hidden;scroll-behavior:smooth}
body{background:#000;color:#fff;font:500 16px/1.55 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}.w{max-width:600px;margin:0 auto;padding:0 20px 60px;position:relative;z-index:1}
.glow{position:fixed;width:620px;height:620px;left:50%;margin-left:-310px;top:-340px;border-radius:50%;background:rgba(212,255,58,.14);filter:blur(110px);pointer-events:none}
.hd{display:flex;align-items:center;gap:10px;padding:20px 0}.hd img{width:34px;height:34px;border-radius:50%}.hd b{font-weight:900;letter-spacing:.04em}.hd a.bk{margin-left:auto;color:var(--mut);font-size:14px;text-decoration:none}
.tag{font:700 11px 'Space Mono',monospace;letter-spacing:.22em;text-transform:uppercase;color:var(--l)}
h1{font:900 clamp(38px,10vw,56px)/.95 Inter;text-transform:uppercase;letter-spacing:-.02em;margin:10px 0 14px}
h1 em{font-style:normal;color:var(--l)}
.lead{color:rgba(255,255,255,.82);font-size:17px}
.buy{display:block;text-align:center;background:var(--l);color:#000;text-decoration:none;font:900 16px Inter;text-transform:uppercase;border-radius:16px;padding:18px;margin:22px 0 8px;box-shadow:0 0 40px rgba(212,255,58,.25)}
.sm{text-align:center;color:var(--mut);font-size:13px}
.inside{margin:18px 0 6px;border:1px solid var(--line);border-radius:16px;padding:14px 16px;background:var(--card)}.inside b{font:700 11px 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--l)}.inside ul{margin:8px 0 0 18px}.inside li{margin:4px 0;font-size:15px}
h2{font:900 13px 'Space Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);margin:36px 0 12px}
ul{padding-left:20px}li{margin:6px 0}
.box{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px}
.note{font-size:13px;color:var(--mut);margin-bottom:10px}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font:400 12.5px 'Space Mono',monospace}
th{text-align:left;color:var(--l);font-weight:700;border-bottom:1px solid #2a2d27;padding:6px 6px 6px 0;white-space:nowrap}td{border-bottom:1px solid #1a1c19;padding:7px 6px 7px 0;vertical-align:top}
.after p{margin-top:10px;font-size:14.5px;color:rgba(255,255,255,.85)}
.no li::marker{content:"✕  ";color:#ff6b6b}.yes li::marker{content:"✓  ";color:var(--l)}
details{border-bottom:1px solid var(--line);padding:12px 0}summary{font-weight:700;cursor:pointer}details p{color:rgba(255,255,255,.75);margin-top:6px;font-size:15px}
.free{text-align:center;margin-top:14px;color:var(--mut)}.free a{color:var(--l)}
.ft{color:#5d6059;font-size:12px;text-align:center;margin-top:36px;line-height:1.6}
.vid{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--line);background:#050605;margin:18px 0 6px;aspect-ratio:9/16;max-height:620px}
.vid video{width:100%;height:100%;object-fit:cover;display:block}
.vid .snd{position:absolute;left:12px;bottom:12px;font:700 11px 'Space Mono';letter-spacing:.15em;background:rgba(0,0,0,.65);color:#fff;border:1px solid rgba(255,255,255,.2);border-radius:30px;padding:8px 12px;text-transform:uppercase}
.vid .lab{position:absolute;right:12px;top:12px;font:700 10px 'Space Mono';letter-spacing:.15em;background:var(--l);color:#000;border-radius:6px;padding:5px 8px;text-transform:uppercase}
.steps{display:grid;gap:10px}.step{display:flex;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px}
.step i{font:900 18px Inter;font-style:normal;color:var(--l);width:28px;flex:none}.step b{display:block}.step p{color:var(--mut);font-size:14px;margin-top:2px}
.grid{display:grid;gap:10px}
.card{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:12px;text-decoration:none;transition:border-color .2s}
.card:hover{border-color:rgba(212,255,58,.5)}
.card .th{width:64px;height:88px;border-radius:12px;background:#111;flex:none;object-fit:cover;display:flex;align-items:center;justify-content:center;font-size:28px;overflow:hidden}
.card .th img{width:100%;height:100%;object-fit:cover}
.card b{font-weight:800;display:block}.card p{color:var(--mut);font-size:13.5px;margin-top:2px;line-height:1.4}
.card .go{margin-left:auto;font:900 15px Inter;color:var(--l);white-space:nowrap;flex:none}
.hero{display:block;background:linear-gradient(160deg,#121410,#070807);border:1px solid rgba(212,255,58,.35);border-radius:22px;padding:18px;text-decoration:none;position:relative;overflow:hidden}
.hero:after{content:"";position:absolute;width:260px;height:260px;right:-90px;top:-120px;border-radius:50%;background:rgba(212,255,58,.14);filter:blur(50px)}
.hero .H{font:900 34px/1 Inter;text-transform:uppercase;display:block;margin:8px 0 8px}.hero p{color:rgba(255,255,255,.75);font-size:14.5px}
.hero .btn{display:inline-block;margin-top:14px;background:var(--l);color:#000;font:900 14px Inter;text-transform:uppercase;border-radius:12px;padding:12px 16px}
.hero .sm{display:block;text-align:left;margin-top:8px}
.flt{display:flex;gap:8px;overflow-x:auto;padding:4px 0 14px;scrollbar-width:none}.flt::-webkit-scrollbar{display:none}
.flt a{flex:none;text-decoration:none;color:var(--mut);font:700 12px 'Space Mono';letter-spacing:.1em;padding:9px 14px;border:1px solid var(--line);border-radius:30px;background:var(--card);text-transform:uppercase}
.flt a:hover{color:#fff;border-color:rgba(255,255,255,.3)}
.cathd{margin:36px 0 12px}.cathd .tag{display:block;margin-bottom:6px}.cathd h2{margin:0;font:900 26px Inter;letter-spacing:-.01em;text-transform:uppercase;color:#fff}.cathd p{color:var(--mut);font-size:14.5px;margin-top:4px}
.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin-top:10px}.items a{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px;text-decoration:none;font-size:13.5px}.items a b{display:block}.items a span{color:var(--mut);font-size:12px}
.trust{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:14px}.trust div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;font-size:13px;color:rgba(255,255,255,.8)}.trust b{display:block;color:#fff;font-size:14px}
"""
HEAD = lambda title, desc, canon, og: f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{og}"><link rel="canonical" href="{canon}">
<meta name="theme-color" content="#000000"><link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,500;14..32,600;14..32,700;14..32,900&display=swap" rel="stylesheet">
<style>{CSS}</style><link rel="stylesheet" href="/assets/brand.css"></head><body><div class="glow"></div><div class="w">"""
FOOT = """<div class="ft">Education only, not financial, legal or medical advice. Sample outputs are from test runs on made-up data. AUTOPILOT.OI is independent and not affiliated with Anthropic. Claude is a product of Anthropic.</div>
</div><script>document.querySelectorAll('.vid').forEach(b=>{const v=b.querySelector('video'),s=b.querySelector('.snd');if(!v)return;b.addEventListener('click',()=>{v.muted=!v.muted;s.textContent=v.muted?'🔇 tap for sound':'🔊 sound on';v.play()})})</script><script src="/assets/ap.js" defer></script></body></html>"""

def video_block(id, label="Demo · sample data"):
    if not id: return ""
    src, poster = (f"/media/ads/web/{id[4:]}.mp4", f"/media/{id}-poster.jpg") if id.startswith("ads/") else (f"/media/freel/web/{id}.mp4", f"/media/freel/{id}-poster.jpg")
    return f'<div class="vid"><video src="{src}" poster="{poster}" muted loop playsinline autoplay preload="metadata"></video><span class="lab">{e(label)}</span><span class="snd">🔇 tap for sound</span></div>'

def page(slug, p):
    rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in p["sample_rows"])
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"] + FAQ_COMMON)
    free = '<p class="free">Not ready? <a href="/brain/">Try the free AI Front Desk first</a>.</p>' if slug == "autopilot" else f'<p class="free">Not ready to buy? <a href="/g/{p["guide"]}/">Try the free guide first</a>.</p>' if p["guide"] else '<p class="free">Not ready to buy? <a href="/free/">Every kit has a free guide</a>.</p>'
    items = ""
    if p.get("items"):
        items = '<h2>What\'s in the bundle</h2><div class="items">' + "".join(f'<a href="/store/{s}/"><b>{e(P[s]["name"])}</b><span>{e(P[s]["short"])}</span></a>' for s in p["items"]) + "</div>"
    got = ("A PDF with the setup agent, the 15 interview questions, the Autopilot instructions (9 commands), a worked example, message templates, a cheat sheet and a time back tracker." if slug == "autopilot" else KIT) if not p.get("bundle") else f"{KIT[:-1]}, for each kit, plus the Pro setup that installs them together in one Claude Project."
    og = f"https://autopilotoi.app/store/{slug}-cover.png" if os.path.exists(f"{ROOT}/docs/store/{slug}-cover.png") else "https://autopilotoi.app/logo.png"
    return HEAD(f"{p['name']} · {p['price']} · AUTOPILOT.OI", p["lead"], f"https://autopilotoi.app/store/{slug}/", og) + f"""
<div class="hd"><a href="/"><img src="/logo.png" alt=""></a><b>AUTOPILOT.OI</b><a class="bk" href="/store/">← Store</a></div>
<div class="tag">{'Claude setup · one time' if slug == 'autopilot' else 'Claude prompt kit'} · {p['price']}{' · bundle' if p.get('bundle') else ''}</div>
<h1>{(e(p['title'].split('|')[0]) + '<br><em>' + e(p['title'].split('|')[1]) + '</em>') if '|' in p['title'] else e(p['title'])}</h1>
<p class="lead">{e(p['lead'])}</p>
<a class="buy" href="{GR}{p['buy']}">Get {"" if slug == "autopilot" else "the "}{e(p['name'])} · {p['price']}</a>
<p class="sm">{'$19.99 once · instant download · free Claude plan works · 30 day refund' if slug == 'autopilot' else "Instant download · works on Claude's free plan"}{(' · ' + p['sep'] + ' separately') if p.get('sep') else ''}</p>
{('<div class="inside"><b>What you get</b><ul>' + li(p['inside']) + '</ul></div>') if p.get('inside') else ''}
{video_block(p['video'], 'Watch it work · sample data')}
{items}
<h2>It's for you if</h2><ul>{li(p['who'])}</ul>
<h2>What it looks like</h2><div class="box"><p class="note">{e(p['sample_note'])}</p>
<div class="tbl"><table><tr>{''.join(f'<th>{e(h)}</th>' for h in p['sample_head'])}</tr>{rows}</table></div>
<div class="after">{''.join(f'<p>{e(x)}</p>' for x in p['sample_after'])}</div></div>
<h2>How it works</h2><div class="steps">{"".join(f'<div class="step"><i>{i+1}</i><div><b>{e(a)}</b><p>{e(b)}</p></div></div>' for i, (a, b) in enumerate(p.get("how", HOW)))}</div>
<h2>What it does</h2><ul class="yes">{li(p['does'])}</ul>
<h2>What it doesn't do</h2><ul class="no">{li(p['doesnt'])}</ul>
<h2>What you need</h2><ul>{li(p['need'])}</ul>
<h2>What you get</h2><p>{e(got)}</p>
<h2>Questions</h2>{faq}
<a class="buy" href="{GR}{p['buy']}">Get {"" if slug == "autopilot" else "the "}{e(p['name'])} · {p['price']}</a>
{free}""" + FOOT

def card(slug):
    p = P[slug]
    th = f'<span class="th"><img src="/store/{slug}-thumb.png" alt=""></span>' if os.path.exists(f"{ROOT}/docs/store/{slug}-thumb.png") else f'<span class="th">{p["ic"]}</span>'
    return f'<a class="card" href="/store/{slug}/">{th}<div><b>{e(p["name"])}</b><p>{e(p["short"])}</p></div><span class="go">{p["price"]}</span></a>'

def index():
    money = "".join(card(s) for s in ["bill", "debt", "subs", "refund", "raise", "deposit"])
    tiktok = "".join(card(s) for s in ["video", "shop", "sell"])
    return HEAD("The store · Claude agents for real jobs · AUTOPILOT.OI", "Claude prompt kits from $10: money agents, TikTok agents and The Workspace for small businesses. Each one reads what you upload and drafts. You decide and send.", "https://autopilotoi.app/store/", "https://autopilotoi.app/store/all6-cover.png") + f"""
<div class="hd"><a href="/"><img src="/logo.png" alt=""></a><b>AUTOPILOT.OI</b><a class="bk" href="/">Home</a></div>
<div class="tag">The store · from $10</div>
<h1>Claude agents<br>for <em>real jobs.</em></h1>
<p class="lead">Each one runs in a Claude Project. It reads what you upload, checks it and drafts the reply, the plan or the letter. You decide and send. Every kit has a free guide you can try first.</p>
<nav class="flt"><a href="#money">Save money</a><a href="#tiktok">Grow on TikTok</a><a href="#business">Run a business</a><a href="/free/">Free guides</a></nav>
{video_block(advid('ap-a') or 'subs-agent', 'Autopilot · example business' if advid('ap-a') else 'Subscription Agent · sample data')}
<a class="hero" href="/store/autopilot/" style="margin-top:14px"><span class="tag">New · for any small business</span><span class="H">Autopilot<br>· $19.99</span><p>Learns your business in a 15 minute interview, then builds your systems in Claude: replies with your prices, quotes, follow ups, reviews, FAQ and your weekly plan. Every draft waits for your OK.</p><span class="btn">See Autopilot →</span><span class="sm">One time · 30 day refund</span></a>
<p class="sm">Every demo on this site is a real run on made-up data, with nothing cut out.</p>
<div class="cathd" id="money"><span class="tag">{e(CATS[0][1])}</span><h2>The money jobs you keep putting off</h2><p>{e(CATS[0][2])}</p></div>
<a class="hero" href="/store/money/"><span class="tag">Best value · all five</span><span class="H">All 5 Money<br>Agents · $39</span><p>Bill, Debt, Subscription, Refund and Raise Agent, plus the Pro setup that installs all 5 in one Claude Project in about 20 minutes.</p><span class="btn">See what's inside →</span><span class="sm">$50 separately · save $11</span></a>
<div class="tag" style="margin:18px 0 8px">Or pick one · $10 each</div>
<div class="grid">{money}</div>
<div class="cathd" id="tiktok"><span class="tag">{e(CATS[1][1])}</span><h2>Sell on TikTok without guessing</h2><p>{e(CATS[1][2])}</p></div>
<a class="hero" href="/store/tiktok/"><span class="tag">TikTok bundle · all three</span><span class="H">TikTok<br>Agents · $24</span><p>Video, Shop and Sales Agent: scripts and CapCut edit plans, profit checks and listing drafts, and reply drafts for comments and DMs.</p><span class="btn">See what's inside →</span><span class="sm">$30 separately · save $6</span></a>
<div class="tag" style="margin:18px 0 8px">Or pick one · $10 each</div>
<div class="grid">{tiktok}</div>
<div class="cathd" id="business"><span class="tag">{e(CATS[2][1])}</span><h2>Hand your busy work to a team</h2><p>{e(CATS[2][2])}</p></div>
<a class="hero" href="/store/autopilot/"><span class="tag">New · for any small business</span><span class="H">Autopilot<br>· $19.99</span><p>Learns your business in a 15 minute interview, then builds your systems in Claude: replies with your prices, quotes, follow ups, reviews, FAQ and your weekly plan. Every draft waits for your OK.</p><span class="btn">See Autopilot →</span><span class="sm">One time · 30 day refund</span></a>
<div style="height:10px"></div>
<a class="hero" href="/workspace/"><span class="tag">Hands off · $49</span><span class="H">The<br>Workspace</span><p>7 agent setups for customers, quotes, bookings and a morning brief. Drafts for your approval, never sends on its own. About an hour to set up. 30 day guarantee.</p><span class="btn">See The Workspace →</span></a>
<div class="grid" style="margin-top:10px"><a class="card" href="/brain/"><span class="th">🧠</span><div><b>AI Front Desk</b><p>Free: answer 10 questions, get a setup that replies with your real prices and rules</p></div><span class="go">FREE</span></a></div>
<h2>Good to know</h2>
<div class="trust"><div><b>Prompt kits, not apps</b>They run inside Claude. Nothing to install.</div><div><b>Free plan works</b>Claude's free plan allows 5 Projects.</div><div><b>You stay in control</b>They draft. They never send, post or pay.</div><div><b>Try before you buy</b><a href="/free/" style="color:var(--l)">Every kit has a free guide</a>.</div></div>
""" + FOOT

for slug, p in P.items():
    d = os.path.join(ROOT, "docs", "store", slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(page(slug, p))
os.makedirs(os.path.join(ROOT, "docs", "autopilot"), exist_ok=True)  # short link used in the ads
open(os.path.join(ROOT, "docs", "autopilot", "index.html"), "w").write(page("autopilot", P["autopilot"]))
open(os.path.join(ROOT, "docs", "store", "index.html"), "w").write(index())
print("built store:", ", ".join(P), "+ index")
