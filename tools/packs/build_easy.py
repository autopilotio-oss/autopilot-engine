"""Beginner layout for a pack PDF: plain pages first, Claude's pages last.
Usage: python3 tools/packs/build_easy.py <slug> <out.pdf>
Reads tools/packs/content_<slug>.py (PACK) plus the beginner fields: quick, quick_result, words, extras, setup_name."""
import html, os, sys, asyncio, importlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = f"file://{ROOT}/tools/story/fonts/"
BASE = eval(re.search(r'CSS = (f""".*?""")', open(f"{ROOT}/tools/workspace/build.py").read(), re.S).group(1), {"F": F})
CSS = BASE + """
body{font-size:14px}
.lead{font-size:17px;line-height:1.5}
.step{display:flex;gap:14px;align-items:center;margin:7px 0;padding:8px 12px;background:linear-gradient(165deg,#161914,#0b0c0a);border:1px solid rgba(255,255,255,.1);border-radius:16px}
.num{flex:none;width:44px;height:44px;border-radius:50%;background:#D4FF3A;color:#0a0a0a;font:24px/46px SA;text-align:center}
.st h3{font-size:20px}.st p{color:#c8cbc4;font-size:13.5px;line-height:1.45}
.phone{flex:none;width:1.45in;height:1.62in;border-radius:20px;border:2px solid #2c3029;background:#101210;padding:9px 8px;position:relative;overflow:hidden}
.phone .bar{font:7px M;letter-spacing:1px;color:#8f928b;display:flex;justify-content:space-between;margin-bottom:7px}
.phone .ttl{font:12px SA;color:#fff;letter-spacing:.3px;margin-bottom:6px;text-transform:uppercase}
.phone .it{font-size:8.5px;color:#d9dcd4;background:#1c1f1a;border-radius:7px;padding:5px 6px;margin:4px 0}
.phone .hi{background:#D4FF3A;color:#0a0a0a;font-weight:700}
.phone .me{margin-left:auto;width:85%;background:#2a2e27;border-radius:9px 9px 2px 9px;padding:5px 6px;font-size:7.5px;color:#fff;margin:5px 0}
.phone .ai{width:88%;background:rgba(212,255,58,.12);border:1px solid rgba(212,255,58,.5);border-radius:9px 9px 9px 2px;padding:5px 6px;font-size:7.5px;color:#e9ffd0;margin:5px 0}
.phone .tap{position:absolute;width:20px;height:20px;border-radius:50%;border:2px solid #D4FF3A;box-shadow:0 0 12px #D4FF3A}
.copy{background:#0d0f0c;border:2px dashed rgba(212,255,58,.6);border-radius:14px;padding:14px 16px;margin:10px 0}
.copy .mono{margin-bottom:8px}.copy pre{font-size:12.5px;line-height:1.55;color:#f2ffe0}
.word{display:flex;gap:16px;align-items:flex-start;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.09)}
.pill{flex:none;min-width:1.3in;text-align:center;background:#D4FF3A;color:#0a0a0a;font:15px M;padding:9px 10px;border-radius:10px}
.word b{display:block;font-size:15px;color:#fff;margin-bottom:3px}.word span{color:#a9ada5;font-size:12.5px}
.note{font:10px M;letter-spacing:1px;color:#7d8179;margin-top:8px}
.divider{margin-top:2.2in}.divider h1{font-size:64px}
.tick{color:#D4FF3A;font-weight:700;margin-right:6px}
"""
slug = sys.argv[1]; C = importlib.import_module(f"content_{slug}").PACK
N = [0]
def page(body, label):
    N[0] += 1
    return (f'<div class="pg"><div class="top"><b>AUTOPILOT.OI</b> · {e(C["name"].upper())}<span>{e(label)} · {N[0]:02d}</span></div>{body}'
            f'<div class="foot">{e(C["foot"])}<span>@autopilot.oi</span></div></div>')
def pre(t, size=None): return f'<pre style="{f"font-size:{size}px;line-height:1.45" if size else ""}">{e(t)}</pre>'
def phone(title, items):
    return f'<div class="phone"><div class="bar"><span>9:41</span><span>● ● ●</span></div><div class="ttl">{e(title)}</div>{"".join(items)}</div>'
