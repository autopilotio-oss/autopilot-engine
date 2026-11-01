
// ---------------------------------------------------------------------------
// Wall dashboards + map table: drawn only from feeds this page receives
// ---------------------------------------------------------------------------
const NC = 'NOT CONNECTED';
const P_ = () => (live.posts || []).filter((p) => !p.draft);
function counts() {
  const T = live.triggers, P = P_();
  const A = [...agents.values()];
  const withRun = A.filter((a) => (a.data && a.data.raw.enabled && a.data.status) || (a.gh && a.gh.conclusion));
  return {
    running: T ? A.filter((a) => a.state === 'WORKING').length : null,
    onShift: T ? T.filter((t) => t.enabled).length : null,
    total: T ? T.length : null,
    queued: live.posts ? P.filter((p) => p.status === 'PENDING').length : null,
    published: live.posts ? P.filter((p) => p.status === 'PUBLISHED').length : null,
    failedPosts: live.posts ? P.filter((p) => p.status === 'ERROR').length : null,
    subs: live.kit ? (live.kit.subscribers ?? 0) : null,
    next24: T ? T.filter((t) => t.enabled && t.next_run_at && new Date(t.next_run_at) - Date.now() < 864e5).length : null,
    health: T && withRun.length ? Math.round(100 * withRun.filter((a) => (a.data ? a.data.status !== 'FAILED' : a.gh.conclusion !== 'failure')).length / withRun.length) : null,
    failedAgents: T ? A.filter((a) => a.state === 'FAILED').length : null,
    revenue: live.hub && !hubStale() ? money(live.hub.revenue) : null, orders7: live.hub && live.hub.revenue ? live.hub.revenue.orders_7d : null,
    approvals: live.hub && !hubStale() && live.hub.approvals ? live.hub.approvals.count : null,
  };
}
const dash = (v) => (v == null ? '—' : String(v));
function panelHead(g, W, title, sub) {
  g.fillStyle = '#05080a'; g.fillRect(0, 0, W, 9999);
  const gr = g.createLinearGradient(0, 0, W, 0); gr.addColorStop(0, 'rgba(200,245,60,.10)'); gr.addColorStop(1, 'rgba(200,245,60,0)'); g.fillStyle = gr; g.fillRect(0, 0, W, 84);
  g.fillStyle = '#C8F53C'; g.fillRect(28, 24, 8, 38);
  g.fillStyle = '#eef0e6'; g.font = '600 40px "Chakra Petch", sans-serif'; g.fillText(title, 50, 57);
  g.fillStyle = '#7f8a74'; g.font = 'bold 24px "Space Mono", monospace'; g.textAlign = 'right'; g.fillText(sub, W - 28, 55); g.textAlign = 'left';
}
function drawWalls(t = 0) {
  const c = counts();
  // LEFT: live operations
  { const { g, W, H, tex } = wallL; panelHead(g, W, 'LIVE OPERATIONS', DEMO ? 'DEMO MODE' : 'LIVE');
    const tiles = [['Agents running', c.running], ['On shift', c.onShift], ['Posts out today', c.published], ['Queued today', c.queued], ['Kit subscribers', c.subs], ['Revenue 7d', c.revenue ?? NC]];
    tiles.forEach(([k, v], i) => { const x = 28 + (i % 3) * 328, y = 100 + Math.floor(i / 3) * 186;
      g.fillStyle = '#0b1210'; g.fillRect(x, y, 312, 172); g.strokeStyle = '#26321f'; g.lineWidth = 2; g.strokeRect(x + 1, y + 1, 310, 170);
      g.fillStyle = '#7f8a74'; g.font = '600 24px "Chakra Petch"'; g.fillText(k.toUpperCase(), x + 18, y + 40);
      const nc = v === NC; g.fillStyle = nc ? '#8a7a45' : '#eef0e6'; g.font = nc ? '600 32px "Chakra Petch"' : '600 100px "Chakra Petch"'; g.fillText(nc ? NC : dash(v), x + 18, y + (nc ? 118 : 150)); });
    g.fillStyle = '#7f8a74'; g.font = '20px "Space Mono"'; g.fillText('Scheduler · Metricool · Kit · Gumroad ledger', 28, H - 22); tex.needsUpdate = true; }
  // CENTER: workflow engine (real pipeline, flows animate only where the feed shows activity)
  { const { g, W, H, tex } = wallC; panelHead(g, W, 'WORKFLOW ENGINE · CONTENT PIPELINE', 'today, ART');
    const wire = [...agents.values()].find((a) => a.ident.code === 'WIRE'), fore = [...agents.values()].find((a) => a.ident.code === 'FOREMAN');
    const nodes = [
      ['NEWS DESK', wire ? STATE[wire.state].label : '—', wire && wire.state === 'WORKING'], ['OPERATOR', fore ? STATE[fore.state].label : '—', fore && fore.state === 'WORKING'],
      ['QA GATE 85/100', 'in build', null], ['METRICOOL QUEUE', dash(c.queued) + ' queued', c.queued > 0], ['PUBLISHED', dash(c.published) + ' live', c.published > 0], ['FAILED', dash(c.failedPosts), c.failedPosts > 0],
    ];
    const pos = [[30, 112], [30, 332], [330, 222], [620, 222], [920, 112], [920, 332]];
    const edges = [[0, 2, nodes[0][2]], [1, 2, nodes[1][2]], [2, 3, nodes[0][2] || nodes[1][2]], [3, 4, c.published > 0], [3, 5, c.failedPosts > 0]];
    for (const [a, b, on] of edges) { const [x1, y1] = pos[a], [x2, y2] = pos[b]; const sx = x1 + 230, sy = y1 + 54, ex = x2, ey = y2 + 54;
      g.strokeStyle = on ? 'rgba(200,245,60,.55)' : '#1f2a1c'; g.lineWidth = 5; g.beginPath(); g.moveTo(sx, sy); g.bezierCurveTo(sx + 60, sy, ex - 60, ey, ex, ey); g.stroke();
      if (on) for (let k = 0; k < 3; k++) { const u = ((t * 0.35 + k / 3) % 1); const bx = (1 - u) ** 3 * sx + 3 * (1 - u) ** 2 * u * (sx + 60) + 3 * (1 - u) * u * u * (ex - 60) + u ** 3 * ex; const by = (1 - u) ** 3 * sy + 3 * (1 - u) ** 2 * u * sy + 3 * (1 - u) * u * u * ey + u ** 3 * ey; g.fillStyle = '#e9ff9a'; g.beginPath(); g.arc(bx, by, 8, 0, 7); g.fill(); } }
    nodes.forEach(([name, sub, on], i) => { const [x, y] = pos[i]; const red = i === 5 && on;
      g.fillStyle = on ? (red ? '#2a0f0d' : '#142010') : '#0b1210'; g.fillRect(x, y, 230, 108); g.strokeStyle = on ? (red ? '#ff5a4f' : '#C8F53C') : '#2c3a24'; g.lineWidth = 3; g.strokeRect(x + 1.5, y + 1.5, 227, 105);
      g.fillStyle = '#eef0e6'; g.font = '600 25px "Chakra Petch"'; g.fillText(name, x + 16, y + 42); g.fillStyle = on ? (red ? '#ff8a80' : '#C8F53C') : '#7f8a74'; g.font = 'bold 22px "Space Mono"'; g.fillText(sub, x + 16, y + 82); });
    g.fillStyle = '#7f8a74'; g.font = '19px "Space Mono"'; g.fillText('Flows move only on reported activity · QA scores: not wired here', 28, H - 18); tex.needsUpdate = true; }
  // RIGHT: alerts + system health
  { const { g, W, H, tex } = wallR; panelHead(g, W, 'ALERTS · SYSTEM HEALTH', c.health == null ? '—' : c.health + '% runs OK');
    const al = alerts(); if (!al.length) { g.fillStyle = '#3bd16f'; g.font = '600 34px "Chakra Petch"'; g.fillText(live.triggers || live.posts ? 'No failures reported' : 'Waiting for feeds', 28, 140); }
    al.slice(0, 4).forEach((x, i) => { const y = 100 + i * 82; g.fillStyle = '#140b0a'; g.fillRect(28, y, W - 56, 72); g.fillStyle = x.c; g.fillRect(28, y, 8, 72); g.fillStyle = '#eef0e6'; g.font = '600 28px "Chakra Petch"'; g.fillText(x.title.slice(0, 44), 52, y + 32); g.fillStyle = '#a7ae9c'; g.font = '19px "Space Mono"'; g.fillText(x.sub.slice(0, 64), 52, y + 60); });
    const feeds = [['Scheduler', 'triggers'], ['Metricool', 'posts'], ['Kit', 'kit']]; feeds.forEach(([n, k], i) => { const x = 28 + i * 330, y = H - 76; const ok = !!live[k] && !live.err[k]; g.fillStyle = ok ? '#3bd16f' : live.err[k] ? '#ff5a4f' : '#4a4d45'; g.beginPath(); g.arc(x + 10, y + 8, 10, 0, 7); g.fill(); g.fillStyle = '#d7dccf'; g.font = '22px "Space Mono"'; g.fillText(n + (ok ? ' live' : live.err[k] ? ' down' : ' …'), x + 28, y + 16); });
    g.fillStyle = '#a8955a'; g.font = '19px "Space Mono"'; g.fillText(live.hub ? `ANALYST feed ${hubStale() ? 'stale' : 'live'} · as of ${ago(live.hub.at)} · Ads: ${NC}` : 'ANALYST feed · Ads: ' + NC, 28, H - 18); tex.needsUpdate = true; }
  drawMap(t);
}
function alerts() {
  const out = [];
  for (const a of agents.values()) if (a.state === 'FAILED') out.push({ c: '#ff5a4f', title: `${a.ident.code} last run failed`, sub: `${shortName(a)} · ${ago(a.data ? a.data.last : a.gh && (a.gh.finished || a.gh.started))}`, id: a.id });
  for (const p of P_()) if (p.status === 'ERROR') out.push({ c: '#ff5a4f', title: `Post failed on ${p.net}`, sub: `${p.time.slice(11, 16)} · ${p.text}` });
  for (const [k, n] of [['triggers', 'Scheduler'], ['posts', 'Metricool'], ['kit', 'Kit'], ['hub', 'ANALYST']]) if (live.err[k]) out.push({ c: '#ffc94a', title: `${n} feed: ${live.err[k].text}`, sub: 'Data from this source is not shown until it reconnects' });
  return out;
}
function drawMap(t) {
  const g = mapCv.getContext('2d'), W = 1024, H = 540; g.clearRect(0, 0, W, H);
  g.fillStyle = 'rgba(8,16,10,.92)'; g.fillRect(0, 0, W, H);
  g.strokeStyle = 'rgba(200,245,60,.16)'; g.lineWidth = 1; for (let x = 0; x < W; x += 32) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); } for (let y = 0; y < H; y += 32) { g.beginPath(); g.moveTo(0, y); g.lineTo(W, y); g.stroke(); }
  g.strokeStyle = 'rgba(200,245,60,.4)'; g.lineWidth = 3; g.beginPath(); g.moveTo(0, 300); g.lineTo(W, 260); g.moveTo(420, 0); g.lineTo(470, H); g.moveTo(760, 0); g.bezierCurveTo(700, 200, 820, 360, 760, H); g.stroke();
  g.fillStyle = 'rgba(127,214,255,.25)'; g.beginPath(); g.moveTo(W, 0); g.lineTo(880, 0); g.bezierCurveTo(900, 200, 860, 380, 920, H); g.lineTo(W, H); g.fill();
  g.fillStyle = '#C8F53C'; g.font = '600 26px "Chakra Petch"'; g.fillText('CHICAGO HQ · NETWORK REACH TODAY', 26, 42); g.fillStyle = '#7f8a74'; g.font = '16px "Space Mono"'; g.fillText(live.posts ? 'Pins = posts published today (Metricool)' : 'Waiting for Metricool', 26, 70);
  const P = P_(); pins.forEach((p) => { const n = live.posts ? P.filter((x) => x.net === p.net && x.status === 'PUBLISHED').length : null; p.n = n;
    const px = (NETS.find((x) => x[0] === p.net)[2] / 6.2 + 0.5) * W, py = (NETS.find((x) => x[0] === p.net)[3] / 3.26 + 0.5) * H;
    g.fillStyle = '#eef0e6'; g.font = '600 22px "Chakra Petch"'; g.fillText(`${p.label} ${dash(n)}`, px + 18, py + 8); });
  mapTex.needsUpdate = true;
}
const packets = [];
function spawnTransfers() {
  const recent = P_().filter((p) => p.status === 'PUBLISHED');
  const seen = spawnTransfers.seen || (spawnTransfers.seen = new Set());
  for (const p of recent) {
    const key = p.time + p.net + p.text; if (seen.has(key)) continue; seen.add(key);
    const isNews = /breaking|security alert|banks|this week in ai|anthropic|binance/i.test(p.text);
    const src = [...agents.values()].find((a) => (isNews ? /news desk/i : /operator/i).test(a.name)); if (!src) continue;
    const m = new THREE.Mesh(new THREE.OctahedronGeometry(0.18), new THREE.MeshBasicMaterial({ color: 0xC8F53C, toneMapped: false }));
    m.position.copy(src.seat).setY(1.6); HQ.add(m);
    const pin = pins.find((x) => x.net === p.net); const to = pin ? new THREE.Vector3(pin.col.position.x, 1.6, pin.col.position.z + 1.2) : new THREE.Vector3(0, 3, -hqD / 2 + 1);
    packets.push({ m, from: m.position.clone(), to, t: -packets.length * 0.6, dur: 3.2 });
  }
}
