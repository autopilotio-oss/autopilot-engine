# AUTOPILOT.OI content playbook (read this before writing any post)

## The business
- Brand: AUTOPILOT.OI (@autopilot.oi on Threads). Faceless. Mascot: AP, a lime robot with a black screen face.
- Free lead magnet: THE BUSINESS BRAIN, https://autopilotio-oss.github.io/autopilot-engine/brain/ (keyword BRAIN). The site root is the link in bio home page.
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
UPDATE (Seb, Oct 30): daily Instagram carousels now use the v2 studio style (black and lime, heavy Inter Display Black caps with white + lime two tone headlines, letter spaced tags with a lime bar, lime glow and diagonal lime slabs, white tweet cards, "PASTE THIS INTO CLAUDE" prompt cards, a lime paper note slide, numbered 01 / 07 pages, AUTOPILOT.OI wordmark footer). Reference: Seb liked @bleverdigital's grid; match the feel, never copy their logo, bolt or lines. Slide types in tools/carousel/t2.html: hook, step, tweet, prompt, lime, cta. To make one: add a key to tools/carousel/data2.json, run node r2.js <key> inside tools/carousel, copy out/<key>/*.jpg to docs/media/carousels/<key>/. One per day, 6 to 8 slides, alternate black and lime slides, every claim true and checkable. Topics: real money and life problems solved with AI for total beginners (credit, bills, debt, budgeting, job hunting, writing). Last slide asks for a comment keyword that has a live ManyChat automation (CREDIT is live first; check before using BILL, DEBT, BRAIN).

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

