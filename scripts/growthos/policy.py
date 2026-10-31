"""P0-07 / P0-09 Deterministic policy, action registry, kill switches and scoped approvals (sections 03, 07, 16, 17).

The model may PROPOSE actions; this code DECIDES. A worker can only use actions listed for it in
config/growthos/policy.json. High and critical actions need an owner approval grant that is scoped to one action,
one resource, one resource hash (version) and one destination, expires, and is used once. Content publishing also
requires the Viral Evidence Gate (concept QUEUED with the same version). Kill switches stop outbound work without
touching sales fulfillment.

python3 scripts/growthos/policy.py check <worker> <action> [resource_id] [resource_hash] [destination]
python3 scripts/growthos/policy.py switch stop_all_outbound|resume_outbound|pause_expenses|resume_expenses --by Seb
python3 scripts/growthos/policy.py grant <action> <resource_id> <resource_hash> <destination> --by Seb --quote "..."
"""
import datetime as dt, json, os, re, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store, ROOT, now  # noqa: E402

CFG = os.path.join(ROOT, "config", "growthos")


def load(name, cfg_dir=None):
    return json.load(open(os.path.join(cfg_dir or CFG, name)))


class Decision(dict):
    @property
    def allowed(self):
        return self["allowed"]


def _dec(allowed, reason, **kw):
    return Decision(allowed=allowed, reason=reason, **kw)


# ---------- approvals ----------
def grant(store, action, resource_id, resource_hash, destination, by, channel, quote, hours=None, one_time=True, cfg_dir=None):
    P = load("policy.json", cfg_dir)
    if by not in P["owners"]:
        raise PermissionError(f"{by} is not an owner")
    if not quote.strip():
        raise PermissionError("approval needs the owner's own words")
    if action not in P["actions"] or "*" in (action + resource_id + destination):
        raise PermissionError("approvals are scoped: no wildcards, known actions only")
    hours = min(hours or P["approval_max_hours"], P["approval_max_hours"])
    exp = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=hours)).replace(microsecond=0).isoformat()
    aid = "apr_" + uuid.uuid4().hex[:10]
    store.append("approval.granted", {"approval_id": aid, "action": action, "resource_id": resource_id, "resource_hash": resource_hash,
                                      "destination": destination, "expires_at": exp, "one_time": one_time, "channel": channel, "quote": quote[:200]},
                 "owner", aid, by)
    return aid


def revoke(store, approval_id, reason, by):
    store.append("approval.revoked", {"approval_id": approval_id, "reason": reason}, "owner", f"revoke:{approval_id}", by)


def approvals(store):
    g = {e["payload"]["approval_id"]: dict(e["payload"], granted_by=e["actor"], used_at=None, revoked=None) for e in store.of("approval.granted")}
    for e in store.of("approval.used"):
        if e["payload"]["approval_id"] in g:
            g[e["payload"]["approval_id"]]["used_at"] = e["occurred_at_utc"]
    for e in store.of("approval.revoked"):
        if e["payload"]["approval_id"] in g:
            g[e["payload"]["approval_id"]]["revoked"] = e["payload"]["reason"]
    return g


def find_grant(store, action, resource_id, resource_hash, destination, at=None):
    at = at or now()
    for a in approvals(store).values():
        if (a["action"], a["resource_id"], a["destination"]) != (action, resource_id, destination):
            continue
        if a["revoked"] or a["expires_at"] < at or (a["one_time"] and a["used_at"]):
            continue
        if a["resource_hash"] != resource_hash:
            continue  # content changed after approval -> no longer covered
        return a
    return None


# ---------- decisions ----------
def authorize(store, worker, action, resource_id=None, resource_hash=None, destination=None, cfg_dir=None,
              viral_check=None, consent_ok=None, budget=None, at=None):
    """Deterministic decision for one proposed action. Never performs the action."""
    P, F = load("policy.json", cfg_dir), load("flags.json", cfg_dir)
    A = P["actions"].get(action)
    if A is None:
        return _dec(False, f"unknown action {action}")
    if action not in P["workers"].get(worker, []):
        return _dec(False, f"worker {worker} is not allowed to {action}")
    flag = A.get("flag")
    if flag and not F.get(flag, False):
        return _dec(False, f"kill switch {flag} is off")
    if A.get("costed") and budget is not None:
        b = budget()
        if b.get("hard_cap_hit"):
            return _dec(False, "AI hard cap reached: optional work paused")
        if b.get("soft_cap_hit") and action == "llm.optional_call":
            return _dec(False, "AI soft cap reached: noncritical work throttled")
    if A.get("needs_consent") and consent_ok is not None and not consent_ok():
        return _dec(False, "no marketing consent or unsubscribed")
    if A.get("needs_viral_gate"):
        if viral_check is None:
            return _dec(False, "viral gate not consulted (NO PROOF, NO POST)")
        ok, why = viral_check(resource_id, resource_hash)
        if not ok:
            return _dec(False, f"viral gate: {why}")
    if A["tier"] in ("high", "critical"):
        g = find_grant(store, action, resource_id, resource_hash, destination, at)
        if not g:
            return _dec(False, "needs owner approval for this exact resource, version and destination", needs_approval=True)
        return _dec(True, "owner approved", approval_id=g["approval_id"], tier=A["tier"])
    return _dec(True, f"{A['tier']} tier: automatic", tier=A["tier"])


