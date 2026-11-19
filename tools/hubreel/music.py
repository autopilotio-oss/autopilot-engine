import numpy as np, wave, sys
out=sys.argv[1]
SR=44100; bpm=128; B=60/bpm; BEATS=28; dur=BEATS*B; n=int(round(SR*dur)); L=np.zeros(n); rng=np.random.default_rng(11)
def add(sig,t,g=1.0):
    i=int(round(t*SR))%n; idx=(i+np.arange(len(sig)))%n; np.add.at(L,idx,sig*g)
x=lambda d:np.arange(int(d*SR))/SR
kick=lambda: np.sin(2*np.pi*(42+140*np.exp(-x(.32)*28))*x(.32))*np.exp(-x(.32)*9)
clap=lambda: np.convolve(rng.standard_normal(int(.16*SR)),np.ones(3)/3,'same')*np.exp(-x(.16)*30)
hat=lambda: np.diff(rng.standard_normal(int(.04*SR)+1))*np.exp(-x(.04)*110)
C=[0,4*B,11*B,19*B,21.5*B,27*B]
for i in range(BEATS*2):
    t=i*B/2; hk=t<C[1]
    if i%2==0: add(kick(),t,.6 if hk else .95)
    if i%4==2 and not hk: add(clap(),t,.4)
    add(hat(),t,.08 if hk else .2)
    if not hk and i%2==1: add(hat(),t+B/4,.1)
roots=[55,43.65,65.4,49,55,43.65,49]; ch=[(220,261.6,329.6),(174.6,220,261.6),(261.6,329.6,392),(196,246.9,293.7),(220,261.6,329.6),(174.6,220,261.6),(196,246.9,293.7)]
for bar in range(BEATS//4):
    r_=roots[bar]; c=ch[bar]
    for j in range(8):
        t=bar*4*B+j*B/2; d=x(B/2*.92); add(np.tanh(2.2*np.sin(2*np.pi*r_*d))*np.exp(-d*2.5)*.33,t,.6 if t<C[1] else 1)
    for j in (0,3,6):
        t=bar*4*B+j*B/2; d=x(.22); add(sum(np.sign(np.sin(2*np.pi*f*d))*.4+np.sin(2*np.pi*f*d) for f in c)*np.exp(-d*15)*.05,t)
def whoosh(d=.3):
    s=np.convolve(rng.standard_normal(int(d*SR)),np.ones(10)/10,'same'); return s*np.sin(np.linspace(0,np.pi,len(s)))**2*.8
boom=lambda: np.sin(2*np.pi*(36+90*np.exp(-x(.9)*7))*x(.9))*np.exp(-x(.9)*4)
add(boom(),0,1.0)
for t in (.25,.55,1.0): add(np.convolve(rng.standard_normal(int(.07*SR)),np.ones(4)/4,'same')*np.exp(-x(.07)*45),t,.4)
for c in C[1:4]: add(whoosh(),c-.2,.6); add(boom(),c,.45)
add(whoosh(.4),C[4]-.25,.6); add(boom(),C[4],.6)
add(whoosh(.35),dur-.4,.55)
t0=C[2]
for a,z in ((t0-.1,t0+.75),(t0+1.95,t0+2.45)):
    for t in np.arange(a,z,0.06): add(np.diff(rng.standard_normal(int(.01*SR)+1))*np.exp(-x(.01)*300),t,.22)
pop=lambda: np.sin(2*np.pi*880*x(.08))*np.exp(-x(.08)*40)
stamp=lambda: np.convolve(rng.standard_normal(int(.07*SR)),np.ones(4)/4,'same')*np.exp(-x(.07)*45)
for t in (t0+1.0,t0+2.6,C[4]+.8,C[4]+1.0): add(pop(),t,.25)
for i in range(5): add(stamp(),C[1]+.12+i*B*1.1+.25,.35)
tick=lambda: np.sin(2*np.pi*1800*x(.02))*np.exp(-x(.02)*200)
for t in np.arange(C[3],C[3]+.9,.075): add(tick(),t,.12)
L=np.tanh(L*1.25); L/=np.abs(L).max()*1.12
w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([L,L],1)*32767).astype(np.int16).tobytes()); w.close(); print(dur)
