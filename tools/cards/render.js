const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+process.cwd()+'/'+(process.env.PAGE||'c.html'));await p.waitForTimeout(800);
const ids=process.argv.slice(2).length?process.argv.slice(2):[...await p.$$eval('.k',e=>e.map(x=>x.id))];for(const id of ids){await (await p.$('#'+id)).screenshot({path:`out/${id}.jpg`,type:'jpeg',quality:90})}
await b.close()})();
