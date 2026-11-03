"""CI secret scan (Master plan WP01 / integration map): no API keys or tokens in any tracked text file,
no unsealed PDFs. Binary files (fonts, images, video, encrypted blobs) are skipped."""
import os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = {
    "meta_token": r"\bEAA[A-Za-z0-9]{40,}",
    "github_token": r"\b(ghp|gho|ghs|ghu)_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}",
    "openai_style_key": r"\bsk-(proj-)?[A-Za-z0-9_-]{32,}",
    "slack_token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
    "private_key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "token_in_url": r"access_token=[A-Za-z0-9_-]{20,}",
}
SKIP_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".mp4", ".mp3", ".wav", ".otf", ".ttf", ".woff", ".woff2",
            ".enc", ".ico", ".zip", ".gz", ".pdf")


def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
    return [f for f in out if f]


def test_no_secrets_in_tracked_text_files():
    hits = []
    for f in tracked():
        if f.lower().endswith(SKIP_EXT):
            continue
        p = os.path.join(ROOT, f)
        try:
            if os.path.getsize(p) > 3_000_000:
                continue
            t = open(p, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for name, rx in PATTERNS.items():
            if re.search(rx, t):
                hits.append((f, name))
    assert not hits, f"possible secrets committed: {hits}"


def test_no_unsealed_pdfs():
    assert not [f for f in tracked() if f.lower().endswith(".pdf")], "unsealed PDF committed"
