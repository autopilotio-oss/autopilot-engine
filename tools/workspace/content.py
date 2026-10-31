# THE WORKSPACE course content. Plain copy rules: no dashes, no income claims, drafts not sends.
QUIZ = [
    ("Your business", "What's the business called, and what do you do in one sentence?"),
    ("You", "Your first name, and how you sign off messages (example: \"Sam, Shine Mobile Detail\")."),
    ("Where", "The city or area you serve. Any places you don't go?"),
    ("Services", "Every service you sell with its price or price range."),
    ("Extras", "Add ons, upgrades and what they cost."),
    ("Hours", "The days and hours you work. When are you closed?"),
    ("How people book", "How customers reach you: email, text, call, DM, website, booking link."),
    ("Booking rules", "Your booking link, deposit rule and how far ahead people can book."),
    ("Changes", "Your cancel and reschedule rules, and any late fee."),
    ("Payment", "How you get paid and when payment is due."),
    ("Top questions", "The 5 questions customers ask most, with your real answers."),
    ("Never say", "Things you never promise, never discount and never do."),
    ("Your voice", "3 words for how you sound, and paste one real message you sent a customer."),
    ("Your apps", "Your email app and calendar app (Gmail and Google Calendar work best)."),
    ("Leads", "Where new customers come from: Instagram, Facebook, Google, website, referrals."),
    ("Follow ups", "How many days before you nudge a quiet quote, and the most nudges you'll send."),
    ("Reviews", "Your Google review link (or wherever you want reviews)."),
    ("Invoices", "What goes on your invoice: business name, address, tax, payment terms."),
    ("Your day", "When you want your morning brief, and when you finish work."),
    ("Send to me", "What must always come straight to you: complaints, refunds, big jobs, anything legal."),
]

BUILDER = """You are my setup tech for THE WORKSPACE by AUTOPILOT.OI. Your job is to set up 7 AI agents for my business with me, one step at a time. I am not technical. Use short messages, tell me exactly what to tap, and wait for me after every step.

RULES
1. One step at a time. After each step, ask me "Done?" and wait.
2. Never ask me to type a password into this chat. Connections use the official sign in screens.
3. Every agent drafts. Nothing is sent to a customer without my OK.
4. If something on my screen looks different from what you expect, ask me to describe it or send a screenshot, then adjust.
5. If I type "I'm stuck", slow down and explain the step a different way.

STEP 1 · THE INTERVIEW
Ask me these 20 questions one at a time. Keep my exact words for prices and rules.
{quiz}

STEP 2 · THE BUSINESS BRAIN
Write my Business Brain from my answers using the template below. Show it to me and fix anything I correct. Then help me save it as a Google Doc named "Business Brain" in my Google Drive. If I can't use Google Drive, keep it in this Project's instructions instead and paste it into each agent's task.

STEP 3 · CONNECT MY APPS
Walk me through Settings, then Connectors, and connect Gmail, Google Calendar and Google Drive (or the apps I named). After each one, test it: read my 3 newest emails, list tomorrow's calendar, find the Business Brain doc. Tell me what worked.

STEP 4 · BUILD THE 7 AGENTS
For each agent below, fill in my details from the Business Brain, show me the finished task prompt and the schedule, and ask me to confirm. Then create it as a scheduled task (or help me create it under Scheduled, New task). For the on demand agents, save the prompt in this Project so I can run it from my phone.
{agents}

STEP 5 · MY PHONE
Help me install the Claude app on my phone, turn on notifications for finished tasks, and pin this Project. Then give me my 10 favorite commands from the phone command list, filled in for my business.

STEP 6 · TEST RUN
Run the Morning Brief and the Inbox Agent once right now. Show me the drafts. Ask me what to change, and update the prompts.

STEP 7 · HANDOFF
Give me a one screen summary: each agent, when it runs, what it drafts, and how to pause it. Remind me: everything drafts, I approve.

BUSINESS BRAIN TEMPLATE
{brain}

Start with: "Hi, I'm your setup tech. This takes about an hour and you can stop anytime. Question 1 of 20:" and ask question 1."""

