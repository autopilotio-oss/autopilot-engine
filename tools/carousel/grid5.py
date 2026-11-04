"""Four alternative cover concepts for the Instagram grid (Seb, Nov 4: "make more that are completely different").
Same content spec as grid v3/v4 ("type", "no", "lines", "mark", "sub", "kicker", "product", "product_sub", "price");
pick the concept with "style": index | lava | chat | vertical.
"""
import html

import grid3

E = html.escape
INK, PAPER, LIME, WHITE = grid3.INK, grid3.PAPER, grid3.LIME, grid3.WHITE
M = 88


def joined(g):
    return " ".join(g["lines"])


def marked(text, mark, bg, fg):
    out = []
    for w in text.split(" "):
        if mark and w.strip(".,?!:").lower() == mark.lower():
            out.append(f'<span style="background:{bg};color:{fg};padding:5px 10px 0;display:inline-block;line-height:.88">{E(w)}</span>')
        else:
            out.append(E(w))
    return " ".join(out)


def tag(g):
    return g.get("kicker") or {"lesson": "LESSON", "store": "THE STORE", "news": "AI NEWS"}[g["type"]]


# 1. INDEX: Swiss editorial. Giant outlined issue number, small sharp headline, lots of air.
def index(g):
    t = grid3.T[g["type"]]
    no = f'{int(g.get("no", 1)):03d}'
    longest = max(len(l) for l in g["lines"])
    size = int(min(104, 880 / (longest * .47)))
    out = (f'<div style="position:absolute;right:-40px;top:40px;font:400 560px/.82 A;color:transparent;'
           f'-webkit-text-stroke:3px {t["fg"]};opacity:.9;letter-spacing:-10px">{no}</div>'
           f'<div class="fx Cc" style="left:{M}px;top:80px;font-size:20px;letter-spacing:6px;color:{t["fg"]}">AUTOPILOT.OI</div>'
           f'<div class="fx Mm" style="left:{M}px;top:116px;font:400 18px M;letter-spacing:3px;color:{t["mu"]}">{E(tag(g).upper())}</div>')
    top = 1210 - len(g["lines"]) * size * .9 - 150
    for i, ln in enumerate(g["lines"]):
        out += (f'<div class="fx A" data-stack="h"{" data-gap=\"8\"" if i == 0 else ""} style="left:{M}px;top:{int(top + i * size)}px;'
                f'font-size:{size}px;line-height:.9;white-space:nowrap;color:{t["fg"]}">'
                f'{marked(ln, g.get("mark"), t["mk"], t["mt"])}</div>')
    out += (f'<div class="fx" data-after="h" data-gap="34" style="left:{M}px;top:1100px;width:820px;font:500 30px/1.3 I;'
            f'color:{t["mu"]}">{E(g.get("sub", ""))}</div>')
    if g["type"] == "store":
        out += (f'<div class="fx A" style="left:{M}px;top:560px;font-size:64px;background:{LIME};color:{INK};padding:12px 22px 4px">'
                f'{E(g["product"])} {E(g["price"])}</div>')
    return out, t["cls"], None


# 2. LAVA: the website's lava fills the tile, the message sits on a frosted glass card.
def lava(g):
    t = grid3.T[g["type"]]
    glass = {"lesson": "#f8f8f4b8", "store": "#0b0b0bb0", "news": "#D4FF3Ad0"}[g["type"]]
    fg = WHITE if g["type"] == "store" else INK
    longest = max(len(l) for l in g["lines"])
    size = int(min(96, 760 / (longest * .47)))
    out = (f'<div style="position:absolute;left:110px;right:110px;top:330px;bottom:330px;border-radius:36px;background:{glass};'
           f'backdrop-filter:blur(26px);-webkit-backdrop-filter:blur(26px);box-shadow:0 30px 80px #0003,inset 0 0 0 1.5px #ffffff66"></div>'
           f'<div class="fx Cc" style="left:540px;top:384px;transform:translateX(-50%);font-size:20px;letter-spacing:6px;color:{fg};'
           f'white-space:nowrap">{E(tag(g).upper())}</div>')
    mk_bg, mk_fg = (LIME, INK) if g["type"] != "news" else (INK, LIME)
    body = "<br>".join(marked(ln, g.get("mark"), mk_bg, mk_fg) for ln in g["lines"])
    out += (f'<div class="fx A" data-stack="h" style="left:150px;top:440px;width:780px;text-align:center;font-size:{size}px;'
            f'line-height:1.0;color:{fg}">{body}</div>')
    sub = E(g.get("sub", ""))
    if g["type"] == "store":
        sub = f'{E(g["product"])} · {E(g["price"])}'
    out += (f'<div class="fx" data-after="h" data-gap="34" style="left:170px;top:800px;width:740px;text-align:center;'
            f'font:600 30px/1.3 I;color:{fg};opacity:.85">{sub}</div>'
            f'<div class="fx Cc" style="left:540px;top:1100px;transform:translateX(-50%);font-size:20px;letter-spacing:6px;'
            f'color:{INK};white-space:nowrap">AUTOPILOT.OI</div>')
    return out, "bg-white", 1.0


