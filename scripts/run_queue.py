"""Publishes every queued post whose time has come. Safe to run every 15 minutes.

Queue files: queue/YYYY-MM-DD.json, a list of posts:
  {"id": "d01-am", "at": "2026-11-03T08:00:00-05:00", "kind": "carousel",
   "text": "...", "media": ["media/d01/slide_1.jpg", ...]}
Drop a file named PAUSE in the repo root to stop all posting.
"""
import os, sys, json, glob, datetime as dt
sys.path.insert(0, os.path.dirname(__file__))
import threads

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state", "posted.json")
DRY = os.environ.get("DRY_RUN") == "1"
MAX_PER_RUN = 3
MAX_PER_DAY = 6   # far below the API's 250, keeps the page looking human

def load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def main(now=None):
    if os.path.exists(os.path.join(ROOT, "PAUSE")):
        print("PAUSE file present, nothing posted."); return []
    token = os.environ.get("THREADS_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "OWNER/autopilot-engine")
    branch = os.environ.get("BRANCH", "main")
    raw = f"https://raw.githubusercontent.com/{repo}/{branch}/"
    now = now or dt.datetime.now(dt.timezone.utc)
    posted = load(STATE, {})
    today = now.date().isoformat()
    today_count = sum(1 for v in posted.values() if v.get("at", "").startswith(today))
    due = []
    for f in sorted(glob.glob(os.path.join(ROOT, "queue", "*.json"))):
        for p in load(f, []):
            if p["id"] in posted: continue
            at = dt.datetime.fromisoformat(p["at"])
            if at <= now and (now - at) < dt.timedelta(hours=6):
                due.append(p)
    done = []
    uid = None
    for p in sorted(due, key=lambda x: x["at"])[:MAX_PER_RUN]:
        if today_count >= MAX_PER_DAY:
            print("daily cap reached"); break
        urls = [raw + m for m in p.get("media", [])]
        if DRY:
            print("DRY", p["id"], p["kind"], len(urls), "media"); mid = "dry"
        else:
            uid = uid or threads.me(token)["id"]
            try:
                mid = threads.post(uid, token, p["kind"], p["text"], urls)
            except threads.ThreadsError as e:
                print("FAILED", p["id"], e); continue
        posted[p["id"]] = {"media_id": mid, "at": now.isoformat(), "kind": p["kind"]}
        today_count += 1; done.append(p["id"]); print("posted", p["id"], mid)
    if done and not DRY:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        json.dump(posted, open(STATE, "w"), indent=1)
    return done

if __name__ == "__main__":
    main()
