const cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)), eo=x=>1-Math.pow(1-x,3), bk=x=>{const c=1.7;x=cl(x);return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const $=id=>document.getElementById(id);
const cap=$('cap');let curG=-1;
function setCap(t){let g=0;for(let i=0;i<GR.length;i++){if(t>=T[GR[i][0]].t-0.02)g=i}
 if(t>=CAPEND){cap.style.opacity=0;return}cap.style.opacity=1;
 if(g!==curG){curG=g;cap.innerHTML=GR[g].map(pi=>T[pi].words.map(w=>`<span data-t="${w.t}" class="${(EM[pi]||[]).includes(w.w.replace(/[.,:?!]/g,'').toLowerCase())?'em':''}">${w.w}</span>`).join('')).join('')}
 const sp=[...cap.querySelectorAll('span')];sp.forEach((s,i)=>{const st=+s.dataset.t,p=cl((t-st+0.04)/0.2);const nx=sp[i+1]?+sp[i+1].dataset.t:st+0.4;const act=t>=st&&t<nx;
 s.style.opacity=p;s.style.filter=`blur(${(1-eo(p))*10}px)`;s.style.transform=`translateY(${(1-eo(p))*40}px) rotate(${(1-eo(p))*-6}deg) scale(${(.8+.2*bk(p))*(act?1.07:1)})`;})}
const scr=$('scr');
function face(t){const fi=Math.round(t*30),m=MO[fi]||0;
 let mode='happy';MOODS.forEach(r=>{if(t>=r[0]&&t<r[1])mode=r[2]});
 const blink=(t%3.3)>3.18&&mode!='star'&&mode!='heart';
 let eyes='';const G='#C8FF3A';
 if(blink)eyes=`<path d="M100 140 h80 M240 140 h80"/>`;
 else if(mode=='happy')eyes=`<path d="M100 150 q40 -45 80 0 M240 150 q40 -45 80 0"/>`;
 else if(mode=='skep')eyes=`<path d="M100 120 l80 12 M240 128 l80 -4"/><path d="M110 150 q30 24 60 0 M250 150 q30 24 60 0" fill="${G}" stroke="none"/>`;
 else if(mode=='wide')eyes=`<circle cx="140" cy="135" r="34"/><circle cx="280" cy="135" r="34"/>`;
 else if(mode=='star')eyes=`<path d="M140 95 l14 30 33 4 -24 22 6 33 -29 -16 -29 16 6 -33 -24 -22 33 -4z M280 95 l14 30 33 4 -24 22 6 33 -29 -16 -29 16 6 -33 -24 -22 33 -4z" fill="${G}" stroke="none"/>`;
 else if(mode=='heart')eyes=`<path d="M140 175 c-50 -35 -30 -75 0 -55 c30 -20 50 20 0 55z M280 175 c-50 -35 -30 -75 0 -55 c30 -20 50 20 0 55z" fill="${G}"/>`;
 const h=6+m*58;
 const mouth=m>0.08?`<path d="M${170-m*8} 222 h${80+m*16} q-6 ${h} -${40+m*8} ${h} q-${34+m*8} 0 -${40+m*8} -${h}z" fill="${G}"/>`:(mode=='skep'?`<path d="M180 240 h60"/>`:`<path d="M170 230 q40 28 80 0"/>`);
 scr.innerHTML=`<svg viewBox="0 0 420 330" style="width:100%;height:100%"><defs><filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="rgba(0,0,0,.35)"/></pattern></defs><g filter="url(#g)" fill="none" stroke="${G}" stroke-width="13" stroke-linecap="round" stroke-linejoin="round">${eyes}${mouth}</g><rect width="420" height="330" fill="url(#sl)"/><path d="M30 40 Q120 10 200 18" stroke="#fff" stroke-opacity=".08" stroke-width="18" fill="none" stroke-linecap="round"/></svg>`;
 const k=Math.floor(t*30)%SCR.length;$('pf').src='fr/'+String(k+1).padStart(4,'0')+'.jpg';
 const [cx,cy,sw,sh,an]=SCR[k];const W=sw*1.03,H=sh*1.04;scr.style.cssText+=`;left:${180+cx-W/2}px;top:${1260+cy-60-H/2}px;width:${W}px;height:${H}px;transform:rotate(${an}deg);border-radius:${W*.16}px`}
let SEGS=null;
// SHIFTED: each scene's first element starts the moment the scene starts (keeps the stagger)
document.querySelectorAll('.sc').forEach(sc=>{const a=+sc.dataset.a;const els=[...sc.querySelectorAll('[data-in]')];if(!els.length)return;
 const m=Math.min(...els.map(e=>+e.dataset.in));if(m>a+0.02){const d=m-a-0.02;els.forEach(e=>e.dataset.in=(+e.dataset.in-d).toFixed(3));
 sc.querySelectorAll('[data-type],[data-count],[data-bar],[data-press],[data-strike],[data-on]').forEach(e=>{for(const k of ['press','strike','on']){if(e.dataset[k])e.dataset[k]=(+e.dataset[k]-d).toFixed(3)}
  for(const k of ['type','count','bar']){if(e.dataset[k]){const v=e.dataset[k].split(',');v[0]=(+v[0]-d).toFixed(3);e.dataset[k]=v.join(',')}}})}
 sc.dataset.b=(+sc.dataset.b+0.12).toFixed(3)});
function chrome(t){
 if(!SEGS){const pr=$('prog');SEGS=SEC.map((x,i)=>{const d=document.createElement('div');d.className='seg';d.innerHTML='<i></i>';pr.appendChild(d);return [x[0],i+1<SEC.length?SEC[i+1][0]:DUR,d.firstChild]})}
 SEGS.forEach(([a,b,el])=>el.style.width=(cl((t-a)/(b-a))*100)+'%');
 const left=Math.max(0,Math.ceil(DUR-t));$('left').textContent='0:'+String(left).padStart(2,'0');
 let s='';SEC.forEach(x=>{if(t>=x[0])s=x[1].replace(/^\d+ · /,'')});$('sec').textContent=s;
 // atmosphere drift
 $('b1').style.transform=`translate(${-200+Math.sin(t*.35)*160}px,${-220+Math.cos(t*.27)*120}px)`;
 $('b2').style.transform=`translate(${500+Math.cos(t*.3)*180}px,${900+Math.sin(t*.22)*160}px)`;
 const ph=(t%5.5)/1.1;$('streak').style.opacity=ph<1?Math.sin(ph*Math.PI)*.8:0;$('streak').style.top=(380+((Math.floor(t/5.5)*373)%700))+'px';$('streak').style.transform=`translateX(${(ph-.5)*600}px)`;
 $('grain').style.backgroundImage=`url(grain${Math.floor(t*24)%6}.png)`;
 // camera: slow push, kick on every scene change
 let last=0;SEC.forEach(x=>{if(t>=x[0])last=x[0]});const k=t-last,kick=last>0?Math.exp(-k*7)*(k<1.2?1:0):0;
 $('cam').style.transform=`scale(${1.0+0.025*Math.sin(t*.25)+kick*0.035}) translate(${Math.sin(k*38)*kick*7}px,${Math.cos(k*31)*kick*5}px) rotate(${Math.sin(k*25)*kick*.35}deg)`;
 $('flash').style.opacity=kick*.55;
}
function render(t){
 chrome(t);setCap(t);face(t);
 document.querySelectorAll('.sc').forEach(sc=>{const a=+sc.dataset.a,b=+sc.dataset.b;const pi=cl((t-a)/0.32),po=cl((t-b+0.18)/0.18);const on=t>=a-0.01&&t<b+0.01;
  sc.style.display=on?'block':'none';if(!on)return;
  sc.style.opacity=Math.min(1,eo(pi)*1.6)*(1-po);sc.style.filter=(pi<1||po>0)?`blur(${(1-eo(pi))*6+po*8}px)`:'none';
  sc.style.transform=`translateX(${(1-eo(pi))*110-po*90}px) skewX(${(1-eo(pi))*-5}deg) scale(${1+po*.05})`});
 document.querySelectorAll('[data-in]').forEach(e=>{const st=+e.dataset.in,p=cl((t-st)/0.42),q=eo(p);e.style.opacity=cl(p*3);
  e.style.transform=(e.dataset.base||'')+` translateY(${(1-q)*70}px) rotateX(${(1-q)*28}deg) scale(${.82+.18*bk(p)})`;e.style.filter=q<1?`blur(${(1-q)*7}px)`:'none';
  if(e.classList.contains('card'))e.style.setProperty('--sh',(-60+cl((t-st-0.25)/0.9)*230)+'%')});
 document.querySelectorAll('[data-on]').forEach(e=>e.classList.toggle('on',t>=+e.dataset.on));
 document.querySelectorAll('[data-type]').forEach(e=>{const [a,d]=e.dataset.type.split(',').map(Number);const tx=e.dataset.text;e.textContent=tx.slice(0,Math.round(cl((t-a)/d)*tx.length));});
 document.querySelectorAll('[data-count]').forEach(e=>{const [a,d,f,to]=e.dataset.count.split(',').map(Number);const v=f+(to-f)*eo(cl((t-a)/d));e.textContent=(e.dataset.pre||'')+(e.dataset.dec?v.toFixed(+e.dataset.dec):Math.round(v).toLocaleString('en-US'))+(e.dataset.suf||'')});
 document.querySelectorAll('[data-bar]').forEach(e=>{const [a,d,f,to]=e.dataset.bar.split(',').map(Number);e.style.width=(f+(to-f)*eo(cl((t-a)/d)))+'%'});
 document.querySelectorAll('[data-press]').forEach(e=>{const p=cl((t-e.dataset.press)/0.25);e.style.transform=`scale(${1-.12*Math.sin(p*Math.PI)})`});
 document.querySelectorAll('[data-strike]').forEach(e=>{e.style.transform=`scaleX(${eo(cl((t-e.dataset.strike)/0.3))})`});
}
window.render=render;window.ready=true;
