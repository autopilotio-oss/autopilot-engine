"""Builds a premium agent pack PDF (same look as THE WORKSPACE).
Usage: python3 tools/packs/build.py <slug> <out.pdf>
Content lives in tools/packs/content_<slug>.py (kept out of the public repo, see .gitignore)."""
import html, os, sys, asyncio, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import re
F = f"file://{ROOT}/tools/story/fonts/"
CSS = eval(re.search(r'CSS = (f""".*?""")', open(f"{ROOT}/tools/workspace/build.py").read(), re.S).group(1), {"F": F})  # shared style with THE WORKSPACE
slug = sys.argv[1]; C = importlib.import_module(f"content_{slug}").PACK
N = [0]
def page(body, label):
    N[0] += 1
    return (f'<div class="pg"><div class="top"><b>AUTOPILOT.OI</b> · {e(C["name"].upper())}<span>{e(label)} · {N[0]:02d}</span></div>{body}'
            f'<div class="foot">{e(C.get("foot", "Education only. AUTOPILOT.OI is independent and not affiliated with Anthropic. Claude is a product of Anthropic."))}<span>@autopilot.oi</span></div></div>')
def pre(t, size=None): return f'<pre style="{f"font-size:{size}px;line-height:1.42" if size else ""}">{e(t)}</pre>'
def build():
    P = []
    P.append(page(f'''<div style="margin-top:1.15in"><span class="chip">{e(C["tag"])}</span>
<h1>{C["title_html"]}</h1><p class="lead">{e(C["lead"])}</p>
<h2>What's <em>inside</em></h2><div class="g2">{"".join(f'<div class="card"><div class="mono">{e(a)}</div>{e(b)}</div>' for a, b in C["inside"])}</div></div>''', "START"))
    P.append(page(f'''<h2>Before you <em>start</em></h2><div class="card"><div class="mono">You need</div><ol>{"".join(f"<li>{x}</li>" for x in C["need"])}</ol></div>
<h2>The <em>{e(C["plan_title"])}</em></h2>{"".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><b>{e(a)}</b> {e(b)}</div></div>' for i, (a, b) in enumerate(C["plan"]))}
<div class="card" style="margin-top:16px"><div class="mono">Starter prompt · paste this</div>{pre(C["starter"], 12.5)}</div>
<p class="mut" style="margin-top:10px">Stuck anytime? Type "I'm stuck" and describe your screen.</p>''', "START HERE"))
    P.append(page(f'<h2>The <em>{len(C["quiz"])} questions</em></h2><p class="mut">Your agent asks these one at a time. Real numbers make better answers.</p>'
                  + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div><b>{e(a)}.</b> <span class="mut">{e(b)}</span></div></div>' for i, (a, b) in enumerate(C["quiz"])), "QUIZ"))
    P.append(page(f'<h2>The <em>Builder</em> prompt</h2><p class="mut">Claude reads this from the PDF. It installs your agent with you.</p><div class="card"><div class="mono">Builder prompt</div>{pre(C["builder"], C.get("builder_size", 10))}</div>', "BUILDER"))
    for i, part in enumerate(C["master"]):
        P.append(page(f'<h2>{"The <em>agent</em> instructions" if i == 0 else "Instructions <em>cont.</em>"}</h2><p class="mut">{"The Builder pastes this into your Project instructions. Keep it there." if i == 0 else ""}</p><div class="card"><div class="mono">Agent instructions · {e(C["name"])}</div>{pre(part, C.get("master_size", 9.8))}</div>', "AGENT"))
    X = C["example"]
    P.append(page(f'''<h2>Worked <em>example</em></h2><p class="lead">{e(X["intro"])}</p>
<div class="card"><div class="mono">You type</div>{pre(X["ask"], 12)}</div>
<div class="card"><div class="mono">{e(X["title"])} · sample</div><table><tr>{"".join(f"<th>{e(c)}</th>" for c in X["cols"])}</tr>{"".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in r) + "</tr>" for r in X["rows"])}</table></div>
{"".join(f'<div class="row"><div class="n">→</div><div>{e(n)}</div></div>' for n in X["notes"])}''', "EXAMPLE"))
    W = C["workflows"]
    for j in range(0, len(W), 3):
        P.append(page(('<h2>Your <em>playbook</em></h2><p class="mut">Type the command, or paste the prompt. Fill the [brackets].</p>' if j == 0 else '<h2>Playbook <em>cont.</em></h2>')
                      + "".join(f'<div class="card"><div class="mono">{e(n)} · command: {e(cmd)}</div>{pre(p, 10.2)}</div>' for n, cmd, p in W[j:j + 3]), "PLAYBOOK"))
    for t, kind, body in C["templates"]:
        if kind == "table":
            inner = f'<table><tr>{"".join(f"<th>{e(c)}</th>" for c in body["cols"])}</tr>{"".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" for v in r) + "</tr>" for r in body["rows"])}</table>' + (f'<p class="mut" style="margin-top:10px">{e(body["note"])}</p>' if body.get("note") else "")
        elif kind == "cards":
            inner = "".join(f'<div class="card"><div class="mono">{e(a)}</div>{pre(b, 10.6)}</div>' for a, b in body)
        else:
            inner = f'<div class="card">{pre(body, 10.8)}</div>'
        P.append(page(f'<h2>{t}</h2>{inner}', "TEMPLATE"))
    T = C["tracker"]
    P.append(page(f'<h2>{T["title"]}</h2><p class="mut">{e(T["note"])}</p><table><tr>{"".join(f"<th>{e(c)}</th>" for c in T["cols"])}</tr>'
                  + "".join("<tr>" + "".join(f"<td>{e(str(v))}</td>" if j < len(r) else "<td style='height:26px'></td>" for j, v in enumerate(list(r) + [""] * (len(T["cols"]) - len(r)))) + "</tr>" for r in T["rows"]) + '</table>', "TRACKER"))
    P.append(page('<h2>Fix <em>it</em></h2>' + "".join(f'<div class="card"><div class="mono">{e(a)}</div>{e(b)}</div>' for a, b in C["fix"])
                  + '<h2>Rules and <em>links</em></h2>' + "".join(f'<div class="row"><div class="n">{i+1:02d}</div><div>{e(s)}</div></div>' for i, s in enumerate(C["rules"]))
                  + '<p style="margin-top:10px">' + " · ".join(f'<a href="{u}">{e(t)}</a>' for t, u in C["links"]) + '</p>'
                  + '<div class="card" style="margin-top:12px">Updates: when the apps change, we update this pack and you get the new version in your Gumroad library at no cost. Not working for you within 30 days? Reply to your Gumroad receipt for a full refund.</div>', "RULES"))
    return "".join(P)
async def main(out):
    from playwright.async_api import async_playwright
    os.makedirs("/tmp/packs", exist_ok=True); h = f"/tmp/packs/{slug}.html"
    open(h, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{build()}</body></html>")
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        await pg.goto(f"file://{h}"); await pg.wait_for_timeout(800)
        bad = await pg.evaluate("[...document.querySelectorAll('.pg')].map((p,i)=>[i+1,p.scrollHeight-p.clientHeight]).filter(x=>x[1]>2)")
        print("pages", N[0], "OVERFLOW" if bad else "fit", bad or "")
        await pg.pdf(path=out, print_background=True, prefer_css_page_size=True); await b.close()
asyncio.run(main(sys.argv[2]))
