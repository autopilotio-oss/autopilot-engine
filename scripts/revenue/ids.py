"""Canonical IDs and UTM links for Revenue Engine 2.0 (see revenue-engine-v2/METRICS.md).

offer_id    = the Gumroad permalink with dashes as underscores, e.g. subs_agent, all_money_agents, workspace
content_id  = <platform>_<format>_<offer short>_<NNN>[_<variant>], e.g. ig_reel_subs_003_b
campaign_id = <topic>_<iso year>w<iso week>, e.g. subscription_leak_2026w45

Only lowercase letters, digits and underscores. Never put personal data in an ID."""
import re, datetime, urllib.parse

ID_RE = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")
PLATFORMS = {"ig": "instagram", "tt": "tiktok", "th": "threads", "x": "x", "yt": "youtube", "em": "email", "site": "site"}
FORMATS = {"reel", "carousel", "post", "story", "video", "text", "card", "email", "demo"}
MEDIUM = {"instagram": "organic_social", "tiktok": "organic_social", "threads": "organic_social", "x": "organic_social",
          "youtube": "organic_social", "email": "email", "site": "site"}


def offer_id(permalink: str) -> str:
    oid = permalink.strip().lower().replace("-", "_")
    if not ID_RE.match(oid):
        raise ValueError(f"bad offer permalink: {permalink!r}")
    return oid


def permalink(offer: str) -> str:
    return offer.replace("_", "-")


def campaign_id(topic: str, when: datetime.date | None = None) -> str:
    when = when or datetime.datetime.utcnow().date()
    y, w, _ = when.isocalendar()
    t = re.sub(r"[^a-z0-9]+", "_", topic.lower()).strip("_")
    cid = f"{t}_{y}w{w:02d}"
    assert ID_RE.match(cid), cid
    return cid


def content_id(platform: str, fmt: str, offer_short: str, n: int, variant: str | None = None) -> str:
    if platform not in PLATFORMS:
        raise ValueError(f"unknown platform {platform!r}, use one of {sorted(PLATFORMS)}")
    if fmt not in FORMATS:
        raise ValueError(f"unknown format {fmt!r}, use one of {sorted(FORMATS)}")
    short = re.sub(r"[^a-z0-9]+", "", offer_short.lower())
    cid = f"{platform}_{fmt}_{short}_{n:03d}" + (f"_{variant.lower()}" if variant else "")
    assert ID_RE.match(cid), cid
    return cid


def parse_content_id(cid: str) -> dict:
    parts = cid.split("_")
    if len(parts) < 4 or parts[0] not in PLATFORMS or parts[1] not in FORMATS:
        return {"valid": False}
    return {"valid": True, "platform": PLATFORMS[parts[0]], "format": parts[1], "offer_short": parts[2],
            "n": int(parts[3]) if parts[3].isdigit() else None, "variant": parts[4] if len(parts) > 4 else None}


def utm_url(url: str, platform: str, campaign: str, content: str) -> str:
    """Add the standard UTM set to a link we control (our site or Gumroad). Existing query params are kept."""
    if platform not in MEDIUM:
        platform = PLATFORMS.get(platform, platform)
    for v in (campaign, content):
        if not ID_RE.match(v):
            raise ValueError(f"bad id {v!r}")
    u = urllib.parse.urlsplit(url)
    q = dict(urllib.parse.parse_qsl(u.query))
    q.update({"utm_source": platform, "utm_medium": MEDIUM.get(platform, "organic_social"),
              "utm_campaign": campaign, "utm_content": content})
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, urllib.parse.urlencode(q), u.fragment))


def source_of(params: dict | None) -> dict:
    """Normalise attribution params from an order or event. Missing values stay 'unknown' (never guessed)."""
    p = {k.lower(): (v[0] if isinstance(v, list) else v) for k, v in (params or {}).items()}
    out = {}
    for k in ("utm_source", "utm_medium", "utm_campaign", "utm_content"):
        v = (p.get(k) or "").strip().lower()
        out[k] = v if v else "unknown"
    return out
