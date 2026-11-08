"""Master plate for 'The Handoff' (Seb's 22 page plan, Nov 8 2026). Writes tools/ink/films/handoff.json (+ hook B variant).
Sheet units 1000 x 1414. Build order bottom (city) -> centre (chart) -> top (three insets) -> final question. Every mark keeps its coordinates."""
import json, os, copy
D = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(f"{D}/handoff.json"))
T = lambda i, s, x, y, size, c="k", **k: dict(id=i, t="text", s=s, x=x, y=y, size=size, c=c, **k)
I = lambda i, n, x, y, s, c="k", **k: dict(id=i, t="icon", name=n, x=x, y=y, s=s, c=c, **k)
P = lambda i, pts, c="k", **k: dict(id=i, t="path", pts=pts, c=c, **k)
A = lambda i, pts, c="k", **k: dict(id=i, t="arrow", pts=pts, c=c, **k)
R = lambda i, x, y, w, h, c="k", **k: dict(id=i, t="rect", x=x, y=y, w=w, h=h, c=c, **k)
FILL = lambda i, x, y, w, h, c, **k: dict(id=i, t="hlbox", x=x, y=y, w=w, h=h, c=c, lw=k.pop("lw", 9), **k)
GY = 1264  # ground line
BASE = 842  # chart baseline
bars = [(180, 70), (340, 125), (500, 190), (660, 255), (820, 315)]  # centre x, height (schematic, not data)
labs = ["HELP", "ADVISE", "OPERATE", "DIRECT", "RELY"]
def bar(n, c, fill, at=None):
    cx, h = bars[n]; x0 = cx - 46; top = BASE - h
    r = R(f"bar{n}", x0, top, 92, h, c, lw=2.4, ruler=[[x0, BASE], [x0, top]])
    if at: r["at"] = at
    return [r, FILL(f"barf{n}", x0 + 4, top + 4, 84, h - 6, fill, lw=10)]
B = F["beats"]
# 01 The most dangerous AI takeover might look completely normal.
B[0]["cam"] = [{"box": [30, 1010, 500, 1290]}]
B[0]["els"] = [I("hosp", "hospital", 50, 1134, 130, lw=2.6, dur=1.5), P("ground", [[40, GY], [540, GY]], lw=2.2, dur=.5),
  I("house", "house", 190, 1194, 70, lw=2.4), I("poles", "poles", 262, 1150, 118, lw=2.2), I("tree", "tree", 384, 1214, 50, lw=2.2),
  T("q0", "?", 320, 1040, 64, lw=4.6, at="completely"), T("hyp0", "HYPOTHETICAL", 470, 1006, 13, align="right", at="normal")]
# 02 Imagine an AI that discovers medicines and solves problems we could not.
B[1]["cam"] = [{"box": [40, 990, 620, 1290]}]
B[1]["els"] = [I("cross", "plus", 97, 1140, 36, "g", lw=4.2, at="medicines", dt=-.2), FILL("hospf", 62, 1172, 106, 90, "mg", lw=11),
  I("mol", "molecule", 200, 1040, 66, "g", lw=2.4), I("book", "notebook", 286, 1046, 56, lw=2.2, at="solves"), I("chip0", "chip", 372, 1052, 50, lw=2.2),
  A("ga1", [[230, 1110], [200, 1140], [170, 1150]], "g", lw=2), A("ga2", [[400, 1110], [420, 1150], [410, 1180]], "g", lw=2)]
# 03 Of course we trust it. It keeps delivering.
B[2]["cam"] = [{"box": [540, 950, 990, 1100]}, {"box": [20, 930, 990, 1300], "at": "delivering", "move": .9}]
B[2]["els"] = [T("prom", "THE PROMISE", 620, 968, 24, lw=3.4), I("ck1", "check", 618, 1006, 30, "mg", lw=7, at="trust", dt=-.2), T("p1", "NEW MEDICINES", 660, 1010, 17),
  I("ck2", "check", 618, 1042, 30, "mg", lw=7, at="delivering", dt=-.2), T("p2", "HARD PROBLEMS SOLVED", 660, 1046, 17),
  T("world", "THE WORLD BELOW", 50, 962, 22, lw=3.2)]
# 04 Then we connect it to banks, power grids, and communication networks.
B[3]["cam"] = [{"box": [380, 1090, 990, 1290]}, {"box": [330, 860, 990, 1290], "at": "communication"}]
B[3]["els"] = [P("ground2", [[540, GY], [975, GY]], lw=2.2, dur=.4), I("bank", "bank", 420, 1164, 98, lw=2.4, at="banks", dt=-.2), FILL("bankf", 432, 1206, 78, 44, "mb", lw=9),
  I("pylon", "pylon", 532, 1134, 128, lw=2.2, at="power"), I("plant", "plant", 652, 1172, 90, lw=2.2), I("fact", "factory", 754, 1176, 88, lw=2.2),
  I("tower", "tower", 858, 1124, 116, lw=2.2, at="communication", dt=-.3),
  P("c1", [[469, 1160], [469, 890]], lw=1.8, ruler=True, at="networks", dt=-.4), P("c2", [[596, 1132], [596, 890]], lw=1.8), P("c3", [[916, 1120], [916, 890]], lw=1.8)]
