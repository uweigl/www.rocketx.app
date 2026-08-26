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
 "At go-live. Setup and integration are waived on annual plans, and a 30 to 45 day pilot with agreed measures comes before any longer commitment.",
 "Your data can be exported in open formats at any time and on exit. Customers in the US and the EU have the same export and exit rights; nothing is withheld or downgraded by region.",
],
"de": [
 "Nein. Die Plattformgebühr ist eine monatliche Pauschale und nie ein Prozentsatz Ihres Bestellvolumens. Es gibt keine Gebühren pro SKU und keine pro Nutzer. Die Stufen richten sich nach dem Unternehmensumsatz, nicht danach, wie stark ein einzelner Monat ausfällt.",
 "Ja. Ihr Außendienst sieht Warenkörbe live beim Entstehen: was darin liegt, was stockt, was seit Tagen unberührt ist. Er ergänzt die fehlende Position, korrigiert die Menge oder greift zum Telefon, bevor die Sache kalt wird.",
 "Ja. Warenkörbe liegen auf dem Server und synchronisieren in Echtzeit zwischen Webshop und nativen Apps. Nichts hängt davon ab, dass eine Browser-Sitzung am Leben bleibt.",
 "Ja. Mehrere Personen arbeiten gleichzeitig am selben Warenkorb. Jede Änderung trägt Name und Zeitstempel.",
 "Ja. Der Warenkorb prüft, was das Kundenkonto bereits gekauft hat, und meldet eine kürzliche Dopplung vor dem Absenden: wer bestellt hat, wie viel, wann geliefert wurde.",
 "Nein. Plätze und Nutzer sind in jedem Plan unbegrenzt. Für Mitarbeiter, Außendienst und autorisierte Mitarbeiter Ihrer Kunden fallen keine Nutzergebühren an.",
 "Die Suche bleibt unter einer Sekunde, ob der Katalog einige hundert SKUs umfasst oder Millionen. Gemessen wird an Ihrem echten Katalog im Piloten, nicht an einem Demo-Datensatz.",
 "Nativ für iOS und Android, gebaut für B2B-Bestellungen statt einer Website in einer App-Hülle. Barcode-Scan und Offline-Zugriff sind enthalten.",
 "Ja. Katalog, Preise, Warenkorb sowie Ihre Broschüren und Produktvideos liegen lokal und synchronisieren, sobald die Verbindung zurück ist.",
 "Mit dem Go-live. Setup und Integration werden bei Jahresplänen erlassen, und vor einer längeren Bindung steht ein Pilot über 30 bis 45 Tage mit vereinbarten Messgrößen.",
 "Ihre Daten lassen sich jederzeit und beim Wechsel in offenen Formaten exportieren. Kunden in den USA und in der EU haben dieselben Export- und Ausstiegsrechte; nichts wird nach Region zurückgehalten oder abgeschwächt.",
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
 "En la puesta en marcha. La implantación y la integración están incluidas en los planes anuales, y antes de cualquier compromiso largo hay un piloto de 30 a 45 días con métricas acordadas.",
 "Puedes exportar tus datos en formatos abiertos en cualquier momento y también al salir. Los clientes de EE. UU. y de la UE tienen los mismos derechos de exportación y salida; no se retiene ni se recorta nada según la región.",
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
 "Bij livegang. Inrichting en integratie zijn kwijtgescholden bij jaarplannen, en vóór een langere verbintenis staat een pilot van 30 tot 45 dagen met afgesproken maatstaven.",
 "Je kunt je gegevens op elk moment en ook bij vertrek exporteren in open formaten. Klanten in de VS en de EU hebben dezelfde export- en exitrechten; er wordt niets achtergehouden of afgezwakt per regio.",
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

if __name__ == "__main__":
    for l in ("en", "de", "es", "nl"):
        f = faqpage(l)
        print("  %s: %d Q&A, first = %s" % (l, len(f["mainEntity"]), f["mainEntity"][0]["name"][:62]))
