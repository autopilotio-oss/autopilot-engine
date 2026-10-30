"""Replies once to any comment that contains a keyword (like BRAIN) with the free link.
Reads state/comments.json (filled by collect.py), remembers who got a reply in state/replied.json."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(__file__))
import threads
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(os.path.join(ROOT, "PAUSE")): sys.exit(0)
def load(p, d):
    try: return json.load(open(os.path.join(ROOT, p)))
    except Exception: return d
token = threads.get_token()
if not token:
    print("No THREADS_TOKEN yet, skipping."); sys.exit(0)
cfg = load("config/keywords.json", {})
rules = {k.upper(): v for k, v in cfg.get("replies", {}).items()} or {w.upper(): cfg.get("reply", "") for w in cfg.get("keywords", [])}
words = list(rules)
com = load("state/comments.json", {}); sent = load("state/replied.json", {})
me = threads.me(token); uid = me["id"]; myname = (me.get("username") or "").lower()
n = 0
for pid, items in com.items():
    for c in items:
        cid, txt, who = c.get("id"), (c.get("text") or ""), (c.get("username") or "").lower()
        if not cid or cid in sent or who == myname: continue
        hit = next((w for w in words if re.search(r"\b" + re.escape(w) + r"\b", txt.upper())), None)
        if not hit: continue
        if n >= cfg.get("max_per_run", 20): break
        try:
            sent[cid] = threads.reply(uid, token, cid, rules[hit]); n += 1; print("keyword reply", cid)
        except threads.ThreadsError as e:
            print("fail", cid, e)
json.dump(sent, open(os.path.join(ROOT, "state/replied.json"), "w"), indent=1)
print("keyword replies sent:", n)
