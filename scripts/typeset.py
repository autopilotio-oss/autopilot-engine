"""AUTOPILOT.OI type system (Pillow). Barlow Condensed Black Italic for headlines (uppercase), Geist for body,
Geist Mono for labels. Mark emphasis words with {curly braces}: same font, lime."""
import os, re
from PIL import ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, "tools", "story", "fonts")
_cache = {}
def font(name, size):
    k = (name, size)
    if k not in _cache: _cache[k] = ImageFont.truetype(os.path.join(FD, name), size)
    return _cache[k]
SANS, SANS_B, MONO = "Geist-SemiBold.otf", "Geist-Bold.otf", "GeistMono-Medium.otf"
DISPLAY = "SairaSemiCondensed-BlackItalic.otf"
SLANT = 0.16   # extra slant on top of the italic, to match the AUTOPILOT.OI headline style

def rich(d, text, x, y, width, size, fill, em_fill, sans=SANS, lead=1.12, track=-0.02, upper=False, line_cb=None):
    """Draws text with {emphasis} words in serif italic. Returns the y below the last line."""
    if upper: text = text.upper()
    toks = [(m.group(1) or m.group(2), bool(m.group(1))) for m in re.finditer(r"\{([^}]*)\}|(\S+)", text)]
    words = []
    for t, em in toks:
        for i, w in enumerate(t.split(" ")):
            words.append((w, em))
    fs = font(sans, size); fe = fs
    space = d.textlength(" ", font=fs) * 0.9
    lines, cur, cw = [], [], 0
    for w, em in words:
        f = fe if em else fs; wl = d.textlength(w, font=f) + size * track * len(w)
        if cur and cw + space + wl > width:
            lines.append(cur); cur, cw = [], 0
        cur.append((w, em, f, wl)); cw += (space if len(cur) > 1 else 0) + wl
    if cur: lines.append(cur)
    lh = int(size * lead); base = y + int(size * 0.9)
    for ln in lines:
        def draw_line(dd, ln=ln, base=base):
            cx = x
            for w, em, f, wl in ln:
                for ch in w:
                    dd.text((cx, base), ch, font=f, fill=em_fill if em else fill, anchor="ls"); cx += dd.textlength(ch, font=f) + size * track
                cx += space - size * track
        if line_cb: line_cb(draw_line)
        else: draw_line(d)
        base += lh
    return base - int(size * 0.9) + int(size * 0.25)

def label(d, text, x, y, size, fill, track=0.12, anchor="la"):
    f = font(MONO, size); cx = x
    if anchor == "ra":
        cx = x - sum(d.textlength(c, font=f) + size * track for c in text)
    for ch in text.upper():
        d.text((cx, y), ch, font=f, fill=fill); cx += d.textlength(ch, font=f) + size * track
    return cx

def _slanted(d, draw_fn):
    """Draws onto a transparent layer, then slants only the text's own box (fast)."""
    from PIL import Image, ImageDraw
    base = d._image; W, H = base.size
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    out = draw_fn(ld)
    bb = layer.getbbox()
    if not bb: return out
    pad = int((bb[3] - bb[1]) * SLANT) + 20
    x0, y0, x1, y1 = max(0, bb[0] - pad), bb[1], min(W, bb[2] + pad), bb[3]
    crop = layer.crop((x0, y0, x1, y1)); h = y1 - y0
    crop = crop.transform(crop.size, Image.AFFINE, (1, SLANT, -SLANT * h / 2, 0, 1, 0), resample=Image.BICUBIC)
    base.paste(crop, (x0, y0), crop)
    return out

def headline(d, text, x, y, width, size, fill=(244, 244, 240), em_fill=(212, 255, 58), lead=0.98):
    """Big sporty headline: Saira SemiCondensed Black Italic + extra slant, uppercase."""
    return rich(d, text, x + int(size * SLANT * 0.45), y, width - 40, size, fill, em_fill, sans=DISPLAY, lead=lead, track=0.0, upper=True,
                line_cb=lambda draw_line: _slanted(d, draw_line))

def slant_text(d, xy, text, size, fill, anchor="ls"):
    """Single line in the headline font with the extra slant."""
    return _slanted(d, lambda ld: ld.text((xy[0] + int(size * SLANT * 0.4), xy[1]), text, font=font(DISPLAY, size), fill=fill, anchor=anchor))
