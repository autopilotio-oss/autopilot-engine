"""Builds THE WORKSPACE course PDF. Usage: python3 tools/workspace/build.py out.pdf"""
import html, os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import QUIZ, BUILDER, BRAIN, AGENTS, COMMANDS, NIGHT, FIX, SAFETY, EXAMPLES
e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = f"file://{ROOT}/tools/story/fonts/"
CSS = f"""@font-face{{font-family:SA;src:url({F}../../office/fonts/Anton-Regular.ttf)}}@font-face{{font-family:GE;font-weight:500;src:url({F}Geist-Medium.otf)}}@font-face{{font-family:GE;font-weight:600;src:url({F}Geist-SemiBold.otf)}}@font-face{{font-family:GE;font-weight:700;src:url({F}Geist-Bold.otf)}}@font-face{{font-family:M;src:url({F}../../office/fonts/ChakraPetch-SemiBold.ttf)}}
@page{{size:Letter;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:500 13px/1.5 GE;color:#ececE6;background:#050605;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;height:11in;overflow:hidden;padding:.6in .7in .7in;position:relative;page-break-after:always;background:radial-gradient(700px 520px at 12% 6%,rgba(212,255,58,.11),transparent 60%),radial-gradient(600px 500px at 95% 100%,rgba(30,110,80,.13),transparent 60%),#050605}}
.top{{display:flex;align-items:center;gap:10px;font:11px M;letter-spacing:2px;color:#8f928b}}.top b{{font:19px SA;color:#fff;letter-spacing:.5px}}.top span{{margin-left:auto}}
.chip{{display:inline-block;background:#D4FF3A;color:#0a0a0a;font:13px SA;padding:5px 12px 3px;border-radius:7px;text-transform:uppercase}}
h1{{font:78px/.9 SA;text-transform:uppercase;margin:22px 0 16px;color:#fff}}h1 em,h2 em{{color:#D4FF3A;font-style:normal}}
h2{{font:34px/1 SA;text-transform:uppercase;margin:22px 0 10px;color:#fff}}h3{{font:18px SA;text-transform:uppercase;color:#fff;margin:2px 0 4px}}
.lead{{font-size:16px;color:#c8cbc4;max-width:6.4in}}.mut{{color:#9a9d96}}
.card{{background:linear-gradient(165deg,#1b1e19,#0c0d0b);border:1px solid rgba(212,255,58,.32);border-radius:14px;padding:13px 16px;margin:9px 0}}
.mono{{font:10.5px M;letter-spacing:2px;color:#D4FF3A;margin-bottom:5px;text-transform:uppercase}}
pre{{white-space:pre-wrap;font:10.4px/1.5 M;color:#e9ffd0}}
ol{{margin-left:18px}}li{{margin:5px 0}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:9px}}.g2 .card{{margin:0}}
.row{{display:flex;gap:12px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.09)}}.row .n{{font:11px M;color:#D4FF3A;min-width:24px;padding-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:12px;margin-top:6px}}th{{font:10px M;letter-spacing:1.5px;color:#D4FF3A;text-align:left;border-bottom:1px solid rgba(212,255,58,.4);padding:7px 6px}}td{{border-bottom:1px solid rgba(255,255,255,.1);padding:8px 6px;vertical-align:top}}
a{{color:#D4FF3A}}.foot{{position:absolute;left:.7in;right:.7in;bottom:.35in;font:9px M;letter-spacing:1px;color:#62655e;display:flex}}.foot span{{margin-left:auto}}
.big{{font:120px/1 SA;color:#D4FF3A}}
"""
N = [0]
def page(body, label):
    N[0] += 1
    return (f'<div class="pg"><div class="top"><b>AUTOPILOT.OI</b> · THE WORKSPACE<span>{e(label)} · {N[0]:02d}</span></div>{body}'
            '<div class="foot">AUTOPILOT.OI is independent and not affiliated with Anthropic. Claude is a product of Anthropic. Features and plans change: check claude.com.<span>@autopilot.oi</span></div></div>')

