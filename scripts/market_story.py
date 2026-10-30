"""Daily market check for Instagram Stories: a short animated video in the AUTOPILOT.OI tweet style.
Crypto (24h, CoinGecko) and stocks (last close, Stooq). Plain English, never advice.
Writes docs/media/stories/<date>.mp4 (+ -poster.jpg) and a queue entry that waits for Seb's YES."""
import os, json, csv, io, math, subprocess, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "tools", "story", "fonts")
ET = ZoneInfo("America/New_York")
LIME, BG, RED, GREY, WHITE, DIM = (212, 255, 58), (0, 0, 0), (255, 107, 107), (113, 118, 123), (231, 233, 234), (22, 24, 28)
CRYPTO = [("bitcoin", "BTC", "Bitcoin"), ("ethereum", "ETH", "Ethereum"), ("solana", "SOL", "Solana")]
STOCKS = [("spy.us", "SPY", "The S&P 500"), ("qqq.us", "QQQ", "The Nasdaq"), ("nvda.us", "NVDA", "Nvidia"), ("aapl.us", "AAPL", "Apple"), ("tsla.us", "TSLA", "Tesla")]
W, H, FPS, DUR = 1080, 1920, 30, 9.0

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 autopilot-brief"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()

def fetch():
    ids = ",".join(c[0] for c in CRYPTO)
    cg = json.loads(get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"))
    crypto = []
    for i, s, n in CRYPTO:
        try: hist = [p[1] for p in json.loads(get(f"https://api.coingecko.com/api/v3/coins/{i}/market_chart?vs_currency=usd&days=7&interval=daily"))["prices"]]
        except Exception: hist = []
        crypto.append({"sym": s, "name": n, "price": cg[i]["usd"], "chg": cg[i]["usd_24h_change"], "hist": hist, "span": "24H"})
    stocks = []
    for code, sym, name in STOCKS:
        rows = [r for r in csv.DictReader(io.StringIO(get(f"https://stooq.com/q/d/l/?s={code}&i=d"))) if r.get("Close")]
        closes = [float(r["Close"]) for r in rows[-8:]]
        stocks.append({"sym": sym, "name": name, "price": closes[-1], "chg": (closes[-1] / closes[-2] - 1) * 100, "hist": closes, "span": "1D"})
    return crypto, stocks

def money(v): return f"${v:,.0f}" if v >= 1000 else f"${v:,.2f}"
def pct(v): return f"{'+' if v >= 0 else '-'}{abs(v):.1f}%"

def lines_for(crypto, stocks, weekend):
    btc, eth = crypto[0], crypto[1]; spx = stocks[0]
    top = max(stocks[2:], key=lambda s: abs(s["chg"]))
    when = "Friday" if weekend else "Yesterday"
    return [f"Bitcoin {pct(btc['chg'])}, Ethereum {pct(eth['chg'])} overnight.",
            f"{when} the S&P 500 closed {pct(spx['chg'])}.",
            f"{top['name']} was the big tech move at {pct(top['chg'])}."]

def font(name, size): return ImageFont.truetype(os.path.join(F, name), size)
ease = lambda x: 1 - (1 - max(0, min(1, x))) ** 3
def back(x):
    x = max(0, min(1, x)); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2

def frame(t, ctx):
    hero, items, lines, now = ctx["hero"], ctx["items"], ctx["lines"], ctx["now"]
    im = ctx["base"].copy(); d = ImageDraw.Draw(im)
    up = hero["chg"] >= 0; col = LIME if up else RED
    # header (tweet style)
    a = ease(t / 0.4)
    im.paste(ctx["logo"], (80, int(150 - 20 * (1 - a))), ctx["mask"])
    d.text((200, 160), "AUTOPILOT.OI", font=font("InterDisplay-SemiBold.otf", 38), fill=WHITE)
    d.text((200, 206), "@autopilot.oi · " + now.strftime("%b %d"), font=font("Inter-Medium.otf", 32), fill=GREY)
    d.text((80, 300), "gm. your 30 second market check", font=font("InterDisplay-Medium.otf", 46), fill=WHITE) if t > 0.2 else None
    # hero: biggest mover
    hp = ease((t - 0.5) / 0.6)
    if hp > 0:
        d.text((80, 410), f"TODAY'S BIG MOVE · {hero['span']}", font=font("SpaceMono-Bold.ttf", 28), fill=GREY)
        d.text((80, 460), hero["name"], font=font("InterDisplay-Medium.otf", 88), fill=WHITE)
        shown = hero["chg"] * ease((t - 0.7) / 1.2)
        d.text((70, 560), pct(shown), font=font("InterDisplay-Light.otf", 230), fill=col)
        d.text((W - 80, 486), money(hero["price"]), font=font("InterDisplay-Light.otf", 60), fill=WHITE, anchor="ra")
    # sparkline draws in
    hist = hero.get("hist") or []
    sp = ease((t - 1.0) / 1.6)
    if len(hist) > 2 and sp > 0:
        x0, x1, y0, y1 = 80, W - 80, 880, 1080
        lo, hi = min(hist), max(hist); rng = (hi - lo) or 1
        pts = [(x0 + (x1 - x0) * i / (len(hist) - 1), y1 - (y1 - y0) * (v - lo) / rng) for i, v in enumerate(hist)]
        n = max(2, int(len(pts) * sp + 1)); seg = pts[:n]
        fill_poly = seg + [(seg[-1][0], y1 + 30), (x0, y1 + 30)]
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
        ld.polygon(fill_poly, fill=col + (22,)); im.paste(layer, (0, 0), layer); d = ImageDraw.Draw(im)
        d.line(seg, fill=col, width=5, joint="curve")
        d.ellipse((seg[-1][0] - 10, seg[-1][1] - 10, seg[-1][0] + 10, seg[-1][1] + 10), fill=col)
        d.text((80, 1122), "LAST 7 DAYS", font=font("SpaceMono-Bold.ttf", 24), fill=GREY)
    # ticker chips slide in
    y = 1190
    for i, it in enumerate(items):
        p = back((t - 2.2 - i * 0.12) / 0.45)
        if p <= 0: continue
        cx = 80 + (i % 4) * 236; cy = y + (i // 4) * 132 + int(60 * (1 - p))
        c = LIME if it["chg"] >= 0 else RED
        d.rounded_rectangle((cx, cy, cx + 216, cy + 112), 20, fill=(8, 8, 9), outline=(44, 44, 46), width=2)
        d.text((cx + 22, cy + 18), it["sym"], font=font("SpaceMono-Bold.ttf", 26), fill=(170, 170, 166))
        d.text((cx + 22, cy + 56), pct(it["chg"]), font=font("InterDisplay-Medium.otf", 38), fill=c)
    # plain english, line by line
    for i, l in enumerate(lines):
        p = ease((t - 3.6 - i * 0.55) / 0.4)
        if p <= 0: continue
        d.text((80 + int(30 * (1 - p)), 1490 + 62 * i), l, font=font("InterDisplay-Medium.otf", 36), fill=tuple(int(v * p) for v in WHITE))
    if t > 5.6:
        d.text((80, 1712), "Not financial advice. Prices as of " + now.strftime("%I:%M %p").lstrip("0") + " ET.", font=font("Inter-Medium.otf", 28), fill=GREY)
    return im

def soundtrack(path, green, n_items, n_lines, sr=44100):
    """Original lofi trap beat made in code (no licensing issues): warm keys, 808 with glide, rolling hats,
    vinyl crackle. Major 7ths on green days, minor on red days. Small pops are timed to the animation."""
    import numpy as np, wave
    N = int(DUR * sr); L = np.zeros(N); rng = np.random.default_rng(11)
    T = lambda d: np.arange(int(d * sr)) / sr
    def add(sig, at, g=1.0):
        i = int(at * sr); j = min(N, i + len(sig))
        if 0 <= i < N: L[i:j] += sig[: j - i] * g
    def env(n, a, d): x = np.arange(n) / sr; return np.minimum(1, x / a) * np.exp(-x / d)
    def lp(x, k):
        y = np.copy(x)
        for _ in range(k): y = np.convolve(y, [.25, .5, .25], "same")
        return y
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    if green: chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]   # Fmaj7 Em7 Dm7 Cmaj7
    else:     chords = [[57, 60, 64, 67], [53, 57, 60, 64], [50, 53, 57, 60], [52, 56, 59, 62]]   # Am7 Fmaj7 Dm7 E7
    bpm = 140; s16 = 60 / bpm / 4; bar = 16 * s16
    def keys(ms, d):
        x = T(d); w = 0
        for m in ms:
            f = mtof(m); w = w + (np.sin(2 * np.pi * f * x) + .25 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 1.1)
        w *= (1 + .12 * np.sin(2 * np.pi * 4.5 * x)) * np.minimum(1, x / .01)
        return lp(w / len(ms), 3)
    def eight08(m, d, glide_to=None):
        x = T(d); f = mtof(m - 24) * np.ones_like(x)
        if glide_to is not None: f = f + (mtof(glide_to - 24) - f) * np.clip((x - d * .7) / (d * .2), 0, 1)
        w = np.sin(2 * np.pi * np.cumsum(f) / sr); return np.tanh(2.2 * w) * np.minimum(1, x / .005) * np.exp(-x / .9)
    def kick():
        x = T(.3); return np.sin(2 * np.pi * np.cumsum(50 + 120 * np.exp(-x * 40)) / sr) * env(len(x), .001, .12)
    def snare():
        x = rng.standard_normal(int(.25 * sr)); x = x - lp(x, 2)
        t = T(.25); body = np.sin(2 * np.pi * 190 * t) * np.exp(-t / .05)
        return (x * env(len(x), .001, .09) * .6 + body * .5)
    def hat():
        x = rng.standard_normal(int(.04 * sr)); x = x - lp(x, 4); return x * env(len(x), .0005, .01) * .5
    def ping(f): x = T(.15); return np.sin(2 * np.pi * f * x) * env(len(x), .002, .035)
    nbars = int(DUR / bar) + 1
    for k in range(nbars):
        t0 = k * bar; ch = chords[k % 4]; nxt = chords[(k + 1) % 4]
        add(keys(ch, bar * 1.05), t0, .55)
        add(eight08(ch[0], bar * .95, nxt[0] if k % 2 else None), t0, .55)
        if t0 > 0.3:
            for st in (0, 10): add(kick(), t0 + st * s16, .5)
            add(snare(), t0 + 8 * s16, .38)
        for st in range(0, 16, 2): add(hat(), t0 + st * s16, .5 if st % 4 == 0 else .32)
        for r in range(6): add(hat(), t0 + 13 * s16 + r * s16 / 2, .22 + .04 * r)   # hat roll
    hiss = lp(rng.standard_normal(N), 6) * .02
    crack = np.zeros(N); idx = rng.integers(0, N, 90); crack[idx] = rng.uniform(.2, .6, 90) * rng.choice([-1, 1], 90)
    L += hiss + lp(crack, 1) * .35
    for i in range(n_items): add(ping(1200 + i * 60), 2.2 + i * 0.12, .12)
    for i in range(n_lines): add(ping(1600), 3.6 + i * 0.55, .1)
    L = np.tanh(L * 1.3)
    L = lp(L, 1)
    L /= max(1e-9, np.abs(L).max()); L *= 0.85
    L[:int(.25 * sr)] *= np.linspace(0, 1, int(.25 * sr))
    L[-int(1.0 * sr):] *= np.linspace(1, 0, int(1.0 * sr))
    pcm = (np.stack([L, L], 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

def build(crypto, stocks, now, out_mp4, out_jpg):
    allm = crypto + stocks
    hero = max(allm, key=lambda x: abs(x["chg"]))
    items = [x for x in allm if x is not hero]
    lines = lines_for(crypto, stocks, now.weekday() >= 5 or now.weekday() == 0)
    base = Image.new("RGB", (W, H), BG)
    logo = Image.open(os.path.join(ROOT, "tools", "story", "logo.png")).convert("RGB").resize((100, 100))
    mask = Image.new("L", (100, 100), 0); ImageDraw.Draw(mask).ellipse((0, 0, 100, 100), fill=255)
    ctx = {"hero": hero, "items": items, "lines": lines, "now": now, "base": base, "logo": logo, "mask": mask}
    wav = out_mp4 + ".wav"; soundtrack(wav, hero["chg"] >= 0, len(items), len(lines))
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", wav, "-shortest",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out_mp4],
                          stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        f = frame(i / FPS, ctx); ff.stdin.write(f.tobytes())
        if i == int(7 * FPS): f.save(out_jpg, quality=90)
    ff.stdin.close(); ff.wait(); os.remove(wav)
    return hero, lines

def main():
    now = dt.datetime.now(ET); day = now.date().isoformat()
    d = os.path.join(ROOT, "docs", "media", "stories"); os.makedirs(d, exist_ok=True)
    crypto, stocks = fetch()
    hero, lines = build(crypto, stocks, now, os.path.join(d, f"{day}.mp4"), os.path.join(d, f"{day}-poster.jpg"))
    at = (now + dt.timedelta(minutes=60)).replace(second=0, microsecond=0)
    q = [{"id": f"story-{day}", "at": at.isoformat(), "kind": "story", "threads": False,
          "media": [f"https://autopilotio-oss.github.io/autopilot-engine/media/stories/{day}.mp4"],
          "text": f"Market check: {hero['name']} {pct(hero['chg'])}. " + " ".join(lines)}]
    json.dump(q, open(os.path.join(ROOT, "queue", f"{day}-story.json"), "w"), indent=1)
    print("story ready", day, hero["name"], lines)

if __name__ == "__main__":
    main()
