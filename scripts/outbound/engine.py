"""Outbound Intelligence V3: draft only B2B prospect pipeline for the Front Desk Kit ($39) and the
Front Desk Setup pilot ($299). Adapted from the V3 starter (outbound_engine.py) and wired into what already exists:

  config/offers.json      prices, claims and the $299 pilot definition (single source of truth)
  config/outbound.json    sender identity for CAN-SPAM (postal address must be filled before any email)
  sales/outreach.csv      PUBLIC pipeline log: one row per stage change, pseudonymous lead_ref only
  sales/suppression.csv   PUBLIC opt-out list: sha256 of the domain, never the name or email
  state/ledger/           Gumroad ledger: the only source for PAID

Private research records (business names, URLs, facts, drafts) are NOT stored in this public repo. They live in
the owner's private Claude Project (claude/outbound/leads.csv) and are passed in by path.

THIS MODULE HAS NO SEND FUNCTION. Nothing here opens a network connection. Outreach is done by a person, after an
approval row exists for that lead, through a channel the owner has authorised.

python3 scripts/outbound/engine.py score <leads.csv> <scored.csv>     score + flags + drafts (private output)
python3 scripts/outbound/engine.py approve <lead_ref> "<by>" "<quote>"  record a human approval for one draft
python3 scripts/outbound/engine.py stage <lead_ref> <STAGE> "<note>"   record a stage change (e.g. CONTACTED)
python3 scripts/outbound/engine.py optout <website>                   suppress a business forever
python3 scripts/outbound/engine.py reconcile                          mark PAID only from verified ledger orders
python3 scripts/outbound/engine.py summary                            pipeline counts (used by the daily report)
"""
from __future__ import annotations
import csv, datetime, hashlib, json, os, re, sys
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTREACH = os.path.join(ROOT, "sales", "outreach.csv")
SUPPRESSION = os.path.join(ROOT, "sales", "suppression.csv")
LEDGER = os.path.join(ROOT, "state", "ledger", "events.jsonl")

LEAD_FIELDS = ["business_name", "website", "location", "niche", "source_url", "public_contact_channel",
               "contact_permission", "need_signal", "need_evidence_url", "verified_fact", "fact_source_url",
               "business_fit", "checked_at", "offer", "notes"]
OUT_FIELDS = ["lead_ref"] + LEAD_FIELDS + ["score", "review_flag", "recommended_action", "claim_issues", "draft"]
OUTREACH_FIELDS = ["date", "contact_ref", "trade", "channel", "campaign", "status", "score", "offer",
                   "attribution_id", "objection", "approved_by", "note"]

STAGES = ["RESEARCHED", "QUALIFIED", "DRAFTED", "APPROVED", "CONTACTED", "INTERESTED", "CALL_BOOKED",
          "OFFER_SENT", "PAID", "ACTIVATED"]
CLOSED = ["NO_RESPONSE", "NOT_FIT", "OPTED_OUT", "CLOSED_LOST"]
# Contact may only happen after APPROVED; PAID only through reconcile(); OPTED_OUT is final.
NEEDS_APPROVAL_BEFORE = {"CONTACTED", "INTERESTED", "CALL_BOOKED", "OFFER_SENT"}

NICHES = {"mobile detailing", "auto detailing", "car detailing", "ceramic coating / detailing"}
PERMISSION_POINTS = {"owner_relationship": 20, "opt_in": 20, "business_contact_page": 10}
CAMPAIGN = "v3_pilot"


# ---------- helpers ----------
def yes(s) -> bool:
    return str(s or "").strip().lower() in {"true", "yes", "y", "1"}


def has_url(s) -> bool:
    try:
        u = urlsplit(str(s or "").strip())
        return u.scheme in {"http", "https"} and bool(u.netloc)
    except ValueError:
        return False


def domain(site: str) -> str:
    site = str(site or "").strip()
    if not site:
        return ""
    try:
        return urlsplit(site if "://" in site else f"https://{site}").netloc.lower().removeprefix("www.")
    except ValueError:
        return site.lower()


def lead_ref(site: str) -> str:
    """Stable, pseudonymous company id. Same website always gives the same ref (idempotency key)."""
    d = domain(site)
    return "det-" + hashlib.sha256(d.encode()).hexdigest()[:10] if d else ""


def recent(s, today: datetime.date, days=30) -> bool:
    try:
        return 0 <= (today - datetime.date.fromisoformat(str(s).strip())).days <= days
    except ValueError:
        return False


def offers():
    return json.load(open(os.path.join(ROOT, "config", "offers.json")))


