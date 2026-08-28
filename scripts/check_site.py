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
import html as _html
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
# keys the scripts read straight out of I18N, with no DOM attribute
USED |= set(re.findall(r"I18N\[[^\]]+\]\['([\w.]+)'\]", S))
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
        # the nav link points at the questions section; its label must be the
        # word that section's own kicker uses, or the pairing reads as broken
        nav = _I[_l]["nav.questions"].strip().lower()
        kick = _I[_l]["fq.k"].replace("/", "").strip().lower()
        check("%s: nav label names the questions section" % _l, nav in kick.split(),
              "%r not a word of %r" % (nav, kick))
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
# the calculator carries the same bands and fees as the deck's fee figure
    _ch = io.open("index.html", encoding="utf-8").read()
    _m = re.search(r"const CALC=\{(.*?)\};", _ch, re.S)
    check("calculator config present", bool(_m))
    if _m:
        for _l in ("en", "de", "es", "nl", "fr"):
            _mm = re.search(r"%s:\{b:\[([\d,]+)\],f:\[([\d,]+)\]\}" % _l, _m.group(1))
            _ok = bool(_mm)
            if _mm:
                import gen_deck as _gdc
                _b = [int(x) for x in _mm.group(1).split(",")]
                _f = [int(x) for x in _mm.group(2).split(",")]
                _ok = (_b == list(_gdc.FIGTXT[_l]["fg1_bands"])
                       and _f == list(_gdc.FIGTXT[_l]["fg1_fees"]))
            check("%s: calculator matches the fee figure" % _l, _ok)
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
        # the visible questions section must say what the JSON-LD says
        _blk = _I[lang] if lang in _I else None
        if _blk is not None:
            _vis_q = [_blk.get("fq.q%d" % i) for i in range(len(deck_q))]
            _vis_a = [re.sub(r"<[^>]+>", "", _blk.get("fq.a%d" % i, ""))
                      for i in range(len(deck_q))]
            check("%s: visible questions match the deck" % lang,
                  _vis_q == deck_q, "first drift: %s" %
                  next((q for q, d in zip(_vis_q, deck_q) if q != d), "?"))
            check("%s: visible answers match the FAQ source" % lang,
                  _vis_a == [re.sub(r"<[^>]+>", "", a) for a in _faq.A[lang]])
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
        # typography: one apostrophe form, and each language's own quotation marks
        _ap = [k for k, v in _S.items()
               if re.search(u"[A-Za-z\u00c0-\u00ff]'[A-Za-z\u00c0-\u00ff]",
                            _html.unescape(v))]
        check("%s: apostrophes are typographic" % _l, not _ap, str(sorted(_ap)[:4]))
        _QUOTES = {"de": (u"\u201e", u"\u201c"), "es": (u"\u00ab", u"\u00bb"),
                   "nl": (u"\u201e", u"\u201d"), "fr": (u"\u00ab", u"\u00bb")}
        _op, _cl = _QUOTES[_l]
        _bad = []
        for k, v in _S.items():
            for ch in re.findall(u"[\u201c\u201d\u201e\u00ab\u00bb\"]",
                                 _html.unescape(v)):
                if ch not in (_op, _cl):
                    _bad.append(k)
        check("%s: quotation marks follow the local convention" % _l, not _bad,
              str(sorted(set(_bad))[:4]))
        # each localisation argues from its own market
        _FOREIGN = {"de": u"Digital Commerce 360|Dept\\. of Commerce|INSEE|FEVAD|CBS",
                    "es": u"Digital Commerce 360|Depto\\. de Comercio|Departamento de Comercio|INSEE|FEVAD|CBS|ECC",
                    "nl": u"Digital Commerce 360|Dept\\. of Commerce|INSEE|FEVAD|ECC",
                    "fr": u"Digital Commerce 360|Dept\\. of Commerce|CBS|ECC"}
        _src = " ".join(v for k, v in _S.items() if k.endswith(("src", "/src")))
        _for = re.findall(_FOREIGN[_l], _src)
        check("%s: market sources are local to this audience" % _l, not _for,
              str(sorted(set(_for))[:4]))

    # the deck's pilot evidence must state the same observation as the site,
    # or the two documents testify differently about the same pilots
    _HALF = {"en": "half the time", "de": "halben Zeit",
             "es": "mitad del tiempo", "nl": "helft van de tijd",
             "fr": u"moiti\u00e9 moins de temps"}
    for _l, _frag in _HALF.items():
        _site_p = re.sub(r"<[^>]+>", "", _I[_l].get("rs.p1", ""))
        _deck_e = _gd.C[_l].get("ev", "")
        check("%s: pilot claim identical on site and deck" % _l,
              _frag.lower() in _site_p.lower() and _frag.lower() in _deck_e.lower(),
              "site=%s deck=%s" % (_frag.lower() in _site_p.lower(),
                                   _frag.lower() in _deck_e.lower()))

    # the guarantee is a claim of record: once named, every surface that talks
    # money must carry it, or one document quietly promises less than another
    _GUAR = {"en": r"ow(?:e|ing) nothing", "de": r"zahlen (?:Sie )?nichts",
             "es": r"no debes nada|sin deber nada", "nl": r"betaal je niets",
             "fr": r"sans rien devoir|ne devez rien"}
    import faq as _fq2
    for _l, _rx in _GUAR.items():
        _surf = {
            "site": re.sub(r"<[^>]+>", "", _I[_l]["pm.p"]) + " " + _I[_l]["pm.l4"],
            "faq": _fq2.A[_l][9],
            "deck-terms": " ".join(x for r in _gd.C[_l]["terms"] for x in r),
            "deck-evidence": _gd.C[_l].get("ev", ""),
            "one-pager": _gd.C[_l]["xs"][5][1],
        }
        _missing = [k for k, v in _surf.items() if not re.search(_rx, v)]
        check("%s: the guarantee is named on every money surface" % _l,
              not _missing, str(_missing))
    # the footer tagline is the deck footer's middle segment; one text, everywhere
    import gen_calendar as _gcal
    for _l in ("en", "de", "es", "nl", "fr"):
        check("%s: footer tagline matches the document footer" % _l,
              _I[_l].get("ft.tag") == _gcal.tagline(_l),
              "%r vs %r" % (_I[_l].get("ft.tag"), _gcal.tagline(_l)))

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
import gen_calendar as _gc
# every document family signs off with the footer the deck established
for _l in _g4.LANGS:
    _ch = "deck/rocketx-calendar-%s.html" % _l
    if os.path.exists(_ch):
        _tag = _gc.tagline(_l)
        _src = io.open(_ch, encoding="utf-8").read()
        check("%s: calendar footer matches the document footer" % _l,
              _src.count(_tag) >= 13, "%d of 13 sheets" % _src.count(_tag))
