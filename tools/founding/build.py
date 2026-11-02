"""Workspace founding member PDF (delivered with the refundable deposit). python3 tools/founding/build.py out.pdf"""
import sys, asyncio, os
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = f"file://{ROOT}/tools/story/fonts/"
H = f"""<html><head><style>
@font-face{{font-family:IN;font-weight:800;src:url({F}Inter-ExtraBold.otf)}}@font-face{{font-family:IN;font-weight:600;src:url({F}Inter-SemiBold.otf)}}@font-face{{font-family:IN;font-weight:500;src:url({F}Inter-Medium.otf)}}
@page{{size:8.5in 11in;margin:0}}*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:IN;color:#F4F6EE;background:#050605}}
.pg{{width:8.5in;height:11in;padding:.8in .8in;position:relative;background:#050605;page-break-after:always}}
.k{{font:600 10px IN;letter-spacing:.22em;text-transform:uppercase;color:#9aa08f}}.k b{{color:#D4FF3A}}
h1{{font:800 44px/1.04 IN;letter-spacing:-.03em;margin:28px 0 16px}}h1 em{{font-style:normal;color:#D4FF3A}}
h2{{font:800 20px IN;letter-spacing:-.02em;margin:30px 0 12px}}
p,li{{font:500 13.5px/1.6 IN;color:#cfd3c7}}ul{{margin-left:18px}}li{{margin:6px 0}}
.card{{background:#141614;border:1px solid #262a25;border-radius:14px;padding:18px 20px;margin:12px 0}}
.row{{display:flex;gap:14px;padding:12px 0;border-bottom:1px solid #1f221f}}.row b{{font:600 12px IN;color:#D4FF3A;min-width:92px}}
.ft{{position:absolute;left:.8in;right:.8in;bottom:.5in;font:500 9.5px IN;color:#6f746a}}
</style></head><body>
<div class="pg"><div class="k"><b>AUTOPILOT.OI</b> · Workspace · founding member</div>
<h1>You're a Workspace<br><em>founding member.</em></h1>
<p>Thank you. Your $49 deposit holds your founding spot for AUTOPILOT Workspace, the software we're building for owner operated service businesses: every new lead answered within a minute, the reply and the quote drafted for you, quiet quotes followed up, and one inbox you approve from your phone.</p>
<div class="card"><p><b style="color:#F4F6EE">Status, honestly:</b> Workspace is in development. It is not available yet. This page tells you exactly what your deposit gets you and how to get it back.</p></div>
<h2>What your deposit gets you</h2>
<ul><li><b style="color:#F4F6EE">$49 credited</b> to your first paid month.</li><li><b style="color:#F4F6EE">First access:</b> founding members get invited to the beta before anyone else.</li><li><b style="color:#F4F6EE">Founding price:</b> $99 a month, locked for your first 12 months.</li><li><b style="color:#F4F6EE">A say in what gets built:</b> we'll email you short questions as we build.</li></ul>
<h2>Refunds</h2>
<ul><li>Changed your mind? Reply to your Gumroad receipt anytime before your first paid month and you get the full $49 back.</li><li>If Workspace isn't open to founding members by February 28, 2027, we refund every deposit in full.</li></ul>
<div class="ft">AUTOPILOT.OI is independent and not affiliated with Anthropic. Questions: reply to your Gumroad receipt.</div></div>
<div class="pg"><div class="k"><b>AUTOPILOT.OI</b> · Workspace · what happens next</div>
<h2 style="margin-top:20px">What happens next</h2>
<div class="row"><b>This week</b><p>You'll get a short email asking what kind of business you run, how leads reach you and which phone system you use. Your answers decide the first integrations.</p></div>
<div class="row"><b>Beta</b><p>When the beta opens we invite founding members in the order they joined. Setup takes about 10 minutes on your phone.</p></div>
<div class="row"><b>Launch</b><p>Your $49 is applied to the first month. You only start paying when you choose to continue.</p></div>
<h2>What Workspace will and won't do</h2>
<div class="card"><p><b style="color:#F4F6EE">Planned for the first version:</b> a lead inbox for calls, texts and web forms; an instant acknowledgment you write once; drafted replies and quotes from your prices and rules; follow ups on quiet quotes; a Monday report.</p></div>
<div class="card"><p><b style="color:#F4F6EE">Always true:</b> apart from the acknowledgment you write and approve yourself, nothing goes to a customer without your tap. You can see every message it drafts and every message it sends.</p></div>
<p style="margin-top:16px">Planned features can change as we build and learn from founding members. We'll tell you what changes and why.</p>
<div class="ft">AUTOPILOT.OI is independent and not affiliated with Anthropic.</div></div>
</body></html>"""
async def main(out):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(); open("/tmp/_founding.html", "w").write(H); await pg.goto("file:///tmp/_founding.html"); await pg.wait_for_timeout(600)
        await pg.pdf(path=out, width="8.5in", height="11in", print_background=True); await b.close()
asyncio.run(main(sys.argv[1]))
