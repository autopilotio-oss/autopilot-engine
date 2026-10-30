import html, os, sys, asyncio
from kits import K
e = html.escape
F = "file:///home/claude/autopilot-engine/tools/story/fonts/"
CSS = f"""@font-face{{font-family:SA;src:url({F}SairaSemiCondensed-BlackItalic.otf)}}@font-face{{font-family:GE;font-weight:600;src:url({F}Geist-SemiBold.otf)}}@font-face{{font-family:GE;font-weight:700;src:url({F}Geist-Bold.otf)}}@font-face{{font-family:GE;font-weight:500;src:url({F}Geist-Medium.otf)}}@font-face{{font-family:M;src:url({F}GeistMono-Medium.otf)}}
@page{{size:Letter;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font:500 13.5px/1.55 GE;color:#ececE6;background:#050605;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.pg{{width:8.5in;min-height:11in;padding:.65in .7in;position:relative;page-break-after:always;background:radial-gradient(700px 520px at 15% 8%,rgba(212,255,58,.12),transparent 60%),radial-gradient(600px 500px at 95% 100%,rgba(30,110,80,.14),transparent 60%),#050605}}
.top{{display:flex;align-items:center;gap:10px;font:12px M;letter-spacing:2px;color:#9a9d96}}.top b{{font:20px SA;color:#fff;letter-spacing:.5px}}.top span{{margin-left:auto}}
.chip{{display:inline-block;background:#D4FF3A;color:#0a0a0a;font:14px SA;padding:5px 12px 3px;border-radius:7px;text-transform:uppercase}}
h1{{font:62px/.92 SA;text-transform:uppercase;margin:22px 0 14px;color:#fff}}h1 em{{color:#D4FF3A;font-style:normal}}
h2{{font:28px/1 SA;text-transform:uppercase;margin:26px 0 12px;color:#fff}}
.lead{{font-size:17px;color:#c8cbc4;max-width:6in}}
.card{{background:linear-gradient(165deg,#1c1f1a,#0d0e0c);border:1px solid rgba(212,255,58,.35);border-radius:16px;padding:16px 18px;margin:10px 0}}
.mono{{font:11px M;letter-spacing:2px;color:#D4FF3A;margin-bottom:6px}}
pre{{white-space:pre-wrap;font:12px/1.55 M;color:#e9ffd0}}
ol{{margin-left:18px}}li{{margin:6px 0}}
table{{width:100%;border-collapse:collapse;font-size:11.5px;margin-top:8px}}th{{font:10px M;letter-spacing:1.5px;color:#D4FF3A;text-align:left;border-bottom:1px solid rgba(212,255,58,.4);padding:7px 6px}}td{{border-bottom:1px solid rgba(255,255,255,.1);height:30px}}
a{{color:#D4FF3A}}.foot{{position:absolute;left:.7in;right:.7in;bottom:.4in;font:9.5px M;letter-spacing:1px;color:#6c6f68;display:flex}}.foot span{{margin-left:auto}}
"""
def kit_html(k, g, n0=1):
    top = lambda p: f'<div class="top"><b>AUTOPILOT.OI</b> · AGENT SETUP<span>{e(g["name"].upper())} · {p}</span></div>'
    foot = '<div class="foot">Education only. Not legal, medical or financial advice. AUTOPILOT.OI is independent and not affiliated with Anthropic. Claude is a product of Anthropic.<span>@autopilot.oi</span></div>'
    p1 = f'''<div class="pg">{top("01")}<div style="margin-top:.9in"><span class="chip">{e(g["tag"])} · AGENT SETUP</span>
<h1>Your <em>{e(g["name"])}</em></h1><p class="lead">{e(g["promise"])}</p>
<h2>What's inside</h2><ol><li>Setup in 10 minutes, step by step</li><li>The master prompt that turns Claude into your {e(g["name"])}</li><li>5 starter prompts for every situation</li><li>Your tracker</li><li>Official links you'll need</li></ol>
<h2>Set it up</h2><ol>{"".join(f"<li>{e(s)}</li>" for s in g["setup"])}</ol></div>{foot}</div>'''
    p2 = f'''<div class="pg">{top("02")}<h2>The master prompt</h2><p style="color:#9a9d96;margin-bottom:6px">Paste this into your Claude Project's instructions. Exactly as written.</p>
<div class="card"><div class="mono">MASTER PROMPT · {e(g["name"].upper())}</div><pre>{e(g["master"])}</pre></div>{foot}</div>'''
    p3 = f'''<div class="pg">{top("03")}<h2>Starter prompts</h2>{"".join(f'<div class="card"><div class="mono">{e(a)}</div><pre>{e(b)}</pre></div>' for a, b in g["starters"])}
<h2>Links you'll need</h2><p>{" · ".join(f'<a href="{u}">{e(t)}</a>' for t, u in g["links"])}</p>{foot}</div>'''
    p4 = f'''<div class="pg">{top("04")}<h2>Your tracker</h2><p style="color:#9a9d96">Print it, or ask your agent to keep it for you.</p>
<table><tr>{"".join(f"<th>{e(c)}</th>" for c in g["tracker"])}</tr>{"".join("<tr>" + "".join("<td></td>" for _ in g["tracker"]) + "</tr>" for _ in range(16))}</table>{foot}</div>'''
    return p1 + p2 + p3 + p4
def doc(body): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for k, g in K.items():
            open(f"out/{k}.html", "w").write(doc(kit_html(k, g)))
            await pg.goto(f"file://{os.getcwd()}/out/{k}.html"); await pg.wait_for_timeout(500)
            await pg.pdf(path=f"out/AUTOPILOT.OI {g['name']} Setup.pdf", print_background=True, prefer_css_page_size=True)
        cover = '<div class="pg"><div class="top"><b>AUTOPILOT.OI</b> · BUNDLE</div><div style="margin-top:2.2in"><span class="chip">3 AGENTS · ONE BUNDLE</span><h1>The <em>Money Agents</em> bundle</h1><p class="lead">Credit Agent, Bill Agent and Debt Agent. Three Claude agents that check your credit, your bills and your debt, so you stop leaving money on the table.</p></div></div>'
        open("out/bundle.html", "w").write(doc(cover + "".join(kit_html(k, g) for k, g in K.items())))
        await pg.goto(f"file://{os.getcwd()}/out/bundle.html"); await pg.wait_for_timeout(500)
        await pg.pdf(path="out/AUTOPILOT.OI Money Agents Bundle.pdf", print_background=True, prefer_css_page_size=True)
        await b.close()
asyncio.run(main())
