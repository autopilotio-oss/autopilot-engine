"""Minimal client for the official Threads API (graph.threads.net)."""
import os, time, json, urllib.request, urllib.parse

BASE = "https://graph.threads.net/v1.0"

class ThreadsError(Exception):
    pass

def _req(method, path, params, token):
    params = dict(params or {}); params["access_token"] = (token or "").strip()
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{BASE}{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{BASE}{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = f"{e.code} {e.read().decode()[:400]}"
        print(f"::error title=Threads API::{msg}", flush=True)
        raise ThreadsError(msg)

def me(token):
    return _req("GET", "/me", {"fields": "id,username"}, token)

def wait_ready(cid, token, tries=30, gap=10):
    for _ in range(tries):
        st = _req("GET", f"/{cid}", {"fields": "status,error_message"}, token)
        if st.get("status") == "FINISHED":
            return
        if st.get("status") in ("ERROR", "EXPIRED"):
            raise ThreadsError(f"container {cid}: {st}")
        time.sleep(gap)
    raise ThreadsError(f"container {cid} never finished")

def container(uid, token, **p):
    return _req("POST", f"/{uid}/threads", p, token)["id"]

def publish(uid, token, cid):
    return _req("POST", f"/{uid}/threads_publish", {"creation_id": cid}, token)["id"]

def post(uid, token, kind, text, urls=()):
    """kind: text | image | video | carousel. urls: public media URLs."""
    if kind == "text":
        cid = container(uid, token, media_type="TEXT", text=text)
    elif kind == "image":
        cid = container(uid, token, media_type="IMAGE", image_url=urls[0], text=text)
    elif kind == "video":
        cid = container(uid, token, media_type="VIDEO", video_url=urls[0], text=text)
    elif kind == "carousel":
        kids = []
        for u in urls[:20]:
            t = "VIDEO" if u.lower().endswith((".mp4", ".mov")) else "IMAGE"
            k = container(uid, token, media_type=t, is_carousel_item="true", **({"video_url": u} if t == "VIDEO" else {"image_url": u}))
            wait_ready(k, token); kids.append(k)
        cid = container(uid, token, media_type="CAROUSEL", children=",".join(kids), text=text)
    else:
        raise ValueError(kind)
    wait_ready(cid, token)
    return publish(uid, token, cid)

def reply(uid, token, to_id, text):
    cid = container(uid, token, media_type="TEXT", text=text, reply_to_id=to_id)
    wait_ready(cid, token)
    return publish(uid, token, cid)

def insights(media_id, token):
    r = _req("GET", f"/{media_id}/insights", {"metric": "views,likes,replies,reposts,quotes,shares"}, token)
    return {m["name"]: m.get("values", [{}])[0].get("value", m.get("total_value", {}).get("value")) for m in r.get("data", [])}

def replies(media_id, token):
    return _req("GET", f"/{media_id}/replies", {"fields": "id,text,username,timestamp"}, token).get("data", [])

def refresh(token):
    r = urllib.request.urlopen(f"https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token={token}", timeout=60)
    return json.loads(r.read())
