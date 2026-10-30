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
import typeset as T
INK, SOFT, LINE = (244, 244, 240), (150, 152, 150), (38, 38, 40)
plain = lambda t: t.replace("{", "").replace("}", "")

def canvas(label, now):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ROOT, "tools", "story", "logo.png")).convert("RGB").resize((76, 76))
    m = Image.new("L", (76, 76), 0); ImageDraw.Draw(m).ellipse((0, 0, 76, 76), fill=255); im.paste(logo, (80, 170), m)
    d.text((176, 182), "AUTOPILOT.OI", font=T.font("Geist-SemiBold.otf", 32), fill=INK)
    T.label(d, now.strftime("%b %d · %Y"), 176, 224, 20, SOFT)
    T.label(d, "NO. " + str(now.timetuple().tm_yday).zfill(3), W - 80, 200, 20, SOFT, anchor="ra")
    d.line([(80, 300), (W - 80, 300)], fill=LINE, width=2)
    T.label(d, label, 80, 340, 24, LIME)
    return im, d

def footer(d, text):
    d.line([(80, 1660), (W - 80, 1660)], fill=LINE, width=2)
    T.label(d, text, 80, 1686, 22, SOFT)
    T.label(d, "@AUTOPILOT.OI", W - 80, 1686, 22, SOFT, anchor="ra")

def tip(item, now, out):
    im, d = canvas("AI TIP OF THE DAY", now)
    y = T.headline(d, item["t"], 80, 410, 920, 118)
    T.label(d, "TYPE THIS", 80, y + 50, 22, SOFT)
    top = y + 96
    yb = T.rich(d, item["x"], 130, top + 34, 840, 54, INK, LIME, sans="Geist-Medium.otf", lead=1.25)
    d.rounded_rectangle((80, top, W - 80, yb + 30), 26, outline=(64, 64, 66), width=2)
    d.rectangle((80, top + 26, 86, yb + 4), fill=LIME)
    footer(d, "SAVE THIS · TRY IT TODAY"); im.save(out, quality=94)