# 3. CHAT: every tile looks like a conversation with Claude. The hub teaches by showing the actual chat.
def chat(g):
    you = joined(g)
    ai = g.get("sub", "")
    if g["type"] == "store":
        ai = f'{g["product"]} · {g["price"]}. {g.get("product_sub", "")}.'
    head = {"lesson": "Claude", "store": "Front Desk Kit", "news": "AI News"}[g["type"]]
    accent = LIME
    out = (f'<div style="position:absolute;left:0;right:0;top:0;height:150px;border-bottom:1.5px solid #ffffff22"></div>'
           f'<div style="position:absolute;left:{M}px;top:62px;width:44px;height:44px;border-radius:50%;background:{accent}"></div>'
           f'<div class="fx Ii" style="left:152px;top:66px;font-size:30px;color:{WHITE}">{E(head)}</div>'
           f'<div class="fx Mm" style="left:700px;top:72px;width:290px;text-align:right;font:400 18px M;letter-spacing:3px;'
           f'color:#a9a9a1" data-free="1">Nº {int(g.get("no", 1)):03d}</div>'
           f'<div class="fx" style="left:250px;top:250px;width:742px;box-sizing:border-box;padding:34px 40px 26px;border-radius:40px 40px 10px 40px;'
           f'background:{PAPER};color:{INK};font:400 74px/1.06 A;text-transform:uppercase">'
           f'{marked(you, g.get("mark"), LIME, INK)}</div>'
           f'<div class="fx" data-free="1" style="left:{M}px;top:760px;width:742px;box-sizing:border-box;padding:30px 36px;border-radius:40px 40px 40px 10px;'
           f'background:#1c1c1a;color:{WHITE};font:500 36px/1.3 I;border:1.5px solid #ffffff1a">{E(ai)}</div>'
           f'<div style="position:absolute;left:{M}px;right:{M}px;top:1150px;height:96px;border-radius:48px;background:#1c1c1a;'
           f'border:1.5px solid #ffffff22"></div>'
           f'<div class="fx Ii" style="left:136px;top:1180px;font-size:30px;color:#a9a9a1">'
           f'{E({"lesson": "Swipe for the prompts", "store": "Watch it work", "news": "Swipe for the story"}[g["type"]])}</div>'
           f'<div style="position:absolute;right:104px;top:1162px;width:72px;height:72px;border-radius:50%;background:{accent};'
           f'display:flex;align-items:center;justify-content:center;font:800 36px I;color:{INK}">↑</div>')
    return out, "bg-black", 0.25


# 4. VERTICAL: one giant word runs up the tile, a quiet column of text beside it.
def vertical(g):
    t = grid3.T[g["type"]]
    word = (g.get("mark") or g["lines"][-1]).strip(".,?!").upper()
    size = int(min(330, 1180 / max(len(word), 3) * 1.55))
    out = (f'<div style="position:absolute;left:0;top:0;width:{int(size * .98)}px;height:1350px;background:{t["mk"]}"></div>'
           f'<div style="position:absolute;left:{int(size * .49)}px;top:675px;transform:translate(-50%,-50%) rotate(-90deg);'
           f'font:400 {size}px/1 A;color:{t["mt"]};white-space:nowrap;padding-top:{int(size * .08)}px">{E(word)}</div>')
    x = int(size * .98) + 60
    w = 1080 - x - M
    out += (f'<div class="fx Cc" style="left:{x}px;top:80px;font-size:18px;letter-spacing:5px;color:{t["fg"]}">AUTOPILOT.OI</div>'
            f'<div class="fx Mm" style="left:{x}px;top:116px;font:400 18px M;letter-spacing:3px;color:{t["mu"]}">{E(tag(g).upper())}</div>'
            f'<div class="fx" style="left:{x}px;top:560px;width:{w}px;font:800 54px/1.05 I;letter-spacing:-1.5px;color:{t["fg"]}">'
            f'{E(joined(g))}</div>'
            f'<div class="fx" style="left:{x}px;top:900px;width:{w}px;font:500 28px/1.3 I;color:{t["mu"]}">{E(g.get("sub", ""))}</div>'
            f'<div class="fx Mm" style="left:{x}px;top:1220px;font:400 18px M;letter-spacing:3px;color:{t["fg"]}">'
            f'Nº {int(g.get("no", 1)):03d} · {E({"lesson": "SWIPE", "store": "WATCH", "news": "SWIPE"}[g["type"]])} →</div>')
    if g["type"] == "store":
        out += (f'<div class="fx A" style="left:{x}px;top:420px;font-size:44px;background:{LIME};color:{INK};padding:10px 18px 2px">'
                f'{E(g["product"])} {E(g["price"])}</div>')
    return out, t["cls"], None


STYLES = {"index": index, "lava": lava, "chat": chat, "vertical": vertical}


def render(g):
    return STYLES[g.get("style", "index")](g)
