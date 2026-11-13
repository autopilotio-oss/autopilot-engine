"""Builds the everyday-people homepage (docs/index.html) and the free Prompt Vault (docs/vault/index.html)
from content/hub/week1_posts.json. The old business homepage lives at /business/. Run: python3 tools/site_hub.py"""
import json, html, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{R}/content/hub/week1_posts.json"))
ORDER = [("7","05_side_hustles","Find money in the skills you already have","7 prompts"),("23","09_bill_fighter","Fight your bills like a pro negotiator","7 scripts"),
 ("17","02_bank_statement","Read your bank statement like a financial advisor","7 prompts"),("10","01_job_agent","Find a better paying job while you sleep","Agent"),
 ("20","03_contract","Read any contract before you sign","7 prompts"),("25","04_night_shift","Put Claude on the night shift","Agent"),
 ("1","07_money_plan","Build your 10 year money plan","7 prompts"),("26","06_team_of_5","Hire a team of 5 AI employees","Agent"),
 ("3","10_interview_coach","Prep for any interview","Agent"),("16","08_six_agents","6 agents that replace an assistant","6 agents"),
 ("24","11_one_percent","Prompt Claude like the 1%","7 upgrades"),("18","12_black_friday","Plan your whole Black Friday","7 prompts")]
UP = {"09_bill_fighter":("bill-agent","Bill Agent"),"02_bank_statement":("subs-agent","Subscription Agent"),"07_money_plan":("debt-agent","Debt Agent"),
      "01_job_agent":("raise-agent","Raise Agent"),"10_interview_coach":("raise-agent","Raise Agent")}
AG = [("bill-agent","Bill Agent","Checks a medical bill against your insurance before you pay"),("debt-agent","Debt Agent","Payoff plan and the script to ask for a lower rate"),
      ("subs-agent","Subscription Agent","Lists the recurring charges on your statements, drafts the cancel messages"),("refund-agent","Refund Agent","Drafts refund requests that name your rights"),
      ("raise-agent","Raise Agent","Pay data, your number and a practice run with pushback")]
