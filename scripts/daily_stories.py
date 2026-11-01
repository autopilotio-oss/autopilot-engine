"""Builds the day's 5 Instagram stories in the black AUTOPILOT.OI style and queues them as one approval batch.
1 market check (video)  2 AI tip  3 quiz question  4 quiz answer  5 poll (reply A or B)
Instagram's API can't add real poll or quiz stickers, so quizzes and polls ask people to reply A, B or C
(replies land in DMs, which also helps reach). Content rotates from tools/story/pool.json."""
import os, sys, json, textwrap, datetime as dt
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

import numpy as np
from PIL import ImageFilter
def _atmos(seed):
    """Studio backdrop: near black, drifting lime and teal light, vignette, film grain (same look as the reels)."""
    rng = np.random.default_rng(seed)
    base = Image.new("RGB", (W, H), (3, 4, 3)); glow = Image.new("RGB", (W, H), (0, 0, 0)); g = ImageDraw.Draw(glow)
    x1, y1 = int(rng.integers(-150, 350)), int(rng.integers(150, 600)); g.ellipse((x1, y1, x1 + 900, y1 + 900), fill=(64, 82, 10))
    x2, y2 = int(rng.integers(450, 800)), int(rng.integers(1000, 1400)); g.ellipse((x2, y2, x2 + 760, y2 + 680), fill=(10, 48, 36))
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    a = np.asarray(base, np.float32) + np.asarray(glow, np.float32)
    yy, xx = np.mgrid[0:H, 0:W]; v = ((xx - W / 2) / (W * .62)) ** 2 + ((yy - H * .46) / (H * .55)) ** 2
    a = a * np.clip(1.25 - v * .75, .25, 1)[..., None] + rng.normal(0, 6, (H, W, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype("uint8"))

def card(im, box, lit=False, radius=34):
    """Glass card with a lime gradient edge and soft shadow."""
    x0, y0, x1, y1 = [int(v) for v in box]; w, h = x1 - x0, y1 - y0
    sh = Image.new("L", (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 24, x1, y1 + 30), radius, fill=170)
    im.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(28)))
    if lit:
        gl = Image.new("L", (W, H), 0); ImageDraw.Draw(gl).rounded_rectangle((x0, y0, x1, y1), radius, fill=140)
        im.paste((150, 190, 30), (0, 0), gl.filter(ImageFilter.GaussianBlur(40)))
    top, bot = ((36, 46, 14), (12, 16, 6)) if lit else ((30, 33, 28), (11, 12, 11))
    k = np.linspace(0, 1, h)[:, None, None]; arr = (np.array(top) * (1 - k) + np.array(bot) * k) * np.ones((1, w, 1))
    body = Image.fromarray(arr.astype("uint8"))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=245)
    im.paste(body, (x0, y0), m)
    edge = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ed = ImageDraw.Draw(edge)
    if lit:
        ed.rounded_rectangle((0, 0, w - 1, h - 1), radius, outline=(212, 255, 58, 255), width=3)
    else:
        ed.rounded_rectangle((0, 0, w - 1, h - 1), radius, outline=(255, 255, 255, 34), width=2)
        lime = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(lime).rounded_rectangle((0, 0, w - 1, h - 1), radius, outline=(212, 255, 58, 255), width=2)
        fade = np.clip(1 - np.arange(w) / (w * .45), 0, 1)[None, :] * np.ones((h, 1)) * 170
        al = np.minimum(np.asarray(lime.split()[3], np.float32), fade).astype("uint8"); lime.putalpha(Image.fromarray(al))
        edge = Image.alpha_composite(edge, lime)
    im.paste(edge, (x0, y0), edge)

def chip(d, text, x, y, size=24):
    f = T.font("SairaSemiCondensed-BlackItalic.otf", size); w = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + w + 36, y + size + 22), 12, fill=LIME)
    d.text((x + 18, y + 11 + size * .82), text, font=f, fill=(8, 10, 4), anchor="ls")

def canvas(label, now):
    im = _atmos(now.toordinal() * 7 + len(label)); d = ImageDraw.Draw(im)
    logo = Image.open(os.path.join(ROOT, "tools", "story", "logo.png")).convert("RGB").resize((76, 76))
    m = Image.new("L", (76, 76), 0); ImageDraw.Draw(m).ellipse((0, 0, 76, 76), fill=255); im.paste(logo, (80, 170), m)
    d.text((176, 222), "AUTOPILOT.OI", font=T.font("SairaSemiCondensed-BlackItalic.otf", 38), fill=INK, anchor="ls")
    T.label(d, now.strftime("%b %d · %Y"), 178, 238, 18, SOFT)
    T.label(d, "NO. " + str(now.timetuple().tm_yday).zfill(3), W - 80, 200, 20, SOFT, anchor="ra")
    chip(d, label, 80, 320, 26)
    return im, d

