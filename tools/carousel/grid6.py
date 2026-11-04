"""AUTOPILOT.OI GRID v6 "Street editorial": black and white photos + big type + one lime accent.

Seb, Nov 4 2026: references = streetwear template feeds (B&W photos, torn paper, neon, big type); he approved
"B&W stock people" (Pexels, generic people, never a named real person; credits kept in credits.json).

Three layouts rotate by post order (k % 3), and each layout owns its base colour, so neighbours never match:
  poster  full bleed B&W photo, torn LIME paper across the bottom with the headline in ink
  frame   INK tile, B&W photo in a tall frame on the right, giant paper headline overlapping it
  cutout  PAPER tile, the person cut out in B&W on the right over a torn lime shape, headline on the left
Same small frame on every tile: AUTOPILOT.OI top left, Nº top right, AUTOPILOTOI.APP running up the right edge.
One idea, one photo, one accent. Motion (anim.js): the photo slowly pushes in, the headline settles; never blank.

Spec p["grid6"]: {"k": 0, "no": 31, "lines": [...], "mark": "word", "sub": "...", "kicker": "...",
                  "photo": "g6-k0/02"  (docs/media/car/photos/<this>.jpg and _cut.png), "layout": optional override}
"""
import html
import random

E = html.escape
INK, PAPER, LIME, WHITE = "#0b0b0b", "#ecece7", "#D4FF3A", "#f2f2ee"
M = 72
LAYOUTS = ["poster", "frame", "cutout"]
BW = "filter:grayscale(1) contrast(1.28) brightness(.96)"


def torn_path(w, y0, amp, seed, top=True):
    r = random.Random(seed)
    pts, x = [], 0
    while x < w:
        pts.append(f"{x},{y0 + r.randint(-amp, amp)}")
        x += r.randint(14, 38)
    pts.append(f"{w},{y0}")
    return " ".join(pts)


def torn_panel(y, color, seed, h=1350):
    edge = torn_path(1080, 30, 22, seed)
    return (f'<svg style="position:absolute;left:0;top:{y}px" width="1080" height="{h}" viewBox="0 0 1080 {h}">'
            f'<polygon points="0,{h} {edge} 1080,{h}" fill="{color}"/>'
            f'<polyline points="{edge}" fill="none" stroke="{WHITE}" stroke-width="6" opacity=".9"/></svg>')


def marked(ln, mark, bg, fg, outline=None):
    out = []
    for w in ln.split(" "):
        if mark and w.strip(".,?!:").lower() == mark.lower():
            if outline:
                out.append(f'<span style="color:transparent;-webkit-text-stroke:3px {outline}">{E(w)}</span>')
            else:
                out.append(f'<span style="background:{bg};color:{fg};padding:6px 12px 0;display:inline-block;line-height:.86">{E(w)}</span>')
        else:
            out.append(E(w))
    return " ".join(out)


def chrome(g, fg, band=None):
    no = f'Nº {int(g.get("no", 1)):03d}'
    side = (f'<div style="position:absolute;right:30px;top:675px;transform:translate(50%,-50%) rotate(90deg) translateY(-50%);'
            f'font:700 18px C;letter-spacing:8px;color:{band or fg};white-space:nowrap;z-index:6">AUTOPILOTOI.APP · {E((g.get("kicker") or "").upper())}</div>')
    return (f'<div class="fx Cc" style="left:{M}px;top:64px;font-size:20px;letter-spacing:6px;color:{fg};z-index:6">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:780px;top:64px;width:150px;text-align:right;font:400 20px M;letter-spacing:2px;color:{fg};z-index:6" '
            f'data-free="1">{no}</div>' + side)


def head(g, x, top, width, size, fg, mk_bg, mk_fg, outline=None, align="left"):
    out = ""
    for i, ln in enumerate(g["lines"]):
        out += (f'<div class="fx A" data-stack="h"{" data-gap=\"6\"" if i == 0 else ""} style="left:{x}px;top:{top + i * size}px;'
                f'font-size:{size}px;line-height:.9;white-space:nowrap;color:{fg};z-index:5;text-align:{align}">'
                f'{marked(ln, g.get("mark"), mk_bg, mk_fg, outline)}</div>')
    return out


def size_for(g, width, cap):
    longest = max(len(l) for l in g["lines"])
    return int(min(cap, width / (longest * 0.47)))


def render(g):
    lay = g.get("layout") or LAYOUTS[int(g.get("k", 0)) % 3]
    src = f'/docs/media/car/photos/{g["photo"]}'
    seed = int(g.get("no", 3))
    sub = E(g.get("sub", ""))
    if lay == "poster":
        out = (f'<div data-push="1" style="position:absolute;inset:0;background:url(\'{src}.jpg\') center 30%/cover;{BW}"></div>'
               f'<div style="position:absolute;inset:0;background:linear-gradient(#0b0b0b88,#0b0b0b00 30%)"></div>')
        out += torn_panel(760, LIME, seed, 620)
        out += chrome(g, WHITE, INK)
        size = size_for(g, 900, 120)
        out += head(g, M, 840, 900, size, INK, INK, LIME)
        if sub:
            out += (f'<div class="fx" data-after="h" data-gap="26" style="left:{M}px;top:1200px;width:860px;font:700 30px/1.25 I;'
                    f'color:{INK};z-index:5">{sub}</div>')
        return out, "bg-black"
    if lay == "frame":
        out = (f'<div style="position:absolute;left:430px;top:150px;width:580px;height:1050px;overflow:hidden;z-index:1">'
               f'<div data-push="1" style="position:absolute;inset:0;background:url(\'{src}.jpg\') center/cover;{BW}"></div></div>'
               f'<div style="position:absolute;left:410px;top:130px;width:580px;height:1050px;border:3px solid {LIME};z-index:2"></div>')
        out += chrome(g, WHITE, LIME)
        size = size_for(g, 900, 132)
        out += head(g, M, 380, 900, size, WHITE, LIME, INK)
        if sub:
            out += (f'<div class="fx" data-after="h" data-gap="30" style="left:{M}px;top:900px;width:520px;font:600 30px/1.3 I;'
                    f'color:{WHITE};z-index:5;background:{INK};padding:14px 18px;box-sizing:border-box">{sub}</div>')
        return out, "bg-black"
    # cutout
    out = (f'<svg style="position:absolute;left:330px;top:300px" width="760" height="1060" viewBox="0 0 760 1060">'
           f'<polygon points="80,40 {torn_path(760, 40, 18, seed)} 760,1060 0,1060" fill="{LIME}"/></svg>'
           f'<img data-push="1" src="{src}_cut.png" style="position:absolute;right:-20px;bottom:0;height:1080px;max-width:820px;'
           f'object-fit:contain;object-position:bottom right;{BW};z-index:2">')
    out += chrome(g, INK, INK)
    size = size_for(g, 760, 124)
    out += head(g, M, 300, 760, size, INK, INK, LIME)
    if sub:
        out += (f'<div class="fx" data-after="h" data-gap="30" style="left:{M}px;top:900px;width:430px;font:700 30px/1.28 I;'
                f'color:{INK};z-index:5;background:{PAPER};padding:12px 16px;box-sizing:border-box">{sub}</div>')
    return out, "bg-white"
