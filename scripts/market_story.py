"""Daily market brief for Instagram Stories: crypto (24h) and stocks (last close), in plain English.
Prices come from public data (CoinGecko, Stooq). Not financial advice. Writes docs/media/stories/<date>.jpg
and a queue entry (Instagram story, waits for Seb's YES like every post)."""
import os, sys, json, csv, io, urllib.request, datetime as dt
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, "tools", "story", "fonts")
ET = ZoneInfo("America/New_York")
LIME, BG, RED, GREY, WHITE = (212, 255, 58), (10, 10, 10), (255, 107, 107), (138, 138, 132), (244, 244, 240)
CRYPTO = [("bitcoin", "BTC", "Bitcoin"), ("ethereum", "ETH", "Ethereum"), ("solana", "SOL", "Solana")]
STOCKS = [("spy.us", "SPY", "The S&P 500"), ("qqq.us", "QQQ", "The Nasdaq"), ("nvda.us", "NVDA", "Nvidia"), ("aapl.us", "AAPL", "Apple"), ("tsla.us", "TSLA", "Tesla")]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 autopilot-brief"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode()

def fetch():
    ids = ",".join(c[0] for c in CRYPTO)
    cg = json.loads(get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd&include_24hr_change=true"))
    crypto = [{"sym": s, "name": n, "price": cg[i]["usd"], "chg": cg[i]["usd_24h_change"]} for i, s, n in CRYPTO]
    stocks = []
    for code, sym, name in STOCKS:
        rows = [r for r in csv.DictReader(io.StringIO(get(f"https://stooq.com/q/d/l/?s={code}&i=d"))) if r.get("Close")]
        a, b = float(rows[-2]["Close"]), float(rows[-1]["Close"])
        stocks.append({"sym": sym, "name": name, "price": b, "chg": (b / a - 1) * 100, "date": rows[-1]["Date"]})
    return crypto, stocks

def money(v):
    return f"${v:,.0f}" if v >= 1000 else f"${v:,.2f}"

def plain(crypto, stocks, weekend):
    lines = []
    btc = crypto[0]
    lines.append(f"Bitcoin is {'up' if btc['chg'] >= 0 else 'down'} {abs(btc['chg']):.1f}% in the last 24 hours.")
    big = max(crypto[1:], key=lambda c: abs(c["chg"]))
    lines.append(f"{big['name']} moved the most: {'+' if big['chg'] >= 0 else '-'}{abs(big['chg']):.1f}%.")
    spx = stocks[0]
    when = "On Friday" if weekend else "Yesterday"
    lines.append(f"{when}, the S&P 500 (SPY) closed {'up' if spx['chg'] >= 0 else 'down'} {abs(spx['chg']):.1f}%.")
    top = max(stocks[2:], key=lambda s: abs(s["chg"]))
    lines.append(f"Biggest big tech move: {top['name']} {'+' if top['chg'] >= 0 else '-'}{abs(top['chg']):.1f}%.")
    return lines

def font(name, size): return ImageFont.truetype(os.path.join(F, name), size)

def render(crypto, stocks, lines, now, out):
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGB", (W, H), BG); g = ImageDraw.Draw(glow)
    g.ellipse((140, -380, 940, 420), fill=(48, 62, 12)); glow = glow.filter(ImageFilter.GaussianBlur(160))
    im.paste(glow); d = ImageDraw.Draw(im)
    for x in range(0, W, 80): d.line([(x, 0), (x, H)], fill=(18, 18, 18))
    for y in range(0, H, 80): d.line([(0, y), (W, y)], fill=(18, 18, 18))
    logo = Image.open(os.path.join(ROOT, "tools", "story", "logo.png")).resize((88, 88))
    m = Image.new("L", (88, 88), 0); ImageDraw.Draw(m).ellipse((0, 0, 88, 88), fill=255); im.paste(logo, (80, 90), m)
    d.text((190, 98), "AUTOPILOT.OI", font=font("SpaceMono-Bold.ttf", 30), fill=WHITE)
    d.text((190, 138), "@autopilot.oi", font=font("Inter-Medium.otf", 28), fill=GREY)
    d.text((80, 220), "MARKET BRIEF", font=font("BebasNeue-Regular.ttf", 128), fill=WHITE)
    d.text((80, 338), now.strftime("%a %b %d").upper(), font=font("BebasNeue-Regular.ttf", 92), fill=LIME)
    d.text((80, 440), "EXPLAINED LIKE YOU'RE BUSY", font=font("SpaceMono-Bold.ttf", 28), fill=GREY)
    def section(y, title, items, label):
        d.text((80, y), title, font=font("SpaceMono-Bold.ttf", 28), fill=LIME)
        d.text((W - 80, y), label, font=font("SpaceMono-Bold.ttf", 22), fill=GREY, anchor="ra")
        y += 46
        for it in items:
            d.rounded_rectangle((80, y, W - 80, y + 80), 22, fill=(20, 22, 24), outline=(40, 42, 44), width=2)
            d.text((112, y + 40), it["sym"], font=font("Inter-ExtraBold.otf", 38), fill=WHITE, anchor="lm")
            d.text((560, y + 40), money(it["price"]), font=font("Inter-SemiBold.otf", 36), fill=(200, 200, 194), anchor="rm")
            up = it["chg"] >= 0; col = LIME if up else RED
            txt = f"{'▲' if up else '▼'} {abs(it['chg']):.2f}%"
            d.rounded_rectangle((W - 330, y + 13, W - 104, y + 67), 28, fill=(32, 44, 10) if up else (52, 22, 22))
            d.text((W - 217, y + 40), txt, font=font("Inter-Bold.otf", 32), fill=col, anchor="mm")
            y += 90
        return y
    y = section(510, "CRYPTO", crypto, "LAST 24H")
    y = section(y + 24, "STOCKS", stocks, "LAST CLOSE")
    y += 20
    d.rounded_rectangle((80, y, W - 80, y + 66 + 50 * len(lines)), 28, fill=(28, 38, 8), outline=(120, 150, 30), width=2)
    d.text((112, y + 26), "IN PLAIN ENGLISH", font=font("SpaceMono-Bold.ttf", 24), fill=LIME)
    for i, l in enumerate(lines):
        d.text((112, y + 70 + 50 * i), l, font=font("Inter-SemiBold.otf", 29), fill=WHITE)
    d.text((W // 2, y + 120 + 50 * len(lines)), f"Prices as of {now.strftime('%I:%M %p').lstrip('0')} ET. Not financial advice.", font=font("Inter-Medium.otf", 26), fill=GREY, anchor="mm")
    im.save(out, quality=92)

def main():
    now = dt.datetime.now(ET)
    day = now.date().isoformat()
    out = os.path.join(ROOT, "docs", "media", "stories", f"{day}.jpg")
    crypto, stocks = fetch()
    lines = plain(crypto, stocks, now.weekday() >= 5 or now.weekday() == 0)
    render(crypto, stocks, lines, now, out)
    at = (now + dt.timedelta(minutes=60)).replace(second=0, microsecond=0)
    q = [{"id": f"story-{day}", "at": at.isoformat(), "kind": "story", "threads": False,
          "media": [f"https://autopilotio-oss.github.io/autopilot-engine/media/stories/{day}.jpg"],
          "text": "Daily market brief. " + " ".join(lines)}]
    json.dump(q, open(os.path.join(ROOT, "queue", f"{day}-story.json"), "w"), indent=1)
    print("story ready", day, lines)

if __name__ == "__main__":
    main()
