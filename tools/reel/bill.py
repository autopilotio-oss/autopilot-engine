from common import *
TAIL = 0.9; CAPEND_PHRASE = None
PHRASES = [("Never pay a medical bill without doing this first.", ["never", "first"]),
 ("Ask for the itemized bill.", ["itemized"]),
 ("Upload it to Claude with your insurance statement and type:", ["insurance", "statement"]),
 ("compare these and find every error.", ["every", "error"]),
 ("Then it writes your call script to ask for financial assistance.", ["call", "script", "financial", "assistance"]),
 ("Most nonprofit hospitals are required to have a program.", ["required"]),
 ("Now make it your Bill Agent,", ["bill", "agent"]),
 ("and every bill gets checked before you pay a cent.", ["before"]),
 ("Comment BILL and I'll send you the full setup, free.", ["bill", "free"])]
GROUPS = [[0], [1], [2, 3], [4], [5], [6], [7], [8]]
MOODS = [(0, 1, "skep"), (3, 4, "wide"), (6, 8, "star"), (8, 99, "star")]
li = lambda c, n, p, t, hi="": f'<div class="row" data-in="{t}" style="padding:14px 26px;font-size:26px;{hi}"><span class="mono dim" style="font-size:18px;min-width:96px">{c}</span><span>{n}</span><span style="margin-left:auto;font-weight:700">{p}</span></div>'
fl = lambda t, f, txt, ok=False: f'<div class="row" data-in="{t}" style="padding:16px 26px;font-size:26px"><span class="flag{" ok" if ok else ""}">{f}</span><span>{txt}</span></div>'
SCENES = [
 (0, "THE BILL", ex + '''<div class="card" data-in="@0+0.0" style="position:absolute;left:150px;right:150px;top:0;padding:34px 40px;background:#F4F4F0;color:#0A0A0A">
  <div class="mono" style="font-size:18px;color:#555">RIVERSIDE MEDICAL CENTER · STATEMENT</div>
  <div class="mono" style="font-size:18px;color:#555;margin-top:30px">AMOUNT DUE</div>
  <div class="big" style="font-size:170px" data-count="@0+0.3,1.4,0,4812" data-pre="$">$0</div>
  <div class="ln" style="background:#ddd"></div><div class="ln" style="background:#ddd;width:60%"></div></div>
 <div data-in="@0+1.5" data-base="rotate(-5deg)" style="position:absolute;left:0;right:0;top:470px;text-align:center"><span class="sticker" style="font-size:96px;background:#ff4d4d;color:#160404;border-radius:18px;padding:14px 30px 4px;display:inline-block">DON'T PAY YET</span></div>'''),
 (1, "GET IT ITEMIZED", ex + '''<div class="card" data-in="@1+0.0" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:8px"><div class="mono" style="padding:22px 26px;color:var(--l)">ITEMIZED BILL</div>''' + li("99284", "ER visit", "$1,920", "@1+0.0") + li("36415", "Blood draw", "$86", "@1+0.35") + li("36415", "Blood draw", "$86", "@1+0.5") + li("71046", "Chest X-ray", "$410", "@1+0.65") + li("J1885", "Injection", "$240", "@1+0.8") + "</div>"),
 (2, "COMPARE", ex + '''<div style="position:absolute;left:90px;right:90px;top:0;display:flex;gap:18px">
  <div class="card" data-in="@2+0.0" style="flex:1;padding:24px"><div class="sticker" style="font-size:52px">BILL</div><div class="ln"></div><div class="ln" style="width:70%"></div></div>
  <div class="card" data-in="@2+0.35" style="flex:1;padding:24px"><div class="sticker" style="font-size:52px">INSURANCE</div><div class="ln"></div><div class="ln" style="width:70%"></div></div></div>
 <div class="card lit" data-in="@3+0.5" style="position:absolute;left:90px;right:90px;top:230px;padding-bottom:8px"><div class="mono" style="padding:22px 26px;color:var(--l)">✳ CLAUDE FLAGGED</div>''' + fl("@3+0.8", "DUPLICATE", "Blood draw billed twice") + fl("@3+1.1", "MISMATCH", "X-ray: insurance says $0 owed") + fl("@3+1.4", "ASK", "Why a level 4 ER visit?") + "</div>"),
 (4, "CALL SCRIPT", '''<div class="card" data-in="@4+0.0" style="position:absolute;left:90px;right:90px;top:0;padding:28px 32px">
  <div class="mono" style="color:var(--l)">CALL SCRIPT · BILLING OFFICE</div>''' + "".join(f'<div data-in="@4+{0.4+i*0.45:.2f}" style="font-size:30px;line-height:1.35;margin-top:20px;padding-left:20px;border-left:4px solid var(--l)">{s}</div>' for i, s in enumerate(["Do you have a financial assistance program?", "Can we review these 3 line items?", "Can I get a no interest payment plan?"])) + "</div>"),
 (5, "KNOW THIS", '''<div style="position:absolute;left:0;right:0;top:20px;text-align:center" data-in="@5+0.0"><span class="sticker" style="font-size:120px;color:#F4F4F0">NONPROFIT<br>HOSPITALS</span></div>
 <div data-in="@5+0.8" style="position:absolute;left:100px;right:100px;top:330px;text-align:center"><span class="chip on" style="font-size:26px;line-height:1.4;white-space:normal">MUST HAVE A FINANCIAL ASSISTANCE POLICY</span></div>'''),
 (6, "YOUR BILL AGENT", ex + agent("BILL AGENT", [("@6+0.6", "NEW BILL", "Riverside Medical · checked"), ("@7+0.0", "FOUND", "2 errors · call script ready"), ("@7+0.6", "STATUS", "Don't pay until it's fixed")], 6)),
 (8, "COMMENT BILL", cta("BILL", "Here you go 🧾 your free Bill Agent setup → link", 8)),
]
