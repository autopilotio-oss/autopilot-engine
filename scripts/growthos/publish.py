"""The only publishing path (Viral Validation V2 + Growth OS 09 + Continuous Improvement 04).

approve   <content_id> --quote "<Seb's exact words>" --dest tiktok,instagram   (interactive session with Seb only)
          -> gate.approve (version bound) -> gate.advance to QUEUED -> one policy grant per destination
plan      -> every QUEUED concept and, per destination, the deterministic decision (allowed or why not)
staged    <content_id> <dest> <metricool_uuid>   -> record that the post was scheduled (STAGED)
published <content_id> <dest> <public_url>       -> PUBLISHED, grant used, event content.published
The Publisher scheduled task may call createScheduledPost ONLY for (content_id, dest) pairs that `plan` marks allowed."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "viral"))
from events import Store, ROOT, now  # noqa: E402
import policy, gate  # noqa: E402

STAGED = os.path.join(ROOT, "viral", "staged.json")


def _staged():
    return json.load(open(STAGED)) if os.path.exists(STAGED) else {}


def approve(cid, quote, dests, by="Seb", store=None):
    store = store or Store()
    c = gate.approve(cid, by, "chat", quote)
    if c["state"] != "OWNER_APPROVED":
        return {"ok": False, "state": c["state"], "reason": c.get("hold_reason")}
    c = gate.advance(cid, "publisher-setup")
    v = gate.version_hash(c)
    grants = {d: policy.grant(store, "content.schedule", cid, v, d, by, "chat", quote) for d in dests}
    store.append("content.approval_granted", {"content_id": cid, "version": v, "approval_id": ",".join(grants.values())}, "owner", f"cap:{cid}:{v}", by)
    return {"ok": True, "state": c["state"], "version": v, "grants": grants}


def plan(store=None):
    store = store or Store(); out = []; st = _staged()
    for c in gate.all_concepts():
        if c["state"] != "QUEUED":
            continue
        v = gate.version_hash(c)
        for d in (c.get("platforms") or []):
            if f"{c['content_id']}:{d}" in st:
                out.append({"content_id": c["content_id"], "dest": d, "allowed": False, "reason": "already staged"}); continue
            dec = policy.authorize(store, "publisher", "content.schedule", c["content_id"], v, d, viral_check=policy.viral_gate_check)
            out.append({"content_id": c["content_id"], "dest": d, "version": v, "allowed": dec.allowed, "reason": dec["reason"],
                        "approval_id": dec.get("approval_id"), "cta": (c.get("cta") or {}).get("url"), "caption": (c.get("script") or {}).get("caption")})
    return out


def staged(cid, dest, uuid_):
    st = _staged(); key = f"{cid}:{dest}"
    if key in st:
        return st[key]
    p = {r["dest"]: r for r in plan() if r["content_id"] == cid}
    if dest not in p or not p[dest]["allowed"]:
        raise PermissionError(f"blocked: {cid} on {dest} is not authorized ({p.get(dest, {}).get('reason', 'not queued')})")
    st[key] = {"metricool_uuid": uuid_, "at": now(), "version": p[dest]["version"], "approval_id": p[dest]["approval_id"]}
    json.dump(st, open(STAGED, "w"), indent=1)
    gate.audit("STAGED", cid, "publisher", dest=dest, metricool_uuid=uuid_)
    return st[key]


def published(cid, dest, url, store=None):
    store = store or Store(); st = _staged().get(f"{cid}:{dest}")
    if not st:
        raise PermissionError("not staged by the publisher")
    gate.mark_published(cid, url, dest, "publisher") if gate.load_concept(cid)["state"] == "QUEUED" else None
    policy.use_grant(store, st["approval_id"], "publisher")
    store.append("content.published", {"content_id": cid, "version": st["version"], "platform": dest, "url": url}, "metricool", f"pub:{cid}:{dest}", "publisher")
    return True


def _arg(f, d=None):
    return sys.argv[sys.argv.index(f) + 1] if f in sys.argv else d


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "approve":
        print(json.dumps(approve(sys.argv[2], _arg("--quote", ""), _arg("--dest", "").split(",")), indent=1))
    elif cmd == "plan":
        print(json.dumps(plan(), indent=1))
    elif cmd == "staged":
        print(json.dumps(staged(sys.argv[2], sys.argv[3], sys.argv[4])))
    elif cmd == "published":
        print(published(sys.argv[2], sys.argv[3], sys.argv[4]))