STARTER = ('Read the file "THE WORKSPACE" in this project. You are my setup tech. Follow the BUILDER PROMPT page exactly, '
           'using the 20 QUESTIONS page, the BUSINESS BRAIN TEMPLATE page and the 7 agent pages. Start now.')

def build():
    P = []
    P.append(page(f'''<div style="margin-top:1.3in"><span class="chip">7 agents · any business</span>
<h1>The<br><em>Workspace</em></h1><p class="lead">Set up 7 Claude agents that draft your email replies, keep your calendar, chase quiet quotes, ask for reviews and brief you every morning. You answer 20 questions. Claude does the setup with you.</p>
<h2>What's inside</h2><div class="g2">{"".join(f'<div class="card"><div class="mono">{a}</div>{e(b)}</div>' for a, b in [
        ("Start here", "What you need and the one hour plan"), ("The 20 questions", "Everything Claude needs to know about your business"),
        ("The Builder prompt", "Turns Claude into your setup tech"), ("Business Brain", "One file with your prices, rules and voice"),
        ("7 agents", "Ready prompts and schedules"), ("50 phone commands", "Run your business from a text"),
        ("The Night Shift", "How agents run on their own"), ("Fix It + safety rules", "Stay in control")])}</div></div>''', "START"))
    P.append(page(f'''<h2>Before you <em>start</em></h2>
<div class="card"><div class="mono">You need</div><ol>
<li><b>Claude.</b> The app on your phone (App Store or Google Play) and on a computer (<a href="https://claude.com/download">claude.com/download</a>) or claude.ai in a browser. Setup is easiest on a computer.</li>
<li><b>A paid Claude plan (Pro or up) for scheduled agents.</b> Paid to Anthropic, not us. See <a href="https://claude.com/pricing">claude.com/pricing</a>. On the free plan you can still run every agent by hand.</li>
<li><b>Gmail and Google Calendar</b> work best. Other apps can work if Claude has a connector for them.</li>
<li><b>About an hour.</b> Most of it is Claude working.</li></ol></div>
<h2>The one hour <em>plan</em></h2>
<div class="row"><div class="n">01</div><div><b>Make a Project.</b> In Claude, open Projects, then New project. Name it "My Workspace". Add this PDF to the project's files.</div></div>
<div class="row"><div class="n">02</div><div><b>Paste one prompt.</b> Open a new chat inside the project and paste the starter prompt below.</div></div>
<div class="row"><div class="n">03</div><div><b>Answer and tap allow.</b> Claude asks the 20 questions, writes your Business Brain, connects your apps with you and builds your 7 agents.</div></div>
<div class="card" style="margin-top:16px"><div class="mono">Starter prompt · paste this</div><pre style="font-size:12.5px">{e(STARTER)}</pre></div>
<p class="mut" style="margin-top:10px">Stuck anytime? Type "I'm stuck" and describe your screen.</p>''', "START HERE"))
    P.append(page('<h2>The <em>20 questions</em></h2><p class="mut">Claude asks these one at a time. Jot answers here first if you like. Real prices and real rules make better drafts.</p>'
                  + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><b>{e(a)}.</b> <span class="mut">{e(b)}</span></div></div>' for i, (a, b) in enumerate(QUIZ)), "QUIZ"))
    core = BUILDER.format(quiz="(Use THE 20 QUESTIONS page.)", agents="(Use the 7 agent pages: name, schedule, task prompt.)", brain="(Use the BUSINESS BRAIN TEMPLATE page.)")
    P.append(page(f'<h2>The <em>Builder</em> prompt</h2><p class="mut">Claude reads this from the PDF. You don\'t need to paste it.</p><div class="card"><div class="mono">Builder prompt</div><pre style="font-size:9.6px;line-height:1.42">{e(core)}</pre></div>', "BUILDER"))
    P.append(page(f'<h2>Business Brain <em>template</em></h2><p class="mut">Claude fills this from your answers and saves it as a Google Doc. Every agent reads it first.</p><div class="card"><div class="mono">Business Brain</div><pre style="font-size:11px">{e(BRAIN)}</pre></div>', "BRAIN"))
    P.append(page('<h2>Your <em>team</em></h2><p class="mut">Example schedule. Claude sets yours around your hours.</p><table><tr><th>#</th><th>Agent</th><th>Job</th><th>When</th></tr>'
                  + "".join(f'<tr><td class="mono">{a["n"]}</td><td><b>{e(a["name"])}</b></td><td>{e(a["job"])}</td><td class="mut">{e(a["when"])}</td></tr>' for a in AGENTS)
                  + '</table><div class="card" style="margin-top:18px"><div class="mono">The deal</div>Every agent drafts. You approve. Nothing goes to a customer without your OK. That keeps every reply accurate and sounding like you.</div>', "TEAM"))
    for a in AGENTS:
        P.append(page(f'''<div style="display:flex;align-items:flex-end;gap:18px"><div class="big">{a["n"]}</div><div style="padding-bottom:14px"><span class="chip">{e(a["kind"])}</span><h2 style="margin:8px 0 0">{e(a["name"])}</h2></div></div>
<p class="lead">{e(a["job"])}</p><div class="card"><div class="mono">Schedule</div>{e(a["when"])}</div>
<div class="card"><div class="mono">Task prompt · {e(a["name"])}</div><pre>{e(a["prompt"])}</pre></div>
<div class="card" style="border-color:rgba(255,255,255,.14)"><div class="mono" style="color:#9a9d96">Sample draft · made up business</div><pre style="color:#ececE6;font-size:11px">{e(EXAMPLES[a["n"]][0])}</pre></div>
<div class="row" style="border:0"><div class="n">TIP</div><div>{e(EXAMPLES[a["n"]][1])}</div></div>''', "AGENT " + a["n"]))
    half = [COMMANDS[:4], COMMANDS[4:]]
    for j, grp in enumerate(half):
        body = ('<h2>50 phone <em>commands</em></h2><p class="mut">Type these in your Workspace project from your phone. Fill the [brackets].</p>' if j == 0 else '<h2>Phone commands <em>cont.</em></h2>')
        body += '<div class="g2" style="margin-top:10px">' + "".join(f'<div class="card"><div class="mono">{e(t)}</div>' + "".join(f'<div style="padding:3px 0;font-size:12px">→ {e(c)}</div>' for c in cs) + '</div>' for t, cs in grp) + '</div>'
        P.append(page(body, "COMMANDS"))
    P.append(page('<h2>The night <em>shift</em></h2><p class="mut">How your agents run on their own.</p>' + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><b>{e(a)}</b> <span class="mut">{e(b)}</span></div></div>' for i, (a, b) in enumerate(NIGHT)), "NIGHT SHIFT"))
    P.append(page('<h2>Fix <em>it</em></h2><p class="mut">When something looks off.</p>' + "".join(f'<div class="card"><div class="mono">{e(a)}</div>{e(b)}</div>' for a, b in FIX), "FIX IT"))
    P.append(page('<h2>Safety <em>rules</em></h2>' + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div>{e(s)}</div></div>' for i, s in enumerate(SAFETY))
                  + '<h2>Updates and <em>refunds</em></h2><div class="card">When Claude\'s screens or plans change, we update this course and you get the new version in your Gumroad library at no cost.</div>'
                  + '<div class="card">Follow the setup. If your agents aren\'t working for you within 30 days, reply to your Gumroad receipt for a full refund.</div>', "RULES"))
    return "".join(P)

async def main(out):
    from playwright.async_api import async_playwright
    os.makedirs("/tmp/ws", exist_ok=True)
    open("/tmp/ws/ws.html", "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{build()}</body></html>")
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto("file:///tmp/ws/ws.html"); await pg.wait_for_timeout(800)
        # overflow check: every page's content must fit
        bad = await pg.evaluate("[...document.querySelectorAll('.pg')].map((p,i)=>[i+1,p.scrollHeight-p.clientHeight]).filter(x=>x[1]>2)")
        if bad: print("OVERFLOW", bad)
        await pg.pdf(path=out, print_background=True, prefer_css_page_size=True); await b.close()
asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/ws/THE WORKSPACE.pdf"))
