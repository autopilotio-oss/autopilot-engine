"""AUTOPILOT.OI carousels (news and prompt posts), 1080x1350, our factory look.

    python3 tools/carousel/build.py <id>      -> docs/media/car/<id>/01.jpg ... (needs node + playwright)

Spec: tools/carousel/posts/<id>.json
  kind: "news" | "prompts"
  bg: factory still in docs/media/car/bg (f00..f11), badge: short chip over the image (optional)
  headline: cover text; *words* in lime. Keep it true: every claim must be in sources.
  slides: [{title, body}] or for prompts [{title, prompt, why}]
  cta: {big, small}   sources: [[title, url], ...] (kept in the spec, shown as "Sources" on the last slide)
Rules: no dashes in copy, no real people's photos, no logos, sample or source for every number."""
import html, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = html.escape


def lime(s):
    t = E(s).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    return re.sub(r"\*(.+?)\*", r'<span class="l">\1</span>', t)


CSS = """
@font-face{font-family:A;src:url(/docs/assets/fonts/Anton-Regular.ttf)}
@font-face{font-family:C;src:url(/docs/assets/fonts/ChakraPetch-SemiBold.ttf);font-weight:600}
@font-face{font-family:C;src:url(/docs/assets/fonts/ChakraPetch-Bold.ttf);font-weight:700}
@font-face{font-family:M;src:url(/tools/office/fonts/JetBrainsMono.ttf)}
*{box-sizing:border-box;margin:0;padding:0}body{background:#000}
.s{width:1080px;height:1350px;position:relative;overflow:hidden;background:#060606;color:#f2f2f2;font-family:C}
.l{color:#B8F23C}
.bgf{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.25) brightness(.85)}
.blob{position:absolute;inset:0;opacity:.42}
.shade{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(transparent,#060606 58%)}
.tagbox{position:absolute;left:0;top:150px;background:#B8F23C;color:#060606;font:400 66px/.9 A;padding:16px 22px 14px 26px;letter-spacing:.5px;box-shadow:6px 6px 0 #060606}
.brk{display:inline-block;background:#B8F23C;color:#060606;font:700 30px C;letter-spacing:2px;padding:4px 14px;margin-bottom:16px;font-style:italic}
.hl{position:absolute;left:44px;right:44px;bottom:118px;text-align:center}
.ln{display:block;font:400 120px/1.0 A;text-transform:uppercase;white-space:nowrap;color:#f2f2f2}
.ln.box{display:inline-block;background:#B8F23C;color:#060606;padding:4px 18px 0;margin-top:10px}
.sub{font:700 30px C;letter-spacing:6px;margin-top:16px;color:#f2f2f2}
.foot1{position:absolute;left:0;right:0;bottom:40px;text-align:center;font:700 26px C;letter-spacing:3px;color:#B8F23C}
.pg{position:absolute;right:46px;top:46px;font:700 26px C;color:#fff8;letter-spacing:2px}
.side{position:absolute;right:-120px;top:0;width:760px;height:1350px;object-fit:cover;filter:grayscale(1) contrast(1.2) brightness(.7);-webkit-mask-image:linear-gradient(90deg,transparent,#000 45%)}
.in{position:absolute;left:56px;width:600px;top:120px;bottom:120px;display:flex;flex-direction:column;justify-content:center;gap:30px}
.in.wide{width:968px}
.t{font:400 118px/.98 A;text-transform:uppercase}
.b{font:600 48px/1.32 C;color:#e8e8e8}
.b b,.why b{color:#B8F23C}
.pr{background:#0d0d0bcc;border:3px solid #B8F23C;border-radius:18px;padding:30px 32px;font:400 35px/1.42 M;color:#fff}
.pr small{display:block;font:700 22px C;letter-spacing:3px;color:#B8F23C;margin-bottom:14px}
.why{font:600 36px/1.35 C;color:#fffa}
.handle{position:absolute;left:56px;bottom:52px;font:700 26px C;letter-spacing:3px;color:#fff8}
.src{font:600 24px/1.4 C;color:#fff8}
.hero{position:absolute;left:57%;top:250px;transform:translateX(-50%) rotate(-4deg);z-index:2}
.tick{background:#0b0b0b;border:4px solid #B8F23C;border-radius:26px;padding:26px 44px 22px;box-shadow:0 0 90px #B8F23C66,12px 12px 0 #000;text-align:left}
.tick small{display:block;font:700 28px C;letter-spacing:4px;color:#B8F23C;white-space:nowrap}
.tick b{display:block;font:400 190px/.95 A;color:#fff}
.tick i{font:700 32px C;font-style:normal;color:#B8F23C;white-space:nowrap}
.chat{width:820px;background:#111;border:3px solid #333;border-radius:30px;padding:30px 34px;box-shadow:0 0 90px #B8F23C44,12px 12px 0 #000;transform:rotate(3deg)}
.chat .u{margin-left:auto;max-width:620px;background:#B8F23C;color:#060606;font:600 34px/1.3 C;padding:20px 26px;border-radius:24px 24px 6px 24px}
.chat .a{max-width:640px;margin-top:20px;background:#222;color:#eee;font:600 30px/1.35 C;padding:18px 24px;border-radius:24px 24px 24px 6px}
.chat .h{font:700 24px C;letter-spacing:3px;color:#fff8;margin-bottom:18px}
.big{font:400 300px/.85 A;color:#B8F23C;text-shadow:0 0 80px #B8F23C66,10px 10px 0 #000}
.big small{display:block;font:700 40px C;letter-spacing:6px;color:#fff;text-shadow:none;text-align:center}
"""

