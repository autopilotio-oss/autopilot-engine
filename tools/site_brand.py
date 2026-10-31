"""Apply brand type to every site page and page template: link /assets/brand.css and drop Google Font families it replaces.
python3 tools/site_brand.py   (idempotent)"""
import glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = '<link rel="stylesheet" href="/assets/brand.css">'
DROP = ["Saira+Semi+Condensed", "Bebas+Neue", "Barlow+Condensed", "Geist+Mono", "Space+Mono"]
def fix(s):
    def gf(m):
        url = m.group(0)
        for d in DROP: url = re.sub(r"family=" + re.escape(d) + r"[^&\"']*&?", "", url)
        return url.replace("?&", "?").replace("&&", "&").replace("&display", "&display")
    s = re.sub(r"https://fonts\.googleapis\.com/css2\?[^\"']+", gf, s)
    if LINK not in s: s = s.replace("</head>", LINK + "</head>", 1)
    return s
n = 0
for f in glob.glob(f"{ROOT}/docs/**/*.html", recursive=True) + [f"{ROOT}/tools/guides/build.py", f"{ROOT}/tools/store/pages.py"]:
    if "/media/" in f: continue
    s = open(f).read(); t = fix(s)
    if t != s: open(f, "w").write(t); n += 1
print("branded", n, "files")
