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
DISPLAY = "BarlowCondensed-BlackItalic.otf"

def rich(d, text, x, y, width, size, fill, em_fill, sans=SANS, lead=1.12, track=-0.02, upper=False):
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
        cx = x
        for w, em, f, wl in ln:
            for ch in w:
                d.text((cx, base), ch, font=f, fill=em_fill if em else fill, anchor="ls"); cx += d.textlength(ch, font=f) + size * track
            cx += space - size * track
        base += lh
    return base - int(size * 0.9) + int(size * 0.25)

def label(d, text, x, y, size, fill, track=0.12, anchor="la"):
    f = font(MONO, size); cx = x
    if anchor == "ra":
        cx = x - sum(d.textlength(c, font=f) + size * track for c in text)
    for ch in text.upper():
        d.text((cx, y), ch, font=f, fill=fill); cx += d.textlength(ch, font=f) + size * track
    return cx

def headline(d, text, x, y, width, size, fill=(244, 244, 240), em_fill=(212, 255, 58), lead=0.96):
    """Big sporty headline: Barlow Condensed Black Italic, uppercase."""
    return rich(d, text, x, y, width, size, fill, em_fill, sans=DISPLAY, lead=lead, track=0.0, upper=True)