check("calendar: twelve strips available for twelve months", len(_g4.STRIPS) >= 12,
      "%d strips" % len(_g4.STRIPS))
for _l in _g4.LANGS:
    _cp = "assets/rocketx-calendar-%s.pdf" % _l
    check("%s: calendar exists" % _l, os.path.exists(_cp))
    if os.path.exists(_cp):
        _n = len(re.findall(rb"/Type\s*/Page[^s]", io.open(_cp, "rb").read()))
        # a cover plus one sheet per month; a short file means a month was dropped
        check("%s: calendar is 13 pages" % _l, _n == 13, "%d pages" % _n)
    _ch = "deck/rocketx-calendar-%s.html" % _l
    if os.path.exists(_ch):
        _src = io.open(_ch, encoding="utf-8").read()
        check("%s: calendar has twelve month sheets" % _l,
              _src.count('<section class="page">') == 12,
              "%d sheets" % _src.count('<section class="page">'))
        # every month must carry a different strip: take the opening line of each
        # month sheet, not every bubble on it
        _sheets = _src.split('<section class="page">')[1:]
        _opens = []
        for _sh in _sheets:
            _m = re.search(r"<text[^>]*>([^<]*)</text>", _sh)
            if _m:
                _opens.append(_m.group(1))
        check("%s: twelve months, twelve different strips" % _l,
              len(_opens) == 12 and len(set(_opens)) == 12,
              "%d sheets, %d distinct" % (len(_opens), len(set(_opens))))
    if os.path.exists("404.html"):
        check("%s: calendar linked from the 404" % _l,
              "rocketx-calendar-%s.pdf" % _l in io.open("404.html", encoding="utf-8").read())
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