def options(d, opts, y, highlight=None):
    for i, o in enumerate(opts):
        L = "ABC"[i]; on = highlight == i; off = highlight is not None and not on
        h0 = y
        yb = T.rich(d, o, 200, y + 40, 690, 46, (110, 110, 110) if off else INK, LIME, sans="Geist-Medium.otf", lead=1.2)
        h = max(130, yb - y + 26)
        d.rounded_rectangle((80, y, W - 80, y + h), 24, fill=(18, 24, 6) if on else None, outline=LIME if on else ((44, 44, 46) if off else (70, 70, 72)), width=3 if on else 2)
        T.rich(d, o, 200, y + 40, 690, 46, (110, 110, 110) if off else INK, LIME, sans="Geist-Medium.otf", lead=1.2)
        d.text((122, y + h // 2), L, font=T.font("SairaSemiCondensed-BlackItalic.otf", 54), fill=(90, 90, 90) if off else LIME, anchor="lm")
        if on:
            cx, cy = W - 128, y + h // 2
            d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=LIME)
            d.line([(cx - 12, cy), (cx - 3, cy + 10), (cx + 13, cy - 9)], fill=BG, width=6, joint="curve")
        y += h + 22
    return y

def quiz_q(item, now, out):
    im, d = canvas("QUIZ · REPLY A, B OR C", now)
    y = T.headline(d, item["q"], 80, 410, 920, 120)
    options(d, item["o"], y + 60); footer(d, "ANSWER IN 2 HOURS"); im.save(out, quality=94)

def quiz_a(item, now, out):
    im, d = canvas("THE ANSWER", now)
    y = T.headline(d, item["q"], 80, 410, 920, 84, SOFT, INK)
    y = options(d, item["o"], y + 50, item["a"])
    T.rich(d, item["why"], 80, y + 40, 920, 50, INK, LIME, sans="Geist-Medium.otf", lead=1.25)
    footer(d, "DID YOU GET IT RIGHT?"); im.save(out, quality=94)

def poll(item, now, out):
    im, d = canvas("QUICK POLL · REPLY A OR B", now)
    y = T.headline(d, item["q"], 80, 410, 920, 140)
    options(d, item["o"], y + 70); footer(d, "REPLY A OR B"); im.save(out, quality=94)

def fact(item, num, now, out):
    im, d = canvas("EVERYDAY FIX · NO. " + str(num).zfill(3), now)
    # giant outlined number as texture
    big = T.font("SairaSemiCondensed-BlackItalic.otf", 700)
    d.text((W + 40, 1640), str(num).zfill(2), font=big, fill=BG, stroke_width=4, stroke_fill=(34, 40, 14), anchor="rs")
    T.label(d, "THE PROBLEM", 80, 400, 24, SOFT)
    T.rich(d, item.get("p", ""), 80, 452, 920, 44, (205, 207, 204), INK, sans="Geist-Medium.otf")
    d.line((80, 500, W - 80, 500), fill=(40, 42, 38), width=2)
    T.label(d, "THE FIX", 80, 560, 24, LIME)
    y = T.headline(d, item["f"], 80, 610, 920, 124)
    d.rectangle((80, y + 30, 240, y + 38), fill=LIME)
    y = T.rich(d, item["more"], 80, y + 80, 900, 48, (205, 207, 204), INK, sans="Geist-Medium.otf", lead=1.3)
    if item.get("try"):
        top = y + 50
        T.label(d, "SAY THIS TO CLAUDE", 120, top + 34, 22, LIME)
        yb = T.rich(d, item["try"], 120, top + 80, 840, 46, INK, LIME, sans="Geist-SemiBold.otf", lead=1.25)
        d.rounded_rectangle((80, top, W - 80, yb + 36), 28, fill=(14, 16, 10), outline=(80, 96, 30), width=2)
        T.label(d, "SAY THIS TO CLAUDE", 120, top + 34, 22, LIME)
        T.rich(d, item["try"], 120, top + 80, 840, 46, INK, LIME, sans="Geist-SemiBold.otf", lead=1.25)
    footer(d, "SAVE THIS · SHARE IT"); im.save(out, quality=94)

def main():
    now = dt.datetime.now(ET); day = now.date().isoformat(); n = now.toordinal()
    pool = json.load(open(os.path.join(ROOT, "tools", "story", "pool.json")))
    out = os.path.join(ROOT, "docs", "media", "stories"); os.makedirs(out, exist_ok=True)
    t = pool["tips"][n % len(pool["tips"])]; q = pool["quizzes"][n % len(pool["quizzes"])]; p = pool["polls"][n % len(pool["polls"])]
    fi = n % len(pool["facts"]); fc = pool["facts"][fi]; fact(fc, fi + 1, now, f"{out}/{day}-fact.jpg")
    tip(t, now, f"{out}/{day}-tip.jpg"); quiz_q(q, now, f"{out}/{day}-quiz.jpg"); quiz_a(q, now, f"{out}/{day}-answer.jpg"); poll(p, now, f"{out}/{day}-poll.jpg")
    items = []
    try:
        crypto, stocks = ms.fetch()
        hero, lines = ms.build(crypto, stocks, now, f"{out}/{day}.mp4", f"{out}/{day}-poster.jpg")
        items.append(("market", "8:30", f"{day}.mp4", f"Market check: {hero['name']} {ms.pct(hero['chg'])}. " + " ".join(lines)))
    except Exception as e:
        print("::warning title=Market data::skipped market story:", e)
    items += [("tip", "10:30", f"{day}-tip.jpg", "AI tip: " + plain(t["t"]) + " " + plain(t["x"])),
              ("quiz", "12:30", f"{day}-quiz.jpg", "Quiz: " + plain(q["q"])),
              ("answer", "14:30", f"{day}-answer.jpg", "Quiz answer: " + q["o"][q["a"]] + ". " + q["why"]),
              ("fact", "16:30", f"{day}-fact.jpg", "Everyday fix: " + plain(fc["f"]) + " " + fc["more"]),
              ("poll", "18:00", f"{day}-poll.jpg", "Poll: " + plain(p["q"]) + " A) " + p["o"][0] + " B) " + p["o"][1])]
    queue = []
    for k, hm, f, text in items:
        h, m = map(int, hm.split(":"))
        at = now.replace(hour=h, minute=m, second=0, microsecond=0)
        queue.append({"id": f"story-{day}-{k}", "group": f"stories-{day}", "at": at.isoformat(), "kind": "story", "threads": False, "media": [BASE + f], "text": text})
    json.dump(queue, open(os.path.join(ROOT, "queue", f"{day}-stories.json"), "w"), indent=1, ensure_ascii=False)
    print("stories ready", [i[0] for i in items])

if __name__ == "__main__":
    main()
