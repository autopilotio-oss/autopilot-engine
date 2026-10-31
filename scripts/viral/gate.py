"""NO PROOF, NO POST: the Viral Evidence Gate (AUTOPILOT.OI Viral Validation V2).

Every video concept lives in viral/concepts/<content_id>.json and moves through one state machine:
  IDEA -> EVIDENCE_PENDING -> VERIFIED -> SCRIPTED -> DEMO_TESTED -> QUALITY_PASSED -> OWNER_APPROVED -> QUEUED
       -> PUBLISHED | TRIAL -> ANALYZED          (any failure -> HOLD with a reason code)
Reference videos live in viral/evidence.jsonl. Every state change, rejection, approval and override request is
appended to viral/audit.jsonl as a hash chained event (editing an old line breaks the chain and `verify-audit` fails).

Only `advance` moves a concept forward, and every step re-runs its checks. Nothing here can mark a concept QUEUED
without an owner approval bound to the exact version hash of the concept, and any edit after approval (script,
references, CTA, claims) changes the hash and sends the concept back to HOLD (APPROVAL_STALE).

CLI
  python3 scripts/viral/gate.py status [content_id]
  python3 scripts/viral/gate.py advance <content_id> [--actor NAME]      # runs the checks for the next state
  python3 scripts/viral/gate.py approve <content_id> --by "Seb" --channel chat --quote "<owner's exact words>"
  python3 scripts/viral/gate.py reject <content_id> --by "Seb" --reason "..."
  python3 scripts/viral/gate.py score <content_id>                        # hard gates + 100 point score
  python3 scripts/viral/gate.py metrics <content_id> --window 24h --data '{"views":..}' --source metricool
  python3 scripts/viral/gate.py check-queue                               # CI: no gated queue item without QUEUED concept
  python3 scripts/viral/gate.py verify-audit
"""
import datetime as dt, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VDIR = os.path.join(ROOT, "viral")
POLICY = json.load(open(os.path.join(VDIR, "policy.json")))
STATES = ["IDEA", "EVIDENCE_PENDING", "VERIFIED", "SCRIPTED", "DEMO_TESTED", "QUALITY_PASSED", "OWNER_APPROVED", "QUEUED",
          "PUBLISHED", "TRIAL", "ANALYZED", "HOLD", "REJECTED"]
NEXT = {"IDEA": "EVIDENCE_PENDING", "EVIDENCE_PENDING": "VERIFIED", "VERIFIED": "SCRIPTED", "SCRIPTED": "DEMO_TESTED",
        "DEMO_TESTED": "QUALITY_PASSED", "QUALITY_PASSED": "OWNER_APPROVED", "OWNER_APPROVED": "QUEUED"}
UNVERIFIED_PROVENANCE = {None, "", "search_snippet_only", "estimated", "ai_estimate", "not verifiable", "creator_claim", "screenshot_no_url"}
URL_RX = {
    "youtube": re.compile(r"^https://(www\.)?youtube\.com/(shorts/[\w-]{6,}|watch\?v=[\w-]{6,})"),
    "tiktok": re.compile(r"^https://(www\.)?tiktok\.com/@[\w.]+/video/\d{8,}"),
    "instagram": re.compile(r"^https://(www\.)?instagram\.com/(reel|reels|p)/[\w-]{5,}"),
}


class GateError(Exception):
    pass


# ---------- storage ----------
def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def _paths(root=None):
    r = root or VDIR
    return {"concepts": os.path.join(r, "concepts"), "evidence": os.path.join(r, "evidence.jsonl"),
            "audit": os.path.join(r, "audit.jsonl"), "metrics": os.path.join(r, "metrics.jsonl")}


def load_evidence(root=None):
    p = _paths(root)["evidence"]
    return {r["ref_id"]: r for r in (json.loads(l) for l in open(p) if l.strip())} if os.path.exists(p) else {}


def load_concept(cid, root=None):
    p = os.path.join(_paths(root)["concepts"], f"{cid}.json")
    if not os.path.exists(p):
        raise GateError(f"unknown content_id {cid}")
    return json.load(open(p))


