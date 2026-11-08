// node tools/ink/render.js <stem> <out.mp4> [RANGE=k/n env]   full render, silent H.264 (sound is muxed by mix.py + make.sh)
// node tools/ink/render.js <stem> --grab 1.0,5.5 <prefix>       single frames (JPG) for QA
// Needs the repo served on :8779 (make.sh does it).
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const [,,stem,a2,a3,a4]=process.argv;const RANGE=process.env.RANGE||'';
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>{if(/MISS|warn/i.test(m.text()))console.log('PAGE',m.text())});
await p.goto(`http://localhost:8779/tools/ink/ink.html?film=${stem}`+(process.env.NOCAP?'&nocap':'')+(process.env.HANDQ?'&hand=1':''));await p.waitForFunction(()=>window.READY===1,null,{timeout:120000});
const D=await p.evaluate(()=>window.DUR);
if(a2==='--grab'){for(const t of a3.split(',').map(Number)){await p.evaluate(t=>window.render(t),t);await p.screenshot({path:`${a4}_${t.toFixed(1)}.jpg`,type:'jpeg',quality:88})}
 fs.writeFileSync(`${a4}_tl.json`,JSON.stringify(await p.evaluate(()=>window.TL)));await b.close();return}
fs.writeFileSync(a2.replace(/\.mp4$/,'')+'.tl.json',JSON.stringify(await p.evaluate(()=>window.TL)));
const N=Math.round(D*30);let F0=0,F1=N;if(process.env.T0){F0=Math.round(+process.env.T0*30);F1=Math.min(N,Math.round(+(process.env.T1||D)*30))}if(RANGE){const A0=F0,A1=F1,[k,n]=RANGE.split('/').map(Number);F0=A0+Math.floor((A1-A0)*k/n);F1=A0+Math.floor((A1-A0)*(k+1)/n)}else if(false){const [k,n]=RANGE.split('/').map(Number);F0=Math.floor(N*k/n);F1=Math.floor(N*(k+1)/n)}
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',a2+'.tmp.mp4']);
console.log('frames',F0,F1,'of',N);const t0=Date.now();
for(let f=F0;f<F1;f++){const u=await p.evaluate(t=>{window.render(t);return document.getElementById('c').toDataURL('image/jpeg',.94).slice(23)},f/30);
 const img=Buffer.from(u,'base64');if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r));if(f%150===0)console.log('frame',f,((Date.now()-t0)/1000|0)+'s')}
ff.stdin.end();await new Promise(r=>ff.on('close',c=>{if(c===0)fs.renameSync(a2+'.tmp.mp4',a2);console.log('rendered',a2,c);r()}));await b.close()})();