# the Worker publishes its assets directory verbatim, so anything left in the
# repository root is served: .git included, which makes the history cloneable
_AI = ".assetsignore"
check("assetsignore exists", os.path.exists(_AI))
if os.path.exists(_AI):
    import fnmatch
    _pats = [l.strip() for l in io.open(_AI, encoding="utf-8")
             if l.strip() and not l.startswith("#")]
    for _must in (".git", "scripts", "deck", "assets/_originals"):
        check("assetsignore withholds %s" % _must, _must in _pats)

    def _ignored(rel):
        parts = rel.split(os.sep)
        return any(p in parts or fnmatch.fnmatch(rel, p)
                   or rel.startswith(p + os.sep) or rel == p for p in _pats)

    # nothing the site actually serves may be caught by those patterns
    _needed = ["index.html", "404.html", "robots.txt", "sitemap.xml", "llms.txt",
               "favicon.ico", "site.webmanifest"]
    _needed += ["%s/index.html" % l for l in ("de", "es", "nl", "fr")]
    _needed += ["%s/llms.txt" % l for l in ("de", "es", "nl", "fr")]
    _needed += [p.replace("https://www.rocketx.app/", "")
                for p in re.findall(r"<loc>(https://www\.rocketx\.app/[^<]*\.pdf)</loc>",
                                    io.open("sitemap.xml", encoding="utf-8").read())]
    _lost = [n for n in _needed if _ignored(n)]
    check("assetsignore keeps everything the site serves", not _lost, str(_lost[:4]))

# fonts are self-hosted on every public surface; a Google Fonts request
# reappearing is the exact pattern German counsel warns about
import gen_legal as _gl
import gen_compare as _gc0
_public = (["index.html", "404.html"]
           + ["%s/index.html" % l for l in ("de", "es", "nl", "fr")]
           + ["%s/%s/index.html" % (_gc0.PREFIX[_l0], _s0)
              for _l0 in _gc0.SETS for _s0 in _gc0.SETS[_l0]]
           + ["%s/index.html" % p for p in _gl.PATHS.values()])
_gf = [p for p in _public if os.path.exists(p)
       and "fonts.googleapis" in io.open(p, encoding="utf-8").read()]
check("no public page calls Google Fonts", not _gf, str(_gf[:3]))
import glob as _glob
_ff = _glob.glob("assets/fonts/*.woff2")
check("self-hosted font files present", len(_ff) >= 8, "%d files" % len(_ff))

# privacy: one page per market, linked, noindex, and its claims match reality
for _l, _pp in _gl.PATHS.items():
    _f = "%s/index.html" % _pp
    check("privacy page %s exists" % _l, os.path.exists(_f))
    if os.path.exists(_f):
        _h = io.open(_f, encoding="utf-8").read()
        check("privacy %s is noindex" % _l, "noindex" in _h)
        check("privacy %s names the processor" % _l, "Cloudflare" in _h)
        check("privacy %s no longer claims a contact form" % _l,
              "MailerSend" not in _h)
# the Impressum: present, current legal basis, correct representative
_imp = "de/impressum/index.html"
check("impressum exists", os.path.exists(_imp))
if os.path.exists(_imp):
    _hi = io.open(_imp, encoding="utf-8").read()
    check("impressum names the representative", "Urban Weigl" in _hi)
    check("impressum cites the DDG, not the repealed TMG",
          "DDG" in _hi and "TMG" not in _hi)
    check("impressum offers two fast contact channels",
          "app@rocketx.app" in _hi and "Telefon: 015678 / 191538" in _hi)
# mentions légales: present, phone, publication director, host — LCEN wants all
_ml = "fr/mentions-legales/index.html"
check("mentions legales exist", os.path.exists(_ml))
if os.path.exists(_ml):
    _hm = io.open(_ml, encoding="utf-8").read()
    check("mentions name the publication director", "Urban Weigl" in _hm)
    check("mentions carry a phone number", "191538" in _hm)
    check("mentions name the host with address", "Cloudflare" in _hm and "Townsend" in _hm)
    check("mentions carry the EU entity registration", "344153" in _hm)
