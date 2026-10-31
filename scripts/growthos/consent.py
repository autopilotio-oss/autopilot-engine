"""P0-04 Consent and unsubscribe source of truth (section 06 Identity and consent; section 11 lifecycle).

Kit is the system of record for email consent (it stores the address, the form that captured it and unsubscribes).
Growth OS keeps only a pseudonymous contact_ref (salted hash of the Kit subscriber id), the consent scope, source,
time and withdrawal, so the public repo never holds an email address.

Rule: marketing email may go only to a contact whose latest consent event is opted_in with scope "marketing_email".
Any later unsubscribe suppresses all future marketing, including sequences already in progress.

python3 scripts/growthos/consent.py ingest <kit_subscribers.json>   (export from the Kit connector: id, state, created_at, fields.source)"""
import hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from events import Store  # noqa: E402

SALT = "autopilot-oi-contact-v1"  # pseudonymisation only; the id alone is not an email


def contact_ref(kit_id):
    return "k_" + hashlib.sha256((SALT + str(kit_id)).encode()).hexdigest()[:16]


def ingest_kit(store, subscribers):
    """Turn Kit subscriber records into consent events. Idempotent per subscriber and state."""
    n = 0
    for s in subscribers:
        ref = contact_ref(s["id"]); state = s.get("state")
        src = ((s.get("fields") or {}).get("source") or "unknown")[:40]
        if state in ("active", "inactive", "cancelled", "bounced", "complained"):
            _, c = store.append("contact.opted_in", {"contact_ref": ref, "consent_scope": "marketing_email",
                                                     "consent_source": f"kit_form:{src}", "region": "unknown"},
                                "kit", f"optin:{s['id']}", "kit_sync", occurred_at=s.get("created_at"))
            n += c
        if state in ("cancelled", "bounced", "complained"):
            _, c = store.append("contact.unsubscribed", {"contact_ref": ref, "kit_state": state}, "kit", f"unsub:{s['id']}", "kit_sync")
            n += c
    return n


def state(store):
    st = {}
    for e in sorted(store.of("contact.opted_in", "contact.unsubscribed"), key=lambda e: (e["occurred_at_utc"], e["recorded_at_utc"])):
        ref = e["payload"]["contact_ref"]
        if e["type"] == "contact.opted_in":
            st.setdefault(ref, {"opted_in": e["occurred_at_utc"], "scope": e["payload"]["consent_scope"], "unsubscribed": None})
        else:
            st.setdefault(ref, {"opted_in": None, "scope": None, "unsubscribed": None})["unsubscribed"] = e["occurred_at_utc"]
    return st


def may_send_marketing(store, ref):
    s = state(store).get(ref)
    return bool(s and s["opted_in"] and s["scope"] == "marketing_email" and not s["unsubscribed"])


def suppression_list(store):
    return sorted(r for r, s in state(store).items() if s["unsubscribed"])


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "ingest":
        st = Store(); subs = json.load(open(sys.argv[2])); subs = subs.get("subscribers", subs) if isinstance(subs, dict) else subs
        print("new consent events:", ingest_kit(st, subs))
        s = state(st); print(json.dumps({"contacts": len(s), "suppressed": len(suppression_list(st))}))
