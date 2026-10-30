"""Builds the day's 5 Instagram stories in the black AUTOPILOT.OI style and queues them as one approval batch.
1 market check (video)  2 AI tip  3 quiz question  4 quiz answer  5 poll (reply A or B)
Instagram's API can't add real poll or quiz stickers, so quizzes and polls ask people to reply A, B or C
(replies land in DMs, which also helps reach). Content rotates from tools/story/pool.json."""
import os, json, textwrap, datetime as dt
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
import market_story as ms

ROOT = ms.ROOT; ET = ms.ET; W, H = 1080, 1920
LIME, WHITE, GREY, BG = ms.LIME, (244, 244, 240), (120, 124, 128), (0, 0, 0)
BASE = "https://autopilotio-oss.github.io/autopilot-engine/media/stories/"
F = lambda n, s: ImageFont.truetype(os.path.join(ROOT, "tools", "story", "fonts", n), s)

def canvas(label, now):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ROOT, "tools", "story", "logo.png")).convert("RGB").resize((100, 100))
    m = Image.new("L", (100, 100), 0); ImageDraw.Draw(m).ellipse((0, 0, 100, 100), fill=255); im.paste(logo, (80, 150), m)
    d.text((200, 160), "AUTOPILOT.OI", font=F("InterDisplay-SemiBold.otf", 38), fill=WHITE)
    d.text((200, 206), "@autopilot.oi · " + now.strftime("%b %d"), font=F("Inter-Medium.otf", 32), fill=GREY)
    d.text((80, 330), label, font=F("SpaceMono-Bold.ttf", 30), fill=LIME)
    return im, d

def wrap(d, text, font, x, y, width, fill, gap=1.22):
    words = text.split(); line = ""; lh = int(font.size * gap)
    for w in words:
        test = (line + " " + w).strip()
        if d.textlength(test, font=font) > width and line:
            d.text((x, y), line, font=font, fill=fill); y += lh; line = w
        else: line = test
    if line: d.text((x, y), line, font=font, fill=fill); y += lh
    return y

def footer(d, text):
    d.text((80, 1690), text, font=F("SpaceMono-Bold.ttf", 28), fill=GREY)

def tip(item, now, out):
    im, d = canvas("AI TIP OF THE DAY", now)
    y = wrap(d, item["t"], F("InterDisplay-Medium.otf", 66), 80, 430, 920, WHITE)
    d.rectangle((80, y + 40, 88, y + 40 + 10), fill=LIME)
    y2 = wrap(d, item["x"], F("InterDisplay-Light.otf", 72), 120, y + 40, 880, LIME)
    d.rectangle((80, y + 40, 88, y2), fill=LIME)
    footer(d, "SAVE THIS · TRY IT TODAY"); im.save(out, quality=92)

def options(d, opts, y, highlight=None):
    for i, o in enumerate(opts):
        L = "ABC"[i]; on = highlight == i; off = highlight is not None and not on
        f = F("InterDisplay-Medium.otf", 44); words = o.split(); lines, cur = 1, ""
        for w in words:
            t2 = (cur + " " + w).strip()
            if d.textlength(t2, font=f) > 760 and cur: lines += 1; cur = w
            else: cur = t2
        h = max(150, 54 * lines + 70)
        d.rounded_rectangle((80, y, W - 80, y + h), 30, fill=(28, 38, 8) if on else (10, 10, 11), outline=LIME if on else (48, 48, 50), width=3 if on else 2)
        d.text((120, y + h // 2), L, font=F("InterDisplay-SemiBold.otf", 58), fill=LIME if not off else (70, 70, 70), anchor="lm")
        wrap(d, o, f, 200, y + (h - 54 * lines) // 2, 760, WHITE if not off else (90, 90, 90))
        y += h + 24
    return y

def quiz_q(item, now, out):
    im, d = canvas("QUIZ · REPLY A, B OR C", now)
    y = wrap(d, item["q"], F("InterDisplay-Medium.otf", 70), 80, 430, 920, WHITE)
    options(d, item["o"], y + 60); footer(d, "ANSWER DROPS IN 2 HOURS"); im.save(out, quality=92)

def quiz_a(item, now, out):
    im, d = canvas("QUIZ ANSWER", now)
    y = wrap(d, item["q"], F("InterDisplay-Medium.otf", 60), 80, 430, 920, (200, 200, 196))
    y = options(d, item["o"], y + 50, item["a"])
    wrap(d, item["why"], F("InterDisplay-Light.otf", 50), 80, y + 40, 920, WHITE)
    footer(d, "DID YOU GET IT RIGHT?"); im.save(out, quality=92)

def poll(item, now, out):
    im, d = canvas("QUICK POLL · REPLY A OR B", now)
    y = wrap(d, item["q"], F("InterDisplay-Medium.otf", 76), 80, 430, 920, WHITE)
    options(d, item["o"], y + 70); footer(d, "I READ EVERY REPLY"); im.save(out, quality=92)

def main():
    now = dt.datetime.now(ET); day = now.date().isoformat(); n = now.toordinal()
    pool = json.load(open(os.path.join(ROOT, "tools", "story", "pool.json")))
    out = os.path.join(ROOT, "docs", "media", "stories"); os.makedirs(out, exist_ok=True)
    t = pool["tips"][n % len(pool["tips"])]; q = pool["quizzes"][n % len(pool["quizzes"])]; p = pool["polls"][n % len(pool["polls"])]
    tip(t, now, f"{out}/{day}-tip.jpg"); quiz_q(q, now, f"{out}/{day}-quiz.jpg"); quiz_a(q, now, f"{out}/{day}-answer.jpg"); poll(p, now, f"{out}/{day}-poll.jpg")
    items = []
    try:
        crypto, stocks = ms.fetch()
        hero, lines = ms.build(crypto, stocks, now, f"{out}/{day}.mp4", f"{out}/{day}-poster.jpg")
        items.append(("market", "8:30", f"{day}.mp4", f"Market check: {hero['name']} {ms.pct(hero['chg'])}. " + " ".join(lines)))
    except Exception as e:
        print("::warning title=Market data::skipped market story:", e)
    items += [("tip", "10:30", f"{day}-tip.jpg", "AI tip: " + t["t"] + " " + t["x"]),
              ("quiz", "12:30", f"{day}-quiz.jpg", "Quiz: " + q["q"]),
              ("answer", "14:30", f"{day}-answer.jpg", "Quiz answer: " + q["o"][q["a"]] + ". " + q["why"]),
              ("poll", "18:00", f"{day}-poll.jpg", "Poll: " + p["q"] + " A) " + p["o"][0] + " B) " + p["o"][1])]
    queue = []
    for k, hm, f, text in items:
        h, m = map(int, hm.split(":"))
        at = now.replace(hour=h, minute=m, second=0, microsecond=0)
        queue.append({"id": f"story-{day}-{k}", "group": f"stories-{day}", "at": at.isoformat(), "kind": "story", "threads": False, "media": [BASE + f], "text": text})
    json.dump(queue, open(os.path.join(ROOT, "queue", f"{day}-stories.json"), "w"), indent=1, ensure_ascii=False)
    print("stories ready", [i[0] for i in items])

if __name__ == "__main__":
    main()
