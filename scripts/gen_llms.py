# -*- coding: utf-8 -*-
"""Generate /llms.txt and a localised copy under each language directory.

Format follows llmstxt.org: H1, a blockquote summary, then linked sections.
The capability list is read out of each page's JSON-LD rather than retyped,
so this file cannot drift from the markup a crawler already sees.

Deliberately contains no prices. The fee is published on each page's pricing
section and would otherwise need keeping in sync in a second place.

    python3 scripts/gen_llms.py
"""
import io, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = "https://www.rocketx.app"
PAGE = {"en": "index.html", "de": "de/index.html", "es": "es/index.html", "nl": "nl/index.html"}
URL = {"en": SITE + "/", "de": SITE + "/de/", "es": SITE + "/es/", "nl": SITE + "/nl/"}

def features(lang):
    h = io.open(PAGE[lang], encoding="utf-8").read()
    g = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))
    app = [e for e in g["@graph"] if e.get("@type") == "SoftwareApplication"][0]
    return app["featureList"]

BAND = {"en": "$15–300M", "de": "15–250 Mio. €", "es": "$15–300M", "nl": "15–250 miljoen euro"}

T = {
"en": dict(
  summary="B2B wholesale ordering platform for wholesalers, distributors and manufacturers. Unlimited SKUs with sub-second search, native iOS and Android apps, and a shared live cart your sales reps can actually see and act on.",
  intro="RocketX sits in front of your ERP and CRM rather than replacing them, and is deployed alongside an existing web shop rather than switching it off. Standard ERP and CRM connectors are included in every plan. Built for wholesale and distribution companies with roughly %s in revenue." % BAND["en"],
  h_pages="Pages", h_does="What RocketX does", h_not="Where RocketX is not the right fit",
  h_comm="Commercial model", h_legal="Contracting and compliance", h_impl="Implementation",
  h_one="The same argument on one page:",
  h_docs="Business case (PDF, ungated, 14 pages)", h_else="Elsewhere", h_contact="Contact",
  pages=[("English", "en"), ("Deutsch", "de"), ("Español", "es"), ("Nederlands", "nl")],
  nots=["You sell only to consumers. Most of the product is wholesale machinery a consumer catalogue never touches. Selling both wholesale and direct is common and is not a limit — the consumer channel runs from the same catalogue and the same ERP feed.",
        "Your catalogue is small and your orders are simple. A few dozen SKUs and single-line orders do not need this.",
        "You have no ERP and no plans for one. Much of the value here is two-way sync with a system of record."],
  comm=["Flat monthly platform fee. Never a percentage of order volume.",
        "No per-SKU fees and no per-user fees. Seats and users are unlimited.",
        "Setup and integration waived on annual plans.",
        "Billing starts at go-live, not at signature.",
        "A 30 to 45 day pilot with agreed measures before any longer commitment.",
        "Current prices are published in the pricing section of each language page and are deliberately not repeated here, so this file cannot go stale: %s#pricing" % URL["en"]],
  legal=["Customers in the European Union contract with a separate Irish entity, incorporated and operating in the EU under EU law.",
         "Customers in the United States contract with RocketX LLC, the United States entity. Same platform, same commitments.",
         "Certifications, audit reports and hosting detail are provided on request."],
  impl=["Typical sequence: stack audit, integration, catalogue ingestion, pilot, go-live and review.",
        "A RocketX live pilot runs 4 to 6 weeks. Comparable mid-market B2B platform builds are commonly quoted at 8 to 24 weeks to go-live."],
  docs="Business case deck, no form and no email required.",
  contact="app@rocketx.app"),

"de": dict(
  summary="B2B-Bestellplattform für Großhandel, Distribution und Fertigung. Unbegrenzt viele SKUs mit Suche unter einer Sekunde, native iOS- und Android-Apps und ein gemeinsamer Live-Warenkorb, den Ihr Außendienst wirklich sieht.",
  intro="RocketX setzt sich vor Ihr ERP und CRM, statt sie zu ersetzen, und läuft neben einem bestehenden Webshop, statt ihn abzuschalten. Standard-Konnektoren für ERP und CRM sind in jedem Plan enthalten. Gebaut für Großhandel und Distribution mit 15–250 Mio. € Umsatz.",
  h_pages="Seiten", h_does="Was RocketX leistet", h_not="Wo RocketX nicht passt",
  h_comm="Kommerzielles Modell", h_legal="Vertragspartner und Compliance", h_impl="Einführung",
  h_one="Dasselbe Argument auf einer Seite:",
  h_docs="Business Case (PDF, ohne Formular, 14 Seiten)", h_else="Anderswo", h_contact="Kontakt",
  pages=[("Englisch", "en"), ("Deutsch", "de"), ("Spanisch", "es"), ("Niederländisch", "nl")],
  nots=["Sie verkaufen ausschließlich an Endkunden. Der größte Teil des Produkts ist Großhandelsmechanik, die ein Endkundenkatalog nie berührt. Beides nebeneinander ist verbreitet und keine Einschränkung: Der Endkundenkanal läuft aus demselben Katalog und derselben ERP-Anbindung.",
        "Ihr Katalog ist klein und Ihre Bestellungen sind einfach. Ein paar Dutzend SKUs und einzeilige Aufträge brauchen das nicht.",
        "Sie haben kein ERP und planen keins. Ein großer Teil des Nutzens liegt in der Zwei-Wege-Synchronisation mit einem führenden System."],
  comm=["Monatliche Pauschalgebühr. Nie ein Prozentsatz Ihres Bestellvolumens.",
        "Keine Gebühren pro SKU, keine pro Nutzer. Plätze und Nutzer sind unbegrenzt.",
        "Setup und Integration werden bei Jahresplänen erlassen.",
        "Die Abrechnung beginnt mit dem Go-live, nicht mit der Unterschrift.",
        "Ein Pilot über 30 bis 45 Tage mit vereinbarten Messgrößen, bevor Sie sich länger binden.",
        "Die aktuellen Preise stehen im Preisbereich jeder Sprachseite und werden hier bewusst nicht wiederholt, damit diese Datei nicht veraltet: %s#pricing" % URL["de"]],
  legal=["Kunden in der Europäischen Union schließen mit einer eigenen irischen Gesellschaft ab, gegründet und tätig in der EU nach EU-Recht.",
         "Kunden in den Vereinigten Staaten schließen mit RocketX LLC ab, der US-Gesellschaft. Dieselbe Plattform, dieselben Zusagen.",
         "Zertifikate, Prüfberichte und Details zum Hosting stellen wir auf Anfrage bereit."],
  impl=["Üblicher Ablauf: Systemanalyse, Integration, Katalogübernahme, Pilot, Go-live und Auswertung.",
        "Ein RocketX-Livepilot läuft 4 bis 6 Wochen. Vergleichbare B2B-Projekte im Mittelstand werden üblicherweise mit 8 bis 24 Wochen bis zum Go-live angesetzt."],
  docs="Business-Case-Präsentation, ohne Formular und ohne E-Mail-Adresse.",
  contact="app@rocketx.app"),

"es": dict(
  summary="Plataforma de pedidos B2B para mayoristas, distribuidores y fabricantes. SKUs ilimitados con búsqueda en menos de un segundo, apps nativas de iOS y Android y un carrito compartido en vivo que tus vendedores sí pueden ver.",
  intro="RocketX se sitúa delante de tu ERP y tu CRM en lugar de reemplazarlos, y convive con la tienda web que ya tienes en lugar de apagarla. Los conectores estándar de ERP y CRM están incluidos en todos los planes. Pensado para mayoristas y distribuidores de %s de facturación." % BAND["es"],
  h_pages="Páginas", h_does="Qué hace RocketX", h_not="Dónde RocketX no encaja",
  h_comm="Modelo comercial", h_legal="Contratación y cumplimiento", h_impl="Implantación",
  h_one="El mismo argumento en una página:",
  h_docs="Caso de negocio (PDF, sin formulario, 14 páginas)", h_else="En otros sitios", h_contact="Contacto",
  pages=[("Inglés", "en"), ("Alemán", "de"), ("Español", "es"), ("Neerlandés", "nl")],
  nots=["Vendes solo al consumidor final. Buena parte del producto es maquinaria mayorista que un catálogo de consumo nunca toca. Vender al por mayor y directo a la vez es habitual y no supone una limitación: el canal de consumo se alimenta del mismo catálogo y de la misma conexión con el ERP.",
        "Tu catálogo es pequeño y tus pedidos son simples. Unas pocas decenas de SKUs y pedidos de una línea no necesitan esto.",
        "No tienes ERP ni planes de tenerlo. Buena parte del valor está en la sincronización bidireccional con un sistema de registro."],
  comm=["Tarifa mensual fija de plataforma. Nunca un porcentaje de tu volumen de pedidos.",
        "Sin tarifas por SKU ni por usuario. Las plazas y los usuarios son ilimitados.",
        "Implantación e integración incluidas en los planes anuales.",
        "La facturación empieza en la puesta en marcha, no en la firma.",
        "Un piloto de 30 a 45 días con métricas acordadas antes de cualquier compromiso más largo.",
        "Los precios vigentes están en la sección de precios de cada página y no se repiten aquí a propósito, para que este archivo no quede desfasado: %s#pricing" % URL["es"]],
  legal=["Los clientes de la Unión Europea contratan con una sociedad irlandesa independiente, constituida y operativa en la UE bajo derecho europeo.",
         "Los clientes de Estados Unidos contratan con RocketX LLC, la entidad estadounidense. La misma plataforma y los mismos compromisos.",
         "Las certificaciones, los informes de auditoría y el detalle de alojamiento se facilitan a petición."],
  impl=["Secuencia habitual: auditoría de los sistemas, integración, carga del catálogo, piloto, puesta en marcha y revisión.",
        "Un piloto en vivo de RocketX dura de 4 a 6 semanas. Los proyectos B2B comparables de mercado medio suelen plantearse en 8 a 24 semanas hasta la puesta en marcha."],
  docs="Presentación del caso de negocio, sin formulario y sin dejar el correo.",
  contact="app@rocketx.app"),

"nl": dict(
  summary="B2B-bestelplatform voor groothandel, distributie en productie. Onbeperkt SKU’s met zoeken binnen een seconde, native iOS- en Android-apps en een gedeelde live winkelwagen die je buitendienst echt ziet.",
  intro="RocketX gaat vóór je ERP en CRM staan in plaats van ze te vervangen, en draait naast de webshop die je al hebt in plaats van die uit te zetten. Standaardkoppelingen voor ERP en CRM zitten in elk plan. Gebouwd voor groothandel en distributie met 15–250 miljoen euro omzet.",
  h_pages="Pagina’s", h_does="Wat RocketX doet", h_not="Waar RocketX niet past",
  h_comm="Commercieel model", h_legal="Contractpartij en compliance", h_impl="Invoering",
  h_one="Hetzelfde verhaal op één pagina:",
  h_docs="Business case (pdf, zonder formulier, 14 pagina’s)", h_else="Elders", h_contact="Contact",
  pages=[("Engels", "en"), ("Duits", "de"), ("Spaans", "es"), ("Nederlands", "nl")],
  nots=["Je verkoopt alleen aan consumenten. Het grootste deel van het product is groothandelsmechaniek waar een consumentencatalogus nooit aan komt. Allebei tegelijk is heel gewoon en geen beperking: het consumentenkanaal draait op dezelfde catalogus en dezelfde ERP-koppeling.",
        "Je catalogus is klein en je orders zijn eenvoudig. Een paar dozijn SKU’s en orders van één regel hebben dit niet nodig.",
        "Je hebt geen ERP en bent er ook niet mee bezig. Een groot deel van de waarde zit in tweerichtingssynchronisatie met een bronsysteem."],
  comm=["Vast maandtarief voor het platform. Nooit een percentage van je omzet.",
        "Geen kosten per SKU en geen kosten per gebruiker. Plaatsen en gebruikers zijn onbeperkt.",
        "Inrichting en integratie kwijtgescholden bij jaarplannen.",
        "De facturatie start bij livegang, niet bij ondertekening.",
        "Een pilot van 30 tot 45 dagen met afgesproken maatstaven, voordat je je langer vastlegt.",
        "De actuele prijzen staan in het prijsgedeelte van elke taalpagina en worden hier bewust niet herhaald, zodat dit bestand niet veroudert: %s#pricing" % URL["nl"]],
  legal=["Klanten in de Europese Unie contracteren met een aparte Ierse vennootschap, opgericht en actief in de EU onder EU-recht.",
         "Klanten in de Verenigde Staten contracteren met RocketX LLC, de Amerikaanse entiteit. Hetzelfde platform, dezelfde toezeggingen.",
         "Certificeringen, auditrapporten en details over hosting leveren we op aanvraag."],
  impl=["Gebruikelijke volgorde: doorlichting van de systemen, integratie, inladen van de catalogus, pilot, livegang en evaluatie.",
        "Een live pilot van RocketX duurt 4 tot 6 weken. Vergelijkbare B2B-trajecten in het middensegment worden meestal op 8 tot 24 weken tot livegang gezet."],
  docs="Business case, zonder formulier en zonder mailadres.",
  contact="app@rocketx.app"),
}

