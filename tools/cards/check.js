// Layout check for poster cards: content must not run into the footer.
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+process.cwd()+'/'+(process.env.PAGE||'p.html'));await p.waitForTimeout(800);
const r=await p.$$eval('.k',ks=>ks.map(k=>{const ft=k.querySelector('.ft').getBoundingClientRect();const kb=k.getBoundingClientRect();let mx=0;
[...k.children].filter(c=>!c.classList.contains('ft')).forEach(c=>mx=Math.max(mx,c.getBoundingClientRect().bottom));
return k.id+' gap='+Math.round(ft.top-mx)+' footer_inside='+(ft.bottom<=kb.bottom)}));
console.log(r.join('\n'));await b.close()})();