BLOBS = """<svg class="blob" viewBox="0 0 1080 1350" preserveAspectRatio="none"><g fill="#B8F23C">
<path d="M-40 260 C120 140 260 230 300 380 C340 520 210 610 250 760 C280 870 120 930 -40 880Z"/>
<path d="M760 90 C900 40 1120 120 1120 300 C1120 470 960 470 930 600 C900 720 1000 800 1120 820 L1120 90Z"/>
<path d="M420 120 C520 60 640 110 630 220 C620 320 520 330 470 300 C400 260 360 170 420 120Z"/></g></svg>"""


def lines_html(lines):
    out = []
    for ln in lines:
        box = ln.startswith("[") and ln.endswith("]")
        txt = ln[1:-1] if box else ln
        out.append(f'<span class="ln{" box" if box else ""}">{lime(txt)}</span>')
    return "".join(out)


def hero(h):
    if not h: return ""
    if h["type"] == "ticker":
        return f'<div class="hero"><div class="tick"><small>{E(h.get("top",""))}</small><b>{E(h["text"])}</b><i>{E(h.get("bottom",""))}</i></div></div>'
    if h["type"] == "chat":
        return f'<div class="hero" style="top:230px"><div class="chat"><div class="h">{E(h.get("app","CLAUDE"))}</div><div class="u">{E(h["you"])}</div><div class="a">{E(h["ai"])}</div></div></div>'
    if h["type"] == "big":
        return f'<div class="hero" style="top:230px"><div class="big">{E(h["text"])}<small>{E(h.get("label",""))}</small></div></div>'
    return ""


def cover(p, n):
    brk = '<div class="brk">BREAKING NEWS</div><br>' if p.get("breaking") else ""
    sub = f'<div class="sub">{E(p["subline"])}</div>' if p.get("subline") else ""
    tag = "AI<br>NEWS" if p["kind"] == "news" else "AI<br>TIPS"
    return f'''<div class="s" id="s1"><img class="bgf" src="/docs/media/car/bg/{p.get("bg","f03")}.jpg">{BLOBS}<div class="shade"></div>
<div class="tagbox">{tag}</div><div class="pg">1/{n}</div>{hero(p.get("hero"))}
<div class="hl">{brk}<div class="fitl">{lines_html(p["lines"])}</div>{sub}</div><div class="foot1">SWIPE FOR THE FULL STORY ▸</div></div>'''


