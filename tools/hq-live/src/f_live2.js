function errText(code, server) {
  return ({ needs_reauth: [`reconnect ${server} in Settings`], server_not_connected: [`add ${server} in Settings`], selection_required: ['choose a connector'], not_in_manifest: ['not allowed here'], blocked_by_policy: ['blocked by policy'], approval_required: ['needs your OK', 'Allow'], not_granted: ['open this page in Claude'], capability_disabled: ['open this page in Claude'], server_unavailable: ['temporarily down'] })[code] || ['unavailable'];
}
let mcp = null; const srv = { ...SERVERS };
async function connect() {
  if (DEMO) return simulate();
  connectDb();
  try { mcp = await window.claude?.use?.('mcp'); } catch (e) { mcp = null; }
  if (!mcp) { ['triggers', 'posts', 'kit'].forEach((k) => (live.err[k] = { text: 'open this page in Claude' })); renderUI(); return; }
  try { // resolve the real display names of the connectors
    const lt = await mcp.listTools(); const names = (lt.servers || []).map((s) => s.server);
    const pick = (re, d) => names.find((n) => re.test(n.replace(/[_\s-]/g, ''))) || d;
    srv.remote = pick(/claudecoderemote/i, srv.remote); srv.metricool = pick(/metricool/i, srv.metricool); srv.kit = pick(/^kit$/i, srv.kit);
  } catch (e) {}
  watch('triggers', srv.remote, 'list_triggers', { enabled: true, limit: 50 }, async (payload) => {
    let page = parseMaybe(payload); if (!page) throw new Error('unreadable');
    const all = [...(page.data || [])]; let guard = 0;
    while (page.has_more && page.next_cursor && guard++ < 4) { const r = await mcp.callTool(srv.remote, 'list_triggers', { enabled: true, limit: 50, cursor: page.next_cursor }); page = parseMaybe(r.payload) || {}; all.push(...(page.data || [])); }
    applyTriggers(all);
  }, 60000);
  const day = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Argentina/Buenos_Aires', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
  watch('posts', srv.metricool, 'getScheduledPosts', { brandId: '7761544', fromDate: day + 'T00:00:00-03:00', toDate: day + 'T23:59:00-03:00', timezone: 'America/Argentina/Buenos_Aires' }, (p) => applyPosts(parseMaybe(p)), 120000);
  watch('kit', srv.kit, 'get_growth_stats', {}, (p) => { const o = parseMaybe(p) || {}; live.kit = o.stats || o; renderUI(); }, 600000);
}
function watch(key, server, tool, input, onData, every) {
  mcp.watchTool(server, tool, input, async (ev) => {
    if (ev.type === 'data') {
      try { await onData(ev.result.payload ?? ev.result); live.at[key] = ev.result.cache ? ev.result.cache.storedAt : Date.now(); live.err[key] = null; }
      catch (e) { live.err[key] = { text: 'unreadable answer' }; }
    } else {
      const code = ev.error && ev.error.code; const [text, action] = errText(code, server);
      live.err[key] = { text, action, fn: async () => { try { const r = await mcp.callTool(server, tool, input); await onData(r.payload ?? r); live.err[key] = null; live.at[key] = Date.now(); } catch (e) { toast('Still not allowed: ' + (e.code || 'error')); } renderUI(); } };
      if (['needs_reauth', 'server_not_connected', 'blocked_by_policy', 'approval_required', 'not_in_manifest'].includes(code)) { live[key] = null; }
    }
    renderUI();
  }, { refetchInterval: every });
}

// CEO actions: real, on your own scheduled tasks, always behind a confirm
async function act(a, kind) {
  if (!mcp) return toast('Actions work when this page is open in Claude.');
  const label = kind === 'run' ? `Start a real run of ${a.name} now?` : kind === 'pause' ? `Pause ${a.name}? It stops firing until you resume it.` : `Resume ${a.name} on its normal schedule?`;
  if (!(await confirmBox(label))) return;
  try {
    if (kind === 'run') await mcp.callTool(srv.remote, 'fire_trigger', { trigger_id: a.id });
    else await mcp.callTool(srv.remote, 'update_trigger', { trigger_id: a.id, enabled: kind === 'resume' });
    toast(kind === 'run' ? `${a.ident.code} is on it.` : kind === 'pause' ? `${a.ident.code} paused.` : `${a.ident.code} back on shift.`);
    logEvent('action', `You: ${kind} ${a.ident.code}`, a.id, '#ffc94a');
    try { await mcp.invalidate(srv.remote, 'list_triggers'); } catch (e) {}
  } catch (e) {
    toast(e.code === 'server_unavailable' || e.code === 'upstream_error' ? 'No answer yet. It may have gone through: check the agent before trying again.' : 'Not done: ' + (e.code || 'error'));
  }
}
function confirmBox(text) {
  return new Promise((res) => { const m = document.getElementById('modal'); document.getElementById('mText').textContent = text; m.hidden = false;
    const done = (v) => { m.hidden = true; res(v); }; document.getElementById('mYes').onclick = () => done(true); document.getElementById('mNo').onclick = () => done(false); });
}
