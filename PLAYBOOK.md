# AUTOPILOT.OI content playbook (read this before writing any post)

## The business
- Brand: AUTOPILOT.OI (@autopilot.oi on Threads). Faceless. Mascot: AP, a lime robot with a black screen face.
- Free lead magnet: THE BUSINESS BRAIN, https://autopilotio-oss.github.io/autopilot-engine/ (keyword BRAIN)
- Paid: THE WORKSPACE, $49 one time, 30 day refund, 7 Claude agents set up in about an hour, https://autopilotio-oss.github.io/autopilot-engine/workspace/ (keyword WORKSPACE). Checkout: https://autopilotoi.gumroad.com/l/ttdat
- Audience: small business owners (trades, salons, shops, cleaners, bakers, roofers), not tech people.

## Hard rules
- Honest only. No fake testimonials, no invented results, no income claims, no fake scarcity or countdowns. Example numbers inside a demo must be clearly an example business.
- No dashes (" - ", " — ") anywhere in captions or graphics.
- Every post ends with ONE action: Comment BRAIN, Comment WORKSPACE, or a real question to reply to.
- Copy formats, hooks and structures from what works for others. Never copy their actual words, visuals or claims.
- Posts are 500 characters max. Times are US Eastern: -04:00 before Nov 1 2026, -05:00 after.
- Max 6 posts a day (bot limit). Default rhythm: 2 a day, ~9:00 and ~12:30 ET (Threads is a morning platform).
- Every post has an image or video. Text only is the weakest format on Threads.
- Mix: about 60% BRAIN (free), 30% WORKSPACE (paid), 10% pure conversation questions.
- Add "topic": "Small Business" or "AI Tools" to each post.

## Formats that convert (ranked)
1. Objection reel: "This Claude setup gives you X. First you might think... Second... Third..." each answered with a demo. CTA comment keyword.
2. Before/after or chatbot vs agent comparisons.
3. "Hard truth" money leak cards (slow replies, quotes with no follow up, no review asks).
4. Frameworks people save ("An AI agent is a new hire. It needs 4 things").
5. Honest limits / anti hype posts (build trust, sell WORKSPACE).
6. Questions that get owners talking about their busy work.

## How to make a card
Use tools/cards/p.html (poster style, Seb Oct 30: "less AI looking, more impact"). Pure black, no glow, no gradients, no grid. One huge Barlow Condensed Black Italic headline (one {lime} phrase), Geist body, Geist Mono labels, hairline rules, phone style message bubbles for examples, big lime keyword in the footer.
Copy one `<div class="k" id="p-...">` block, change the words, run `PAGE=p.html node render.js <id>` then `node check.js` (every card must show gap >= 0 and footer_inside=true) from tools/cards, and copy out/<id>.jpg to docs/media/cards/. The old glowing c.html cards are retired.
Media URL pattern: https://autopilotio-oss.github.io/autopilot-engine/media/cards/<file>.jpg