def inner(p, i, n, sl):
    bg = sl.get("bg") or p.get("bg2") or "f07"
    if "prompt" in sl:
        body = f'<div class="t">{lime(sl["title"])}</div><div class="pr"><small>COPY THIS</small>{E(sl["prompt"])}</div>' + (f'<div class="why">{lime(sl["why"])}</div>' if sl.get("why") else "")
        return f'''<div class="s" id="s{i}"><img class="side" src="/docs/media/car/bg/{bg}.jpg" style="opacity:.35"><div class="pg">{i}/{n}</div>
<div class="in wide"><div class="fit2">{body}</div></div><div class="handle">@AUTOPILOT.OI · SAVE THIS</div></div>'''
    body = f'<div class="t">{lime(sl["title"])}</div><div class="b">{lime(sl["body"])}</div>'
    return f'''<div class="s" id="s{i}"><img class="side" src="/docs/media/car/bg/{bg}.jpg"><div class="pg">{i}/{n}</div>
<div class="in"><div class="fit2">{body}</div></div><div class="handle">@AUTOPILOT.OI</div></div>'''


def last(p, i, n):
    c = p["cta"]; src = ""
    if p.get("sources"):
        src = '<div class="src">Sources: ' + " · ".join(E(t) for t, _ in p["sources"]) + "</div>"
    note = f'<div class="why">{E(p["note"])}</div>' if p.get("note") else ""
    return f'''<div class="s" id="s{i}"><img class="bgf" src="/docs/media/car/bg/{p.get("bg3","f09")}.jpg" style="opacity:.45">{BLOBS}<div class="shade" style="height:80%"></div><div class="pg">{i}/{n}</div>
<div class="tagbox">AUTO<br>PILOT</div>
<div class="in wide" style="justify-content:flex-end"><div class="t">{lime(c["big"])}</div><div class="b">{lime(c["small"])}</div>{note}{src}</div>
<div class="handle">FOLLOW @AUTOPILOT.OI FOR AI NEWS FIRST</div></div>'''


FIT = """<script>
async function go(){await document.fonts.ready;
 for(const box of document.querySelectorAll('.fitl')){const ls=[...box.querySelectorAll('.ln')];
   let f=Math.min(...ls.map(l=>{l.style.fontSize='100px';const w=l.getBoundingClientRect().width;return 100*(l.classList.contains('box')?940:990)/w}));
   f=Math.min(f,170);ls.forEach(l=>l.style.fontSize=f+'px');
   while(box.parentElement.getBoundingClientRect().top<330&&f>50){f-=3;ls.forEach(l=>l.style.fontSize=f+'px')}}
 for(const el of document.querySelectorAll('.fit2')){const b=el.parentElement;let k=1;while(el.scrollHeight>b.clientHeight&&k>.5){k-=.04;el.style.zoom=k}}
 document.body.dataset.ready=1}
go();</script>"""


def build(cid):
    p = json.load(open(os.path.join(ROOT, "tools", "carousel", "posts", cid + ".json")))
    n = len(p["slides"]) + 2
    slides = [cover(p, n)] + [inner(p, i + 2, n, s) for i, s in enumerate(p["slides"])] + [last(p, n, n)]
    page = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(slides)}{FIT}</body></html>"
    hp = os.path.join(ROOT, "tools", "carousel", f"_{cid}.html"); open(hp, "w").write(page)
    out = os.path.join(ROOT, "docs", "media", "car", cid); os.makedirs(out, exist_ok=True)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1350}}}});
await p.goto('http://localhost:8779/tools/carousel/_{cid}.html');await p.waitForFunction(()=>document.body.dataset.ready==='1');
for(let i=1;i<={n};i++){{await (await p.$('#s'+i)).screenshot({{path:'{out}/'+String(i).padStart(2,'0')+'.jpg',type:'jpeg',quality:88}})}}
await b.close()}})();"""
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8779"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        import time; time.sleep(0.8)
        subprocess.run(["node", "-e", js], check=True, cwd="/tmp")
    finally:
        srv.terminate()
    print(f"carousel ready: docs/media/car/{cid}/ ({n} slides)")
    return n


if __name__ == "__main__":
    build(sys.argv[1])
