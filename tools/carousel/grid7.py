"""AUTOPILOT.OI GRID v7: photo-led concepts with audited editorial B&W portraits (Seb, Nov 4: "images you use have to
be elite ... no basic things everything must be a hook").

Photo audit rule: only dramatic, editorial B&W portraits (hard light, strong gesture or silhouette, clean background).
No smiling office stock, no laptops on desks, no group shots, no logos. Kept in docs/media/car/photos/eN/.

Styles ("style"):
  magazine  full bleed portrait, fashion cover type: tiny label, giant headline at the bottom, one word in lime
  torn      portrait on top, torn edge, solid block (lime / ink / paper by k) holding the headline
  depth     solid lime or ink tile, giant headline BEHIND the cut out person (depth effect), small sub in front
Spec p["grid7"] = {"style", "k", "no", "lines", "mark", "sub", "kicker", "photo": "e9", "pos": "center 25%"}
"""
import html
import random

E = html.escape
INK, PAPER, LIME, WHITE = "#0b0b0b", "#ecece7", "#D4FF3A", "#f2f2ee"
BW = "filter:grayscale(1) contrast(1.18)"
M = 70


def mark_html(ln, mark, bg, fg):
    out = []
    for w in ln.split(" "):
        if mark and w.strip(".,?!:$").lower() == mark.strip("$").lower():
            out.append(f'<span style="background:{bg};color:{fg};padding:6px 12px 0;display:inline-block;line-height:.86">{E(w)}</span>')
        else:
            out.append(E(w))
    return " ".join(out)


def lines(g, x, top, size, fg, mbg, mfg, z=5, align="left", width=940):
    out = ""
    for i, ln in enumerate(g["lines"]):
        out += (f'<div class="fx A" data-stack="h"{" data-gap=\"4\"" if i == 0 else ""} style="left:{x}px;top:{int(top + i * size * .9)}px;'
                f'font-size:{size}px;line-height:.9;white-space:nowrap;color:{fg};z-index:{z}">{mark_html(ln, g.get("mark"), mbg, mfg)}</div>')
    return out


def fit(g, width, cap):
    return int(min(cap, width / (max(len(l) for l in g["lines"]) * 0.47)))


def top_bar(g, fg):
    return (f'<div class="fx Cc" style="left:{M}px;top:62px;font-size:19px;letter-spacing:6px;color:{fg};z-index:7">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:740px;top:62px;width:270px;text-align:right;font:400 19px M;letter-spacing:3px;'
            f'color:{fg};z-index:7" data-free="1">{E((g.get("kicker") or "").upper()[:22])}</div>')


def photo(g):
    return f'/docs/media/car/photos/{g["photo"]}'


def magazine(g):
    src = photo(g)
    size = fit(g, 940, 150)
    n = len(g["lines"])
    top = 1190 - n * size * .9 - (70 if g.get("sub") else 0)
    out = (f'<div data-push="1" style="position:absolute;inset:0;background:url(\'{src}.jpg\') {g.get("pos", "center 25%")}/cover;{BW}"></div>'
           f'<div style="position:absolute;inset:0;background:linear-gradient(#0b0b0b00 35%,#0b0b0bdd 82%)"></div>')
    out += top_bar(g, WHITE)
    out += lines(g, M, int(top), size, WHITE, LIME, INK)
    if g.get("sub"):
        out += (f'<div class="fx" data-after="h" data-gap="24" style="left:{M}px;top:1200px;width:900px;font:600 30px/1.25 I;'
                f'color:#e8e8e2;z-index:5">{E(g["sub"])}</div>')
    return out, "bg-black"


def torn_edge(seed, y, color, h):
    r = random.Random(seed)
    pts, x = [], 0
    while x < 1080:
        pts.append(f"{x},{30 + r.randint(-20, 20)}")
        x += r.randint(16, 40)
    pts.append("1080,30")
    p = " ".join(pts)
    return (f'<svg style="position:absolute;left:0;top:{y}px;z-index:3" width="1080" height="{h}" viewBox="0 0 1080 {h}">'
            f'<polygon points="0,{h} {p} 1080,{h}" fill="{color}"/></svg>')


def torn(g):
    k = int(g.get("k", 0))
    block, fg, mbg, mfg = [(LIME, INK, INK, LIME), (INK, WHITE, LIME, INK), (PAPER, INK, LIME, INK)][k % 3]
    src = photo(g)
    out = (f'<div data-push="1" style="position:absolute;left:0;top:0;width:1080px;height:860px;background:url(\'{src}.jpg\') '
           f'{g.get("pos", "center 25%")}/cover;{BW}"></div>')
    out += torn_edge(int(g.get("no", 3)), 760, block, 600)
    out += top_bar(g, WHITE)
    size = fit(g, 940, 116)
    out += lines(g, M, 850, size, fg, mbg, mfg)
    if g.get("sub"):
        out += (f'<div class="fx" data-after="h" data-gap="22" style="left:{M}px;top:1220px;width:900px;font:700 28px/1.25 I;'
                f'color:{fg};z-index:5;opacity:.85">{E(g["sub"])}</div>')
    return out, "bg-black"


def depth(g):
    k = int(g.get("k", 0))
    bg, fg = [(LIME, INK), (INK, LIME), (LIME, INK)][k % 3]
    src = photo(g)
    words = [w.rstrip(".,") for w in " ".join(g["lines"]).upper().split(" ")]
    # giant words behind the person, stacked, fitted to width
    big = ""
    rows, row = [], ""
    for w in words:
        if len(row) + len(w) + 1 <= 9 or not row:
            row = (row + " " + w).strip()
        else:
            rows.append(row); row = w
    rows.append(row)
    rows = rows[:4]
    size = int(min(300, 1000 / (max(len(r) for r in rows) * 0.46)))
    y = 150
    for r in rows:
        big += (f'<div style="position:absolute;left:{M - 6}px;top:{y}px;font:400 {size}px/.86 A;color:{fg};white-space:nowrap;'
                f'z-index:1">{E(r)}</div>')
        y += int(size * .88)
    out = (f'<div style="position:absolute;inset:0;background:{bg}"></div>{big}'
           f'<img data-push="1" src="{src}_cut.png" style="position:absolute;left:{g.get("cut_x", 330)}px;bottom:0;'
           f'height:{g.get("cut_h", 900)}px;width:760px;object-fit:contain;object-position:bottom right;{BW};z-index:2">')
    out += top_bar(g, fg)
    if g.get("sub"):
        out += (f'<div class="fx" style="left:{M}px;top:1190px;max-width:620px;font:800 30px/1.2 I;color:{INK if bg == LIME else INK};'
                f'background:{WHITE if bg == LIME else LIME};padding:14px 18px;z-index:5">{E(g["sub"])}</div>')
    return out, "bg-lime" if bg == LIME else "bg-black"


STYLES = {"magazine": magazine, "torn": torn, "depth": depth}


def render(g):
    return STYLES[g.get("style", "magazine")](g)
