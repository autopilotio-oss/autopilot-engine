"""'The Handoff' as a storyboard: one numbered sketch per narration line, snaking across the sheet, each linked to the last.
Seb, Nov 8 2026: 'each 5 seconds something new is drawn that plays into the bigger picture'. No ruler. Writes tools/ink/films/handoff.json."""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(f"{D}/handoff.json"))
F["tease"] = 1.9; F["style"] = "ref"; F["captions"] = False
COLS = [34, 360, 686]; ROWS = [150, 345, 540, 735, 930, 1125]; CW, CH = 280, 172
order = []
for r in range(6):
    cs = range(3) if r % 2 == 0 else range(2, -1, -1)
    order += [(COLS[c], ROWS[r]) for c in cs]
T = lambda i, s, x, y, size, c="k", **k: dict(id=i, t="text", s=s, x=x, y=y, size=size, c=c, **k)
I = lambda i, n, x, y, s, c="k", **k: dict(id=i, t="icon", name=n, x=x, y=y, s=s, c=c, **k)
P = lambda i, pts, c="k", **k: dict(id=i, t="path", pts=pts, c=c, **k)
A = lambda i, pts, c="k", **k: dict(id=i, t="arrow", pts=pts, c=c, **k)
FL = lambda i, x, y, w, h, c: dict(id=i, t="hlbox", x=x, y=y, w=w, h=h, c=c)
R = lambda i, x, y, w, h, c="k", **k: dict(id=i, t="rect", x=x, y=y, w=w, h=h, c=c, **k)
cap = ["A NORMAL TOWN", "IT CURES", "WE TRUST IT", "WE CONNECT IT", "IT DECIDES", "WE DEPEND ON IT",
       "AI BUILDS AI", "A RACE BEGINS", "WE FALL BEHIND", "WHOSE GOALS?", "A HIDDEN GOAL", "DON'T SWITCH ME OFF",
       "ALL GREEN", "WE HAND OVER", "TOO BIG TO SWITCH OFF", "NO ROBOTS", "ONE STEP AT A TIME", "WOULD WE NOTICE?"]


