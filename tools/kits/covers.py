import asyncio, os
F = "file:///home/claude/autopilot-engine/tools/story/fonts/"
LOGO = "file:///home/claude/autopilot-engine/tools/story/logo.png"
P = [("credit","CREDIT AGENT","Audits your credit reports, writes your disputes, tracks every deadline."),
     ("bill","BILL AGENT","Checks every medical bill against your insurance before you pay."),
     ("debt","DEBT AGENT","Lower rate scripts, fastest payoff plan, what to pay every payday."),
     ("bundle","MONEY AGENTS","Credit, Bill and Debt Agent. Three Claude agents, one bundle.")]
def page(w,h,title,sub,price,big):
    return f"""<html><head><style>@font-face{{font-family:SA;src:url({F}SairaSemiCondensed-BlackItalic.otf)}}@font-face{{font-family:GE;src:url({F}Geist-SemiBold.otf)}}@font-face{{font-family:M;src:url({F}GeistMono-Medium.otf)}}
*{{margin:0;box-sizing:border-box}}body{{width:{w}px;height:{h}px;overflow:hidden;background:radial-gradient({w*.8}px {h*.9}px at 20% 15%,rgba(212,255,58,.22),transparent 60%),radial-gradient({w*.6}px {h*.7}px at 100% 100%,rgba(30,120,85,.25),transparent 60%),#040504;color:#fff;font-family:GE;position:relative;padding:{h*.09}px {w*.06}px}}
.t{{display:flex;align-items:center;gap:14px;font:{h*.035}px M;letter-spacing:3px;color:#b9bcb4}}.t img{{width:{h*.08}px;height:{h*.08}px;border-radius:50%}}
.chip{{display:inline-block;margin-top:{h*.08}px;background:#D4FF3A;color:#0a0a0a;font:{h*.04}px SA;padding:{h*.012}px {h*.025}px;border-radius:10px}}
h1{{font:{big}px/.9 SA;margin-top:{h*.035}px;color:#D4FF3A;text-shadow:0 0 60px rgba(212,255,58,.4)}}
p{{font-size:{h*.045}px;color:#d6d9d2;margin-top:{h*.03}px;max-width:{w*.75}px;line-height:1.3}}
.pr{{position:absolute;right:{w*.06}px;bottom:{h*.09}px;font:{h*.1}px SA;color:#fff}}</style></head><body>
<div class="t"><img src="{LOGO}">AUTOPILOT.OI · CLAUDE AGENT SETUP</div><div class="chip">{"BUNDLE · 3 AGENTS" if price=="$24" else "AGENT SETUP · 10 MIN"}</div><h1>{title}</h1><p>{sub}</p><div class="pr">{price}</div></body></html>"""
async def main():
    from playwright.async_api import async_playwright
    os.makedirs("out/covers", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for k,t,s in P:
            price = "$24" if k=="bundle" else "$10"
            for (w,h,big,suf) in [(1280,720,150,"cover"),(600,600,96,"thumb")]:
                pg = await b.new_page(viewport={"width":w,"height":h}); fn=os.path.abspath(f"out/covers/_{k}{suf}.html"); open(fn,"w").write(page(w,h,t,s,price,big)); await pg.goto("file://"+fn); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f"out/covers/{k}-{suf}.png"); await pg.close()
        await b.close()
asyncio.run(main())
