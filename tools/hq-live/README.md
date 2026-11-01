# AUTOPILOT.OI Chicago HQ (live)

A three.js page (published as a claude.ai artifact) that shows the agent workforce as hooded operatives in a converted
Chicago warehouse. Live data comes from the viewer's own connectors via the artifact `mcp` capability:

- Claude Code Remote `list_triggers`: every scheduled agent, its last run and next run. State per agent:
  WORKING (run fired and not finished), COMPLETED (finished in the last 20 min), IDLE, FAILED, PAUSED (disabled).
  PLANNING / COLLABORATING / REVIEWING / AWAITING APPROVAL are not shown because nothing reports them yet.
- Metricool `getScheduledPosts` (today, ART): posts out, queued, failed; a packet flies from the creating desk to
  the wall screen for each published post.
- Kit `get_growth_stats`: subscribers.

CEO actions (behind an in-page confirm): Run now (`fire_trigger`), Pause / Resume (`update_trigger enabled`).
GitHub Actions workers (health, revenue ledger, kit sync) have desks but show NO LIVE FEED until a feed exists.
Revenue shows "Gumroad not linked" until a Gumroad source reaches the page.
`#demo` in the address loads clearly labeled SIMULATED data for design checks only.
Artifact: https://claude.ai/artifact/1u49cT2kQkXCM9WKmApZVM
