const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
const name=process.argv[2],only=process.argv[3];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/'+name+'.html');await p.waitForFunction('window.ready');await p.waitForTimeout(400);
if(only){const ts=only.split(',').map(Number);for(let i=0;i<ts.length;i++){await p.evaluate(async t=>{render(t);await document.getElementById('pf').decode()},ts[i]);await p.screenshot({path:`/tmp/${name}_${i}.jpg`,type:'jpeg',quality:85})}await b.close();return}
const D=JSON.parse(fs.readFileSync(name+'.meta.json')).dur,F=30,N=Math.round(D*F);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+F,'-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',name+'_silent.mp4']);
for(let i=0;i<N;i++){await p.evaluate(async t=>{render(t);await document.getElementById('pf').decode()},i/F);const buf=await p.screenshot({type:'jpeg',quality:92});
 if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done',name)})();
