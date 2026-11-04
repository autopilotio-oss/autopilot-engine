"""AUTOPILOT.OI site v2: home, /marketplace, /workspace (software), redirects. python3 tools/site/build.py
Product pages (/store/<slug>, /office-autopilot) stay where they are; this only builds the top level pages."""
import os, html
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); D = f"{ROOT}/docs"
e = html.escape; GR = "https://autopilotoi.gumroad.com/l/"
def head(title, desc, path, img="autopilot-cover.png"):  # share image: the product the page sells
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="https://autopilotoi.app{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="https://autopilotoi.app/store/{img}">
<meta name="theme-color" content="#0a0a0a"><link rel="icon" href="/logo-128.png">
<link rel="preload" href="/assets/fonts/APWide-Black.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=4"></head><body>"""
def nav(on):
    a = lambda href, t, k, c="": f'<a href="{href}" class="{c}{" on" if k == on else ""}">{t}</a>'
    return f'<div class="nav"><div class="wrap"><a class="brand" href="/"><span class="eyes"><i></i><i></i></span>AUTOPILOT.OI</a><div class="links">{a("/front-desk/", "Front Desk", "f", "hm")}{a("/brain/", "Free starter", "c")}{a("/#agents", "Agents", "m", "hm")}{a(GR + "owner-toolkit", "All 4 · $24", "x", "cta buy")}</div></div></div>'
FOOT = """<div class="foot"><div class="wrap"><div class="big">AUTOPILOT<span>.</span>OI</div>
<div><div>Simple AI helpers for business owners.<br>Independent. Not affiliated with Anthropic. Claude is a product of Anthropic.</div>
<div style="display:flex;gap:18px;flex-wrap:wrap"><a href="/marketplace/">Marketplace</a><a href="/front-desk/">Front Desk</a><a href="/workspace/">Workspace</a><a href="/brain/">Free starter</a><a href="/library/">Library</a><a href="https://www.instagram.com/autopilot.oi/">Instagram</a></div></div></div></div>
<script src="/assets/ap.js" defer></script></body></html>"""
def redirect(path, to):
    os.makedirs(f"{D}{path}", exist_ok=True)
    open(f"{D}{path}index.html", "w").write(f'<!DOCTYPE html><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="https://autopilotoi.app{to}"><meta http-equiv="refresh" content="0; url={to}"><script>location.replace("{to}"+location.search)</script><a href="{to}">Continue</a>')
def write(path, s): os.makedirs(f"{D}{path}", exist_ok=True); open(f"{D}{path}index.html", "w").write(s)

INBOX = """<div class="ui"><div class="bar"><span>Leads · today</span><span>Product preview</span></div>
<div class="row"><div class="av">DR</div><div class="t"><b>Dana R.</b><span>How much for a full detail on an SUV? Free Saturday?</span></div><span class="st g">REPLIED 0:48</span></div>
<div class="row"><div class="av">MT</div><div class="t"><b>Mark T.</b><span>Ceramic coating, 2022 Tacoma</span></div><span class="st g">QUOTE READY</span></div>
<div class="row"><div class="av">PS</div><div class="t"><b>Priya S.</b><span>Quote sent Tuesday, no reply</span></div><span class="st">FOLLOW UP · DAY 2</span></div>
<div class="draft"><div class="label" style="margin-bottom:10px">DRAFT FOR DANA · WAITING FOR YOU</div><div class="msg">How much for a full detail on an SUV? Free Saturday?</div>
<div class="dr">A full SUV detail is $250, about 3 hours, and we come to you. I have Saturday at 9 or 1. Want me to hold one?</div><div class="acts"><span>Edit</span><span class="ok">Approve & send</span></div></div>
<div class="label" style="margin-top:12px;text-align:center">Example business. Workspace is in development.</div></div>"""

TOOLS = [
 ("Invoice Chaser", "9.99", "invoice-chaser", "Unpaid invoices", "Turns your job notes into a clean invoice, keeps a list of who owes you, and writes the right reminder for how late they are.", "chase Dave"),
 ("Review Desk", "9.99", "review-desk", "Ignored reviews", "Writes a reply to every review in your voice, good or angry, plus the text that asks happy customers for a new one.", "reply"),
 ("Bookkeeping Sorter", "9.99", "bookkeeping-sorter", "Messy receipts", "Upload a bank statement and every charge lands in a category with monthly totals for your accountant. It asks when it isn't sure.", "sort"),
 ("Content Week", "9.99", "content-week", "Nothing to post", "Answer 5 questions on Sunday. Get 7 posts for the week: what to shoot, the caption and the hashtags.", "week"),
]
def agent_rows():
    return "".join(f'''<div class="ag"><div class="ag-n">0{i}</div><div class="ag-p"><span class="ag-l">Problem</span><h3>{e(pb)}</h3></div><div class="ag-d"><span class="ag-l">The agent</span><b>{e(n)}</b><p>{e(d)}</p><span class="ag-t">You type <code>{e(cmd)}</code></span></div><div class="ag-b"><div class="ag-pr">${p}</div><a class="b5 buy" href="{GR}{perm}">Get it</a></div></div>''' for i, (n, p, perm, pb, d, cmd) in enumerate(TOOLS, 1))
SAMPLES = [("Review Desk", "reply", "Thanks so much, Jen! Glad the SUV came out spotless. See you next time. Mike, Northside Detail"),
           ("Content Week", "week", "Mon: before and after of the Tacoma\nTue: 15 second tip, pet hair\nWed: behind the scenes, 6 AM setup\nThu: customer story\nFri: open slots this weekend")]
FAQ = [("Is it a subscription?", "No. You pay once and keep it. No monthly fee from us."),
       ("Do I need tech skills?", "No. You copy one message into Claude and answer a few questions. The guide shows every tap."),
       ("Do I have to pay for Claude?", "No. Every agent works on Claude's free plan."),
       ("What do I get?", "A PDF guide with the setup message, a worked example and a cheat sheet. Instant download after checkout."),
       ("Does it send anything for me?", "No. Everything is a draft. You read it and send it yourself."),
       ("What if it doesn't help?", "Reply to your receipt within 30 days for a full refund.")]
V5 = """<style>
body.v5{--pp:#ecece7;--wh:#f8f8f4;--ik:#0b0b0b;--rl:rgba(11,11,11,.14);--mt:#5d5d56;background:var(--pp);color:var(--ik)}
.v5 .nav{background:#ecece7;-webkit-backdrop-filter:none;backdrop-filter:none;border-bottom:1.5px solid var(--ik)}.v5 .brand{color:var(--ik)}.v5 .brand .eyes{background:var(--ik)}.v5 .brand .eyes i{box-shadow:none}
.v5 .nav .links{color:var(--mt)}.v5 .nav .links a:hover{color:var(--ik)}.v5 .nav .links .cta,.v5 .nav .links .cta:hover{background:var(--ik);color:#fff;border-radius:6px}
.v5 .w5,.v5 .wrap{max-width:1240px;margin:0 auto;padding:0 24px}
.v5 .lab{font:600 12px/1 var(--T);letter-spacing:.16em;text-transform:uppercase;color:var(--mt)}
.v5 h1,.v5 h2{color:var(--ik)}.v5 h1 em,.v5 h2 em{color:var(--ik);font-style:normal;background:var(--l);padding:0 .08em;margin:0 -.08em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.b5{display:inline-flex;align-items:center;justify-content:center;height:54px;padding:0 26px;border-radius:6px;font:700 16px var(--T);background:var(--ik);color:#fff;border:1.5px solid var(--ik);white-space:nowrap;transition:background .15s,color .15s}
.b5:hover{background:var(--l);color:var(--ik)}.b5.o{background:transparent;color:var(--ik)}.b5.o:hover{background:var(--ik);color:#fff}.b5.l{background:var(--l);color:var(--ik);border-color:var(--l)}.b5.l:hover{background:#fff;border-color:#fff}
/* hero */
.hx{position:relative;border-bottom:1.5px solid var(--ik)}.hx .h5{border-bottom:0}
.lava-page{position:fixed;left:0;top:0;width:100%;height:100vh;height:100lvh;z-index:-1;pointer-events:none;display:block;background:var(--pp)}
html{background:#ecece7}body.v5{background:transparent!important}
.hx .b5.o{background:#fff}.hx .b5.o:hover{background:var(--ik);color:#fff}
.lx{position:relative;border-radius:6px;border:1.5px solid var(--ik);padding:46px;margin-top:40px}

.lc{margin-top:44px;padding:64px 46px}.lci{position:relative;z-index:1;display:inline-block;max-width:640px}
.lc h3{font:400 clamp(30px,4.4vw,58px)/.95 var(--W);text-transform:uppercase;letter-spacing:-.025em}.lc p{margin:14px 0 24px;font:600 17px var(--T)}
.lcb{display:flex;gap:10px;flex-wrap:wrap}.lc .b5.o{background:#fff}
@media(max-width:720px){.h5 h1{font-size:clamp(32px,9.4vw,40px);margin:14px 0 16px}.h5 .lead{font-size:16px}.hx .h5{padding:26px 0 36px}.trust{margin-top:18px}.lx{padding:22px}.lc{padding:40px 22px}}
.h5{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(320px,.8fr);gap:56px;align-items:center;padding:64px 0 56px;border-bottom:1.5px solid var(--ik)}
.h5 h1{font-size:clamp(38px,5.6vw,82px);line-height:.93;margin:20px 0 26px}
.h5 .lead{color:#33332e;max-width:600px}
.h5 .row{margin-top:32px;gap:10px}
.trust{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:26px;font:600 14px var(--T);color:var(--ik)}.trust span:before{content:"✓";margin-right:7px;font-weight:700}
.rc{background:var(--wh);border:1.5px solid var(--ik);border-radius:4px;padding:22px 22px 18px;font:500 14.5px/1.45 var(--T);box-shadow:8px 8px 0 var(--ik)}
.rc .rh{display:flex;justify-content:space-between;font:700 12px var(--T);letter-spacing:.14em;text-transform:uppercase;padding-bottom:12px;border-bottom:1.5px dashed var(--ik)}
.rc .me{margin:14px 0 10px;font:600 14px ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--mt)}
.rc .r{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px dotted rgba(11,11,11,.35);font-variant-numeric:tabular-nums}
.rc .tt{display:flex;justify-content:space-between;padding:10px 0 2px;font-weight:700;border-top:1.5px solid var(--ik);margin-top:6px}
.rc .q{margin-top:12px;background:var(--l);padding:9px 11px;border-radius:3px;font-weight:600;font-size:14px}
.rc .ft{margin-top:12px;font-size:12px;color:var(--mt)}
.tk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.tk>div{border:1.5px solid var(--ik);border-radius:4px;padding:30px;background:var(--wh)}.tk h3{font:400 clamp(22px,2.2vw,30px)/1.02 var(--W);text-transform:uppercase;letter-spacing:-.02em;margin:12px 0 14px}.tk p{color:#33332e;margin:0 0 14px;font-size:15.5px}.tk ul{list-style:none;padding:0;margin:0;display:grid;gap:11px}.tk li{padding-left:22px;position:relative;font-size:15.5px;line-height:1.45;color:#22221e}.tk li:before{content:"";position:absolute;left:0;top:.45em;width:10px;height:10px;background:var(--l);border:1.5px solid var(--ik);border-radius:2px}.tk li b{font-weight:700;color:var(--ik)}
@media(max-width:1000px){.tk{grid-template-columns:1fr}.tk>div{padding:24px}}
/* How we work: dark band that pops */
.dk{position:relative;background:#0b0b0b;color:#f2f2ee;overflow:hidden;isolation:isolate;border-bottom:1.5px solid var(--ik)}
.dk .w5{position:relative;z-index:1}
.dk-glow{position:absolute;inset:-20%;z-index:0;pointer-events:none;background:radial-gradient(520px 420px at var(--mx,70%) var(--my,30%),rgba(212,255,58,.16),transparent 70%),radial-gradient(700px 500px at 10% 110%,rgba(212,255,58,.07),transparent 70%);transition:background .2s}
@media(pointer:fine){html.fx .dk-glow{animation:dkdrift 14s ease-in-out infinite alternate}}
@keyframes dkdrift{0%{transform:translate3d(-3%,0,0)}100%{transform:translate3d(3%,4%,0)}}
.dk .lab{color:#9a9b92}.dk h2{color:#fff}.dk .sh5 p{color:#c9c9c2}
.dk h2 em{color:#0b0b0b}
html.fx .dk .sh5 h2 em{background:linear-gradient(var(--l),var(--l)) no-repeat 0 0/0% 100%;transition:background-size .9s cubic-bezier(.7,0,.2,1) .35s}
html.fx .dk .sh5.in h2 em{background-size:100% 100%}
.dk .tk{perspective:1200px}
.dk .tk>div{position:relative;background:linear-gradient(180deg,#151515,#0f0f0f);border:1px solid #2a2a27;border-radius:10px;padding:32px 30px 30px;overflow:hidden;transition:transform .5s cubic-bezier(.2,.8,.2,1),border-color .4s,box-shadow .5s}
.dk .tk>div:before{content:"";position:absolute;left:0;top:0;height:3px;width:100%;background:var(--l);transform:scaleX(0);transform-origin:0 50%;transition:transform 1s cubic-bezier(.7,0,.2,1) .25s}
.dk .tk>div.in:before,html:not(.fx) .dk .tk>div:before{transform:scaleX(1)}
.dk .tk>div:hover{transform:translateY(-8px);border-color:rgba(212,255,58,.55);box-shadow:0 30px 70px -30px rgba(212,255,58,.35)}
.dk .tk h3{color:#fff}.dk .tk p{color:#bdbdb5}.dk .tk li{color:#dcdcd5}.dk .tk li b{color:var(--l)}
.dk .tk li:before{background:transparent;border:1.5px solid var(--l);transition:background .35s}
.dk .tk li:after{content:"";position:absolute;left:3.5px;top:.45em;margin-top:1.5px;width:3.5px;height:6px;border:solid #0b0b0b;border-width:0 2px 2px 0;transform:rotate(45deg) scale(0);transition:transform .3s cubic-bezier(.3,1.6,.5,1)}
.dk .tk>div.in li:before,html:not(.fx) .dk .tk li:before{background:var(--l)}
.dk .tk>div.in li:after,html:not(.fx) .dk .tk li:after{transform:rotate(45deg) scale(1)}
html.fx .dk [data-r].tk>div,html.fx .dk .tk>[data-r]{transform:translateY(60px) rotateX(14deg);transform-origin:50% 100%}
html.fx .dk .tk>[data-r].in{transform:none}
html.fx .dk .tk li{opacity:0;transform:translateX(-14px);transition:opacity .5s,transform .6s cubic-bezier(.2,.8,.2,1)}
html.fx .dk .tk>div.in li{opacity:1;transform:none}
html.fx .dk .tk>div.in li:nth-child(1),html.fx .dk .tk>div.in li:nth-child(1):before,html.fx .dk .tk>div.in li:nth-child(1):after{transition-delay:0.45s}
html.fx .dk .tk>div.in li:nth-child(2),html.fx .dk .tk>div.in li:nth-child(2):before,html.fx .dk .tk>div.in li:nth-child(2):after{transition-delay:0.61s}
html.fx .dk .tk>div.in li:nth-child(3),html.fx .dk .tk>div.in li:nth-child(3):before,html.fx .dk .tk>div.in li:nth-child(3):after{transition-delay:0.77s}
html.fx .dk .tk>div.in li:nth-child(4),html.fx .dk .tk>div.in li:nth-child(4):before,html.fx .dk .tk>div.in li:nth-child(4):after{transition-delay:0.93s}
html.fx .dk .tk>div.in li:nth-child(5),html.fx .dk .tk>div.in li:nth-child(5):before,html.fx .dk .tk>div.in li:nth-child(5):after{transition-delay:1.09s}
/* the "no" card: each reason gets crossed out like a decision made */
.dk .tk>.no li:before{border-color:#6d6d66}.dk .tk>.no.in li:before,html:not(.fx) .dk .tk>.no li:before{background:#2a2a27}
.dk .tk>.no li:after{left:2px;top:.45em;margin-top:5px;width:9px;height:0;border:0;border-top:2px solid var(--l);transform:rotate(-45deg) scale(0)}
.dk .tk>.no.in li:after,html:not(.fx) .dk .tk>.no li:after{transform:rotate(-45deg) scale(1)}
/* the first week card: a timeline that draws itself */
.dk .tl ul{position:relative;gap:16px}
.dk .tl ul:before{content:"";position:absolute;left:5px;top:10px;bottom:10px;width:2px;background:linear-gradient(var(--l),rgba(212,255,58,.15));transform:scaleY(0);transform-origin:50% 0;transition:transform 1.4s cubic-bezier(.7,0,.2,1) .45s}
.dk .tl.in ul:before,html:not(.fx) .dk .tl ul:before{transform:scaleY(1)}
.dk .tl li:before{border-radius:50%;box-shadow:0 0 0 4px #121212}
.dk .tl.in li:before{animation:dkpulse 2.4s ease-out infinite}
.dk .tl li:nth-child(2):before{animation-delay:.6s!important}.dk .tl li:nth-child(3):before{animation-delay:1.2s!important}.dk .tl li:nth-child(4):before{animation-delay:1.8s!important}
@keyframes dkpulse{0%{box-shadow:0 0 0 4px #121212,0 0 0 4px rgba(212,255,58,.5)}70%{box-shadow:0 0 0 4px #121212,0 0 0 14px rgba(212,255,58,0)}100%{box-shadow:0 0 0 4px #121212,0 0 0 14px rgba(212,255,58,0)}}
@media(prefers-reduced-motion:reduce){.dk-glow,.dk .tl li:before{animation:none!important}}
/* section heads */
.s5{padding:88px 0;border-bottom:1.5px solid var(--ik)}
.sh5{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:32px;align-items:end;margin-bottom:44px}
.sh5 h2{font-size:clamp(30px,4.6vw,62px);line-height:.95;margin-top:16px}.sh5 p{font-size:18px;color:#33332e;max-width:460px;justify-self:end}
/* agents price list */
.ags{border-top:1.5px solid var(--ik)}
.ag{display:grid;grid-template-columns:56px minmax(0,1.05fr) minmax(0,1.5fr) 190px;gap:28px;align-items:start;padding:30px 0;border-bottom:1px solid var(--rl)}
.ag-n{font:400 22px/1 var(--W);padding-top:22px}
.ag-l{display:block;font:600 11.5px var(--T);letter-spacing:.16em;text-transform:uppercase;color:var(--mt);margin-bottom:10px}
.ag-p h3{font:400 clamp(24px,2.6vw,36px)/1 var(--W);text-transform:uppercase;letter-spacing:-.02em}
.ag-d b{font:700 18px var(--T)}.ag-d p{margin:6px 0 10px;color:#33332e;font-size:15.5px;max-width:520px}
.ag-t{font:500 14px var(--T);color:var(--mt)}.ag-t code{font:700 13.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--ik);color:var(--l);padding:3px 7px;border-radius:3px;margin-left:4px}
.ag-b{display:flex;flex-direction:column;align-items:stretch;gap:12px;padding-top:16px}.ag-pr{font:400 34px/1 var(--W);letter-spacing:-.02em;text-align:right}
/* bundle */
.bd{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:center;background:var(--ik);color:#f3f3ef;border-radius:4px;padding:48px;margin-top:40px}
.bd .lab{color:#a2a39a}.bd h3{font:400 clamp(30px,4vw,56px)/.95 var(--W);text-transform:uppercase;letter-spacing:-.025em;margin:14px 0 16px}.bd p{color:#c9c9c2;max-width:480px}
.bd .px{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}.bd .px s{font:400 28px var(--W);color:#7b7b74}.bd .px b{font:400 clamp(56px,7vw,96px)/1 var(--W);color:var(--l);letter-spacing:-.03em}
.bd .sv{display:inline-block;margin:10px 0 22px;font:700 14px var(--T);background:var(--l);color:var(--ik);padding:6px 10px;border-radius:3px}
.bd .b5{width:100%}
.fd{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;margin-top:18px;padding:22px 0;border-top:1px solid var(--rl);border-bottom:1px solid var(--rl);font-size:16px}
.fd b{font-weight:700}.fd a{font-weight:700;text-decoration:underline;text-underline-offset:4px}
/* samples */
.sp{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}.sp>*{min-width:0}
.sm{background:var(--wh);border:1.5px solid var(--ik);border-radius:4px;display:flex;flex-direction:column}
.sm .sh{display:flex;justify-content:space-between;gap:10px;padding:14px 18px;border-bottom:1.5px solid var(--ik);font:700 12px var(--T);letter-spacing:.12em;text-transform:uppercase}
.sm .sh code{font:700 12.5px ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:0;text-transform:none;background:var(--ik);color:var(--l);padding:2px 6px;border-radius:3px}
.sm pre{white-space:pre-wrap;font:500 15.5px/1.55 var(--T);padding:20px 18px;margin:0;flex:1}.sm .ex{padding:0 18px 14px;font-size:12px;color:var(--mt)}
/* steps */
.st5{display:grid;grid-template-columns:repeat(3,1fr);border-top:1.5px solid var(--ik)}
.st5>div{padding:28px 28px 8px 0}.st5>div+div{padding-left:28px;border-left:1px solid var(--rl)}
.st5 b{display:block;font:400 56px/1 var(--W);margin-bottom:22px}.st5 h3{font:700 20px var(--T)}.st5 p{color:#33332e;margin-top:6px}
/* try + guarantee */
.tg{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:20px}
.tg>div{border:1.5px solid var(--ik);border-radius:4px;padding:34px;background:var(--wh)}
.tg h3{font:400 clamp(26px,2.8vw,38px)/1 var(--W);text-transform:uppercase;letter-spacing:-.02em;margin:14px 0 14px}
.tg .cp5{margin-top:18px;background:var(--pp);border:1.5px dashed var(--ik);border-radius:4px;padding:16px;white-space:pre-wrap;font:500 14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace}
.tg .gu{background:var(--l);display:flex;flex-direction:column}.tg .gu p{font-size:18px;max-width:400px}.tg .gu ul{list-style:none;margin:22px 0 28px;display:flex;flex-direction:column;gap:10px;font:600 16px var(--T)}.tg .gu li:before{content:"✓";margin-right:9px}.tg .gu .b5{margin-top:auto;align-self:flex-start}
/* faq */
.fq{display:grid;grid-template-columns:repeat(3,1fr);gap:0 36px;border-top:1.5px solid var(--ik)}
.fq>div{padding:24px 0;border-bottom:1px solid var(--rl)}.fq h3{font:700 17.5px var(--T)}.fq p{color:#33332e;margin-top:8px;font-size:15.5px}
/* footer on paper */
.v5 .foot{border-top:0;color:var(--mt);background:var(--ik);color:#9c9c95}.v5 .foot .big{color:#f3f3ef}
/* sticky buy bar (phones) */
.sb{position:fixed;left:0;right:0;bottom:0;z-index:30;display:none;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px calc(12px + env(safe-area-inset-bottom));background:var(--ik);color:#fff;transform:translateY(110%);transition:transform .25s}
.sb.on{transform:none}.sb b{font:400 18px var(--W)}.sb span{display:block;font-size:12.5px;color:#a2a39a}.sb .b5{height:46px;padding:0 18px}
@media(max-width:1000px){.h5{grid-template-columns:1fr;align-items:start}.rc{max-width:440px}.ag{grid-template-columns:44px minmax(0,1fr) 150px;}.ag-d{grid-column:2/4}.ag-b{grid-column:3;grid-row:1}.ag-p{grid-column:2}
 .sp{grid-template-columns:1fr}.fq{grid-template-columns:1fr 1fr}.bd{grid-template-columns:1fr;padding:34px}}
@media(max-width:720px){.sh5{grid-template-columns:1fr;gap:16px}.sh5 p{justify-self:start}.s5{padding:64px 0}.h5{padding:40px 0 44px}
 .ag{grid-template-columns:1fr;gap:14px;padding:26px 0}.ag-n{padding:0;font-size:16px;color:var(--mt)}.ag-p,.ag-d,.ag-b{grid-column:auto;grid-row:auto}.ag-b{flex-direction:row;align-items:center;justify-content:space-between;padding:0}.ag-b .b5{flex:0 0 160px}.ag-pr{text-align:left}
 .st5{grid-template-columns:1fr}.st5>div,.st5>div+div{padding:24px 0;border-left:0;border-bottom:1px solid var(--rl)}.st5 b{font-size:40px;margin-bottom:12px}
 .tg{grid-template-columns:1fr}.tg>div{padding:24px}.fq{grid-template-columns:1fr}.sb{display:flex}.v5 .foot{padding-bottom:110px}.h5 .row .b5{flex:1 1 100%}.bd{padding:26px}.rc{box-shadow:5px 5px 0 var(--ik)}}
/* phone mockup: original frame drawn in CSS */
.pw{display:flex;flex-direction:column;align-items:center;gap:14px;justify-self:center}
.ph{position:relative;width:318px;aspect-ratio:9/19.4;border-radius:56px;padding:11px;background:linear-gradient(145deg,#4a3a3e 0%,#1d1517 38%,#2e2326 62%,#120c0e 100%);box-shadow:0 0 0 1.5px #0b0b0b,inset 0 0 0 2px rgba(255,255,255,.08),0 40px 80px -20px rgba(11,11,11,.45),0 18px 30px -18px rgba(11,11,11,.5)}
.ph .bt{position:absolute;width:4px;border-radius:2px;background:#2a1f22}.ph .b1{left:-3px;top:118px;height:26px}.ph .b2{left:-3px;top:166px;height:52px}.ph .b3{left:-3px;top:228px;height:52px}.ph .b4{right:-3px;top:190px;height:84px}
.ph .scr{position:relative;height:100%;border-radius:46px;background:#0e0e0e;overflow:hidden;color:#f3f3ef;font:500 13px/1.4 var(--T);display:flex;flex-direction:column}
.ph .isl{position:absolute;top:11px;left:50%;transform:translateX(-50%);width:96px;height:28px;border-radius:20px;background:#000}
.ph .sbar{display:flex;justify-content:space-between;align-items:center;padding:16px 26px 0 30px;height:44px;font:700 14px var(--T)}
.ph .sig{display:flex;align-items:flex-end;gap:2px}.ph .sig i{width:3px;background:#f3f3ef;border-radius:1px}.ph .sig i:nth-child(1){height:4px}.ph .sig i:nth-child(2){height:6px}.ph .sig i:nth-child(3){height:8px}.ph .sig i:nth-child(4){height:10px}.ph .sig b{width:22px;height:11px;border:1.5px solid #f3f3ef;border-radius:3px;margin-left:5px;position:relative}.ph .sig b:after{content:"";position:absolute;inset:1.5px;right:5px;background:#f3f3ef;border-radius:1px}
.ph .ah{display:flex;align-items:center;gap:10px;padding:14px 16px 12px;border-bottom:1px solid #222}.ph .av{width:30px;height:30px;border-radius:50%;background:var(--l);color:#0b0b0b;display:flex;align-items:center;justify-content:center;font:400 14px var(--W)}
.ph .ah b{display:block;font:700 13.5px var(--T)}.ph .ah span{font-size:11px;color:#8d8d86}
.ph .chat{flex:1;display:flex;flex-direction:column;gap:8px;padding:14px 12px;overflow:hidden}
.ph .me{align-self:flex-end;background:#2a2a2a;border-radius:16px 16px 4px 16px;padding:8px 12px;max-width:80%;display:flex;flex-direction:column;gap:6px;font-weight:600}
.ph .fc{font:600 11px var(--T);background:#3a3a3a;border-radius:8px;padding:6px 8px;color:#d8d8d2}.ph .fc:before{content:"PDF  ";color:var(--l);font-weight:700}
.ph .bot{align-self:flex-start;background:#181818;border:1px solid #2a2a2a;border-radius:16px 16px 16px 4px;padding:10px 12px;width:88%}
.ph .bh{font:700 10.5px var(--T);letter-spacing:.14em;text-transform:uppercase;color:#8d8d86;margin-bottom:4px}
.ph .r{display:flex;justify-content:space-between;padding:3.5px 0;border-bottom:1px solid #242424;font-variant-numeric:tabular-nums}.ph .r.tt{border:0;font-weight:700;padding-top:6px}
.ph .q{background:var(--l);color:#0b0b0b;border:0;font-weight:600;width:auto;max-width:88%}
.ph .inp{margin:0 12px 10px;height:38px;border-radius:19px;background:#1d1d1d;display:flex;align-items:center;justify-content:space-between;padding:0 6px 0 14px;color:#77776f;font-size:12.5px}.ph .inp i{width:26px;height:26px;border-radius:50%;background:var(--l)}
.ph .hb{width:110px;height:4px;border-radius:2px;background:#f3f3ef;opacity:.85;margin:0 auto 9px}
.pcap{font-size:12.5px;color:var(--mt);text-align:center;max-width:300px}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

@media(max-width:1000px){.pw{justify-self:start}}@media(max-width:720px){.pw{justify-self:center;margin-top:8px}.ph{width:296px}}

/* wide device mockup: original frame drawn in CSS */
.tw{display:flex;flex-direction:column;align-items:center;gap:16px;margin:8px 0 0}
.tb{position:relative;width:min(100%,860px);aspect-ratio:1.42/1;border-radius:44px;padding:12px;background:linear-gradient(150deg,#d9d6cf 0%,#8f8b84 22%,#cfccc5 45%,#77736d 78%,#bdb9b2 100%);box-shadow:0 0 0 1.5px #0b0b0b,inset 0 0 0 2px rgba(255,255,255,.35),0 50px 90px -30px rgba(11,11,11,.45),0 20px 30px -20px rgba(11,11,11,.4)}
.tb .tk{position:absolute;height:4px;border-radius:2px;background:#8a867f}.tb .k1{top:-3px;right:14%;width:46px}.tb .k2{top:-3px;right:22%;width:46px}.tb .k3{right:-3px;top:22%;width:4px;height:60px}
.tb .tsc{height:100%;border-radius:34px;background:#0e0e0e;overflow:hidden;color:#f3f3ef;font:500 13.5px/1.4 var(--T);display:flex;flex-direction:column}
.tb .tsb{display:flex;justify-content:space-between;align-items:center;padding:12px 26px 6px;font:700 13px var(--T)}
.tb .sig{display:flex;align-items:flex-end;gap:2px}.tb .sig i{width:3px;background:#f3f3ef;border-radius:1px}.tb .sig i:nth-child(1){height:4px}.tb .sig i:nth-child(2){height:6px}.tb .sig i:nth-child(3){height:8px}.tb .sig i:nth-child(4){height:10px}.tb .sig b{width:22px;height:11px;border:1.5px solid #f3f3ef;border-radius:3px;margin-left:5px;position:relative}.tb .sig b:after{content:"";position:absolute;inset:1.5px;right:5px;background:#f3f3ef;border-radius:1px}
.tb .tgr{flex:1;display:grid;grid-template-columns:34% 1fr;min-height:0}
.tb .tsd{border-right:1px solid #222;padding:10px 12px;display:flex;flex-direction:column;gap:4px}.tb .tsh{font:700 10.5px var(--T);letter-spacing:.14em;text-transform:uppercase;color:#8d8d86;padding:6px 8px 8px}
.tb .ti{display:flex;align-items:center;gap:10px;padding:9px 8px;border-radius:12px}.tb .ti.on{background:#1f1f1f}.tb .ti b{display:block;font:700 13px var(--T)}.tb .ti span{font-size:11.5px;color:#8d8d86}
.tb .tav{flex:none;width:28px;height:28px;border-radius:50%;background:#2a2a2a;color:#f3f3ef;display:flex;align-items:center;justify-content:center;font:400 12px var(--W)}.tb .ti.on .tav{background:var(--l);color:#0b0b0b}
.tb .tmn{display:flex;flex-direction:column;min-width:0;min-height:0}.tb .tth{display:flex;justify-content:space-between;align-items:center;padding:10px 18px;border-bottom:1px solid #222}.tb .tth b{font:700 14px var(--T)}.tb .tth span{font-size:11.5px;color:#8d8d86}
.tb .tch{flex:1;display:flex;flex-direction:column;gap:8px;padding:12px 16px;overflow:hidden;min-height:0}
.tb .me{align-self:flex-end;background:#2a2a2a;border-radius:16px 16px 4px 16px;padding:7px 12px;font-weight:600}
.tb .bot{align-self:flex-start;background:#181818;border:1px solid #2a2a2a;border-radius:16px 16px 16px 4px;padding:9px 12px;width:92%}
.tb .bh{font:700 10px var(--T);letter-spacing:.14em;text-transform:uppercase;color:#8d8d86;margin-bottom:5px}
.tb .r{display:flex;justify-content:space-between;gap:10px;padding:3px 0;border-bottom:1px solid #242424;font-variant-numeric:tabular-nums}.tb .r.tt{border:0;font-weight:700}
.tb .dr{border-color:rgba(212,255,58,.55)}.tb .tac{display:flex;justify-content:flex-end;gap:8px;margin-top:9px}.tb .tac span{font:700 12px var(--T);padding:6px 12px;border-radius:9px;border:1px solid #333;color:#a2a39a}.tb .tac .ok{background:var(--l);border-color:var(--l);color:#0b0b0b}
.tb .inp{margin:0 16px 10px;height:36px;border-radius:18px;background:#1d1d1d;display:flex;align-items:center;justify-content:space-between;padding:0 6px 0 14px;color:#77776f;font-size:12.5px}.tb .inp i{width:24px;height:24px;border-radius:50%;background:var(--l)}
.tb .hb{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);width:140px;height:4px;border-radius:2px;background:#f3f3ef;opacity:.8}

@media(max-width:860px){.tb .tsd{display:none}.tb .tgr{grid-template-columns:1fr}.tb{border-radius:32px;padding:9px}.tb .tsc{border-radius:24px;font-size:11.5px}.tb .tch{padding:8px 10px;gap:6px}.tb .tth{padding:8px 12px}.tb .tsb{padding:9px 18px 4px}.tb .hb{bottom:14px;width:90px}.tb .bot{width:100%}.tb .inp{display:none}}
@media(max-width:520px){.tb{aspect-ratio:auto}.tb .tsc{min-height:420px}}
</style>"""
FX = r"""<style>
/* motion layer: only when JS runs and the visitor allows motion */
@media (prefers-reduced-motion:no-preference){
html.fx .h5 h1 .wd{display:inline-block;overflow:hidden;vertical-align:top;padding-bottom:.04em}
html.fx .h5 h1 .wd>span{display:inline-block;transform:translateY(105%);transition:transform .9s cubic-bezier(.2,.8,.2,1)}
html.fx .h5 h1.in .wd>span{transform:none}
html.fx .h5 h1 em{background-size:0% 100%;background-image:linear-gradient(var(--l),var(--l));background-repeat:no-repeat;background-color:transparent;transition:background-size .8s cubic-bezier(.7,0,.2,1) .9s}
html.fx .h5 h1.in em{background-size:100% 100%}
html.fx .h5 .lab,html.fx .h5 .lead,html.fx .h5 .row,html.fx .h5 .trust{opacity:0;transform:translateY(14px);transition:opacity .7s,transform .7s cubic-bezier(.2,.8,.2,1)}
html.fx .h5.in .lab{opacity:1;transform:none}html.fx .h5.in .lead{opacity:1;transform:none;transition-delay:.55s}html.fx .h5.in .row{opacity:1;transform:none;transition-delay:.7s}html.fx .h5.in .trust{opacity:1;transform:none;transition-delay:.85s}
html.fx .pw{opacity:0;transform:translateY(60px) rotate(4deg);transition:opacity 1s,transform 1.2s cubic-bezier(.2,.8,.2,1) .2s}
html.fx .h5.in .pw{opacity:1;transform:none}
html.fx .ph{transition:transform .35s cubic-bezier(.2,.8,.2,1);will-change:transform}
html.fx .pw.idle .ph{animation:flo 6s ease-in-out infinite}
@keyframes flo{50%{translate:0 -10px}}
html.fx [data-r]{opacity:0;transform:translateY(34px);transition:opacity .8s,transform .9s cubic-bezier(.2,.8,.2,1)}
html.fx [data-r].in{opacity:1;transform:none}
html.fx .tw .tb{transform:perspective(1400px) rotateX(var(--rx,24deg)) scale(var(--sc,.9));transform-origin:50% 100%;will-change:transform}
html.fx .bd .px s{position:relative;color:#7b7b74}html.fx .bd .px s{text-decoration:none}
html.fx .bd .px s:after{content:"";position:absolute;left:-4%;top:52%;height:4px;width:0;background:#ff5a36;transform:rotate(-8deg);transition:width .5s cubic-bezier(.7,0,.2,1) .5s}
html.fx .bd.in .px s:after{width:108%}
html.fx .bd .px b{display:inline-block;transform:scale(.4);opacity:0;transition:transform .7s cubic-bezier(.2,1.6,.4,1) 1s,opacity .3s 1s}
html.fx .bd.in .px b{transform:none;opacity:1}
html.fx .bd .sv{transform:translateX(-12px);opacity:0;transition:all .5s 1.4s}html.fx .bd.in .sv{transform:none;opacity:1}
html.fx .st5 b{background:linear-gradient(90deg,var(--ik) 50%,transparent 50%);background-size:200% 100%;background-position:100% 0;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-stroke:1.5px var(--ik);transition:background-position 1s cubic-bezier(.7,0,.2,1) .2s}
html.fx .st5>div.in b{background-position:0 0}
html.fx .m-h{display:none}
}
.ag{transition:background .25s,padding .25s}.ag:hover{background:var(--wh)}.ag .ag-n{transition:color .25s}.ag:hover .ag-n{color:#6f9800}
.ag:hover .ag-pr{animation:pop .5s}@keyframes pop{40%{transform:scale(1.08)}}
.b5{position:relative;overflow:hidden}.b5:after{content:"";position:absolute;top:0;bottom:0;left:-60%;width:40%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.45),transparent);transform:skewX(-20deg);transition:left .6s}
.b5:hover:after{left:130%}
.typ{align-self:flex-start;background:#181818;border:1px solid #2a2a2a;border-radius:16px 16px 16px 4px;padding:10px 12px;display:flex;gap:4px}
.typ i{width:6px;height:6px;border-radius:50%;background:#8d8d86;animation:dot 1s infinite}.typ i:nth-child(2){animation-delay:.15s}.typ i:nth-child(3){animation-delay:.3s}
@keyframes dot{30%{transform:translateY(-4px);background:var(--l)}}
.mi{animation:mi .45s cubic-bezier(.2,.8,.2,1) both}@keyframes mi{from{opacity:0;transform:translateY(10px) scale(.97)}}
.inp .tx{color:#f3f3ef}.inp .tx:after{content:"";display:inline-block;width:1.5px;height:1em;background:var(--l);margin-left:2px;vertical-align:-2px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.inp i.go{animation:sendp .4s}@keyframes sendp{50%{transform:scale(.8)}}
.ok.pl{animation:okp 1.2s 2}@keyframes okp{50%{box-shadow:0 0 0 6px rgba(212,255,58,.25)}}
</style>
<script>
(function(){
var R=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var D=document,H=D.documentElement;if(!R)H.classList.add('fx');
if(!R)Array.prototype.forEach.call(D.querySelectorAll('[data-m]'),function(m){if(!m.closest('.pw'))m.classList.add('m-h')});
function $(s,r){return (r||D).querySelector(s)}function $$(s,r){return Array.prototype.slice.call((r||D).querySelectorAll(s))}
var wait=function(ms){return new Promise(function(r){setTimeout(r,ms)})};
function money(n,dec){return '$'+(dec?n.toFixed(2):Math.round(n).toLocaleString('en-US'))}
function count(el,to,ms,from){var t0=null,f=from||0,dec=String(to).indexOf('.')>-1;function st(t){t0=t0||t;var k=Math.min(1,(t-t0)/ms),e=1-Math.pow(1-k,3);el.textContent=money(f+(to-f)*e,dec);if(k<1)requestAnimationFrame(st)}requestAnimationFrame(st)}
/* headline words */
var h1=$('.h5 h1');
if(h1&&!R){var n=0;(function wrap(node){$$('*',node);Array.prototype.slice.call(node.childNodes).forEach(function(c){if(c.nodeType===3){var f=D.createDocumentFragment();c.textContent.split(/(\s+)/).forEach(function(w){if(!w)return;if(/^\s+$/.test(w)){f.appendChild(D.createTextNode(w));return}var o=D.createElement('span');o.className='wd';var i=D.createElement('span');i.textContent=w;i.style.transitionDelay=(n++*0.07)+'s';o.appendChild(i);f.appendChild(o)});c.parentNode.replaceChild(f,c)}else if(c.nodeType===1)wrap(c)})})(h1)}
requestAnimationFrame(function(){requestAnimationFrame(function(){if(h1)h1.classList.add('in');var h5=$('.h5');if(h5)h5.classList.add('in');setTimeout(function(){var p=$('.pw');if(p)p.classList.add('idle')},2200)})});
/* tilt the hero phone toward the pointer */
var ph=$('.ph'),hz=$('.h5');
if(ph&&hz&&!R&&matchMedia('(pointer:fine)').matches){hz.addEventListener('mousemove',function(e){var b=ph.getBoundingClientRect(),x=(e.clientX-(b.left+b.width/2))/b.width,y=(e.clientY-(b.top+b.height/2))/b.height;ph.style.transform='perspective(1200px) rotateY('+(x*14).toFixed(2)+'deg) rotateX('+(-y*10).toFixed(2)+'deg)'});hz.addEventListener('mouseleave',function(){ph.style.transform=''})}
/* chat playback: type into the input, send, show typing dots, reply */
function play(box,loop){var chat=$(box.dataset.chat,box),inp=$('.inp span',box),btn=$('.inp i',box),steps=$$('[data-m]',chat);if(!chat||R)return;
 var ph0=inp?inp.textContent:'';
 function reset(){steps.forEach(function(s){s.classList.add('m-h');s.classList.remove('mi')});$$('.typ',chat).forEach(function(t){t.remove()})}
 async function run(){reset();await wait(150);
  for(var i=0;i<steps.length;i++){var s=steps[i];
   if(s.dataset.m==='me'){var w=s.dataset.w||s.textContent.trim();if(inp){inp.className='tx';inp.textContent='';for(var k=0;k<w.length;k++){inp.textContent+=w[k];await wait(70)}await wait(250);if(btn){btn.classList.remove('go');void btn.offsetWidth;btn.classList.add('go')}inp.className='';inp.textContent=ph0}
    s.classList.remove('m-h');s.classList.add('mi');await wait(450)}
   else{var t=D.createElement('div');t.className='typ mi';t.innerHTML='<i></i><i></i><i></i>';chat.insertBefore(t,s);await wait(900);t.remove();s.classList.remove('m-h');s.classList.add('mi');
    $$('[data-count]',s).forEach(function(c){count(c,parseFloat(c.dataset.count),900)});$$('.ok',s).forEach(function(o){o.classList.remove('pl');void o.offsetWidth;o.classList.add('pl')});await wait(700)}}
  if(loop){await wait(8000);run()}}
 run()}
if(!R){var hp=$('.pw');if(hp)setTimeout(function(){play(hp,true)},4200)}
/* scroll reveals with a stagger inside each group */
var groups=['.sh5','.ag','.bd','.fd','.tw','.sm','.st5>div','.tg>div','.tk>div','.fq>div'];
var els=[];groups.forEach(function(g){$$(g).forEach(function(el,i){el.setAttribute('data-r','');el.style.transitionDelay=Math.min(i,6)*0.08+'s';els.push(el)})});
if('IntersectionObserver' in window&&!R){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);
  if(e.target.classList.contains('tw'))setTimeout(function(){play(e.target,true)},400);
  if(e.target.classList.contains('bd')){var sv=$('.sv b',e.target);if(sv)setTimeout(function(){count(sv,15.96,900)},1400)}}})},{threshold:.18,rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else els.forEach(function(el){el.classList.add('in')});
/* How we work: lime spotlight follows the pointer, cards tilt toward it */
var dk=$('#why');
if(dk&&!R&&matchMedia('(pointer:fine)').matches){dk.addEventListener('pointermove',function(e){var b=dk.getBoundingClientRect();dk.style.setProperty('--mx',((e.clientX-b.left)/b.width*100+20/1.4).toFixed(1)+'%');dk.style.setProperty('--my',((e.clientY-b.top)/b.height*100+20/1.4).toFixed(1)+'%')});
 $$('.tk>div',dk).forEach(function(c){c.addEventListener('mousemove',function(e){var b=c.getBoundingClientRect(),x=(e.clientX-b.left)/b.width-.5,y=(e.clientY-b.top)/b.height-.5;c.style.transform='translateY(-8px) perspective(900px) rotateY('+(x*8).toFixed(2)+'deg) rotateX('+(-y*8).toFixed(2)+'deg)'});c.addEventListener('mouseleave',function(){c.style.transform=''})})}
/* the wide screen lifts flat as it scrolls into view */
var tw=$('.tw'),tb=tw&&$('.tb',tw);
if(tb&&!R){var tick=false;function upd(){tick=false;var r=tw.getBoundingClientRect(),vh=innerHeight,p=Math.max(0,Math.min(1,(vh-r.top)/(vh*0.8)));tb.style.setProperty('--rx',(24*(1-p)).toFixed(2)+'deg');tb.style.setProperty('--sc',(0.9+0.1*p).toFixed(3))}
 addEventListener('scroll',function(){if(!tick){tick=true;requestAnimationFrame(upd)}},{passive:true});upd()}
})();
</script>"""

def home():
    rows = agent_rows()
    samples = "".join(f'<div class="sm"><div class="sh"><span>{e(n)}</span><code>{e(c)}</code></div><pre>{e(t)}</pre><div class="ex">Example output for a sample business.</div></div>' for n, c, t in SAMPLES)
    faq = "".join(f"<div><h3>{e(q)}</h3><p>{e(a)}</p></div>" for q, a in FAQ)
    page = head("AUTOPILOT.OI · Easy set up AI agents for small business owners, $9.99", "Four AI agents for the jobs you put off: unpaid invoices, ignored reviews, messy receipts and nothing to post. $9.99 each or all 4 for $24. One payment, free Claude plan works, 30 day refund.", "/", "toolkit-cover.png") + nav("") + f"""
{V5}
<canvas class="lava-page" data-lava-page aria-hidden="true"></canvas><div class="hx"><div class="w5"><div class="h5"><div><div class="lab" data-lava-avoid>AI agents for small business owners</div>
<h1 data-lava-avoid>Easy set up AI agents that make your life <em>easier.</em></h1>
<p class="lead" data-lava-avoid>Four agents for the jobs you keep putting off: chasing invoices, answering reviews, sorting receipts and planning posts. $9.99 each. Set up in about 15 minutes, right on your phone.</p>
<div class="row" data-lava-avoid><a class="b5 buy" href="{GR}owner-toolkit">Get all 4 for $24</a><a class="b5 o" href="#agents">See each agent · $9.99</a></div>
<div class="trust" data-lava-avoid><span>One payment, no subscription</span><span>Free Claude plan works</span><span>Instant download</span><span>30 day refund</span></div></div>
<div class="pw" data-chat=".chat"><div class="ph" role="img" aria-label="Example on a phone: you type sort with your October statement and get every charge sorted with totals and one question">
<i class="bt b1"></i><i class="bt b2"></i><i class="bt b3"></i><i class="bt b4"></i>
<div class="scr" data-lava-avoid-front><div class="isl"></div><div class="sbar"><span>9:41</span><span class="sig"><i></i><i></i><i></i><i></i><b></b></span></div>
<div class="ah"><span class="av">B</span><div><b>Bookkeeping Sorter</b><span>Your agent · example</span></div></div>
<div class="chat"><div class="me" data-m="me" data-w="sort"><span class="fc">october.pdf</span>sort</div>
<div class="bot" data-m="bot"><div class="bh">October, sorted</div><div class="r"><span>Supplies</span><span>$612</span></div><div class="r"><span>Gas and car</span><span>$388</span></div><div class="r"><span>Advertising</span><span>$150</span></div><div class="r"><span>Software</span><span>$74</span></div><div class="r"><span>Personal</span><span>$219</span></div><div class="r tt"><span>Business total</span><span data-count="1224">$1,224</span></div></div>
<div class="bot q" data-m="bot">Home Depot, $64 on Oct 12: work or home?</div>
<div class="me" data-m="me">work</div><div class="bot" data-m="bot">Got it. Supplies is now <span data-count="676">$676</span>. Want me to always count Home Depot as work?</div></div>
<div class="inp"><span>Type a word</span><i></i></div><div class="hb"></div></div></div>
<div class="pcap">Sample business. Your numbers come from your own statement.</div></div></div></div></div></div><script src="/assets/lava.js?v=21" defer></script>
<div class="s5" id="agents"><div class="w5"><div class="sh5"><div><div class="lab">The agents</div><h2>Pick the job <em>you hate.</em></h2></div><p>Each agent fixes one problem for $9.99. Pay once, keep it, use it every week.</p></div>
<div class="ags">{rows}</div>
<div class="bd"><div><div class="lab">Best value</div><h3>All 4 agents</h3><p>Invoices, reviews, receipts and posts. Every agent above in one download.</p></div>
<div><div class="px"><s>$39.96</s><b>$24</b></div><div class="sv">You save <b>$15.96</b></div><a class="b5 l buy" href="{GR}owner-toolkit">Get all 4 for $24</a></div></div>
<div class="fd"><span><b>Run a service business that texts all day?</b> The Front Desk Kit drafts replies, quotes and follow ups from your real prices. $39.</span><a href="/front-desk/">See the Front Desk Kit</a></div></div></div>
<div class="s5"><div class="w5"><div class="sh5"><div><div class="lab">What it writes</div><h2>One word in. <em>A draft out.</em></h2></div><p>The kind of thing you get back after one word. You read it, then send it.</p></div>
<div class="tw" data-chat=".tch"><div class="tb" role="img" aria-label="Example on a wide screen: the Invoice Chaser keeps a list of who owes you and drafts the reminder for Dave">
<i class="tk k1"></i><i class="tk k2"></i><i class="tk k3"></i>
<div class="tsc"><div class="tsb"><span>Wed 9:41</span><span class="sig"><i></i><i></i><i></i><i></i><b></b></span></div>
<div class="tgr"><div class="tsd"><div class="tsh">Your agents</div>
<div class="ti on"><span class="tav">I</span><div><b>Invoice Chaser</b><span>3 people owe you</span></div></div>
<div class="ti"><span class="tav">R</span><div><b>Review Desk</b><span>2 new reviews</span></div></div>
<div class="ti"><span class="tav">B</span><div><b>Bookkeeping Sorter</b><span>October sorted</span></div></div>
<div class="ti"><span class="tav">C</span><div><b>Content Week</b><span>7 posts planned</span></div></div></div>
<div class="tmn"><div class="tth"><b>Invoice Chaser</b><span>Example business</span></div>
<div class="tch"><div class="me" data-m="me">owed</div>
<div class="bot" data-m="bot"><div class="bh">Who owes you</div><div class="r"><span>Dave · SUV detail</span><span>$520 · 7 days late</span></div><div class="r"><span>Laura · Interior</span><span>$150 · due Fri</span></div><div class="r"><span>Tom · Ceramic</span><span>$490 · due Mon</span></div><div class="r tt"><span>Still owed</span><span data-count="1160">$1,160</span></div></div>
<div class="me" data-m="me">chase Dave</div>
<div class="bot dr" data-m="bot"><div class="bh">Draft · 1 week late · friendly but clear</div>Hi Dave, following up on invoice 1042 for $520, due Oct 14. Here's the link to pay: [your link]. Let me know if you have any questions. Mike<div class="tac"><span>Edit</span><span class="ok">Copy and send</span></div></div></div>
<div class="inp"><span>Type a word</span><i></i></div></div></div><div class="hb"></div></div></div>
<div class="pcap">Sample business and numbers. Every message waits for you to send it.</div></div>
<div class="sp" style="margin-top:56px">{samples}</div></div></div>
<div class="s5 dk" id="why"><i class="dk-glow" aria-hidden="true"></i><div class="w5"><div class="sh5"><div><div class="lab">Before you buy</div><h2>How we <em>work.</em></h2></div><p>Most AI tools sell you features. Here is what we believe, when we would tell you to skip us, and what your first week looks like.</p></div>
<div class="tk"><div><div class="lab">What we believe</div><h3>Save hours, not add homework.</h3><ul><li>One agent, one boring job. Nothing new to learn.</li><li>You stay in charge. Nothing sends, posts or pays without you.</li><li>Cheap enough to try. If it does not save you time, you get your money back.</li></ul></div>
<div class="no"><div class="lab">When we would tell you no</div><h3>Don't buy what you won't use.</h3><p>We would rather you buy one agent you use every week than four you forget.</p><ul><li>Send two invoices a month? Skip the Invoice Chaser. A phone reminder is enough.</li><li>Get a review once a season? Use the free prompt below instead of the Review Desk.</li><li>Your accountant already sorts your receipts? You don't need the Bookkeeping Sorter.</li><li>Only need one job done? Buy that one for $9.99, not the bundle.</li></ul></div>
<div class="tl"><div class="lab">Your first week</div><h3>What it's like after you buy.</h3><ul><li><b>Minute 1.</b> You get the PDF right away.</li><li><b>Minute 15.</b> You paste one message and answer a few questions about your business. Your agent is set up.</li><li><b>Day 1.</b> You type one word, like "chase Dave", and read your first draft.</li><li><b>Every week after.</b> Same word, same result, in your voice. Stuck? Reply to your receipt and we help.</li></ul></div></div></div></div>
<div class="s5" id="how"><div class="w5"><div class="sh5"><div><div class="lab">Setup</div><h2>Ready in about <em>15 minutes.</em></h2></div><p>No code, no apps to learn. If you can send a text, you can do this.</p></div>
<div class="st5"><div><b>01</b><h3>Open Claude</h3><p>The free app or claude.ai. The free plan works.</p></div><div><b>02</b><h3>Paste one message</h3><p>It asks a few easy questions about your business.</p></div><div><b>03</b><h3>Type one word</h3><p>chase, reply, sort or week. Read the draft. Send it.</p></div></div></div></div>
<div class="s5" id="free"><div class="w5"><div class="tg"><div><div class="lab">Free · 60 seconds</div><h3>Try it before you buy</h3><p>Paste this into Claude with a real review of your business. It writes the reply.</p>
<div class="cp5" id="fp">Here is a review of my business. Write a short reply I can post.
My business: [name and what you do]
My name: [your first name]
The review: [paste it]
Keep it warm and real, 2 to 3 sentences. Don't make up any details.</div>
<button class="b5" style="margin-top:18px" onclick="navigator.clipboard.writeText(document.getElementById('fp').innerText);this.textContent='Copied'">Copy the message</button></div>
<div class="gu"><div class="lab" style="color:#3c3c36">Our promise</div><h3>30 day refund</h3><p>If an agent doesn't help your business, reply to your receipt within 30 days and get your money back.</p><ul><li>No forms, no calls</li><li>One payment, nothing recurring</li><li>Works on the free Claude plan</li></ul><a class="b5 buy" href="{GR}owner-toolkit">Get all 4 for $24</a></div></div></div></div>
<div class="s5"><div class="w5"><div class="sh5"><div><div class="lab">Questions</div><h2>Before <em>you buy.</em></h2></div><p>Still stuck after you buy? Reply to your receipt and we help.</p></div><div class="fq">{faq}</div>
<div class="lx lc"><div class="lci"><h3 data-lava-avoid>Pick the job you hate.</h3><p data-lava-avoid>$9.99 each, or all 4 for $24. One payment, 30 day refund.</p><div class="lcb" data-lava-avoid><a class="b5 buy" href="{GR}owner-toolkit">Get all 4 for $24</a><a class="b5 o" href="#agents">Pick one · $9.99</a></div></div></div></div></div>
<div class="sb" id="sb"><div><b>All 4 agents · $24</b><span>One payment · 30 day refund</span></div><a class="b5 l buy" href="{GR}owner-toolkit">Get them</a></div>
<script>(function(){{var s=document.getElementById('sb'),h=document.querySelector('.h5 .row');if(!('IntersectionObserver' in window)||!s||!h)return;new IntersectionObserver(function(x){{s.classList.toggle('on',!x[0].isIntersecting&&x[0].boundingClientRect.top<0)}}).observe(h)}})();</script>""" + FX + FOOT
    return page.replace("<body>", '<body class="v5">', 1)

PRODUCTS = [
 ("Front Desk Kit", "39", "/front-desk/", GR + "autopilot", "Customer replies, quotes and follow ups, drafted in your voice from your real prices.", ["15 question business interview", "Reply, quote, chase, review, FAQ, plan week", "3 extra systems built for your business", "Free Claude plan works"]),
 ("Bookkeeping Sorter", "9.99", "/#tools", GR + "bookkeeping-sorter", "Upload a statement, type sort. Each expense sorted into a category, with totals.", ["Setup helper, tap by tap", "Monthly and yearly totals", "Asks when it isn't sure", "Free Claude plan works"]),
 ("Invoice Chaser", "9.99", "/#tools", GR + "invoice-chaser", "Invoices from job notes and the right reminder for every late customer.", ["Setup helper, tap by tap", "Owed list", "Friendly to firm reminders", "Free Claude plan works"]),
 ("Review Desk", "9.99", "/#tools", GR + "review-desk", "Replies to every review in your voice, and the text that asks for new ones.", ["Setup helper, tap by tap", "Calm replies to bad reviews", "Never fake reviews", "Free Claude plan works"]),
 ("Content Week", "9.99", "/#tools", GR + "content-week", "5 questions on Sunday, 7 posts for the week.", ["Setup helper, tap by tap", "What to shoot, captions, hashtags", "Replies to comments", "Free Claude plan works"]),
 ("Owner Toolkit", "24", "/#tools", GR + "owner-toolkit", "All 4 tools: bookkeeping, invoices, reviews and posts. $39.96 separately.", ["4 setup helpers", "Works in the free Claude app", "You send everything", "30 day refund"]),
]
SOON = [("Done for you setup", "We set up your tools with your real prices and test them on your real messages."), ("Workspace", "Software that answers new leads while you are on a job. In development."), ("More tools", "Tell us the job you hate most. Reply to any receipt.")]
def marketplace():
    cards = "".join(f'<div class="card prod"><div class="nm">{e(n)}</div><div class="price">${p}<small>one time</small></div><p>{e(d)}</p><ul>{"".join(f"<li>{e(x)}</li>" for x in li[:3])}</ul><div class="go row"><a class="btn dark buy" style="flex:1" href="{g}">Get it · ${p}</a><a class="btn ghost" href="{u}">Details</a></div></div>' for n, p, u, g, d, li in PRODUCTS)
    soon = "".join(f'<div class="card"><span class="tagline dev">Coming soon</span><h3 style="margin:16px 0 8px">{e(n)}</h3><p>{e(d)}</p></div>' for n, d in SOON)
    return head("Marketplace · AI setup kits for small businesses · AUTOPILOT.OI", "Guided setup kits that install AI into your own Claude account. They draft; you decide and send. One time price, 30 day refund.", "/marketplace/") + nav("m") + f"""
<div class="wrap hero"><div class="k">Marketplace</div><h1 style="margin:22px 0 24px">Every tool.<br><em>From $9.99.</em></h1>
<p class="lead">Setup kits for your own Claude account. It drafts; you send. 30 day refund.</p></div>
<div class="sec paper"><div class="wrap"><div class="grid3">{cards}</div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Next</div><h2 style="margin-bottom:36px">Coming <em>soon.</em></h2><div class="grid3">{soon}</div></div></div>
<div class="sec"><div class="wrap grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development</span><h2 style="margin:20px 0 18px;font-size:clamp(28px,3.9vw,50px)">Answers leads <em>while you work.</em></h2><p class="lead">Workspace, our software, in development. It catches new leads and has the reply ready for your tap.</p><a class="btn" style="margin-top:28px" href="/workspace/">See Workspace</a></div>{INBOX}</div></div>""" + FOOT

def workspace():
    return head("Workspace · every lead answered · AUTOPILOT.OI", "Software for owner operated service businesses: every new lead answered within a minute, replies and quotes drafted, quiet quotes followed up. In development; founding spots open.", "/workspace/", "workspace-founding-cover.png") + nav("w") + f"""
<div class="wrap hero grid2" style="align-items:center;gap:44px"><div><span class="tagline dev">In development · founding spots open</span>
<h1 class="s" style="margin:22px 0 24px">Answers new leads <em>while you're on a job.</em></h1>
<p class="lead">Software we're building for service businesses. New leads get your acknowledgment within a minute; the reply and quote are drafted from your prices. You approve from your phone.</p>
<div class="row" style="margin-top:30px"><a class="btn buy" href="{GR}workspace-founding">Hold a founding spot · $49</a><a class="btn ghost" href="#list">Join the free list</a></div>
<p class="label" style="margin-top:14px">Deposit fully refundable · credited to your first month · $99 a month planned</p></div>{INBOX}</div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">How it will work</div><h2 style="margin-bottom:44px">How it <em>will work.</em></h2>
<div class="steps"><div><h3>Connect your line</h3><p style="color:var(--mut)">Phone line and form email. Quo (formerly OpenPhone) first.</p></div>
<div><h3>Teach it your business</h3><p style="color:var(--mut)">A 15 question interview. You write the one acknowledgment it may send.</p></div>
<div><h3>Approve with a tap</h3><p style="color:var(--mut)">Reply and quote drafted. Approve, edit or skip.</p></div></div></div></div>
<div class="sec"><div class="wrap"><div class="k" style="margin-bottom:16px">Permissions</div><h2 style="margin-bottom:36px">What it can <em>and can't do.</em></h2>
<div class="perm"><div class="card"><h3>It reads</h3><ul><li>New calls and texts on the line you connect</li><li>Lead emails you forward</li><li>Your calendar's free times (read only)</li></ul></div>
<div class="card"><h3>It sends on its own</h3><ul><li>Only your acknowledgment, written and approved by you</li><li>Nothing else</li></ul></div>
<div class="card"><h3>It always waits for you</h3><ul><li>Replies, quotes and follow ups</li><li>Anything with a price or a promise</li><li>Every message is logged where you can see it</li></ul></div></div></div></div>
<div class="sec paper"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Founding members</div><h2 style="font-size:clamp(28px,3.6vw,46px)">Hold a spot. <em>$49, refundable.</em></h2><p class="lead" style="margin-top:14px">Fully refundable, and credited to your first month.</p></div>
<div class="card"><div class="prod"><ul><li>$49 credited to your first paid month</li><li>First access to the beta, in the order you joined</li><li>$99 a month locked for your first 12 months</li><li>A say in what gets built first</li><li>Refund anytime before your first paid month; full refund if it's not open to founding members by Feb 28, 2027</li></ul><a class="btn dark buy" style="margin-top:18px" href="{GR}workspace-founding">Hold a founding spot · $49</a></div></div></div></div>
<div class="sec" id="list"><div class="wrap grid2" style="gap:44px"><div><div class="k" style="margin-bottom:16px">Free list</div><h2>Join the <em>free list.</em></h2><p class="lead" style="margin-top:14px">Free. Three questions tell us what to build first.</p></div>
<form class="form" id="wl"><input type="email" name="email_address" required placeholder="Your email" autocomplete="email">
<select name="fields[trade]" required><option value="">What kind of business?</option><option>Auto detailing</option><option>Cleaning</option><option>Landscaping or lawn</option><option>Handyman or home repair</option><option>HVAC, plumbing or electrical</option><option>Pressure washing</option><option>Other service business</option></select>
<select name="fields[leads_per_week]" required><option value="">New leads per week?</option><option>Under 5</option><option>5 to 15</option><option>16 to 40</option><option>More than 40</option></select>
<select name="fields[phone_system]" required><option value="">Business phone?</option><option>My cell phone</option><option>Quo (OpenPhone)</option><option>Google Voice</option><option>RingCentral or other VoIP</option><option>Other</option></select>
<button class="btn" type="submit">Join the list</button><p class="label" id="wlm">No spam. Unsubscribe anytime.</p></form></div></div>
<div class="sec"><div class="wrap grid2" style="gap:44px"><div><h2>Questions<em>.</em></h2></div><div>
<details><summary>Can I use Workspace today?</summary><p>Not yet. It's in development. Founding members get the beta first. Until then, the Front Desk Kit in our Marketplace drafts replies and quotes inside your own Claude account.</p></details>
<details><summary>What will it cost?</summary><p>$99 a month is the planned price. Founding members lock $99 for 12 months and get their $49 deposit credited to the first month.</p></details>
<details><summary>Will it text my customers on its own?</summary><p>Only the acknowledgment you write and approve during setup. Replies, quotes and follow ups always wait for your tap.</p></details>
<details><summary>Which phone systems will it work with?</summary><p>We plan to start with Quo (formerly OpenPhone). Tell us yours in the list form above; the answers decide what we connect next.</p></details>
<details><summary>How do refunds work?</summary><p>Reply to your Gumroad receipt anytime before your first paid month for the full $49. If Workspace isn't open to founding members by February 28, 2027, every deposit is refunded.</p></details></div></div></div>
<script>document.getElementById('wl').addEventListener('submit',function(ev){{ev.preventDefault();var f=new FormData(this);f.append('fields[source]','workspace_list');fetch('https://app.kit.com/forms/10118407/subscriptions',{{method:'POST',body:f,mode:'no-cors'}}).finally(function(){{document.getElementById('wlm').textContent="You're on the list. Check your email to confirm.";}});try{{if(window.fbq)fbq('track','Lead',{{content_name:'workspace_list'}})}}catch(e){{}};try{{if(window.goatcounter)goatcounter.count({{path:'optin/workspace-list',event:true}})}}catch(e){{}}}});</script>""" + FOOT

write("/", home()); write("/marketplace/", marketplace()); write("/workspace/", workspace())
redirect("/check/", "/brain/"); redirect("/store/", "/library/")  # old store links (Kit money and TikTok emails) land on the full catalog
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import frontdesk
write("/front-desk/", frontdesk.page(head, nav, FOOT))
for _v in ("after-hours", "demo"): write(frontdesk.VARIANTS[_v]["path"], frontdesk.page(head, nav, FOOT, _v))
import fdguides
for _g in fdguides.GUIDES: write(f"/guides/{_g['slug']}/", fdguides.page(_g, head, nav, FOOT))
redirect("/autopilot/", "/front-desk/"); redirect("/store/autopilot/", "/front-desk/")
print("site built")
