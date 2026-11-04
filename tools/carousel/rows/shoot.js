// node shoot.js out.png width height url
const {chromium}=require('playwright');(async()=>{const [o,w,h,u]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+h}});p.on('pageerror',e=>{console.error(e.message);process.exit(1)});
await p.goto(u);await p.waitForFunction('window.READY',null,{timeout:20000});await p.waitForTimeout(300);
await p.screenshot({path:o,type:o.endsWith('.jpg')?'jpeg':'png',...(o.endsWith('.jpg')?{quality:94}:{})});
console.log('fit',await p.evaluate(()=>window.FIT||0));await b.close()})();
