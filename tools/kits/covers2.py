"""Store covers v2 (Oct 31): product-shot style. A real page of example output on paper, editorial type,
price sticker. Outputs docs/store/<key>-cover.png (1280x720) and <key>-thumb.png (600x600).
Run from repo root: python3 tools/kits/covers2.py [key ...]"""
import asyncio, os, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = "file://" + os.path.join(ROOT, "tools", "story", "fonts") + "/"
e = html.escape

def table(head, rows, foot=None):
    t = "<table><tr>" + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr>"
    t += "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows) + "</table>"
    if foot: t += f'<div class="tot">{e(foot)}</div>'
    return t

def letter(lines):
    return '<div class="let">' + "".join(f"<p>{e(l)}</p>" for l in lines) + "</div>"

P = {
 "subs": dict(cat="MONEY", no="01", t1="SUBSCRIPTION", t2="AGENT", sub="Find every recurring charge. Cancel what you don't use.",
   doc="Monthly sweep", body=table(["Merchant", "Every", "Yearly"], [["Gym", "Month", "$180.00"], ["Photo app", "Month", "$239.88"], ["Music, 2nd plan", "Month", "$143.88"], ["Trial turned paid", "Month", "$83.88"], ["Cloud storage", "Year", "$29.99"]], "4 to cancel · drafts ready"), price="$10"),
 "bill": dict(cat="MONEY", no="02", t1="BILL", t2="AGENT", sub="Check a medical bill against your insurance before you pay.",
   doc="Bill check", body=table(["Line", "Billed", "EOB"], [["Office visit", "$310.00", "$40 copay"], ["Lab panel x2", "$192.00", "Listed once"], ["Facility fee", "$185.00", "Not listed"], ["Total due", "$687.00", "$63.40"]], "3 questions for billing"), price="$10"),
 "debt": dict(cat="MONEY", no="03", t1="DEBT", t2="AGENT", sub="A payoff plan and the script to ask for a lower rate.",
   doc="Payoff plan", body=table(["Card", "Balance", "APR", "Pay"], [["Store card", "$860", "31.0%", "$310"], ["Visa", "$4,120", "27.9%", "$120"], ["Mastercard", "$2,300", "21.4%", "$65"]], "Extra goes to the highest rate"), price="$10"),
 "refund": dict(cat="MONEY", no="04", t1="REFUND", t2="AGENT", sub="Refund requests that name your rights. You review and send.",
   doc="Refund request", body=letter(["Subject: Refund for canceled flight UA 1482, Oct 12", "Hello,", "My flight was canceled and I did not accept the rebooking. Under the DOT refund rule I'm requesting a cash refund of $318 to my original card.", "Please confirm within 7 days.", "Thank you,"]), price="$10"),
 "raise": dict(cat="MONEY", no="05", t1="RAISE", t2="AGENT", sub="Real pay data, your number and a practice run before you ask.",
   doc="Raise prep", body=table(["", ""], [["Market range", "$68k to $76k"], ["Your ask", "$74,000"], ["Walk away", "$70,000"], ["Wins logged", "9"]], "Practice: manager pushes back x3") , price="$10"),
 "video": dict(cat="TIKTOK", no="06", t1="VIDEO", t2="AGENT", sub="Scripts, CapCut edit plans and a posting schedule.",
   doc="This week", body=table(["Day", "Hook"], [["Mon", "\"I almost threw this out\""], ["Tue", "\"Stop doing this\""], ["Thu", "\"What $40 gets you\""], ["Sat", "\"3 things I wish I knew\""]], "Edit plans ready for CapCut"), price="$10"),
 "shop": dict(cat="TIKTOK", no="07", t1="SHOP", t2="AGENT", sub="Check your profit before you list on TikTok Shop.",
   doc="Profit check", body=table(["", ""], [["Price", "$24.99"], ["Product + shipping", "$9.40"], ["Fees (check Seller Center)", "$2.40"], ["Creator commission 15%", "$3.75"], ["Profit per sale", "$9.44"]], "Listing draft ready"), price="$10"),
 "sell": dict(cat="TIKTOK", no="08", t1="SALES", t2="AGENT", sub="Sales video drafts, LIVE scripts and DM reply drafts.",
   doc="DM reply drafts", body=letter(["\"Does it come in black?\"", "Yes! Black and sand. Black ships tomorrow, want the link?", "\"Is it worth it for a small kitchen?\"", "It folds flat to 2 inches, so it fits in a drawer. Here's a 10 sec demo."]), price="$10"),
 "all6": dict(cat="MONEY BUNDLE", no="5 KITS", t1="ALL 5", t2="MONEY AGENTS", sub="Bills, debt, subscriptions, refunds and raises.",
   stack=["Bill Agent", "Debt Agent", "Subscription Agent", "Refund Agent", "Raise Agent"], price="$39", was="$50"),
 "tiktok": dict(cat="TIKTOK BUNDLE", no="3 KITS", t1="ALL 3", t2="TIKTOK AGENTS", sub="Videos, your shop and sales, planned with Claude.",
   stack=["Video Agent", "Shop Agent", "Sales Agent"], price="$24", was="$30"),
}