def save_concept(c, root=None):
    d = _paths(root)["concepts"]; os.makedirs(d, exist_ok=True)
    json.dump(c, open(os.path.join(d, f"{c['content_id']}.json"), "w"), indent=1, ensure_ascii=False)


def all_concepts(root=None):
    d = _paths(root)["concepts"]
    return [json.load(open(os.path.join(d, f))) for f in sorted(os.listdir(d)) if f.endswith(".json")] if os.path.isdir(d) else []


def audit(event, cid, actor, root=None, **detail):
    """Append a hash chained audit event. Returns the event."""
    p = _paths(root)["audit"]; prev = "GENESIS"
    if os.path.exists(p):
        lines = [l for l in open(p) if l.strip()]
        if lines:
            prev = json.loads(lines[-1])["hash"]
    e = {"ts": _now(), "event": event, "content_id": cid, "actor": actor, "detail": detail, "prev": prev}
    e["hash"] = hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    with open(p, "a") as f:
        f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return e


def verify_audit(root=None):
    p = _paths(root)["audit"]; prev = "GENESIS"; n = 0
    for l in (open(p) if os.path.exists(p) else []):
        if not l.strip():
            continue
        e = json.loads(l); h = e.pop("hash")
        if e["prev"] != prev or hashlib.sha256(json.dumps(e, sort_keys=True, ensure_ascii=False).encode()).hexdigest() != h:
            return False, n
        prev = h; n += 1
    return True, n


# ---------- version binding ----------
CONTENT_KEYS = ["content_id", "agent", "offer_id", "platforms", "problem", "audience", "references", "hook", "script",
                "storyboard", "claims", "demo", "cta", "rights", "editorial"]


def version_hash(c):
    body = {k: c.get(k) for k in CONTENT_KEYS}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


# ---------- evidence ----------
def _days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def qualify(ref, today=None):
    """Return (qualified: bool, reasons: list[str], flags: list[str]) for one reference under the default policy."""
    today = today or dt.date.today().isoformat(); P = POLICY["reference"]; why = []; flags = []
    plat = ref.get("platform")
    if not ref.get("url") or plat not in URL_RX or not URL_RX[plat].match(ref["url"]):
        why.append("URL_INVALID")
    if not ref.get("creator"):
        why.append("CREATOR_MISSING")
    if not isinstance(ref.get("views"), int) or ref.get("views_provenance") in UNVERIFIED_PROVENANCE:
        why.append("VIEWS_UNVERIFIED")
    elif ref["views"] < P["min_views"]:
        why.append("VIEWS_BELOW_FLOOR")
    if ref.get("is_paid_ad"):
        why.append("PAID_AD_NOT_ORGANIC_PROOF")
    pub = ref.get("published")
    if not pub:
        why.append("DATE_MISSING")
    else:
        age = _days(pub, today)
        if age > P["max_age_days"]:
            why.append("TOO_OLD")
        elif age > P["fresh_days"]:
            flags.append("FRESHNESS_FLAG")
    cap = ref.get("captured")
    if not cap or _days(cap, today) > P["evidence_valid_days"]:
        why.append("EVIDENCE_EXPIRED")
    med, n = ref.get("creator_median"), len(ref.get("recent_views_sample") or [])
    if ref.get("top_decile_documented"):
        pass
    elif not isinstance(med, int) or med <= 0 or n < P["median_min_sample"]:
        why.append("OUTPERFORMANCE_NOT_MEASURABLE")
    elif isinstance(ref.get("views"), int) and ref["views"] / med < P["min_outperformance"]:
        why.append("WEAK_RELATIVE_PERFORMANCE")
    if isinstance(med, int) and n >= P["median_min_sample"]:
        s = sorted(ref["recent_views_sample"]); m = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) // 2
        if abs(m - med) > max(1, med * 0.01):
            why.append("MEDIAN_DOES_NOT_MATCH_SAMPLE")
    return (not why), why, flags


