"""Premium product covers (1280x720 + 640x360 thumb): product name, one line, real UI card. No mascot sign, no price on the robot.
python3 tools/store/covers_v2.py  -> docs/store/<slug>-cover.png"""
import os, asyncio
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = f"file://{ROOT}/tools/story/fonts/"
CSS = f"""@font-face{{font-family:IN;font-weight:800;src:url({F}Inter-ExtraBold.otf)}}@font-face{{font-family:IN;font-weight:600;src:url({F}Inter-SemiBold.otf)}}@font-face{{font-family:IN;font-weight:500;src:url({F}Inter-Medium.otf)}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1280px;height:720px;background:#050605;font-family:IN;color:#F4F6EE;overflow:hidden;position:relative}}
.glow{{position:absolute;right:-120px;top:-160px;width:760px;height:760px;border-radius:50%;background:radial-gradient(circle,rgba(212,255,58,.10),rgba(212,255,58,0) 62%)}}
.L{{position:absolute;left:84px;top:96px;width:520px}}.k{{font:600 15px IN;letter-spacing:.24em;text-transform:uppercase;color:#8d9286}}.k b{{color:#F4F6EE}}.k i{{font-style:normal;color:#D4FF3A}}
h1{{font:800 72px/1.0 IN;letter-spacing:-.045em;margin:36px 0 22px}}h1 em{{font-style:normal;color:#D4FF3A}}
.sub{{font:500 23px/1.45 IN;color:#b9beb2}}.meta{{position:absolute;left:84px;bottom:84px;font:600 15px IN;letter-spacing:.14em;text-transform:uppercase;color:#8d9286}}
.eyes{{position:absolute;right:64px;bottom:58px;display:flex;gap:10px}}.eyes i{{width:12px;height:12px;border-radius:50%;background:#D4FF3A;box-shadow:0 0 14px rgba(212,255,58,.8)}}
.R{{position:absolute;right:84px;top:118px;width:500px;background:#121412;border:1px solid #262a25;border-radius:26px;padding:26px 26px 28px;box-shadow:0 40px 90px rgba(0,0,0,.6)}}
.bar{{display:flex;justify-content:space-between;font:600 13px IN;letter-spacing:.16em;text-transform:uppercase;color:#8d9286;margin-bottom:18px}}.bar b{{color:#D4FF3A}}
.in{{display:inline-block;background:#232622;border-radius:20px 20px 20px 6px;padding:13px 17px;font:500 19px/1.35 IN;color:#e9ece3;max-width:88%}}
.who{{text-align:right;font:600 12px IN;letter-spacing:.16em;color:#D4FF3A;margin:16px 0 8px}}
.out{{margin-left:auto;max-width:92%;background:#1b1f19;border:1px solid rgba(212,255,58,.45);border-radius:20px 20px 6px 20px;padding:14px 17px;font:600 19px/1.35 IN;color:#F4F6EE}}
.act{{display:flex;gap:10px;margin-top:18px;justify-content:flex-end}}.act span{{font:600 15px IN;padding:10px 18px;border-radius:12px;border:1px solid #2c302a;color:#b9beb2}}.act .ok{{background:#D4FF3A;color:#07090a;border-color:#D4FF3A}}
.li{{display:flex;justify-content:space-between;align-items:center;padding:13px 0;border-bottom:1px solid #1f221f;font:500 18px IN;color:#e3e6dc}}.li:last-child{{border:0}}.li em{{font-style:normal;font:600 13px IN;letter-spacing:.1em;color:#8d9286}}.li .g{{color:#D4FF3A}}
"""
def page(k, h1, sub, meta, right):
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='glow'></div><div class='L'><div class='k'><b>AUTOPILOT.OI</b> · <i>{k}</i></div><h1>{h1}</h1><div class='sub'>{sub}</div></div><div class='meta'>{meta}</div>{right}<div class='eyes'><i></i><i></i></div></body></html>"
COVERS = {
 "autopilot": page("Marketplace", "Front Desk<br><em>Kit</em>", "Your replies, quotes and follow ups, drafted in your voice from your real prices.", "Setup kit · runs in your Claude account · $39",
   "<div class='R'><div class='bar'><span><b>Reply</b> · draft</span><span>Example business</span></div><div class='in'>How much for a full detail on an SUV? Free Saturday?</div><div class='who'>DRAFT · WAITING FOR YOU</div><div class='out'>A full SUV detail is $250, about 3 hours. I have Saturday at 9 or 1. Want one?</div><div class='act'><span>Edit</span><span class='ok'>Send</span></div></div>"),
 "workspace": page("Marketplace", "Office<br><em>Autopilot</em>", "Seven scheduled Claude agents on your Gmail and Calendar. They draft; you approve.", "Setup kit · paid Claude plan · $79",
   "<div class='R'><div class='bar'><span><b>Morning brief</b> · 7:00 AM</span><span>Example</span></div><div class='li'>3 new leads <em class='g'>DRAFTS READY</em></div><div class='li'>2 quotes quiet for 3 days <em class='g'>CHASES READY</em></div><div class='li'>Today: 4 jobs, first at 9:00 <em>CALENDAR</em></div><div class='li'>1 invoice overdue <em class='g'>REMINDER READY</em></div><div class='li'>2 review asks <em class='g'>READY</em></div></div>"),
 "workspace-founding": page("Workspace · in development", "Every lead,<br><em>answered.</em>", "Software for owner operated service businesses. Founding spots open, deposit refundable.", "Founding spot · $49 refundable · credited to month one",
   "<div class='R'><div class='bar'><span><b>Leads</b> · today</span><span>Product preview</span></div><div class='li'>Dana R. · Full detail, SUV <em class='g'>REPLIED 0:48</em></div><div class='li'>Mark T. · Ceramic coating <em class='g'>QUOTE READY</em></div><div class='li'>Priya S. · Interior only <em>FOLLOW UP DAY 2</em></div><div class='li'>Unknown caller · missed call <em class='g'>TEXTED BACK</em></div></div>"),
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 720})
        for slug, h in COVERS.items():
            open("/tmp/_cover.html", "w", encoding="utf-8").write(h); await pg.goto("file:///tmp/_cover.html"); await pg.wait_for_timeout(500)
            out = f"{ROOT}/docs/store/{slug}-cover.png"; await pg.screenshot(path=out)
            from PIL import Image; Image.open(out).resize((640, 360)).save(f"{ROOT}/docs/store/{slug}-thumb.png")
        await b.close()
asyncio.run(main())
