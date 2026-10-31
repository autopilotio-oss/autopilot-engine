"""Revenue ledger: Gumroad is the source of truth for orders and refunds.

python3 scripts/revenue/ledger.py sync       (needs GUMROAD_TOKEN, runs in GitHub Actions)
python3 scripts/revenue/ledger.py summary    (rebuild state/ledger/summary.json from the events file)

Writes PII-free records only: no email, name, IP, card, address or license key. Order ids are hashed.
The repo is public, so this file must never hold personal data. See revenue-engine-v2/METRICS.md."""
import hashlib, json, os, sys, urllib.parse, urllib.request, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ids import offer_id, source_of

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIR = os.path.join(ROOT, "state", "ledger")
EVENTS = os.path.join(DIR, "events.jsonl")
SUMMARY = os.path.join(DIR, "summary.json")
PRODUCTS = os.path.join(DIR, "products.json")
API = "https://api.gumroad.com/v2"
SALT = "autopilot-oi-ledger-v1"  # not a secret: hashing only keeps raw Gumroad ids out of a public repo


def h(x):
    return hashlib.sha256((SALT + str(x)).encode()).hexdigest()[:16]


def now():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None).isoformat() + "Z"


def load_events(path=EVENTS):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path) if l.strip()]


def to_events(sale: dict) -> list:
    """Map one Gumroad sale object to ledger events. Pure function (tested)."""
    perm = sale.get("product_permalink") or sale.get("permalink") or ""
    oid = offer_id(perm) if perm else "unknown"
    cur = (sale.get("currency") or sale.get("currency_symbol") or "usd").lower()
    cur = {"$": "usd"}.get(cur, cur)
    gross = int(sale.get("price") or 0)              # cents, what the buyer paid
    fee = int(sale.get("gumroad_fee") or 0)          # cents
    params = sale.get("url_params") or {}
    if isinstance(params, str):
        params = dict(urllib.parse.parse_qsl(params))
    src = source_of(params)
    ref = (sale.get("referrer") or "").split("?")[0][:120] or "unknown"
    oh = h(sale.get("id") or sale.get("sale_id"))
    ts = sale.get("created_at") or sale.get("sale_timestamp") or now()
    evs = [{"event_id": f"order_paid:{oh}", "type": "order_paid", "order": oh, "offer_id": oid, "gross_cents": gross,
            "fee_cents": fee, "currency": cur, "ts": ts, "referrer": ref, **src,
            "test": bool(sale.get("test")), "free": gross == 0}]
    refunded = sale.get("refunded") or sale.get("partially_refunded") or sale.get("chargedback")
    if refunded:
        amt = gross if sale.get("refunded") or sale.get("chargedback") else int(sale.get("amount_refunded_cents") or 0)
        evs.append({"event_id": f"refund_processed:{oh}", "type": "refund_processed", "order": oh, "offer_id": oid,
                    "refund_cents": amt, "currency": cur, "ts": sale.get("refunded_at") or ts,
                    "reason": "chargeback" if sale.get("chargedback") else "refund"})
    return evs


def merge(existing: list, new: list) -> tuple[list, int]:
    """Idempotent: an event_id is stored once, however many times a sale is seen."""
    seen = {e["event_id"] for e in existing}
    added = [e for e in new if e["event_id"] not in seen and not seen.add(e["event_id"])]
    return existing + added, len(added)


