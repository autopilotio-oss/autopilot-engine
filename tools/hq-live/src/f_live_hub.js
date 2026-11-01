// ---- ANALYST feed: GitHub Actions workers, verified revenue (Gumroad ledger), approvals waiting.
// The hourly ANALYST scheduled task writes status/hub into this page's own database. Older than 2.5h = stale.
function hubStale() { return !live.hub || Date.now() - Date.parse(live.hub.at) > 2.5 * 3600e3; }
function ghState(g) {
  if (!g || hubStale()) return 'NOFEED';
  if (g.status === 'in_progress' || g.status === 'queued') return 'WORKING';
  if (g.conclusion === 'failure' || g.conclusion === 'timed_out') return 'FAILED';
  if (g.conclusion === 'success' && g.finished && Date.now() - Date.parse(g.finished) < 20 * 60000) return 'COMPLETED';
  return 'IDLE';
}
function applyHub(d) {
  if (!d || !d.at) return;
  const first = !live.hub; live.hub = d; live.at.hub = Date.parse(d.at);
  live.err.hub = hubStale() ? { text: 'stale since ' + ago(d.at) } : null;
  for (const a of agents.values()) if (a.ghost && a.ident.wf) { a.gh = (d.github || {})[a.ident.wf] || null; a.shownState = null; setState(a, ghState(a.gh)); }
  if (first) logEvent('feed', `ANALYST feed ${DEMO ? '(DEMO)' : 'live'}: GitHub workers, revenue ledger, approvals (as of ${ago(d.at)})`, null, '#7fd6ff');
  renderUI();
}
async function connectDb() {
  let db = null; try { db = await window.claude?.use?.('db'); } catch (e) { db = null; }
  if (!db) { live.err.hub = { text: 'open this page in Claude' }; renderUI(); return; }
  const timer = setTimeout(() => { if (!live.hub) { live.err.hub = { text: 'not reachable yet' }; renderUI(); } }, 10000);
  try {
    db.doc('status/hub').onSnapshot((snap) => { clearTimeout(timer); if (snap.exists) applyHub(snap.data()); else { live.err.hub = { text: 'no ANALYST report yet' }; renderUI(); } },
      (e) => { clearTimeout(timer); live.err.hub = { text: 'feed error: ' + (e && e.code || 'unavailable') }; renderUI(); });
  } catch (e) { clearTimeout(timer); live.err.hub = { text: 'feed error' }; renderUI(); }
}
const money = (r) => { if (!r) return null; const n = r.net_7d || {}; const k = Object.keys(n); return k.length ? k.map((c) => (c === 'USD' ? '$' : c + ' ') + Number(n[c]).toFixed(0)).join(' · ') : '$0'; };
