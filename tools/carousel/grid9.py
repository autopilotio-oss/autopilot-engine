"""AUTOPILOT.OI GRID v9: photo + a designed graphic kit (Seb, Nov 4: v8 "too simple", v2 "too much clutter").
Each tile = one cinematic photo + 2 or 3 kit pieces, never more. Three compositions rotate by k so the grid looks
art directed, like the streetwear template references, in our colours (ink, paper, lime) and fonts.

  arch   ink tile, photo in an arch window on the right with a lime offset outline, giant vertical word on the left,
         spinning text badge on the arch corner, headline at the bottom
  tape   full bleed photo, a lime tape strip across it with the key word repeated, headline under it, X marks
  torn   photo on top, torn edge into lime, outline echo of the key word behind the headline, dot grid
Spec p["grid9"] = {"k", "no", "lines", "mark", "sub", "kicker", "photo", "pos", "badge": "NO DM NEEDED * ALL 24 INSIDE *",
                   "badge_center": "24", "vertical": "PROMPTS"}
"""
import html
import random

E = html.escape
INK, PAPER, LIME, WHITE = "#0b0b0b", "#ecece7", "#D4FF3A", "#f2f2ee"
CINE = "filter:saturate(.7) contrast(1.15) brightness(.9)"
M = 64
LAYOUTS = ["arch", "tape", "torn"]


def mk(ln, mark, bg, fg):
    out = []
    for w in ln.split(" "):
        if mark and w.strip(".,?!:").lower() == mark.lower():
            out.append(f'<span style="background:{bg};color:{fg};padding:6px 12px 0;display:inline-block;line-height:.86">{E(w)}</span>')
        else:
            out.append(E(w))
    return " ".join(out)


def head(g, x, top, size, fg, mbg, mfg, z=6):
    out = ""
    for i, ln in enumerate(g["lines"]):
        out += (f'<div class="fx A" data-stack="h"{" data-gap=\"4\"" if i == 0 else ""} style="left:{x}px;top:{int(top + i * size * .9)}px;'
                f'font-size:{size}px;line-height:.9;white-space:nowrap;color:{fg};z-index:{z}">{mk(ln, g.get("mark"), mbg, mfg)}</div>')
    return out


def fit(g, w, cap):
    return int(min(cap, w / (max(len(l) for l in g["lines"]) * .47)))


def bar(g, fg):
    return (f'<div class="fx Cc" style="left:{M}px;top:58px;font-size:19px;letter-spacing:6px;color:{fg};z-index:8">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:700px;top:58px;width:316px;text-align:right;font:400 18px M;letter-spacing:3px;'
            f'color:{fg};z-index:8" data-free="1">Nº {int(g.get("no", 1)):03d}</div>')


