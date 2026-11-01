"""AUTOPILOT.OI carousels: news and prompt posts, 1080x1350, tabloid news style (lime, Anton).

    python3 tools/carousel/build.py <id>      -> docs/media/car/<id>/01.jpg ... (needs node + playwright)

Spec: tools/carousel/posts/<id>.json
  kind: "news" | "prompts";  breaking: true (or ribbon: "EXCLUSIVE" etc.)
  lines: cover headline, one entry per stacked line. *word* = lime word, {line} = whole line lime, [line] = lime box line.
  subline: small letterspaced line under the headline (optional)
  hero: the evidence object on the cover (no real people's photos, no logos):
     {"type":"doc","org":"SEC FILING","date":"OCT 26 2026","title":"FORM S-1","marks":["Ticker: ANT"],"stamp":"FILED","x":230,"y":170}
     {"type":"phone","app":"CLAUDE","you":"...","ai":"...","notes":[["TITLE","text"]],"x":330,"y":120}
     {"type":"ticker","top":"NASDAQ","text":"ANT","bottom":"...","x":220,"y":230}
     {"type":"big","text":"$9.4M","label":"...","x":200,"y":200}
     optional "ring":[x,y,size] lime circle callout, "chevrons":[x,y]
  bg_words: 2 to 4 big words for the newspaper collage; bg_facts: short true lines for its columns
  slides: [{title, body, hero?}] or for prompts [{title, prompt, why}]; cta: {big, small}; note; sources: [[title, url]]
Copy rules: true and sourced, no dashes, plain words. <b>..</b> allowed in body text (lime bold)."""
import html, json, os, re, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E = html.escape


def lime(s):
    t = E(s).replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")
    return re.sub(r"\*(.+?)\*", r'<span class="l">\1</span>', t)


def plain(s):
    return E(re.sub(r"</?b>|\*", "", s))


CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "style.css")).read()

GRAIN = ('<svg class="grain" width="1080" height="1350"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".9" '
         'numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>')
BLOBS = ('<svg class="blob" viewBox="0 0 1080 1350" preserveAspectRatio="none"><defs><radialGradient id="lg" cx="40%" cy="35%" r="75%"><stop offset="0" stop-color="#F0FF9A"/><stop offset=".55" stop-color="#D4FF3A"/><stop offset="1" stop-color="#B9F01E"/></radialGradient></defs><g fill="url(#lg)">'
         '<path d="M150 230 C330 120 520 210 560 360 C600 500 470 560 520 690 C560 800 420 860 300 800 C170 740 60 660 90 520 C110 420 20 320 150 230Z"/>'
         '<path d="M700 160 C820 100 1010 140 1050 290 C1090 440 960 470 940 590 C920 700 1010 760 980 820 C900 860 780 780 720 680 C650 560 600 230 700 160Z"/></g></svg>')


def paper(p, light=False):
    words = p.get("bg_words") or ["AI", "NEWS"]
    facts = p.get("bg_facts") or [s.get("body", s.get("why", "")) for s in p.get("slides", [])]
    blocks = "".join(f"<b>{E(w)}</b>{plain(f)} " for w, f in zip((words * 4)[:8], (facts * 4)[:8]))
    return (f'<div class="paper{" light" if light else ""}"><div class="mast"><span>THE AI WIRE</span><small>VOL. 01 &middot; {E(p.get("ow", {}).get("fig", "01"))}</small></div>'
            f'<div class="bar2"><span>BREAKING</span><span>TECH &middot; MONEY &middot; YOU</span><span>@AUTOPILOT.OI</span></div>'
            f'<div class="big1">{E(" ".join(words[:2]))}</div><div class="cols">{blocks}</div></div>')


