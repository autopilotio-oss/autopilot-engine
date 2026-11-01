// ---------------------------------------------------------------------------
// Config: agent identities. Matched to real scheduled tasks by name. Anything
// that does not match still gets a desk, so no agent is ever dropped.
// ---------------------------------------------------------------------------
const DEMO = location.hash === '#demo'; // DEMO MODE: separate test data, never mixed with live feeds
const SERVERS = { remote: 'Claude Code Remote', metricool: 'Metricool Social Media Management', kit: 'Kit' };
const ROSTER = [ // first match wins: specific names before broad ones
  { re: /news desk/i, code: 'WIRE', dept: 'content', role: 'Breaks big AI and money news first as fact checked carousels.', vibe: 'Restless, always scanning headlines.', hue: 0x111214 },
  { re: /operator/i, code: 'FOREMAN', dept: 'exec', role: 'Runs FIRST SALES MODE each morning: factory reels, funnels, ads, scoreboard.', vibe: 'Calm, decisive, owns the plan.', hue: 0x0e0f10 },
  { re: /final report/i, code: 'CLOSER', dept: 'exec', role: 'Writes the FIRST SALES MODE final report on Nov 11.', vibe: 'Waits for the numbers, then talks.', hue: 0x0f1012 },
  { re: /support|inbox/i, code: 'SHIELD', dept: 'care', role: 'Reads the inbox, drafts replies, opens incidents. Never sends on its own.', vibe: 'Patient and careful.', hue: 0x141517 },
  { re: /monthly|scale review/i, code: 'LEDGER', dept: 'finance', role: 'Monthly scale review: finances, portfolio, next month priorities.', vibe: 'Quiet, counts everything twice.', hue: 0x101113 },
  { re: /test result|reel test/i, code: 'JUDGE', dept: 'finance', role: 'Reads the factory reel test results and gives the verdict.', vibe: 'Blunt, data first.', hue: 0x131416 },
  { re: /analyst/i, code: 'ANALYST', dept: 'finance', role: 'Hourly: Metricool and Kit numbers, scoreboard, winners, and the live feed for this HQ.', vibe: 'Lives in the numbers.', hue: 0x121416 },
  { re: /draft factory/i, code: 'FACTORY', dept: 'content', role: 'Every 2 hours: builds and QA checks carousel drafts into the ready bank. Never posts.', vibe: 'Heads down, always shipping drafts.', hue: 0x141416 },
  { re: /site improver/i, code: 'BUILDER', dept: 'systems', role: 'Every 3 hours: improves one guide or page for conversion. Never touches prices.', vibe: 'Tinkerer, tests on a phone first.', hue: 0x131517 },
  { re: /pulse/i, code: 'PULSE', dept: 'systems', role: 'Daily Pulse: health, unapproved post guard, daily report.', vibe: 'Never misses a heartbeat.', hue: 0x111215 },
  { re: /newsletter/i, code: 'INK', dept: 'content', role: 'Drafts the weekly newsletter for your approval.', vibe: 'Wordsmith, hates fluff.', hue: 0x131315 },
  { re: /tiktok shop/i, code: 'MERCH', dept: 'content', role: 'Keeps TikTok Shop knowledge current, weekly.', vibe: 'Knows every fee and rule.', hue: 0x141517 },
  { re: /kit welcome|kit sync/i, code: 'POSTMAN', dept: 'systems', role: 'Routes new subscribers into the right Kit welcome sequence every 3 hours.', vibe: 'Never loses a letter.', hue: 0x121315 },
  { re: /publisher/i, code: 'DISPATCH', dept: 'content', role: 'Schedules only content the approval code marks allowed.', vibe: 'Strict at the door.', hue: 0x111315 },
  { re: /sprint|weekly/i, code: 'COACH', dept: 'finance', role: 'Weekly sprint: picks the one experiment and writes the weekly report.', vibe: 'Pushes the team, keeps score.', hue: 0x121315 },
  { re: /trend|scout|viral/i, code: 'SCOUT', dept: 'content', role: 'Finds trends and proven formats before anyone else. Research only.', vibe: 'Curious, always on the phone.', hue: 0x151618 },
];
const GH_WORKERS = [ // GitHub Actions workers. Live status arrives through the ANALYST feed (status/hub in this page's database).
  { code: 'RELAY', tools: ['GitHub', 'Threads API'], wf: 'post.yml', name: 'Post to Threads (GitHub Actions)', dept: 'content', role: 'Every 15 minutes: publishes the approved Threads queue.' },
  { code: 'REELS', tools: ['GitHub', 'Render pipeline', 'ElevenLabs'], wf: 'freel.yml', name: 'Factory reels render (GitHub Actions)', dept: 'content', role: 'Daily 06:07 ART: renders the next factory reels.' },
  { code: 'STORIES', tools: ['GitHub', 'Render pipeline'], wf: 'market.yml', name: 'Daily stories (GitHub Actions)', dept: 'content', role: 'Daily: builds the stories set.' },
  { code: 'REPLY', tools: ['GitHub', 'Threads API', 'Metricool'], wf: 'daily.yml', name: 'Stats and comment replies (GitHub Actions)', dept: 'care', role: 'Hourly: collects stats and replies to comments.' },
  { code: 'TILL', tools: ['GitHub', 'Gumroad'], wf: 'revenue.yml', name: 'Revenue ledger (GitHub Actions)', dept: 'finance', role: 'Every 3 hours: Gumroad sales and site numbers into the ledger.' },
  { code: 'SYNC', tools: ['GitHub', 'Gumroad'], wf: 'gumroad.yml', name: 'Gumroad products (GitHub Actions)', dept: 'finance', role: 'Every 6 hours: keeps products, files and codes in sync.' },
  { code: 'HEALTH', tools: ['GitHub', 'Site checks'], wf: 'health.yml', name: 'Growth OS health checks (GitHub Actions)', dept: 'systems', role: 'Hourly: site, checkout and page checks.' },
  { code: 'CI', tools: ['GitHub', 'pytest'], wf: 'ci.yml', name: 'Tests (GitHub Actions)', dept: 'systems', role: 'Runs the test suite on every push.' },
];
const DEPTS = { // desk grid per department: 3 columns, rows 3.3 apart from z0
  exec: { name: 'Executive', x: 0, z: -7.5, z0: -9.2, rows: 2 },
  content: { name: 'Content + Research', x: -11, z: 4.8, z0: 1.4, rows: 3 },
  care: { name: 'Customer Support', x: 11, z: 3, z0: 1.4, rows: 2 },
  finance: { name: 'Finance + Analytics', x: 11, z: -6, z0: -9.2, rows: 3 },
  systems: { name: 'Systems + Automation', x: -11, z: -6, z0: -9.2, rows: 3 },
};
const STATE = {
  WORKING: { c: '#D4FF3A', label: 'WORKING' }, COMPLETED: { c: '#7fd6ff', label: 'COMPLETED' }, IDLE: { c: '#9aa18f', label: 'ON CALL' },
  FAILED: { c: '#ff5a4f', label: 'FAILED' }, OFFLINE: { c: '#666', label: 'PAUSED' }, NOFEED: { c: '#4a4d45', label: 'FEED PENDING' }, WAITING: { c: '#4a4d45', label: 'WAITING FOR FEED' },
};
