// Tools an agent uses, detected from words in its own standing orders (not invented).
const TOOL_RULES = [
  [/metricool/i, 'Metricool'], [/\bkit\b|newsletter|subscriber/i, 'Kit'], [/gmail|inbox|email/i, 'Gmail'], [/github|repo|commit|actions/i, 'GitHub'],
  [/gumroad/i, 'Gumroad'], [/web ?search|search the web|websearch|sources?/i, 'Web search'], [/meta ads|adspirer|ad set|campaign/i, 'Meta Ads'],
  [/carousel|build\.py|render|ffmpeg|reel/i, 'Render pipeline'], [/manychat/i, 'ManyChat'], [/claude docs|\bdoc\b/i, 'Docs'], [/scheduled task|trigger/i, 'Scheduler'],
];
// Who hands work to whom: from how the system is configured (FIRST SALES MODE plan), not from live telemetry.
const COLLAB = {
  WIRE: ['SCOUT', 'FACTORY', 'PULSE'], FOREMAN: ['JUDGE', 'REELS', 'HEALTH', 'CLOSER'], SHIELD: ['REPLY', 'POSTMAN'], LEDGER: ['TILL', 'COACH', 'ANALYST'], CLOSER: ['FOREMAN', 'JUDGE', 'TILL'],
  JUDGE: ['FOREMAN', 'ANALYST'], PULSE: ['HEALTH', 'DISPATCH', 'FOREMAN'], COACH: ['LEDGER', 'ANALYST', 'INK'], INK: ['POSTMAN', 'COACH'], SCOUT: ['WIRE', 'FACTORY'], MERCH: ['SCOUT', 'BUILDER'],
  POSTMAN: ['SHIELD', 'INK'], DISPATCH: ['FACTORY', 'RELAY', 'PULSE'], ANALYST: ['TILL', 'RELAY', 'HEALTH', 'COACH'], FACTORY: ['WIRE', 'SCOUT', 'DISPATCH'], BUILDER: ['HEALTH', 'SYNC', 'FOREMAN'],
  RELAY: ['DISPATCH', 'WIRE'], REELS: ['FOREMAN', 'JUDGE'], STORIES: ['WIRE'], REPLY: ['SHIELD', 'ANALYST'], TILL: ['LEDGER', 'ANALYST'], SYNC: ['TILL', 'BUILDER'], HEALTH: ['PULSE', 'BUILDER'], CI: ['HEALTH', 'BUILDER'],
};
// Workflow steps: read from the standing orders when they declare steps (numbered lines or CAPS headings).
function parseSteps(prompt) {
  const out = [];
  for (const raw of String(prompt || '').split(/\n+/)) {
    const l = raw.trim(); let m;
    if ((m = l.match(/^(?:step\s*)?(\d{1,2})[.)]\s+([^.:\n]{3,60})/i))) out.push(m[2].replace(/[*_#`]/g, '').trim());
    else if ((m = l.match(/^#{1,4}\s*(.{3,50})$/))) out.push(m[1].replace(/[*_`]/g, '').trim());
    else if ((m = l.match(/^\**([A-Z][A-Z0-9 +&/'-]{2,40})\**\s*[:—-]/))) out.push(m[1].trim());
    if (out.length >= 9) break;
  }
  return [...new Set(out)].map((s) => s.length > 42 ? s.slice(0, 40) + '…' : s);
}
const toolsFor = (prompt) => TOOL_RULES.filter(([re]) => re.test(prompt || '')).map(([, n]) => n);
const NAV = [
  ['exec', 'Executive', 'M3 12l9-8 9 8M5 10v10h14V10'], ['agents', 'Agents', 'M12 12a4 4 0 100-8 4 4 0 000 8zM4 21a8 8 0 0116 0'], ['workflows', 'Workflows', 'M5 6h4v4H5zM15 14h4v4h-4zM9 8h4a2 2 0 012 2v4'],
  ['tasks', 'Tasks', 'M9 6h11M9 12h11M9 18h11M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2'], ['content', 'Content', 'M4 5h16v14H4zM4 15l5-5 4 4 3-3 4 4'], ['publishing', 'Publishing', 'M4 12l16-8-6 16-3-7z'],
  ['automations', 'Automations', 'M12 3v3M12 18v3M3 12h3M18 12h3M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2M12 9a3 3 0 100 6 3 3 0 000-6z'], ['intel', 'Intelligence', 'M12 3a6 6 0 00-3 11v3h6v-3a6 6 0 00-3-11zM10 21h4'],
  ['analytics', 'Analytics', 'M4 20V10M10 20V4M16 20v-7M22 20H2'], ['finance', 'Finance', 'M12 2v20M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6'], ['integrations', 'Integrations', 'M9 7V3M15 7V3M7 7h10v5a5 5 0 01-10 0zM12 17v4'],
  ['activity', 'Activity', 'M3 12h4l3-8 4 16 3-8h4'], ['settings', 'Settings', 'M12 15a3 3 0 100-6 3 3 0 000 6zM19 12a7 7 0 00-.1-1l2-1.6-2-3.4-2.4 1a7 7 0 00-1.7-1L14.5 3h-5l-.3 2.6a7 7 0 00-1.7 1l-2.4-1-2 3.4 2 1.6a7 7 0 000 2l-2 1.6 2 3.4 2.4-1a7 7 0 001.7 1l.3 2.4h5l.3-2.6a7 7 0 001.7-1l2.4 1 2-3.4-2-1.6c.1-.3.1-.7.1-1z'],
];
const ico = (d) => `<svg class="i" viewBox="0 0 24 24"><path d="${d}"/></svg>`;
const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
const ago = (iso) => { if (!iso) return 'n/a'; const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000); if (m < 0) { const a = -m; return a < 60 ? `in ${a}m` : a < 1440 ? `in ${Math.round(a / 60)}h` : `in ${Math.round(a / 1440)}d`; } return m < 60 ? `${m}m ago` : m < 1440 ? `${Math.round(m / 60)}h ago` : `${Math.round(m / 1440)}d ago`; };
