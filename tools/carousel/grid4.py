"""AUTOPILOT.OI GRID v4 "THE LINE": every Instagram cover is a stop on one connected line.

Seb, Nov 4 2026: "make all grids connect in a dynamic way to make it wow factor" (after "simple ... upscale ... an
AI hub that teaches people and has a cool store").

Why it always connects: Instagram shifts every tile one place when a new post goes up, so a normal puzzle feed
breaks. Here every tile has the SAME four ports, so any tile lines up with any neighbour:
  left port  (x=0,    y=1060)  -> right port (x=1080, y=1060)   horizontal line
  top port   (x=990,  y=0)     -> bottom port (x=990, y=1350)    vertical line
  station (junction) at (990, 1060)
Inside a tile the line can bend (each layout routes it differently), but it always enters and leaves at the
ports. On the profile the whole grid becomes one metro map: lessons, store and news are stops on the same line.
Profile crop is 3:4 (x 34 to 1046), so ports sit inside it.

Colours: line = lime with an ink outline (reads on paper, ink and lime tiles). Tiles: lesson = paper, store = ink,
news = lime (same as v3). Motion: light pulses travel the line (same speed on every tile), the headline settles,
the product floats. Frame 0 is the finished cover.

Spec p["grid4"] = grid v3 spec ("type", "no", "lines", "mark", "sub", "kicker", "product", "product_sub", "price").
"""
import html

import grid3

E = html.escape
INK, PAPER, LIME, WHITE = grid3.INK, grid3.PAPER, grid3.LIME, grid3.WHITE
PX, PY = 945, 1060          # station


def line_svg(kind, t, no=0):
    # horizontal route differs per tile type, ports fixed
    if kind == "store":       # dips under the product card
        h = f"M -20 {PY} L 120 {PY} C 200 {PY} 200 1140 280 1140 L 760 1140 C 840 1140 840 {PY} 920 {PY} L 1100 {PY}"
    elif kind == "news":      # sharp signal zigzag
        h = f"M -20 {PY} L 520 {PY} L 580 1000 L 640 1120 L 700 {PY} L 1100 {PY}"
    else:                     # lesson: one clean loop, its place moves from post to post
        x = 200 + ((no * 7) % 5) * 110
        h = (f"M -20 {PY} L {x} {PY} C {x + 80} {PY} {x + 120} 1000 {x + 120} 960 C {x + 120} 900 {x + 40} 900 {x + 40} 960 "
             f"C {x + 40} 1010 {x + 100} {PY} {x + 180} {PY} L 1100 {PY}")
    v = f"M {PX} -20 L {PX} 1370"
    ink = INK if kind != "store" else "#000"
    out = ""
    for d in (v, h):
        out += (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="40" stroke-linejoin="round" stroke-linecap="butt"/>'
                f'<path d="{d}" fill="none" stroke="{LIME}" stroke-width="30" stroke-linejoin="round" stroke-linecap="butt"/>'
                f'<path data-dash="260" d="{d}" fill="none" stroke="{WHITE}" stroke-opacity=".9" stroke-width="8" '
                f'stroke-linecap="round" stroke-dasharray="26 234"/>')
    st = (f'<circle cx="{PX}" cy="{PY}" r="44" fill="{INK}"/><circle cx="{PX}" cy="{PY}" r="33" fill="{WHITE}"/>'
          f'<circle cx="{PX}" cy="{PY}" r="17" fill="{INK}"/>')
    return f'<svg style="position:absolute;left:0;top:0;z-index:3" width="1080" height="1350" viewBox="0 0 1080 1350">{out}{st}</svg>'


def render(g):
    t = grid3.T[g["type"]]
    M = grid3.M
    no = f'Nº {int(g.get("no", 1)):03d}'
    kick = g.get("kicker") or {"lesson": "LESSON", "store": "THE STORE", "news": "AI NEWS"}[g["type"]]
    act = (g.get("action") or "").replace("\u2192", "").strip() or {"lesson": "SWIPE", "store": "WATCH", "news": "SWIPE"}[g["type"]]
    out = line_svg(g["type"], t, int(g.get("no", 0)))
    out += (f'<div class="fx Cc" style="left:{M}px;top:80px;font-size:20px;letter-spacing:6px;color:{t["fg"]}">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:660px;top:80px;width:220px;text-align:right;font:400 20px M;letter-spacing:2px;'
            f'color:{t["fg"]}" data-free="1">{no}</div>'
            f'<div style="position:absolute;left:{M}px;top:132px;width:792px;height:2px;background:{t["rule"]}"></div>'
            # station label, under the line on the left, like a metro stop sign
            f'<div class="fx Mm" style="left:{M}px;top:1180px;font:400 20px M;letter-spacing:3px;color:{t["mu"]}">'
            f'{E(kick.upper())}</div>'
            f'<div class="fx Cc" style="left:{M}px;top:1222px;font-size:22px;letter-spacing:4px;background:{INK};color:{LIME};'
            f'padding:10px 16px 8px;border-radius:4px">{E(no)} · {E(act)} →</div>')
    longest = max(len(l) for l in g["lines"])
    if g["type"] == "store":
        out += (f'<div data-float="1" style="position:absolute;left:240px;top:560px;width:520px;height:440px;z-index:4;'
                f'transform:rotate(-5deg)">'
                f'<div style="position:absolute;inset:0;border-radius:20px;background:{PAPER};box-shadow:0 50px 80px #000b,0 0 0 1px #fff2"></div>'
                f'<div style="position:absolute;left:0;top:0;bottom:0;width:24px;border-radius:20px 0 0 20px;background:{LIME}"></div>'
                f'<div style="position:absolute;left:64px;top:54px;font:400 17px M;letter-spacing:3px;color:#6b6b63">AUTOPILOT.OI · STORE</div>'
                f'<div style="position:absolute;left:64px;top:130px;width:420px;font:400 86px/.9 A;text-transform:uppercase;color:{INK}">'
                f'{E(g["product"])}</div>'
                f'<div style="position:absolute;left:64px;bottom:54px;font:600 24px I;color:#3a3a35">{E(g.get("product_sub", ""))}</div>'
                f'<div style="position:absolute;right:-30px;top:-36px;width:140px;height:140px;border-radius:50%;background:{LIME};'
                f'border:4px solid {INK};display:flex;align-items:center;justify-content:center;font:400 52px A;color:{INK};'
                f'transform:rotate(9deg)">{E(g["price"])}</div></div>')
        size = int(g.get("size") or min(108, 800 / (longest * 0.47)))
        out += grid3.headline(g, t, 190, size)
        if g.get("sub"):
            out += (f'<div class="fx" data-after="h" data-gap="26" style="left:{M}px;top:420px;width:820px;'
                    f'font:500 32px/1.25 I;letter-spacing:-.4px;color:{t["mu"]}">{E(g["sub"])}</div>')
    else:
        size = int(g.get("size") or min(150, 800 / (longest * 0.47)))
        sub_lines = -(-len(g.get("sub", "")) // 38) if g.get("sub") else 0
        h = len(g["lines"]) * size * 0.9 + (50 + sub_lines * 48 if sub_lines else 0)
        out += grid3.headline(g, t, int(560 - h / 2), size)
        if g.get("sub"):
            out += (f'<div class="fx" data-after="h" data-gap="50" style="left:{M}px;top:800px;width:800px;'
                    f'font:500 38px/1.25 I;letter-spacing:-.6px;color:{t["mu"]}">{E(g["sub"])}</div>')
    return out, t["cls"]