CSS = f"""
@font-face{{font-family:BB;src:url({F}BebasNeue-Regular.ttf)}}
@font-face{{font-family:SM;src:url({F}SpaceMono-Regular.ttf)}}
@font-face{{font-family:SMB;src:url({F}SpaceMono-Bold.ttf)}}
@font-face{{font-family:IN;src:url({F}Inter-Medium.otf)}}
@font-face{{font-family:INB;src:url({F}Inter-Bold.otf)}}
*{{margin:0;box-sizing:border-box}}
body{{background:#0c0c0b;color:#f3f2ec;overflow:hidden;position:relative;font-family:IN}}
.grain{{position:absolute;inset:0;opacity:.09;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}}
.vig{{position:absolute;inset:0;background:radial-gradient(120% 90% at 70% 40%,transparent 40%,rgba(0,0,0,.55))}}
.bar{{position:absolute;left:56px;right:56px;top:40px;display:flex;justify-content:space-between;font:15px SM;letter-spacing:3px;color:#8d8c86;border-bottom:1px solid #2a2a27;padding-bottom:14px}}
.bar b{{font-family:SMB;color:#f3f2ec;letter-spacing:2px}}
.cat{{font:15px SMB;letter-spacing:4px;color:#c8f03a}}
.h{{font-family:BB;line-height:.86;letter-spacing:1px}}
.h .a{{color:#f3f2ec}}.h .b{{color:#c8f03a}}
.sub{{color:#b2b1aa;line-height:1.35}}
.inc{{font:14px SM;color:#8d8c86;letter-spacing:1px;line-height:1.9}}
.inc span{{color:#f3f2ec}}
.paper{{position:absolute;background:#f2f0e8;color:#141412;border-radius:6px;box-shadow:0 30px 60px rgba(0,0,0,.6),0 6px 14px rgba(0,0,0,.4);padding:30px 30px 26px}}
.paper.back{{background:#d9d6cb}}
.ph{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #141412;padding-bottom:10px;margin-bottom:14px}}
.ph b{{font:30px BB;letter-spacing:1px}}.ph span{{font:11px SM;letter-spacing:2px;color:#6d6b63}}
table{{width:100%;border-collapse:collapse;font:15px SM}}
th{{text-align:left;font:11px SMB;letter-spacing:1.5px;color:#6d6b63;text-transform:uppercase;padding:0 0 8px}}
td{{padding:9px 0;border-top:1px solid #d3d0c4}}td:last-child,th:last-child{{text-align:right}}
.tot{{margin-top:14px;background:#141412;color:#c8f03a;font:13px SMB;letter-spacing:1px;padding:10px 12px;border-radius:4px}}
.let p{{font:15px/1.5 SM;margin-bottom:10px}}
.foot{{position:absolute;left:30px;right:30px;bottom:14px;font:10px SM;letter-spacing:2px;color:#8a887f;display:flex;justify-content:space-between}}
.st{{position:absolute;z-index:50;width:150px;height:150px;border-radius:50%;background:#c8f03a;color:#0c0c0b;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);box-shadow:0 14px 30px rgba(0,0,0,.45)}}
.st b{{font:62px/.8 BB}}.st span{{font:11px SMB;letter-spacing:2px;margin-top:6px}}.st s{{font:15px SM;opacity:.6}}
.file{{position:absolute;background:#f2f0e8;color:#141412;border-radius:6px;box-shadow:0 -2px 0 rgba(0,0,0,.08),0 22px 46px rgba(0,0,0,.55);padding:0 26px;border-top:1px solid #fff}}
.file:nth-child(odd){{background:#ebe8de}}
.fh{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #cfccbf}}
.fh b{{font-family:BB;letter-spacing:1px}}.fh span{{font-family:SM;letter-spacing:2px;color:#6d6b63}}
.file i{{display:block;height:10px;background:#dcd9ce;border-radius:2px;margin-top:16px}}.file i.s{{width:60%}}
.mini{{position:absolute;width:300px;height:390px;background:#f2f0e8;color:#141412;border-radius:6px;box-shadow:0 24px 50px rgba(0,0,0,.6);padding:24px}}
.mini .k{{font:11px SM;letter-spacing:2px;color:#6d6b63}}.mini b{{display:block;font:44px/.9 BB;margin-top:10px}}
.mini i{{display:block;height:9px;background:#dcd9ce;border-radius:2px;margin-top:12px}}.mini i.s{{width:60%}}
"""

