"""Posts comment replies that Claude wrote into queue/replies.json:
  [{"reply_to": "<comment id>", "text": "..."}]  Each is sent once."""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import threads
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.exists(os.path.join(ROOT, "PAUSE")): sys.exit(0)
def load(p, d):
    try: return json.load(open(os.path.join(ROOT, p)))
    except Exception: return d
token = os.environ["THREADS_TOKEN"]
todo = load("queue/replies.json", []); sent = load("state/replied.json", {})
uid = None
for r in todo[:20]:
    if r["reply_to"] in sent: continue
    uid = uid or threads.me(token)["id"]
    try:
        sent[r["reply_to"]] = threads.reply(uid, token, r["reply_to"], r["text"]); print("replied", r["reply_to"])
    except threads.ThreadsError as e:
        print("fail", r["reply_to"], e)
json.dump(sent, open(os.path.join(ROOT, "state/replied.json"), "w"), indent=1)
