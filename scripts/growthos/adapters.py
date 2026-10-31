"""Provider adapters and the access matrix (sections 04, 17; test T14).

Each adapter reports its real status. If access is missing it says LIVE_BLOCKED and uses a mock that is labeled as
a mock, so nothing downstream can mistake simulated data for live data."""
import hmac, os

STATUS = {
    "gumroad":   {"status": "LIVE", "how": "GUMROAD_TOKEN in GitHub Actions; polled every 3h (static site: no webhook endpoint)"},
    "metricool": {"status": "LIVE", "how": "Claude connector, brand 7761544 (sessions only)"},
    "kit":       {"status": "LIVE", "how": "Claude connector (sessions only)"},
    "github":    {"status": "LIVE", "how": "repo scoped token; secrets list and org endpoints blocked"},
    "elevenlabs": {"status": "LIVE", "how": "ELEVENLABS_API_KEY in GitHub Actions"},
    "manychat":  {"status": "LIVE_BLOCKED", "how": "no API or connector available; owner edits keywords in the app", "smallest_ask": "none possible today; keep CTA rule (config/manychat.json)"},
    "goatcounter": {"status": "LIVE_BLOCKED", "how": "script on site, no API token", "smallest_ask": "GOATCOUNTER_TOKEN repo secret (read only API key)"},
    "support_inbox": {"status": "LIVE", "how": "Gmail connector (business inbox) in the Support + inbox monitor task; drafts only, verified 2026-10-31"},
}


class Blocked(Exception):
    pass


class ManyChatAdapter:
    """No live access exists. send() refuses; status() tells the truth."""
    name = "manychat"

    def __init__(self, token=None):
        self.live = bool(token)

    def status(self):
        return STATUS["manychat"] if not self.live else {"status": "UNVERIFIED", "how": "token given but never tested"}

    def send(self, *a, **k):
        raise Blocked("manychat: LIVE_BLOCKED (no API access); nothing sent")


class MockManyChat:
    name = "manychat.mock"
    is_mock = True

    def __init__(self):
        self.sent = []

    def send(self, keyword, link):
        self.sent.append({"keyword": keyword, "link": link, "mock": True})
        return {"mock": True, "ok": True}


def verify_gumroad_ping(form, expected_seller_id, url_secret, expected_secret):
    """Gumroad pings are not signed. Defense: a secret in the ping URL plus the seller_id check (constant time),
    then re-fetch the sale from the API before trusting it. Returns (ok, reason)."""
    if not expected_secret or not hmac.compare_digest(str(url_secret or ""), str(expected_secret)):
        return False, "bad or missing url secret"
    if not hmac.compare_digest(str(form.get("seller_id", "")), str(expected_seller_id)):
        return False, "seller_id mismatch"
    for k in ("sale_id", "product_permalink", "price"):
        if not form.get(k):
            return False, f"missing {k}"
    if not str(form["price"]).isdigit():
        return False, "price must be integer cents"
    return True, "ok (still re-fetch the sale from the API before counting it)"


def matrix():
    return STATUS
