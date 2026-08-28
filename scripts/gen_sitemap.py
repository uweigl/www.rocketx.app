#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build sitemap.xml.

It was hand-maintained, and it showed: French was appended in a different
indentation style, and a new PDF family had to be remembered in five places or
it silently went unlisted. Everything here is derived instead - languages come
from gen_404, so adding a sixth language adds its rows on its own.

lastmod is each file's own modification time rather than today's date, so
rebuilding an unchanged site does not churn every row.
"""
import datetime, io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_404 as g4

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rocketx.app"
LANGS = g4.LANGS                     # "en" is the root page, the rest are /xx/
DEFAULT = "en"

# family -> (asset stem, changefreq, priority)
PDFS = [
    ("business-case", "monthly", "0.6"),
    ("one-page",      "monthly", "0.6"),
    ("calendar",      "yearly",  "0.4"),
]


def page_path(lang):
    return "index.html" if lang == DEFAULT else "%s/index.html" % lang


def page_url(lang):
    return SITE + "/" if lang == DEFAULT else "%s/%s/" % (SITE, lang)


def pdf_path(stem, lang):
    return "assets/rocketx-%s-%s.pdf" % (stem, lang)


def pdf_url(stem, lang):
    return "%s/%s" % (SITE, pdf_path(stem, lang))


def lastmod(relpath):
    p = os.path.join(ROOT, relpath)
    ts = os.path.getmtime(p)
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")


def entry(loc, mod, alts, changefreq, priority):
    """One <url>, with every language of the same thing as an alternate."""
    rows = ["  <url>", "    <loc>%s</loc>" % loc, "    <lastmod>%s</lastmod>" % mod]
    for lang in LANGS:
        rows.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>'
                    % (lang, alts[lang]))
    rows.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s"/>'
                % alts[DEFAULT])
    rows.append("    <changefreq>%s</changefreq>" % changefreq)
    rows.append("    <priority>%s</priority>" % priority)
    rows.append("  </url>")
    return "\n".join(rows)


COMPARE = ["shopify-b2b", "pepperi", "sana-commerce"]
TRUST = {"en": "trust", "de": "de/sicherheit", "es": "es/seguridad",
         "nl": "nl/beveiliging", "fr": "fr/securite"}


def compare_entry(slug):
    loc = "%s/compare/%s/" % (SITE, slug)
    mod = lastmod("compare/%s/index.html" % slug)
    return "\n".join([
        "  <url>", "    <loc>%s</loc>" % loc, "    <lastmod>%s</lastmod>" % mod,
        "    <changefreq>monthly</changefreq>", "    <priority>0.5</priority>",
        "  </url>"])


def build():
    missing = [p for p in
               [page_path(l) for l in LANGS] +
               [pdf_path(s, l) for s, _c, _p in PDFS for l in LANGS] +
               ["compare/%s/index.html" % g for g in COMPARE]
               if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        sys.exit("sitemap: these are listed but not built: %s" % ", ".join(missing))

    out = []
    alts = dict((l, page_url(l)) for l in LANGS)
    for lang in LANGS:
        out.append(entry(page_url(lang), lastmod(page_path(lang)), alts,
                         "weekly", "1.0" if lang == DEFAULT else "0.9"))
    for stem, freq, prio in PDFS:
        palts = dict((l, pdf_url(stem, l)) for l in LANGS)
        for lang in LANGS:
            out.append(entry(pdf_url(stem, lang), lastmod(pdf_path(stem, lang)),
                             palts, freq, prio))

    for slug in COMPARE:
        out.append(compare_entry(slug))

    talts = dict((l, "%s/%s/" % (SITE, p)) for l, p in TRUST.items())
    for lang, p in TRUST.items():
        out.append(entry("%s/%s/" % (SITE, p), lastmod("%s/index.html" % p),
                         talts, "yearly", "0.5"))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(out) + "\n</urlset>\n")
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    return len(out)


if __name__ == "__main__":
    n = build()
    print("wrote sitemap.xml (%d urls: %d pages + %d pdfs)"
          % (n, len(LANGS), len(PDFS) * len(LANGS)))
