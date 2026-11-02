"""One use, 100% off test code for a checkout + delivery test (the order is $0, so the ledger never counts it as revenue).
python3 scripts/gumroad_test_code.py create <permalink> <CODE> | delete <permalink> <CODE>"""
import os, sys, json, urllib.request, urllib.parse
TOK = os.environ["GUMROAD_TOKEN"]; API = "https://api.gumroad.com/v2"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
act, perm, code = sys.argv[1], sys.argv[2], sys.argv[3].upper()
pid = json.load(open(os.path.join(ROOT, "state", "products.json")))[perm]["id"]
def call(m, p, d=None):
    d = dict(d or {}, access_token=TOK)
    return json.loads(urllib.request.urlopen(urllib.request.Request(API + p, data=urllib.parse.urlencode(d).encode(), method=m), timeout=60).read())
if act == "create":
    r = call("POST", f"/products/{pid}/offer_codes", {"name": code, "amount_off": 100, "offer_type": "percent", "max_purchase_count": 1})
    print("created", code, "for", perm, "max uses 1, success:", r.get("success"))
else:
    codes = json.loads(urllib.request.urlopen(f"{API}/products/{pid}/offer_codes?" + urllib.parse.urlencode({"access_token": TOK}), timeout=60).read()).get("offer_codes", [])
    for c in codes:
        if (c.get("name") or "").upper() == code: call("DELETE", f"/products/{pid}/offer_codes/{c['id']}"); print("deleted", code)
