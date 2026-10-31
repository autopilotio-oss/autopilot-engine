"""Share images (1200x630) for every free guide -> docs/g/<slug>/og.png. Run after build.py."""
import asyncio, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides import G
F = f"file://{ROOT}/tools/story/fonts/"; LOGO = f"file://{ROOT}/tools/story/logo.png"
def page(g):
    return f"""<html><head><style>@font-face{{font-family:SA;src:url({F}SairaSemiCondensed-BlackItalic.otf)}}@font-face{{font-family:M;src:url({F}GeistMono-Medium.otf)}}
*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:630px;overflow:hidden;background:radial-gradient(900px 600px at 15% 10%,rgba(212,255,58,.2),transparent 60%),#040504;color:#fff;padding:60px 70px;position:relative}}
.t{{display:flex;align-items:center;gap:14px;font:24px M;letter-spacing:3px;color:#b9bcb4}}.t img{{width:52px;height:52px;border-radius:50%}}
.c{{display:inline-block;margin-top:44px;background:#D4FF3A;color:#0a0a0a;font:26px SA;padding:8px 16px 4px;border-radius:10px}}
h1{{font:{96 if len(g['title'])>40 else 104}px/.92 SA;margin-top:24px;color:#D4FF3A;text-transform:uppercase;max-width:1060px}}
.f{{position:absolute;left:70px;bottom:52px;font:24px M;color:#9a9d96;letter-spacing:2px}}</style></head><body>
<div class="t"><img src="{LOGO}">AUTOPILOT.OI · FREE GUIDE</div><div class="c">{g.get('cat','MONEY × AI')} · {g['kw']}</div><h1>{g['title']}</h1><div class="f">AUTOPILOTOI.APP · FREE · WORKS WITH CLAUDE</div></body></html>"""
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1200, "height": 630})
        for k, g in G.items():
            fn = f"/tmp/og_{k}.html"; open(fn, "w").write(page(g)); await pg.goto("file://" + fn); await pg.wait_for_timeout(250)
            await pg.screenshot(path=f"{ROOT}/docs/g/{k}/og.png")
        await b.close()
asyncio.run(main())
