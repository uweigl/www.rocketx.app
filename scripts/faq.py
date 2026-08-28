# -*- coding: utf-8 -*-
"""FAQPage structured data.

The questions are the ones the deck tells a buyer to put to any vendor, read
straight out of gen_deck so the two cannot diverge. The answers live here.

Every answer is grounded in something the site or the deck already states.
Note this is for machine extraction rather than Google rich results: Google
restricted FAQ rich results to government and health sites in 2023.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_deck

A = {
"en": [
 "No. The platform fee is a flat monthly amount and never a percentage of your order volume. There are no per-SKU fees and no per-user fees. Plans are banded by company revenue, not by how busy a given month was.",
 "Yes. Your reps see carts live as they are built: what is in them, what has stalled, what has sat idle for days. They can add the missing line, correct a quantity, or call before it goes cold.",
 "Yes. Carts persist server-side and sync in real time across the web shop and the native apps. Nothing depends on a browser session staying alive.",
 "Yes. Several people work the same cart at once, and every change is attributed and timestamped.",
 "Yes. The cart checks what the account already bought and flags a recent duplicate before the order is submitted, showing who ordered it, how many, and when it arrived.",
 "No. Seats and users are unlimited on every plan. There are no per-user charges for employees, field reps, or authorised staff at your customers.",
 "Search stays under a second whether the catalogue runs to hundreds of SKUs or millions. It is measured on your own catalogue during the pilot, not on a demo set.",
 "Native iOS and Android, purpose-built for B2B ordering rather than a website wrapped in a shell. Barcode scanning and offline access are included.",
 "Yes. The catalogue, pricing, cart, and your brochures and product video are held locally and sync when the connection returns.",
 "At go-live. Setup and integration are waived on annual plans, and a 30 to 45 day pilot with agreed measures comes before any longer commitment. If the pilot misses those measures, you walk away owing nothing.",
],
"fr": [
 "Non. Le coût de la plateforme est un forfait mensuel, jamais un pourcentage de votre chiffre d’affaires. Il n’y a ni frais par référence, ni frais par utilisateur. Les paliers suivent le chiffre d’affaires de l’entreprise, pas l’intensité d’un mois donné.",
 "Oui. Vos commerciaux voient les paniers se construire en direct : ce qu’ils contiennent, ce qui bloque, ce qui dort depuis plusieurs jours. Ils ajoutent la ligne manquante, corrigent une quantité ou décrochent le téléphone avant que l’affaire refroidisse.",
 "Oui. Les paniers vivent sur le serveur et se synchronisent en temps réel entre la boutique en ligne et les applications natives. Rien ne dépend d’une session de navigateur restée ouverte.",
 "Oui. Plusieurs personnes travaillent le même panier en même temps, et chaque modification porte un nom et une heure.",
 "Oui. Le panier vérifie ce que le compte a déjà acheté et signale un doublon récent avant l’envoi de la commande : qui a commandé, combien, quand la marchandise est arrivée.",
 "Non. Les postes et les utilisateurs sont illimités dans tous les plans. Aucun frais par utilisateur pour vos salariés, vos commerciaux itinérants ou le personnel autorisé de vos clients.",
 "La recherche reste sous la seconde, que le catalogue compte quelques centaines de références ou plusieurs millions. Elle est mesurée sur votre propre catalogue pendant le pilote, pas sur un jeu de démonstration.",
 "Natives iOS et Android, conçues pour la commande B2B plutôt qu’un site web enfermé dans une coque. Lecture de code-barres et accès hors connexion compris.",
 "Oui. Le catalogue, les prix, le panier ainsi que vos brochures et vidéos produit sont conservés en local et se synchronisent au retour de la connexion.",
 "À la mise en service. Les frais de mise en service et d’intégration sont offerts sur les plans annuels, et un pilote de 30 à 45 jours avec des mesures convenues précède tout engagement plus long. S’il manque ces mesures, vous partez sans rien devoir.",
],
"de": [
 "Nein. Die Plattformgebühr ist eine monatliche Pauschale und nie ein Prozentsatz Ihres Bestellvolumens. Es gibt keine Gebühren pro SKU und keine pro Nutzer. Die Stufen richten sich nach dem Unternehmensumsatz, nicht danach, wie stark ein einzelner Monat ausfällt.",
 "Ja. Ihr Außendienst sieht Warenkörbe live beim Entstehen: was darin liegt, was stockt, was seit Tagen unberührt ist. Er ergänzt die fehlende Position, korrigiert die Menge oder greift zum Telefon, bevor die Sache kalt wird.",
 "Ja. Warenkörbe liegen auf dem Server und synchronisieren in Echtzeit zwischen Webshop und nativen Apps. Nichts hängt davon ab, dass eine Browser-Sitzung am Leben bleibt.",
 "Ja. Mehrere Personen arbeiten gleichzeitig am selben Warenkorb. Jede Änderung trägt Name und Zeitstempel.",
 "Ja. Der Warenkorb weiß, was das Konto bereits gekauft hat. Vor dem Absenden meldet er jede kürzliche Dopplung: wer bestellt hat, wie viel, wann geliefert wurde.",
 "Nein. Plätze und Nutzer sind in jedem Plan unbegrenzt. Für Mitarbeiter, Außendienst und autorisierte Mitarbeiter Ihrer Kunden fallen keine Nutzergebühren an.",
 "Die Suche bleibt unter einer Sekunde, ob der Katalog einige hundert SKUs umfasst oder Millionen. Der Pilot misst an Ihrem echten Katalog, nicht an einem Demo-Datensatz.",
 "Nativ für iOS und Android, gebaut für B2B-Bestellungen statt einer Website in einer App-Hülle. Barcode-Scan und Offline-Zugriff sind enthalten.",
 "Ja. Katalog, Preise, Warenkorb sowie Ihre Broschüren und Produktvideos liegen lokal und synchronisieren, sobald die Verbindung zurück ist.",
 "Mit dem Go-live. Bei Jahresplänen zahlen Sie für Setup und Integration nichts. Und vor einer längeren Bindung läuft ein Pilot: 30 bis 45 Tage, mit vereinbarten Messgrößen. Verfehlt er sie, gehen Sie und zahlen nichts.",
],
"es": [
 "No. La tarifa de plataforma es mensual y fija, y nunca un porcentaje de tu volumen de pedidos. No hay tarifas por SKU ni por usuario. Los tramos van por facturación de la empresa, no por lo movido que haya sido un mes.",
 "Sí. Tus vendedores ven los carritos en vivo mientras nacen: qué llevan dentro, qué se ha atascado, qué lleva días quieto. Pueden añadir la línea que falta, corregir una cantidad o descolgar el teléfono antes de que se enfríe.",
 "Sí. Los carritos se guardan en el servidor y se sincronizan en tiempo real entre la tienda web y las apps nativas. Nada depende de que una sesión del navegador siga viva.",
 "Sí. Varias personas trabajan el mismo carrito a la vez, y cada cambio queda con nombre y hora.",
 "Sí. El carrito comprueba lo que la cuenta ya compró y avisa de un duplicado reciente antes de enviar el pedido: quién lo pidió, cuánto y cuándo llegó.",
 "No. Las plazas y los usuarios son ilimitados en todos los planes. No se cobra por empleados, vendedores ni personal autorizado de tus clientes.",
 "La búsqueda se mantiene por debajo del segundo, tanto si el catálogo tiene cientos de SKUs como millones. Se mide sobre tu catálogo real durante el piloto, no sobre uno de demostración.",
 "Nativas para iOS y Android, construidas para el pedido B2B y no un sitio web dentro de una carcasa. Incluyen escaneo de códigos y acceso sin conexión.",
 "Sí. El catálogo, los precios, el carrito y tus folletos y vídeos de producto quedan en local y se sincronizan al volver la conexión.",
 "En la puesta en marcha. La implantación y la integración están incluidas en los planes anuales, y antes de cualquier compromiso largo hay un piloto de 30 a 45 días con métricas acordadas. Si no las alcanza, te vas sin deber nada.",
],
"nl": [
 "Nee. De platformkosten zijn een vast maandbedrag en nooit een percentage van je omzet. Er zijn geen kosten per SKU en geen kosten per gebruiker. De schijven gaan op bedrijfsomzet, niet op hoe druk een maand toevallig was.",
 "Ja. Je buitendienst ziet winkelwagens live ontstaan: wat erin ligt, wat vastloopt, wat al dagen stilstaat. Ze zetten de juiste regel erbij, corrigeren een aantal of bellen, voordat het afkoelt.",
 "Ja. Winkelwagens staan op de server en synchroniseren live tussen de webshop en de native apps. Niets hangt af van een browsersessie die in leven blijft.",
 "Ja. Meerdere mensen werken tegelijk in dezelfde winkelwagen. Elke wijziging staat op naam en met tijdstempel.",
 "Ja. De winkelwagen kijkt wat het account al gekocht heeft en meldt een recente dubbele bestelling vóór het verzenden: wie, hoeveel en wanneer geleverd.",
 "Nee. Plaatsen en gebruikers zijn onbeperkt in elk plan. Er wordt niets gerekend voor medewerkers, buitendienst of gemachtigde mensen bij je klant.",
 "Zoeken blijft onder de seconde, of de catalogus nu honderden SKU’s telt of miljoenen. Het wordt gemeten op je eigen catalogus tijdens de pilot, niet op een demoset.",
 "Native voor iOS en Android, gebouwd voor B2B-bestellen en geen website in een omhulsel. Barcodes scannen en toegang zonder verbinding zitten erbij.",
 "Ja. Catalogus, prijzen, winkelwagen en je brochures en productvideo’s staan lokaal en synchroniseren zodra de verbinding terug is.",
 "Bij livegang. Inrichting en integratie zijn kwijtgescholden bij jaarplannen, en vóór een langere verbintenis staat een pilot van 30 tot 45 dagen met afgesproken maatstaven. Haalt de pilot ze niet, dan stap je eruit en betaal je niets.",
],
}
SITE = "https://www.rocketx.app"

def questions(lang):
    return list(gen_deck.C[lang]["quest"])

def faqpage(lang):
    qs, ans = questions(lang), A[lang]
    if len(qs) != len(ans):
        raise SystemExit("faq %s: %d questions but %d answers" % (lang, len(qs), len(ans)))
    url = SITE + "/" if lang == "en" else "%s/%s/" % (SITE, lang)
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "inLanguage": lang,
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in zip(qs, ans)
        ],
    }

def inject_en(path=None):
    """Refresh the English FAQPage inside index.html.

    The localised pages rebuild this node from faqpage(lang) every time, but the
    English one sat static in index.html, so a reworded deck question drifted
    out of the markup and only the check noticed. Serialised exactly as
    build_i18n_pages does, so the two cannot disagree on formatting either.
    """
    import json, re, io as _io, os as _os
    path = path or _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "index.html")
    html = _io.open(path, encoding="utf-8").read()
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    if not m:
        raise SystemExit("faq: no JSON-LD block in %s" % path)
    g = json.loads(m.group(1))
    before = [e for e in g["@graph"] if e.get("@type") == "FAQPage"]
    g["@graph"] = [e for e in g["@graph"] if e.get("@type") != "FAQPage"]
    g["@graph"].append(faqpage("en"))
    out = ('<script type="application/ld+json">'
           + json.dumps(g, ensure_ascii=False, separators=(",", ":")) + "</script>")
    new_html = html[:m.start()] + out + html[m.end():]
    changed = new_html != html
    if changed:
        _io.open(path, "w", encoding="utf-8").write(new_html)
    return changed, bool(before)



def inject_visible(path=None):
    """Write the visible section's dialogue into I18N, every language.

    The markup in index.html carries data-i18n="fq.qN"/"fq.aN" hooks; the words
    come from here - questions from the deck, answers from A - so the on-page
    section, the JSON-LD and the deck cannot say different things.
    """
    import re, io as _io, os as _os
    path = path or _os.path.join(
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "index.html")
    s = _io.open(path, encoding="utf-8").read()

    def lang_span(t, lang):
        st = re.search(r"const I18N=\{", t).end()
        tag = '"%s": {' % lang
        a = t.index(tag, st)
        d, j = 0, a + len(tag) - 1
        while True:
            if t[j] == "{":
                d += 1
            elif t[j] == "}":
                d -= 1
                if d == 0:
                    return a, j
            j += 1

    def esc(v):
        return v.replace("\\", "\\\\").replace('"', '\\"')

    changed = 0
    for lang in sorted(A):
        qs, ans = questions(lang), A[lang]
        kv = {}
        for i in range(len(ans)):
            kv["fq.q%d" % i] = qs[i]
            kv["fq.a%d" % i] = ans[i]
        a, b = lang_span(s, lang)
        seg = s[a:b]
        for k, v in kv.items():
            m = re.search(r'("%s": ")((?:[^"\\]|\\.)*)(")' % re.escape(k), seg)
            if m:
                if m.group(2) != esc(v):
                    seg = seg[:m.start()] + m.group(1) + esc(v) + m.group(3) + seg[m.end():]
                    changed += 1
            else:
                tag = '"%s": {' % lang
                i2 = seg.index(tag) + len(tag)
                seg = seg[:i2] + '"%s": "%s", ' % (k, esc(v)) + seg[i2:]
                changed += 1
        s = s[:a] + seg + s[b:]
    if changed:
        _io.open(path, "w", encoding="utf-8").write(s)
    return changed


if __name__ == "__main__":
    for l in LANGS if "LANGS" in dir() else ("en", "de", "es", "nl", "fr"):
        f = faqpage(l)
        print("  %s: %d Q&A, first = %s"
              % (l, len(f["mainEntity"]), f["mainEntity"][0]["name"][:62]))
    changed, had = inject_en()
    print("  index.html FAQPage: %s" % ("rewritten" if changed else "already current"))
    n = inject_visible()
    print("  visible questions: %d i18n string(s) written" % n)
