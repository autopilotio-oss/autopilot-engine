function applyTriggers(list) {
  const first = !live.triggers; live.triggers = list;
  for (const t of list) {
    let a = agents.get(t.id);
    if (!a) a = addAgent(t.id, t.name, identityFor(t.name));
    const prevLast = a.data && a.data.last;
    a.data = { raw: t, status: ((t.last_run || {}).status || '').replace('ROUTINE_RUN_STATUS_', ''), last: (t.last_run || {}).fired_at || t.last_fired_at, finished: (t.last_run || {}).finished_at, next: t.next_run_at, cron: t.cron_expression || (t.run_once_at ? 'once ' + t.run_once_at : ''), prompt: (t.derived_state || {}).prompt || '' };
    a.steps = parseSteps(a.data.prompt); a.tools = toolsFor(a.data.prompt);
    if (!first && prevLast !== a.data.last && a.data.last) logEvent('run', `${a.ident.code} run fired`, a.id);
    a.name = t.name; a.shownState = null; setState(a, deriveState(t));
  }
  if (first) logEvent('feed', `Scheduler feed ${DEMO ? '(DEMO)' : 'live'}: ${list.length} scheduled agents`, null, '#7fd6ff');
  renderUI();
}
const postSeen = new Map();
function applyPosts(payload) {
  const rows = [];
  for (const p of (payload && payload.data) || []) for (const pr of p.providers || []) rows.push({ time: (p.publicationDate || {}).dateTime || '', net: pr.network, status: pr.status, draft: !!p.draft, text: String(p.text || '').split('\n')[0], url: pr.publicUrl || '' });
  const first = !live.posts; live.posts = rows;
  for (const r of rows) { const k = r.time + r.net + r.text; const was = postSeen.get(k); if (!first && was && was !== r.status) logEvent('post', `${(NETS.find((n) => n[0] === r.net) || [0, r.net])[1]} ${r.status.toLowerCase()}: ${r.text.slice(0, 48)}`, null, r.status === 'ERROR' ? '#ff5a4f' : '#C8F53C'); postSeen.set(k, r.status); }
  if (first) logEvent('feed', `Metricool feed ${DEMO ? '(DEMO)' : 'live'}: ${rows.length} posts today`, null, '#7fd6ff');
  renderUI(); spawnTransfers();
}