def evidence(h):
    if not h:
        return ""
    t = h["type"]; x, y = h.get("x", 230), h.get("y", 180); out = ""
    if t == "doc":
        lines = "".join('<div class="dl" style="width:%d%%"></div>' % w for w in (96, 88, 92, 70))
        marks = "".join(f'<p style="margin:12px 0"><mark>{E(m)}</mark></p>' for m in h.get("marks", []))
        stamp = f'<div class="stamp">{E(h["stamp"])}</div>' if h.get("stamp") else ""
        out = (f'<div class="ev" style="left:{x}px;top:{y}px"><div class="doc"><div class="dh"><span>{E(h.get("org", ""))}</span>'
               f'<span>{E(h.get("date", ""))}</span></div><h4>{E(h["title"])}</h4>{lines}{marks}<div class="dl" style="width:80%"></div>{stamp}</div></div>')
    elif t == "phone":
        inner = "".join(f'<div class="nt"><b>{E(a)}</b>{E(b)}</div>' for a, b in h.get("notes", []))
        if h.get("you"): inner += f'<div class="u">{E(h["you"])}</div>'
        if h.get("ai"): inner += f'<div class="a">{E(h["ai"])}</div>'
        out = (f'<div class="ev" style="left:{x}px;top:{y}px"><div class="phone"><div class="notch"></div>'
               f'<div class="app">{E(h.get("app", ""))}</div>{inner}</div></div>')
    elif t == "ticker":
        spark = ('<svg width="550" height="90"><polyline points="0,80 60,70 120,74 180,52 240,58 300,36 360,44 420,22 480,28 550,8" '
                 'fill="none" stroke="#D4FF3A" stroke-width="7"/></svg>') if h.get("spark", True) else ""
        out = (f'<div class="ev" style="left:{x}px;top:{y}px"><div class="tick"><small>{E(h.get("top", ""))}</small>'
               f'<b>{E(h["text"])}</b><i>{E(h.get("bottom", ""))}</i>{spark}</div></div>')
    elif t == "cutout":
        w = h.get("w", 760)
        return f'<img class="cut{" duo" if h.get("duo") else ""}" src="/docs/media/car/{E(h["src"])}" style="left:{x}px;top:{y}px;width:{w}px">' + (
            f'<div class="ring" style="left:{h["ring"][0]}px;top:{h["ring"][1]}px;width:{h["ring"][2]}px;height:{h["ring"][2]}px"></div>' if h.get("ring") else "")
    elif t == "big":
        out = f'<div class="ev" style="left:{x}px;top:{y}px"><div class="bigno">{E(h["text"])}<small>{E(h.get("label", ""))}</small></div></div>'
    if h.get("ring"):
        rx, ry, rs = h["ring"]; out += f'<div class="ring" style="left:{rx}px;top:{ry}px;width:{rs}px;height:{rs}px"></div>'
    if h.get("chevrons"):
        cx, cy = h["chevrons"]; out += f'<div class="chev" style="left:{cx}px;top:{cy}px"><span>&#8250;&#8250;</span>&#8250;&#8250;&#8250;</div>'
    return out


def lines_html(lines):
    out = []
    for ln in lines:
        box = ln.startswith("[") and ln.endswith("]"); lm = ln.startswith("{") and ln.endswith("}")
        txt = ln[1:-1] if (box or lm) else ln
        out.append(f'<span class="ln{" box" if box else ""}{" lm" if lm else ""}">{lime(txt)}</span>')
    return "".join(out)


def barcode(x, y, w=210, h=54, seed=7):
    import random
    r = random.Random(seed); bars = []; cx = 0
    while cx < w:
        bw = r.choice([2, 2, 3, 4, 6]); gap = r.choice([2, 3, 4])
        bars.append(f'<rect x="{cx}" y="0" width="{bw}" height="{h}" fill="#f4f4f4"/>'); cx += bw + gap
    return f'<svg class="bc" style="left:{x}px;top:{y}px" width="{w}" height="{h + 22}">{"".join(bars)}<text x="0" y="{h + 18}" fill="#fff9" font-family="I" font-weight="700" font-size="14" letter-spacing="3">AP.{seed:04d}.OI</text></svg>'


def offwhite(p, n, cover=True):
    """Clean by default: just the ap. logo. One optional accent per post via "ow": {"zip": "WORD"} or {"label": .., "pointer": ..}."""
    ow = p.get("ow", {}); out = ""
    if cover:
        out += '<img class="aplogo" src="/docs/logo.png">'
        if ow.get("zip"):
            zx, zy = ow.get("zip_at", [820, 230])
            out += f'<div class="zip" style="left:{zx}px;top:{zy}px;transform:rotate(9deg)"><div class="str"></div><div class="tg">"{E(ow["zip"])}"<small>AUTOPILOT.OI</small></div></div>'
        elif ow.get("label"):
            lx, ly = ow.get("label_at", [700, 560]); out += f'<div class="lab" style="left:{lx}px;top:{ly}px"><b>"{E(ow["label"])}"</b></div>'
            if ow.get("pointer"):
                px, py, pw, pa = ow["pointer"]; out += f'<div class="ptr" style="left:{px}px;top:{py}px;width:{pw}px;transform:rotate({pa}deg)"></div>'
    return out


def wall():
    lines = "".join(f'<i style="top:{60 + k * 64}px"></i>' for k in range(19))
    marks = "".join(f'<span style="left:22px;top:{40 + k * 128}px">{90 - k * 4}&quot;</span><span style="right:22px;top:{40 + k * 128}px">{90 - k * 4}&quot;</span>' for k in range(10))
    return f'<div class="wallbg">{lines}{marks}</div>'