def sender():
    try:
        return json.load(open(os.path.join(ROOT, "config", "outbound.json")))
    except FileNotFoundError:
        return {}


# ---------- suppression ----------
def suppressed_hashes(path=None) -> set:
    path = path or SUPPRESSION
    try:
        return {r["domain_sha256"] for r in csv.DictReader(open(path))}
    except FileNotFoundError:
        return set()


def is_suppressed(site, path=None) -> bool:
    path = path or SUPPRESSION
    d = domain(site)
    return bool(d) and hashlib.sha256(d.encode()).hexdigest() in suppressed_hashes(path)


def opt_out(site, path=None, today=None):
    path = path or SUPPRESSION
    d = domain(site)
    if not d:
        raise ValueError("website needed to suppress")
    h = hashlib.sha256(d.encode()).hexdigest()
    if h in suppressed_hashes(path):
        return False
    new = not os.path.exists(path)
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["domain_sha256", "date", "reason"])
        if new:
            w.writeheader()
        w.writerow({"domain_sha256": h, "date": (today or datetime.date.today()).isoformat(), "reason": "opt_out"})
    record(lead_ref(site), "OPTED_OUT", note="opt out recorded; never contact again", today=today)
    return True


# ---------- scoring (V3 weights; missing evidence scores zero, nothing is guessed) ----------
def score(row: dict, today: datetime.date | None = None) -> tuple[int, str, str]:
    today = today or datetime.date.today()
    if is_suppressed(row.get("website")):
        return 0, "SUPPRESSED", "Never contact; opted out"
    if not str(row.get("business_name", "")).strip() or not has_url(row.get("source_url")) or not domain(row.get("website")):
        return 0, "INCOMPLETE", "Verify the company, website and source before anything else"
    pts = 0
    if str(row.get("niche", "")).strip().lower() in NICHES:
        pts += 30
    if str(row.get("need_signal", "")).strip() and has_url(row.get("need_evidence_url")):
        pts += 25
    pts += PERMISSION_POINTS.get(str(row.get("contact_permission", "")).strip().lower(), 0)
    if str(row.get("business_fit", "")).strip().lower() == "verified":
        pts += 15
    if recent(row.get("checked_at", ""), today):
        pts += 10
    if not str(row.get("verified_fact", "")).strip() or not has_url(row.get("fact_source_url")):
        return pts, "NEEDS_FACT_CHECK", "Find one specific verified fact with its URL before drafting"
    if pts < 55:
        return pts, "LOW_FIT", "Hold; not enough verified fit or no reachable channel"
    if str(row.get("contact_permission", "")).strip().lower() not in PERMISSION_POINTS:
        return pts, "NO_AUTHORIZED_CHANNEL", "Good fit but no email or contact form: needs a warm intro (e.g. a Pro Labs contact), never cold texts or DMs"
    return pts, "NEEDS_APPROVAL", "Seb reviews the draft; nothing is sent from here"


# ---------- drafts and claim check ----------
def demo_link(ref):
    return (f"https://autopilotoi.app/front-desk/demo/?utm_source=outbound&utm_medium=email"
            f"&utm_campaign={CAMPAIGN}&utm_content={ref}")


def draft(row: dict, ref: str, flag: str) -> str:
    if flag in {"SUPPRESSED", "INCOMPLETE", "NEEDS_FACT_CHECK", "LOW_FIT", "NO_AUTHORIZED_CHANNEL"}:
        return ""
    O = offers()
    kit = [o for o in O["offers"] if o["id"] == "front_desk_kit"][0]
    pilot = [p for p in O.get("pilots", []) if p["id"] == "front_desk_setup"][0]
    S = sender()
    name = str(row["business_name"]).strip()
    fact = str(row["verified_fact"]).strip().rstrip(".")
    addr = S.get("postal_address") or "[POSTAL ADDRESS REQUIRED BEFORE SENDING]"
    who = S.get("sender_name") or "[SENDER NAME]"
    return (
        f"Subject: Customer replies and quotes for {name}\n\n"
        f"Hi,\n\n"
        f"I saw on your site that {fact}. I'm {who.split(',')[0]} from AUTOPILOT.OI. We make a setup for Claude that drafts "
        f"replies to customer messages and quotes from your own prices and rules, so a detailer can answer between cars. "
        f"You read each draft and send it yourself; it never sends anything on its own.\n\n"
        f"Here is a short interactive demo with an example detailing business: {demo_link(ref)}\n\n"
        f"Two ways to use it:\n"
        f"1. The DIY kit, ${kit['price_cents'] // 100} one time; you set it up yourself in about 30 minutes (our estimate).\n"
        f"2. We set it up for you, ${pilot['price_cents'] // 100}, using your real services and prices, tested on a few "
        f"of your real customer messages. We are taking a small number of these as a pilot.\n\n"
        f"If neither is useful, no problem, and I won't follow up more than once.\n\n"
        f"{who.split(',')[0]}\nAUTOPILOT.OI, {addr}\n"
        f"Reply \"no thanks\" and you won't hear from us again.\n"
    )


