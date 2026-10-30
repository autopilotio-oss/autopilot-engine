const {chromium}=require('playwright');const {spawn}=require('child_process');
const [,,page,out,only,from,to]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('http://localhost:8777/film/'+page);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
if(only){const ts=only.split(',').map(Number);for(let i=0;i<ts.length;i++){await p.evaluate(t=>render(t),ts[i]);await p.waitForTimeout(60);await p.screenshot({path:`/tmp/f_${i}.jpg`,type:'jpeg',quality:85})}await b.close();return}
const D=await p.evaluate(()=>DUR);const a=+(from||0),z=+(to||D);
const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',out+'.tmp.mp4']);
for(let f=Math.round(a*30);f<Math.round(z*30);f++){await p.evaluate(t=>render(t),f/30);const img=await p.screenshot({type:'jpeg',quality:92});if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r))}
ff.stdin.end();ff.on('close',c=>{if(c===0)require('fs').renameSync(out+'.tmp.mp4',out);console.log('done',out,c)});await b.close()})();
