"""Pulls views and replies for everything posted in the last 14 days into state/insights.json
and new comments into state/comments.json, so the weekly report and reply writer can read them."""
import os, sys, json, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import threads
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p, d):
    try: return json.load(open(os.path.join(ROOT, p)))
    except Exception: return d
token = os.environ["THREADS_TOKEN"]
posted = load("state/posted.json", {})
ins = load("state/insights.json", {}); com = load("state/comments.json", {})
cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=14)
for pid, v in posted.items():
    if v.get("media_id") in (None, "dry") or dt.datetime.fromisoformat(v["at"]) < cut: continue
    try:
        ins[pid] = {**threads.insights(v["media_id"], token), "checked": dt.datetime.now(dt.timezone.utc).isoformat()}
        com[pid] = threads.replies(v["media_id"], token)
    except threads.ThreadsError as e:
        print("skip", pid, e)
json.dump(ins, open(os.path.join(ROOT, "state/insights.json"), "w"), indent=1)
json.dump(com, open(os.path.join(ROOT, "state/comments.json"), "w"), indent=1)
print("collected", len(ins))
