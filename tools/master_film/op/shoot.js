const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1200,height:1600}});p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>console.log('C',m.text()));
await p.goto('http://localhost:8778/tools/master_film/op/pose.html');await p.waitForFunction(()=>window.READY===1,null,{timeout:120000});
const poses=JSON.parse(process.argv[2]);for(const [name,pz] of Object.entries(poses)){await p.evaluate(pz=>window.pose(pz),pz);await p.waitForTimeout(300);await p.screenshot({path:`/home/claude/autopilot-engine/tools/master_film/op/${name}.png`,omitBackground:true})}
await b.close()})();
