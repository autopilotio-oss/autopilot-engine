"""AUTOPILOT.OI GRID v3 "Editorial": the one cover system for every Instagram post (carousels and reel thumbnails).

Seb, Nov 4 2026: "too much clutter ... unique and simple ... look upscale ... an AI hub that teaches people and has
a cool store with items for sale". So: lots of space, one idea per tile, the same frame on every tile, and three
tile types that tell people what we are at a glance:

  LESSON  paper #ecece7, ink type       prompts, how tos, stories (the hub teaches)
  STORE   ink #0b0b0b, paper type       a product object with its real price (the store sells)
  NEWS    lime #D4FF3A, ink type        verified AI news (the hub reports)

Frame (identical on every tile so the profile reads as one magazine): AUTOPILOT.OI top left, issue number top right,
hairline at y=132, hairline at y=1196, a small kicker bottom left and the action bottom right. 88 px margins.
Headline: Anton, left aligned, ragged, 3 lines max, ONE word on a lime marker (on lime tiles the marker is ink).
No echoes, stripes, tickers or badges. Motion is quiet and never blank: the headline settles, the marker wipes,
the product floats, the lava drifts underneath.

Spec p["grid3"]:
  {"type": "lesson|store|news", "no": 38, "lines": ["Claude prompts", "that should", "be illegal."],
   "mark": "illegal" (word to put on the marker), "sub": "24 prompts for business owners. All inside.",
   "kicker": "PROMPTS", "action": "SWIPE", "size": 150,
   store only: "product": "Front Desk Kit", "product_sub": "Claude agent kit", "price": "$39"}
"""
import html

E = html.escape
INK, PAPER, LIME, WHITE = "#0b0b0b", "#ecece7", "#D4FF3A", "#f2f2ee"
T = {
    "lesson": dict(bg=PAPER, fg=INK, mu="#6b6b63", rule="#0b0b0b33", mk=LIME, mt=INK, cls="bg-white"),
    "store": dict(bg=INK, fg=WHITE, mu="#a9a9a1", rule="#f2f2ee33", mk=LIME, mt=INK, cls="bg-black"),
    "news": dict(bg=LIME, fg=INK, mu="#0b0b0b99", rule="#0b0b0b40", mk=INK, mt=LIME, cls="bg-lime"),
}
M = 88


def frame(g, t):
    no = f'Nº {int(g.get("no", 1)):03d}'
    act = {"lesson": "SWIPE →", "store": "WATCH →", "news": "SWIPE →"}[g["type"]]
    kick = g.get("kicker") or {"lesson": "LESSON", "store": "THE STORE", "news": "AI NEWS"}[g["type"]]
    return (f'<div class="fx Cc" style="left:{M}px;top:80px;font-size:20px;letter-spacing:6px;color:{t["fg"]}">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:860px;top:80px;font:400 20px M;letter-spacing:2px;color:{t["fg"]}">{no}</div>'
            f'<div style="position:absolute;left:{M}px;right:{M}px;top:132px;height:2px;background:{t["rule"]}"></div>'
            f'<div style="position:absolute;left:{M}px;right:{M}px;top:1196px;height:2px;background:{t["rule"]}"></div>'
            f'<div class="fx Mm" style="left:{M}px;top:1226px;font:400 20px M;letter-spacing:3px;color:{t["mu"]}">{E(kick.upper())}</div>'
            f'<div class="fx Mm" style="left:{1080 - M - 160}px;top:1226px;width:160px;text-align:right;font:400 20px M;'
            f'letter-spacing:3px;color:{t["fg"]}" data-free="1">{E(g.get("action", act))}</div>')


def headline(g, t, top, size):
    mark = (g.get("mark") or "").lower()
    out = ""
    for i, ln in enumerate(g["lines"]):
        words = []
        for w in ln.split(" "):
            bare = w.strip(".,?!:").lower()
            if mark and bare == mark:
                words.append(f'<span class="mk" style="background:{t["mk"]};color:{t["mt"]};padding:6px 14px 0;'
                             f'margin:0 -4px;display:inline-block;line-height:.86">{E(w)}</span>')
            else:
                words.append(E(w))
        gap = ' data-gap="10"' if i == 0 else ""
        out += (f'<div class="fx A" data-stack="h"{gap} style="left:{M}px;top:{top + i * size}px;font-size:{size}px;'
                f'line-height:.9;white-space:nowrap;color:{t["fg"]}">{" ".join(words)}</div>')
    return out


def render(g):
    t = T[g["type"]]
    out = frame(g, t)
    longest = max(len(l) for l in g["lines"])
    size = int(g.get("size") or min(150, 896 / (longest * 0.47)))
    if g["type"] == "store":
        # product object: a premium kit card floating at an angle, real price on a lime tag
        out += (f'<div data-float="1" style="position:absolute;left:262px;top:640px;width:560px;height:500px;'
                f'transform:rotate(-5deg)">'
                f'<div style="position:absolute;inset:0;border-radius:22px;background:{PAPER};box-shadow:0 60px 90px #000a,0 0 0 1px #fff2"></div>'
                f'<div style="position:absolute;left:0;top:0;bottom:0;width:26px;border-radius:22px 0 0 22px;background:{LIME}"></div>'
                f'<div style="position:absolute;left:70px;top:60px;font:400 18px M;letter-spacing:3px;color:#6b6b63">AUTOPILOT.OI</div>'
                f'<div style="position:absolute;left:70px;top:150px;width:460px;font:400 92px/.9 A;text-transform:uppercase;color:{INK}">'
                f'{E(g["product"])}</div>'
                f'<div style="position:absolute;left:70px;bottom:64px;font:600 26px I;color:#3a3a35">{E(g.get("product_sub", ""))}</div>'
                f'<div style="position:absolute;right:-34px;top:-40px;width:150px;height:150px;border-radius:50%;background:{LIME};'
                f'display:flex;align-items:center;justify-content:center;font:400 56px A;color:{INK};transform:rotate(9deg);'
                f'box-shadow:0 18px 40px #0007">{E(g["price"])}</div></div>')
        out += headline(g, t, 196, int(g.get("size") or min(110, 896 / (longest * 0.47))))
        if g.get("sub"):
            out += (f'<div class="fx" data-after="h" data-gap="28" style="left:{M}px;top:420px;width:904px;'
                    f'font:500 34px/1.25 I;letter-spacing:-.4px;color:{t["mu"]}">{E(g["sub"])}</div>')
    else:
        sub_lines = -(-len(g.get("sub", "")) // 40) if g.get("sub") else 0
        h = len(g["lines"]) * size * 0.9 + (54 + sub_lines * 48 if sub_lines else 0)
        out += headline(g, t, int(664 - h / 2), size)
        if g.get("sub"):
            out += (f'<div class="fx" data-after="h" data-gap="54" style="left:{M}px;top:900px;width:860px;'
                    f'font:500 38px/1.25 I;letter-spacing:-.6px;color:{t["mu"]}">{E(g["sub"])}</div>')
    return out, t["cls"]