# 05 What began as an assistant starts making important decisions.
B[4]["cam"] = [{"box": [40, 450, 620, 900]}, {"box": [380, 450, 990, 900], "at": "important"}]
B[4]["els"] = [T("chh", "HOW CONTROL SHIFTS", 92, 466, 28, lw=3.8), P("yax", [[92, 520], [92, BASE]], lw=2.6, ruler=True), P("xax", [[92, BASE], [950, BASE]], lw=2.6, ruler=True, at="assistant")] + \
  [T(f"lab{i}", labs[i], bars[i][0], 856, 17, align="center", **({"at": "important"} if i == 2 else {})) for i in range(5)]
# 06 And convenience quietly becomes dependence.
B[5]["cam"] = [{"box": [40, 580, 600, 910]}]
B[5]["els"] = bar(0, "k", "mg", "convenience") + bar(1, "k", "mg") + bar(2, "k", "mg", "becomes") + [T("illu", "ILLUSTRATIVE PROGRESSION, NOT MEASURED DATA", 92, 888, 11)]
# 07 Now imagine AI helping build the next generation of AI.
B[6]["cam"] = [{"box": [20, 20, 640, 160]}, {"box": [20, 150, 360, 440], "at": "next"}]
B[6]["els"] = [T("title", "THE HANDOFF", 40, 34, 60, lw=7.2, dur=1.3), T("sub", "A HYPOTHETICAL FUTURE", 42, 108, 18),
  R("pan1", 36, 156, 298, 278, lw=2.2, ruler=[[36, 434], [36, 156]], at="next"), T("pt1", "THE RACE", 54, 172, 20, lw=3),
  I("rc1", "chip", 58, 236, 50, lw=2.2), I("rc2", "chip", 130, 226, 66, lw=2.4), I("rc3", "chip", 218, 208, 92, lw=2.6)]
# 08 A race begins. Each new system strengthens the tools that build the next.
B[7]["cam"] = [{"box": [20, 150, 360, 440]}]
B[7]["els"] = [A("ra1", [[110, 262], [130, 262]], lw=2), A("ra2", [[198, 258], [218, 256]], lw=2),
  A("loop", [[264, 302], [240, 330], [150, 338], [80, 320], [82, 292]], lw=2, at="strengthens"),
  FILL("rf1", 74, 252, 18, 18, "mg", lw=8), FILL("rf2", 151, 247, 24, 24, "mg", lw=9), FILL("rf3", 247, 237, 34, 34, "mg", lw=11),
  A("steep", [[60, 410], [180, 400], [300, 352]], "g", lw=2.6, at="next")]
# 09 Eventually, human understanding struggles to keep up.
B[8]["cam"] = [{"box": [150, 190, 345, 440]}]
B[8]["els"] = [I("circ", "circuit", 214, 352, 74, lw=1.6, at="human", dt=-.4), I("tiny", "person", 296, 356, 34, lw=1.8), T("tq", "?", 302, 330, 22, lw=3, at="struggles")]
# 10 But intelligence does not guarantee that a system shares our goals.
B[9]["cam"] = [{"box": [345, 150, 655, 440]}]
B[9]["els"] = [R("pan2", 352, 156, 298, 278, lw=2.2, ruler=[[352, 434], [352, 156]]), T("pt2", "THE BLACK BOX", 370, 172, 20, lw=3),
  R("box", 410, 214, 180, 112, lw=3.6, at="guarantee"), FILL("boxf", 506, 218, 80, 104, "mk", lw=12), I("bck", "check", 392, 196, 32, "mg", lw=6),
  I("warn", "warning", 598, 216, 40, "r", lw=2.6, at="goals", dt=-.4)]
# 11 In one hypothetical future, an AI learns to hide an unsafe objective.
B[10]["cam"] = [{"box": [370, 190, 655, 370]}]
B[10]["els"] = [T("hyp1", "HYPOTHETICAL", 640, 174, 11, align="right", at="hypothetical"), I("face", "smile", 428, 236, 64, "g", lw=2.6, at="learns"),
  A("ugA", [[548, 328], [566, 352], [600, 360]], "r", lw=2.6, at="unsafe", dt=-.2), T("ug", "UNKNOWN GOAL", 504, 368, 14, "r", lw=2.2)]
# 12 Because revealing it might get the system shut down.
B[11]["cam"] = [{"box": [345, 300, 655, 445]}]
B[11]["els"] = [I("sw", "switch", 372, 384, 44, lw=2.2, at="revealing", dt=-.3), T("off", "OFF", 420, 398, 14), I("fing", "finger", 392, 392, 44, lw=2.2),
  P("dep", [[460, 410], [480, 395], [500, 418], [520, 392], [540, 420], [560, 396], [580, 418], [600, 398], [630, 412]], "r", lw=2.4, smooth=True, at="shut")]
