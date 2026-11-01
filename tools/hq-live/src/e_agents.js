
// ---------------------------------------------------------------------------
// Agents: live state keyed by scheduled task id. Floating HTML cards, no fake progress.
// ---------------------------------------------------------------------------
const agents = new Map();
const events = []; // session event log: only things this page actually observed
function logEvent(kind, text, agentId, color) { events.unshift({ at: Date.now(), kind, text, agentId, color: color || '#C8F53C' }); if (events.length > 200) events.pop(); if (curView === 'activity') renderView(); renderStatus(); }
const deptSlots = { exec: 0, content: 0, care: 0, finance: 0, systems: 0 };
const slotPos = (dept, n) => { const d = DEPTS[dept]; const col = n % 3, row = Math.floor(n / 3); return { x: d.x + (col - 1) * 3.9, z: d.z0 + row * 3.3, rot: 0 }; };
const deptFor = (want) => (deptSlots[want] < DEPTS[want].rows * 3 ? want : Object.keys(DEPTS).find((k) => deptSlots[k] < DEPTS[k].rows * 3) || want);
function identityFor(name) { const r = ROSTER.find((x) => x.re.test(name)); return r ? { ...r } : { code: name.replace(/[^A-Za-z]/g, '').slice(0, 6).toUpperCase() || 'AGENT', dept: 'systems', role: name, vibe: 'New hire.', hue: 0x1b1c1e }; }
const cardsEl = document.getElementById('cards');
function addAgent(id, name, ident, ghost) {
  const dept = deptFor(ident.dept); ident.dept = dept; const n = deptSlots[dept]++; const p = slotPos(dept, n);
  const desk = makeDesk(p.x, p.z, p.rot);
  const rig = makeOperative(agents.size, ident.hue);
  rig.root.position.set(p.x + 1.4, 0.25, p.z + 1.4); HQ.add(rig.root);
  rig.root.traverse((o) => { if (o.isMesh) o.userData.agentId = id; });
  desk.g.traverse((o) => { if (o.isMesh) o.userData.agentId = id; });
  const card = document.createElement('div'); card.className = 'card glass dot'; card.onclick = () => openInspector(id, true); card.onmouseenter = () => (hoverId = id); card.onmouseleave = () => { if (hoverId === id) hoverId = null; }; cardsEl.append(card);
  const a = { id, name, ident, desk, rig, card, state: ghost ? 'NOFEED' : 'WAITING', shownState: null, data: null, ghost: !!ghost,
    seat: new THREE.Vector3(p.x, 0.25, p.z + 0.95), stand: new THREE.Vector3(p.x + 1.5, 0.25, p.z + 1.6), pos: new THREE.Vector3(p.x + 1.5, 0.25, p.z + 1.6), phase: rnd() * 10 };
  agents.set(id, a); drawMonitor(a); drawCard(a); if (typeof heroState !== 'undefined' && heroState.loaded) attachHero(a, heroState.src, heroState.SU, heroState.scale); return a;
}
GH_WORKERS.forEach((w) => addAgent('gh:' + w.code, w.name, { code: w.code, dept: w.dept, role: w.role, vibe: 'Runs on GitHub Actions.', hue: 0x1b1c1e, wf: w.wf }, true).tools = w.tools);
const shortName = (a) => a.name.replace(/^AUTOPILOT\.OI\s*/i, '').replace(/\s*\(.*?\)\s*/g, ' ').trim();
function activity(a) {
  const d = a.data;
  if (a.ghost) { const g = a.gh; if (!g) return 'Waiting for the ANALYST feed'; if (a.state === 'WORKING') return 'Running now (as of ' + ago(live.hub.at) + ')'; if (a.state === 'FAILED') return 'Last run failed ' + ago(g.finished || g.started); return 'Last run ' + ago(g.finished || g.started) + (g.runs24h != null ? ' · ' + g.runs24h + ' runs in 24h' : ''); }
  if (!d) return 'Waiting for live feed';
  if (a.state === 'WORKING') return 'Run started ' + ago(d.last);
  if (a.state === 'FAILED') return 'Last run failed ' + ago(d.last);
  if (a.state === 'COMPLETED') return 'Finished ' + ago(d.finished);
  if (a.state === 'OFFLINE') return 'Paused by you';
  return d.next ? 'Next run ' + ago(d.next) : 'No run scheduled';
}
function drawCard(a) {
  const st = STATE[a.state];
  a.card.innerHTML = `<div class="n"><i style="background:${st.c};box-shadow:0 0 8px ${st.c}"></i>${a.ident.code}${a.state === 'WORKING' ? ico('M13 2L4 14h7l-1 8 9-12h-7z') : ''}</div>
<div class="r">${st.label} · ${DEPTS[a.ident.dept].name}</div><div class="a">${esc(activity(a))}</div>
${a.state === 'WORKING' ? '<div class="bar"><b></b></div><div class="l">Running · progress not reported</div>' : ''}`;
  a.card.style.borderColor = a.state === 'WORKING' ? 'var(--edge2)' : a.state === 'FAILED' ? '#5a2522' : '';
}
function drawMonitor(a) {
  const g = a.desk.cv.getContext('2d'), W = 256, H = 150, st = STATE[a.state];
  g.fillStyle = a.state === 'OFFLINE' || a.state === 'NOFEED' ? '#050606' : '#06100a'; g.fillRect(0, 0, W, H);
  if (a.state === 'OFFLINE') { a.desk.tex.needsUpdate = true; return; }
  g.fillStyle = st.c; g.font = 'bold 15px "Space Mono", monospace'; g.fillText(a.ident.code + ' · ' + st.label, 10, 22);
  g.fillStyle = '#7f8a74'; g.font = '11px "Space Mono", monospace';
  const d = a.data;
  const gh = a.gh; const lines = d ? [`last run  ${ago(d.last)}`, `result    ${d.status || 'n/a'}`, `next      ${ago(d.next)}`] : gh ? [`last run  ${ago(gh.finished || gh.started)}`, `result    ${(gh.conclusion || gh.status || "n/a").toUpperCase()}`, `24h runs  ${gh.runs24h ?? "n/a"}`] : a.ghost ? ['GitHub Actions worker', 'waiting for ANALYST feed'] : ['waiting for live feed'];
  lines.forEach((l, i) => g.fillText(l, 10, 46 + i * 16));
  for (let i = 0; i < 26; i++) { const h = a.state === 'WORKING' ? 6 + Math.abs(Math.sin(i * 1.7 + a.phase)) * 34 : 3 + (i % 5); g.fillStyle = a.state === 'FAILED' ? '#5a2522' : '#2c4a1a'; g.fillRect(10 + i * 9, H - 10 - h, 6, h); }
  a.desk.tex.needsUpdate = true;
}
function setState(a, s) {
  if (a.shownState === s) return;
  const prev = a.state; a.state = s; a.shownState = s; const st = STATE[s];
  if (prev && prev !== s && !['WAITING', 'NOFEED'].includes(prev)) logEvent('state', `${a.ident.code} ${STATE[prev].label} → ${st.label}`, a.id, st.c);
  a.desk.glow.material.color.set(st.c); drawMonitor(a); drawCard(a);
  a.rig.root.visible = s !== 'OFFLINE';
  const dim = s === 'NOFEED' || s === 'WAITING'; a.rig.hoodie.color.copy(new THREE.Color(dim ? 0x2b2d2a : a.ident.hue).lerp(new THREE.Color(0x2a2a2e), dim ? 0 : 0.55));
}
