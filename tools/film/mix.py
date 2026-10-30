import sys, numpy as np, wave
sys.path.insert(0,'../reel'); import sfx
from sfx import add,kick,clap,hat,note,whoosh,click,chime,pop,SR
D=32.5; sfx.init(D); L,R=sfx.L,sfx.R
bpm=124; b=60/bpm
roots=[55.0,43.65,49.0,41.2]  # A F G E
for i in range(int(D/b)):
    t=i*b; bar=i//4
    if t>D-1.2: break
    if t>=0.25: add(kick(),t,.9 if t<28.9 else .7)
    if i%4 in (1,3) and t>3.3: add(clap(),t,.25)
    add(hat(),t+b/2,.18,pan=.3)
    if i%2==0: add(note(roots[bar%4],b*1.8,'bass'),t,.45)
for j in range(0,int(D/(4*b))):
    r=roots[j%4]*4
    for f in (r,r*1.26,r*1.5): add(note(f,4*b,'pad'),j*4*b,.05)
cuts=[3.3,6.3,8.5,11.1,13.7,16.3,18.9,22.2,24.2,28.9]
for c in cuts: add(whoosh(.4),c-.32,.5); add(kick(),c,.6)
for i in range(4): add(click(),.9+i*.38+.15,.6); add(pop(),.9+i*.38+.15,.25)
add(chime(),5.0,.25)
for c,d in [(9.1,0),(11.95,0),(15.0,0),(17.5,0)]: add(pop(),c,.5)
add(chime(),20.5,.35)
for k in range(8): add(click(),22.4+k*.06,.5)
add(whoosh(.25),22.9,.6)
for i in range(4): add(click(),24.2+.9+i*.5,.6); add(pop(),24.2+.9+i*.5,.3)
add(chime(),27.4,.35)
add(chime(),29.3,.4)
m=np.stack([L,R],1); m=m/np.max(np.abs(m))*.85
fade=np.ones(len(m)); n=int(1.0*SR); fade[-n:]=np.linspace(1,0,n); m*=fade[:,None]
w=wave.open('leak.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes((m*32767).astype(np.int16).tobytes());w.close();print('ok')
