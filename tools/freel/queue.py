"""Factory reel queue. One JSON per reel in queue/freel/.
status: rendered -> (proof gate passes + test plan) approved -> posted.   Nothing posts while gate != "pass".
python tools/freel/queue.py add <ep-stem>        (CI, after render)
python tools/freel/queue.py list
python tools/freel/queue.py set <id> <field> <value>"""
import os, sys, json, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); Q = f"{ROOT}/queue/freel"
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
def add(ep):
    E = json.load(open(f"{ROOT}/tools/freel/eps/{ep}.json")); os.makedirs(Q, exist_ok=True); p = f"{Q}/{E['id']}.json"
    old = json.load(open(p)) if os.path.exists(p) else {}
    kw = E["beats"][-1]["screen"].get("kw")
    old.update({"id": E["id"], "ep": ep, "kind": E.get("kind"), "hook": E["hook"], "keyword": kw,
                "video": f"https://autopilotoi.app/media/freel/{E['id']}.mp4", "poster": f"https://autopilotoi.app/media/freel/{E['id']}-poster.jpg",
                "caption": E["caption"], "rendered_at": now()})
    old.setdefault("status", "rendered"); old.setdefault("gate", "pending"); old.setdefault("posts", [])
    json.dump(old, open(p, "w"), indent=1, ensure_ascii=False); print("queued", E["id"], old["status"], "gate", old["gate"])
def lst():
    for f in sorted(os.listdir(Q)) if os.path.isdir(Q) else []:
        j = json.load(open(f"{Q}/{f}")); print(j["id"], j["status"], "gate:", j["gate"], j["video"])
if __name__ == "__main__":
    c = sys.argv[1]
    if c == "add": add(sys.argv[2])
    elif c == "list": lst()
    elif c == "set":
        p = f"{Q}/{sys.argv[2]}.json"; j = json.load(open(p)); v = sys.argv[4]
        try: v = json.loads(v)
        except Exception: pass
        j[sys.argv[3]] = v; json.dump(j, open(p, "w"), indent=1, ensure_ascii=False); print("ok")