def chevrons(x, y, n_gray=2, n_lime=3):
    return f'<div class="chev2" style="left:{x}px;top:{y}px">' + "<b></b>" * n_gray + '<b class="g"></b>' * n_lime + "</div>"


def cover_photo(p, n):
    """Photo cover (news with a real photo): photo up top, the subject cut out and lifted off it with a lime rim,
    optional round badge holding a second cutout (an object, never a company logo), divider with our mark, then the
    headline as full width justified lines (*word* = lime). Spec: p["photo"] = {src, cut?, badge?, pos?, cut_h?, cut_x?,
    lines: [...], sub?, kicker?}"""
    ph = p["photo"]
    cut = (f'<img class="ph-cut" src="{E(ph["cut"])}" style="height:{ph.get("cut_h", 760)}px;left:{ph.get("cut_x", 540)}px">'
           if ph.get("cut") else "")
    badge = f'<div class="ph-badge"><img src="{E(ph["badge"])}"></div>' if ph.get("badge") else ""
    kick = f'<div class="ph-kick">{E(ph["kicker"])}</div>' if ph.get("kicker") else ""
    lines = "".join(f'<div class="ln">{lime(l)}</div>' for l in ph["lines"])
    sub = f'<div class="ph-sub">{lime(ph["sub"])}</div>' if ph.get("sub") else ""
    return (f'<div class="s L-photo{" has-cut" if cut else ""}" id="s1">'
            f'<div class="ph-bg" style="background-image:url(\'{E(ph["src"])}\');background-position:{ph.get("pos", "center 30%")}"></div>'
            f'<div class="ph-tint"></div>{cut}{badge}{kick}'
            f'<div class="ph-div"><i></i><img src="/docs/logo.png"><i></i></div>'
            f'<div class="ph-text"><div class="fitl" data-w="980">{lines}</div>{sub}</div>'
            f'<div class="ph-swipe">SWIPE FOR MORE <b>&#9656;</b></div>{GRAIN}<div class="pg">1/{n}</div></div>')


def cover(p, n):
    if p.get("photo"):
        return cover_photo(p, n)
    if p.get("cover_html"):
        cls = p.get("cover_bg", "bg-black")
        lava = ""
        if p.get("lava", True):
            pal = {"bg-black": "dark", "bg-lime": "lime", "bg-white": "white"}.get(cls, "dark")
            lava = f'<iframe class="lava" style="opacity:{p.get('lava_opacity', {'dark': .6, 'lime': .75, 'white': .8}[pal])}" src="/tools/carousel/lava.html?pal={pal}&seed={p.get("seed", 2)}"></iframe>'
        body = f'<div class="lavafg">{p["cover_html"]}</div>' if lava else p["cover_html"]
        return (f'<div class="s {cls}" id="s1">{lava}{body}{GRAIN if p.get("grain", True) else ""}'
                f'<img class="aplogo" src="/docs/logo.png"><div class="pg">1/{n}</div></div>')
    lay = p.get("layout", "stack")
    if lay == "stack":
        return cover_stack(p, n)
    tag = ('<span class="qm">&ldquo;</span>AI<br>NEWS<span class="qm">&rdquo;</span>' if p["kind"] == "news"
           else '<span class="qm">&ldquo;</span>AI<br>TIPS<span class="qm">&rdquo;</span>')
    rib = p.get("ribbon") or ("BREAKING NEWS" if p.get("breaking") else "")
    brk = f'<div class="brk">{E(rib)}</div><br>' if rib else ""
    ev = evidence(p.get("hero")); ow = offwhite(p, n)
    head = f'<div class="tagbox">{tag}</div><div class="pg">1/{n}</div>'
    foot = '<div class="foot1">SWIPE FOR THE FULL STORY &#9656;</div>'
    dek = f'<div class="dek">{lime(p["dek"])}</div>' if p.get("dek") else ""
    if lay == "split":
        return (f'<div class="s L-split" id="s1">{paper(p)}<div class="shade2"></div>{BLOBS.replace("class=\"blob\"", "class=\"blob\" style=\"left:380px\"")}{ev}{GRAIN}{ow}{head}'
                f'<div class="hl2">{brk}<div class="fitl" data-w="560">{lines_html(p["lines"])}</div>{dek}</div>{foot}</div>')
    if lay == "wall":
        sub = f'<div class="sub">{E(p["subline"])}</div>' if p.get("subline") else ""
        return (f'<div class="s L-wall" id="s1">{wall()}{BLOBS}{ev}<div class="band"></div>{GRAIN}{ow}{head}'
                f'<div class="hl">{brk}<div class="fitl">{lines_html(p["lines"])}</div>{sub}</div>{foot}</div>')
    if lay == "front":
        sub = f'<div class="sub">{E(p["subline"])}</div>' if p.get("subline") else ""
        return (f'<div class="s L-front" id="s1">{paper(p, light=True)}{ev}<div class="shade"></div>{GRAIN}{ow}{head}'
                f'<div class="hl">{brk}<div class="fitl">{lines_html(p["lines"])}</div>{sub}</div>{foot}</div>')
    if lay == "arrow":
        kick = f'<div class="kick">{lime(p["kicker"])}</div>' if p.get("kicker") else ""
        cx, cy = p.get("chev_at", [470, 980])
        return (f'<div class="s L-arrow" id="s1"><div style="opacity:.55">{paper(p)}</div>{ev}{GRAIN}{ow}{head}{chevrons(cx, cy)}'
                f'<div class="hl3">{brk}<div class="fitl" data-w="{p.get('head_w', 520)}">{lines_html(p["lines"])}</div>{kick}</div>{foot}</div>')
    return cover_stack(p, n)


