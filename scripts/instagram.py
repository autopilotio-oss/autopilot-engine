"""Minimal client for the official Instagram API with Instagram Login (graph.instagram.com).
Publishes reels, single images and carousels to a professional Instagram account."""
import os, time, json, subprocess, urllib.request, urllib.parse

BASE = os.environ.get("IG_API_BASE", "https://graph.facebook.com/v21.0")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENC = os.path.join(ROOT, "state", "ig_token.enc")

class IGError(Exception):
    pass

def _req(method, path, params, token):
    params = dict(params or {}); params["access_token"] = token
    data = urllib.parse.urlencode(params).encode()
    url = path if path.startswith("http") else BASE + path
    req = urllib.request.Request(f"{url}?{data.decode()}") if method == "GET" else urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = f"{e.code} {e.read().decode()[:400]}"
        print(f"::error title=Instagram API::{msg}", flush=True)
        raise IGError(msg)

def get_token():
    """System user token from the IG_TOKEN secret (never expires). Falls back to an encrypted Instagram Login key."""
    t = "".join(os.environ.get("IG_TOKEN", "").split())
    if t:
        return t
    key = "".join(os.environ.get("IG_APP_SECRET", "").split())
    if not key or not os.path.exists(ENC):
        return ""
    r = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-a", "-A", "-pass", "env:K", "-in", ENC],
                       capture_output=True, text=True, env={**os.environ, "K": key})
    return r.stdout.strip() if r.returncode == 0 else ""

def user_id(token):
    """Instagram account id: IG_USER_ID if set, otherwise discovered from the token."""
    uid = "".join(os.environ.get("IG_USER_ID", "").split())
    if uid:
        return uid
    try:
        for pg in _req("GET", "/me/accounts", {"fields": "instagram_business_account"}, token).get("data", []):
            if pg.get("instagram_business_account"):
                return pg["instagram_business_account"]["id"]
    except IGError:
        pass
    return _req("GET", "/me", {"fields": "user_id"}, token).get("user_id")

def wait_ready(cid, token, tries=40, gap=10):
    for _ in range(tries):
        st = _req("GET", f"/{cid}", {"fields": "status_code"}, token).get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            raise IGError(f"container {cid}: {st}")
        time.sleep(gap)
    raise IGError(f"container {cid} never finished")

def post(uid, token, kind, caption, urls):
    """kind: video | image | carousel | story. Text only posts are skipped (Instagram needs media)."""
    if kind == "video":
        cid = _req("POST", f"/{uid}/media", {"media_type": "REELS", "video_url": urls[0], "caption": caption, "share_to_feed": "true"}, token)["id"]
    elif kind == "story":
        cid = _req("POST", f"/{uid}/media", {"media_type": "STORIES", "image_url": urls[0]}, token)["id"]
    elif kind == "image":
        cid = _req("POST", f"/{uid}/media", {"image_url": urls[0], "caption": caption}, token)["id"]
    elif kind == "carousel":
        kids = []
        for u in urls[:10]:
            v = u.lower().endswith((".mp4", ".mov"))
            k = _req("POST", f"/{uid}/media", {"is_carousel_item": "true", **({"media_type": "VIDEO", "video_url": u} if v else {"image_url": u})}, token)["id"]
            wait_ready(k, token); kids.append(k)
        cid = _req("POST", f"/{uid}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": caption}, token)["id"]
    else:
        return None
    wait_ready(cid, token)
    return _req("POST", f"/{uid}/media_publish", {"creation_id": cid}, token)["id"]

def ig_caption(text):
    """Threads copy adapted for Instagram: links are not clickable there, so point to the bio."""
    import re
    t = re.sub(r"https?://\S+", "Link in bio.", text)
    return t + "\n\n#smallbusiness #aitools #claudeai #automation #smallbusinessowner"
