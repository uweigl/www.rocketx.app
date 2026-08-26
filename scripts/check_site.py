#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Consistency checks for the RocketX site and the business-case decks.

Run from the repo root after editing index.html or regenerating the decks:

    python3 scripts/check_site.py

Exits non-zero if any invariant is broken, so it can gate a deploy.
The page-count check exists because the site advertised "8 pages" for
months after the deck grew to 14 - a claim about an artifact drifts
silently unless something compares the two.
"""
import io, json, os, re, json, sys, html
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FAIL = []
def check(name, ok, detail=""):
    print("  %-42s %s%s" % (name, "PASS" if ok else "FAIL", "  " + detail if detail and not ok else ""))
    if not ok: FAIL.append(name)

S = io.open("index.html", encoding="utf-8").read()
BODY = S[S.index("</style>"):]
LANGS = ("de", "es", "nl")

# ---------------------------------------------------------------- i18n
print("\ni18n")
lit = re.search(r'const I18N=(\{.*?\});\n', S, re.S).group(1)
dups = []
def hook(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen: dups.append(k)
        seen[k] = v
    return seen
D = json.loads(lit, object_pairs_hook=hook)
json.loads(re.search(r'const MAILTO=(\{.*?\});\n', S, re.S).group(1))
USED = set()
for attr in ("data-i18n", "data-i18n-aria", "data-i18n-title", "data-i18n-text"):
    USED |= set(re.findall(r'%s="([^"]+)"' % attr, S))
check("no duplicate keys", not dups, str(sorted(set(dups))))
for l in LANGS:
    miss = sorted(k for k in USED if k not in D[l])
    orph = sorted(k for k in D[l] if k not in USED)
    check("%s: every DOM key translated" % l, not miss, str(miss))
    check("%s: no orphaned keys" % l, not orph, str(orph))
check("all keysets identical", set(D["de"]) == set(D["es"]) == set(D["nl"]),
      str(sorted(set(D["de"]) ^ set(D["es"]) ^ set(D["nl"]))))

# ---------------------------------------------------------------- structure
print("\nstructure")
VOID = {'br','img','meta','link','input','hr','source','path','circle','stop','use','area',
        'col','rect','ellipse','line','polygon','image','text'}
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.st=[]; self.err=[]
    def handle_starttag(self, t, a):
        if t not in VOID: self.st.append(t)
    def handle_endtag(self, t):
        if t in VOID: return
        if self.st and self.st[-1] == t: self.st.pop()
        elif t in self.st:
            while self.st and self.st.pop() != t: pass
        else: self.err.append(t)
p = Parser(); p.feed(S)
check("html well formed", not p.st and not p.err, "unclosed=%s stray=%s" % (p.st[:4], p.err[:4]))
ids = re.findall(r'\sid="([^"]+)"', S)
check("no duplicate ids", len(ids) == len(set(ids)),
      str([i for i in set(ids) if ids.count(i) > 1]))
bad_anchor = sorted(a for a in re.findall(r'href="#([^"]+)"', S) if a not in ids and a != "top")
check("anchors resolve", not bad_anchor, str(bad_anchor))
bad_js = sorted(set(re.findall(r"getElementById\('([^']+)'\)", S)) - set(ids))
check("js element targets exist", not bad_js, str(bad_js))
svg_bad = []
for cls in re.findall(r'<svg class="(\w+)"', S):
    m = re.search(r'<svg class="%s".*?</svg>' % cls, S, re.S)
    try: ET.fromstring(m.group(0))
    except Exception: svg_bad.append(cls)
check("inline svgs parse as xml", not svg_bad, str(svg_bad))

# ---------------------------------------------------------------- assets
print("\nassets")
refs = sorted(set(re.findall(r'(?:href|src)="((?:assets/|favicon|site\.web)[^"]+)"', S)))
missing = [r for r in refs if not os.path.exists(r)]
check("every referenced asset exists", not missing, str(missing))

# ---------------------------------------------------------------- decks
print("\ndecks")
def pdf_pages(path):
    return len(re.findall(rb'/Type\s*/Page[^s]', io.open(path, "rb").read()))
counts = {}
for l in ("en", "de", "es", "nl"):
    pdf = "assets/rocketx-business-case-%s.pdf" % l
    if not os.path.exists(pdf):
        check("pdf %s present" % l, False); continue
    counts[l] = pdf_pages(pdf)
check("all three decks have equal page counts", len(set(counts.values())) == 1, str(counts))

# the check this file exists for: does the site's claim match the artifact?
claimed = set()
for txt in [html.unescape(re.sub(r'<[^>]+>', '', m)) for m in
            re.findall(r'data-i18n="ln.decknote">(.*?)</p>', BODY, re.S)] + \
           [D[l]["ln.decknote"] for l in LANGS if "ln.decknote" in D[l]]:
    for n in re.findall(r'(\d+)\s*(?:pages?|Seiten|páginas)', txt, re.I):
        claimed.add(int(n))
actual = set(counts.values())
check("site's stated page count matches the PDFs",
      bool(claimed) and claimed == actual, "site says %s, PDFs are %s" % (sorted(claimed), sorted(actual)))

for l in ("en", "de", "es", "nl"):
    f = "deck/rocketx-business-case-%s.html" % l
    if not os.path.exists(f): continue
    h = io.open(f, encoding="utf-8").read()
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    check("%s: no double-escaped entities" % l, not re.search(r'&amp;[a-z#0-9]+;', h))
    check("%s: no unverified certifications" % l, not re.search(r'ISO 27001|SOC 2|PCI DSS', t))
    # RocketX's own amounts must stay out. A competitor's published cap, cited
    # with attribution in the fee-share chart, is not RocketX pricing.
    check("%s: no rocketx pricing" % l, not re.search(
        r'\$6,000|\$8,500|\$12,000|\$64,800|\$91,800|\$129,600'
        r'|5\.000\s*€|7\.000\s*€|10\.000\s*€|54\.000\s*€|75\.600\s*€|108\.000\s*€'
        r'|€\s*5\.000|€\s*7\.000|€\s*10\.000|€\s*54\.000|€\s*75\.600|€\s*108\.000', t))
    check("%s: page numbers present" % l, 'class="foot"' in h)
    check("%s: baymard citation resolves" % l, ("Baymard" not in t) or bool(re.search(r'70\s*%', t)))

# ------------------------------------------------- fee curve vs live pricing
print("\nfee curve")
try:
    site = io.open("index.html", encoding="utf-8").read()
    I18N = json.loads(re.search(r"const I18N=(\{.*?\});\n", site, re.S).group(1))
    gd = io.open("scripts/gen_deck.py", encoding="utf-8").read()
    def nums(txt, lo, hi):
        out = []
        for m in re.findall(r"\d[\d.,]*", txt):
            v = m.rstrip(".,").replace(".", "").replace(",", "")
            if v.isdigit() and lo <= int(v) <= hi:
                out.append(int(v))
        return out
    for lang in ("en", "de", "es", "nl"):
        d = I18N[lang]
        fees = [nums(d["pr.a%d" % i], 1000, 10 ** 7)[0] for i in (1, 2, 3)]
        b1 = nums(d["pr.for1"], 1, 999)
        b3 = nums(d["pr.for3"], 1, 999)
        bands = [b1[0], b1[1], b3[0], b3[1]]
        blk = gd[gd.index('"%s": dict(' % lang):]
        blk = blk[:blk.index("fg2_ha")]
        gf = [int(x) for x in re.findall(r"fg1_fees=\[([^\]]*)\]", blk)[0].replace(" ", "").split(",")]
        gb = [int(x) for x in re.findall(r"fg1_bands=\[([^\]]*)\]", blk)[0].replace(" ", "").split(",")]
        check("%s: fee curve fees match site pricing" % lang, gf == fees, "%s vs %s" % (gf, fees))
        check("%s: fee curve bands match site pricing" % lang, gb == bands, "%s vs %s" % (gb, bands))
except Exception as e:
    check("fee curve cross-check ran", False, repr(e))

# ---------------------------------------------------------------- seo
print("\nseo")
import xml.etree.ElementTree as ET
PAGES = {"en": "index.html", "de": "de/index.html", "es": "es/index.html", "nl": "nl/index.html"}
CANON = {"en": "https://www.rocketx.app/", "de": "https://www.rocketx.app/de/",
         "es": "https://www.rocketx.app/es/", "nl": "https://www.rocketx.app/nl/"}
for lang, path in PAGES.items():
    if not os.path.exists(path):
        check("%s page exists" % lang, False, path); continue
    h = io.open(path, encoding="utf-8").read()
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    check("%s: meta description" % lang, bool(d) and len(d.group(1)) > 80)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    check("%s: canonical correct" % lang, bool(c) and c.group(1) == CANON[lang],
          c.group(1) if c else "missing")
    hl = set(re.findall(r'hreflang="([^"]+)"', h))
    check("%s: hreflang covers all languages" % lang, hl >= {"en", "de", "es", "nl", "x-default"}, str(sorted(hl)))
    check("%s: html lang attribute" % lang, ('<html lang="%s"' % lang) in h)
    check("%s: og:image + twitter card" % lang,
          'property="og:image"' in h and 'name="twitter:card"' in h)
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    ok = False
    if m:
        try:
            g = json.loads(m.group(1)); ok = "@graph" in g and len(g["@graph"]) >= 3
        except Exception: ok = False
    check("%s: JSON-LD parses" % lang, ok)

check("og:image file exists", os.path.exists("assets/og-image.png"))
check("robots.txt exists", os.path.exists("robots.txt"))
if os.path.exists("robots.txt"):
    rb = io.open("robots.txt", encoding="utf-8").read()
    check("robots.txt references the sitemap", "Sitemap:" in rb)
    check("robots.txt names AI crawlers",
          all(a in rb for a in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended")))
check("sitemap.xml exists", os.path.exists("sitemap.xml"))
if os.path.exists("sitemap.xml"):
    try:
        root = ET.parse("sitemap.xml").getroot(); sm_ok = True
    except Exception: sm_ok = False
    check("sitemap.xml parses", sm_ok)
    if sm_ok:
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        locs = [u.find(ns + "loc").text for u in root.findall(ns + "url")]
        local = [l.replace("https://www.rocketx.app/", "") or "index.html" for l in locs]
        local = [x if x.endswith((".pdf", ".html")) else x + "index.html" for x in local]
        gone = [x for x in local if not os.path.exists(x)]
        check("every sitemap url resolves to a file", not gone, str(gone))

# the pre-rendered pages are generated from index.html and go stale silently
def i18n_of(path):
    t = io.open(path, encoding="utf-8").read()
    m = re.search(r'const I18N=(\{.*?\});\n', t, re.S)
    return m.group(1) if m else None
base = i18n_of("index.html")
for lang in ("de", "es", "nl"):
    p = "%s/index.html" % lang
    if os.path.exists(p):
        check("%s page in sync with index.html" % lang, i18n_of(p) == base,
              "run scripts/build_i18n_pages.py")

# Canonical host. Confirmed as www.rocketx.app; a stray apex or http URL in a
# canonical, og:url or JSON-LD id silently splits ranking signals.
CANON_HOST = "https://www.rocketx.app"
bad_host = []
for f in ["index.html", "de/index.html", "es/index.html", "nl/index.html", "robots.txt", "sitemap.xml"]:
    if not os.path.exists(f): continue
    t = io.open(f, encoding="utf-8").read()
    for u in re.findall(r'https?://[A-Za-z0-9.-]*rocketx\.app', t):
        if u != CANON_HOST: bad_host.append("%s: %s" % (f, u))
check("all absolute urls use the canonical host", not bad_host, str(sorted(set(bad_host))[:4]))

print()
if FAIL:
    print("%d CHECK(S) FAILED: %s" % (len(FAIL), ", ".join(FAIL)))
    sys.exit(1)
print("all checks passed")