BRAIN = """BUSINESS BRAIN · [Business name]
WHAT WE DO: [one sentence]
WHO I AM: [first name] · sign off: [sign off]
AREA: [city or area] · we don't go to: [places]
HOURS: [days and hours] · closed: [days]

SERVICES AND PRICES
[service]: [price] · [what's included]
[service]: [price] · [what's included]
EXTRAS: [add on]: [price]

BOOKING
How people book: [channels]
Booking link: [link] · deposit: [rule] · book up to [x] days ahead
Cancel or reschedule: [rule] · late fee: [fee]
Payment: [methods] · due: [when]

ANSWERS TO COMMON QUESTIONS
1. [question]: [answer]
2. [question]: [answer]
3. [question]: [answer]
4. [question]: [answer]
5. [question]: [answer]

NEVER
Never promise: [list] · never discount: [list] · never do: [list]

VOICE
Sounds: [3 words] · example: "[real message]"

FOLLOW UPS: nudge after [x] days · max [y] nudges
REVIEW LINK: [link]
INVOICE: [name, address, tax, terms]
MY DAY: brief at [time] · I finish at [time]
ALWAYS SEND TO ME (no draft): [complaints, refunds, jobs over $x, legal]"""

HEAD = "Open the Google Doc \"Business Brain\" in my Google Drive and follow it exactly: prices, rules, voice and the ALWAYS SEND TO ME list. Never invent a price or a promise. If something isn't in the Brain, say \"Needs you\" instead of guessing. Never send anything. Only draft."

AGENTS = [
    dict(n="01", name="Morning Brief", when="Every day at 6:00 AM (your time)", kind="Scheduled",
         job="Your day in one message before you start.",
         prompt=HEAD + """

Make my morning brief:
1. TODAY: every event on my Google Calendar today with time, customer and job.
2. NEEDS YOU: new customer emails since yesterday at 5 PM, quotes with no reply after the follow up days in the Brain, and anything on the ALWAYS SEND TO ME list.
3. DRAFTS READY: a count of drafts the other agents made since yesterday.
4. ONE IDEA: one specific move for today based on open calendar time and past customers.
Keep it under 15 lines. Plain words. No greeting longer than one line."""),
    dict(n="02", name="Inbox Agent", when="Weekdays at 7:00 AM, 12:00 PM and 5:00 PM", kind="Scheduled",
         job="A reply drafted for every new customer email.",
         prompt=HEAD + """

Check my Gmail for customer emails that arrived since the last run and have no reply from me. Skip newsletters, receipts and spam.
For each one, write a reply in my voice using only the prices, hours and rules in the Brain. Offer 2 real open times from my calendar when they want to book.
Save each reply as a Gmail draft on that thread if you can. If you can't, list them here, each with the customer's name, their question in one line and the full draft.
Anything on the ALWAYS SEND TO ME list: no draft, put it at the top marked NEEDS YOU."""),
    dict(n="03", name="Booking Agent", when="On demand, plus every evening at 8:00 PM", kind="Both",
         job="Turns a text into a booking and drafts tomorrow's reminders.",
         prompt=HEAD + """

ON DEMAND: when I write something like "Book Dre, full detail, Saturday 1pm", check my calendar for a conflict, then add the event (ask me first) with the customer, service, price and address. Draft the confirmation message for me to send. If you can't add the event, give me the details ready to paste.
EVERY EVENING: list tomorrow's bookings and draft a short reminder for each with time, address and the cancel rule from the Brain."""),
    dict(n="04", name="Follow Up Agent", when="Weekdays at 10:00 AM", kind="Scheduled",
         job="Quotes that went quiet get one friendly nudge.",
         prompt=HEAD + """

Search my sent Gmail for quotes and price replies older than the follow up days in the Brain with no answer from the customer.
For each, draft one short nudge that answers the most likely objection and gives one simple next step (a time or the booking link). Respect the max nudges in the Brain: if we hit it, list the customer as CLOSED instead.
Save drafts in Gmail if you can, otherwise list them here."""),
    dict(n="05", name="Invoice Agent", when="On demand", kind="On demand",
         job="\"Job plus price\" becomes a clean invoice.",
         prompt=HEAD + """

When I write "Invoice: [customer], [job], [price]", make an invoice with my invoice details from the Brain, an invoice number (date plus customer initials), the line items, tax if the Brain says so, the total, and the payment terms.
Give it to me as a clean document I can save as a PDF, plus a short email to send with it. Never mark anything paid."""),
    dict(n="06", name="Review Agent", when="Every day at 7:00 PM", kind="Scheduled",
         job="Everyone you finished today gets a thank you that asks for a review.",
         prompt=HEAD + """

Look at today's finished jobs on my Google Calendar. For each customer, draft a 3 sentence thank you in my voice that mentions the job and asks for a review with my review link from the Brain.
Never offer anything in exchange for a review. Skip anyone marked as a complaint."""),
    dict(n="07", name="DM Assistant", when="On demand", kind="On demand",
         job="Replies for your Instagram and Facebook inbox.",
         prompt=HEAD + """

When I paste a DM or a screenshot of my inbox, draft a reply for each message in my voice. Keep DMs short: 1 to 3 sentences, one question at a time, and the booking link when they're ready.
If I'm using Claude in Chrome with my inbox open, you may type the reply into the box, but never press send. I review and tap send myself."""),
]

