from common import *
TAIL = 0.9; CAPEND_PHRASE = None
PHRASES = [("You're probably paying for a subscription you forgot about.", ["forgot"]),
 ("Download three months of bank statements and black out the account numbers.", ["three", "months", "black", "out"]),
 ("Upload them to Claude and type:", ["claude"]),
 ("find every recurring charge and what I save by canceling.", ["every", "recurring", "save"]),
 ("It lists each one, the yearly cost, and how to cancel.", ["yearly", "cancel"]),
 ("Then it writes the cancel message for you.", ["cancel", "message"]),
 ("Now make it your Subscription Agent,", ["subscription", "agent"]),
 ("and it checks every month for new charges.", ["every", "month"]),
 ("Comment SUBS and I'll send you the full setup, free.", ["subs", "free"])]
GROUPS = [[0], [1], [2, 3], [4], [5], [6], [7], [8]]
MOODS = [(0, 1, "skep"), (3, 4, "wide"), (6, 8, "star"), (8, 99, "star")]
li = lambda n, d, p, t: f'<div class="row" data-in="{t}" style="padding:14px 26px;font-size:26px"><span>{n}</span><span class="mono dim" style="font-size:18px;margin-left:18px">{d}</span><span style="margin-left:auto;font-weight:700">{p}</span></div>'
SCENES = [
 (0, "THE LEAK", '''<div style="position:absolute;left:0;right:0;top:20px;text-align:center" data-in="@0+0.0"><span class="sticker" style="font-size:120px;color:#F4F4F0">FORGOTTEN<br>SUBSCRIPTIONS</span></div>
 <div data-in="@0+1.2" data-base="rotate(-5deg)" style="position:absolute;left:0;right:0;top:380px;text-align:center"><span class="sticker" style="font-size:90px;background:#ff4d4d;color:#160404;border-radius:18px;padding:14px 30px 4px;display:inline-block">STILL CHARGING</span></div>'''),
 (1, "STATEMENTS", ex + '''<div class="card" data-in="@1+0.0" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:8px"><div class="mono" style="padding:22px 26px;color:var(--l)">BANK STATEMENT · ACCT ████████</div>''' + li("STREAMFLIX", "monthly", "$15.49", "@1+0.3") + li("CLOUD STORAGE", "monthly", "$2.99", "@1+0.5") + li("FIT APP", "monthly", "$12.99", "@1+0.7") + li("NEWS PLUS", "monthly", "$9.99", "@1+0.9") + "</div>"),
 (2, "ONE PROMPT", ex + '''<div class="card lit" data-in="@2+0.2" style="position:absolute;left:90px;right:90px;top:0;padding:30px 32px;font-size:34px;line-height:1.35">Find every recurring charge and what I save by canceling.</div>'''),
 (4, "THE LIST", ex + '''<div class="card lit" data-in="@4+0.0" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:8px"><div class="mono" style="padding:22px 26px;color:var(--l)">✳ CLAUDE FOUND 4</div>''' + li("STREAMFLIX", "per year", "$186", "@4+0.3") + li("FIT APP", "per year", "$156", "@4+0.55") + li("NEWS PLUS", "per year", "$120", "@4+0.8") + li("CLOUD STORAGE", "per year", "$36", "@4+1.05") + "</div>"),
 (5, "CANCEL MESSAGE", '''<div class="card" data-in="@5+0.0" style="position:absolute;left:90px;right:90px;top:0;padding:28px 32px">
  <div class="mono" style="color:var(--l)">CANCEL MESSAGE · READY</div>''' + "".join(f'<div data-in="@5+{0.4+i*0.45:.2f}" style="font-size:30px;line-height:1.35;margin-top:20px;padding-left:20px;border-left:4px solid var(--l)">{s}</div>' for i, s in enumerate(["Please cancel my membership today.", "Confirm in writing there are no more charges.", "Refund any charge after this date."])) + "</div>"),
 (6, "YOUR SUBS AGENT", ex + agent("SUBS AGENT", [("@6+0.6", "THIS MONTH", "4 subscriptions checked"), ("@7+0.0", "NEW CHARGE", "Flagged · cancel message ready"), ("@7+0.6", "STATUS", "Nothing slips through")], 6)),
 (8, "COMMENT SUBS", cta("SUBS", "Here you go ✂️ your free Subscription Agent setup → link", 8)),
]
