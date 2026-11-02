"""1080x1350 demo cards for posts: a real customer style message and the kit's draft for an example business."""
import asyncio, os, html
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); F = f"file://{ROOT}/tools/story/fonts/"; e = html.escape
CARDS = [("fd-price", "A price question at 7:40 PM", "Northside Detail (example)", "How much for a full detail on an SUV? Free Saturday?", "Hi! A full SUV detail is $250 and takes about 3 hours. We come to you. I have Saturday at 9 AM or 1 PM. Want me to lock one in? Mike"),
         ("fd-late", "A request that came in after hours", "Bright Home Cleaning (example)", "Hi, any chance you can do a move out clean this weekend?", "Hi! Yes, we do move out cleans. For the price I need the size of the home: how many bedrooms and bathrooms? [CHECK: weekend availability] Ana"),
         ("fd-chase", "A quote that went quiet", "Ridge Handyman (example)", "(Quote sent Friday: replace 3 interior doors, $620. No reply.)", "Hi Jen, following up on the 3 interior doors ($620 installed). I can order the doors this week so we're set for next Tuesday. Should I go ahead? Sam")]
def h(t, biz, q, a):
    return f"""<html><head><meta charset='utf-8'><style>@font-face{{font-family:IN;font-weight:800;src:url({F}Inter-ExtraBold.otf)}}@font-face{{font-family:IN;font-weight:600;src:url({F}Inter-SemiBold.otf)}}@font-face{{font-family:IN;font-weight:500;src:url({F}Inter-Medium.otf)}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1350px;background:#050605;font-family:IN;color:#F4F6EE;padding:90px 80px;position:relative}}
.k{{font:600 24px IN;letter-spacing:.2em;text-transform:uppercase;color:#9aa08f}}.k b{{color:#D4FF3A}}h1{{font:800 76px/1.04 IN;letter-spacing:-.04em;margin:30px 0 56px}}
.ui{{background:#0e100e;border:2px solid #232723;border-radius:44px;padding:40px}}.biz{{font:600 22px IN;letter-spacing:.14em;color:#9aa08f;margin-bottom:22px}}
.in{{display:inline-block;background:#232622;border-radius:32px 32px 32px 10px;padding:26px 30px;font:500 36px/1.35 IN;color:#e9ece3}}
.lab{{font:600 22px IN;letter-spacing:.14em;color:#D4FF3A;margin:34px 0 14px}}.out{{background:#141714;border:2px solid rgba(212,255,58,.5);border-radius:32px 32px 10px 32px;padding:28px 30px;font:600 38px/1.4 IN}}
.ft{{position:absolute;left:80px;right:80px;bottom:80px;display:flex;justify-content:space-between;font:600 24px IN;color:#7d8277;letter-spacing:.06em}}.ft b{{color:#F4F6EE}}</style></head><body>
<div class='k'><b>AUTOPILOT.OI</b> · Front Desk Kit</div><h1>{e(t)}</h1><div class='ui'><div class='biz'>{e(biz.upper())}</div><div class='in'>{e(q)}</div><div class='lab'>KIT DRAFT · YOU REVIEW AND SEND</div><div class='out'>{e(a)}</div></div>
<div class='ft'><span>Example business. Drafts only, you send.</span><b>autopilotoi.app/front-desk</b></div></body></html>"""
async def main():
    os.makedirs(f"{ROOT}/docs/media/cards", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, *rest in CARDS:
            open("/tmp/_fdc.html", "w", encoding="utf-8").write(h(*rest)); await pg.goto("file:///tmp/_fdc.html"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=f"{ROOT}/docs/media/cards/{n}.jpg", type="jpeg", quality=88)
        await b.close()
asyncio.run(main())