def paper_html(p, x, y, w, h, rot, scale=1):
    if "stack" in p: return ""
    return (f'<div class="paper back" style="left:{x+18}px;top:{y+14}px;width:{w}px;height:{h}px;transform:rotate({rot+3}deg) scale({scale})"></div>'
            f'<div class="paper" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg) scale({scale})">'
            f'<div class="ph"><b>{e(p["doc"])}</b><span>EXAMPLE OUTPUT</span></div>{p["body"]}'
            f'<div class="foot"><span>AUTOPILOT.OI</span><span>{e(p["t1"].title())} {e(p["t2"].title())}</span></div></div>')

def stack_html(p, cx, cy, sc=1.0):
    n = len(p["stack"]); out = ""; step = 62 * sc; w = 420 * sc; h = 360 * sc
    top = cy - (h + step * (n - 1)) / 2
    for i, name in enumerate(p["stack"]):
        out += (f'<div class="file" style="left:{cx - w/2 + i*14*sc}px;top:{top + i*step}px;width:{w}px;height:{h}px;z-index:{i};transform:rotate(-5deg)">'
                f'<div class="fh" style="height:{step}px"><b style="font-size:{34*sc}px">{e(name)}</b><span style="font-size:{10*sc}px">KIT {i+1:02d}</span></div>'
                f'<i></i><i></i><i class="s"></i><i></i><i class="s"></i><i></i></div>')
    return out

def sticker(p, x, y, size=150):
    was = f'<s>{p["was"]}</s>' if p.get("was") else ""
    return f'<div class="st" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px">{was}<b>{p["price"]}</b><span>{"BUNDLE" if p.get("was") else "PROMPT KIT"}</span></div>'

def cover(k, p):
    right = stack_html(p, 930, 410, 0.85) if "stack" in p else paper_html(p, 690, 120, 470, 520, -4)
    return f"""<!DOCTYPE html><html><head><style>{CSS} body{{width:1280px;height:720px}}</style></head><body><div class="grain"></div><div class="vig"></div>
<div class="bar"><b>AUTOPILOT.OI</b><span>CLAUDE PROMPT KIT · {'NO. ' if p['no'].isdigit() else ''}{p['no']}</span></div>
<div style="position:absolute;left:56px;top:128px;width:600px">
<div class="cat">{e(p['cat'])}</div>
<div class="h" style="font-size:{150 if len(p['t1'])<10 else 118}px;margin-top:18px"><div class="a">{e(p['t1'])}</div><div class="b">{e(p['t2'])}</div></div>
<div class="sub" style="font-size:24px;margin-top:22px;max-width:540px">{e(p['sub'])}</div></div>
<div class="inc" style="position:absolute;left:56px;bottom:46px"><span>INSIDE</span> · Master prompt · 5 starter prompts · Tracker · 10 min setup</div>
{right}{sticker(p, 590 if 'stack' not in p else 1080, 455 if 'stack' not in p else 96)}
</body></html>"""

def thumb(k, p):
    right = stack_html(p, 300, 430, 0.62) if "stack" in p else paper_html(p, 120, 175, 380, 410, -4)
    t1 = (64 if "stack" in p else 96) if len(p['t1']) < 10 else 76
    return f"""<!DOCTYPE html><html><head><style>{CSS} body{{width:600px;height:600px}} .paper table{{font-size:13px}} .let p{{font-size:12.5px;margin-bottom:7px}}</style></head><body><div class="grain"></div><div class="vig"></div>
<div style="position:absolute;left:40px;top:38px"><div class="cat" style="font-size:13px">{e(p['cat'])}</div>
<div class="h" style="font-size:{t1}px;margin-top:10px"><span class="a">{e(p['t1'])}</span> <span class="b">{e(p['t2'])}</span></div></div>
{right}{sticker(p, 40, 440, 116) if 'stack' not in p else sticker(p, 452, 452, 112)}</body></html>"""

async def main(keys):
    from playwright.async_api import async_playwright
    out = os.path.join(ROOT, "docs", "store"); tmp = "/tmp/cov2"; os.makedirs(tmp, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for k in keys:
            p = P[k]
            for kind, w, h, fn in [("cover", 1280, 720, cover), ("thumb", 600, 600, thumb)]:
                pg = await b.new_page(viewport={"width": w, "height": h})
                f = f"{tmp}/{k}-{kind}.html"; open(f, "w").write(fn(k, p))
                await pg.goto("file://" + f); await pg.wait_for_timeout(350)
                await pg.screenshot(path=f"{out}/{k}-{kind}.png"); await pg.close()
            print("made", k)
        await b.close()

asyncio.run(main(sys.argv[1:] or list(P)))
