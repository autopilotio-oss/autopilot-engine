// node tools/series/rend.js <page relative to tools/> <out.mp4|x> [t1,t2..]   (needs: python3 -m http.server 8777 in tools/)
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const [,,page,out,only]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://localhost:8777/'+page);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
if(only){const ts=only.split(',').map(Number);for(let i=0;i<ts.length;i++){await p.evaluate(t=>render(t),ts[i]);await p.waitForTimeout(40);await p.screenshot({path:`/tmp/s_${i}.jpg`,type:'jpeg',quality:85})}await b.close();return}
const D=await p.evaluate(()=>DUR);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',out+'.tmp.mp4']);
for(let f=0;f<Math.round(D*30);f++){await p.evaluate(t=>render(t),f/30);const img=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r))}
ff.stdin.end();ff.on('close',c=>{if(c===0)fs.renameSync(out+'.tmp.mp4',out);console.log('rendered',out,c)});await b.close()})();
