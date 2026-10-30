// Renders the v2 (lime + black studio style) carousels: node r2.js [key]
const {chromium}=require('playwright');const fs=require('fs');(async()=>{const D=fs.readFileSync('data2.json','utf8');const only=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
p.on('pageerror',e=>console.log('ERR',e.message));
for(const key of Object.keys(JSON.parse(D))){if(only&&key!==only)continue;fs.writeFileSync('_t.html',fs.readFileSync('t2.html','utf8').replace('__DATA__',D).replace('__KEY__',JSON.stringify(key)));
 await p.goto('file://'+process.cwd()+'/_t.html');await p.waitForTimeout(800);const n=await p.$$eval('.k',e=>e.length);fs.mkdirSync('out/'+key,{recursive:true});
 for(let i=1;i<=n;i++)await (await p.$('#s'+i)).screenshot({path:`out/${key}/${i}.jpg`,type:'jpeg',quality:92});console.log(key,n)}
await b.close()})();
