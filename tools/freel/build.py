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
        "hook": E["hook"], "beats": beats, "words": W, "cta": beats[-1]["s"], "dur": dur, "title": E["hook"]}
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
 ('const zoom=cl((60-h)/30);const sh=(.07*zoom-.05*(1-zoom))*h;', 'const sh=.05*h;'),
 ('function camAt(t){', 'function camAt(t){if(DATA.reel){const st=camState(DATA.room);st.h=13.5;const u=ease(cl(t/2.6));return{...st,h:st.h*(1.5-.5*u)*(1-.04*cl((t-3)/20)),az:36+9*u+Math.sin(t*.3)*2,k:DATA.room,u:1}}'),
 ('dom(t,c);comp.render()', '(window.reelDom||dom)(t);comp.render()'),
]
for a, b in P:
    assert a in h, a; h = h.replace(a, b)
h = h.replace("</body>", open(f"{D}/reel.html").read() + "</body>").replace("/*DATA*/null", json.dumps(data))
open(f"{D}/{ep}.html", "w").write(h)
json.dump({"dur": dur, "cuts": [b["s"] for b in beats[1:]], "beats": beats}, open(f"{D}/{ep}.meta.json", "w"))
print("built", ep, dur, "s")