def badge(g, x, y, size, bg, fg):
    txt = (g.get("badge") or "AUTOPILOT.OI * SAVE THIS *").replace("*", "✱").strip() + " "
    c, r = size / 2, size / 2 - 22
    circ = 6.2832 * r
    txt = txt * max(1, int(circ / 18 // len(txt)))
    fs = max(15, min(22, circ / (len(txt) * .95)))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:7">'
            f'<div style="position:absolute;inset:0;border-radius:50%;background:{bg}"></div>'
            f'<svg data-spin="-24" width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="position:absolute;inset:0">'
            f'<defs><path id="b{x}{y}" d="M {c},{c} m -{r},0 a {r},{r} 0 1,1 {2 * r},0 a {r},{r} 0 1,1 -{2 * r},0"/></defs>'
            f'<text font-family="C" font-weight="700" font-size="{fs:.1f}" letter-spacing="3" fill="{fg}">'
            f'<textPath href="#b{x}{y}" textLength="{circ - 6:.0f}">{E(txt)}</textPath></text></svg>'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:400 {int(size * .38)}px/1 A;'
            f'color:{fg};padding-top:5px">{E(g.get("badge_center", "→"))}</div></div>')


def xmarks(x, y, color, n=3):
    return "".join(f'<div style="position:absolute;left:{x + i * 46}px;top:{y}px;font:400 46px/1 A;color:{color};z-index:7">✕</div>'
                   for i in range(n))


def dots(x, y, color, cols=6, rows=4):
    return "".join(f'<i style="position:absolute;left:{x + c * 22}px;top:{y + r * 22}px;width:7px;height:7px;border-radius:50%;'
                   f'background:{color};z-index:2"></i>' for r in range(rows) for c in range(cols))


def photo_bg(g, extra=""):
    return f"background:url('/docs/media/car/photos/{g['photo']}.jpg') {g.get('pos', 'center 35%')}/cover;{CINE};{extra}"


def arch(g):
    word = (g.get("vertical") or g.get("mark") or "AI").upper()
    vs = int(min(230, 860 / max(len(word), 3) * 1.6))
    out = (f'<div style="position:absolute;inset:0;background:{INK}"></div>'
           f'<div style="position:absolute;left:{M + 6}px;top:150px;width:{int(vs * .95)}px;height:760px;display:flex;align-items:center;justify-content:center;z-index:2">'
           f'<div style="transform:rotate(-90deg);font:400 {vs}px/1 A;color:{LIME};white-space:nowrap;text-transform:uppercase">{E(word)}</div></div>'
           f'<div style="position:absolute;left:418px;top:166px;width:560px;height:760px;border:4px solid {LIME};border-radius:280px 280px 0 0;z-index:1"></div>'
           f'<div style="position:absolute;left:440px;top:140px;width:560px;height:760px;border-radius:280px 280px 0 0;overflow:hidden;z-index:3">'
           f'<div data-push="1" style="position:absolute;inset:0;{photo_bg(g)}"></div></div>')
    out += badge(g, 830, 120, 210, LIME, INK)
    out += dots(440, 930, "#f2f2ee55")
    out += bar(g, WHITE)
    size = fit(g, 940, 104)
    out += head(g, M, 1000, size, WHITE, LIME, INK)
    return out, "bg-black"


def tape(g):
    word = (g.get("mark") or "AI").upper().strip(".")
    run = (f"{word} ✱ ") * 14
    out = (f'<div data-push="1" style="position:absolute;inset:0;{photo_bg(g)}"></div>'
           f'<div style="position:absolute;inset:0;background:linear-gradient(#0b0b0b66,#0b0b0b00 25%,#0b0b0b00 45%,#0b0b0bee 78%)"></div>'
           f'<div style="position:absolute;left:-120px;top:600px;width:1400px;height:96px;background:{LIME};transform:rotate(-7deg);'
           f'z-index:4;overflow:hidden;box-shadow:0 20px 40px #0006">'
           f'<div data-scroll="60" style="position:absolute;left:0;top:14px;white-space:nowrap;font:400 70px/1 A;color:{INK}">{E(run)}</div></div>')
    out += xmarks(860, 150, LIME)
    out += bar(g, WHITE)
    size = fit(g, 940, 112)
    out += head(g, M, 810, size, WHITE, LIME, INK)
    if g.get("sub"):
        out += (f'<div class="fx" data-after="h" data-gap="22" style="left:{M}px;top:1220px;width:900px;font:600 28px/1.25 I;'
                f'color:#e6e6e0;z-index:6">{E(g["sub"])}</div>')
    return out, "bg-black"


def torn(g):
    r = random.Random(int(g.get("no", 3)))
    pts, x = [], 0
    while x < 1080:
        pts.append(f"{x},{30 + r.randint(-22, 22)}"); x += r.randint(16, 40)
    pts.append("1080,30")
    word = (g.get("mark") or "AI").upper().strip(".")
    out = (f'<div data-push="1" style="position:absolute;left:0;top:0;width:1080px;height:800px;{photo_bg(g)}"></div>'
           f'<svg style="position:absolute;left:0;top:700px;z-index:3" width="1080" height="650" viewBox="0 0 1080 650">'
           f'<polygon points="0,650 {" ".join(pts)} 1080,650" fill="{LIME}"/></svg>'
           f'<div style="position:absolute;left:-30px;top:770px;font:400 300px/.85 A;color:transparent;-webkit-text-stroke:3px #0b0b0b26;'
           f'white-space:nowrap;z-index:4">{E(word)} {E(word)}</div>')
    out += dots(880, 1180, "#0b0b0b66", 5, 4)
    if g.get("badge"):
        out += badge(g, 820, 590, 190, INK, LIME)
    out += bar(g, WHITE)
    size = fit(g, 900, 112)
    out += head(g, M, 820, size, INK, INK, LIME)
    if g.get("sub"):
        out += (f'<div class="fx" data-after="h" data-gap="22" style="left:{M}px;top:1220px;width:760px;font:700 28px/1.25 I;'
                f'color:{INK};z-index:6">{E(g["sub"])}</div>')
    return out, "bg-lime"


def render(g):
    return {"arch": arch, "tape": tape, "torn": torn}[g.get("layout") or LAYOUTS[int(g.get("k", 0)) % 3]](g)
