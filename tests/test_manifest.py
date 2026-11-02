"""config/offers.json is the single source of truth for offers. These tests fail the build when any surface drifts:
Gumroad product files, site pages, keyword DM replies, the support knowledge base, unposted queued posts and promotions."""
import datetime as dt, glob, html, json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "config", "offers.json")))
OFFERS = {o["id"]: o for o in M["offers"]}


def text(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def site_pages():
    pages = []
    for f in glob.glob(os.path.join(ROOT, "docs", "**", "index.html"), recursive=True):
        if "/media/" in f: continue
        pages.append(f)
    return pages


def unposted_queue_text():
    posted = json.load(open(os.path.join(ROOT, "state", "posted.json")))
    out = []
    for f in glob.glob(os.path.join(ROOT, "queue", "*.json")):
        for p in json.load(open(f)):
            if p.get("id") not in posted: out.append((f, p.get("id"), json.dumps(p, ensure_ascii=False), p.get("at", "")))
    return out


def test_manifest_matches_gumroad_product_files():
    for o in M["offers"]:
        p = json.load(open(os.path.join(ROOT, "products", o["permalink"], "product.json")))
        assert p["price_cents"] == o["price_cents"], (o["id"], p["price_cents"])
        if o.get("gumroad_name"): assert p["name"] == o["gumroad_name"], (o["id"], p["name"])
        assert not p.get("retired"), o["id"]
    for slug, lib in M["library"].items():
        p = json.load(open(os.path.join(ROOT, "products", slug, "product.json")))
        assert p["price_cents"] == lib["price_cents"] and p["name"] == lib["name"], slug


def test_landing_pages_show_manifest_price_and_checkout():
    for o in M["offers"]:
        if not o.get("landing"): continue
        f = os.path.join(ROOT, "docs", o["landing"].strip("/"), "index.html")
        raw = open(f, encoding="utf-8").read()
        assert f"${o['price_cents'] // 100}" in text(f), (o["id"], "price missing on landing")
        assert f"gumroad.com/l/{o['permalink']}" in raw, (o["id"], "checkout link missing on landing")


def test_hero_page_states_limits_and_refund():
    t = text(os.path.join(ROOT, "docs", "front-desk", "index.html")).lower()
    for must in ["claude", "you send", "30 day refund", "not an auto reply service", "example business"]:
        assert must in t, must


def test_workspace_never_presented_as_live_software():
    t = text(os.path.join(ROOT, "docs", "workspace", "index.html")).lower()
    assert "in development" in t and "refundable" in t
    for bad in ["start your subscription", "sign up for workspace", "now available", "start free trial"]:
        assert bad not in t, bad


def test_no_stale_offer_copy_on_live_surfaces():
    hits = []
    surfaces = site_pages() + [os.path.join(ROOT, "config", "keywords.json"), os.path.join(ROOT, "config", "growthos", "support_kb.json")]
    for f in surfaces:
        t = text(f) if f.endswith(".html") else open(f, encoding="utf-8").read()
        for s in M["stale_phrases"]:
            for m in re.finditer(re.escape(s), t):
                ctx = t[max(0, m.start() - 60): m.end() + 60]
                if "formerly" in ctx.lower() or "now called" in ctx.lower(): continue
                hits.append((os.path.relpath(f, ROOT), s))
    for f, pid, t, _ in unposted_queue_text():
        for s in M["stale_phrases"]:
            if s in t: hits.append((os.path.relpath(f, ROOT) + ":" + pid, s))
    assert not hits, hits


def test_no_forbidden_capability_claims():
    hits = []
    for f in site_pages() + [os.path.join(ROOT, "config", "keywords.json")]:
        t = (text(f) if f.endswith(".html") else open(f, encoding="utf-8").read()).lower()
        for sent in re.split(r"(?<=[.!?])\s+", t):
            if re.search(r"\b(not|never|no|doesn't|does not|won't)\b", sent): continue
            for c in M["forbidden_claims"]:
                if c.lower() in sent: hits.append((os.path.relpath(f, ROOT), c))
    assert not hits, hits


def test_keyword_reply_links_resolve():
    k = json.load(open(os.path.join(ROOT, "config", "keywords.json")))
    for kw, reply in k["replies"].items():
        for path in re.findall(r"https://autopilotoi\.app/([^\s?#]*)", reply):
            assert os.path.exists(os.path.join(ROOT, "docs", path.strip("/"), "index.html")), (kw, path)


def test_promotions_not_mentioned_after_expiry():
    now = dt.datetime.now(dt.timezone.utc)
    for promo in M["promotions"]:
        until = dt.datetime.fromisoformat(promo["until"].replace("Z", "+00:00"))
        for f, pid, t, at in unposted_queue_text():
            if promo["code"] in t and at:
                assert dt.datetime.fromisoformat(at) < until, (f, pid, "post with expired promo")
        if now > until:
            for f in site_pages():
                assert promo["code"] not in open(f, encoding="utf-8").read(), (f, promo["code"], "expired promo on site")


def test_paid_ads_cap_is_the_strict_one():
    assert M["budget"]["paid_ads_usd_cap"] <= 60


def test_sales_dashboard_excludes_test_and_free_orders(tmp_path, monkeypatch):
    import importlib, sys
    sys.path.insert(0, os.path.join(ROOT, "scripts", "revenue"))
    import sales_dashboard as sd
    root = tmp_path; (root / "state" / "ledger").mkdir(parents=True); (root / "sales").mkdir()
    ev = [{"type": "order_paid", "order": "a", "offer_id": "autopilot", "gross_cents": 3900, "fee_cents": 440, "currency": "usd", "ts": "2026-11-05T10:00:00Z", "utm_source": "meta", "utm_campaign": "fd1"},
          {"type": "order_paid", "order": "b", "offer_id": "autopilot", "gross_cents": 3900, "fee_cents": 0, "currency": "usd", "ts": "2026-11-05T11:00:00Z", "utm_source": "unknown", "utm_campaign": "unknown", "test": True},
          {"type": "order_paid", "order": "c", "offer_id": "autopilot", "gross_cents": 0, "fee_cents": 0, "currency": "usd", "ts": "2026-11-05T12:00:00Z", "utm_source": "unknown", "utm_campaign": "unknown", "free": True}]
    (root / "state" / "ledger" / "events.jsonl").write_text("\n".join(json.dumps(e) for e in ev))
    (root / "sales" / "spend.csv").write_text("date,channel,campaign,usd,approved_by,note\n2026-11-05,meta,fd1,20,Seb,\n")
    monkeypatch.setattr(sd, "ROOT", str(root))
    out = sd.build()
    row = [r for r in out if r["channel"] == "meta"][0]
    assert row["verified_orders"] == 1 and row["cac_usd"] == 20.0 and row["contribution_usd"] == round(39 - 4.4 - 20, 2)
    assert sum(r["verified_orders"] for r in out) == 1
