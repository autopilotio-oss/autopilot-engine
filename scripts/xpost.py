"""Posts text threads to X with the official X API v2 (pay per use, about $0.015 a post, $0.20 if it has a link).
Needs secrets X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET (from the X developer portal, Keys and tokens)."""
import os, json, time, hmac, hashlib, base64, secrets, urllib.request, urllib.parse

URL = "https://api.x.com/2/tweets"

class XError(Exception):
    pass

def creds():
    k = {n: "".join(os.environ.get(n, "").split()) for n in ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")}
    return k if all(k.values()) else None

def _auth(method, url, c):
    q = lambda s: urllib.parse.quote(str(s), safe="~")
    o = {"oauth_consumer_key": c["X_API_KEY"], "oauth_nonce": secrets.token_hex(16), "oauth_signature_method": "HMAC-SHA1",
         "oauth_timestamp": str(int(time.time())), "oauth_token": c["X_ACCESS_TOKEN"], "oauth_version": "1.0"}
    params = "&".join(f"{q(k)}={q(v)}" for k, v in sorted(o.items()))
    base = "&".join([method, q(url), q(params)])
    key = f"{q(c['X_API_SECRET'])}&{q(c['X_ACCESS_SECRET'])}"
    o["oauth_signature"] = base64.b64encode(hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()).decode()
    return "OAuth " + ", ".join(f'{q(k)}="{q(v)}"' for k, v in sorted(o.items()))

def tweet(text, reply_to=None, c=None):
    c = c or creds()
    body = {"text": text}
    if reply_to: body["reply"] = {"in_reply_to_tweet_id": reply_to}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"Authorization": _auth("POST", URL, c), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())["data"]["id"]
    except urllib.error.HTTPError as e:
        msg = f"{e.code} {e.read().decode()[:300]}"
        print(f"::error title=X API::{msg}", flush=True)
        raise XError(msg)

def thread(tweets):
    c = creds()
    if not c: raise XError("X keys not set")
    first = prev = None
    for t in tweets:
        prev = tweet(t[:280], prev, c); first = first or prev
        time.sleep(2)
    return first

def from_carousel(slides):
    """Turns carousel slide data into a text thread (one tweet per slide)."""
    out = []
    for i, s in enumerate(slides, 1):
        parts = [p for p in [(f"{s['n']}. " if s.get("n") and s["n"].isdigit() else "") + s["t"], s.get("s", ""), s.get("x", ""), s.get("s2", "")] if p]
        t = "\n\n".join(parts)
        if s.get("hook"): t = t.rstrip(" 👇") + " 🧵👇"
        if s.get("cta"): t = t.replace("Comment BRAIN and I'll send you", "Get").replace("Comment BRAIN and I'll send it free.", "Get it free:") + "\n\nautopilotio-oss.github.io/autopilot-engine"
        out.append(t)
    return out