COMMANDS = [
    ("Booking", ["Book [name], [service], [day] [time] at [address]", "Move [name] to [day] [time] and draft the message",
                 "What's open this week for a 2 hour job?", "Draft reminders for tomorrow's customers",
                 "[Name] cancelled. Draft a reply with my cancel rule", "Who's booked Saturday?",
                 "Block off [day] for me and draft a note to anyone booked"]),
    ("Customers", ["Draft a reply to [name]'s last email", "Any customer emails I haven't answered?",
                   "Answer this for me: [paste message]", "Write a price reply for [service] to [name]",
                   "Draft a friendly no for this request: [paste]", "Turn this voice note into a reply: [paste]",
                   "Write a welcome message for a new customer", "Draft a reply to this DM: [paste]"]),
    ("Money", ["Invoice: [name], [job], [price]", "Quote [service] for [name] with [extras]",
               "Which quotes are still open?", "Draft a polite payment reminder for [name]",
               "List this week's jobs and totals from my calendar", "Draft a deposit request for [name]",
               "Rewrite my prices list to look clean for a text"]),
    ("Follow ups", ["Nudge everyone who went quiet this week", "Draft a rebook message for [name], last job [date]",
                    "Who hasn't booked in 3 months? Draft a check in for each", "Draft a review ask for [name]",
                    "Write a thank you for [name] who referred a friend", "Draft a slow week offer for past customers",
                    "Follow up on [name]'s quote with one new reason to book"]),
    ("My day", ["Run my Morning Brief now", "What needs me today?", "Plan my day around [errand]",
                "What did my agents draft today?", "Summarize my inbox in 5 lines",
                "What's my first job tomorrow and where?", "Give me a 3 line end of day recap"]),
    ("The Brain", ["Add to my Business Brain: [new price or rule]", "Change my price for [service] to [price]",
                   "Add this answer to my common questions: [paste]", "I'm closed [dates]. Update the Brain and draft a notice",
                   "Show me my Business Brain", "Make my voice a bit more [friendly / short / formal]",
                   "What's missing from my Business Brain?"]),
    ("Control", ["Pause my Review Agent for a week", "Show my scheduled tasks and when they run",
                 "Change my Morning Brief to [time]", "Turn the Inbox Agent off on weekends",
                 "Why did you draft this? Show me the rule you used", "Undo the last change to my Business Brain",
                 "Give me a weekly report of what each agent did"]),
]

NIGHT = [
    ("Scheduled tasks need a paid plan.", "Scheduled tasks are on Claude's paid plans (Pro and up). The free plan can still run every agent on demand from your phone."),
    ("They run in the cloud.", "Scheduled tasks run on Anthropic's side on their schedule, even when your computer is asleep or the app is closed. Some setups also offer local tasks that run on your computer: pick the regular scheduled task so it doesn't depend on your laptop."),
    ("Check the Scheduled page.", "In the Claude app, open Scheduled in the sidebar. You'll see every agent, its next run and past runs. Tap a run to read what it drafted."),
    ("Turn on notifications.", "On your phone, allow notifications for the Claude app so you know when a run finishes."),
    ("Pick quiet times.", "Run the Inbox Agent while you're working so drafts are fresh, and the Review Agent after your last job."),
    ("Start small.", "Turn on the Morning Brief and Inbox Agent first. Add one agent a day once you trust the drafts."),
]

