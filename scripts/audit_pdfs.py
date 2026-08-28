# -*- coding: utf-8 -*-
"""Deep audit of the fifteen PDFs against the sources that generate them.

Everything is checked in the PDFs' own extracted text - not in the HTML they
were printed from - so a stale print, a font that dropped glyphs, or a page
that silently overflowed all surface here.
"""
import io, os, re, sys, unicodedata
SP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser("~/Downloads/rocketx-site3")
sys.path.insert(0, SP)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
os.chdir(ROOT)
import pdftext, gen_deck, gen_404, gen_calendar, faq

LANGS = ["en", "de", "es", "nl", "fr"]
results = []


def norm(t):
    """Whitespace-and-apostrophe-insensitive form for matching."""
    t = unicodedata.normalize("NFKC", t)
    t = t.replace(u"ʼ", u"’").replace("'", u"’")
    t = re.sub(u"[\\s   ]+", "", t)
    return t.casefold()


def has(pages, needle, page=None):
    n = norm(needle)
    hay = pages if page is None else [pages[page]]
    return any(n in norm(p) for p in hay)


def check(name, ok, detail=""):
    results.append((name, ok, detail))


def strip_tags(t):
    import html
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


# ---------------------------------------------------------------- decks
BOTH = {"en": u"And the browser stays", "de": u"Und der Browser bleibt",
        "es": u"Y el navegador se queda", "nl": u"En de browser blijft",
        "fr": u"Et le navigateur reste"}
WEBAPP = {"en": u"web app in any browser", "de": u"Web-App in jedem Browser",
          "es": u"web app de RocketX en cualquier navegador",
          "nl": u"RocketX-webapp in elke browser",
          "fr": u"web app RocketX dans tout navigateur"}

for l in LANGS:
    pages = pdftext.extract("assets/rocketx-business-case-%s.pdf" % l)
    C = gen_deck.C[l]
    tag = "deck-%s" % l
    check("%s: 14 pages of text" % tag, len(pages) == 14 and all(len(p) > 60 for p in pages),
          "pages=%d min=%d" % (len(pages), min(len(p) for p in pages) if pages else 0))
    check("%s: names both channels, web and native" % tag,
          has(pages, BOTH[l]) and has(pages, WEBAPP[l]))
    # the cover carries the document title
    check("%s: cover title" % tag, has(pages, C["title"], 0))
    # every quest question reaches the questions page
    qmiss = [q[:36] for q in C["quest"] if not has(pages, q)]
    check("%s: all %d questions present" % (tag, len(C["quest"])), not qmiss, str(qmiss[:2]))
    # the guarantee is in the printed terms
    guar = {"en": "owing nothing", "de": "zahlen nichts", "es": "sin deber nada",
            "nl": "betaal je niets", "fr": "sans rien devoir"}[l]
    check("%s: guarantee printed" % tag, has(pages, guar))
    # compliance page names both entities
    check("%s: both entities" % tag, has(pages, "RocketX LLC") and has(pages, "RocketX Limited"))
    check("%s: EU registration printed" % tag, has(pages, "344153") and has(pages, "F35"))
    check("%s: US registration printed" % tag, has(pages, "25040687"))
    # the fee figure plots fee as a share of revenue: what prints is the band
    # boundaries and the competitor cap, not the absolute fees
    bands = gen_deck.FIGTXT[l]["fg1_bands"]
    bmiss = [str(b) for b in bands if not has(pages, str(b))]
    cap_probe = {"en": "40,000", "de": "40.000", "es": "40.000",
                 "nl": "40.000", "fr": u"40\u00a0000"}[l]
    check("%s: fee figure bands + cap" % tag,
          not bmiss and has(pages, cap_probe), "missing %s" % bmiss)
    # the cover carries the fee strip; the punchline proves all three bubbles
    _ci = gen_deck.COVER_STRIP_IDX.get(l, 2)
    check("%s: cover strip %d punchline" % (tag, _ci + 1),
          has(pages, gen_404.STRIPS[_ci]["text"][l][2], 0))
    # page 2 closes on the observed evidence
    check("%s: pilot evidence on page 2" % tag, has(pages, C["ev"], 1))
    # stats block numbers
    smiss = [a for a, b in C["stats"] if not has(pages, a)]
    check("%s: stat figures" % tag, not smiss, str(smiss))
    # source notes name the local institutions
    src_probe = {"en": "Digital Commerce 360", "de": "ECC", "es": "CEPAL",
                 "nl": "CBS", "fr": "INSEE"}[l]
    check("%s: local sources cited" % tag, has(pages, src_probe))
    # footer on the content pages
    tagline = gen_calendar.tagline(l)
    n_tag = sum(1 for p in pages if norm(tagline) in norm(p))
    check("%s: footer tagline on %d pages" % (tag, n_tag), n_tag >= 13, "%d" % n_tag)
    # nothing leaked from the template
    check("%s: no template artifacts" % tag,
          not any(x in "".join(pages) for x in ("None", "undefined", "{x}", "NaN")))

