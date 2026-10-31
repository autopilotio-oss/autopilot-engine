"""Factory reel page: tools/office/engine.html (reel mode, top half) + reel.html overlay (agent work screen, bottom half).
python tools/freel/build.py <ep-stem>  -> tools/freel/<stem>.html + <stem>.meta.json   (needs <stem>.words.json from voice.py)"""
import os, sys, json, re
D = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(D))
ep = sys.argv[1]; E = json.load(open(f"{D}/eps/{ep}.json")); W = json.load(open(f"{D}/{ep}.words.json"))
beats, i = [], 0
for b in E["beats"]:
    n = len(b["say"].split()); ws = W[i:i + n]; i += n
    beats.append({"chip": b.get("chip"), "screen": b["screen"], "s": ws[0][1], "e": ws[-1][2]})
dur = round(beats[-1]["e"] + 2.4, 2)
ORDER = ['viral','gate','owner','studio','dm','email','store','ledger','support','health','vault','command']
NAMES = {'viral':'Viral Lab','gate':'Proof Gate','owner':"Owner's Desk",'studio':'Studio','dm':'DM Room','email':'Email Room','store':'The Store','ledger':'Ledger','support':'Support Desk','health':'Health Room','vault':'The Vault','command':'Growth Commander'}
data = {"reel": True, "room": E["room"], "roomNo": ORDER.index(E["room"]) + 1, "roomName": NAMES[E["room"]], "agent": E["agent"],
        "hook": E["hook"], "hookLines": E.get("hook_lines") or E["hook"], "beats": beats, "words": W, "cta": beats[-1]["s"], "dur": dur, "title": E["hook"]}
h = open(f"{ROOT}/tools/office/engine.html").read()
P = [  # reel mode patches on the office engine
 ('"./vendor/', '"/tools/office/vendor/'),
 ('const DATA=/*DATA*/null;', 'const DATA=/*DATA*/null;window.DATA=DATA;const TOPH=1010;'),
 ('<canvas id="gl" width="1080" height="1920">', '<canvas id="gl" width="1080" height="1010">'),
 ('rd.setSize(1080,1920,false)', 'rd.setSize(1080,TOPH,false)'),
 ('new THREE.WebGLRenderTarget(1080,1920,', 'new THREE.WebGLRenderTarget(1080,TOPH,'),
 ('comp.setSize(1080,1920)', 'comp.setSize(1080,TOPH)'),
 ('new THREE.Vector2(360,640)', 'new THREE.Vector2(360,337)'),
 ('w=h*1080/1920', 'w=h*1080/TOPH'),
 ('const zoom=cl((60-h)/30);const sh=(.07*zoom-.05*(1-zoom))*h;', 'const sh=.24*h;'),
 ('function camAt(t){', 'function camAt(t){if(DATA.reel){const st=camState(DATA.room);st.h=13.5;const u=ease(cl(t/2.6));return{...st,h:st.h*(1.5-.5*u)*(1-.04*cl((t-3)/20)),az:36+9*u+Math.sin(t*.3)*2,k:DATA.room,u:1}}'),
 ('dom(t,c);comp.render()', '(window.reelDom||dom)(t);comp.render()'),
 ("await document.fonts.load('40px ID');", "await document.fonts.load('100px AN');await document.fonts.load('500 20px CP');await document.fonts.load('700 20px CP');await document.fonts.load('40px ID');"),
 ("function tagTex(name,c){return ctex(512,128,(x,w,h)=>{x.font='600 34px JB';", "function tagTex(name,c){return ctex(512,128,(x,w,h)=>{x.font='700 36px CP';"),
 ("function bubbleTex(text,bg,fg){return ctex(640,160,(x,w,h)=>{x.font='600 44px JB';", "function bubbleTex(text,bg,fg){return ctex(640,160,(x,w,h)=>{x.font='700 46px CP';"),
 ("function chipTex(text,c){return ctex(512,112,(x,w,h)=>{x.font='700 40px JB';", "function chipTex(text,c){return ctex(512,112,(x,w,h)=>{x.font='700 42px CP';"),
]
for a, b in P:
    assert a in h, a; h = h.replace(a, b)
h = h.replace("</body>", open(f"{D}/reel.html").read() + "</body>").replace("/*DATA*/null", json.dumps(data))
open(f"{D}/{ep}.html", "w").write(h)
def events():
    ev = [["impact", i * .11, i] for i in range(len(data["hookLines"]))] + [["whoosh", 2.45, 0]]
    for bi, b in enumerate(beats):
        bs = b["s"] - .15 if bi else 0; be = beats[bi + 1]["s"] - .15 if bi + 1 < len(beats) else dur; L = max(.5, be - bs); sc = b["screen"]; T = lambda p: bs + p * L
        if bi: ev.append(["trans", bs, bi])
        k = sc["type"]
        if k == "ask":
            for i, _ in enumerate(sc.get("files", [])): ev.append(["drop", T(.05 + i * .1 + .06), i])
            t0 = .28 if sc.get("files") else .05; n = len(sc["text"])
            for c in range(n):
                if sc["text"][c] != " ": ev.append(["key", T(t0 + .45 * (c + 1) / n), c])
            ev.append(["send", T(t0 + .47), 0])
        elif k == "work":
            n = len(sc["lines"])
            for i in range(n): ev.append(["blip", T(i / (n + .6)), i]); ev.append(["tick", T((i + .85) / (n + .6)), i])
        elif k == "table":
            n = len(sc["rows"])
            for i in range(n): ev.append(["row", T(i * .62 / n), i])
            if sc.get("foot"): ev.append(["win", T(.72), 0])
        elif k == "checks":
            n = len(sc["rows"])
            for i in range(n): ev.append(["tick" if sc["rows"][i][2] else "deny", T(i * .6 / n), i])
            ev.append(["stamp_ok" if sc["ok"] else "stamp_no", T(.7), 0])
        elif k == "doc":
            n = len(sc["text"])
            for c in range(0, n, 3): ev.append(["key", T(c / n / 1.25), c])
        elif k == "dm":
            n = len(sc["msgs"])
            for i in range(n): ev.append(["msg", T(i * .7 / n), i])
        elif k == "cta": ev.append(["cta", T(0) + .05, 0])
    return [e for e in ev if 0 <= e[1] < dur]
json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]], "beats": beats, "events": events()}, open(f"{D}/{ep}.meta.json", "w"))
print("built", ep, dur, "s")
