"""P0-06 Durable task queue (sections 04 and 07).

Jobs: CREATED > VALIDATED > QUEUED > RUNNING > SUCCEEDED | RETRY_WAIT | NEEDS_APPROVAL | FAILED_FINAL | CANCELLED
Every transition is appended to state/jobs/jobs.jsonl (actor, UTC time, reason, previous and new state, trace id).
External side effects go through Queue.effect(job, key, fn): the effect key is written to state/jobs/effects.jsonl
right after the provider confirms, so a job resumed after a crash never repeats a side effect it already completed.
Transient failures (timeouts, 429, 5xx) retry with exponential backoff and jitter; after max_attempts the job is
dead lettered (FAILED_FINAL + job.failed event). Irreversible actions are never retried blindly."""
import datetime as dt, json, os, random, time, uuid

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TERMINAL = {"SUCCEEDED", "FAILED_FINAL", "CANCELLED"}


class TransientError(Exception):
    def __init__(self, msg, status=None):
        super().__init__(msg); self.status = status


class PermanentError(Exception):
    pass


class NeedsApproval(Exception):
    pass


def _now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


class Queue:
    def __init__(self, root=None, max_attempts=3, base_delay=2.0, max_delay=60.0, concurrency=None, events=None, sleep=time.sleep, rng=None):
        d = root or os.path.join(ROOT, "state", "jobs"); os.makedirs(d, exist_ok=True)
        self.log, self.fx = os.path.join(d, "jobs.jsonl"), os.path.join(d, "effects.jsonl")
        self.max_attempts, self.base, self.cap = max_attempts, base_delay, max_delay
        self.concurrency = concurrency or {}          # integration -> max RUNNING jobs
        self.events, self.sleep, self.rng = events, sleep, rng or random.Random(7)
        self.delays = []

    # ---- storage ----
    def _append(self, rec):
        with open(self.log, "a") as f:
            f.write(json.dumps(rec, sort_keys=True) + "\n")

    def jobs(self):
        cur = {}
        for l in (open(self.log) if os.path.exists(self.log) else []):
            if l.strip():
                r = json.loads(l)
                if r["kind"] == "create":
                    cur[r["job"]["job_id"]] = dict(r["job"])
                else:
                    cur[r["job_id"]].update(r.get("set", {}))
        return cur

    def _set(self, job_id, actor, reason, **fields):
        prev = self.jobs()[job_id]["status"]
        self._append({"kind": "update", "job_id": job_id, "at": _now(), "actor": actor, "reason": reason, "prev": prev,
                      "set": fields, "trace_id": self.jobs()[job_id]["trace_id"]})

    def done_effects(self):
        return {json.loads(l)["key"] for l in open(self.fx) if l.strip()} if os.path.exists(self.fx) else set()

    # ---- api ----
    def enqueue(self, type_, resource_id, idempotency_key, allowed_actions=(), integration=None, budget_cap_usd=None,
                deadline_utc=None, priority=5, policy_version="growthos-1", actor="system"):
        for j in self.jobs().values():
            if j["idempotency_key"] == idempotency_key:
                return j  # same work requested twice: one job
        job = {"job_id": "job_" + uuid.uuid4().hex[:12], "type": type_, "resource_id": resource_id, "idempotency_key": idempotency_key,
               "allowed_actions": list(allowed_actions), "integration": integration, "budget_cap_usd": budget_cap_usd,
               "deadline_utc": deadline_utc, "priority": priority, "policy_version": policy_version, "attempts": 0,
               "status": "CREATED", "trace_id": uuid.uuid4().hex, "created": _now()}
        self._append({"kind": "create", "job": job, "at": _now(), "actor": actor})
        if not type_ or not resource_id:
            self._set(job["job_id"], actor, "invalid job", status="CANCELLED"); return self.jobs()[job["job_id"]]
        self._set(job["job_id"], actor, "schema ok", status="VALIDATED")
        self._set(job["job_id"], actor, "ready", status="QUEUED")
        return self.jobs()[job["job_id"]]

    def effect(self, job, key, fn):
        """Run an external side effect once per key, ever. Returns the provider response or 'already_done'."""
        k = f"{job['idempotency_key']}:{key}"
        if k in self.done_effects():
            return "already_done"
        resp = fn()
        with open(self.fx, "a") as f:
            f.write(json.dumps({"key": k, "at": _now(), "job_id": job["job_id"], "provider_ref": str(resp)[:120]}) + "\n")
        return resp

    def run(self, job_id, handler, actor="worker", gate=None):
        """handler(job, queue) -> output dict. gate(job) -> None or a reason string to hold (kill switch, budget, approval)."""
        j = self.jobs()[job_id]
        if j["status"] in TERMINAL:
            return j
        integ = j.get("integration")
        if integ and self.concurrency.get(integ) is not None:
            running = sum(1 for x in self.jobs().values() if x["status"] == "RUNNING" and x.get("integration") == integ and x["job_id"] != job_id)
            if running >= self.concurrency[integ]:
                return j  # stays QUEUED: concurrency cap
        if gate:
            why = gate(j)
            if why:
                status = "NEEDS_APPROVAL" if why.startswith("approval") else "CANCELLED" if why.startswith("cancel") else "QUEUED"
                self._set(job_id, actor, why, status=status, held=why)
                return self.jobs()[job_id]
        while True:
            j = self.jobs()[job_id]
            self._set(job_id, actor, "start", status="RUNNING", attempts=j["attempts"] + 1)
            try:
                out = handler(self.jobs()[job_id], self)
                self._set(job_id, actor, "ok", status="SUCCEEDED", output=out)
                return self.jobs()[job_id]
            except NeedsApproval as e:
                self._set(job_id, actor, str(e), status="NEEDS_APPROVAL"); return self.jobs()[job_id]
            except PermanentError as e:
                return self._dead(job_id, actor, f"permanent: {e}")
            except TransientError as e:
                n = self.jobs()[job_id]["attempts"]
                if n >= self.max_attempts:
                    return self._dead(job_id, actor, f"retries exhausted: {e} ({e.status})")
                delay = min(self.cap, self.base * (2 ** (n - 1))) * (0.5 + self.rng.random())
                self.delays.append(round(delay, 2))
                self._set(job_id, actor, f"transient {e.status}: retry in {delay:.1f}s", status="RETRY_WAIT")
                self.sleep(delay)

    def _dead(self, job_id, actor, why):
        self._set(job_id, actor, why, status="FAILED_FINAL", dead_letter=True, error=why)
        if self.events is not None:
            self.events.append("job.failed", {"job_id": job_id, "error": why[:200]}, "growthos.jobs", f"dead:{job_id}", actor)
        return self.jobs()[job_id]

    def recover_stale(self, actor="recovery"):
        """After a crash, RUNNING jobs go back to QUEUED. Their completed effects are kept and will be skipped."""
        n = 0
        for j in self.jobs().values():
            if j["status"] == "RUNNING":
                self._set(j["job_id"], actor, "recovered after interrupted run", status="QUEUED"); n += 1
                if self.events is not None:
                    self.events.append("job.recovered", {"job_id": j["job_id"]}, "growthos.jobs", f"rec:{j['job_id']}:{n}", actor)
        return n

    def dead_letters(self):
        return [j for j in self.jobs().values() if j.get("dead_letter")]
