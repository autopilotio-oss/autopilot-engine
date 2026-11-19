const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,html,outdir,mode,cta]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+html+'?cta='+(cta||'ig'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const DUR=await p.evaluate(()=>window.DUR);fs.mkdirSync(outdir,{recursive:true});
const N=Math.round(DUR*30);
const ts= mode==='check' ? [0,0.6,1.5,2.3,3.4,5.0,6.5,7.6,9.3,10.9,11.7,12.6,13.6,14.5,14.75,(N-1)/30] : Array.from({length:N},(_,i)=>i/30);
let i=0;for(const t of ts){await p.evaluate(t=>render(t),t);await p.screenshot({path:`${outdir}/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:93});i++;}
console.log('frames',ts.length,'dur',DUR);await b.close();})();
