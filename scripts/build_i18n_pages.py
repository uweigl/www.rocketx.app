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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import faq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SITE = "https://www.rocketx.app"
TMP = os.path.join(ROOT, ".build_tmp.html")

TITLE = {
 "fr": "RocketX — Plateforme de commande B2B, commerce de gros",
 "nl": "RocketX — B2B-bestelplatform voor de groothandel",
 "de": "RocketX — B2B-Bestellplattform für den Großhandel",
 "es": "RocketX — Plataforma de pedidos B2B para mayoristas",
}
DESC = {
 "fr": "Commande B2B pour le commerce de gros, 15–250\u00a0M€. Références illimitées, applications natives, panier partagé en direct. Un forfait, jamais un pourcentage.",
 "nl": "B2B-groothandelsbestellingen voor 15–250 miljoen euro omzet. Onbeperkt SKU’s, native apps, gedeelde live winkelwagen. Vast tarief, nooit een percentage.",
 "de": "B2B-Großhandelsbestellungen für 15–250 Mio.\u00a0€ Umsatz. Unbegrenzt SKUs, native Apps, gemeinsamer Live-Warenkorb. Pauschalgebühr, nie ein Prozentsatz.",
 "es": "Pedidos mayoristas B2B para distribuidores de $15–300M. SKUs ilimitados, apps nativas, carrito compartido en vivo. Tarifa fija, nunca un porcentaje.",
}
LOC = {"de": "de_DE", "es": "es_ES", "nl": "nl_NL", "fr": "fr_FR"}

# Structured data a crawler or an assistant actually quotes back. featureList
# and the offer were English on every localised page, and the offer claimed USD
# on the German and Dutch pages, which price in euro.
CURRENCY = {"de": "EUR", "es": "USD", "nl": "EUR", "fr": "EUR"}

OFFER_DESC = {
 "fr": "Forfait mensuel pour la plateforme. Jamais un pourcentage de votre chiffre d’affaires, aucun frais par référence ni par utilisateur. Mise en service offerte sur les plans annuels ; la facturation commence à la mise en service.",
 "de": "Monatliche Pauschalgebühr für die Plattform. Nie ein Prozentsatz Ihres Bestellvolumens, keine Gebühren pro SKU oder pro Nutzer. Setup bei Jahresplänen erlassen; die Abrechnung beginnt mit dem Go-live.",
 "es": "Tarifa mensual fija de plataforma. Nunca un porcentaje de tus ventas, sin tarifas por SKU ni por usuario. Implantación incluida en planes anuales; la facturación empieza en la puesta en marcha.",
 "nl": "Vast maandtarief voor het platform. Nooit een percentage van je omzet, geen kosten per SKU of per gebruiker. Inrichtingskosten kwijtgescholden bij jaarplannen; de facturatie start bij livegang.",
}

FEATURES = {
 "fr": ["Références illimitées, recherche sous la seconde",
        "Applications natives iOS et Android pour commander",
        "Paniers partagés en direct, visibles par vos commerciaux",
        "Plusieurs personnes sur le même panier en temps réel",
        "Détection des commandes en double sur tout le compte",
        "Prix et conditions propres à chaque client",
        "Stock en direct sur tous les entrepôts",
        "Intégration bidirectionnelle ERP et CRM (NetSuite, SAP, Microsoft Dynamics, Epicor)",
        "Postes et utilisateurs illimités",
        "Commander directement depuis vos PDF et catalogues existants"],
 "de": ["Unbegrenzt viele SKUs, Suche unter einer Sekunde",
        "Native iOS- und Android-Apps zum Bestellen",
        "Live-Warenkörbe, die der Außendienst sieht",
        "Mehrere Nutzer arbeiten gleichzeitig an einem Warenkorb",
        "Dublettenerkennung über das gesamte Kundenkonto",
        "Kundenspezifische Preise und Vertragskonditionen",
        "Live-Bestände über alle Lager",
        "Zwei-Wege-Integration mit ERP und CRM (NetSuite, SAP, Microsoft Dynamics, Epicor)",
        "Unbegrenzte Plätze und Nutzer",
        "Direkt aus vorhandenen PDFs und Katalogen bestellen"],
 "es": ["SKUs ilimitados con búsqueda en menos de un segundo",
        "Apps nativas de iOS y Android para pedir",
        "Carritos en vivo que los vendedores sí ven",
        "Varias personas trabajando el mismo carrito a la vez",
        "Detección de pedidos duplicados en toda la cuenta",
        "Precios y condiciones específicos por cliente",
        "Stock en tiempo real en todos los almacenes",
        "Integración bidireccional con ERP y CRM (NetSuite, SAP, Microsoft Dynamics, Epicor)",
        "Usuarios y plazas ilimitados",
        "Pedir directamente desde PDFs y catálogos existentes"],
 "nl": ["Onbeperkt SKU\u2019s, zoeken binnen een seconde",
        "Native iOS- en Android-apps om te bestellen",
        "Live winkelwagens die je buitendienst echt ziet",
        "Meerdere mensen tegelijk in dezelfde winkelwagen",
        "Dubbele orders herkennen over het hele account",
        "Klantspecifieke prijzen en contractvoorwaarden",
        "Live voorraad over alle magazijnen",
        "Tweerichtingskoppeling met ERP en CRM (NetSuite, SAP, Microsoft Dynamics, Epicor)",
        "Onbeperkt plaatsen en gebruikers",
        "Rechtstreeks bestellen vanuit bestaande pdf\u2019s en catalogi"],
}