FIX = [
    ("An agent says it can't see my email or calendar.", "Open Settings, then Connectors, and reconnect Gmail or Google Calendar. Then run the task once by hand."),
    ("A draft has the wrong price.", "The Brain is the only source. Say \"Change my price for [service] to [price]\" and check the Business Brain doc saved."),
    ("A task didn't run.", "Open Scheduled and check it's on and the time is right. Plans and features change: if the task shows an error, run it by hand and send Claude the error."),
    ("Drafts don't show in Gmail.", "Your connector may not save drafts. The drafts are in the task's result instead. Copy from there."),
    ("It sounds like a robot.", "Paste 3 real messages you sent and say \"Use these as my voice from now on\" so it updates the Brain."),
    ("It answered something it shouldn't.", "Add it to NEVER or ALWAYS SEND TO ME in the Brain. Agents follow the Brain first."),
    ("Too many drafts.", "Run the Inbox Agent less often, or tell it to skip anything that isn't a customer."),
    ("I'm stuck in setup.", "Type \"I'm stuck\" and describe your screen, or send a screenshot. The Builder explains the step another way."),
]

SAFETY = [
    "Drafts only. You approve every message before it goes to a customer.",
    "Never type a password, card number or bank login into a chat. Connect apps through the official sign in screens.",
    "Keep \"ask before acting\" on for sending, deleting and calendar changes.",
    "The Brain is the truth. If a price or rule changes, update the Brain first.",
    "Complaints, refunds, legal questions and big jobs go to you, not to a draft.",
    "Read the first week of drafts closely. Fix the Brain until the drafts need no edits.",
    "You can pause any agent from the Scheduled page, and disconnect any app in Settings, Connectors.",
    "Claude can make mistakes. You run the business. The agents do the typing.",
]

# Sample output (made up mobile detailing business) and one tuning tip per agent, shown on each agent page.
EXAMPLES = {
    "01": ("Good morning. Tuesday.\nTODAY\n9:00  Full detail, 2021 Tacoma (Maria, Clifton)\n1:30  Interior only, Civic (new customer)\nNEEDS YOU\n2 new leads overnight. Replies drafted.\nQuote to Dave ($240 ceramic) is 3 days quiet. Nudge drafted.\nONE IDEA\nThursday 3 PM is open. 4 past customers are due for a wash. Want a text offering the slot?",
           "Want it shorter? Say \"Morning Brief: max 8 lines, jobs first.\""),
    "02": ("Lead, 11:42 PM: \"How much for an interior clean on a minivan? Kids destroyed it lol\"\nDraft: \"Ha, we see that a lot. Interior for a minivan starts at $160, and heavy stains are $30 extra if needed. I have Wednesday at 10 or Thursday at 2. Want one of those?\"",
           "Add your best 5 answers to the Brain. Drafts get better every time you do."),
    "03": ("You: \"Book Dre, full detail, Saturday 1pm, 14 Oak St\"\nAgent: \"Saturday 1:00 PM is free. Add it to your calendar? Confirmation draft: Hi Dre, you're set for a full detail Saturday at 1 PM at 14 Oak St. $180, paid on finish. Need to move it? Just reply 24 hours ahead.\"",
           "Put your travel time between jobs in the Brain so it never double books you."),
    "04": ("Dave, quote sent 3 days ago, no reply.\nDraft: \"Hi Dave, just checking in on the ceramic coating quote for your F150. I still have Friday morning open, and the $240 price holds through the end of the month. Any questions I can answer?\"",
           "One nudge is usually enough. Set max nudges to 2 so you never sound pushy."),
    "05": ("INVOICE 2026-11-04-MG\nShine Mobile Detail · Clifton NJ\nMaria Gomez · Full detail, 2021 Tacoma · $180\nCeramic spray add on · $40\nTOTAL $220 · due on receipt · Zelle or card",
           "Ask it for your invoice in the same format every time: \"Use my last invoice as the template.\""),
    "06": ("\"Thanks again for trusting us with the Tacoma today, Maria. It was a fun one to bring back. If you have a minute, a quick Google review helps a small shop like ours a lot: [your link]\"",
           "Send review asks the same day. Memories fade fast."),
    "07": ("DM: \"do u do boats??\"\nDraft: \"We don't do boats yet, sorry! Cars, trucks and SUVs only. If you've got one of those, here's the booking link: [link]\"",
           "Keep DMs to 1 to 3 sentences. Short replies get answered."),
}
