# Daily agent drop (runs every day, 8 AM Argentina)

Seb's decision (Oct 31 2026): fully automatic. Every day we find one real problem, build a new $10 agent that solves it, make a robot demo video that shows exactly what the agent does, publish it and post it everywhere. If no idea clears the gate, ship nothing that day and say why. A skipped day beats a bad product.

## 0. Setup
- Repo: `/home/claude/autopilot-engine`. If it's missing, clone `github.com/autopilotio-oss/autopilot-engine` there.
- Run `git pull --rebase` first.
- Commit as `autopilotio-oss <autopilotio-oss@users.noreply.github.com>`.
- Read `PLAYBOOK.md`: hard rules, the Idea gate, the rejected list.
- Read `config/approvals_queue.md` and `docs/daily/` so you never repeat an agent or a rejected idea.

## 1. Find a real problem (web research, 20 to 30 min)
Look for a money, time or hassle problem that regular people or small business owners hit, which Claude can genuinely help with by reading what they upload and drafting something.

Good places to look:
- CFPB and FTC consumer complaint topics, and state attorney general alerts.
- Reddit threads (r/personalfinance, r/smallbusiness, r/povertyfinance, r/legaladvice style questions: read them, never copy them).
- News from this week.
- Our own comments and DMs (state/comments.json).

Good examples of the shape:
- Fight a parking ticket.
- Read a lease before signing.
- Dispute a security deposit deduction.
- Write a landlord repair request.
- Check a car repair quote.
- Prepare for a negotiation with a phone, internet or insurance company.
- Turn receipts into an expense report.

Never:
- Credit repair (Gumroad prohibited).
- Tech support or installation services (Gumroad prohibited).
- Medical diagnosis or dosing.
- Legal representation.
- Investing or trading advice.
- Gambling.
- Anything on the PLAYBOOK rejected list.
- Anything we already sell.

Need 2+ sources showing the problem is real and common. Put the URLs in `gate.problem_sources`.

## 2. Score it with the Idea gate
Six criteria, each scored 0 to 2, written into `gate.scores`:
- `real_problem`
- `honest_claim`
- `easy_to_run` (a non tech person sets it up in 10 min)
- `fits_brand`
- `sellable` (people would pay $10)
- `not_done_before`

Ship only at 10/12 or higher with no zeros. Score honestly. If your best idea scores 9, look for another one. If nothing passes after 3 ideas, stop. Then send Seb a SendUserMessage with the 3 ideas and their scores, and make no product that day.

## 3. Write the spec: `tools/daily/specs/<slug>.json`
Use `tools/daily/specs/EXAMPLE.json` as the template.

**IDs**
- `slug` is `<word>-agent`.
- `key` is the short word, used for the guide URL `/g/<key>/`.
- `kw` is the comment keyword in caps.
- `cat` is MONEY, LIFE, BUSINESS or TIKTOK.

**Product copy.** These fields are the honest Gumroad description, in the same format as every other product:
- `headline`
- `what`
- `need`
- `doesnt`, which says what the agent does NOT do.

**`kit`.** These are the real deliverables. Make them genuinely useful, not filler:
- `tag`
- `promise`
- `setup`: 4 to 6 steps.
- `master`: the master prompt, written as instructions for a Claude Project, 1500 to 3000 chars. It must say "never invent facts" and "I review and send everything myself".
- `starters`: 5 pairs of [title, prompt].
- `links`: official sources.
- `tracker`: 4 to 6 column names.

**`guide`.** The free guide teaches the whole process for free. Its fields:
- `title`, `sub`, `time`, `need`, `why`
- `steps`: a list of [title, text, prompt or null, []].
- `warn`
- `agent`: {name, what, setup[], instr}
- `sources`: [[title, url]]

**`cover`.** For the format, see `tools/kits/covers2.py` (`covers_extra`). It shows an example output page:
- `cat`, `no`, `t1` (NAME), `t2` "AGENT", `sub`, `doc`
- `table` {head, rows, foot} or `letter` [lines]

**`demo`.** This is the robot video script. It must show exactly what the agent does:
- `color`: lime, green, cyan or gold.
- `problem`: 2 to 4 words.
- `does_title`, plus `does` (3 short lines).
- `beats` in this order: intro, upload, prompt, work, result, draft (optional), cta.
  - Every beat has a `say` line for the voice: short, spoken and plain.
  - Total voice is 80 to 110 words.
  - The intro hook names the problem in the first sentence.
  - The cta says "ten dollar Claude prompt kit" and "Comment <KW> for the free guide".
- Copy the field shapes (files, text, lines, cols/rows/foot, title/text) from `tools/demo/eps/subs-agent.json`.
- Every number on screen is an example. The panel already labels it EXAMPLE OUTPUT.

**`reply`.** The DM reply for the keyword. It must include `https://autopilotoi.app/g/<key>/`.

**`posts`.** One caption each for `tiktok` (one paragraph, no line breaks), `instagram`, `threads` and `x`:
- Under 500 chars each.
- Each ends with one action: Comment <KW> (IG and TikTok), or the guide link (Threads and X).

**Honesty rules (the script enforces some of them)**
- No dashes.
- No income or outcome promises.
- No "guaranteed", "on its own", "while you sleep" or "automatically".
- It is a Claude prompt kit the person runs. It drafts, they decide and send.
- Every factual claim (laws, deadlines, rights) must match the sources and be current. Check them on official sites.

## 4. Build it
```
python3 tools/daily/new_agent.py tools/daily/specs/<slug>.json --check   # fix anything it flags
python3 tools/daily/new_agent.py tools/daily/specs/<slug>.json
```
Then:
- Open `docs/store/<key>-cover.png` and `docs/g/<key>/index.html` (screenshot it) and check them.
- Commit everything with the message `Daily agent: <Name>`, then push.

The push starts three things:
- The Gumroad sync creates the product.
- The demo workflow renders `docs/media/demo/<slug>.mp4` (about 12 minutes).
- Pages deploys the guide.

## 5. Verify, then post
- Wait for the `Agent demo videos` and `Gumroad products` runs to finish (`gh run list`), then `git pull`.
- Check `docs/live.json` includes the slug. If it's not live, don't post a sales link. Post the guide link only, and say so in the report.
- Watch the video: extract frames with ffmpeg and look at 6 of them. Check the duration matches the voice.
- Schedule with Metricool (blogId 7761544, timezone America/New_York), using the video URL `https://autopilotoi.app/media/demo/<slug>.mp4`. Wait about 2 min after the push for Pages to serve it.
  - TikTok at 13:45 ET: tiktokData.title = first line, isAigc true.
  - Instagram REEL at 13:45 ET.
  - Threads at 12:30 ET.
  - X at 14:00 ET.
  - If a slot is taken, move by 30 min.

## 6. Report
- Update `docs/daily/<date>-<slug>.json` with the Metricool post ids.
- Append one line to the Project doc `claude/daily-drops.md`: date, agent, gate score, links.
- Send Seb one short SendUserMessage: the problem, the agent, the video link, and when each post goes out. No recap of steps.