IMG_ALT = {
 "fr": "RocketX \u2014 commander sans friction. Commande B2B pour le commerce de gros, avec références illimitées, applications natives et paniers partagés en direct.",
 "de": "RocketX \u2014 Bestellen ohne Reibung. B2B-Gro\u00dfhandelsbestellungen mit unbegrenzt vielen SKUs, nativen Apps und gemeinsamen Live-Warenk\u00f6rben.",
 "es": "RocketX \u2014 pedidos sin fricci\u00f3n. Pedidos mayoristas B2B con SKUs ilimitados, apps nativas y carritos compartidos en vivo.",
 "nl": "RocketX \u2014 bestellen zonder wrijving. B2B-groothandelsbestellingen met onbeperkt SKU\u2019s, native apps en gedeelde live winkelwagens.",
}

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
    # every JS-built asset path, not just the deck: a localised page lives one
    # level down, so an un-prefixed 'assets/... resolves to /<lang>/assets/...
    html = re.sub(r"'assets/(rocketx-[a-z-]+-)'", r"'../assets/\1'", html)
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
    html = re.sub(r'<meta property="og:image:alt" content="[^"]*"',
                  '<meta property="og:image:alt" content="%s"' % IMG_ALT[lang], html, count=1)
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
            if e.get("@type") == "SoftwareApplication":
                e["featureList"] = FEATURES[lang]
                if isinstance(e.get("offers"), dict):
                    e["offers"]["priceCurrency"] = CURRENCY[lang]
                    e["offers"]["description"] = OFFER_DESC[lang]
                    e["offers"]["url"] = "%s/%s/#pricing" % (SITE, lang)
            if e.get("@type") == "WebPage":
                e["@id"] = "%s/%s/#webpage" % (SITE, lang)
                e["url"] = "%s/%s/" % (SITE, lang)
                e["name"] = TITLE[lang]
        g["@graph"] = [e for e in g["@graph"] if e.get("@type") != "FAQPage"]
        g["@graph"].append(faq.faqpage(lang))
        html = html[:m.start()] + '<script type="application/ld+json">' + \
               json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>" + html[m.end():]
    # 4. default to this page's language instead of the visitor's locale
    html = html.replace("setLang(saved||(I18N[guess]?guess:'en'))", "setLang(saved||'%s')" % lang)
    # 5. drop the build hook
    html = re.sub(r'<script>addEventListener\("load",function\(\)\{try\{localStorage[^<]*</script>', "", html)
    html = html.replace(' data-prerendered="%s"' % lang, "")
    return html


if __name__ == "__main__":

    built = []
    for lang in ("de", "es", "nl", "fr"):
        os.makedirs(lang, exist_ok=True)
        html = fix(render(lang), lang)
        path = os.path.join(lang, "index.html")
        io.open(path, "w", encoding="utf-8").write(html)
        built.append((path, len(html)))
        print("  wrote %-16s %d bytes" % (path, len(html)))

    # sanity: the translated copy must actually be in the file
    checks = {"de": "Bestellen", "es": "sin fricción", "nl": "zonder wrijving", "fr": "sans friction"}
    for lang, needle in checks.items():
        txt = io.open(os.path.join(lang, "index.html"), encoding="utf-8").read()
        ok = needle in txt and 'lang="%s"' % lang in txt
        print("  %s: translated copy present and lang attribute set ... %s" % (lang, "yes" if ok else "NO"))
        if not ok: sys.exit(1)
    print("done")
