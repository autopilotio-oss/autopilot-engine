// ---------------------------------------------------------------------------
// Live data
// ---------------------------------------------------------------------------
const live = { triggers: null, posts: null, kit: null, hub: null, at: {}, err: {} };
function deriveState(t) {
  if (!t.enabled) return 'OFFLINE';
  const lr = t.last_run || {}; const st = (lr.status || '').replace('ROUTINE_RUN_STATUS_', '');
  if (lr.fired_at && !lr.finished_at && st !== 'FAILED') return 'WORKING';
  if (st === 'RUNNING' || st === 'PENDING' || st === 'IN_PROGRESS') return 'WORKING';
  if (st === 'FAILED' || st === 'ERROR' || st === 'TIMED_OUT') return 'FAILED';
  if (st === 'SUCCEEDED' && lr.finished_at && Date.now() - new Date(lr.finished_at) < 20 * 60000) return 'COMPLETED';
  return 'IDLE';
}
function parseMaybe(p) {
  if (p && typeof p === 'object') return p;
  const s = String(p || ''); const i = s.indexOf('{');
  for (let j = s.lastIndexOf('}'), n = 0; j > i && n < 40; j = s.lastIndexOf('}', j - 1), n++) { try { return JSON.parse(s.slice(i, j + 1)); } catch (e) {} }
  return null;
}
