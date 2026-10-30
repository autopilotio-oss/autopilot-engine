"""Seb approves every post before it goes out.

About 1 hour before a post is due, a GitHub issue is opened with the exact caption and media,
assigned to the repo owner so the GitHub app sends a notification.
Reply on the issue:  YES (or ✅ 👍 ok approve post)  -> it posts at its time (or right away if late)
                     NO  (or ❌ 👎 skip)              -> it never posts
No answer = it waits (up to 6 hours after its time), then expires without posting.
Turn this off with config/approval.json {"required": false}.
"""
import os, re, json, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state", "approvals.json")
CFG = os.path.join(ROOT, "config", "approval.json")
YES = re.compile(r"(\b(yes|yep|yeah|approve|approved|ok|okay|go|post it|send it|lgtm)\b|✅|👍|🔥)", re.I)
NO = re.compile(r"(\b(no|nope|skip|don'?t|reject|kill)\b|❌|👎)", re.I)
SITE = "https://autopilotio-oss.github.io/autopilot-engine/"

def required():
    try: return json.load(open(CFG)).get("required", True)
    except Exception: return True

def _load():
    try: return json.load(open(STATE))
    except Exception: return {}

def _save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True); json.dump(s, open(STATE, "w"), indent=1)

def _gh(method, path, body=None):
    tok = os.environ.get("GITHUB_TOKEN", ""); repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not tok or not repo: raise RuntimeError("no GitHub token")
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}{path}", method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read() or "null")

def _owner():
    return os.environ.get("GITHUB_REPOSITORY", "/").split("/")[0]

def _body(p, ig_caption):
    m = (p.get("media") or [""])[0]
    if p.get("kind") == "video":
        poster = m.rsplit(".", 1)[0] + "-poster.jpg"
        media = f"### ▶️ [Watch the reel]({m})\n\n![preview]({poster})"
    elif p.get("kind") == "carousel":
        media = "\n".join(f"**Slide {i}**\n\n![slide {i}]({u})\n" for i, u in enumerate(p.get("media", []), 1))
    elif m:
        media = f"![post]({m})"
    else:
        media = "_Text only (Threads only)_"
    return f"""## Reply **YES** to post it, or **NO** to skip it.

**Goes out:** {p['at']} (US Eastern) · **Where:** {'Instagram only' if p.get('threads') is False else ('Threads' + ('' if p.get('kind') == 'text' or p.get('ig') is False else ' + Instagram'))}

{media}

### Threads caption
```
{p['text']}
```

### Instagram caption
```
{ig_caption}
```

_No answer = it waits and does not post. Want changes? Tell Claude in chat._
"""

def request_upcoming(posts, now, ig_caption, posted_ids, lead_minutes=75):
    """Open an approval issue for each post due within the next ~hour."""
    import datetime as dt
    s = _load(); changed = False
    for p in posts:
        if p["id"] in s or p["id"] in posted_ids: continue
        at = dt.datetime.fromisoformat(p["at"])
        if now < at <= now + dt.timedelta(minutes=lead_minutes) or (at <= now and now - at < dt.timedelta(hours=6)):
            try:
                iss = _gh("POST", "/issues", {"title": f"Approve post · {at.strftime('%a %b %d %I:%M %p')} ET · {p['id']}",
                                              "body": _body(p, ig_caption(p["text"])), "assignees": [_owner()]})
                s[p["id"]] = {"issue": iss["number"], "status": "waiting"}; changed = True
                print("approval requested", p["id"], "issue", iss["number"])
            except Exception as e:
                print("could not open approval issue", p["id"], e)
    if changed: _save(s)

def status(pid):
    """approved | rejected | waiting"""
    s = _load(); a = s.get(pid)
    if not a: return "waiting"
    if a["status"] in ("approved", "rejected"): return a["status"]
    try:
        for c in _gh("GET", f"/issues/{a['issue']}/comments?per_page=100") or []:
            if c["user"]["login"].lower() != _owner().lower(): continue
            t = c.get("body") or ""
            if NO.search(t): a["status"] = "rejected"
            elif YES.search(t): a["status"] = "approved"
        if a["status"] == "waiting":
            iss = _gh("GET", f"/issues/{a['issue']}")
            if iss.get("state") == "closed" and iss.get("state_reason") == "completed": a["status"] = "approved"
            elif iss.get("state") == "closed": a["status"] = "rejected"
    except Exception as e:
        print("approval check failed", pid, e)
    s[pid] = a; _save(s)
    return a["status"]

def finish(pid, note):
    s = _load(); a = s.get(pid)
    if not a: return
    try:
        _gh("POST", f"/issues/{a['issue']}/comments", {"body": note})
        _gh("PATCH", f"/issues/{a['issue']}", {"state": "closed"})
    except Exception as e:
        print("could not close issue", pid, e)
    a["closed"] = True; s[pid] = a; _save(s)