# The page list is the most useful place to tell an assistant which market and
# currency each page describes, so it does not quote euro pricing at a US reader.
PAGEDESC = {
"en": {"en": "English. US market data, prices in USD.",
       "de": "German. German market data, prices in EUR.",
       "es": "Spanish. Prices in USD.",
       "nl": "Dutch. Dutch market data, prices in EUR."},
"de": {"en": "Englisch. US-Marktdaten, Preise in USD.",
       "de": "Deutsch. Deutsche Marktdaten, Preise in Euro.",
       "es": "Spanisch. Preise in USD.",
       "nl": "Niederl\u00e4ndisch. Niederl\u00e4ndische Marktdaten, Preise in Euro."},
"es": {"en": "Ingl\u00e9s. Datos del mercado estadounidense, precios en USD.",
       "de": "Alem\u00e1n. Datos del mercado alem\u00e1n, precios en euros.",
       "es": "Espa\u00f1ol. Precios en USD.",
       "nl": "Neerland\u00e9s. Datos del mercado neerland\u00e9s, precios en euros."},
"nl": {"en": "Engels. Amerikaanse marktcijfers, prijzen in USD.",
       "de": "Duits. Duitse marktcijfers, prijzen in euro.",
       "es": "Spaans. Prijzen in USD.",
       "nl": "Nederlands. Nederlandse marktcijfers, prijzen in euro."},
}