check("impressum carries phone and EU entity",
      os.path.exists(_imp) and "191538" in io.open(_imp, encoding="utf-8").read()
      and "344153" in io.open(_imp, encoding="utf-8").read())
_idx2 = io.open("index.html", encoding="utf-8").read()
# the German WhatsApp contact: correct wa.me digits, gated to /de/, and the
# German privacy page discloses the channel it advertises
check("whatsapp numbers per market are wired",
      "wa.me/18294997677" in _idx2 and "wa.me/4986774099628" in _idx2
      and "08677 / 4099628" in _idx2 and "(829) 499-7677" in _idx2)
check("whatsapp hidden where only email is offered",
      "WACFG" in _idx2 and "e.hidden=!c" in _idx2)
_ep = "privacy/index.html"
check("english privacy discloses whatsapp",
      os.path.exists(_ep) and "499-7677" in io.open(_ep, encoding="utf-8").read())
_dp = "de/datenschutz/index.html"
check("german privacy discloses whatsapp",
      os.path.exists(_dp) and "4099628" in io.open(_dp, encoding="utf-8").read())
# the trust page is the deck's compliance page in web form: derived, not
# retyped, so the two cannot testify differently
import gen_trust as _gt
for _l, _tp in _gt.PATHS.items():
    _tf = "%s/index.html" % _tp
    check("trust page %s exists" % _l, os.path.exists(_tf))
    if os.path.exists(_tf):
        _th = io.open(_tf, encoding="utf-8").read()
        check("trust %s is indexable" % _l, "noindex" not in _th)
        _resid = _gd.C[_l]["eu"][1][1][:60]
        check("trust %s carries the deck's residency claim" % _l, _resid in _th,
              _resid[:40])
        check("trust %s invents no certification for RocketX itself" % _l,
              "SOC 2" not in _th and "SOC2" not in _th)
        check("trust %s maps Part 11 without claiming compliance" % _l,
              ("21 CFR" in _th) and not re.search(
                  r"Part\s*11[- ]?(compliant|konform|conforme|compatibel)", _th, re.I))
        check("trust %s carries the contract checklist" % _l,
              _gd.C[_l]["at"][0] in _th)
check("trust linked from the footer", "data-trust" in _idx2 and "ft.trust" in _idx2)
# the footer strip links every single section of the homepage, and each label
# is that section's own kicker minus the slash - checked both ways
_mainseg = _idx2[_idx2.index("<main"):_idx2.index("</main>")]
_secids = re.findall(r'<section[^>]*id="([\w-]+)"', _mainseg)
_footseg = re.search(r'<footer class="site">.*?</footer>', _idx2, re.S).group(0)
_unlinked = [i for i in _secids if ('href="#%s"' % i) not in _footseg]
check("footer strip links every homepage section", not _unlinked, str(_unlinked))
_KICK = {"demo": "demo.k", "features": "ft.k", "market": "mk.k", "native": "na.k",
         "results": "rs.k", "compare": "cp.k", "insights": "in.k",
         "pricing": "pr.k", "questions": "fq.k", "liftoff": "ln.k"}
for _l in ("en", "de", "es", "nl", "fr"):
    _drift = [sid for sid, kk in _KICK.items()
              if (D[_l].get("fmap.%s" % sid) or "").casefold()
              != re.sub(r"^/\s*", "", D[_l].get(kk, "")).strip().casefold()]
    check("%s: footer strip labels match the section kickers" % _l,
          not _drift, str(_drift))
check("privacy linked from the footer", "data-privacy" in _idx2 and "ft.privacy" in _idx2)
# the page promises no analytics; hold the site to it
check("site carries no analytics, as the privacy page promises",
      not re.search(r"gtag|googletagmanager|plausible|matomo|fathom|hotjar", _idx2))

# the comparison pages: localized per market, sourced, honest. The closing
# pilot sentence must carry each language's approved guarantee clause, the
# same words the homepage uses in pm.p.
import gen_compare as _gc2
_GUARC = {"en": "walk away owing nothing", "de": "gehen Sie und zahlen nichts",
          "es": "te vas sin deber nada", "nl": "stap je eruit en betaal je niets",
          "fr": "vous partez sans rien devoir"}
