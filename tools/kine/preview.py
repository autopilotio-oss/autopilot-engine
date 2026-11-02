"""Composited still frames for checking layout: python3 tools/kine/preview.py <stem> t1,t2,... -> /tmp/pv_<i>.jpg + /tmp/pv_sheet.jpg"""
import sys, json, subprocess, os
D = os.path.dirname(os.path.abspath(__file__)); ep, ts = sys.argv[1], [float(x) for x in sys.argv[2].split(",")]
M = json.load(open(f"{D}/out/{ep}.meta.json"))
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch({{args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']}});const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
p.on('pageerror',e=>console.log('ERR',e.message));await p.goto('http://localhost:8778/tools/kine/out/{ep}.html?alpha');await p.waitForFunction(()=>window.READY===1);
const ts={json.dumps(ts)};for(let i=0;i<ts.length;i++){{await p.evaluate(t=>window.render(t),ts[i]);await p.screenshot({{path:'/tmp/pva_'+i+'.png',omitBackground:true}})}}await b.close()}})();"""
open("/tmp/pv.js", "w").write(js); subprocess.run(["node", "/tmp/pv.js"], check=True, env={**os.environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"]).decode().strip()})
outs = []
for i, t in enumerate(ts):
    pl = next(p for p in M["plates"] if p["s"] <= t < p["e"] + .001)
    ct = pl["off"] + (t - pl["s"]) * pl["rate"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(min(ct, 4.95)), "-i", f"{D}/plates/{pl['plate']}.mp4", "-i", f"/tmp/pva_{i}.png",
                    "-filter_complex", "[0:v][1:v]overlay=0:0", "-frames:v", "1", f"/tmp/pv_{i}.jpg"], check=True); outs.append(f"/tmp/pv_{i}.jpg")
from PIL import Image
ims = [Image.open(o).resize((270, 480)) for o in outs]; n = len(ims); cols = min(n, 7); rows = -(-n // cols)
sh = Image.new("RGB", (270 * cols, 480 * rows)); [sh.paste(im, ((i % cols) * 270, (i // cols) * 480)) for i, im in enumerate(ims)]; sh.save("/tmp/pv_sheet.jpg", quality=85); print("sheet", n)
