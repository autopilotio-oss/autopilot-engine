
// ---------------------------------------------------------------------------
// Interface: command bar, nav + views, inspector, status bar, dock
// ---------------------------------------------------------------------------
const $ = (id) => document.getElementById(id);
let toastT; function toast(t) { ui.toast.textContent = t; ui.toast.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(() => ui.toast.classList.remove('on'), 3400); }
const ART = (d) => new Intl.DateTimeFormat('en-US', { timeZone: 'America/Argentina/Buenos_Aires', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(d);
const chiTime = () => new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', hour: 'numeric', minute: '2-digit' }).format(new Date());
const I = {
  clock: 'M12 7v5l3 2M12 21a9 9 0 110-18 9 9 0 010 18z', bolt: 'M13 2L4 14h7l-1 8 9-12h-7z', users: 'M9 11a4 4 0 100-8 4 4 0 000 8zM2 21a7 7 0 0114 0M17 11a3 3 0 100-6M22 21a6 6 0 00-5-6', list: 'M8 6h13M8 12h13M8 18h13M3 6h1M3 12h1M3 18h1',
  send: 'M4 12l16-8-6 16-3-7z', dollar: 'M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6', mail: 'M3 6h18v12H3zM3 7l9 6 9-6', cog: NAV[6][2], heart: 'M3 12h4l3-8 4 16 3-8h4', check: 'M20 6L9 17l-5-5', bell: 'M6 16V11a6 6 0 0112 0v5l2 2H4zM10 20a2 2 0 004 0', search: 'M11 18a7 7 0 100-14 7 7 0 000 14zM21 21l-5-5', menu: 'M4 6h16M4 12h16M4 18h16',
};
function renderTop() {
  const c = counts(); const nc = '<span class="nc" style="white-space:normal;line-height:1.05;display:block;font-size:9.5px!important">NOT CONNECTED</span>';
  const tiles = [
    ['Chicago', I.clock, chiTime()], ['Running', I.bolt, dash(c.running)], ['On shift', I.users, c.onShift == null ? '—' : `${c.onShift}<small style="color:var(--mut);font-size:13px">/${c.total}</small>`],
    ['Task queue', I.list, dash(c.queued)], ['Published', I.send, dash(c.published)], ['Revenue 7d', I.dollar, c.revenue == null ? nc : c.revenue + (c.orders7 != null ? `<small style="color:var(--mut);font-size:12px"> ${c.orders7} orders</small>` : '')], ['Subscribers', I.mail, dash(c.subs)],
    ['Runs 24h', I.cog, dash(c.next24)], ['Health', I.heart, c.health == null ? '—' : c.health + '%'], ['Approvals', I.check, c.approvals == null ? nc : String(c.approvals)],
  ];
  $('metrics').innerHTML = (innerWidth <= 820 ? `<button class="m glass" id="menuBtn" style="min-width:0;cursor:pointer;color:var(--lime)">${ico(I.menu)}</button>` : '') +
    tiles.map(([k, i, v], n) => `<div class="m glass" title="${k}" style="${n === 0 ? 'min-width:118px' : ''}"><em>${k}</em><div>${ico(i)}<strong>${v}</strong></div></div>`).join('') +
    `<button class="m glass" id="bell" style="min-width:0;cursor:pointer;color:${alerts().length ? 'var(--red)' : 'var(--lime)'}" title="Notifications">${ico(I.bell)}<strong style="font-size:13px">${alerts().length}</strong></button>`;
  const mb = $('menuBtn'); if (mb) mb.onclick = () => document.body.classList.toggle('menu');
  $('bell').onclick = () => openView('activity');
}
let curView = null, searchQ = '';
function renderSide() {
  const A = [...agents.values()]; const c = counts();
  const ct = { agents: A.length, tasks: c.next24 ?? '', content: live.posts ? P_().length : '', activity: events.length || '', integrations: ['triggers', 'posts', 'kit', 'hub'].filter((k) => live[k] && !live.err[k]).length * 1 + (live.hub && !live.err.hub ? 2 : 0) + '/7' };
  const deps = Object.entries(DEPTS).map(([k, d]) => `<div class="dp" data-dept="${k}"><i style="${A.some((a) => a.ident.dept === k && a.state === 'WORKING') ? '' : 'background:#3a4434;box-shadow:none'}"></i>${d.name}<b>${A.filter((a) => a.ident.dept === k).length}</b></div>`).join('');
  const side = $('side'); const had = side.querySelector('input'); const focus = had && document.activeElement === had;
  side.innerHTML = `<label class="search">${ico(I.search)}<input id="q" placeholder="Search agents  /" value="${esc(searchQ)}" autocomplete="off"></label>
${searchQ ? A.filter(matches).slice(0, 6).map((a) => `<div class="dp" data-agent="${a.id}"><i style="background:${STATE[a.state].c}"></i>${a.ident.code}<b>${esc(shortName(a)).slice(0, 18)}</b></div>`).join('') || '<div class="note" style="padding:6px 9px">No agent matches</div>' : ''}
${NAV.map(([k, n, d]) => `<div class="nv ${curView === k || (!curView && k === 'exec') ? 'on' : ''}" data-view="${k}">${ico(d)}${n}${ct[k] !== undefined && ct[k] !== '' ? `<span class="ct">${ct[k]}</span>` : ''}</div>`).join('')}
<div class="sh">DEPARTMENTS</div>${deps}`;
  const q = $('q'); if (focus) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
  q.oninput = () => { searchQ = q.value; renderSide(); };
  q.onkeydown = (e) => { if (e.key === 'Enter') { const a = A.find(matches); if (a) { openInspector(a.id, true); searchQ = ''; renderSide(); } } if (e.key === 'Escape') { searchQ = ''; q.blur(); renderSide(); } };
  side.querySelectorAll('[data-view]').forEach((el) => (el.onclick = () => { document.body.classList.remove('menu'); el.dataset.view === 'exec' ? closeView() : openView(el.dataset.view); }));
  side.querySelectorAll('[data-dept]').forEach((el) => (el.onclick = () => { closeView(); goto(el.dataset.dept); setDock(el.dataset.dept); }));
  side.querySelectorAll('[data-agent]').forEach((el) => (el.onclick = () => openInspector(el.dataset.agent, true)));
}
const matches = (a) => { const q = searchQ.trim().toLowerCase(); return q && (a.ident.code.toLowerCase().includes(q) || a.name.toLowerCase().includes(q) || DEPTS[a.ident.dept].name.toLowerCase().includes(q)); };
function renderStatus() {
  const c = counts(); const down = ['triggers', 'posts', 'kit', 'hub'].filter((k) => live.err[k]).length; const syncs = Object.values(live.at).filter(Boolean);
  $('status').innerHTML = `<span class="on" style="${down ? 'color:var(--amber)' : ''}"><i style="${down ? 'background:var(--amber);box-shadow:0 0 8px var(--amber)' : ''}"></i>${DEMO ? 'DEMO MODE · TEST DATA' : down ? down + ' FEED' + (down > 1 ? 'S' : '') + ' DOWN' : 'ALL FEEDS LIVE'}</span>
<span class="s">Agents <b>${dash(c.running)}</b> running / <b>${dash(c.onShift)}</b> on shift</span><span class="s">Posts today <b>${dash(c.published)}</b> out · <b>${dash(c.queued)}</b> queued</span>
<span class="s">Subscribers <b>${dash(c.subs)}</b></span><span class="s">Last sync <b>${syncs.length ? ago(new Date(Math.max(...syncs)).toISOString()) : '—'}</b></span><span class="s">Events <b>${events.length}</b></span>
<span class="city">CHICAGO, IL · ${chiTime()} ${ico(I.heart)}</span>`;
}
const DOCK = [['hq', 'Overview', NAV[0][2]], ['exec', 'Executive', I.users], ['content', 'Content', NAV[4][2]], ['care', 'Support', I.mail], ['finance', 'Finance', I.dollar], ['systems', 'Systems', I.cog], ['street', 'Street', 'M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6']];
function renderDock() {
  $('dock').innerHTML = DOCK.map(([k, n, d], i) => `<button data-cam="${k}" title="${n} (${i + 1})" class="${k === 'hq' ? 'on' : ''}">${ico(d)}${n}</button>`).join('') + `<span class="sep"></span><button data-act="replay" title="Replay session activity (R)">${ico('M4 4v6h6M4 10a8 8 0 112 7')}Replay</button>`;
  $('dock').querySelectorAll('[data-cam]').forEach((b) => (b.onclick = () => { closeView(); setDock(b.dataset.cam); goto(b.dataset.cam); }));
  $('dock').querySelector('[data-act=replay]').onclick = replay;
}
function setDock(k) { $('dock').querySelectorAll('[data-cam]').forEach((x) => x.classList.toggle('on', x.dataset.cam === k)); }

// ---- views
function openView(k) { curView = k; $('view').hidden = false; renderView(); renderSide(); }
function closeView() { curView = null; $('view').hidden = true; renderSide(); }
const ncCard = (what, why, how) => `<div class="ncard"><b>NOT CONNECTED</b> · ${what}<br><span style="color:#b9b08a">${why}</span>${how ? `<br><span style="color:#8f9886">${how}</span>` : ''}</div>`;
const row = (cells, id) => `<tr ${id ? `class="click" data-agent="${id}"` : ''}>${cells.map((c) => `<td>${c}</td>`).join('')}</tr>`;
const stPill = (s) => `<span class="pill" style="color:${STATE[s].c};border-color:${STATE[s].c}55">● ${STATE[s].label}</span>`;
const netName = (n) => ({ instagram: 'Instagram', tiktok: 'TikTok', threads: 'Threads', twitter: 'X' })[n] || n;
function renderView() {
  if (!curView) return; const A = [...agents.values()]; const c = counts(); const P = P_().slice().sort((a, b) => a.time.localeCompare(b.time));
  const title = (NAV.find((n) => n[0] === curView) || [0, curView])[1];
  let body = '';
  if (curView === 'agents') body = `<table class="t"><tr><th>Agent</th><th>Department</th><th>State</th><th>Last run</th><th>Next run</th></tr>${A.map((a) => row([`<b>${a.ident.code}</b><br><span class="note">${esc(shortName(a))}</span>`, DEPTS[a.ident.dept].name, stPill(a.state), a.data ? `${ago(a.data.last)}<br><span class="note">${a.data.status || ''}</span>` : a.gh ? `${ago(a.gh.finished || a.gh.started)}<br><span class="note">${(a.gh.conclusion || a.gh.status || '').toUpperCase()}</span>` : '—', a.data ? ago(a.data.next) : a.gh ? (a.gh.runs24h ?? '—') + ' runs / 24h' : a.ghost ? 'waiting for ANALYST' : '—'], a.id)).join('')}</table>`;
  else if (curView === 'workflows') body = A.filter((a) => a.data).map((a) => `<div class="sec" style="border:1px solid #1d241a;border-radius:10px;margin-bottom:10px"><h4><span>${a.ident.code} · ${esc(shortName(a))}</span>${stPill(a.state)}</h4>${a.steps && a.steps.length ? `<ol class="flow">${a.steps.map((s) => `<li class="${a.state === 'WORKING' ? '' : ''}"><i></i>${esc(s)}</li>`).join('')}</ol><div class="note" style="margin-top:6px">Steps read from this agent's standing orders. Which step is running is not reported by the scheduler.</div>` : '<div class="note">No numbered steps declared in its standing orders.</div>'}</div>`).join('') || '<div class="note">Waiting for the scheduler feed.</div>';
  else if (curView === 'tasks') { const run = A.filter((a) => a.state === 'WORKING'); const up = A.filter((a) => a.data && a.data.raw.enabled && a.data.next).sort((a, b) => new Date(a.data.next) - new Date(b.data.next));
    body = `<h4 class="sh" style="margin-left:0">RUNNING NOW</h4>${run.length ? `<table class="t">${run.map((a) => row([`<b>${a.ident.code}</b>`, esc(shortName(a)), 'started ' + ago(a.data.last)], a.id)).join('')}</table>` : '<div class="note">Nothing running right now.</div>'}
<h4 class="sh" style="margin-left:0">UP NEXT</h4><table class="t"><tr><th>When</th><th>Agent</th><th>Task</th><th></th></tr>${up.map((a) => row([ago(a.data.next) + `<br><span class="note">${ART(new Date(a.data.next))} ART</span>`, `<b>${a.ident.code}</b>`, esc(shortName(a)), `<button class="btn" data-run="${a.id}">Run now</button>`], a.id)).join('')}</table>
<div class="note" style="margin-top:8px">Run now assigns the task to the agent immediately, after you confirm. It acts on your real scheduled task.</div>`; }
  else if (curView === 'content') body = live.posts ? `<table class="t"><tr><th>Time ART</th><th>Network</th><th>Status</th><th>Post</th></tr>${P.map((p) => row([p.time.slice(11, 16), netName(p.net), `<span style="color:${p.status === 'PUBLISHED' ? 'var(--lime)' : p.status === 'ERROR' ? 'var(--red)' : 'var(--mut)'}">${p.status}</span>`, esc(p.text.slice(0, 90)) + (p.url ? ` <a href="${esc(p.url)}" target="_blank" rel="noopener">open</a>` : '')])).join('')}</table>` : `<div class="note">${live.err.posts ? 'Metricool feed: ' + live.err.posts.text : 'Waiting for Metricool.'}</div>`;
  else if (curView === 'publishing') body = live.posts ? `<table class="t"><tr><th>Network</th><th>Published</th><th>Queued</th><th>Failed</th><th>Daily cap</th></tr>${NETS.map(([n]) => { const r = P.filter((p) => p.net === n); return row([netName(n), r.filter((p) => p.status === 'PUBLISHED').length, r.filter((p) => p.status === 'PENDING').length, r.filter((p) => p.status === 'ERROR').length, n === 'instagram' ? 2 : 3]); }).join('')}</table><div class="note" style="margin-top:8px">Caps come from your cadence rules (Instagram 2 a day, others 3). Counts are today in Argentina time.</div>` : '<div class="note">Waiting for Metricool.</div>';
  else if (curView === 'automations') body = `<table class="t"><tr><th>Automation</th><th>Runs on</th><th>Schedule</th><th>State</th></tr>${A.map((a) => row([`<b>${a.ident.code}</b> ${esc(shortName(a))}`, a.ghost ? 'GitHub Actions' : 'Claude scheduler', a.data ? esc((a.data.cron || 'on demand').replace(/CRON_TZ=\S+\s/, '')) : a.ghost ? a.ident.wf : '—', stPill(a.state)], a.id)).join('')}</table>`;
  else if (curView === 'intel') { const s = A.filter((a) => ['WIRE', 'SCOUT'].includes(a.ident.code)); body = `${s.map((a) => `<div class="sec">${a.ident.code} · ${esc(shortName(a))} ${stPill(a.state)}<div class="note">${esc(activity(a))}</div></div>`).join('')}${ncCard('Research findings feed', 'Sources the news desk checked and trends it rejected are written to the repo, not sent to this page yet.', 'Next step: a findings file the page can read.')}`; }
  else if (curView === 'analytics') body = ncCard('Reach, views, saves, follows', 'Metricool analytics are available but this page only has permission for the post schedule.', 'Next step: allow Metricool getAnalyticsDataByMetrics on this page.') + `<div class="note" style="margin-top:10px">Today you can see post status (Content, Publishing) and Kit subscribers. Nothing here is estimated.</div>`;
  else if (curView === 'finance') body = (live.hub && live.hub.revenue ? (() => { const r = live.hub.revenue; return `<table class="t"><tr><th>Verified (Gumroad ledger)</th><th></th></tr>${row(['Orders, all time', r.orders_all_time ?? '—'])}${row(['Orders, last 7 days', r.orders_7d ?? '—'])}${row(['Net, last 7 days', money(r)])}${row(['Refunds, all time', r.refunds_all_time ?? '—'])}${row(['Ledger synced', r.ledger_synced ? ago(r.ledger_synced) : '—'])}</table><div class="note" style="margin:8px 0 12px">Net = gross minus Gumroad fees and refunds. Delivered by ANALYST ${ago(live.hub.at)}${hubStale() ? ' (STALE)' : ''}.</div>`; })() : ncCard('Revenue', 'Waiting for the first ANALYST report (it copies the Gumroad ledger summary here every hour).', '')) + '<br>' + ncCard('Ad spend', 'Meta ads ($10/day, $60 cap from Nov 5) are managed through Adspirer, which is not allowed on this page.', 'Spending stays approval only.');
  else if (curView === 'integrations') { const f = (n, k) => { const ok = live[k] && !live.err[k]; return row([n, ok ? '<span style="color:var(--lime)">● LIVE</span>' : live.err[k] ? `<span style="color:var(--red)">● ${esc(live.err[k].text)}</span>` : DEMO ? 'DEMO' : '…', live.at[k] ? ago(new Date(live.at[k]).toISOString()) : '—']); };
    body = `<table class="t"><tr><th>Source</th><th>Status</th><th>Last sync</th></tr>${f('Claude scheduler (agents)', 'triggers')}${f('Metricool (posts)', 'posts')}${f('Kit (subscribers)', 'kit')}${f('Gumroad ledger (revenue) · via ANALYST', 'hub')}${f('GitHub Actions (workers) · via ANALYST', 'hub')}${f('Approval queue (repo) · via ANALYST', 'hub')}${row(['Meta Ads (spend)', '<span class="nc">NOT CONNECTED</span>', '—'])}</table>`; }
  else if (curView === 'activity') body = `<div class="row" style="margin-bottom:10px"><button class="btn lime" id="rp">${ico('M4 4v6h6M4 10a8 8 0 112 7')}Replay session</button></div>
${alerts().length ? `<h4 class="sh" style="margin-left:0">NEEDS ATTENTION</h4>${alerts().map((x) => `<div class="sec" style="border-left:3px solid ${x.c}"><b>${esc(x.title)}</b><div class="note">${esc(x.sub)}</div></div>`).join('')}` : ''}
<h4 class="sh" style="margin-left:0">SESSION LOG · SINCE YOU OPENED THIS PAGE</h4><div class="log">${events.map((e) => `<div ${e.agentId ? `data-agent="${e.agentId}" style="cursor:pointer"` : ''}><span>${ART(new Date(e.at))}</span><span style="color:${e.color}">${esc(e.text)}</span></div>`).join('') || '<div><span></span><span class="note">No changes observed yet.</span></div>'}</div>`;
  else if (curView === 'settings') body = `<h4 class="sh" style="margin-left:0">PERFORMANCE PROFILE</h4><div class="row">${Object.entries(PROFILES).map(([k, p]) => `<button class="btn ${k === profileKey ? 'lime' : ''}" data-prof="${k}">${p.label}</button>`).join('')}</div>
<div class="note" style="margin-top:6px">High: full resolution, soft shadows, bloom. Standard: lighter shadows and bloom. Mobile: no shadows, no bloom, compact cards. Detected: ${PROFILES[autoProfile].label}.</div>
<h4 class="sh" style="margin-left:0">LIGHTING</h4><div class="row">${['auto', 'day', 'sunset', 'night'].map((k) => `<button class="btn ${k === lightMode ? 'lime' : ''}" data-light="${k}">${k === 'auto' ? 'Chicago time' : k}</button>`).join('')}</div>
<h4 class="sh" style="margin-left:0">DATA MODE</h4><div class="note">${DEMO ? 'DEMO MODE is on: every number is test data. <a href="#" id="toLive">Back to live</a>' : 'Live. Add #demo to the address for a clearly labeled test dataset (never mixed with live data).'}</div>
<h4 class="sh" style="margin-left:0">ENVIRONMENT</h4><div class="note">Real textures, HDRI light and furniture from Poly Haven (CC0). Loaded: ${assetState.textures} textures, ${assetState.models} models${assetState.failed.length ? ', failed: ' + assetState.failed.join(', ') : ''}.</div>
<h4 class="sh" style="margin-left:0">CHARACTERS</h4><div class="note">Operative v1: MakeHuman body (CC0, anatomically modeled, real eyes), 52 bone Mixamo-compatible skeleton with fingers, black fleece hoodie, modeled hood and knit balaclava, cargo pants, sneakers. Built in Blender by tools/character in the repo. Poses are driven by each agent's real state. Status: ${heroState.loaded ? 'loaded' : heroState.failed ? 'failed, using placeholders' : 'loading'}.<br>Not yet: cloth simulation wrinkles, finger poses, eye movement, per agent body variation, motion captured animation.</div>
<h4 class="sh" style="margin-left:0">KEYBOARD</h4><div class="log">${[['1 to 7', 'Camera presets'], ['/', 'Search agents'], ['[ ]', 'Previous / next agent'], ['A W T L', 'Agents, Workflows, Tasks, Activity'], ['R', 'Replay session'], ['Esc', 'Close panels']].map(([k, v]) => `<div><span>${k}</span><span>${v}</span></div>`).join('')}</div>`;
  $('view').innerHTML = `<div class="ih"><span>${title.toUpperCase()}${DEMO ? ' · <span style="color:var(--red)">DEMO</span>' : ''}</span><button class="x" id="vx">✕</button></div><div class="vb">${body}</div>`;
  $('vx').onclick = closeView;
  $('view').querySelectorAll('[data-agent]').forEach((el) => (el.onclick = (e) => { if (e.target.closest('button,a')) return; openInspector(el.dataset.agent, true); }));
  $('view').querySelectorAll('[data-run]').forEach((el) => (el.onclick = () => act(agents.get(el.dataset.run), 'run')));
  $('view').querySelectorAll('[data-prof]').forEach((el) => (el.onclick = () => { applyProfile(el.dataset.prof); renderView(); toast(PROFILES[el.dataset.prof].label + ' profile'); }));
  $('view').querySelectorAll('[data-light]').forEach((el) => (el.onclick = () => { lightMode = el.dataset.light; applyLight(); renderView(); }));
  const tl = $('toLive'); if (tl) tl.onclick = (e) => { e.preventDefault(); location.hash = ''; location.reload(); };
  const rp = $('rp'); if (rp) rp.onclick = replay;
}

// ---- inspector
let openId = null;
const portrait = { rt: null, cam: new THREE.PerspectiveCamera(28, 1, 0.05, 50), px: null };
function openInspector(id, fly) {
  const a = agents.get(id); if (!a) return; openId = id; $('insp').hidden = false; if (innerWidth <= 820) closeView();
  if (fly) { cam.goal = { t: a.seat.clone().setY(1.2), yaw: cam.yaw, pitch: Math.max(0.5, Math.min(cam.pitch, 0.8)), dist: 7.5 }; }
  renderInspector();
}
function closeInspector() { openId = null; $('insp').hidden = true; }
function renderInspector() {
  const a = agents.get(openId); if (!a) return; const d = a.data; const st = STATE[a.state];
  const dur = d && d.last ? (d.finished ? Math.max(0, Math.round((new Date(d.finished) - new Date(d.last)) / 60000)) + ' min last run' : a.state === 'WORKING' ? 'running ' + ago(d.last).replace(' ago', '') : '—') : '—';
  const collab = (COLLAB[a.ident.code] || []).map((code) => { const b = [...agents.values()].find((x) => x.ident.code === code); return b ? `<span data-agent="${b.id}" style="cursor:pointer;border-color:${STATE[b.state].c}66">${code}</span>` : ''; }).join('');
  const recent = events.filter((e) => e.agentId === a.id).slice(0, 5);
  const enabled = d && d.raw.enabled;
  $('insp').innerHTML = `<div class="ih"><span>AGENT INSPECTOR${DEMO ? ' · <span style="color:var(--red)">DEMO</span>' : ''}</span><button id="ix">✕</button></div>
<div class="prof"><canvas id="pc" width="172" height="172"></canvas><div><div class="id">${a.ghost ? 'GitHub Actions' : 'ID ' + esc(String(a.id).slice(-8))}</div><h3><i style="background:${st.c};box-shadow:0 0 8px ${st.c}"></i>${a.ident.code}</h3><div class="note">${DEPTS[a.ident.dept].name}</div><span class="pill" style="margin-top:6px;color:${st.c};border-color:${st.c}66">● ${st.label}</span><br><span class="tag" style="color:#9aa18f;border-color:#2a3226">${heroState.loaded ? 'OPERATIVE v1 · CC0 BODY' : heroState.failed ? 'PLACEHOLDER MODEL' : 'LOADING MODEL'}</span></div></div>
<dl class="kv"><dt>Role</dt><dd>${esc(a.ident.role)}</dd><dt>Task</dt><dd>${esc(shortName(a))}</dd><dt>Activity</dt><dd>${esc(activity(a))}</dd><dt>Elapsed</dt><dd>${dur}</dd>
${d ? `<dt>Schedule</dt><dd>${esc((d.cron || 'on demand').replace(/CRON_TZ=\S+\s/, ''))}${String(d.cron).startsWith('CRON_TZ') ? ' ART' : ''}</dd><dt>Next run</dt><dd>${ago(d.next)}${d.next ? ' · ' + ART(new Date(d.next)) + ' ART' : ''}</dd><dt>Last result</dt><dd>${d.status || 'not run yet'}</dd>` : (a.gh ? `<dt>Workflow</dt><dd>${a.ident.wf}</dd><dt>Last run</dt><dd>${ago(a.gh.finished || a.gh.started)} · ${(a.gh.conclusion || a.gh.status || '').toUpperCase()}</dd><dt>Runs 24h</dt><dd>${a.gh.runs24h ?? '—'} (${a.gh.fails24h ?? 0} failed)</dd><dt>Feed</dt><dd>ANALYST, ${ago(live.hub.at)}${hubStale() ? ' · STALE' : ''}</dd>` : `<dt>Feed</dt><dd>${a.ghost ? 'GitHub Actions worker. Waiting for the ANALYST report.' : 'Waiting for the live feed.'}</dd>`)}</dl>
${a.state === 'WORKING' ? `<div class="sec"><h4><span>PROGRESS</span><span class="note">not reported</span></h4><div class="bar"><b></b></div><div class="note" style="margin-top:6px">The scheduler reports started and finished, not percent done, so no number is shown.</div></div>` : ''}
<div class="sec"><h4><span>WORKFLOW</span><span class="note">from standing orders</span></h4>${a.steps && a.steps.length ? `<ol class="flow">${a.steps.map((s) => `<li><i></i>${esc(s)}</li>`).join('')}</ol>` : '<div class="note">No declared steps.</div>'}</div>
<div class="sec"><h4><span>TOOLS</span><span class="note">named in its orders</span></h4><div class="chips">${(a.tools || []).map((t) => `<span>${t}</span>`).join('') || '<span>—</span>'}</div></div>
<div class="sec"><h4><span>COLLABORATORS</span><span class="note">from config</span></h4><div class="chips">${collab || '<span>—</span>'}</div></div>
<div class="sec"><h4><span>PERFORMANCE 7D</span></h4><span class="nc">NOT CONNECTED</span><div class="note">Run history beyond the last run is not in the feed.</div></div>
<div class="sec"><h4><span>REVENUE ATTRIBUTED</span></h4><span class="nc">NOT CONNECTED</span></div>
<div class="sec"><h4><span>RECENT ACTIVITY</span><span class="note">this session</span></h4><div class="log">${recent.map((e) => `<div><span>${ART(new Date(e.at))}</span><span style="color:${e.color}">${esc(e.text)}</span></div>`).join('') || '<div><span></span><span class="note">No changes seen yet</span></div>'}</div></div>
<div class="sec"><h4><span>ERRORS AND APPROVALS</span></h4>${a.state === 'FAILED' ? '<div style="color:var(--red);font-size:12px">Last run failed. Open the run in Claude to see why.</div>' : '<div class="note">No failure on the last run.</div>'}<div style="margin-top:6px"><span class="nc">APPROVALS: NOT CONNECTED</span></div></div>
${d && !a.ghost ? `<div class="sec"><div class="row"><button class="btn lime" id="iRun" ${!enabled || a.state === 'WORKING' ? 'disabled' : ''}>${ico(I.bolt)}Run now</button><button class="btn ${enabled ? 'red' : ''}" id="iTog">${enabled ? 'Pause' : 'Resume'}</button></div><div class="note" style="margin-top:8px">${DEMO ? 'Demo mode: buttons do nothing.' : 'Acts on your real scheduled task after you confirm.'}</div></div>` : ''}`;
  $('ix').onclick = closeInspector;
  $('insp').querySelectorAll('[data-agent]').forEach((el) => (el.onclick = () => openInspector(el.dataset.agent, true)));
  const r = $('iRun'); if (r) r.onclick = () => (DEMO ? toast('Demo mode: nothing was run.') : act(a, 'run'));
  const tg = $('iTog'); if (tg) tg.onclick = () => (DEMO ? toast('Demo mode: nothing changed.') : act(a, enabled ? 'pause' : 'resume'));
  drawPortrait();
}
function drawPortrait() {
  const a = agents.get(openId); const cv = $('pc'); if (!a || !cv || !renderer) return;
  if (!portrait.rt) { portrait.rt = new THREE.WebGLRenderTarget(172, 172); portrait.px = new Uint8Array(172 * 172 * 4); }
  const head = new THREE.Vector3(); a.rig.head.getWorldPosition(head);
  const fwd = new THREE.Vector3(0, 0, 1).applyQuaternion(a.rig.root.quaternion);
  portrait.cam.position.copy(head).addScaledVector(fwd, 1.15).add(new THREE.Vector3(0, 0.05, 0)); portrait.cam.lookAt(head.x, head.y - 0.12, head.z);
  renderer.setRenderTarget(portrait.rt); renderer.render(scene, portrait.cam); renderer.readRenderTargetPixels(portrait.rt, 0, 0, 172, 172, portrait.px); renderer.setRenderTarget(null);
  const g = cv.getContext('2d'); const img = g.createImageData(172, 172);
  for (let y = 0; y < 172; y++) img.data.set(portrait.px.subarray((171 - y) * 688, (172 - y) * 688), y * 688);
  g.putImageData(img, 0, 0);
}

// ---- floating cards: projected from 3D each frame
const proj = new THREE.Vector3(); let hoverId = null;
function placeCards() {
  const mini = PROFILES[profileKey].cards === 'mini';
  for (const a of agents.values()) {
    const el = a.card; if (!a.rig.root.visible) { el.style.display = 'none'; continue; }
    proj.copy(a.pos).setY(a.state === 'WORKING' || a.state === 'FAILED' || a.state === 'COMPLETED' ? 2.45 : 2.75).applyMatrix4(HQ.matrixWorld).project(camera);
    const d = camera.position.distanceTo(a.pos);
    if (proj.z > 1 || Math.abs(proj.x) > 1.05 || Math.abs(proj.y) > 1.05 || d > 70) { el.style.display = 'none'; continue; }
    el.style.display = ''; el.style.left = ((proj.x + 1) / 2 * innerWidth) + 'px'; el.style.top = ((1 - proj.y) / 2 * innerHeight) + 'px';
    const focus = a.id === openId || a.id === hoverId; el.classList.toggle('dot', !focus); el.classList.toggle('mini', focus && (mini || d > 30)); el.style.zIndex = String(focus ? 2000 : 1000 - Math.round(d)); el.style.opacity = focus ? '1' : d > 45 ? '0.55' : '0.85';
    el.style.outline = a.id === openId ? '1px solid var(--edge2)' : '';
  }
}

// ---- replay: walk the camera through this session's events, oldest first
let replaying = null;
function replay() {
  const list = events.filter((e) => e.agentId && agents.has(e.agentId)).slice(0, 12).reverse();
  if (!list.length) return toast('Nothing to replay yet: no agent changes observed this session.');
  clearInterval(replaying); let i = 0; closeView();
  const step = () => { if (i >= list.length) { clearInterval(replaying); replaying = null; toast('Replay finished'); goto('hq'); setDock('hq'); return; } const e = list[i++]; openInspector(e.agentId, true); toast(`${ART(new Date(e.at))} · ${e.text}`); };
  step(); replaying = setInterval(step, 3200);
}

// ---- keyboard
addEventListener('keydown', (e) => {
  if (e.target.closest && e.target.closest('input,textarea')) return;
  const A = [...agents.values()];
  if (e.key >= '1' && e.key <= '7') { const k = DOCK[+e.key - 1][0]; closeView(); setDock(k); goto(k); }
  else if (e.key === '/') { e.preventDefault(); $('q').focus(); }
  else if (e.key === 'Escape') { if (replaying) { clearInterval(replaying); replaying = null; } if (!$('modal').hidden) return; if (curView) closeView(); else closeInspector(); }
  else if (e.key === '[' || e.key === ']') { const i = Math.max(0, A.findIndex((a) => a.id === openId)); const n = A[(i + (e.key === ']' ? 1 : -1) + A.length) % A.length]; openInspector(n.id, true); }
  else if (/^[awtl]$/i.test(e.key)) openView({ a: 'agents', w: 'workflows', t: 'tasks', l: 'activity' }[e.key.toLowerCase()]);
  else if (/^r$/i.test(e.key)) replay();
  else if (e.key === '?') openView('settings');
});

function renderUI() {
  renderTop(); renderSide(); renderStatus(); drawWalls(clockT());
  if (curView) renderView(); if (openId) renderInspector();
  for (const a of agents.values()) drawCard(a);
}
const clockT = () => performance.now() / 1000;

// ---- DEMO MODE: separate, clearly labeled test dataset. Only with #demo. Never mixed with live feeds.
function simulate() {
  const s = document.createElement('div'); s.id = 'demo'; s.textContent = 'DEMO MODE · TEST DATA · NOT REAL'; document.body.append(s);
  const now = Date.now(), iso = (m) => new Date(now + m * 60000).toISOString();
  const mk = (id, name, fired, fin, st, en = true, prompt = 'Demo standing orders.') => (fired == null ? { id, name, enabled: en, next_run_at: iso(600), run_once_at: iso(600), derived_state: { prompt } } : ({ id, name, enabled: en, cron_expression: 'CRON_TZ=America/Argentina/Buenos_Aires 49 * * * *', next_run_at: iso(40), last_run: { status: 'ROUTINE_RUN_STATUS_' + st, fired_at: iso(fired), finished_at: fin == null ? null : iso(fin) }, derived_state: { prompt } }));
  const wireOrders = '1. SCAN the wires with web search\n2. VERIFY two sources\n3. LIMITS AND SLOTS check cadence\n4. BUILD carousel with build.py and render\n5. PUBLISH to Metricool\n6. LEARN from results';
  applyTriggers([mk('d1', 'AUTOPILOT.OI News Desk (hourly)', -2, null, 'RUNNING', true, wireOrders), mk('d2', 'FIRST SALES MODE operator', -200, -180, 'SUCCEEDED', true, '1. Factory reels\n2. Funnels and Kit\n3. Meta ads check\n4. Scoreboard to GitHub'), mk('d3', 'Support + inbox monitor', -15, -10, 'SUCCEEDED', true, 'Read Gmail inbox, draft replies.'),
    mk('d4', 'Monthly Scale Review', -300, -290, 'FAILED'), mk('d5', 'Daily Pulse', -1, null, 'RUNNING'), mk('d6', 'Weekly sprint', -3000, -2990, 'SUCCEEDED', false), mk('d7', 'AUTOPILOT.OI trend scout', -60, -50, 'SUCCEEDED'), mk('d8', 'FIRST SALES MODE final report', null, null, '')]);
  applyPosts({ data: [{ publicationDate: { dateTime: '2026-11-01T10:00:00' }, providers: [{ network: 'instagram', status: 'PUBLISHED' }, { network: 'tiktok', status: 'PUBLISHED' }], text: 'Demo post one' }, { publicationDate: { dateTime: '2026-11-01T18:00:00' }, providers: [{ network: 'threads', status: 'PENDING' }, { network: 'twitter', status: 'PENDING' }], text: 'Demo post two' }] });
  live.kit = { subscribers: 0 }; ['triggers', 'posts', 'kit'].forEach((k) => (live.at[k] = now));
  applyHub({ at: iso(-12), by: 'ANALYST (demo)', github: { 'post.yml': { status: 'in_progress', started: iso(-1), runs24h: 40, fails24h: 0 }, 'health.yml': { status: 'completed', conclusion: 'success', started: iso(-15), finished: iso(-14), runs24h: 14, fails24h: 0 }, 'daily.yml': { status: 'completed', conclusion: 'failure', started: iso(-50), finished: iso(-49), runs24h: 6, fails24h: 1 }, 'revenue.yml': { status: 'completed', conclusion: 'success', started: iso(-90), finished: iso(-88), runs24h: 5, fails24h: 0 } },
    revenue: { orders_all_time: 3, orders_7d: 3, net_7d: { USD: 21 }, refunds_all_time: 0, ledger_synced: iso(-90) }, approvals: { count: 2, items: ['Demo approval one', 'Demo approval two'] } });
  setTimeout(() => { const a = agents.get('d3'); a.data.raw.last_run = { status: 'ROUTINE_RUN_STATUS_RUNNING', fired_at: new Date().toISOString() }; a.data.last = a.data.raw.last_run.fired_at; logEvent('run', 'SHIELD run fired (demo)', 'd3'); a.shownState = null; setState(a, 'WORKING'); renderUI(); }, 4000);
  renderUI();
}

// ---- optional licensed character: assets/agent.glb replaces the placeholders when present
let glbState = 'no GLB found, using placeholders';
async function tryGLB() {
  try {
    const head = await fetch('assets/agent.glb', { method: 'HEAD' }); if (!head.ok) return;
    glbState = 'loading assets/agent.glb';
    const [{ GLTFLoader }, SU] = await Promise.all([import('three/addons/loaders/GLTFLoader.js'), import('three/addons/utils/SkeletonUtils.js')]);
    const gltf = await new GLTFLoader().loadAsync('assets/agent.glb');
    const box3 = new THREE.Box3().setFromObject(gltf.scene); const h = box3.max.y - box3.min.y || 1; const scale = 1.75 / h;
    const clip = (re) => gltf.animations.find((c) => re.test(c.name));
    for (const a of agents.values()) {
      const m = SU.clone(gltf.scene); m.scale.setScalar(scale); m.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.userData.agentId = a.id; } });
      const mixer = new THREE.AnimationMixer(m); const acts = {};
      for (const [k, re] of [['idle', /idle|stand/i], ['walk', /walk/i], ['type', /typ|keyboard|sit.*work/i], ['sit', /sit/i]]) { const c = clip(re); if (c) acts[k] = mixer.clipAction(c); }
      a.rig.root.traverse((o) => { if (o.isMesh) o.visible = false; }); a.rig.root.add(m); a.glb = { m, mixer, acts, cur: null };
    }
    glbState = `loaded (${gltf.animations.length} clips)`;
  } catch (e) { glbState = 'GLB failed to load, using placeholders'; }
}
function glbPose(a, kind, dt) {
  const G = a.glb; if (!G) return false; const want = kind === 'walk' ? 'walk' : kind === 'type' ? 'type' : ['sit', 'slump', 'relax'].includes(kind) ? 'sit' : 'idle';
  const act = G.acts[want] || G.acts.idle; if (act && G.cur !== act) { if (G.cur) G.cur.fadeOut(0.3); act.reset().fadeIn(0.3).play(); G.cur = act; }
  G.mixer.update(dt); return true;
}
