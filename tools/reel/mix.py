import numpy as np, wave, sys, json
name=sys.argv[1]; meta=json.load(open(f'{name}.meta.json')); D=meta['dur']; P=meta['P']
DUR=D
import sfx; sfx.init(D); from sfx import add,kick,clap,hat,note,whoosh,click,chime,pop,SR
L,R=sfx.L,sfx.R
bpm=100;b=60/bpm;bar=4*b
prog=[(220.0,[220,261.6,329.6]),(174.6,[174.6,220,261.6]),(130.8,[261.6,329.6,392]),(196,[196,246.9,293.7])]
t=0.0
while t<DUR-1.0:
    root,ch=prog[int(t/bar)%4];beat=int(round(t/b))
    add(kick(),t,.2)
    if beat%4 in (1,3): add(clap(),t,.07)
    add(hat(),t+b/2,.05,pan=.25); add(note(root/2,b*.9,'bass'),t,.09)
    if beat%4==0:
        for f in ch: add(note(f,bar,'pad'),t,.022)
    t+=b
import importlib; spec=importlib.import_module(name)
for k,(pi,_,_) in enumerate(spec.SCENES):
    if k: s=P[pi]; add(whoosh(.5),s-0.45,.16); add(click(),s,.35)
add(chime(1568),P[spec.SCENES[-1][0]]+0.5,.22); add(pop(1200),P[spec.SCENES[-1][0]]+1.3,.18)
m=np.stack([L,R],1); m/=np.abs(m).max(); m*=0.32
m[-int(1.0*SR):]*=np.linspace(1,0,int(1.0*SR))[:,None]
with wave.open(f'{name}_bed.wav','wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((m*32767).astype('<i2').tobytes())
print('bed',name)