def evidence_check(c, ev, today=None):
    refs = [ev.get(r) for r in c.get("references", [])]
    missing = [r for r, x in zip(c.get("references", []), refs) if x is None]
    q = []; detail = {}
    for x in refs:
        if x is None:
            continue
        ok, why, flags = qualify(x, today)
        detail[x["ref_id"]] = {"qualified": ok, "reasons": why, "flags": flags}
        if ok:
            q.append(x)
    creators = {x["creator"].lower() for x in q}
    fails = []
    if missing:
        fails.append("REFERENCE_NOT_IN_REGISTER")
    if len(q) < POLICY["reference"]["min_refs"]:
        fails.append("FEWER_THAN_3_QUALIFIED_REFERENCES")
    if len(creators) < POLICY["reference"]["min_creators"]:
        fails.append("FEWER_THAN_2_CREATORS")
    return fails, detail, q


# ---------- claims, rights, CTA, demo ----------
def _copy_text(c):
    s = c.get("script") or {}
    parts = [c.get("hook", "")] + [b.get("vo", "") + " " + b.get("on_screen", "") for b in s.get("beats", [])] + [s.get("caption", "")]
    return " ".join(parts)


def claims_check(c):
    fails = []; text = _copy_text(c).lower()
    for w in POLICY["banned_phrases"]:
        if w in text:
            fails.append(f"BANNED_PHRASE:{w}")
    if re.search(r"\s[-–—]\s|—|–", _copy_text(c)):
        fails.append("DASH_IN_COPY")
    for cl in c.get("claims", []):
        if not cl.get("source_url", "").startswith("https://"):
            fails.append(f"UNSOURCED_CLAIM:{cl.get('claim', '')[:40]}")
    if re.search(r"\$\s?\d|\d+\s?%|\d{2,}", text) and not c.get("claims"):
        fails.append("NUMBERS_WITHOUT_CLAIM_SOURCES")
    return fails


def rights_check(c):
    r = c.get("rights") or {}; fails = []
    if r.get("copied_footage") is not False or r.get("copied_script") is not False:
        fails.append("COPIED_OR_UNDECLARED_CONTENT")
    for k in ("audio", "footage", "voice"):
        if r.get(k) not in ("original", "licensed"):
            fails.append(f"RIGHTS_UNCLEAR:{k}")
    if r.get("platform_issues"):
        fails.append("DISALLOWED_PLATFORM_BEHAVIOR")
    return fails


def cta_check(c, today=None):
    cta = c.get("cta") or {}; fails = []; today = today or dt.date.today().isoformat()
    url = cta.get("url", "")
    if not url.startswith("https://autopilotoi.app/"):
        fails.append("CTA_NOT_OWN_DOMAIN")
    else:
        path = url.split("autopilotoi.app/", 1)[1].split("?")[0].split("#")[0]
        f = os.path.join(ROOT, "docs", path, "index.html") if not path.endswith(".html") else os.path.join(ROOT, "docs", path)
        if not os.path.exists(f):
            fails.append("CTA_PAGE_MISSING")
        elif "noindex" in open(f).read()[:4000] and not cta.get("allow_noindex"):
            fails.append("CTA_PAGE_IS_DRAFT")
    if "utm_content=" + c["content_id"] not in url:
        fails.append("CTA_NOT_TRACKED")
    if not cta.get("checked") or _days(cta["checked"], today) > 7 or cta.get("status") != 200:
        fails.append("CTA_NOT_QA_TESTED")
    prod = cta.get("product_permalink")
    if prod:
        live = json.load(open(os.path.join(ROOT, "docs", "live.json"))).get("live", [])
        if prod not in live:
            fails.append("PRODUCT_NOT_LIVE")
    return fails


def demo_check(c):
    d = c.get("demo") or {}; fails = []
    if not d.get("tested"):
        fails.append("DEMO_NOT_TESTED")
    art = d.get("artifact")
    if not art or not os.path.exists(os.path.join(ROOT, art)):
        fails.append("DEMO_ARTIFACT_MISSING")
    if d.get("synthetic") and not d.get("labeled"):
        fails.append("SYNTHETIC_DEMO_NOT_LABELED")
    return fails