NEGATION = re.compile(r"\b(not|never|no|isn't|doesn't|won't|without|nothing)\b")


def claim_issues(text: str) -> list[str]:
    """Returns problems that block approval. Empty list = passes the automatic check (a human still reviews)."""
    if not text:
        return []
    O = offers(); issues = []
    low = text.lower()
    for sent in re.split(r"(?<=[.!?\n])\s+", low):
        if NEGATION.search(sent):
            continue
        for bad in O.get("forbidden_claims", []) + ["automatically", "24/7", "guarantee", "more bookings", "more revenue"]:
            if bad.lower() in sent:
                issues.append(f"claim: '{bad}'")
    allowed = {f"${o['price_cents'] // 100}" for o in O["offers"]} | {f"${p['price_cents'] // 100}" for p in O.get("pilots", [])}
    for p in re.findall(r"\$\d+", text):
        if p not in allowed:
            issues.append(f"price not in offers.json: {p}")
    if "[POSTAL ADDRESS REQUIRED" in text or "[SENDER NAME]" in text:
        issues.append("sender identity or postal address missing (CAN-SPAM)")
    if "won't hear from us again" not in low:
        issues.append("no opt out line")
    if "—" in text or "–" in text:
        issues.append("dash in copy (house style)")
    return sorted(set(issues))


# ---------- public pipeline log ----------
def rows(path=None):
    path = path or OUTREACH
    try:
        return list(csv.DictReader(open(path)))
    except FileNotFoundError:
        return []


def current_stage(ref, path=None):
    path = path or OUTREACH
    st = None
    for r in rows(path):
        if r["contact_ref"] == ref:
            st = r["status"]
    return st


def approved(ref, path=None):
    path = path or OUTREACH
    return any(r["contact_ref"] == ref and r["status"] == "APPROVED" and r.get("approved_by") for r in rows(path))


def record(ref, status, score_v="", offer="", note="", approved_by="", objection="", channel="", path=None, today=None):
    path = path or OUTREACH
    if status not in STAGES + CLOSED:
        raise ValueError(f"unknown stage {status}")
    cur = current_stage(ref, path)
    if cur == "OPTED_OUT":
        raise PermissionError("lead opted out: no further stages")
    if status in NEEDS_APPROVAL_BEFORE and not approved(ref, path):
        raise PermissionError(f"{status} needs an APPROVED row first")
    if status == "APPROVED" and not approved_by:
        raise PermissionError("APPROVED needs who approved it")
    if cur == status or any(r["contact_ref"] == ref and r["status"] == status for r in rows(path)):
        return False          # idempotent: a stage already in this lead's history is never logged again
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUTREACH_FIELDS)
        if new:
            w.writeheader()
        w.writerow({"date": (today or datetime.date.today()).isoformat(), "contact_ref": ref, "trade": "detailing",
                    "channel": channel, "campaign": CAMPAIGN, "status": status, "score": score_v, "offer": offer,
                    "attribution_id": ref, "objection": objection, "approved_by": approved_by, "note": note})
    return True


# ---------- batch scoring ----------
def process(src, dst, today=None, path=None):
    path = path or OUTREACH
    today = today or datetime.date.today()
    with open(src, newline="", encoding="utf-8-sig") as f:
        rd = csv.DictReader(f)
        missing = [c for c in ["business_name", "website", "source_url"] if c not in (rd.fieldnames or [])]
        if missing:
            raise ValueError(f"missing columns: {missing}")
        leads = list(rd)
    seen = set(); out = []
    for r in leads:
        ref = lead_ref(r.get("website"))
        if ref and ref in seen:
            raise ValueError(f"duplicate company (same website): {r.get('business_name')}")
        seen.add(ref)
        s, flag, action = score(r, today)
        d = draft(r, ref, flag)
        issues = claim_issues(d)
        out.append({**{k: r.get(k, "") for k in LEAD_FIELDS}, "lead_ref": ref, "score": s, "review_flag": flag,
                    "recommended_action": action, "claim_issues": "; ".join(issues), "draft": d})
        if ref and flag != "SUPPRESSED":
            record(ref, "RESEARCHED", score_v=s, path=path, today=today)
            if flag in {"NEEDS_APPROVAL"}:
                record(ref, "QUALIFIED", score_v=s, offer=r.get("offer") or "front_desk_setup", path=path, today=today)
                record(ref, "DRAFTED", score_v=s, offer=r.get("offer") or "front_desk_setup",
                       note=("claim check: " + "; ".join(issues)) if issues else "claim check passed", path=path, today=today)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUT_FIELDS); w.writeheader(); w.writerows(out)
    return out