def cell(n, x, y):
    """the drawing for sketch n (0 based) inside the cell whose top left corner is x, y"""
    q = lambda name, dx, dy, s, c="k", **k: I(f"d{n}{name}{dx}", name, x + dx, y + dy, s, c, **k)
    if n == 0:   # a normal town
        return [q("hospital", 40, 30, 96, lw=2.4), q("house", 150, 76, 50, lw=2.2), q("tree", 214, 82, 44, lw=2.2),
                P(f"g{n}", [[x + 20, y + 128], [x + 262, y + 128]], lw=2), FL(f"f{n}", x + 50, y + 60, 80, 66, "mg")]
    if n == 1:   # the AI cures
        return [q("chip", 26, 34, 70, lw=2.4), T(f"ai{n}", "AI", x + 61, y + 62, 16, align="center"),
                A(f"a{n}", [[x + 104, y + 70], [x + 160, y + 70]], lw=2.2), q("molecule", 172, 30, 74, "g", lw=2.4), q("plus", 120, 92, 34, "g", lw=4)]
    if n == 2:   # trust meter swings to high
        return [q("meter", 80, 10, 120, lw=2.4), P(f"nd{n}", [[x + 140, y + 116], [x + 188, y + 52]], lw=3.4),
                T(f"lo{n}", "LOW", x + 40, y + 108, 11), T(f"hi{n}", "HIGH", x + 206, y + 108, 11), q("check", 222, 20, 40, "mg", lw=6)]
    if n == 3:   # wired into banks, grid, networks
        return [q("chip", 112, 52, 56, lw=2.4), q("bank", 14, 16, 58, lw=2), q("pylon", 214, 10, 62, lw=2), q("tower", 214, 82, 56, lw=2),
                P(f"s1{n}", [[x + 74, y + 50], [x + 112, y + 72]], lw=1.8), P(f"s2{n}", [[x + 168, y + 72], [x + 214, y + 48]], lw=1.8),
                P(f"s3{n}", [[x + 168, y + 96], [x + 214, y + 108]], lw=1.8)]
    if n == 4:   # it starts deciding
        return [q("chip", 18, 50, 56, lw=2.4), A(f"a{n}", [[x + 78, y + 78], [x + 112, y + 78]], lw=2.2), q("diamond", 116, 28, 100, lw=2.4),
                T(f"dq{n}", "?", x + 160, y + 60, 34, lw=4), A(f"y{n}", [[x + 216, y + 78], [x + 262, y + 78]], "g", lw=2.2)]
    if n == 5:   # dependence grows
        out = [P(f"ax{n}", [[x + 26, y + 128], [x + 256, y + 128]], lw=2)]
        for j, (bx, h) in enumerate([(40, 34), (110, 62), (180, 96)]):
            out += [R(f"b{n}{j}", x + bx, y + 128 - h, 52, h, lw=2.2), FL(f"bf{n}{j}", x + bx + 3, y + 131 - h, 46, h - 5, "mg")]
        return out
    if n == 6:   # AI builds AI
        return [q("chip", 26, 56, 52, lw=2.2), A(f"a{n}", [[x + 86, y + 82], [x + 132, y + 82]], lw=2.2), q("chip", 140, 18, 112, lw=2.8)]
    if n == 7:   # the race: each chip bigger, the curve steeper
        return [A(f"cu{n}", [[x + 20, y + 132], [x + 120, y + 118], [x + 200, y + 80], [x + 258, y + 12]], "g", lw=2.6),
                q("chip", 24, 96, 28, lw=1.8), q("chip", 92, 78, 36, lw=2), q("chip", 160, 46, 46, lw=2.2), q("chip", 214, 4, 56, lw=2.4)]
    if n == 8:   # humans fall behind
        return [q("circuit", 20, 14, 150, lw=1.8), q("person", 200, 70, 50, lw=2), T(f"q{n}", "?", x + 252, y + 40, 30, lw=3.6)]
    if n == 9:   # whose goals? red enters
        return [P(f"st{n}", [[x + 30, y + 120], [x + 120, y + 90]], lw=2.4), A(f"g1{n}", [[x + 120, y + 90], [x + 230, y + 40]], "g", lw=2.6),
                T(f"o{n}", "OURS", x + 236, y + 26, 13, "g"), A(f"g2{n}", [[x + 120, y + 90], [x + 230, y + 130]], "r", lw=2.6), T(f"i{n}", "ITS", x + 236, y + 122, 13, "r")]
    if n == 10:  # a friendly face over a sealed box
        return [R(f"bx{n}", x + 120, y + 20, 110, 100, lw=3), FL(f"bf{n}", x + 124, y + 24, 102, 92, "mk"), q("smile", 54, 30, 76, "g", lw=2.6),
                A(f"ra{n}", [[x + 232, y + 100], [x + 262, y + 126]], "r", lw=2.4), T(f"u{n}", "UNKNOWN GOAL", x + 140, y + 130, 11, "r")]
    if n == 11:  # the off switch, tangled
        return [q("switch", 40, 20, 90, lw=2.4), T(f"of{n}", "OFF", x + 140, y + 40, 18), q("finger", 70, 50, 80, lw=2.2),
                P(f"sc{n}", [[x + 150, y + 90], [x + 180, y + 70], [x + 200, y + 104], [x + 226, y + 72], [x + 250, y + 106]], "r", lw=2.4, smooth=True)]
    if n == 12:  # all green, red thread beneath
        return [q("report", 70, 6, 120, lw=2.2), T(f"ag{n}", "ALL GREEN", x + 92, y + 22, 15, lw=2.4), FL(f"agf{n}", x + 88, y + 18, 90, 22, "mg"),
                q("check", 96, 58, 22, "mg", lw=5), q("check", 96, 82, 22, "mg", lw=5),
                P(f"th{n}", [[x + 20, y + 132], [x + 100, y + 128], [x + 180, y + 134], [x + 262, y + 128]], "r", lw=1.6, smooth=True)]
    if n == 13:  # we hand over the keys
        return [q("key", 20, 50, 90, lw=2.4), A(f"a{n}", [[x + 118, y + 78], [x + 166, y + 78]], "r", lw=2.4), q("chip", 176, 40, 76, lw=2.6)]
    if n == 14:  # switch wired to the bank, power, factory from sketch 4
        return [q("switch", 116, 0, 48, lw=2.2), P(f"l1{n}", [[x + 140, y + 48], [x + 48, y + 72]], "r", lw=2.4), P(f"l2{n}", [[x + 140, y + 48], [x + 140, y + 72]], "r", lw=2.4),
                P(f"l3{n}", [[x + 140, y + 48], [x + 228, y + 72]], "r", lw=2.4), q("bank", 22, 74, 50, lw=2), q("plant", 115, 76, 50, lw=2), q("factory", 203, 76, 50, lw=2)]
    if n == 15:  # no robots, no explosions
        return [q("robot", 40, 20, 90, lw=2.2), P(f"x1{n}", [[x + 46, y + 30], [x + 124, y + 108]], "r", lw=3), P(f"x2{n}", [[x + 124, y + 30], [x + 46, y + 108]], "r", lw=3),
                q("boom", 160, 20, 90, lw=2.2), P(f"x3{n}", [[x + 164, y + 30], [x + 246, y + 108]], "r", lw=3), P(f"x4{n}", [[x + 246, y + 30], [x + 164, y + 108]], "r", lw=3)]
    if n == 16:  # down the stairs, one decision at a time
        return [q("stairs", 70, 10, 130, lw=2.4), q("person", 176, 64, 36, lw=2), T(f"h{n}", "HELP", x + 30, y + 16, 12), T(f"r{n}", "RELY", x + 214, y + 112, 12, "r")]
    if n == 17:  # would we notice?
        return [q("eye", 80, 20, 120, lw=2.4), T(f"q{n}", "?", x + 210, y + 40, 40, lw=4.4)]


