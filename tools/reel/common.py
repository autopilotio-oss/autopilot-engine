def cta(kw, reply, p):
    return f'''
 <div class="card" data-in="@{p}+0.05" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:16px">
  <div class="mono" style="padding:24px 28px;border-bottom:1px solid rgba(255,255,255,.08)">COMMENTS</div>
  <div class="row" data-in="@{p}+0.5" style="border:0;font-size:38px;background:rgba(212,255,58,.1);border-radius:20px;margin:14px 14px 6px"><div style="width:56px;height:56px;border-radius:50%;background:var(--l);flex:none"></div><div><div class="mono" style="font-size:16px;color:var(--l)">you · just now</div><b>{kw}</b></div></div>
  <div class="row" data-in="@{p}+1.3" style="border:0;font-size:27px;margin:6px 14px 0 70px;line-height:1.3"><img src="logo.png" style="width:50px;height:50px;border-radius:12px"><div><div class="mono" style="font-size:16px;color:var(--l)">autopilot.oi · reply</div>{reply}</div></div></div>
 <div data-in="@{p}+0.9" style="position:absolute;left:0;right:0;top:560px;text-align:center"><span style="display:inline-flex;align-items:center;gap:18px;background:var(--l);color:var(--d);border-radius:999px;padding:26px 50px;font:700 34px M;letter-spacing:4px;box-shadow:0 0 80px rgba(212,255,58,.5)">COMMENT "{kw}"</span></div>'''
def agent(name, rows, p):
    r = "".join(f'<div class="row" data-in="{t}" style="padding:18px 26px;font-size:28px"><span class="mono" style="color:var(--l);font-size:17px;min-width:170px">{a}</span><span>{b}</span></div>' for t, a, b in rows)
    return f'''<div class="card lit" data-in="@{p}+0.05" style="position:absolute;left:90px;right:90px;top:0;padding-bottom:10px">
  <div style="display:flex;align-items:center;padding:26px 28px"><span class="sticker" style="font-size:64px;color:var(--l)">✳ {name}</span><span class="chip on" style="margin-left:auto;font-size:16px;padding:8px 14px">ON</span></div>{r}</div>'''
ex = '<div class="note" style="position:absolute;right:96px;top:-40px">EXAMPLE</div>'