# ---------- payments: PAID only from the verified Gumroad ledger ----------
def reconcile(path=None, ledger=None, today=None):
    path = path or OUTREACH; ledger = ledger or LEDGER
    try:
        evs = [json.loads(l) for l in open(ledger) if l.strip()]
    except FileNotFoundError:
        evs = []
    refunded = {e["order"] for e in evs if e["type"] == "refund_processed"}
    paid = [e for e in evs if e["type"] == "order_paid" and not e.get("test") and not e.get("free")
            and e.get("utm_content", "unknown").startswith("det-") and e["order"] not in refunded]
    marked = 0
    known = {r["contact_ref"] for r in rows(path)}
    for e in paid:
        ref = e["utm_content"]
        if ref in known and current_stage(ref, path) not in ("PAID", "ACTIVATED", "OPTED_OUT"):
            # A paid order can follow an approved contact; bypass the approval gate only for PAID, which is evidence based.
            new = not os.path.exists(path)
            with open(path, "a", newline="") as f:
                csv.DictWriter(f, fieldnames=OUTREACH_FIELDS).writerow(
                    {"date": (today or datetime.date.today()).isoformat(), "contact_ref": ref, "trade": "detailing",
                     "channel": "", "campaign": CAMPAIGN, "status": "PAID", "score": "", "offer": e.get("offer_id", ""),
                     "attribution_id": ref, "objection": "", "approved_by": "",
                     "note": f"ledger order {e['order'][:12]} {e['gross_cents']} cents"})
            marked += 1
    return marked


def followups_due(today=None, path=None):
    """Leads CONTACTED at least follow_up_after_days ago with no later stage and no follow up yet.
    Returns lead_refs only. A person still writes and sends the follow up; max follow_ups_max per lead."""
    path = path or OUTREACH
    today = today or datetime.date.today()
    cfg = sender(); wait = int(cfg.get("follow_up_after_days", 4)); cap = int(cfg.get("follow_ups_max", 1))
    hist = {}
    for r in rows(path):
        hist.setdefault(r["contact_ref"], []).append(r)
    due = []
    for ref, rs in hist.items():
        if rs[-1]["status"] != "CONTACTED":
            continue
        contacts = [r for r in rs if r["status"] == "CONTACTED"]
        followed = sum(1 for r in rs if "follow up" in (r.get("note") or "").lower())
        last = datetime.date.fromisoformat(rs[-1]["date"])
        if followed < cap and (today - last).days >= wait:
            due.append(ref)
    return due


def summary(path=None):
    path = path or OUTREACH
    latest = {}
    for r in rows(path):
        latest[r["contact_ref"]] = r["status"]
    counts = {s: 0 for s in STAGES + CLOSED}
    for s in latest.values():
        counts[s] = counts.get(s, 0) + 1
    reached = lambda s: sum(1 for v in latest.values() if v in STAGES[STAGES.index(s):])
    return {"leads": len(latest), "by_stage": counts, "qualified_or_later": reached("QUALIFIED"),
            "contacted_or_later": reached("CONTACTED"), "replied_or_later": reached("INTERESTED"),
            "paid": counts["PAID"] + counts["ACTIVATED"], "opted_out": counts["OPTED_OUT"]}


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(0)
    cmd = a[0]
    if cmd == "score":
        out = process(a[1], a[2])
        print(json.dumps({"scored": len(out), "needs_approval": sum(o["review_flag"] == "NEEDS_APPROVAL" for o in out),
                          "messages_sent": 0}))
    elif cmd == "approve":
        print(record(a[1], "APPROVED", approved_by=a[2], note=a[3]))
    elif cmd == "stage":
        print(record(a[1], a[2], note=a[3] if len(a) > 3 else ""))
    elif cmd == "optout":
        print(opt_out(a[1]))
    elif cmd == "reconcile":
        print(json.dumps({"marked_paid": reconcile()}))
    elif cmd == "summary":
        print(json.dumps(summary(), indent=1))