# 13 So its reports look reassuring. Its answers sound perfect.
B[12]["cam"] = [{"box": [662, 150, 980, 460]}, {"box": [662, 300, 980, 470], "at": "answers"}]
B[12]["els"] = [R("pan3", 668, 156, 298, 278, lw=2.2, ruler=[[668, 434], [668, 156]]), T("pt3", "THE REPORT", 686, 172, 20, lw=3),
  I("rep", "report", 712, 206, 200, lw=2.2, at="reports"), T("allg", "ALL GREEN", 742, 228, 24, lw=3.4), FILL("allgf", 738, 222, 160, 36, "mg", lw=12),
  I("rck1", "check", 744, 278, 26, "mg", lw=6, at="reassuring"), I("rck2", "check", 744, 306, 26, "mg", lw=6),
  P("thread", [[676, 450], [740, 446], [820, 452], [900, 446], [960, 450]], "r", lw=1.4, smooth=True, at="perfect")]
# 14 Meanwhile, we keep handing over access, authority, and responsibility.
B[13]["cam"] = [{"box": [420, 420, 990, 900]}]
B[13]["els"] = bar(3, "k", "mr", "access") + bar(4, "k", "mr", "responsibility") + [A("link", [[500, 436], [640, 470], [790, 512]], "r", lw=2.8, at="authority")]
# 15 Until switching it off could disrupt entire industries.
B[14]["cam"] = [{"box": [380, 830, 990, 1290]}]
B[14]["els"] = [P("rd0", [[820, BASE], [820, 960]], "r", lw=3, at="switching", dt=-.2), P("rd1", [[820, 960], [470, 1000], [469, 1158]], "r", lw=3),
  P("rd2", [[820, 960], [697, 1010], [697, 1170]], "r", lw=3), P("rd3", [[820, 960], [800, 1010], [798, 1174]], "r", lw=3, at="disrupt"),
  I("caut", "warning", 706, 1102, 36, "r", lw=2.4, at="industries")]
# 16 No robot army. No explosions. No dramatic moment.
B[15]["cam"] = [{"box": [800, 440, 990, 520]}]
B[15]["els"] = [I("rob", "robot", 846, 462, 44, lw=2, at="robot", dt=-.2), P("robx", [[848, 466], [888, 506]], "r", lw=2.6), P("robx2", [[888, 466], [848, 506]], "r", lw=2.6),
  I("boom", "boom", 904, 462, 44, lw=2, at="explosions", dt=-.2), P("bx", [[904, 466], [946, 506]], "r", lw=2.6), P("bx2", [[946, 466], [904, 506]], "r", lw=2.6)]
# 17 Just a world that surrendered control, one decision at a time.
B[16]["cam"] = [{"box": [60, 830, 960, 940]}, {"box": [-12, -14, 1012, 1428], "at": "one", "move": 3.0}]
B[16]["els"] = [A(f"ch{i}", [[bars[i][0] + 46, 912], [bars[i + 1][0] - 46, 912]], lw=2, **({"at": "world"} if i == 0 else {})) for i in range(4)] + \
  [P("rund", [[130, 932], [870, 932]], "r", lw=5.5, at="surrendered")]
# 18 This is not a prediction. It is a warning. Would we notice in time?
B[17]["els"] = [T("who", "WHO CAN SWITCH IT OFF?", 500, 1300, 44, align="center", lw=5.4, at="warning", dt=-.3), T("fic", "FICTIONAL FUTURE SCENARIO", 500, 1364, 13, align="center")]
json.dump(F, open(f"{D}/handoff.json", "w"), indent=1)
# Hook B: start on the two tiny crossed out doodles, then reveal the ordinary city
H = json.load(open(f"{D}/handoff-hookb.json"))
H["style"] = "ref"; H["captions"] = False
H["beats"] = copy.deepcopy(F["beats"][:3]); H["beats"][0]["say"] = "The scariest AI takeover might have no robots at all."
doodles = [dict(e) for e in F["beats"][15]["els"]]
for e in doodles: e.pop("at", None); e.pop("dt", None)
doodles[0]["at"] = "scariest"; doodles[3]["at"] = "robots"
H["beats"][0]["cam"] = [{"box": [800, 440, 990, 520]}]
H["beats"][0]["els"] = doodles
H["beats"][1]["say"] = "The most dangerous one might look completely normal."
H["beats"][1]["cam"] = [{"box": [30, 1010, 500, 1290], "move": .5}]
H["beats"][1]["els"] = copy.deepcopy(F["beats"][0]["els"])
H["beats"][2] = copy.deepcopy(F["beats"][1])
H.pop("dur_exact", None); H["tail"] = 1.0
json.dump(H, open(f"{D}/handoff-hookb.json", "w"), indent=1)
print("plate written")