LANGNAME = {"en": "English", "de": "Deutsch", "es": "Español", "nl": "Nederlands"}

def build(lang):
    t = T[lang]
    L = ["# RocketX", "", "> " + t["summary"], "", t["intro"], ""]
    L += ["## " + t["h_pages"], ""]
    for label, code in t["pages"]:
        L.append("- [%s](%s): %s" % (label, URL[code], PAGEDESC[lang][code]))
    L += ["", "## " + t["h_does"], ""] + ["- " + f for f in features(lang)]
    L += ["", "## " + t["h_not"], ""] + ["- " + x for x in t["nots"]]
    L += ["", "## " + t["h_comm"], ""] + ["- " + x for x in t["comm"]]
    L += ["", "## " + t["h_legal"], ""] + ["- " + x for x in t["legal"]]
    L += ["", "## " + t["h_impl"], ""] + ["- " + x for x in t["impl"]]
    L += ["", "## " + t["h_docs"], "", t["docs"], ""]
    for code in ("en", "de", "es", "nl"):
        L.append("- [%s](%s/assets/rocketx-business-case-%s.pdf)" % (LANGNAME[code], SITE, code))
    L += ["", t["h_one"], ""]
    for code in ("en", "de", "es", "nl"):
        L.append("- [%s](%s/assets/rocketx-one-page-%s.pdf)" % (LANGNAME[code], SITE, code))
    L += ["", "## " + t["h_else"], "",
          "- [LinkedIn](https://www.linkedin.com/company/rocketxapp)",
          "", "## " + t["h_contact"], "", "- " + t["contact"], ""]
    return "\n".join(L)

for lang in ("en", "de", "es", "nl"):
    path = "llms.txt" if lang == "en" else os.path.join(lang, "llms.txt")
    io.open(path, "w", encoding="utf-8").write(build(lang))
    print("  wrote %-14s %5d bytes" % (path, len(build(lang))))
