"""AUTOPILOT.OI GRID v2: one design system for every Instagram cover (carousels and reel thumbnails).

Seb, Nov 4 2026: "the profile grid need to look like one ... like something built with a crazy design team",
with streetwear template references (neon on black, white, torn paper, outline repeats, round text badges,
vertical type, tickers). Our brand only: ink #0b0b0b, paper #ecece7 / #f2f2ee, lime #D4FF3A; Anton, Inter,
Chakra Petch, JetBrains Mono. No photos of people.

THE GRID RULES
1. Three themes rotate so no two neighbours in the 3 wide profile grid ever match: for the k-th IG post (counted
   in publish order), theme = THEMES[(k + k // 3) % 3]  (lime, black, paper). See theme_for().
2. Every cover shares the same frame: a top bar (AUTOPILOT.OI, category tag, issue number) with a full bleed rule at
   y=112, and a full bleed ticker band at y=1176 to 1236. They line up across the whole row on the profile, so the
   grid reads as one piece.
3. One giant idea per cover: Anton type fitted to 968 px, one KEY line treated (block or outline repeats), plus at
   most one sticker (round spinning badge, stamp or stripes).
4. Never blank: every element is visible in frame 0 and every frame after; motion = spin, ticker scroll, settle,
   pulse (tools/carousel/anim.js).

Spec p["grid2"]:
  {"k": 4 (or "theme": "lime|black|paper"), "layout": "stack|side|split", "tag": "PROMPTS", "no": 7,
   "lines": ["Claude prompts", "that should be", "illegal"], "key": 2,
   "ring": "NO DM NEEDED * ALL 24 INSIDE *", "ring_center": "24",
   "vertical": "PROMPTS" (side layout), "sub": "Copy. Paste. Swap the *[brackets]*.",
   "ticker": "COPY * PASTE * SWAP THE BRACKETS", "button": "SAVE IT · SWIPE ▸"}
"""
import html
import random
import re

E = html.escape
INK, PAPER, LIME, WHITE = "#0b0b0b", "#ecece7", "#D4FF3A", "#f2f2ee"
THEMES = ["lime", "black", "paper"]
T = {  # bg, main type, key fill, key text, accent, band bg, band text, muted
    "lime": dict(bg=LIME, fg=INK, kb=INK, kt=LIME, ac=INK, band=INK, bt=LIME, mu="#0b0b0bb0", cls="bg-lime"),
    "black": dict(bg=INK, fg=WHITE, kb=LIME, kt=INK, ac=LIME, band=LIME, bt=INK, mu="#f2f2eeb0", cls="bg-black"),
    "paper": dict(bg=PAPER, fg=INK, kb=LIME, kt=INK, ac=INK, band=INK, bt=LIME, mu="#5d5d56", cls="bg-white"),
}


