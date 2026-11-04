"""Builds the site's display face "AP Wide" (docs/assets/fonts/APWide-Black.woff): Inter Display Black stretched
horizontally into a heavy extended grotesk, plus a Latin subset of Inter for body text. OFL 1.1 (Inter has no
Reserved Font Name; the derivative is renamed and keeps the license, see docs/assets/fonts/Inter-OFL.txt).
python3 tools/site/widefont.py [path to Inter otf folder]"""
import os, sys
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/usr/share/fonts/opentype/inter"
OUT = f"{ROOT}/docs/assets/fonts"
SX = 1.34  # horizontal stretch: verticals get heavier, horizontals stay, like a cut extended face
UNI = "U+0020-007E,U+00A0-00FF,U+2013-2014,U+2018-201D,U+2022,U+2026,U+20AC,U+2192,U+2713,U+00B7"


def sub(path, feats):
    f = TTFont(path)
    o = subset.Options(); o.layout_features = feats; o.name_IDs = ["*"]; o.notdef_outline = True; o.hinting = False
    s = subset.Subsetter(o); s.populate(unicodes=subset.parse_unicodes(UNI)); s.subset(f)
    return f


def rename(f, family, style="Regular"):
    for r in f["name"].names:
        if r.nameID in (1, 16): r.string = family
        elif r.nameID in (2, 17): r.string = style
        elif r.nameID == 4: r.string = f"{family} {style}".strip()
        elif r.nameID == 6: r.string = f"{family.replace(' ', '')}-{style}"


def _scale_values(f, sx):
    """Kerning lives in GPOS ValueRecords; stretch every horizontal value with the outlines."""
    if "GPOS" not in f: return
    def vr(v):
        if v is None: return
        for a in ("XAdvance", "XPlacement"):
            if hasattr(v, a): setattr(v, a, round(getattr(v, a) * sx))
    for lk in f["GPOS"].table.LookupList.Lookup:
        for st in lk.SubTable:
            st = getattr(st, "ExtSubTable", st)
            if st.LookupType == 1:
                if st.Format == 1: vr(st.Value)
                else: [vr(v) for v in st.Value]
            elif st.LookupType == 2:
                if st.Format == 1:
                    for ps in st.PairSet:
                        for r in ps.PairValueRecord: vr(r.Value1); vr(r.Value2)
                else:
                    for c1 in st.Class1Record:
                        for c2 in c1.Class2Record: vr(c2.Value1); vr(c2.Value2)


def wide():
    f = sub(f"{SRC}/InterDisplay-Black.otf", ["kern", "liga", "case", "tnum"])
    top = f["CFF "].cff.topDictIndex[0]; cs = top.CharStrings; gs = f.getGlyphSet(); hm = f["hmtx"].metrics
    new = {}
    for g in f.getGlyphOrder():
        w = round(hm[g][0] * SX)
        pen = T2CharStringPen(w, gs)
        gs[g].draw(TransformPen(pen, (SX, 0, 0, 1, 0, 0)))
        new[g] = (pen.getCharString(private=cs[g].private, globalSubrs=cs[g].globalSubrs), w)
    for g, (c, w) in new.items():
        cs[g] = c; c.compile(); b = c.calcBounds(cs) if hasattr(c, "calcBounds") else None
        hm[g] = (w, round(b[0]) if b else round(hm[g][1] * SX))
    _scale_values(f, SX)
    bb = top.FontBBox; top.FontBBox = [round(bb[0] * SX), bb[1], round(bb[2] * SX), bb[3]]
    f["head"].xMin = round(f["head"].xMin * SX); f["head"].xMax = round(f["head"].xMax * SX)
    f["hhea"].advanceWidthMax = max(w for w, _ in hm.values())
    rename(f, "AP Wide", "Black")
    f.flavor = "woff"; f.save(f"{OUT}/APWide-Black.woff")


def body():
    for w in ("Medium", "SemiBold", "Bold"):
        f = sub(f"{SRC}/Inter-{w}.otf", ["kern", "liga", "calt", "tnum", "case"])
        rename(f, "AP Text", w); f.flavor = "woff"; f.save(f"{OUT}/APText-{w}.woff")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); wide(); body()
    for n in sorted(os.listdir(OUT)):
        if n.startswith("AP"): print(n, os.path.getsize(f"{OUT}/{n}") // 1024, "KB")
