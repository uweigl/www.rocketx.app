#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-render /de/ and /es/ from index.html.

The site switches language in the browser from a JS dictionary, which means
the German and Spanish copy never exists in any HTML a crawler can read, and
there is no distinct URL for either. This renders each language to a real
page so search engines and AI crawlers can index the actual translated text.

Run from the repo root after editing index.html:

    python3 scripts/build_i18n_pages.py
"""
import io, os, re, subprocess, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "https://www.rocketx.app"
TMP = os.path.join(ROOT, ".build_tmp.html")

TITLE = {
 "nl": "RocketX — B2B-bestelplatform voor de groothandel | Onbeperkt SKU's, native apps",
 "de": "RocketX — B2B-Bestellplattform für den Großhandel | Unbegrenzt SKUs, native Apps",
 "es": "RocketX — Plataforma de pedidos B2B para mayoristas | SKUs ilimitados, apps nativas",
}
DESC = {
 "nl": "B2B-groothandelsbestellingen voor bedrijven met 15–250 miljoen euro omzet. Onbeperkt SKU's met zoeken binnen een seconde, native iOS- en Android-apps en een gedeelde live winkelwagen die je buitendienst echt kan zien. Vaste prijs, nooit een percentage van je omzet.",
 "de": "B2B-Großhandelsbestellungen für Unternehmen mit 15–250 Mio. € Umsatz. Unbegrenzt viele SKUs mit Suche unter einer Sekunde, native iOS- und Android-Apps und ein gemeinsamer Live-Warenkorb, den Ihr Außendienst wirklich sieht. Pauschalgebühr, nie ein GMV-Prozentsatz.",
 "es": "Pedidos mayoristas B2B para distribuidores de $15–300M. SKUs ilimitados con búsqueda en menos de un segundo, apps nativas de iOS y Android y un carrito compartido en vivo que tus vendedores sí pueden ver. Tarifa fija, nunca un porcentaje del GMV.",
}
LOC = {"de": "de_DE", "es": "es_ES", "nl": "nl_NL"}

def render(lang):
    """Load index.html, switch language in the browser, dump the resulting DOM."""
    src = io.open("index.html", encoding="utf-8").read()
    # force the language before the normal locale guess runs, and wait for fonts
    hook = ('<script>addEventListener("load",function(){'
            'try{localStorage.removeItem("rx-lang")}catch(e){}'
            'setLang("%s");document.documentElement.setAttribute("data-prerendered","%s");});</script>' % (lang, lang))
    io.open(TMP, "w", encoding="utf-8").write(src.replace("</body>", hook + "</body>", 1))
    out = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=12000",
         "--dump-dom", "file://" + TMP],
        capture_output=True, text=True).stdout
    os.remove(TMP)
    if 'data-prerendered="%s"' % lang not in out:
        sys.exit("render failed for %s (language never applied)" % lang)
    return out

def fix(html, lang):
    # 1. the pages live one directory down
    html = re.sub(r'(href|src)="(assets/|favicon\.ico|site\.webmanifest|sitemap\.xml)',
                  lambda m: '%s="../%s' % (m.group(1), m.group(2)), html)
    html = html.replace("'assets/rocketx-business-case-'", "'../assets/rocketx-business-case-'")
    # 2. head: language-specific title, description, canonical, og
    html = re.sub(r'<title>.*?</title>', '<title>%s</title>' % TITLE[lang], html, count=1, flags=re.S)
    html = re.sub(r'<meta name="description" content="[^"]*"',
                  '<meta name="description" content="%s"' % DESC[lang], html, count=1)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  '<link rel="canonical" href="%s/%s/"' % (SITE, lang), html, count=1)
    for prop, val in (("og:locale", LOC[lang]), ("og:url", "%s/%s/" % (SITE, lang)),
                      ("og:title", TITLE[lang]), ("og:description", DESC[lang])):
        html = re.sub(r'<meta property="%s" content="[^"]*"' % re.escape(prop),
                      '<meta property="%s" content="%s"' % (prop, val), html, count=1)
    for name, val in (("twitter:title", TITLE[lang]), ("twitter:description", DESC[lang])):
        html = re.sub(r'<meta name="%s" content="[^"]*"' % re.escape(name),
                      '<meta name="%s" content="%s"' % (name, val), html, count=1)
    # 3. JSON-LD: swap description/inLanguage/url for this language
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if m:
        g = json.loads(m.group(1))
        for e in g["@graph"]:
            if "description" in e: e["description"] = DESC[lang]
            if e.get("@type") in ("WebSite", "WebPage"): e["inLanguage"] = lang
            if e.get("@type") == "WebPage":
                e["@id"] = "%s/%s/#webpage" % (SITE, lang)
                e["url"] = "%s/%s/" % (SITE, lang)
                e["name"] = TITLE[lang]
        html = html[:m.start()] + '<script type="application/ld+json">' + \
               json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>" + html[m.end():]
    # 4. default to this page's language instead of the visitor's locale
    html = html.replace("setLang(saved||(I18N[guess]?guess:'en'))", "setLang(saved||'%s')" % lang)
    # 5. drop the build hook
    html = re.sub(r'<script>addEventListener\("load",function\(\)\{try\{localStorage[^<]*</script>', "", html)
    html = html.replace(' data-prerendered="%s"' % lang, "")
    return html

built = []
for lang in ("de", "es", "nl"):
    os.makedirs(lang, exist_ok=True)
    html = fix(render(lang), lang)
    path = os.path.join(lang, "index.html")
    io.open(path, "w", encoding="utf-8").write(html)
    built.append((path, len(html)))
    print("  wrote %-16s %d bytes" % (path, len(html)))

# sanity: the translated copy must actually be in the file
checks = {"de": "Bestellen", "es": "sin fricción", "nl": "zonder wrijving"}
for lang, needle in checks.items():
    txt = io.open(os.path.join(lang, "index.html"), encoding="utf-8").read()
    ok = needle in txt and 'lang="%s"' % lang in txt
    print("  %s: translated copy present and lang attribute set ... %s" % (lang, "yes" if ok else "NO"))
    if not ok: sys.exit(1)
print("done")