def cover_stack(p, n):
    rib = p.get("ribbon") or ("BREAKING NEWS" if p.get("breaking") else "")
    brk = f'<div class="brk">{E(rib)}</div><br>' if rib else ""
    sub = f'<div class="sub">{E(p["subline"])}</div>' if p.get("subline") else ""
    tag = ('<span class="qm">&ldquo;</span>AI<br>NEWS<span class="qm">&rdquo;</span>' if p["kind"] == "news"
           else '<span class="qm">&ldquo;</span>AI<br>TIPS<span class="qm">&rdquo;</span>')
    return (f'<div class="s" id="s1">{paper(p)}{BLOBS}{evidence(p.get("hero"))}<div class="shade"></div>{GRAIN}{offwhite(p, n)}'
            f'<div class="tagbox">{tag}</div><div class="pg">1/{n}</div>'
            f'<div class="hl">{brk}<div class="fitl">{lines_html(p["lines"])}</div>{sub}</div>'
            f'<div class="foot1">SWIPE FOR THE FULL STORY &#9656;</div></div>')


def inner(p, i, n, sl):
    if "prompt" in sl:
        body = (f'<div class="num">PROMPT {i - 1}</div><div class="t">{lime(sl["title"])}</div>'
                f'<div class="pr"><small>COPY THIS</small>{E(sl["prompt"])}</div>' + (f'<div class="why">{lime(sl["why"])}</div>' if sl.get("why") else ""))
        return (f'<div class="s" id="s{i}"><div class="side" style="opacity:.35">{paper(p)}</div>{GRAIN}<div class="pg">{i}/{n}</div>'
                f'<div class="in wide"><div class="fit2">{body}</div></div><div class="handle"><img class="hlogo" src="/docs/logo.png">"SAVE THIS" &nbsp;&middot;&nbsp; @AUTOPILOT.OI &nbsp;&middot;&nbsp; FIG. {i:02d}</div></div>')
    body = f'<div class="t">{lime(sl["title"])}</div><div class="b">{lime(sl["body"])}</div>'
    ev = evidence(sl["hero"]) if sl.get("hero") else ""
    if sl.get("lite") or (i % 3 == 0 and sl.get("lite") is not False):
        big = f'<div class="bignum">{E(sl["num"])}</div>' if sl.get("num") else ""
        return (f'<div class="s lite" id="s{i}">{GRAIN}<div class="pg">{i}/{n}</div>'
                f'<div class="in wide"><div class="fit2">{big}{body}</div></div><div class="handle"><img class="hlogo" src="/docs/logo.png">"@AUTOPILOT.OI" &nbsp;&middot;&nbsp; FIG. {i:02d}</div></div>')
    return (f'<div class="s" id="s{i}"><div class="side">{paper(p)}</div>{ev}'
            f'<div class="shade" style="height:100%;background:linear-gradient(90deg,#0c0c0c 46%,#0c0c0c00 80%)"></div>{GRAIN}'
            f'<div class="pg">{i}/{n}</div><div class="in"><div class="fit2">{body}</div></div>'
            f'<div class="handle"><img class="hlogo" src="/docs/logo.png">"@AUTOPILOT.OI" &nbsp;&middot;&nbsp; FIG. {i:02d}</div></div>')


