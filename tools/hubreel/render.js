const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,html,outdir,mode,cta,times]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
const errs=[];p.on('pageerror',e=>errs.push(String(e)));
await p.goto('file://'+html+'?cta='+(cta||'ig'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.evaluate(()=>window.measure&&window.measure());
const DUR=await p.evaluate(()=>window.DUR);fs.mkdirSync(outdir,{recursive:true});const N=Math.round(DUR*30);
const ts= mode==='check' ? times.split(',').map(Number) : Array.from({length:N},(_,i)=>i/30);
let i=0;for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${outdir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});i++;}
console.log('frames',ts.length,'errors',errs.length,errs.slice(0,3));await b.close();})();
