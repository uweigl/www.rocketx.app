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
import io, json, sys, os, re, json, sys, html
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
for attr in ("data-i18n", "data-i18n-aria", "data-i18n-title", "data-i18n-text", "data-i18n-alt"):
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

# ------------------------------------------------- nav labels vs section kickers
print("\nlabels")
try:
    _src = io.open("index.html", encoding="utf-8").read()
    _I = json.loads(re.search(r"const I18N=(\{.*?\});\n", _src, re.S).group(1))
    for _l in ("en", "de", "es", "nl", "fr"):
        odd = [k for k, v in _I[_l].items() if k.endswith(".k") and not v.startswith("/ ")]
        check("%s: section kickers use the '/ ' prefix" % _l, not odd, str(odd))
        # a nav label and the section it points at should name the same thing
        nav = _I[_l]["nav.insights"].strip().lower()
        kick = _I[_l]["in.k"].replace("/", "").strip().lower()
        check("%s: nav label matches the articles kicker" % _l, nav == kick,
              "%r vs %r" % (nav, kick))
except Exception as e:
    check("label cross-check ran", False, repr(e))

# ------------------------------------------------- fee curve vs live pricing
print("\nfee curve")
try:
    site = io.open("index.html", encoding="utf-8").read()
    I18N = json.loads(re.search(r"const I18N=(\{.*?\});\n", site, re.S).group(1))
    gd = io.open("scripts/gen_deck.py", encoding="utf-8").read()
    def nums(txt, lo, hi):
        # French uses a space as the thousands separator, German and Spanish a
        # point, so strip all three before reading the figure
        out = []
        for m in re.findall(u"\\d[\\d.,\u00a0 ]*", txt):
            v = m.rstrip(u".,\u00a0 ").replace(".", "").replace(",", "")
            v = v.replace(u"\u00a0", "").replace(" ", "")
            if v.isdigit() and lo <= int(v) <= hi:
                out.append(int(v))
        return out
    for lang in ("en", "de", "es", "nl", "fr"):
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

# ---------------------------------------------------------------- FAQPage
print("\nfaq")
sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
try:
    import faq as _faq
    _P = {"en": "index.html", "de": "de/index.html", "es": "es/index.html", "nl": "nl/index.html", "fr": "fr/index.html"}
    for lang, path in _P.items():
        if not os.path.exists(path):
            continue
        h = io.open(path, encoding="utf-8").read()
        g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))
        node = [e for e in g["@graph"] if e.get("@type") == "FAQPage"]
        check("%s: FAQPage present" % lang, bool(node))
        if not node:
            continue
        qs = node[0]["mainEntity"]
        # the questions are the deck's, so a change there must reach the markup
        deck_q = _faq.questions(lang)
        check("%s: FAQ matches the deck questions" % lang,
              [q["name"] for q in qs] == deck_q,
              "%d vs %d" % (len(qs), len(deck_q)))
        thin = [q["name"][:30] for q in qs
                if len((q.get("acceptedAnswer") or {}).get("text", "")) < 40]
        check("%s: every FAQ answer is substantive" % lang, not thin, str(thin))
        check("%s: FAQ inLanguage correct" % lang, node[0].get("inLanguage") == lang)
        if lang != "en":
            check("%s: FAQ is not English" % lang,
                  "Does the platform fee" not in json.dumps(node[0], ensure_ascii=False))
except Exception as e:
    check("faq cross-check ran", False, repr(e))

# ------------------------------------------------- localisation typography
print("\ntypography")
try:
    import sys as _sys
    _sys.path.insert(0, os.path.join(os.getcwd(), "scripts"))
    import gen_deck as _gd
    _src = io.open("index.html", encoding="utf-8").read()
    _I = json.loads(re.search(r"const I18N=(\{.*?\});\n", _src, re.S).group(1))
    def _flat(d):
        out = {}
        for k, v in d.items():
            if isinstance(v, str):
                out[k] = v
            elif isinstance(v, (list, tuple)):
                for i, e in enumerate(v):
                    if isinstance(e, (list, tuple)):
                        for j, x in enumerate(e):
                            if isinstance(x, str):
                                out["%s[%d][%d]" % (k, i, j)] = x
                    elif isinstance(e, str):
                        out["%s[%d]" % (k, i)] = e
        return out
    NB = u"\u00a0"
    RX = re.compile(u"(\\d)([ \u00a0])(\u20ac|%)|(\u20ac)([ \u00a0])(\\d)")
    for _l in ("de", "es", "nl", "fr"):
        _S = dict(("site/" + k, re.sub(r"<[^>]+>", "", v)) for k, v in _I[_l].items())
        _S.update(("deck/" + k, v) for k, v in _flat(_gd.C[_l]).items())
        # a number must never separate from its currency or percent sign
        bad = [k for k, v in _S.items() for m in RX.finditer(v)
               if (m.group(2) or m.group(5)) != NB]
        check("%s: currency and percent use protected spaces" % _l, not bad, str(sorted(set(bad))[:4]))
        # French groups thousands with a space; it must not break across lines
        if _l == "fr":
            GRP = re.compile(u"\\d+(?: \\d{3})+")
            wrap = [k for k, v in _S.items() if GRP.search(v)]
            check("fr: thousands separators are non-breaking", not wrap,
                  str(sorted(set(wrap))[:4]))
    # register: German is Sie throughout, Dutch is je throughout
    de_all = dict(_I["de"]); de_all.update(_flat(_gd.C["de"]))
    check("de: no informal address", not [k for k, v in de_all.items()
          if re.search(r"\b(du|dein\w*|dich)\b", str(v))])
    nl_all = dict(_I["nl"]); nl_all.update(_flat(_gd.C["nl"]))
    check("nl: no formal address", not [k for k, v in nl_all.items()
          if re.search(r"\b(uw)\b", str(v))])