# ---------- scoring ----------
def score(c, ev, today=None):
    """Hard gates first, then the 100 point editorial score. Evidence dimensions are computed, never typed in."""
    ef, detail, q = evidence_check(c, ev, today)
    hard = ef + claims_check(c) + rights_check(c) + cta_check(c, today) + demo_check(c)
    pts = {}
    pts["reference_quality"] = min(25, round(25 * len(q) / 3)) if q else 0
    mults = [x["views"] / x["creator_median"] for x in q if isinstance(x.get("creator_median"), int) and x["creator_median"] > 0]
    deciles = [x for x in q if x.get("top_decile_documented")]
    strong = len(mults) + len(deciles)
    creators = len({x["creator"].lower() for x in q})
    pts["outperformance"] = 0 if strong < 3 else (20 if creators >= 3 else 16)
    ed = c.get("editorial") or {}
    caps = {"opening_hook": 15, "audience_relevance": 15, "proof_on_screen": 10, "business_fit_cta": 10, "visual_craft": 5}
    for k, mx in caps.items():
        v = ed.get(k)
        pts[k] = max(0, min(mx, int(v))) if isinstance(v, (int, float)) else 0
    if demo_check(c):
        pts["proof_on_screen"] = 0
    if cta_check(c, today):
        pts["business_fit_cta"] = 0
    total = sum(pts.values())
    decision = "HOLD" if hard else ("PASS" if total >= POLICY["pass_score"] else ("REVISE" if total >= POLICY["revise_score"] else "REJECT"))
    return {"hard_fails": hard, "points": pts, "total": total, "decision": decision, "evidence": detail,
            "reviewer": ed.get("reviewer"), "version": version_hash(c)}


# ---------- state machine ----------
def _hold(c, reason, actor, root=None, **d):
    old = c["state"]; c["state"] = "HOLD"; c["hold_reason"] = reason
    save_concept(c, root); audit("HOLD", c["content_id"], actor, root, frm=old, reason=reason, **d)
    return c


def revalidate(c, actor="system", root=None, today=None):
    """Approval is void if the content changed or the evidence expired since approval."""
    if c["state"] in ("OWNER_APPROVED", "QUEUED"):
        a = (c.get("approval") or {})
        if a.get("version") != version_hash(c):
            return _hold(c, "APPROVAL_STALE_CONTENT_CHANGED", actor, root)
        ef, _, _ = evidence_check(c, load_evidence(root), today)
        if ef:
            return _hold(c, "APPROVAL_STALE_EVIDENCE", actor, root, fails=ef)
    return c


def advance(cid, actor="system", root=None, today=None):
    c = load_concept(cid, root); ev = load_evidence(root)
    before = c["state"]; c = revalidate(c, actor, root, today)
    if c["state"] == "HOLD" and before != "HOLD":
        return c  # approval voided this run; the next advance restarts from evidence
    cur = c["state"]
    if cur == "HOLD":
        # a held concept restarts the checks from evidence, never jumps back to where it was
        cur = c["state"] = "EVIDENCE_PENDING"; c.pop("hold_reason", None)
    if cur not in NEXT:
        raise GateError(f"{cid}: no forward move from {cur}")
    tgt = NEXT[cur]
    if tgt == "VERIFIED":
        f, detail, _ = evidence_check(c, ev, today)
        if f:
            return _hold(c, "EVIDENCE", actor, root, fails=f, refs=detail)
    elif tgt == "SCRIPTED":
        if not (c.get("script") or {}).get("beats") or not c.get("hook"):
            return _hold(c, "NO_SCRIPT", actor, root)
        f = claims_check(c) + rights_check(c)
        if f:
            return _hold(c, "CLAIMS_OR_RIGHTS", actor, root, fails=f)
    elif tgt == "DEMO_TESTED":
        f = demo_check(c)
        if f:
            return _hold(c, "DEMO", actor, root, fails=f)
    elif tgt == "QUALITY_PASSED":
        s = score(c, ev, today); c["last_score"] = s
        if s["decision"] != "PASS":
            return _hold(c, f"SCORE_{s['decision']}", actor, root, total=s["total"], hard=s["hard_fails"])
    elif tgt == "OWNER_APPROVED":
        raise GateError("owner approval is recorded with `approve`, never with `advance`")
    elif tgt == "QUEUED":
        a = c.get("approval") or {}
        if not a or a.get("version") != version_hash(c):
            audit("BYPASS_BLOCKED", cid, actor, root, wanted="QUEUED", why="no owner approval for this version")
            raise GateError("blocked: no owner approval for this exact version")
        s = score(c, ev, today)
        if s["decision"] != "PASS":
            return _hold(c, "SCORE_CHANGED_AFTER_APPROVAL", actor, root, total=s["total"], hard=s["hard_fails"])
        c["queued"] = {"at": _now(), "version": version_hash(c)}
    c["state"] = tgt; c["updated"] = _now(); save_concept(c, root)
    audit("STATE", cid, actor, root, frm=cur, to=tgt, version=version_hash(c))
    return c