G = "https://autopilotoi.gumroad.com/l/"
e = html.escape
def br(t): return re.sub(r"\[(.*?)\]", r"<b>[\1]</b>", e(t))
HEAD = lambda title, desc, path: f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="https://autopilotoi.app/media/hub/week1/posts/05_side_hustles/01.jpg"><link rel="canonical" href="https://autopilotoi.app{path}">
<meta name="theme-color" content="#0a0a0a"><link rel="icon" href="/logo-128.png"><link rel="preload" href="/assets/fonts/APWide-Black.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=4"><style>
.hub h1{{margin:20px 0 22px}}.hub h1 em{{color:var(--l)}}
.cap{{display:flex;gap:10px;flex-wrap:wrap;margin-top:26px;max-width:560px}}.cap input{{flex:1;min-width:220px;height:56px;border-radius:999px;border:1.5px solid rgba(255,255,255,.22);background:#111;color:#fff;padding:0 22px;font:500 16px var(--T)}}
.msg{{margin-top:12px;color:#c9c9c2;font-size:14px;min-height:20px}}.msg b{{color:var(--l)}}
.drops{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;margin-top:34px}}.drop{{display:block;border-radius:18px;overflow:hidden;border:1px solid var(--line);background:var(--g2)}}
.drop img{{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}}.drop div{{padding:14px 16px 16px}}.drop b{{display:block;font:700 15px/1.25 var(--T)}}.drop span{{font:600 11.5px var(--T);letter-spacing:.14em;text-transform:uppercase;color:var(--l)}}
.ags{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px;margin-top:30px}}.ags .card b{{font:700 18px var(--T);display:block}}.ags .card .go{{display:inline-block;margin-top:14px;color:var(--l);font:700 15px var(--T)}}
h2.hh{{font:400 clamp(26px,5vw,44px)/1 var(--W);text-transform:uppercase;letter-spacing:-.02em}}
.post{{padding:54px 0;border-top:1px solid var(--line)}}.post h2{{font:400 clamp(22px,4.4vw,34px)/1.05 var(--W);text-transform:uppercase;letter-spacing:-.02em;margin:10px 0 8px}}
.pr{{position:relative;background:var(--g2);border:1px solid var(--line);border-left:5px solid var(--l);border-radius:14px;padding:18px 18px 18px 20px;margin-top:14px;white-space:pre-wrap;font:500 15px/1.55 var(--T);color:#e9e8e2}}
.pr b{{font-weight:500;color:#000;background:var(--l);padding:0 .15em;border-radius:3px}}.pr .t{{display:block;font:700 12px var(--T);letter-spacing:.14em;text-transform:uppercase;color:var(--l);margin-bottom:8px}}
.cpy{{position:absolute;top:12px;right:12px;font:700 12px var(--T);background:var(--l);color:#000;border:0;border-radius:999px;padding:7px 14px;cursor:pointer}}
.locked .pr{{filter:blur(7px);user-select:none;pointer-events:none}}.gate{{display:none}}.locked .gate{{display:block;position:sticky;top:76px;z-index:5;background:#0d0d0d;border:1.5px solid var(--l);border-radius:22px;padding:24px;margin:26px 0}}
.how{{color:#c9c9c2;font-size:15px;margin-top:6px}}.up{{display:inline-block;margin-top:16px;font:600 14px var(--T);color:var(--mut)}}.up a{{color:var(--l)}}
</style></head><body class="hub"><div class="nav"><div class="wrap"><a class="brand" href="/"><span class="eyes"><i></i><i></i></span>AUTOPILOT.OI</a><div class="links"><a href="/vault/" class="hm {'on' if path=='/vault/' else ''}">Free Vault</a><a href="/#agents" class="hm">Agents</a><a href="/business/" class="hm">For business</a><a href="/vault/" class="cta">Get it free</a></div></div></div>'''
FOOT = '''<div class="foot"><div class="wrap"><div class="big">AUTOPILOT<span>.</span>OI</div><div><span>Free Claude prompts and agents, new every day.</span><span><a href="https://www.instagram.com/autopilot.oi/">Instagram</a> · <a href="/vault/">Free Vault</a> · <a href="/business/">For business</a> · <a href="/library/">All kits</a></span></div></div></div>
<script src="/assets/ap.js"></script><script>
function kit(f,src,done){f.addEventListener('submit',function(ev){ev.preventDefault();var i=f.querySelector('input'),b=f.querySelector('button'),m=f.parentNode.querySelector('.msg'),em=i.value.trim();
 if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(em)){m.textContent='Check that email and try again.';return}
 b.disabled=true;var fd=new FormData();fd.append('email_address',em);fd.append('fields[source]',src);
 fetch('https://app.kit.com/forms/10118407/subscriptions',{method:'POST',body:fd,mode:'no-cors'}).then(function(){try{localStorage.setItem('ap_vault','1')}catch(x){}
  try{if(window.goatcounter)goatcounter.count({path:'optin/'+src,event:true})}catch(x){}done(m)}).catch(function(){b.disabled=false;m.textContent='Something went wrong. Try again in a moment.'})})}
</script>'''
FORM = lambda btn: f'<form class="cap"><input type="email" required placeholder="Your email" autocomplete="email" aria-label="Your email"><button class="btn" type="submit">{btn}</button></form><div class="msg"></div>'
# ---------- home
drops = "".join(f'<a class="drop" href="/vault/#{s}"><img loading="lazy" src="/media/hub/week1/posts/{s}/01.jpg" alt="{e(t)}"><div><span>{k}</span><b>{e(t)}</b></div></a>' for _, s, t, k in ORDER)
ags = "".join(f'<div class="card"><b>{n}</b><p>{e(d)}</p><a class="go buy" href="{G}{s}">Get it · $10 →</a></div>' for s, n, d in AG)
home = HEAD("AUTOPILOT.OI · Free Claude prompts and agents that save you money", "Free copy and paste Claude prompts and 10 minute agents for bills, jobs, money and everyday life. New every day.", "/") + f'''
<div class="wrap hero"><span class="tagline live">Free · new every day</span>
<h1>Free Claude prompts and agents that <em>save you money.</em></h1>
<p class="lead">Lower your bills, find a better job, read the fine print and plan your money. Copy, paste, done. No experience needed.</p>
{FORM("Unlock the free Vault")}<p class="label" style="margin-top:6px">Every prompt from our posts in one place. Free. Unsubscribe any time.</p></div>
<div class="sec"><div class="wrap"><span class="tagline">This week in the Vault</span><h2 class="hh" style="margin-top:16px">12 free drops.</h2><div class="drops">{drops}</div></div></div>
<div class="sec" id="agents"><div class="wrap"><span class="tagline">Want it done for you?</span><h2 class="hh" style="margin-top:16px">Ready made money agents.</h2>
<p class="lead" style="margin-top:14px">The free prompts get you started. These are full setups for one job each: the master prompt, starter prompts, a 10 minute setup guide and a tracker. $10 each, one payment, 30 day refund.</p>
<div class="ags">{ags}<div class="card" style="border-color:var(--l)"><b>All 5 Money Agents</b><p>Every agent above in one bundle.</p><a class="go buy" href="{G}all-money-agents">Get all 5 · $39 →</a></div></div></div></div>
<div class="sec"><div class="wrap"><span class="tagline">Run a business?</span><h2 class="hh" style="margin-top:16px">We have kits for that too.</h2><p style="margin-top:18px"><a class="btn ghost" href="/business/">See the business kits</a></p></div></div>
{FOOT}<script>kit(document.querySelector('.cap'),'vault_home',function(m){{m.innerHTML='<b>You’re in.</b> Opening the Vault...';setTimeout(function(){{location.href='/vault/'}},700)}});</script></body></html>'''
open(f"{R}/docs/index.html", "w").write(home)
# ---------- vault
posts = ""
for k, s, t, kind in ORDER:
    d = D[k]
    if d["type"] == "p":
        how = "Set up: open Claude, tap Projects, New project, and paste one into the Instructions box." if d.get("steps") == "a" else "Open Claude (free at claude.ai), paste a prompt, and swap the [brackets] for your own."
        body = "".join(f'<div class="pr"><span class="t">{i+1}. {e(a)}</span>{br(b)}<button class="cpy">Copy</button></div>' for i, (a, b) in enumerate(d["items"]))
        if d.get("prep"): how += " " + d["prep"]
    else:
        how = f'Set up in 10 minutes: open Claude, tap Projects, New project, name it “{d["name"]}”, paste this into the Instructions box' + (f', add {d["add"]}' if d.get("add") else "") + ', then open a chat and type “go”.'
        body = f'<div class="pr"><span class="t">Agent instructions</span>{br(d["instr"])}<button class="cpy">Copy</button></div>'
    up = f'<span class="up">Want the full setup? <a class="buy" href="{G}{UP[s][0]}">Get the {UP[s][1]} · $10 →</a></span>' if s in UP else ""
    note = f'<p class="how">{e(d["note"])}</p>' if d.get("note") else ""
    posts += f'<div class="post" id="{s}"><span class="tagline">{kind}</span><h2>{e(t)}</h2><p class="how">{e(how)}</p>{body}{note}{up}</div>'
vault = HEAD("The Free Prompt Vault · AUTOPILOT.OI", "Every Claude prompt and agent from our posts, free to copy.", "/vault/") + f'''
<div class="wrap hero" style="padding-bottom:20px"><span class="tagline live">Free · updated every day</span><h1>The Prompt <em>Vault.</em></h1>
<p class="lead">Every prompt and agent from our posts. Tap copy, paste into Claude, done.</p></div>
<div class="wrap locked" id="v"><div class="gate"><b style="font:700 20px var(--T)">Unlock everything, free.</b><p class="how">Enter your email and the whole Vault opens. We send new prompts as they drop.</p>{FORM("Unlock the Vault")}</div>{posts}</div>
{FOOT}<script>
var v=document.getElementById('v');function open_(){{v.classList.remove('locked')}}
try{{if(localStorage.getItem('ap_vault'))open_()}}catch(x){{}}
kit(document.querySelector('.cap'),'vault_page',function(m){{open_()}});
document.querySelectorAll('.cpy').forEach(function(b){{b.addEventListener('click',function(){{var p=b.parentNode.cloneNode(true);p.querySelector('.cpy').remove();var t=p.querySelector('.t');if(t)t.remove();navigator.clipboard.writeText(p.textContent.trim()).then(function(){{b.textContent='Copied';setTimeout(function(){{b.textContent='Copy'}},1400)}})}})}});
</script></body></html>'''
open(f"{R}/docs/vault/index.html", "w").write(vault)
print("built", len(home), len(vault))