except Exception as e:
    check("typography cross-check ran", False, repr(e))

# ---------------------------------------------------------------- one-pager
print("\none-pager")
for _l in ("en", "de", "es", "nl", "fr"):
    _p = "assets/rocketx-one-page-%s.pdf" % _l
    if not os.path.exists(_p):
        check("%s: one-pager exists" % _l, False, _p); continue
    _b = io.open(_p, "rb").read()
    _n = max([int(x) for x in re.findall(rb"/Count (\d+)", _b)] or [0])
    check("%s: one-pager exists" % _l, True)
    # the whole point of the document is that it is one page
    check("%s: one-pager is a single page" % _l, _n == 1, "%d pages" % _n)
    check("%s: one-pager linked from the site" % _l,
          'data-onepager' in io.open("index.html", encoding="utf-8").read())

# ---------------------------------------------------------------- llms.txt
print("\nllms.txt")
LLMS = {"en": "llms.txt", "de": "de/llms.txt", "es": "es/llms.txt", "nl": "nl/llms.txt", "fr": "fr/llms.txt"}
PRICE_RX = re.compile(r"\$6,000|\$8,500|\$12,000|\$64,800|\$91,800|\$129,600"
                      r"|5\.000\s*\u20ac|7\.000\s*\u20ac|10\.000\s*\u20ac"
                      r"|54\.000\s*\u20ac|75\.600\s*\u20ac|108\.000\s*\u20ac")
for lang, path in LLMS.items():
    if not os.path.exists(path):
        check("%s: llms.txt exists" % lang, False, path); continue
    t = io.open(path, encoding="utf-8").read()
    check("%s: llms.txt exists" % lang, True)
    check("%s: llms.txt has H1 and summary" % lang,
          t.startswith("# RocketX") and "\n> " in t)
    # every local URL it advertises must actually be on disk
    bad = []
    for u in re.findall(r"\]\((https://www\.rocketx\.app[^)]*)\)", t):
        rel = u.replace("https://www.rocketx.app", "").split("#")[0].lstrip("/")
        cand = rel if rel else "index.html"
        if cand.endswith("/"):
            cand += "index.html"
        if not os.path.exists(cand):
            bad.append(u)
    check("%s: llms.txt links resolve" % lang, not bad, str(bad))
    check("%s: llms.txt carries no prices" % lang, not PRICE_RX.search(t))
    check("%s: llms.txt in its own language" % lang,
          ("What RocketX does" in t) if lang == "en" else ("What RocketX does" not in t))
    # the boundaries are the deck's, so they must appear verbatim
    try:
        import sys as _s
        _s.path.insert(0, os.path.join(os.getcwd(), "scripts"))
        import gen_deck as _g
        check("%s: llms.txt boundaries match the deck" % lang,
              all(b in t for _, b in _g.C[lang]["nf"]))
    except Exception as _e:
        check("%s: llms.txt boundary cross-check ran" % lang, False, repr(_e))

# ---------------------------------------------------------------- seo
print("\nseo")
import xml.etree.ElementTree as ET
PAGES = {"en": "index.html", "de": "de/index.html", "es": "es/index.html", "nl": "nl/index.html", "fr": "fr/index.html"}
CANON = {"en": "https://www.rocketx.app/", "de": "https://www.rocketx.app/de/",
         "es": "https://www.rocketx.app/es/", "nl": "https://www.rocketx.app/nl/",
         "fr": "https://www.rocketx.app/fr/"}