## Queue format
queue/*.json is a list of {"id","at","kind":"text|image|video|carousel","media":[urls],"topic","text"}. ids must be unique forever (posted ones are tracked in state/posted.json).

## Learning loop
state/insights.json has views/likes/replies per posted id. Each day: find the top 2 and bottom 2 posts, write more like the top, stop doing what the bottom did. Log what you learned in LEARNINGS.md (date, finding, change made).

## Instagram
When Instagram is connected (state/ig_token.enc exists), every image, video and carousel post is also published to Instagram automatically. Text only posts stay on Threads. Links become "Link in bio." and hashtags are added. Set "ig": false on a post to keep it Threads only. Reels do best on Instagram, so favor video.

## Seb approves every post
About 1 hour before each post, the bot opens a GitHub issue with the exact media and both captions and assigns it to Seb. It only posts after he replies YES. NO or no answer means it never posts. So every post must be elite: strong hook in the first line, a visual that stops the scroll, one clear CTA. Every new video needs a matching <name>-poster.jpg next to it in docs/media (used for the preview).

## Instagram style (Seb's call, Oct 30)
Instagram gets human, tweet style carousels only (tools/carousel: black background, ap. avatar, AUTOPILOT.OI @autopilot.oi, big simple text, lime accents, 1 to 10 slides, last slide CTA). Topics that teach total beginners Claude and AI in the simplest words, with viral titles like "The 3 things they don't want you to know about AI" or "Top AI prompts of 2026". Everything must be true. Set "threads": false on Instagram only posts. The robot graphics stay on Threads only ("ig": false). Threads gets more volume.
To make one: add a new key to tools/carousel/data.json, run node r.js inside tools/carousel, copy out/<key>/*.jpg to docs/media/carousels/<key>/.

## X (Twitter)
Every Instagram carousel is also posted on X as a text thread (one tweet per slide) at the same time, kind "x_thread" with a "tweets" list. Build it with scripts/xpost.py from_carousel(). Only the last tweet has a link (links cost more on X). Threads posts never go to Instagram; Instagram posts never go to Threads.

## Daily market story (Instagram Stories only)
.github/workflows/market.yml runs every morning (about 8 AM ET), pulls crypto (CoinGecko) and stock (Stooq) prices, renders an animated 9 second story video docs/media/stories/<date>.mp4 (tweet style, biggest mover as the hero with a 7 day chart, green or red mood) with scripts/market_story.py and queues it as an Instagram story an hour later. It waits for Seb's YES like everything else. Numbers only from the data, plain English, always "Not financial advice". Never predict prices or tell people what to buy.

## 5 Instagram stories a day (all black)
.github/workflows/market.yml ("Daily stories", about 7 AM ET) runs scripts/daily_stories.py: 8:30 market check video, 10:30 AI tip, 12:30 quiz question, 14:30 quiz answer, 18:00 poll (ET). Pure black background, InterDisplay type, lime accents. The API can't add real poll or quiz stickers, so stories ask people to reply A, B or C. Content rotates from tools/story/pool.json: keep adding fresh, true tips, quizzes and polls there (never repeat within 2 weeks). Seb approves all 5 with one YES (they share a "group").

## Type system (Seb approved Oct 30)
Headlines: Barlow Condensed Black Italic, UPPERCASE, emphasis words in lime (mark with {braces}). Body: Geist Medium/SemiBold. Labels: Geist Mono, uppercase, wide tracking. No serif, no thin weights, no glow. Pure black backgrounds with hairline rules and a header (logo, AUTOPILOT.OI, date, issue number). Helpers: scripts/typeset.py (headline, rich, label).

## Voice (Seb: "nothing cringe")
Write like a sharp operator texting a busy owner: calm, plain, specific, short. Never use: "they don't want you to know" (except the one carousel Seb named), "nobody tells you", "imagine", "be honest", "serious question", "secret", "hack", "game changer", "unlock", "level up", "AI employee", "zero/no tech words", hype emojis (👀🔥🚀), "it's live", "save this before", "most underrated". No fake urgency, no claims we can't back. One clear CTA. Read every line out loud: if it sounds like an ad or a guru, rewrite it.

## Real Facts (Snapple style) and quality bar for everything generated
Daily story at 4:30 PM ET: "AI FACT · NO. 0xx" from tools/story/pool.json "facts": a "whoa, AI can do that?" fact people can use today (most of them), with one {lime} phrase, one line of context and an optional "try" line (a prompt to copy). Only a few history facts, and only the jaw-dropping ones. Facts must be true and checkable: only add one after confirming it with a reliable source in a web search, and keep the wording precise (say "first recorded", "commonly credited" when that's the honest version). Topics: AI ONLY (history of AI, how chatbots and models work, milestones, AI companies and tools). No general tech or random trivia. No stats you can't source, no "studies show".
Quality bar for every tip, quiz, poll and fact: it must teach something useful or surprising in one read. If it's generic, obvious, preachy or sounds like an ad, don't use it.

## Trust first (Seb, Oct 30)
For now we teach, we don't sell. Instagram runs the "AI for Beginners" lesson series (Lesson 1, 2, 3... one a day, CTA = save/follow for the next lesson, no product pitches). Threads CTAs point only to the free Business Brain or a question, never THE WORKSPACE, until Seb says to start selling.

## Everyday fix story (Seb, Oct 30)
The 4:30 PM story is an "Everyday fix": a real problem normal people deal with (a bill, a lease, dinner, a hard email, homework) + how Claude solves it + the exact sentence to say to Claude. No trivia, no history, no scare facts. Never promise medical, legal or money outcomes; for health, "use it to prepare questions for your doctor".

## Approval OFF (Seb, Oct 30 10:14)
Seb: "I don't wanna approve, just post, we are behind." config/approval.json is false. Everything posts automatically at its slot, so the quality bar is on us: render and look at every image, reread every caption against the banned list before queuing. Seb can turn approval back on by asking.