# ---------------------------------------------------------------- one-pagers
for l in LANGS:
    pages = pdftext.extract("assets/rocketx-one-page-%s.pdf" % l)
    C = gen_deck.C[l]
    tag = "one-pager-%s" % l
    check("%s: single dense page" % tag, len(pages) == 1 and len(pages[0]) > 2000,
          "pages=%d chars=%d" % (len(pages), len(pages[0]) if pages else 0))
    check("%s: names the web app beside the native apps" % tag,
          has(pages, WEBAPP[l]))
    hmiss = [h for h, _b in C["xs"] if not has(pages, h)]
    check("%s: all six row heads" % tag, not hmiss, str(hmiss[:2]))
    guar = {"en": "owing nothing", "de": "zahlen Sie nichts", "es": "no debes nada",
            "nl": "betaal je niets", "fr": "sans rien devoir"}[l]
    check("%s: guarantee printed" % tag, has(pages, guar))
    check("%s: audience line" % tag, has(pages, C["forwho"]))
    check("%s: contact present" % tag, has(pages, "app@rocketx.app"))
    check("%s: footer" % tag, has(pages, "rocketx.app"))

# ---------------------------------------------------------------- calendars
for l in LANGS:
    pages = pdftext.extract("assets/rocketx-calendar-%s.pdf" % l)
    tag = "calendar-%s" % l
    check("%s: 13 pages of text" % tag, len(pages) == 13, "pages=%d" % len(pages))
    # month i on sheet i, in order
    order_ok = all(has(pages, gen_calendar.MONTHS[l][i], i + 1) for i in range(12))
    check("%s: twelve months in order" % tag, order_ok)
    # each month carries its strip's punchline
    pmiss = [i + 1 for i in range(12)
             if not has(pages, gen_404.STRIPS[i]["text"][l][2], i + 1)]
    check("%s: each month has its strip" % tag, not pmiss, "months %s" % pmiss[:4])
    # the year on every sheet
    n_year = sum(1 for p in pages if "2027" in p)
    check("%s: year on every sheet" % tag, n_year >= 13, "%d" % n_year)
    # weekday header in this language
    check("%s: weekday row localised" % tag, has(pages, "".join(gen_calendar.WEEKDAYS[l]), 1))
    # tagline on the sheets
    tl = gen_calendar.tagline(l)
    n_tag = sum(1 for p in pages if norm(tl) in norm(p))
    check("%s: tagline on the sheets" % tag, n_tag >= 13, "%d" % n_tag)
    # February 2027 has 28 days and no 29
    feb = pages[2]
    check("%s: February has 28 days" % tag, "28" in feb and not re.search(r"\b29\b", feb))

# ---------------------------------------------------------------- report
fails = [(n, d) for n, ok, d in results if not ok]
print("PDF AUDIT: %d checks, %d failed" % (len(results), len(fails)))
for n, ok, d in results:
    if not ok:
        print("  FAIL  %-46s %s" % (n, d))
if not fails:
    print("  all passed")
else:
    sys.exit(1)