for _cl in ("en", "de", "es", "nl", "fr"):
    for _slug in _gc2.SETS[_cl]:
        _cp = "%s/%s/index.html" % (_gc2.PREFIX[_cl], _slug)
        check("%s/%s exists" % (_gc2.PREFIX[_cl], _slug), os.path.exists(_cp))
        if not os.path.exists(_cp):
            continue
        _h = io.open(_cp, encoding="utf-8").read()
        _ext = len(set(re.findall(r'href="(https?://(?!www\.rocketx\.app)[^"]+)"', _h)))
        check("%s/%s cites at least 3 external sources" % (_gc2.PREFIX[_cl], _slug),
              _ext >= 3, "%d" % _ext)
        check("%s/%s says who the competitor is right for" % (_gc2.PREFIX[_cl], _slug),
              "data-fair" in _h)
        check("%s/%s closes on the approved guarantee clause" % (_gc2.PREFIX[_cl], _slug),
              _GUARC[_cl] in _h)
        check("%s/%s highlights the RocketX edge" % (_gc2.PREFIX[_cl], _slug),
              _h.count('<ul class="edge">') == 1
              and _h.split('<ul class="edge">', 1)[1].split("</ul>", 1)[0].count("<li>") == 7)
        check("%s/%s links home in its own language" % (_gc2.PREFIX[_cl], _slug),
              ('href="/#compare"' if _cl == "en" else 'href="/%s/#compare"' % _cl) in _h)
_idx = io.open("index.html", encoding="utf-8").read()
check("comparison section links the English set, root-absolute",
      all(('href="/compare/%s/"' % _s2) in _idx for _s2 in _gc2.SETS["en"]))
check("CMPCFG carries every language's own comparison set",
      all(("/%s/%s/" % (_gc2.PREFIX[_cl2], _sl2)) in _idx
          for _cl2 in _gc2.SETS for _sl2 in _gc2.SETS[_cl2]))
# the prerendered pages must link their own market's comparisons
for _cl in ("de", "es", "nl", "fr"):
    if os.path.exists("%s/index.html" % _cl):
        _lh = io.open("%s/index.html" % _cl, encoding="utf-8").read()
        check("/%s/ links its own localized comparisons" % _cl,
              all(('href="/%s/%s/"' % (_gc2.PREFIX[_cl], _sl)) in _lh
                  for _sl in _gc2.SETS[_cl]))
# a relative compare link 404s from /de/ and the other language folders
check("no relative compare links anywhere on the page",
      'href="compare/' not in _idx)

# the contact path: CTAs are prefilled mailto links again (dialog retired
# for now, worker kept for when it returns)
check("contact CTAs are prefilled mailto links",
      re.search(r'data-mailto="quote" href="mailto:app@rocketx\.app\?subject=', _idx)
      and re.search(r'data-mailto="demo" href="mailto:app@rocketx\.app\?subject=', _idx))
check("contact dialog stays retired", "cdlg" not in _idx)
_w = io.open("worker.js", encoding="utf-8").read() if os.path.exists("worker.js") else ""
check("worker handles /api/contact", '"/api/contact"' in _w and "handleContact" in _w)
check("worker falls through to assets", "env.ASSETS.fetch" in _w)
_wc = io.open("wrangler.jsonc", encoding="utf-8").read()
check("wrangler config wires worker + assets binding",
      '"main": "worker.js"' in _wc and '"binding": "ASSETS"' in _wc)

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
    # the sitemap is generated from these lists, so a new language or a new PDF
    # family lands in it automatically - this catches it having been edited away
    import gen_sitemap as _gs
    _locs = set(re.findall(r"<loc>([^<]+)</loc>",
                           io.open("sitemap.xml", encoding="utf-8").read()))
    _want = set([_gs.page_url(_l) for _l in _gs.LANGS] +
                [_gs.pdf_url(_st, _l) for _st, _c, _p in _gs.PDFS for _l in _gs.LANGS] +
                list(_gs.COMPARE_URLS) +
                ["%s/%s/" % (_gs.SITE, _p) for _p in _gs.TRUST.values()])
    check("sitemap lists every page and pdf in every language", not (_want - _locs),
          str(sorted(_want - _locs)[:4]))
    check("sitemap lists nothing that is not built", not (_locs - _want),
          str(sorted(_locs - _want)[:4]))
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
