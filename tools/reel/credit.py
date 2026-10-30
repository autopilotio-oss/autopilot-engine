from common import *
TAIL = 0.9; CAPEND_PHRASE = None
PHRASES = [("One in five people have an error on their credit report.", ["one", "in", "five", "error"]),
 ("Here's how to fix yours with a Claude agent.", ["claude", "agent"]),
 ("Pull all three reports free at AnnualCreditReport.com", ["free"]),
 ("Upload them to Claude and type:", []),
 ("find every error and tell me what to dispute.", ["every", "error"]),
 ("It even writes your dispute letters.", ["dispute", "letters"]),
 ("Then turn it into your Credit Agent.", ["credit", "agent"]),
 ("Every month it checks your new reports,", ["every", "month"]),
 ("tracks every dispute,", []),
 ("and tells you your next move.", ["next", "move"]),
 ("No credit repair company.", ["no"]),
 ("Comment CREDIT and I'll send you the full setup, free.", ["credit", "free"])]
GROUPS = [[0], [1], [2], [3, 4], [5], [6], [7], [8, 9], [10], [11]]
MOODS = [(0, 1, "skep"), (4, 5, "skep"), (6, 7, "star"), (10, 11, "skep"), (11, 99, "star")]
rep = lambda r, t, f: f'<div class="row" data-in="{t}" style="padding:16px 26px;font-size:27px"><span>{r}</span><span class="flag" style="margin-left:auto">{f}</span></div>'
SCENES = [
 (0, "THE PROBLEM", '''<div style="position:absolute;left:0;right:0;top:-20px;text-align:center" data-in="@0+0.0"><div class="big" style="font-size:290px;color:var(--l);text-shadow:0 0 80px rgba(212,255,58,.35)">1 IN 5</div><div class="mono dim" style="font-size:22px;margin-top:-6px">PEOPLE HAVE AN ERROR ON A CREDIT REPORT</div></div>
 <div class="card" data-in="@0+1.3" style="position:absolute;left:130px;right:130px;top:350px;padding:8px 0">
  <div class="mono" style="padding:18px 26px;color:var(--l)">CREDIT REPORT</div>''' + rep("Late payment · Mar", "@0+1.6", "ERROR?") + rep("Collection · $1,240", "@0+1.9", "ERROR?") + '''</div>
 <div data-in="@1+0.0" style="position:absolute;left:0;right:0;top:640px;text-align:center"><span class="chip on" style="font-size:26px">✳ FIX IT WITH A CLAUDE AGENT</span></div>'''),
 (2, "FREE REPORTS", '''<div style="position:absolute;left:70px;right:70px;top:0;display:flex;gap:18px">''' + "".join(f'<div class="card" data-in="@2+{0.15+i*0.25:.2f}" style="flex:1;padding:26px 18px;text-align:center"><div class="sticker" style="font-size:44px">{n}</div><div class="ln"></div><div class="ln" style="width:70%"></div><div class="ln" style="width:85%"></div><div class="chip on" data-in="@2+{1.0+i*0.3:.2f}" style="font-size:16px;padding:8px 14px;margin-top:10px">PDF ✓</div></div>' for i, n in enumerate(["EQUIFAX", "EXPERIAN", "TRANSUNION"])) + '''</div>
 <div data-in="@2+1.2" style="position:absolute;left:0;right:0;top:360px;text-align:center"><span class="sticker" style="font-size:96px;background:#F4F4F0;color:#0A0A0A;border-radius:18px;padding:14px 30px 4px;display:inline-block;transform:rotate(-2deg)">FREE · EVERY WEEK</span></div>
 <div data-in="@2+1.6" style="position:absolute;left:0;right:0;top:540px;text-align:center"><span class="chip" style="font-size:26px">annualcreditreport.com</span></div>'''),
 (3, "ONE PROMPT", ex + '''<div class="card" data-in="@3+0.0" style="position:absolute;left:90px;right:90px;top:0;padding:22px 24px;display:flex;align-items:center;gap:16px">
  <div style="flex:1;font-size:31px;font-weight:600;min-height:84px"><span data-type="@4-0.1,1.3" data-text="Find every error and tell me what to dispute."></span><span style="color:var(--l)">|</span></div>
  <div data-press="@4+1.3" style="width:64px;height:64px;border-radius:18px;background:var(--l);display:grid;place-items:center;font-size:30px;color:var(--d);font-weight:900;flex:none">↑</div></div>
 <div class="card lit" data-in="@4+1.5" style="position:absolute;left:90px;right:90px;top:170px;padding-bottom:8px">
  <div style="display:flex;align-items:center;padding:24px 26px"><span class="mono" style="color:var(--l)">✳ CLAUDE FOUND 3 ITEMS</span></div>''' + rep("Late payment reported twice", "@4+1.8", "DUPLICATE") + rep("Paid balance still showing", "@4+2.1", "WRONG") + rep("Account you don't recognize", "@4+2.4", "CHECK") + "</div>"),
 (5, "DISPUTE LETTERS", '''<div class="card" data-in="@5+0.0" style="position:absolute;left:150px;right:150px;top:0;padding:34px 40px;background:#F4F4F0;color:#0A0A0A">
  <div class="mono" style="font-size:18px;color:#555">TO: TRANSUNION · RE: DISPUTE</div>
  <div style="font-size:26px;line-height:1.45;margin-top:18px">I'm writing to dispute the late payment reported for the account ending 4417. My records show it was paid on time. Please investigate and correct this item under the Fair Credit Reporting Act.</div>
  <div class="ln" style="background:#ddd;width:60%"></div><div class="ln" style="background:#ddd;width:40%"></div></div>
 <div data-in="@5+0.9" data-base="rotate(-6deg)" style="position:absolute;right:120px;top:430px"><span class="sticker" style="font-size:72px;color:var(--d);background:var(--l);border-radius:16px;padding:12px 26px 2px;display:inline-block;box-shadow:0 0 60px rgba(212,255,58,.5)">READY TO SEND</span></div>'''),
 (6, "YOUR CREDIT AGENT", ex + agent("CREDIT AGENT", [("@7+0.0", "NOV 1", "New reports checked · 1 change"), ("@8+0.0", "DISPUTE #2", "Day 24 of 30 · follow up ready"), ("@9+0.0", "NEXT MOVE", "Pay card 2 under 30%")], 6)),
 (10, "NO MIDDLEMAN", '''<div style="position:absolute;left:0;right:0;top:40px;text-align:center"><div style="position:relative;display:inline-block" data-in="@10+0.0"><span class="sticker" style="font-size:110px;color:#cfcfc8">CREDIT REPAIR<br>COMPANY</span><div class="redx" data-strike="@10+0.5"></div></div></div>
 <div data-in="@10+0.8" style="position:absolute;left:0;right:0;top:420px;text-align:center"><span class="chip on" style="font-size:30px">DO IT YOURSELF · FREE</span></div>'''),
 (11, "COMMENT CREDIT", cta("CREDIT", "Here you go 💳 your free Credit Agent setup → link", 11)),
]