def theme_for(k):
    return THEMES[(k + k // 3) % 3]


def star(s):
    return E(s).replace("*", "✱")


def lime_marks(s, t):
    return re.sub(r"\*(.+?)\*", rf'<span style="background:{t["kb"]};color:{t["kt"]};padding:0 6px">\1</span>', E(s))


def frame(g, t):
    """Top bar + full bleed rule + ticker band. Decorative (not QA text) except the bar labels."""
    no = f'NO. {int(g.get("no", 1)):03d}'
    bar = (f'<div class="fx Cc" style="left:56px;top:58px;font-size:22px;letter-spacing:5px;color:{t["fg"]}">AUTOPILOT.OI</div>'
           f'<div class="fx Cc" style="left:540px;top:52px;transform:translateX(-50%);font-size:20px;letter-spacing:4px;'
           f'background:{t["band"]};color:{t["bt"]};padding:9px 16px 7px;border-radius:4px;white-space:nowrap">{E(g.get("tag", "PROMPTS"))}</div>'
           f'<div class="fx Cc" style="left:772px;top:58px;font-size:22px;letter-spacing:4px;color:{t["fg"]}" data-free="1">{no}</div>'
           f'<div style="position:absolute;left:0;right:0;top:112px;height:3px;background:{t["fg"]};opacity:.9"></div>')
    tick = star(g.get("ticker", "SAVE THIS * AUTOPILOT.OI")) + " ✱ "
    run = (tick * 12)
    band = (f'<div style="position:absolute;left:0;right:0;top:1176px;height:60px;background:{t["band"]};overflow:hidden">'
            f'<div data-scroll="70" style="position:absolute;left:0;top:9px;white-space:nowrap;font:400 40px/1 A;'
            f'letter-spacing:2px;color:{t["bt"]};text-transform:uppercase">{run}</div></div>')
    return bar + band


def ring(g, t, x, y, size=250, after=None):
    txt = star(g["ring"]).strip() + " "
    c = size / 2
    r = c - 26
    circ = 2 * 3.1416 * r
    reps = max(1, int(circ / 19 // len(txt)))
    txt = txt * reps
    fs = max(16, min(25, circ / (len(txt) * 0.95)))
    center = E(g.get("ring_center", ""))
    aft = f' data-after="{after}" data-gap="-70"' if after else ""
    return (f'<div{aft} style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:6;transform:rotate(-8deg)">'
            f'<div style="position:absolute;inset:0;border-radius:50%;background:{t["band"]}"></div>'
            f'<svg data-spin="-28" width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="position:absolute;inset:0">'
            f'<defs><path id="rg" d="M {c},{c} m -{r},0 a {r},{r} 0 1,1 {2 * r},0 a {r},{r} 0 1,1 -{2 * r},0"/></defs>'
            f'<text font-family="C" font-weight="700" font-size="{fs:.1f}" letter-spacing="3" fill="{t["bt"]}">'
            f'<textPath href="#rg" textLength="{2 * 3.1416 * r - 8:.0f}">{txt}</textPath></text></svg>'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
            f'font:400 {int(size * .42)}px/1 A;color:{t["bt"]};padding-top:6px">{center}</div></div>')


def torn(t, y, color, seed=3, up=False):
    r = random.Random(seed)
    pts, x = [], 0
    while x < 1080:
        pts.append(f"{x},{r.randint(0, 34)}")
        x += r.randint(18, 46)
    pts.append("1080,10")
    poly = " ".join(pts)
    return (f'<svg style="position:absolute;left:0;top:{y}px" width="1080" height="1400" viewBox="0 0 1080 1400">'
            f'<polygon points="0,1400 {poly} 1080,1400" fill="{color}"/></svg>')


def stripes(x, y, w, h, color, n=7):
    s = "".join(f'<line x1="{i * w / n * 1.6 - w * .3:.0f}" y1="{h}" x2="{i * w / n * 1.6 - w * .3 + h * .6:.0f}" y2="0" '
                f'stroke="{color}" stroke-width="{w / n * .45:.0f}"/>' for i in range(n + 3))
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<clipPath id="sc{x}{y}"><rect width="{w}" height="{h}"/></clipPath><g clip-path="url(#sc{x}{y})">{s}</g></svg>')


def head_lines(g, t, top=150, left=56, width=968, size=160, key_style="block"):
    out = ""
    for i, ln in enumerate(g["lines"]):
        key = i == g.get("key", len(g["lines"]) - 1)
        st = ""
        if key and key_style == "block":
            st = f"background:{t['kb']};color:{t['kt']};padding:14px 22px 0;box-sizing:border-box;"
        gap = ' data-gap="18"' if i == 0 else ""
        w = int(min(width, width * max(len(ln), 4) / 7.5))   # short lines stay short instead of turning giant
        out += (f'<div class="fx A" data-fit="{w}" data-stack="h"{gap} style="left:{left}px;top:{top + i * 170}px;'
                f'font-size:{size}px;white-space:nowrap;color:{t["fg"]};{st}">{E(ln)}</div>')
    return out


def echo(word, t, top, size=170):
    """Outline repeats of the key word behind the headline (the SALE SALE SALE move), decorative."""
    rows = "".join(f'<div style="white-space:nowrap">{E(word)} {E(word)}</div>' for _ in range(3))
    return (f'<div data-scroll="-40" style="position:absolute;left:-40px;top:{top}px;font:400 {size}px/.86 A;'
            f'text-transform:uppercase;color:transparent;-webkit-text-stroke:3px {t["fg"]};opacity:.14">{rows}</div>')


def bottom(g, t, after="h", gap=60):
    sub = lime_marks(g.get("sub", ""), t)
    sub = f'<div style="font:800 44px/1.18 I;letter-spacing:-.8px;color:{t["fg"]};text-wrap:balance">{sub}</div>' if sub else ""
    btn = (f'<div style="font:700 24px C;letter-spacing:3px;color:{t["kt"]};background:{t["kb"]};'
           f'padding:16px 26px 14px;border-radius:6px">{E(g.get("button", "SAVE IT · SWIPE ▸"))}</div>')
    return (f'<div class="fx" data-after="{after}" data-gap="{gap}" style="left:56px;top:900px;width:690px;display:flex;'
            f'flex-direction:column;align-items:flex-start;gap:44px">{sub}{btn}</div>')


def render(g):
    """-> (cover_html, cover_bg class)"""
    th = g.get("theme") or theme_for(int(g.get("k", 0)))
    t = T[th]
    lay = g.get("layout", "stack")
    key_word = g["lines"][g.get("key", len(g["lines"]) - 1)]
    out = frame(g, t)
    if lay == "stack":
        # echo behind, headline stack, ring badge overlapping the key line, sub + button
        out = echo(key_word, t, 640) + out + head_lines(g, t)
        if g.get("ring"):
            out += ring(g, t, 772, 700, 270, after="h")
        out += bottom(g, t, gap=70)
    elif lay == "side":
        # giant vertical word on a band at the left, headline and stripes on the right
        v = E(g.get("vertical", g.get("tag", "PROMPTS")))
        out += (f'<div style="position:absolute;left:0;top:115px;width:250px;height:1061px;background:{t["band"]}"></div>'
                f'<div style="position:absolute;left:125px;top:645px;transform:translate(-50%,-50%) rotate(-90deg);'
                f'font:400 230px/1 A;color:{t["bt"]};white-space:nowrap;text-transform:uppercase">{v}</div>')
        out += head_lines(g, t, top=170, left=300, width=724, size=130)
        out += stripes(300, 900, 300, 230, t["fg"])
        if g.get("ring"):
            out += ring(g, t, 680, 880, 260)
        sub = lime_marks(g.get("sub", ""), t)
        if sub:
            out += (f'<div class="fx" data-after="h" data-gap="44" style="left:300px;top:700px;width:724px;'
                    f'font:800 36px/1.22 I;letter-spacing:-.5px;color:{t["fg"]}">{sub}</div>')
    elif lay == "split":
        # headline on top, torn edge, second color zone with sub and button
        other = T["black" if th != "black" else "lime"]
        out = out + head_lines(g, t, top=150)
        out += torn(t, 760, other["bg"], seed=int(g.get("no", 3)))
        tz = dict(other)
        sub = lime_marks(g.get("sub", ""), tz)
        out += (f'<div class="fx" style="left:56px;top:850px;width:968px;display:flex;flex-direction:column;'
                f'align-items:center;gap:36px"><div style="font:800 40px/1.2 I;letter-spacing:-.5px;color:{tz["fg"]};'
                f'text-align:center">{sub}</div><div style="font:700 24px C;letter-spacing:3px;color:{tz["kt"]};'
                f'background:{tz["kb"]};padding:16px 26px 14px;border-radius:6px">{E(g.get("button", "SWIPE ▸"))}</div></div>')
        if g.get("ring"):
            out += ring(g, t, 800, 640, 230)
    return out, t["cls"]
