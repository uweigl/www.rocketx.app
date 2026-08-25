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
import io, os, re, json, sys, html
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
LANGS = ("de", "es")

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
check("de/es keysets identical", set(D["de"]) == set(D["es"]),
      str(sorted(set(D["de"]) ^ set(D["es"]))))

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
for l in ("en", "de", "es"):
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

for l in ("en", "de", "es"):
    f = "deck/rocketx-business-case-%s.html" % l
    if not os.path.exists(f): continue
    h = io.open(f, encoding="utf-8").read()
    t = html.unescape(re.sub(r'<[^>]+>', ' ', h))
    check("%s: no double-escaped entities" % l, not re.search(r'&amp;[a-z#0-9]+;', h))
    check("%s: no unverified certifications" % l, not re.search(r'ISO 27001|SOC 2|PCI DSS', t))
    check("%s: no pricing" % l, not re.search(r'\$6,000|\$8,500|\$12,000|\$40,000|34\.000 €|54\.000 €', t))
    check("%s: page numbers present" % l, 'class="foot"' in h)
    check("%s: baymard citation resolves" % l, ("Baymard" not in t) or bool(re.search(r'70\s*%', t)))

print()
if FAIL:
    print("%d CHECK(S) FAILED: %s" % (len(FAIL), ", ".join(FAIL)))
    sys.exit(1)
print("all checks passed")