def footer(d, text):
    d.line([(80, 1660), (W - 80, 1660)], fill=(40, 44, 36), width=2)
    T.label(d, text, 80, 1686, 22, LIME)
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

def options(d, opts, y, highlight=None, im=None):
    for i, o in enumerate(opts):
        L = "ABC"[i]; on = highlight == i; off = highlight is not None and not on
        probe = ImageDraw.Draw(Image.new("RGB", (W, 600)))
        yb = T.rich(probe, o, 0, 50, 640, 46, INK, LIME, sans="Geist-SemiBold.otf", lead=1.2)
        h = max(140, yb + 40)
        if im is not None: card(im, (80, y, W - 80, y + h), lit=on)
        T.rich(d, o, 220, y + 56 + (h - 140) // 2 * 0, 640, 46, (96, 98, 94) if off else INK, LIME, sans="Geist-SemiBold.otf", lead=1.2)
        bx, by = 112, y + h // 2 - 38
        d.rounded_rectangle((bx, by, bx + 76, by + 76), 20, fill=LIME if not off else (40, 42, 38))
        d.text((bx + 38, by + 60), L, font=T.font("SairaSemiCondensed-BlackItalic.otf", 58), fill=(8, 10, 4) if not off else (100, 100, 96), anchor="ms")
        if on:
            cx, cy = W - 132, y + h // 2
            d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=LIME)
            d.line([(cx - 14, cy), (cx - 3, cy + 12), (cx + 15, cy - 11)], fill=BG, width=7, joint="curve")
        y += h + 24
    return y

def quiz_q(item, now, out):
    abc = "A, B OR C" if len(item["o"]) > 2 else "A OR B"; im, d = canvas("QUIZ · REPLY " + abc, now)
    y = T.headline(d, item["q"], 80, 410, 920, 120)
    options(d, item["o"], y + 70, im=im); footer(d, "REPLY " + abc + " · ANSWER IN 2 HOURS"); im.save(out, quality=94)

def quiz_a(item, now, out):
    im, d = canvas("THE ANSWER", now)
    y = T.headline(d, item["q"], 80, 410, 920, 84, SOFT, INK)
    y = options(d, item["o"], y + 60, item["a"], im=im)
    T.rich(d, item["why"], 80, y + 40, 920, 50, INK, LIME, sans="Geist-Medium.otf", lead=1.25)
    footer(d, "DID YOU GET IT RIGHT?"); im.save(out, quality=94)

def poll(item, now, out):
    im, d = canvas("QUICK POLL · REPLY A OR B", now)
    y = T.headline(d, item["q"], 80, 410, 920, 140)
    options(d, item["o"], y + 80, im=im); footer(d, "REPLY A OR B"); im.save(out, quality=94)

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
    # NO PROOF, NO POST (owner, Oct 31): auto stories carry no content_id, so they are drafts in queue/hold/,
    # never in queue/ where the viral queue guard (SEV-1) and loaders read. Monthly review 2026-11-01.
    json.dump(queue, open(os.path.join(ROOT, "queue", "hold", f"{day}-stories.json"), "w"), indent=1, ensure_ascii=False)
    print("stories ready", [i[0] for i in items])


def trend(item, now, out):
    """Trending story/card: {"tag": "TRENDING", "h": "headline with {lime} words", "what": "what happened", "do": "what to do / the prompt", "src": "Source name"}"""
    im, d = canvas(item.get("tag", "TRENDING NOW").upper(), now)
    y = T.headline(d, item["h"], 80, 420, 920, 112)
    y = T.rich(d, item["what"], 80, y + 50, 920, 44, (205, 207, 204), INK, sans="Geist-Medium.otf", lead=1.3)
    if item.get("do"):
        top = y + 50; probe = ImageDraw.Draw(Image.new("RGB", (W, 900)))
        hb = T.rich(probe, item["do"], 0, 80, 840, 44, INK, LIME, sans="Geist-SemiBold.otf", lead=1.25)
        card(im, (80, top, W - 80, top + hb + 40), lit=True)
        T.label(d, item.get("do_label", "WHAT TO DO"), 120, top + 34, 22, LIME)
        T.rich(d, item["do"], 120, top + 80, 840, 44, INK, LIME, sans="Geist-SemiBold.otf", lead=1.25)
    if item.get("src"): T.label(d, "SOURCE: " + item["src"].upper(), 80, 1610, 18, SOFT)
    footer(d, "FOLLOW FOR ONE AI FIX A DAY"); im.save(out, quality=94)


def trend_cli():
    """python scripts/daily_stories.py trend '<json item>' <out.jpg>"""
    item = json.loads(sys.argv[2]); trend(item, dt.datetime.now(ET), sys.argv[3])

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "trend": trend_cli()
    else: main()
