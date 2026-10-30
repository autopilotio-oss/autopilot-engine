"""Instagram version of keyword replies: anyone who comments a keyword (CREDIT, BILL, DEBT...) on our
Instagram posts gets a public reply with the free guide link. Needs the comments permission on IG_TOKEN."""
import os, sys, json, re, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import instagram
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(os.path.join(ROOT, "PAUSE")): sys.exit(0)
def load(p, d):
    try: return json.load(open(os.path.join(ROOT, p)))
    except Exception: return d
token = instagram.get_token()
if not token: print("No IG token, skipping."); sys.exit(0)
cfg = load("config/keywords.json", {}); rules = {k.upper(): v for k, v in cfg.get("replies", {}).items()}
sent = load("state/ig_replied.json", {}); posted = load("state/posted_ig.json", {})
cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=21); n = 0
try: me = instagram._req("GET", "/" + instagram.user_id(token), {"fields": "username"}, token).get("username", "").lower()
except Exception: me = "autopilot.oi"
for pid, v in posted.items():
    mid = v.get("media_id")
    if not mid or v.get("kind") == "story" or dt.datetime.fromisoformat(v["at"]) < cut: continue
    try: cs = instagram._req("GET", f"/{mid}/comments", {"fields": "id,text,username", "limit": 50}, token).get("data", [])
    except Exception as e: print("::warning title=IG comments::", pid, str(e)[:200]); continue
    for c in cs:
        cid, txt, who = c.get("id"), (c.get("text") or ""), (c.get("username") or "").lower()
        if not cid or cid in sent or who == me: continue
        hit = next((w for w in rules if re.search(r"\b" + re.escape(w) + r"\b", txt.upper())), None)
        if not hit or n >= cfg.get("max_per_run", 20): continue
        try:
            r = instagram._req("POST", f"/{cid}/replies", {"message": f"@{who} " + rules[hit] if who else rules[hit]}, token)
            sent[cid] = r.get("id", True); n += 1; print("ig keyword reply", cid, hit)
        except Exception as e: print("::warning title=IG reply::", str(e)[:200])
json.dump(sent, open(os.path.join(ROOT, "state/ig_replied.json"), "w"), indent=1)
print("ig keyword replies sent:", n)