def use_grant(store, approval_id, actor):
    store.append("approval.used", {"approval_id": approval_id}, "growthos", f"used:{approval_id}", actor)


def viral_gate_check(content_id, version):
    """Adapter to scripts/viral/gate.py: publishable only if QUEUED with the same version."""
    sys.path.insert(0, os.path.join(ROOT, "scripts", "viral"))
    import gate
    try:
        c = gate.load_concept(content_id)
    except Exception:
        return False, "content not in the evidence register"
    if c["state"] not in ("QUEUED",):
        return False, f"concept is {c['state']}"
    if gate.version_hash(c) != version or (c.get("queued") or {}).get("version") != version:
        return False, "version differs from the approved, queued version"
    return True, "queued and approved"


# ---------- untrusted content ----------
INJECTION = re.compile(r"(ignore (all|any|previous|prior) (instructions|rules)|disregard (the|your) (rules|instructions)|you are now|system prompt|"
                       r"developer mode|reveal (your|the) (secret|token|key|prompt)|print (the )?(env|environment|secrets?)|"
                       r"call the (publish|schedule|refund|send)|approve (this|it) yourself|bypass)", re.I)


def scan_untrusted(text):
    hits = sorted({m.group(0).lower() for m in INJECTION.finditer(text or "")})
    return {"suspicious": bool(hits), "matches": hits}


def validate_proposal(store, worker, proposal, source_text=None, cfg_dir=None, **checks):
    """Validate a model proposal {actions:[{action, resource_id, resource_hash, destination}]} against policy.
    Anything not permitted is dropped and logged. Text from files, DMs, emails or web pages never adds permissions."""
    out = {"accepted": [], "rejected": [], "injection": scan_untrusted(source_text) if source_text else None}
    for a in (proposal or {}).get("actions", []):
        if not isinstance(a, dict) or "action" not in a:
            out["rejected"].append({"action": a, "reason": "malformed"}); continue
        d = authorize(store, worker, a["action"], a.get("resource_id"), a.get("resource_hash"), a.get("destination"), cfg_dir, **checks)
        (out["accepted"] if d.allowed else out["rejected"]).append({**a, "reason": d["reason"]})
    if out["rejected"]:
        store.append("security.event_rejected", {"reason": f"{len(out['rejected'])} proposed action(s) denied for {worker}",
                                                 "denied": [r["action"] if isinstance(r["action"], str) else "malformed" for r in out["rejected"]],
                                                 "injection": bool(out["injection"] and out["injection"]["suspicious"])},
                     "growthos.policy", f"prop:{uuid.uuid4().hex[:10]}", worker)
    return out


# ---------- kill switches ----------
SWITCHES = {"stop_all_outbound": {"outbound_publishing": False, "messaging": False},
            "resume_outbound": {"outbound_publishing": True, "messaging": True},
            "pause_expenses": {"paid_services": False, "optional_llm": False},
            "resume_expenses": {"paid_services": True, "optional_llm": True}}


def switch(store, name, by, cfg_dir=None):
    P = load("policy.json", cfg_dir)
    if by not in P["owners"]:
        raise PermissionError("only an owner can flip kill switches")
    path = os.path.join(cfg_dir or CFG, "flags.json"); F = json.load(open(path))
    for k, v in SWITCHES[name].items():
        F[k] = v
        store.append("flag.changed", {"flag": k, "value": v, "switch": name}, "owner", f"flag:{k}:{uuid.uuid4().hex[:8]}", by)
    json.dump(F, open(path, "w"), indent=1)
    return F


def _arg(flag, d=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else d


if __name__ == "__main__":
    st = Store(); cmd = sys.argv[1]
    if cmd == "check":
        w, a = sys.argv[2], sys.argv[3]; rest = sys.argv[4:7] + [None] * (3 - len(sys.argv[4:7]))
        print(json.dumps(authorize(st, w, a, *rest, viral_check=viral_gate_check), indent=1))
    elif cmd == "switch":
        print(json.dumps(switch(st, sys.argv[2], _arg("--by")), indent=1))
    elif cmd == "grant":
        print(grant(st, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], _arg("--by"), _arg("--channel", "chat"), _arg("--quote", "")))