def summarize(events: list, today: datetime.date | None = None) -> dict:
    today = today or datetime.datetime.now(datetime.timezone.utc).date()
    paid = [e for e in events if e["type"] == "order_paid" and not e.get("test") and not e.get("free")]
    refunds = {e["order"]: e for e in events if e["type"] == "refund_processed"}

    def window(days):
        start = today - datetime.timedelta(days=days - 1)
        sel = [e for e in paid if start.isoformat() <= e["ts"][:10] <= today.isoformat()]
        by_cur = {}
        for e in sel:
            c = by_cur.setdefault(e["currency"], {"orders": 0, "gross_cents": 0, "fee_cents": 0, "refund_cents": 0})
            c["orders"] += 1; c["gross_cents"] += e["gross_cents"]; c["fee_cents"] += e["fee_cents"]
            if e["order"] in refunds:
                c["refund_cents"] += refunds[e["order"]]["refund_cents"]
        for c in by_cur.values():
            c["net_cents"] = c["gross_cents"] - c["fee_cents"] - c["refund_cents"]
        return {"orders": len(sel), "by_currency": by_cur}

    by_offer, by_source = {}, {}
    for e in paid:
        o = by_offer.setdefault(e["offer_id"], {"orders": 0, "gross_cents": 0, "refunds": 0})
        o["orders"] += 1; o["gross_cents"] += e["gross_cents"]; o["refunds"] += e["order"] in refunds
        s = by_source.setdefault(e["utm_source"], {"orders": 0, "gross_cents": 0})
        s["orders"] += 1; s["gross_cents"] += e["gross_cents"]
    attributed = sum(1 for e in paid if e["utm_source"] != "unknown")
    return {"generated": now(), "verified_orders_all_time": len(paid),
            "last_1d": window(1), "last_7d": window(7), "last_30d": window(30),
            "by_offer": by_offer, "by_source": by_source,
            "attribution_coverage": (attributed / len(paid)) if paid else None,
            "refunds_all_time": len(refunds), "currencies": sorted({e["currency"] for e in paid}),
            "notes": "Gumroad is the source of truth. Net = gross - Gumroad fee - refunds. Taxes are not included. Currencies are never mixed."}


def api_get(path, params):
    tok = os.environ["GUMROAD_TOKEN"].strip()
    q = urllib.parse.urlencode({**params, "access_token": tok})
    return json.loads(urllib.request.urlopen(f"{API}{path}?{q}", timeout=60).read().decode())


def sync():
    os.makedirs(DIR, exist_ok=True)
    status = {"ran": now(), "sales_api": "unknown", "products_api": "unknown"}
    # products: public facts only (what is buyable and at what price)
    try:
        r = api_get("/products", {})
        prods = [{"permalink": (p.get("custom_permalink") or (p.get("short_url") or "").rstrip("/").split("/")[-1]),
                  "name": p.get("name"), "published": bool(p.get("published")), "price_cents": p.get("price"),
                  "currency": p.get("currency"), "sales_count": p.get("sales_count"), "deleted": bool(p.get("deleted"))}
                 for p in r.get("products", [])]
        json.dump({"checked": now(), "products": sorted(prods, key=lambda x: x["permalink"] or "")}, open(PRODUCTS, "w"), indent=1)
        status["products_api"] = f"ok ({len(prods)} products)"
    except Exception as e:
        status["products_api"] = "error: " + repr(e)[:160]
    events = load_events(); new = []; page_key = None; pages = 0
    try:
        while pages < 50:
            params = {"page_key": page_key} if page_key else {}
            r = api_get("/sales", params)
            for s in r.get("sales", []):
                new += to_events(s)
            page_key = r.get("next_page_key"); pages += 1
            if not page_key:
                break
        status["sales_api"] = f"ok ({pages} page(s))"
    except Exception as e:
        status["sales_api"] = "error: " + repr(e)[:160]
    events, added = merge(events, new)
    events.sort(key=lambda e: (e["ts"], e["event_id"]))
    with open(EVENTS, "w") as f:
        for e in events:
            f.write(json.dumps(e, sort_keys=True) + "\n")
    s = summarize(events); s["sync"] = status | {"new_events": added}
    json.dump(s, open(SUMMARY, "w"), indent=1)
    print(json.dumps(s["sync"]))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    if cmd == "sync":
        sync()
    else:
        s = summarize(load_events()); json.dump(s, open(SUMMARY, "w"), indent=1); print(json.dumps(s, indent=1)[:600])
