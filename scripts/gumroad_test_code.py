"""One use, 100% off test code for a checkout + delivery test (the order is $0, so the ledger never counts it as revenue).
python3 scripts/gumroad_test_code.py create <permalink> <CODE> [cents_off] | delete <permalink> <CODE>
With cents_off (e.g. 3800 on the $39 kit) the code leaves a small paid order for the ledger and refund test; the list price never changes."""
import os, sys, json, urllib.request, urllib.parse
TOK = os.environ["GUMROAD_TOKEN"]; API = "https://api.gumroad.com/v2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
act, perm, code = sys.argv[1], sys.argv[2], sys.argv[3].upper()
pid = json.load(open(os.path.join(ROOT, "state", "products.json")))[perm]["id"]
def call(m, p, d=None):
    d = dict(d or {}, access_token=TOK)
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + p, data=urllib.parse.urlencode(d).encode(), method=m), timeout=60).read())
if act == "create":
    cents = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] else ""
    body = {"name": code, "max_purchase_count": 1}
    body.update({"amount_off": int(cents), "offer_type": "cents"} if cents else {"amount_off": 100, "offer_type": "percent"})
    r = call("POST", f"/products/{pid}/offer_codes", body)
    print("created", code, "for", perm, "off:", (cents + " cents") if cents else "100%", "max uses 1, success:", r.get("success"))
else:
    codes = json.loads(urllib.request.urlopen(f"{API}/products/{pid}/offer_codes?" + urllib.parse.urlencode({"access_token": TOK}), timeout=60).read()).get("offer_codes", [])
    for c in codes:
        if (c.get("name") or "").upper() == code: call("DELETE", f"/products/{pid}/offer_codes/{c['id']}"); print("deleted", code)