def approve(cid, by, channel, quote, root=None, today=None):
    c = load_concept(cid, root)
    if by not in POLICY["owners"]:
        audit("BYPASS_BLOCKED", cid, by, root, wanted="OWNER_APPROVED", why="approver is not an owner")
        raise GateError(f"blocked: {by} is not an owner")
    if channel not in POLICY["approval_channels"] or not quote.strip():
        audit("BYPASS_BLOCKED", cid, by, root, wanted="OWNER_APPROVED", why="no owner channel/quote")
        raise GateError("blocked: approval needs the owner's own words from an owner channel")
    if c["state"] != "QUALITY_PASSED":
        audit("BYPASS_BLOCKED", cid, by, root, wanted="OWNER_APPROVED", why=f"state is {c['state']}")
        raise GateError(f"blocked: {cid} is {c['state']}, must be QUALITY_PASSED")
    s = score(c, load_evidence(root), today)
    if s["decision"] != "PASS":
        return _hold(c, "SCORE_AT_APPROVAL", by, root, total=s["total"])
    c["approval"] = {"by": by, "channel": channel, "quote": quote, "at": _now(), "version": version_hash(c), "score": s["total"]}
    c["state"] = "OWNER_APPROVED"; save_concept(c, root)
    audit("OWNER_APPROVED", cid, by, root, channel=channel, quote=quote, version=version_hash(c), score=s["total"])
    return c


def reject(cid, by, reason, root=None):
    c = load_concept(cid, root); old = c["state"]; c["state"] = "REJECTED"; c["rejected"] = {"by": by, "reason": reason, "at": _now()}
    save_concept(c, root); audit("REJECTED", cid, by, root, frm=old, reason=reason)
    return c


def mark_published(cid, url, platform, actor, root=None, trial=False):
    c = load_concept(cid, root)
    if c["state"] != "QUEUED" or (c.get("queued") or {}).get("version") != version_hash(c):
        audit("BYPASS_BLOCKED", cid, actor, root, wanted="PUBLISHED", why=f"state {c['state']}")
        raise GateError("blocked: only QUEUED concepts with an unchanged approved version can be published")
    c.setdefault("published", []).append({"url": url, "platform": platform, "at": _now()})
    old = c["state"]; c["state"] = "TRIAL" if trial else "PUBLISHED"; save_concept(c, root)
    audit("STATE", cid, actor, root, frm=old, to=c["state"], url=url)
    return c