## Posting cadence (set Oct 30, research based)
New account, so we run hot but never past where each post starts eating the next one's reach.
- Threads: 4 a day, all before 4 PM ET (evenings 6 to 11 PM are the weakest slots in Buffer's 2.5M post data). Slots ET: 7:30 text tip, 9:00 main post (video or image), 12:30 second post, 3:30 Everyday Fix card. Never more than 5 (dilution). Replying to comments lifts engagement ~42%, so keyword replies stay on.
- Instagram feed: 1 carousel every day (lessons), target 10+ feed posts a week once reels exist (Buffer: 10+/week = fastest follower growth). Reels 3 to 4 a week when we have voice or footage.
- Instagram stories: 6 a day (already above the 2 to 5 baseline; brands posting 30+ frames a week had the best completion).
- X: every IG carousel as a thread + 2 to 3 single posts a day once X is connected.
- API ceilings are not a factor: Instagram 100 posts per 24h, Threads 250 per 24h.
If a slot's posts score in the bottom 3 for a week, move or drop that slot.

## Money series + agents (Seb, Oct 30)
Main content now: real money problems solved with Claude, in the AP robot reel format (objections reel style, ElevenLabs voice). Every reel ends with a comment keyword that sends a free guide (docs/g/<slug>/, built by tools/guides/build.py from tools/guides/guides.py). Every guide ends with "make it automatic": a Claude Project agent setup, and a waitlist for done-for-you agent setups (planned upsell: $10 per agent, later, Seb decides when). Topics: CREDIT, BILL, DEBT live; next LEAKS, RAISE, LOWER, BUDGET, DISPUTE, DEPOSIT, LEASE, SIDE, TAXES. Rules: education only, never promise results, only dispute what is wrong, no upfront-fee services, cite official sources (FTC, CFPB, CMS).
- Voices: ElevenLabs "Brian - Deep, Resonant and Comforting" (eleven v4). ALWAYS speed every voice to 1.2x (Seb, Oct 30). Reels use the AP robot template in the money reel engine.
- Reel captions: Saira SemiCondensed BlackItalic, uppercase, 82px, lime emphasis, placed low just above the robot (eye line, keeps people locked in); visuals sit at the top; card text Geist Bold. Seb, Oct 30.
- Reel studio look (Seb, Oct 30): segmented progress bar with seconds left at the top, drifting lime light + grain + vignette background (no grid), cards with gradient edges and a shine sweep, 3D tilt and blur entrances, word by word captions with the active word popping, camera kick + flash on scene changes, scenes crossfade (never a blank frame). Source in tools/reel (needs the AP presenter frames and fonts locally).

## Instagram publishing = Metricool (Oct 30)
Meta blocked our app (every call returns "API access blocked"). Instagram now goes through Metricool (brand id 7761544, connected to @autopilot.oi). Claude schedules IG posts with the Metricool connector (createScheduledPost: REEL needs video + videoThumbnailUrl, carousel = POST with several images, STORY = image with no text). GitHub no longer posts to Instagram (config/instagram.json). Threads still posts from GitHub.

## Morning trend scout (Seb, Oct 30)
Every morning find what's viral or trending that we can genuinely help with: AI agent news, new AI features normal people can use, and money or everyday problems trending (scams, fees, price hikes, tax deadlines, bills). Only post when we add real value (a fix, a prompt, a clear explanation). Never fake news, never hype, always check 2 sources, name the source on the card. Card: python scripts/daily_stories.py trend '<json>' docs/media/trends/<date>-<slug>.jpg  (keys: tag, h with {lime} words, what, do, do_label, src).

## Products (Gumroad, automatic)
Paid kits: $10 per agent, bundles $24. A product = products/<permalink>/product.json + sealed file (bash tools/kits/seal.sh <pdf> products/<permalink>). Pushing it runs .github/workflows/gumroad.yml, which creates and publishes it on Gumroad (secrets GUMROAD_TOKEN, KIT_PRIVATE_KEY) and writes state/products.json. Never commit an unsealed paid PDF (tools/kits/out is gitignored). Kit PDF: python tools/kits/build.py <kit.json> <out.pdf> (keys: name, price, tag, promise, setup[], master, starters[[title,prompt]], tracker[], links[[title,url]]). Cover: tools/kits/covers.py style, saved to docs/store/<key>-cover.png. Add every new product to docs/store/index.html.

## Stories value gate (Seb, Oct 30 13:49: "I don't like the stories, only post after making sure it's something someone finds of value")
Stories are paused by default. No story is scheduled in Metricool unless it passes ALL of these, checked on the rendered image:
1. A stranger would screenshot or send it to a friend: it solves a real problem they have this week (a scam to avoid, a bill to fight, a deadline, a prompt that saves real time).
2. One specific, usable takeaway they can act on in under a minute (an exact prompt, a number, a step). No trivia, no filler quizzes or polls, no "fun facts", nothing generic.
3. Verified with 2 sources when it states a fact.
4. If in doubt, don't post. Zero stories on a day is fine. Filler stories are worse than none.
The automatic 5 a day story set (tip, quiz, answer, fact, poll) no longer goes to Metricool on autopilot.


## Threads publishing = Metricool (Oct 30)
Threads is connected in Metricool (brand 7761544). GitHub no longer posts to Threads (config/threads.json paused). The daily "Instagram + Threads loader" scheduled task schedules Threads queue items into Metricool and records them in state/posted.json. Our bot can't read or reply to Threads comments anymore and ManyChat doesn't cover Threads, so on Threads never ask people to comment a keyword: put the direct link in the post instead (free guide or /free/ page). Comment keywords are for Instagram only, where ManyChat answers them.


## Rename (Seb, Oct 30)
The free lead magnet at /brain/ is now called **The AI Front Desk** (was THE BUSINESS BRAIN). Use the new name in all new posts, emails and pages. The URL stays /brain/ and the comment keyword stays BRAIN (it already works in ManyChat and old posts). Inside the paid Workspace the setup file can still be called the Business Brain.

## Voiced reels (ElevenLabs)
- Voice: ElevenLabs "Brian - Deep, Resonant and Comforting", ALWAYS sped to 1.2x (scripts/tts.py does it with ffmpeg atempo).
- To make a reel: add tools/reel/<name>.py (copy credit.py: PHRASES, GROUPS, MOODS, SCENES) and push. The "Voiced reels" workflow renders every spec without a reel into docs/media/reels/money-<name>.mp4 + poster and commits it.
- Needs repo secret ELEVENLABS_API_KEY. Robot body frames live in tools/reel/fr/ (241 frames, rebuilt from the first 3 reels). The face screen is drawn on top.
- Post the mp4 to IG/Threads through Metricool as a REEL, using the poster as the cover.

## Day series: "AI agents that pay you back" (voiced, like the viral "Day 05: repos you should know" format)
- One agent per episode, Day 01, 02, 03... Brian voice at 1.2x with word timestamps, word by word captions with lime highlight boxes on key words, dark minimal app screens, a white "here's the smart part" beat, a PRO TIP, and a Follow + comment KEYWORD ending that teases tomorrow's day.
- Write tools/series/eps/day-NN-<slug>.json (beats: say, em words, scene: title / card / prompt / list / big / white / fan / tip / cta) and push. The "Day series" workflow voices and renders it to docs/media/series/<ep>.mp4 + poster.
- Keyword in the cta must exist in ManyChat and config/keywords.json. Facts in the script must match the free guide.
