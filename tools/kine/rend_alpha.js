// node tools/kine/rend_alpha.js <page> <out.mov>  (RANGE=k/n optional) -> ProRes 4444 with alpha. Needs repo served on :8778.
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const [,,page,out]=process.argv;const RANGE=process.env.RANGE||'';
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('PAGEERR',e.message));
await p.goto('http://localhost:8778/'+page+'?alpha');await p.waitForFunction(()=>window.READY===1,null,{timeout:120000});await p.waitForTimeout(800);
const D=await p.evaluate(()=>window.DUR);const N=Math.round(D*30);let F0=0,F1=N;if(RANGE){const [k,n]=RANGE.split('/').map(Number);F0=Math.floor(N*k/n);F1=Math.floor(N*(k+1)/n)}
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','prores_ks','-profile:v','4444','-pix_fmt','yuva444p10le','-qscale:v','11',out+'.tmp.mov']);
console.log('frames',F0,F1,'of',N);const t0=Date.now();
for(let f=F0;f<F1;f++){await p.evaluate(t=>window.render(t),f/30);const img=await p.screenshot({type:'png',omitBackground:true});if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r));if(f%150===0)console.log('frame',f,((Date.now()-t0)/1000|0)+'s')}
ff.stdin.end();await new Promise(r=>ff.on('close',c=>{if(c===0)fs.renameSync(out+'.tmp.mov',out);console.log('rendered',out,c);r()}));await b.close()})();
