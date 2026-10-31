# Growth OS runbooks (section 22) and owner commands

## Owner commands (say them to Claude in chat)
| You say | What runs |
|---|---|
| "stop all outbound" | `python3 scripts/growthos/policy.py switch stop_all_outbound --by Seb` (publishing + messaging off; Gumroad fulfillment keeps working) |
| "resume outbound" | `... switch resume_outbound --by Seb` |
| "pause expenses" | `... switch pause_expenses --by Seb` (paid services + optional AI off) |
| "approve <content_id>" | `python3 scripts/viral/gate.py approve <id> --by Seb --channel chat --quote "<your words>"` then `advance` to QUEUED |
| "set AI caps $X soft, $Y hard per day" | edit config/growthos/budget.json (cents) |

## A. No published content
1. `gate.py status <id>`: state and version hash. 2. Metricool getScheduledPosts: is it there, ERROR? 3. Destination valid (brand 7761544 networks)? 4. Retry only the same post (same uuid) once. 5. If the gate fails, HOLD. 6. If an approved release is blocked, record an incident and tell Seb.

## B. Customer paid, kit not delivered
1. Gumroad: sale exists and is paid (ledger, `orders.py report`). 2. `health.py` check paid_but_undelivered. 3. Product mapping: state/products.json id + published + file version. 4. Gumroad delivers the file itself; if the product had no file, re-upload via the gumroad.yml sync (bump version). 5. Escalate to Seb with the order hash. Never send a different product.

## C. Email or DM compliance failure
1. `policy.py switch stop_all_outbound`. 2. Check consent and suppression (`consent.py`). 3. Find affected contact_refs. 4. Reconcile unsent messages and complaints in Kit. 5. Resume only with Seb's approval.

## D. AI spend spike
1. At the hard cap the policy refuses costed actions automatically. 2. Find the job ids (state/jobs, spend events). 3. Disable the runaway scheduled task (update_trigger enabled false). 4. Write the impact and a revised budget. 5. Resume within the approved cap.

## E. Bad content or customer safety claim
1. Set pending related Metricool posts to draft. 2. Capture the concept version, evidence, time and reach. 3. Seb decides removal or correction. 4. Fix the source and the agent guidance. 5. Add a test so the gate rejects the defect.

## F. Privacy or security incident
1. Stop affected integrations; revoke tokens only with Seb's OK (he holds the accounts). 2. Preserve evidence. 3. Scope affected data. 4. Tell Seb immediately. 5. Follow notification duties. 6. Never hide it from the dashboard.

## Rollback
- Code: `git revert <sha>` (every module is its own commit). Event history is append only and stays.
- Flags: restore config/growthos/flags.json from git.
- Scheduled tasks: restore the prompt snapshot in growth-os/rollback/ with update_trigger (snapshots are taken at cutover).
- Health workflow: disable `.github/workflows/health.yml` (Actions > workflow > Disable) or delete the file.
