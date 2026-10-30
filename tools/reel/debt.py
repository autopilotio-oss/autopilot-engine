from common import *
TAIL = 0.9; CAPEND_PHRASE = None
PHRASES = [("Your card company might lower your interest rate if you just ask.", ["lower", "just", "ask"]),
 ("Most people never call.", ["never"]),
 ("Give Claude your balances and rates.", ["balances", "rates"]),
 ("It writes the call script,", ["call", "script"]),
 ("then builds the fastest payoff plan for your exact numbers.", ["fastest", "payoff", "plan"]),
 ("Then set it up as your Debt Agent.", ["debt", "agent"]),
 ("Every payday it tells you exactly what to pay,", ["every", "payday"]),
 ("and how much interest you're saving.", ["saving"]),
 ("Comment DEBT and I'll send you the full setup, free.", ["debt", "free"])]
GROUPS = [[0], [1], [2], [3], [4], [5], [6], [7], [8]]
MOODS = [(0, 1, "wide"), (1, 2, "skep"), (4, 5, "star"), (8, 99, "star")]
row = lambda t, n, b, r: f'<div class="row" data-in="{t}" style="padding:16px 26px;font-size:28px"><span style="min-width:230px">{n}</span><span style="font-weight:700">{b}</span><span class="mono" style="margin-left:auto;color:#ff8a8a;font-size:22px">{r}</span></div>'
bar = lambda t, n, f, to, p: f'<div data-in="{t}" style="margin-top:22px"><div style="display:flex;font-size:26px;font-weight:600"><span>{n}</span><span class="mono dim" style="margin-left:auto;font-size:18px">{p}</span></div><div class="barw"><i data-bar="{t}+0.4,1.6,{f},{to}"></i></div></div>'
SCENES = [
 (0, "THE ASK", ex + '''<div class="card" data-in="@0+0.0" style="position:absolute;left:150px;right:150px;top:0;padding:30px 40px;text-align:center">
  <div class="mono dim">YOUR CARD'S APR</div><div style="position:relative;display:inline-block"><div class="big" style="font-size:200px;color:#ff8a8a">29.99%</div><div class="redx" data-strike="@0+2.0"></div></div></div>
 <div data-in="@0+2.4" data-base="rotate(-4deg)" style="position:absolute;left:0;right:0;top:400px;text-align:center"><span class="sticker" style="font-size:110px;background:var(--l);color:var(--d);border-radius:18px;padding:14px 34px 4px;display:inline-block;box-shadow:0 0 70px rgba(212,255,58,.5)">JUST ASK</span></div>'''),
 (1, "MOST NEVER CALL", '''<div class="card" data-in="@1+0.0" style="position:absolute;left:190px;right:190px;top:0;padding:34px;text-align:center">
  <svg viewBox="0 0 24 24" style="width:96px;height:96px;fill:none;stroke:#D4FF3A;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 18px rgba(212,255,58,.6))"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg><div style="font-size:34px;font-weight:700;margin-top:6px">Card services</div><div class="mono dim" style="font-size:20px;margin-top:8px">NO CALLS MADE</div></div>
 <div data-in="@1+0.5" style="position:absolute;left:0;right:0;top:400px;text-align:center"><span class="sticker" style="font-size:90px;background:#F4F4F0;color:#0A0A0A;border-radius:18px;padding:12px 28px 2px;display:inline-block;transform:rotate(-2deg)">MOST PEOPLE NEVER CALL</span></div>'''),
 (2, "YOUR NUMBERS", ex + '''<div class="card" data-in="@2+0.0" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:8px"><div class="mono" style="padding:22px 26px;color:var(--l)">YOUR CARDS</div>''' + row("@2+0.4", "Visa", "$4,200", "29.99%") + row("@2+0.7", "Mastercard", "$1,850", "24.49%") + row("@2+1.0", "Store card", "$640", "31.99%") + "</div>"),
 (3, "CALL SCRIPT", '''<div class="card" data-in="@3+0.0" style="position:absolute;left:90px;right:90px;top:0;padding:28px 32px">
  <div class="mono" style="color:var(--l)">✳ CALL SCRIPT</div>''' + "".join(f'<div data-in="@3+{0.3+i*0.35:.2f}" style="font-size:30px;line-height:1.35;margin-top:18px;padding-left:20px;border-left:4px solid var(--l)">{s}</div>' for i, s in enumerate(["I've been a customer since 2019.", "I've paid on time every month.", "Can you lower my APR?"])) + "</div>"),
 (4, "PAYOFF PLAN", ex + '''<div class="card lit" data-in="@4+0.0" style="position:absolute;left:90px;right:90px;top:0;padding:26px 30px 32px">
  <div style="display:flex;align-items:center"><span class="mono" style="color:var(--l)">✳ FASTEST PAYOFF PLAN</span><span class="chip on" style="margin-left:auto;font-size:15px;padding:7px 12px">HIGHEST APR FIRST</span></div>''' + bar("@4+0.0", "Store card", 100, 0, "PAID · MONTH 3") + bar("@4+0.5", "Visa", 100, 35, "MONTH 14") + bar("@4+0.8", "Mastercard", 100, 60, "MONTH 19") + '''
  <div data-in="@4+2.0" style="margin-top:26px;text-align:center"><span class="sticker" style="font-size:64px;color:var(--l)">DEBT FREE · MONTH 19</span></div></div>'''),
 (5, "YOUR DEBT AGENT", ex + agent("DEBT AGENT", [("@6+0.0", "PAYDAY", "Pay $410 on the Store card"), ("@6+0.7", "THE REST", "Minimums on Visa and Mastercard")], 5) + '''
 <div class="card" data-in="@7+0.0" style="position:absolute;left:90px;right:90px;top:430px;padding:24px 30px;display:flex;align-items:center"><span class="mono" style="color:var(--l)">INTEREST SAVED SO FAR</span><span class="big" style="margin-left:auto;font-size:76px;color:var(--l)" data-count="@7+0.0,1.2,0,612" data-pre="$">$0</span></div>'''),
 (8, "COMMENT DEBT", cta("DEBT", "Here you go 💸 your free Debt Agent setup → link", 8)),
]