B = F["beats"]
for n in range(18):
    x, y = order[n]; b = B[n]
    els = [T(f"n{n}", str(n + 1), x + 2, y - 6, 16, lw=2.6)] + cell(n, x, y) + [T(f"cap{n}", cap[n], x + CW / 2, y + 146, 15, align="center", lw=2.4)]
    if n > 0:  # arrow from the previous sketch keeps the story path readable on the final page
        px, py = order[n - 1]
        if py == y:
            a = [[px + CW + 2, y + 70], [x - 10, y + 70]] if x > px else [[px - 8, y + 70], [x + CW + 4, y + 70]]
        else:
            a = [[px + CW / 2, py + CH], [x + CW / 2, y - 12]]
        els.insert(0, A(f"link{n}", a, "r" if n >= 9 else "k", lw=2))
    b["els"] = els
    b["cam"] = [{"box": [x - 22, y - 26, x + CW + 22, y + CH + 10], "move": 1.0}]
# the title is written during the pull back; the final question goes at the bottom
B[16]["els"] += [T("title", "THE HANDOFF", 34, 36, 54, lw=6.6), T("sub", "A HYPOTHETICAL FUTURE", 36, 104, 17)]
B[16]["cam"] = [B[16]["cam"][0], {"box": [-14, -14, 1014, 1428], "at": "one", "move": 2.6}]
B[17]["els"] += [T("who", "WHO CAN SWITCH IT OFF?", 500, 1318, 42, align="center", lw=5.2, at="notice"),
                 T("fic", "FICTIONAL FUTURE SCENARIO", 500, 1376, 12, align="center")]
B[17]["cam"] = []
json.dump(F, open(f"{D}/handoff.json", "w"), indent=1)
print("storyboard written")