def add_metrics(cid, window, data, source, root=None, ledger_events=None):
    """Attach 24h/72h/7d metrics to the right content ID. Sales are only counted from orders whose utm_content
    equals this content ID; anything else stays 'unknown', never guessed."""
    c = load_concept(cid, root)
    if c["state"] not in ("PUBLISHED", "TRIAL", "ANALYZED"):
        raise GateError(f"{cid} is not published")
    if window not in ("24h", "72h", "7d"):
        raise GateError("window must be 24h, 72h or 7d")
    orders = [e for e in (ledger_events or []) if e.get("utm_content") == cid and e.get("type") == "sale"]
    rec = {"content_id": cid, "window": window, "source": source, "at": _now(), "data": data,
           "attributed_orders": len(orders), "attributed_gross_cents": sum(e.get("gross_cents", 0) for e in orders),
           "attribution": "utm_content match" if orders else "none matched (unknown, not zero)"}
    with open(_paths(root)["metrics"], "a") as f:
        f.write(json.dumps(rec) + "\n")
    audit("METRICS", cid, source, root, window=window)
    if window == "7d":
        c["state"] = "ANALYZED"; save_concept(c, root)
    return rec


def check_queue(root=None, qdir=None):
    """Every queue item dated on or after the policy start must carry a content_id whose concept is QUEUED
    (or later) with an unchanged approved version. Returns a list of problems."""
    probs = []; start = POLICY["enforce_from"]
    qdir = qdir or os.path.join(ROOT, "queue")
    for f in sorted(os.listdir(qdir)) if os.path.isdir(qdir) else []:
        if not f.endswith(".json"):
            continue
        for p in json.load(open(os.path.join(qdir, f))):
            if str(p.get("at", ""))[:10] < start or p.get("format") in POLICY["exempt_formats"]:
                continue
            cid = p.get("content_id")
            if not cid:
                probs.append(f"{f}:{p.get('id')}: no content_id (NO PROOF, NO POST)"); continue
            try:
                c = load_concept(cid, root)
            except GateError:
                probs.append(f"{f}:{p.get('id')}: {cid} not in register"); continue
            if c["state"] not in ("QUEUED", "PUBLISHED", "TRIAL", "ANALYZED") or (c.get("queued") or {}).get("version") != version_hash(c):
                probs.append(f"{f}:{p.get('id')}: {cid} is {c['state']}, not approved+queued")
    return probs


def status(cid=None, root=None):
    rows = all_concepts(root) if not cid else [load_concept(cid, root)]
    return [{"content_id": c["content_id"], "agent": c.get("agent"), "state": c["state"], "hold_reason": c.get("hold_reason"),
             "score": (c.get("last_score") or {}).get("total"), "version": version_hash(c)} for c in rows]


def _arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    try:
        if cmd == "status":
            print(json.dumps(status(sys.argv[2] if len(sys.argv) > 2 else None), indent=1))
        elif cmd == "advance":
            print(json.dumps(status(advance(sys.argv[2], _arg("--actor", "cli"))["content_id"]), indent=1))
        elif cmd == "approve":
            approve(sys.argv[2], _arg("--by"), _arg("--channel"), _arg("--quote", "")); print("approved", sys.argv[2])
        elif cmd == "reject":
            reject(sys.argv[2], _arg("--by"), _arg("--reason", "")); print("rejected", sys.argv[2])
        elif cmd == "score":
            print(json.dumps(score(load_concept(sys.argv[2]), load_evidence()), indent=1))
        elif cmd == "metrics":
            print(json.dumps(add_metrics(sys.argv[2], _arg("--window"), json.loads(_arg("--data", "{}")), _arg("--source", "manual")), indent=1))
        elif cmd == "check-queue":
            p = check_queue(); print("\n".join(p) or "queue OK: every gated item is approved and queued"); sys.exit(1 if p else 0)
        elif cmd == "verify-audit":
            ok, n = verify_audit(); print(("audit chain OK" if ok else "AUDIT CHAIN BROKEN at event"), n); sys.exit(0 if ok else 1)
        elif cmd == "evidence":
            for r in load_evidence().values():
                ok, why, fl = qualify(r); print(("PASS " if ok else "FAIL ") + r["ref_id"], r.get("views"), r.get("creator"), ",".join(why + fl))
    except GateError as e:
        print("BLOCKED:", e); sys.exit(2)
