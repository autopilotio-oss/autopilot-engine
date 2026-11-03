// node tools/office/rend.js <page path from repo root> <out.mp4|x> [t1,t2..]   (needs: python3 -m http.server 8778 at repo root)
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const [,,page,out,only]=process.argv;const RANGE=process.env.RANGE||'';
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--enable-webgl']});
const p=await b.newPage({viewport:{width:1080,height:1920}});p.on('pageerror',e=>console.log('PAGEERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CONSOLE',m.text())});
await p.goto('http://localhost:8778/'+page);await p.waitForFunction(()=>window.READY===1,null,{timeout:120000});await p.waitForTimeout(1500);
const step=async t=>{await p.evaluate(t=>window.render(t),t)};
if(only){const ts=only.split(',').map(Number);for(let i=0;i<ts.length;i++){await step(ts[i]);await p.screenshot({path:`/tmp/o_${i}.jpg`,type:'jpeg',quality:88})}await b.close();return}
const D=await p.evaluate(()=>window.DUR);const t0=Date.now();
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out+'.tmp.mp4']);
const N=Math.round(D*30);let F0=0,F1=N;if(RANGE){const [k,n]=RANGE.split('/').map(Number);F0=Math.floor(N*k/n);F1=Math.floor(N*(k+1)/n)}console.log('frames',F0,F1,'of',N);for(let f=F0;f<F1;f++){await step(f/30);const img=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r));if(f%150===0)console.log('frame',f,'/',N,((Date.now()-t0)/1000|0)+'s')}
ff.stdin.end();await new Promise(r=>ff.on('close',c=>{if(c===0)fs.renameSync(out+'.tmp.mp4',out);console.log('rendered',out,c);r()}));await b.close()})();
