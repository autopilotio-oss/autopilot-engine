"""P0-02 Immutable event store (Growth OS 3.0 section 05).

Append only JSONL, hash chained, unique (source, source_event_id). Facts about orders, publications, approvals, jobs,
incidents and spend are events; dashboards are views computed from them. Invalid payloads are rejected and the
rejection itself is recorded as a security.event_rejected event (no state change).

The public repo store (state/events/events.jsonl) holds NO personal data: customers appear only as salted hashes.
Contact and support details stay in Kit and in the private artifact database (see growth-os/ARCHITECTURE.md)."""
import datetime as dt, hashlib, json, os, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT = os.path.join(ROOT, "state", "events", "events.jsonl")
NS = uuid.UUID("6f1d2c5e-8a3b-4c71-9e0f-2b7a4d5c6e81")

# required payload keys per event type (payload_version 1)
SCHEMA = {
    "content.evidence_verified": ["content_id", "refs"],
    "content.qa_passed": ["content_id", "score", "version"],
    "content.approval_granted": ["content_id", "version", "approval_id"],
    "content.published": ["content_id", "version", "platform", "url"],
    "landing.viewed": ["page"],
    "guide.requested": ["guide_id"],
    "contact.opted_in": ["contact_ref", "consent_scope", "consent_source"],
    "contact.unsubscribed": ["contact_ref"],
    "email.sent": ["contact_ref", "campaign_id"],
    "checkout.started_if_available": ["product_id"],
    "order.paid": ["order_id", "provider", "product_id", "amount_minor", "currency", "fee_minor"],
    "order.refunded": ["order_id", "provider", "refund_minor", "currency"],
    "product.delivered": ["order_id", "product_id", "version"],
    "support.opened": ["case_id", "category", "severity"],
    "support.resolved": ["case_id", "resolution"],
    "job.failed": ["job_id", "error"],
    "job.recovered": ["job_id"],
    "spend.recorded": ["vendor", "amount_minor", "currency", "kind"],
    "spend.approved": ["approval_id", "limit_minor", "currency"],
    "deployment.approved": ["approval_id", "sha"],
    "incident.opened": ["incident_id", "severity", "check"],
    "incident.resolved": ["incident_id"],
    "security.event_rejected": ["reason"],
    "flag.changed": ["flag", "value"],
    "approval.granted": ["approval_id", "action", "resource_id"],
    "approval.used": ["approval_id"],
    "approval.revoked": ["approval_id", "reason"],
}
INT_FIELDS = {"amount_minor", "fee_minor", "refund_minor", "limit_minor"}


class EventError(ValueError):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


class Store:
    def __init__(self, path=DEFAULT):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._keys = None

    def all(self):
        if not os.path.exists(self.path):
            return []
        return [json.loads(l) for l in open(self.path) if l.strip()]

    def _index(self):
        if self._keys is None:
            self._keys = {(e["source"], e["source_event_id"]): e for e in self.all()}
        return self._keys

    def _last_hash(self):
        ev = self.all()
        return ev[-1]["hash"] if ev else "GENESIS"

    def validate(self, etype, payload):
        if etype not in SCHEMA:
            raise EventError(f"unknown event type {etype}")
        if not isinstance(payload, dict):
            raise EventError("payload must be an object")
        miss = [k for k in SCHEMA[etype] if payload.get(k) in (None, "")]
        if miss:
            raise EventError(f"{etype}: missing {miss}")
        for k in INT_FIELDS & set(payload):
            if not isinstance(payload[k], int) or isinstance(payload[k], bool) or payload[k] < 0:
                raise EventError(f"{etype}: {k} must be a non negative integer (minor units)")
        if "currency" in payload and not (isinstance(payload["currency"], str) and len(payload["currency"]) == 3):
            raise EventError(f"{etype}: currency must be a 3 letter code")
        if "@" in json.dumps(payload):
            raise EventError(f"{etype}: payload looks like it contains an email address (PII not allowed here)")

    def append(self, etype, payload, source, source_event_id, actor="system", correlation_id=None, occurred_at=None):
        """Returns (event, created: bool). A repeated (source, source_event_id) returns the original, unchanged."""
        key = (source, str(source_event_id))
        if key in self._index():
            return self._index()[key], False
        try:
            self.validate(etype, payload)
        except EventError as e:
            self._write("security.event_rejected", {"reason": str(e)[:300], "rejected_type": etype}, "growthos",
                        f"rej:{source}:{source_event_id}", actor, correlation_id, None)
            raise
        return self._write(etype, payload, source, str(source_event_id), actor, correlation_id, occurred_at), True

    def _write(self, etype, payload, source, seid, actor, cid, occurred_at):
        e = {"event_id": str(uuid.uuid5(NS, f"{source}|{seid}")), "type": etype, "occurred_at_utc": occurred_at or now(),
             "recorded_at_utc": now(), "source": source, "source_event_id": seid, "actor": actor, "payload_version": 1,
             "payload": payload, "correlation_id": cid or str(uuid.uuid4()), "prev": self._last_hash()}
        e["hash"] = hashlib.sha256(json.dumps(e, sort_keys=True).encode()).hexdigest()
        with open(self.path, "a") as f:
            f.write(json.dumps(e, sort_keys=True) + "\n")
        self._index()[(source, seid)] = e
        return e

    def verify(self):
        prev = "GENESIS"
        for i, e in enumerate(self.all()):
            h = e.pop("hash")
            if e["prev"] != prev or hashlib.sha256(json.dumps(e, sort_keys=True).encode()).hexdigest() != h:
                return False, i
            prev = h
        return True, len(self.all())

    def of(self, *types):
        return [e for e in self.all() if e["type"] in types]