def it(t, hi=False): return f'<div class="it{" hi" if hi else ""}">{e(t)}</div>'
def me(t): return f'<div class="me">{e(t)}</div>'
def ai(t): return f'<div class="ai">{e(t)}</div>'
def build():
    P = []; name = C["name"]; proj = C["setup_name"]
    # 1 cover
    does = "".join(f'<div class="card"><div class="mono">{e(a)}</div>{e(b)}</div>' for a, b in C["does"])
    P.append(page(f'''<div style="margin-top:.9in"><span class="chip">No tech skills needed</span>
<h1>{C["title_html"]}</h1><p class="lead">{e(C["lead"])}</p>
<h2>What it does <em>for you</em></h2><div class="g2">{does}</div>
<div class="card" style="margin-top:14px"><div class="mono">How this guide works</div>Page 2: try it right now in 60 seconds. Page 3: set it up once so it remembers your business. Page 4: the words you type. The pages at the back are for Claude to read, not you.</div></div>''', "START"))
    # 2 quick win
    QR = C["quick_result"]
    P.append(page(f'''<h2>Try it <em>right now</em></h2><p class="lead">No setup yet. Open the Claude app (free at claude.ai), tap New chat, and paste this. {e(C.get("quick_note", ""))}</p>
<div class="copy"><div class="mono">Copy this · paste into Claude</div>{pre(C["quick"], 12.5)}</div>
<div style="display:flex;gap:18px;align-items:flex-start;margin-top:8px">{phone("New chat", [me(QR["you"]), ai(QR["claude"])])}
<div><h3>What you'll see</h3><p class="mut" style="margin-top:6px">{e(QR["explain"])}</p>
<div class="card" style="margin-top:12px"><div class="mono">Liked it?</div>Turn to page 3. Fifteen minutes of setup and it knows your business every time, so you only type one word.</div></div></div>''', "60 SECONDS"))
    # 3 setup with phone screens
    steps = [
        ("Make a Project", f'In the Claude app tap the menu, then Projects, then New project. Name it "{proj}". A Project is a folder that remembers your business.',
         phone("Projects", [it("+ New project", True), it("My first chat"), '<div class="tap" style="left:58px;top:46px"></div>'])),
        ("Add this guide", "Inside the Project tap Add files (the + or paperclip) and pick this PDF from your downloads.",
         phone(proj, [it("Files"), it(f"{name}.pdf", True), it("Instructions"), '<div class="tap" style="left:60px;top:66px"></div>'])),
        ("Paste one message", "Start a chat inside the Project and paste the starter message below. Claude asks you 7 easy questions, one at a time.",
         phone(proj, [me("Read the PDF in this project. You are my setup helper..."), ai("Hi! Question 1 of 7: what's your business called?")])),
        ("Save your box", "At the end Claude gives you one box of text. Tap Copy, open the Project's Instructions, paste it, tap Save. Then start a new chat. Done.",
         phone("Instructions", [it("Paste here", True), it("MY RULES ..."), it("Save"), '<div class="tap" style="left:56px;top:96px"></div>'])),
    ]
    P.append(page('<h2>Set it up <em>once</em></h2><p class="mut">About 15 minutes. Works on your phone. Screens are simplified, your app may look a little different.</p>'
                  + "".join(f'<div class="step"><div class="num">{i+1}</div><div class="st" style="flex:1"><h3>{e(a)}</h3><p>{e(b)}</p></div>{ph}</div>' for i, (a, b, ph) in enumerate(steps))
                  + f'<div class="copy" style="margin-top:6px;padding:10px 14px"><div class="mono">Starter message · step 3</div>{pre(C["starter"], 11)}</div>', "SETUP"))
    # 4 words
    W = C["words"]
    P.append(page('<h2>The words <em>you type</em></h2><p class="lead">After setup, open a new chat in your Project and type one of these. That\'s the whole job.</p>'
                  + "".join(f'<div class="word"><div class="pill">{e(w)}</div><div><b>{e(g)}</b><span>{e(x)}</span></div></div>' for w, g, x in W)
                  + '<div class="card" style="margin-top:14px"><div class="mono">Stuck?</div>Type: I\'m stuck, and describe what you see on your screen. Claude walks you through it.</div>', "YOUR WORDS"))
    # 5 example
    X = C["example"]
    P.append(page(f'''<h2>See it <em>work</em></h2><p class="lead">{e(X["intro"])}</p>
<div class="card"><div class="mono">You type</div>{pre(X["ask"], 12.5)}</div>
<div class="card"><div class="mono">{e(X["title"])} · sample</div><table><tr>{"".join(f"<th>{e(c)}</th>" for c in X["cols"])}</tr>{"".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in r) + "</tr>" for r in X["rows"])}</table></div>
{"".join(f'<div class="row"><div class="n">→</div><div>{e(n)}</div></div>' for n in X["notes"])}''', "EXAMPLE"))
    # 6 extras: useful even without AI
    for t, kind, body in C["extras"]:
        if kind == "table":
            inner = f'<table><tr>{"".join(f"<th>{e(c)}</th>" for c in body["cols"])}</tr>{"".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in r) + "</tr>" for r in body["rows"])}</table>' + (f'<p class="mut" style="margin-top:10px">{e(body["note"])}</p>' if body.get("note") else "")
        elif kind == "cards":
            inner = "".join(f'<div class="card"><div class="mono">{e(a)}</div>{pre(b, 11.2)}</div>' for a, b in body)
        elif kind == "list":
            rows = "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div>{e(x)}</div></div>' for i, x in enumerate(body))
            inner = f'<div style="column-count:2;column-gap:22px;font-size:12.5px">{rows}</div>' if len(body) > 12 else rows
        else:
            inner = f'<div class="card">{pre(body, 11.2)}</div>'
        P.append(page(f'<h2>{t}</h2><p class="mut">Bonus: use these even without AI.</p>{inner}', "BONUS"))
    for t, kind, body in [x for x in C["templates"] if "cheat sheet" not in x[0]]:
        if kind == "table":
            inner = f'<table><tr>{"".join(f"<th>{e(c)}</th>" for c in body["cols"])}</tr>{"".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in r) + "</tr>" for r in body["rows"])}</table>' + (f'<p class="mut" style="margin-top:10px">{e(body["note"])}</p>' if body.get("note") else "")
        else:
            inner = "".join(f'<div class="card"><div class="mono">{e(a)}</div>{pre(b, 11.2)}</div>' for a, b in body)
        P.append(page(f'<h2>{t}</h2>{inner}', "CHEAT SHEET"))
    P.append(page('<h2>If something <em>goes wrong</em></h2>' + "".join(f'<div class="card"><div class="mono">{e(a)}</div>{e(b)}</div>' for a, b in C["fix"])
                  + '<h2>The <em>rules</em></h2>' + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div>{e(s)}</div></div>' for i, s in enumerate(C["rules"]))
                  + '<p style="margin-top:10px">' + " · ".join(f'<a href="{u}">{e(t)}</a>' for t, u in C["links"]) + '</p>'
                  + '<div class="card" style="margin-top:12px">Need help? Reply to your Gumroad receipt and a person answers. Updates are free in your Gumroad library. Not working for you within 30 days? Reply to your receipt for a full refund.</div>', "HELP"))
    # appendix: for Claude
    P.append(page(f'''<div class="divider"><span class="chip">For Claude, not for you</span><h1>The pages<br><em>Claude reads.</em></h1>
<p class="lead">You don't need to read anything after this page. Claude reads these when you paste the starter message. They tell it how to set up {e(name)} with you and how to do each job.</p>
<div class="card" style="margin-top:20px"><span class="tick">✓</span>The 7 questions it will ask you<br><span class="tick">✓</span>The setup steps it follows<br><span class="tick">✓</span>The instructions it saves into your Project</div></div>''', "APPENDIX"))
    P.append(page(f'<h2>The <em>{len(C["quiz"])} questions</em></h2><p class="mut">Claude asks these one at a time. Real answers make better results.</p>'
                  + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><b>{e(a)}.</b> <span class="mut">{e(b)}</span></div></div>' for i, (a, b) in enumerate(C["quiz"])), "QUESTIONS"))
    P.append(page(f'<h2>The <em>Builder</em> prompt</h2><p class="mut">For Claude: setup steps.</p><div class="card"><div class="mono">Builder prompt</div>{pre(C["builder"], C.get("builder_size", 10))}</div>', "BUILDER"))
    for i, part in enumerate(C["master"]):
        P.append(page(f'<h2>{"The <em>agent</em> instructions" if i == 0 else "Instructions <em>cont.</em>"}</h2><p class="mut">For Claude: this goes into your Project Instructions during setup.</p><div class="card"><div class="mono">Agent instructions · {e(name)}</div>{pre(part, C.get("master_size", 10))}</div>', "AGENT"))
    return "".join(P)
async def main(out):
    from playwright.async_api import async_playwright
    os.makedirs("/tmp/packs", exist_ok=True); h = f"/tmp/packs/{slug}_easy.html"
    open(h, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{build()}</body></html>")
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto(f"file://{h}"); await pg.wait_for_timeout(800)
        bad = await pg.evaluate("[...document.querySelectorAll('.pg')].map((p,i)=>[i+1,p.scrollHeight-p.clientHeight]).filter(x=>x[1]>2)")
        print("pages", N[0], "OVERFLOW" if bad else "fit", bad or "")
        await pg.pdf(path=out, print_background=True, prefer_css_page_size=True); await b.close()
asyncio.run(main(sys.argv[2]))