for lang, path in PAGES.items():
    if not os.path.exists(path):
        check("%s page exists" % lang, False, path); continue
    h = io.open(path, encoding="utf-8").read()
    d = re.search(r'<meta name="description" content="([^"]*)"', h)
    check("%s: meta description" % lang, bool(d) and len(d.group(1)) > 80)
    # a title over ~60 chars and a description over ~160 are cut off in results,
    # so the distinctive part has to fit inside the budget
    check("%s: description fits a search result" % lang,
          bool(d) and len(d.group(1)) <= 160, "%d chars" % len(d.group(1)) if d else "missing")
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    check("%s: title fits a search result" % lang,
          bool(t) and len(t.group(1)) <= 60, "%d chars" % len(t.group(1)) if t else "missing")
    # GMV was dropped from every localised body; the metadata must not reinstate it
    if lang != "en":
        meta_txt = " ".join(re.findall(r'<(?:meta|title)[^>]*content="([^"]*)"', h)
                            + ([t.group(1)] if t else []))
        check("%s: metadata avoids GMV" % lang, "GMV" not in meta_txt)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    check("%s: canonical correct" % lang, bool(c) and c.group(1) == CANON[lang],
          c.group(1) if c else "missing")
    if lang != "en":
        # JS rebuilds PDF hrefs on a language switch; from /<lang>/ an
        # un-prefixed 'assets/... resolves to /<lang>/assets/... and 404s
        stray = re.findall(r"(?<!\.\./)'assets/rocketx-[a-z-]+-'", h)
        check("%s: JS asset paths point out of the subdirectory" % lang,
              not stray, str(sorted(set(stray))))
    hl = set(re.findall(r'hreflang="([^"]+)"', h))
    check("%s: hreflang covers all languages" % lang,
          hl >= {"en", "de", "es", "nl", "fr", "x-default"}, str(sorted(hl)))
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
# the comic strips: dialogue is wrapped at build time, so a longer line silently
# grows a bubble downwards until its tail lands in somebody's head
import gen_404 as _g4
# topmost ink, not the head circle: the manager's hairs and the developer's
# fringe both stand well above it, and a tail landing there is what shows
_FIG_TOP = {0: _g4.FLOOR - 86 - 15 - 16,   # manager hair, panels 0 and 2
            1: _g4.DESK_Y - 52 - 14 - 6,   # developer fringe, panel 1
            2: _g4.FLOOR - 86 - 15 - 16}
_clash, _wide = [], []
for _n, _st in enumerate(_g4.STRIPS):
    for _l in _g4.LANGS:
        for _p in range(3):
            _lines = _g4.wrap(_st["text"][_l][_p], _g4.BW - 28)
            _bottom = _g4.BY + 16 + _g4.LH * len(_lines) + _g4.TAIL_H
            if _bottom >= _FIG_TOP[_p]:
                _clash.append("strip%d/%s/p%d" % (_n, _l, _p))
            if len(_lines) > 3:
                _wide.append("strip%d/%s/p%d" % (_n, _l, _p))
check("404: no speech bubble collides with a figure", not _clash, str(_clash[:4]))
check("404: no bubble runs past three lines", not _wide, str(_wide[:4]))
check("404: every strip has all five languages",
      all(sorted(_st["text"]) == sorted(_g4.LANGS) for _st in _g4.STRIPS))
check("404: every strip has three lines and three screens",
      all(len(_st["screens"]) == 3 and all(len(_st["text"][_l]) == 3 for _l in _g4.LANGS)
          for _st in _g4.STRIPS))

# a 404 must be a real page, in every language, with working root-absolute links
_404 = "404.html"
check("404 page exists", os.path.exists(_404))
if os.path.exists(_404):
    _h4 = io.open(_404, encoding="utf-8").read()
    check("404: noindex", 'content="noindex' in _h4)
    check("404: covers every language",
          all('class="l l-%s"' % l in _h4 for l in ("en", "de", "es", "nl", "fr")),
          str([l for l in ("en", "de", "es", "nl", "fr") if 'class="l l-%s"' % l not in _h4]))
    # served from any depth, so a relative link would resolve against the wrong folder
    _rel = re.findall(r'(?:href|src)="(?!https?:|/|#|mailto:|data:)([^"]+)"', _h4)
    check("404: every link is root-absolute", not _rel, str(sorted(set(_rel))[:4]))
    _tgt = re.findall(r'(?:href|src)="(/[^"#]*)"', _h4)
    _gone = [t for t in _tgt if not os.path.exists(t.lstrip("/") or "index.html")]
    check("404: every link resolves to a file", not _gone, str(sorted(set(_gone))[:4]))

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
for lang in ("de", "es", "nl", "fr"):
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