def last(p, i, n):
    c = p["cta"]
    src = ('<div class="src">Sources: ' + " &middot; ".join(E(t) for t, _ in p["sources"]) + "</div>") if p.get("sources") else ""
    note = f'<div class="why">{E(p["note"])}</div>' if p.get("note") else ""
    return (f'<div class="s" id="s{i}">{paper(p)}<div style="opacity:.3">{BLOBS}</div><div class="shade" style="height:88%"></div>{GRAIN}<div class="pg">{i}/{n}</div>'
            f'<div class="tagbox"><span class="qm">&ldquo;</span>AUTO<br>PILOT<span class="qm">&rdquo;</span></div><div class="in wide" style="justify-content:flex-end">'
            f'<div class="t">{lime(c["big"])}</div><div class="b">{lime(c["small"])}</div>{note}{src}</div>'
            f'<div class="handle"><img class="hlogo" src="/docs/logo.png">FOLLOW @AUTOPILOT.OI &middot; AI NEWS FIRST</div></div>')


FIT = """<script>
async function go(){await document.fonts.ready;
 for(const box of document.querySelectorAll('.fitl')){const ls=[...box.querySelectorAll('.ln')];
   const W=+(box.dataset.w||1000);
   ls.forEach(l=>{l.style.fontSize='100px';const w=l.getBoundingClientRect().width;l.dataset.f=Math.min(230,100*(l.classList.contains('box')?W*.96:W)/w)});
   let k=1;const apply=()=>ls.forEach(l=>l.style.fontSize=(l.dataset.f*k)+'px');apply();
   const P=box.parentElement;
   if(box.dataset.w){while(P.getBoundingClientRect().bottom>1240&&k>.4){k-=.03;apply()}}
   else{while(P.getBoundingClientRect().top<560&&k>.4){k-=.03;apply()}}}
 for(const el of document.querySelectorAll('.fit2')){const b=el.parentElement;let k=1;while(el.scrollHeight>b.clientHeight&&k>.5){k-=.04;el.style.zoom=k}}
 document.body.dataset.ready=1}
go();</script>"""


def build(cid):
    p = json.load(open(os.path.join(ROOT, "tools", "carousel", "posts", cid + ".json")))
    n = len(p["slides"]) + 2
    slides = [cover(p, n)] + [inner(p, i + 2, n, s) for i, s in enumerate(p["slides"])] + [last(p, n, n)]
    page = f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body class=\"th-{p.get('theme', 'dark')}\">{''.join(slides)}{FIT}</body></html>"
    hp = os.path.join(ROOT, "tools", "carousel", f"_{cid}.html"); open(hp, "w").write(page)
    out = os.path.join(ROOT, "docs", "media", "car", cid); os.makedirs(out, exist_ok=True)
    lava = bool(p.get("cover_html")) and p.get("lava", True)
    FRAMES = 192 if (lava and os.environ.get("CAR_STILL") != "1") else 0
    fdir = f"/tmp/carframes/{cid}"
    if FRAMES:
        subprocess.run(["rm", "-rf", fdir]); os.makedirs(fdir)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch({{args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl']}});const p=await b.newPage({{viewport:{{width:1080,height:1350}}}});
await p.goto('http://localhost:8779/tools/carousel/_{cid}.html');await p.waitForFunction(()=>document.body.dataset.ready==='1');
const lf=p.frames().find(f=>f.url().includes('lava.html'));if(lf){{await lf.waitForFunction(()=>window.READY===1,null,{{timeout:60000}});await lf.evaluate(()=>window.render(0))}}
for(let i=1;i<={n};i++){{await (await p.$('#s'+i)).screenshot({{path:'{out}/'+String(i).padStart(2,'0')+'.jpg',type:'jpeg',quality:88}})}}
if(lf&&{FRAMES}){{const s1=await p.$('#s1');for(let k=0;k<{FRAMES};k++){{await lf.evaluate(t=>window.render(t),k*8/{FRAMES});await s1.screenshot({{path:'{fdir}/'+String(k).padStart(4,'0')+'.jpg',type:'jpeg',quality:92}})}}}}
await b.close()}})();"""
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8779"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(0.8)
        subprocess.run(["node", "-e", js], check=True, cwd="/tmp")
    finally:
        srv.terminate()
    if FRAMES:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", f"{fdir}/%04d.jpg", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", os.path.join(out, "cover.mp4")], check=True)
        # 3 loops = 24s so IG plays it long enough to read
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "2", "-i", os.path.join(out, "cover.mp4"), "-c", "copy", os.path.join(out, "cover_ig.mp4")], check=True)
        print(f"animated cover: docs/media/car/{cid}/cover.mp4")
    print(f"carousel ready: docs/media/car/{cid}/ ({n} slides)")
    return n


if __name__ == "__main__":
    build(sys.argv[1])
