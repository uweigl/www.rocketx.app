#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the RocketX business-case deck (print-optimised HTML) in EN/DE/ES.

No prices anywhere: commercial terms are described structurally
(flat fee vs GMV %, setup waived, billing at go-live) without figures,
so the PDF cannot go stale when pricing moves.
"""
import io, os

OUT = os.path.expanduser("~/Downloads/rocketx-site3/deck")

# ---------------------------------------------------------------- content
C = {}

C["en"] = dict(
    lang="en", file="rocketx-business-case-en",
    doctitle="RocketX — The Business Case for Modern B2B Ordering",
    kicker="INTERNAL BUSINESS CASE",
    title="The business case for modern B2B ordering",
    sub="Prepared for wholesale, distribution, and manufacturing teams evaluating how their buyers place orders.",
    forwho="For companies with $15–300M in revenue and high-volume wholesale ordering",
    date="2026 edition",
    p1h="Why this is on the agenda now",
    p1a="B2B purchasing has moved online while overall B2B trade has stayed flat. The growth is not in more buyers — it is in a larger share of the same buyers ordering digitally, and choosing suppliers by how easy that is.",
    stats=[("$2.93T", "U.S. B2B ecommerce in 2025, up 13% while total B2B sales stayed roughly flat"),
           ("39%", "of B2B buyers will place orders above $500K through digital self-service — up from 28% two years earlier"),
           ("94%", "of smartphone time is spent inside apps rather than a browser"),
           (">40%", "of revenue at leading B2B organizations is driven or influenced by mobile")],
    p1b="The practical consequence: the ordering experience is no longer a back-office system. It is the surface your customers judge you on, and the point at which they decide whether to reorder or call somebody else.",
    p2h="What the current setup usually costs",
    p2a="Most mid-market wholesalers are running one of three things: an aging ERP portal, a general-purpose ecommerce platform bent into B2B shape, or phone-and-email order entry. Each carries a cost that rarely appears as a line item.",
    costs=[("Catalog performance", "Platforms built for consumer retail slow down at wholesale catalog sizes. Buyers abandon search and call a rep, which converts a self-service order into a staffed one."),
           ("Per-seat licensing", "Charging per user means the warehouse team, the field reps, and the customer's own staff are rationed. The people who would use the system most are the ones left out."),
           ("Percentage-of-GMV fees", "Fees tied to order volume mean your platform cost rises exactly as you succeed. Growth is taxed rather than supported."),
           ("Implementation drag", "Mid-market B2B builds on general platforms commonly run four to eight months or more before launch, with integration work billed throughout."),
           ("Manual catalog upkeep", "Product data maintained by hand across PDFs, spreadsheets, and the ERP consumes staff time continuously and still drifts out of date.")],
    p3h="What RocketX changes",
    caps=[("Unlimited SKUs, sub-second search", "Whether the catalogue runs to eight hundred SKUs or eight million, filter and order in milliseconds — and never pay by the SKU. Performance other platforms do not match at scale."),
          ("Native iOS and Android apps", "Purpose-built for B2B ordering, not a wrapped website. Full catalog in the buyer's pocket."),
          ("Unlimited seats and users", "Every employee, rep, and authorised customer gets full access. No per-user fees, no per-SKU fees, no rationing."),
          ("Real-time cart collaboration", "Multiple team members work the same cart at once, with every action logged — who, what, when."),
          ("Customer-specific pricing", "Each buyer sees their negotiated prices, volume breaks, and contract terms automatically."),
          ("Live inventory across warehouses", "Real-time stock and availability, so buyers stop ordering what cannot ship."),
          ("Order directly from PDFs", "AI reads existing brochures and catalogs so buyers order straight from them — no re-keying."),
          ("Deep ERP and CRM integration", "RocketX sits in front of your ERP rather than replacing it. Products, customer-specific pricing and live stock flow out of NetSuite, SAP, Microsoft Dynamics or Epicor; carts, orders and approvals flow back. Standard connectors are included in every plan.")],
    p4h="Why the native app matters commercially",
    p4a="A responsive website and a native app are not the same product. For repeat wholesale ordering the difference shows up directly in order frequency.",
    native=[("Reordering is a habit, not a search", "Most B2B orders are repeat orders. A browser makes the buyer find a bookmark, load a site, and log in every time. An app is one tap, already signed in — friction removed from every reorder for the life of the account."),
            ("A permanent position on the buyer's phone", "Your icon sits on the home screen. Competitors have to be searched for and rediscovered."),
            ("Push reaches buyers that email does not", "Back-in-stock alerts, contract renewals, and reorder reminders arrive directly. Users who opt into push retain at two to three times the rate of those who do not."),
            ("The work happens away from a desk", "Buyers order from warehouse aisles, loading docks, and trade-show floors. Native camera access means barcode scanning and reorder from a shelf label."),
            ("It survives losing signal", "Steel-walled warehouses and rural routes kill reception. The catalog, pricing, and cart stay local and sync when the connection returns.")],
    p5h="How the commercial terms reduce risk",
    p5a="The structure of the agreement is designed so the platform proves itself before it costs anything. No figures are quoted here — current pricing is on the website and in your proposal.",
    terms=[("Flat fee, never a percentage of GMV", "Platform cost does not rise because your order volume did. Growth is not taxed."),
           ("Unlimited SKUs and seats included", "Nothing is metered. No per-user or per-SKU pricing to negotiate, or to ration as the catalogue and the team grow."),
           ("Setup and integration fee waived on annual plans", "The implementation cost that usually front-loads these projects is removed."),
           ("Billing starts at go-live, not at signature", "You pay nothing until the platform is live and delivering value."),
           ("30–45 day pilot with joint ROI review", "A defined evaluation window with agreed measures, before a longer commitment."),
           ("Native apps and standard integrations included", "Not sold as add-on modules on top of a base licence.")],
    p6h="What implementation looks like",
    steps=[("1. Stack audit", "We map the existing catalog, pricing rules, ERP, and order flow, and identify what has to move and what stays."),
           ("2. Integration", "Two-way sync is built against your ERP and CRM. Standard connectors cover the major systems; anything beyond standard scope is quoted as a defined block of work."),
           ("3. Catalog ingestion", "Existing PDFs, brochures, and product data are read in. No manual re-keying of the catalog."),
           ("4. Pilot", "A 30–45 day live pilot with a defined buyer group and agreed success measures."),
           ("5. Go-live and review", "Full rollout, with a joint ROI review against the measures agreed at pilot.")],
    # --- the cart: the differentiator, and where orders are actually lost
    p8h="Where the order is actually lost",
    p8a="Most evaluations compare catalogues and checkout. The money leaks somewhere less visible: in the cart, between the moment a buyer starts an order and the moment somebody submits it.",
    cart=[("A half-built order is invisible", "On most platforms nobody on your side can see a cart until it becomes an order. A stalled cart looks exactly like no cart at all, so the first time you learn it existed is when it never arrives."),
          ("Carts die with the session", "Browser carts are tied to a device and a session. A buyer interrupted on the warehouse floor comes back to an empty basket and rebuilds it by phone, or does not bother."),
          ("One person builds what six to ten people decide", "Gartner puts a complex B2B purchase in the hands of six to ten people. When only one of them can touch the cart, the order is assembled by email and retyped, and it arrives incomplete."),
          ("The duplicate nobody caught becomes a return", "When colleagues at the same account cannot see each other's orders, the same SKU gets ordered twice. That is the most expensive kind of transaction you can create."),
          ("What RocketX does instead", "Carts persist server-side and sync live across the web shop and the native apps. Your reps see live customer carts, including what has stalled, and can act before it goes cold. The whole buying team edits one cart with every change attributed. And the cart flags a SKU the account already bought recently, before the order is placed.")],
    p9h="How to size this for your business",
    p9a="No two distributors leak value in the same proportions, so the honest version of this page is a worksheet rather than a promise. Substitute your own figures; the arithmetic is deliberately simple.",
    levers=[("Carts recovered", "Carts started each month &times; share abandoned &times; average order value &times; the share your reps now rescue because they can finally see them."),
            ("Returns avoided", "Returns each month &times; the share caused by a duplicate or wrong item &times; your fully loaded cost per return. Count the labour: a single return consumes the handling of eight to ten normal orders."),
            ("Rep hours redeployed", "Reps &times; hours each week spent taking and re-keying orders &times; loaded hourly cost &times; 52. Every hour moved out of order entry is an hour available for selling."),
            ("Order size", "Average order value &times; the uplift you expect from the full catalogue being searchable in seconds, unlimited seats, and reorder from any device.")],
    p9n="Against those four, set the platform fee and the implementation effort from your proposal. If the first two alone do not clear the cost, the case does not need the other two.",
    p7h="Questions worth asking any vendor",
    quest=["Does the platform fee change as our order volume grows?",
           "Can our reps see a customer's cart before it becomes an order?",
           "Does a cart survive a closed browser, a flat battery, a change of device?",
           "Can several people at the same customer build one order together?",
           "Will the system warn us when the same SKU was already ordered recently?",
           "Are field reps and our customers' staff charged as seats?",
           "What is the search response time at our actual catalog size, not a demo catalog?",
           "Are the mobile apps native, or a website in an app shell?",
           "Does the catalog work when a buyer has no signal?",
           "When does billing start — at signature or at go-live?",
           "What happens to our data and integrations if we leave?"],
    ctah="Next step",
    ctap="A personalised demo against your own catalog, a short stack audit, and a low-risk pilot with measurable results within weeks.",
    contact="app@rocketx.app",
    srch="Sources",
    src="Digital Commerce 360 / U.S. Department of Commerce for B2B ecommerce totals and growth. Baymard Institute for the cart-abandonment rate, averaged across 50 studies (2006-2025); that figure covers all ecommerce and is not segmented for B2B. Gartner for the size of the buying group on a complex B2B purchase. Return-handling effort per the B2B E-commerce Association\u2019s distribution benchmarks. McKinsey B2B Pulse, ninth annual survey of 3,942 B2B decision makers across 13 countries, for digital order values. Sensor Tower, State of Mobile 2026, for share of smartphone time outside the browser; this figure covers all smartphone use, not B2B ordering specifically. Boston Consulting Group with Google, “Mobile Marketing and the New B2B Buyer” (2017), for mobile's share of B2B revenue. Airship retention benchmarks for push opt-in. Implementation timelines reflect 2026 market benchmarks for mid-market B2B builds and vary by scope.",
    foot="RocketX LLC · app@rocketx.app · rocketx.app",
    pg="Page",
)

C["de"] = dict(
    lang="de", file="rocketx-business-case-de",
    doctitle="RocketX — Der Business Case für modernes B2B-Bestellen",
    kicker="INTERNE ENTSCHEIDUNGSVORLAGE",
    title="Der Business Case für modernes B2B-Bestellen",
    sub="Für Teams in Großhandel, Distribution und Fertigung, die prüfen, wie ihre Kunden Bestellungen aufgeben.",
    forwho="Für Unternehmen mit 15–250 Mio. € Umsatz und hohem Bestellvolumen im Großhandel",
    date="Ausgabe 2026",
    p1h="Warum das Thema jetzt auf der Agenda steht",
    p1a="Der B2B-Einkauf ist online, während der B2B-Handel insgesamt stagniert. Das Wachstum entsteht nicht durch mehr Kunden, sondern dadurch, dass dieselben Kunden einen größeren Teil digital bestellen — und ihre Lieferanten danach auswählen, wie einfach das ist.",
    stats=[("509 Mrd. €", "B2B-Internethandel in Deutschland 2024 (Onlineshops & Marktplätze) — plus 7 % trotz Konjunkturflaute"),
           ("1,5 Bio. €", "gesamter deutscher B2B-E-Commerce inkl. EDI — knapp ein Viertel aller B2B-Umsätze läuft bereits online"),
           ("94 %", "der Smartphone-Zeit wird in Apps verbracht, nicht im Browser"),
           ("> 40 %", "des Umsatzes führender B2B-Unternehmen werden durch Mobile getrieben oder beeinflusst")],
    p1b="Die praktische Folge: Das Bestellerlebnis ist kein Backoffice-System mehr. Es ist die Oberfläche, an der Ihre Kunden Sie messen — und der Punkt, an dem sie entscheiden, ob sie nachbestellen oder woanders anrufen.",
    p2h="Was die heutige Lösung meist kostet",
    p2a="Die meisten mittelständischen Großhändler betreiben eines von drei Dingen: ein in die Jahre gekommenes ERP-Portal, eine allgemeine E-Commerce-Plattform, die zum B2B-System umgebogen wurde, oder Auftragserfassung per Telefon und E-Mail. Jede Variante verursacht Kosten, die selten als Position auftauchen.",
    costs=[("Katalog-Performance", "Plattformen für den Endkundenhandel werden bei Großhandels-Katalogen langsam. Einkäufer brechen die Suche ab und rufen an — aus einer Self-Service-Bestellung wird eine personalbesetzte."),
           ("Lizenzierung pro Nutzer", "Preise pro Nutzer führen dazu, dass Lager, Außendienst und Kundenmitarbeiter rationiert werden. Genau die Menschen, die das System am meisten nutzen würden, bleiben außen vor."),
           ("Umsatzabhängige Gebühren", "An das Bestellvolumen gekoppelte Gebühren lassen Ihre Plattformkosten genau dann steigen, wenn Sie erfolgreich sind. Wachstum wird besteuert statt unterstützt."),
           ("Implementierungsdauer", "B2B-Projekte im Mittelstand auf allgemeinen Plattformen laufen üblicherweise vier bis acht Monate oder länger bis zum Start — Integrationsarbeit wird durchgehend abgerechnet."),
           ("Manuelle Katalogpflege", "Von Hand über PDFs, Tabellen und das ERP gepflegte Produktdaten binden laufend Personalzeit und sind trotzdem nie aktuell.")],
    p3h="Was RocketX verändert",
    caps=[("Unbegrenzt viele SKUs, Suche unter einer Sekunde", "Ob der Katalog achthundert SKUs umfasst oder acht Millionen — filtern und bestellen in Millisekunden, und nie eine Gebühr pro SKU. Eine Performance, die andere Plattformen in dieser Größenordnung nicht erreichen."),
          ("Native iOS- und Android-Apps", "Speziell für B2B-Bestellungen entwickelt, keine verpackte Website. Der vollständige Katalog in der Tasche des Einkäufers."),
          ("Unbegrenzte Plätze und Nutzer", "Jeder Mitarbeiter, Vertriebler und autorisierte Kunde erhält vollen Zugriff. Keine Gebühren pro Nutzer, keine pro SKU, keine Rationierung."),
          ("Zusammenarbeit am Warenkorb in Echtzeit", "Mehrere Teammitglieder arbeiten gleichzeitig am selben Warenkorb — jede Aktion protokolliert: wer, was, wann."),
          ("Kundenspezifische Preise", "Jeder Einkäufer sieht automatisch seine verhandelten Preise, Mengenstaffeln und Vertragskonditionen."),
          ("Live-Bestände über alle Lager", "Bestände und Verfügbarkeit in Echtzeit — Schluss mit Bestellungen auf nicht lieferbare Ware."),
          ("Direkt aus PDFs bestellen", "Unsere KI liest bestehende Broschüren und Kataloge, sodass Einkäufer direkt daraus bestellen — ohne erneute Dateneingabe."),
          ("Tiefe ERP- und CRM-Integration", "RocketX setzt sich vor Ihr ERP, statt es zu ersetzen. Produkte, kundenspezifische Preise und Live-Bestände fließen aus NetSuite, SAP, Microsoft Dynamics oder Epicor heraus; Warenkörbe, Bestellungen und Freigaben fließen zurück. Standard-Konnektoren sind in jedem Plan enthalten.")],
    p4h="Warum die native App wirtschaftlich zählt",
    p4a="Eine responsive Website und eine native App sind nicht dasselbe Produkt. Bei wiederkehrenden Großhandelsbestellungen zeigt sich der Unterschied direkt in der Bestellfrequenz.",
    native=[("Nachbestellen ist Gewohnheit, keine Suche", "Die meisten B2B-Bestellungen sind Wiederholungsbestellungen. Im Browser muss der Einkäufer jedes Mal das Lesezeichen finden, die Seite laden und sich anmelden. Eine App ist ein Fingertipp entfernt, bereits angemeldet — diese Reibung entfällt dauerhaft bei jeder Nachbestellung."),
            ("Ein fester Platz auf dem Telefon des Einkäufers", "Ihr Icon liegt auf dem Homescreen. Wettbewerber müssen jedes Mal neu gesucht werden."),
            ("Push erreicht Einkäufer, die E-Mail nicht erreicht", "Verfügbarkeitsmeldungen, Vertragsverlängerungen und Nachbestell-Erinnerungen kommen direkt an. Nutzer, die Push aktivieren, bleiben zwei- bis dreimal so lange aktiv."),
            ("Gearbeitet wird nicht am Schreibtisch", "Einkäufer bestellen aus Lagergängen, von der Laderampe und vom Messestand. Nativer Kamerazugriff ermöglicht Barcode-Scan und Nachbestellung direkt vom Regaletikett."),
            ("Sie funktioniert auch ohne Empfang", "Hallen mit Stahlwänden und ländliche Touren kosten Empfang. Katalog, Preise und Warenkorb bleiben lokal verfügbar und synchronisieren, sobald die Verbindung zurück ist.")],
    p5h="Wie die Vertragskonditionen das Risiko senken",
    p5a="Die Vertragsstruktur ist so angelegt, dass sich die Plattform beweist, bevor sie etwas kostet. Hier werden bewusst keine Beträge genannt — die aktuellen Preise finden Sie auf der Website und in Ihrem Angebot.",
    terms=[("Pauschalgebühr, niemals ein Umsatzprozentsatz", "Die Plattformkosten steigen nicht, weil Ihr Bestellvolumen gestiegen ist. Wachstum wird nicht besteuert."),
           ("Unbegrenzte SKUs und Plätze inklusive", "Nichts wird nach Menge berechnet. Keine Preise pro Nutzer oder pro SKU, die verhandelt oder rationiert werden müssten, wenn Katalog und Team wachsen."),
           ("Setup- und Integrationsgebühr bei Jahresplänen erlassen", "Die Implementierungskosten, die solche Projekte sonst vorbelasten, entfallen."),
           ("Abrechnung ab Go-live, nicht ab Unterschrift", "Sie zahlen nichts, bis die Plattform live ist und Wert liefert."),
           ("30–45-Tage-Pilot mit gemeinsamem ROI-Review", "Ein definierter Bewertungszeitraum mit vereinbarten Kennzahlen, vor einer längeren Bindung."),
           ("Native Apps und Standard-Integrationen inklusive", "Nicht als Zusatzmodule über einer Basislizenz verkauft.")],
    p6h="Wie die Einführung abläuft",
    steps=[("1. Stack-Audit", "Wir erfassen bestehenden Katalog, Preisregeln, ERP und Bestellprozess und bestimmen, was migriert wird und was bleibt."),
           ("2. Integration", "Die bidirektionale Synchronisation wird gegen Ihr ERP und CRM aufgebaut. Standard-Konnektoren decken die großen Systeme ab; alles darüber hinaus wird als definierter Entwicklungsblock angeboten."),
           ("3. Katalog-Übernahme", "Bestehende PDFs, Broschüren und Produktdaten werden eingelesen. Keine manuelle Neuerfassung des Katalogs."),
           ("4. Pilot", "Ein 30–45-tägiger Live-Pilot mit definierter Einkäufergruppe und vereinbarten Erfolgskriterien."),
           ("5. Go-live und Review", "Vollständiger Rollout, mit gemeinsamem ROI-Review anhand der im Piloten vereinbarten Kennzahlen.")],
    p8h="Wo die Bestellung wirklich verloren geht",
    p8a="Die meisten Evaluationen vergleichen Kataloge und Checkout. Der Verlust entsteht an einer weniger sichtbaren Stelle: im Warenkorb, zwischen dem Moment, in dem ein Einkäufer beginnt, und dem Moment, in dem jemand absendet.",
    cart=[("Eine halbfertige Bestellung ist unsichtbar", "Auf den meisten Plattformen kann niemand auf Ihrer Seite einen Warenkorb sehen, bevor daraus eine Bestellung wird. Ein stehengebliebener Warenkorb sieht aus wie gar kein Warenkorb — Sie erfahren von ihm erst, wenn er nie ankommt."),
          ("Warenkörbe sterben mit der Sitzung", "Browser-Warenkörbe hängen an Gerät und Sitzung. Ein im Lager unterbrochener Einkäufer findet einen leeren Korb vor und baut ihn telefonisch neu auf — oder lässt es."),
          ("Einer baut, was sechs bis zehn entscheiden", "Laut Gartner liegt eine komplexe B2B-Beschaffung in den Händen von sechs bis zehn Personen. Wenn nur eine davon den Warenkorb anfassen kann, wird die Bestellung per E-Mail zusammengetragen, abgetippt — und kommt unvollständig an."),
          ("Die übersehene Dopplung wird zur Retoure", "Wenn Kollegen beim selben Kunden die Bestellungen der anderen nicht sehen, wird dieselbe SKU zweimal bestellt. Das ist die teuerste Transaktion, die Sie erzeugen können."),
          ("Was RocketX stattdessen tut", "Warenkörbe werden serverseitig gespeichert und live zwischen Webshop und nativen Apps synchronisiert. Ihr Außendienst sieht laufende Kundenwarenkörbe samt allem, was stockt, und kann handeln, bevor die Sache kalt wird. Das gesamte Einkaufsteam arbeitet an einem Warenkorb, jede Änderung mit Name. Und der Warenkorb weist auf eine SKU hin, die das Konto kürzlich schon gekauft hat — vor dem Absenden.")],
    p9h="So bemessen Sie das für Ihr Unternehmen",
    p9a="Kein Distributor verliert Wert in denselben Anteilen wie ein anderer. Die ehrliche Fassung dieser Seite ist deshalb ein Rechenblatt statt eines Versprechens. Setzen Sie Ihre eigenen Zahlen ein; die Arithmetik ist bewusst einfach.",
    levers=[("Zurückgeholte Warenkörbe", "Warenkörbe pro Monat &times; Abbruchquote &times; durchschnittlicher Bestellwert &times; Anteil, den Ihr Außendienst jetzt rettet, weil er sie endlich sieht."),
            ("Vermiedene Retouren", "Retouren pro Monat &times; Anteil durch Dopplung oder falschen Artikel &times; Ihre vollbelasteten Kosten je Retoure. Rechnen Sie die Arbeitszeit mit: Eine einzige Retoure verschlingt den Aufwand von acht bis zehn normalen Bestellungen."),
            ("Freigesetzte Außendienststunden", "Mitarbeiter &times; Wochenstunden für Auftragsannahme und -erfassung &times; vollbelastete Stundenkosten &times; 52. Jede Stunde weniger Erfassung ist eine Stunde mehr Vertrieb."),
            ("Bestellgröße", "Durchschnittlicher Bestellwert &times; erwarteter Zuwachs dadurch, dass der vollständige Katalog in Sekunden durchsuchbar ist, Plätze unbegrenzt sind und von jedem Gerät nachbestellt werden kann.")],
    p9n="Diesen vier Posten stellen Sie Plattformgebühr und Implementierungsaufwand aus Ihrem Angebot gegenüber. Wenn schon die ersten beiden die Kosten nicht decken, brauchen Sie die anderen beiden nicht.",
    p7h="Fragen, die man jedem Anbieter stellen sollte",
    quest=["Ändert sich die Plattformgebühr, wenn unser Bestellvolumen wächst?",
           "Kann unser Außendienst den Warenkorb eines Kunden sehen, bevor daraus eine Bestellung wird?",
           "Übersteht ein Warenkorb geschlossenen Browser, leeren Akku, Gerätewechsel?",
           "Können mehrere Personen beim selben Kunden gemeinsam eine Bestellung aufbauen?",
           "Warnt das System, wenn dieselbe SKU kürzlich bereits bestellt wurde?",
           "Werden Außendienst und Mitarbeiter unserer Kunden als Plätze berechnet?",
           "Wie schnell antwortet die Suche bei unserer echten Katalogröße, nicht bei einem Demo-Katalog?",
           "Sind die Mobile-Apps nativ oder eine Website in einer App-Hülle?",
           "Funktioniert der Katalog, wenn ein Einkäufer keinen Empfang hat?",
           "Wann beginnt die Abrechnung — bei Unterschrift oder bei Go-live?",
           "Was passiert mit unseren Daten und Integrationen, wenn wir wechseln?"],
    ctah="Nächster Schritt",
    ctap="Eine persönliche Demo an Ihrem eigenen Katalog, ein kurzes Stack-Audit und ein risikoarmer Pilot mit messbaren Ergebnissen innerhalb weniger Wochen.",
    contact="app@rocketx.app",
    srch="Quellen",
    src="ECC KÖLN B2B-Marktmonitor 2025 (mit FIS und Shopware) für die deutschen B2B-E-Commerce-Zahlen. Baymard Institute für die Warenkorb-Abbruchquote, gemittelt über 50 Studien (2006–2025); dieser Wert umfasst den gesamten E-Commerce und ist nicht nach B2B segmentiert. Gartner zur Größe des Buying-Centers bei komplexen B2B-Beschaffungen. Aufwand für Retouren nach Benchmarks der B2B E-commerce Association für die Distribution. McKinsey B2B Pulse, neunte Jahresbefragung von 3.942 B2B-Entscheidern in 13 Ländern. Sensor Tower, State of Mobile 2026, für den Anteil der Smartphone-Zeit außerhalb des Browsers; diese Angabe umfasst die gesamte Smartphone-Nutzung, nicht speziell B2B-Bestellungen. Boston Consulting Group mit Google, „Mobile Marketing and the New B2B Buyer“ (2017), für den Mobile-Anteil am B2B-Umsatz. Airship-Benchmarks zur Push-Aktivierung. Implementierungszeiträume entsprechen Marktbenchmarks 2026 für mittelständische B2B-Projekte und variieren je nach Umfang.",
    foot="RocketX LLC · app@rocketx.app · rocketx.app",
    pg="Seite",
)

C["es"] = dict(
    lang="es", file="rocketx-business-case-es",
    doctitle="RocketX — El caso de negocio para pedidos B2B modernos",
    kicker="CASO DE NEGOCIO INTERNO",
    title="El caso de negocio para pedidos B2B modernos",
    sub="Para equipos de mayoreo, distribución y manufactura que evalúan cómo sus clientes hacen pedidos.",
    forwho="Para empresas de $15–300M de facturación con pedidos mayoristas de alto volumen",
    date="Edición 2026",
    p1h="Por qué está en la agenda ahora",
    p1a="Las compras B2B se han movido a lo digital mientras el comercio B2B total se mantiene plano. El crecimiento no viene de más clientes, sino de que los mismos clientes piden una porción mayor de forma digital — y eligen proveedor según lo fácil que resulte.",
    stats=[("$2.93B", "ecommerce B2B en EE. UU. en 2025, un 13% más mientras las ventas B2B totales se mantuvieron planas"),
           ("39%", "de los compradores B2B harán pedidos de más de $500K por autoservicio digital — frente al 28% dos años antes"),
           ("94%", "del tiempo en el móvil se pasa dentro de apps, no en el navegador"),
           (">40%", "de los ingresos de las principales empresas B2B es impulsado o influido por el móvil")],
    p1b="La consecuencia práctica: la experiencia de pedido ya no es un sistema de trastienda. Es la superficie por la que sus clientes le juzgan, y el punto en el que deciden si repiten o llaman a otro.",
    p2h="Lo que suele costar la solución actual",
    p2a="La mayoría de los mayoristas de mercado medio operan una de tres cosas: un portal ERP envejecido, una plataforma de ecommerce general forzada a funcionar como B2B, o captura de pedidos por teléfono y correo. Cada una tiene un costo que rara vez aparece como partida.",
    costs=[("Rendimiento del catálogo", "Las plataformas creadas para el comercio minorista se ralentizan con catálogos mayoristas. Los compradores abandonan la búsqueda y llaman a un vendedor, convirtiendo un pedido de autoservicio en uno atendido."),
           ("Licencias por usuario", "Cobrar por usuario significa racionar al equipo de almacén, a los vendedores y al personal del propio cliente. Quienes más usarían el sistema quedan fuera."),
           ("Comisiones sobre el GMV", "Las tarifas ligadas al volumen hacen que el costo de la plataforma suba justo cuando usted tiene éxito. El crecimiento se grava en vez de apoyarse."),
           ("Duración de la implementación", "Los proyectos B2B de mercado medio sobre plataformas generales suelen tardar de cuatro a ocho meses o más en lanzarse, con trabajo de integración facturado durante todo el proceso."),
           ("Mantenimiento manual del catálogo", "Los datos de producto mantenidos a mano entre PDFs, hojas de cálculo y el ERP consumen tiempo de personal continuamente y aun así se desactualizan.")],
    p3h="Qué cambia RocketX",
    caps=[("SKUs ilimitados, búsqueda en menos de un segundo", "Tanto si el catálogo tiene ochocientos SKUs como ocho millones, filtre y pida en milisegundos — y nunca pague por SKU. Un rendimiento que otras plataformas no igualan a esta escala."),
          ("Apps nativas de iOS y Android", "Creadas específicamente para pedidos B2B, no un sitio web empaquetado. El catálogo completo en el bolsillo del comprador."),
          ("Usuarios y accesos ilimitados", "Cada empleado, vendedor y cliente autorizado tiene acceso completo. Sin tarifas por usuario, sin tarifas por SKU, sin racionar."),
          ("Colaboración en el carrito en tiempo real", "Varios miembros del equipo trabajan el mismo carrito a la vez, con cada acción registrada: quién, qué y cuándo."),
          ("Precios por cliente", "Cada comprador ve automáticamente sus precios negociados, escalas por volumen y condiciones de contrato."),
          ("Inventario en vivo entre almacenes", "Stock y disponibilidad en tiempo real, para dejar de pedir lo que no puede enviarse."),
          ("Pedidos directos desde PDFs", "Nuestra IA lee folletos y catálogos existentes para que los compradores pidan directamente desde ellos, sin volver a teclear."),
          ("Integración profunda con ERP y CRM", "RocketX se sitúa delante de tu ERP en lugar de reemplazarlo. Productos, precios por cliente y stock en vivo salen de NetSuite, SAP, Microsoft Dynamics o Epicor; carritos, pedidos y aprobaciones vuelven. Los conectores estándar están incluidos en todos los planes.")],
    p4h="Por qué la app nativa importa comercialmente",
    p4a="Un sitio web responsivo y una app nativa no son el mismo producto. En pedidos mayoristas recurrentes la diferencia se ve directamente en la frecuencia de pedido.",
    native=[("Recomprar es un hábito, no una búsqueda", "La mayoría de los pedidos B2B son repeticiones. En un navegador el comprador debe encontrar el marcador, cargar el sitio e iniciar sesión cada vez. Una app está a un toque, con la sesión iniciada — fricción eliminada en cada recompra, de forma permanente."),
            ("Una posición permanente en el teléfono del comprador", "Su icono queda en la pantalla de inicio. A la competencia hay que buscarla y redescubrirla."),
            ("Las notificaciones llegan donde el correo no", "Avisos de reposición, renovaciones de contrato y recordatorios de recompra llegan directamente. Quienes activan las notificaciones se retienen entre dos y tres veces más."),
            ("El trabajo ocurre lejos del escritorio", "Los compradores piden desde pasillos de almacén, muelles de carga y ferias. El acceso nativo a la cámara permite escanear códigos y recomprar desde la etiqueta del estante."),
            ("Sobrevive a la pérdida de señal", "Los almacenes con paredes de acero y las rutas rurales acaban con la cobertura. El catálogo, los precios y el carrito quedan en local y sincronizan al volver la conexión.")],
    p5h="Cómo las condiciones comerciales reducen el riesgo",
    p5a="La estructura del acuerdo está diseñada para que la plataforma se demuestre antes de costar nada. Aquí no se citan importes — los precios vigentes están en el sitio web y en su propuesta.",
    terms=[("Tarifa fija, nunca un porcentaje del GMV", "El costo de la plataforma no sube porque su volumen de pedidos lo haya hecho. El crecimiento no se grava."),
           ("SKUs y usuarios ilimitados incluidos", "Nada se mide. Sin precios por usuario ni por SKU que negociar o racionar cuando crecen el catálogo y el equipo."),
           ("Tarifa de setup e integración incluida en planes anuales", "Se elimina el costo de implementación que normalmente carga estos proyectos por adelantado."),
           ("La facturación empieza en el go-live, no en la firma", "No paga nada hasta que la plataforma esté en producción generando valor."),
           ("Piloto de 30–45 días con revisión conjunta de ROI", "Una ventana de evaluación definida con métricas acordadas, antes de un compromiso más largo."),
           ("Apps nativas e integraciones estándar incluidas", "No se venden como módulos adicionales sobre una licencia base.")],
    p6h="Cómo es la implementación",
    steps=[("1. Auditoría del stack", "Mapeamos el catálogo actual, las reglas de precios, el ERP y el flujo de pedidos, e identificamos qué debe migrar y qué se queda."),
           ("2. Integración", "Se construye la sincronización bidireccional contra su ERP y CRM. Los conectores estándar cubren los sistemas principales; lo que exceda ese alcance se cotiza como un bloque de trabajo definido."),
           ("3. Ingesta del catálogo", "Se leen los PDFs, folletos y datos de producto existentes. Sin volver a teclear el catálogo."),
           ("4. Piloto", "Un piloto en vivo de 30–45 días con un grupo de compradores definido y métricas de éxito acordadas."),
           ("5. Go-live y revisión", "Despliegue completo, con revisión conjunta de ROI frente a las métricas acordadas en el piloto.")],
    p8h="Dónde se pierde realmente el pedido",
    p8a="Casi todas las evaluaciones comparan catálogos y checkout. El dinero se escapa en un sitio menos visible: en el carrito, entre el momento en que un comprador empieza y el momento en que alguien envía.",
    cart=[("Un pedido a medio construir es invisible", "En la mayoría de plataformas nadie de tu lado puede ver un carrito hasta que se convierte en pedido. Un carrito atascado se ve igual que ningún carrito: te enteras de que existía cuando nunca llega."),
          ("Los carritos mueren con la sesión", "Los carritos de navegador dependen del dispositivo y de la sesión. Un comprador interrumpido en el almacén vuelve a una cesta vacía y la reconstruye por teléfono, o lo deja."),
          ("Uno construye lo que deciden seis a diez", "Gartner sitúa una compra B2B compleja en manos de seis a diez personas. Si solo una puede tocar el carrito, el pedido se arma por correo, se reteclea y llega incompleto."),
          ("El duplicado que nadie vio acaba en devolución", "Cuando los compañeros del mismo cliente no ven los pedidos de los demás, el mismo SKU se pide dos veces. Es la transacción más cara que puedes generar."),
          ("Qué hace RocketX en su lugar", "Los carritos persisten en el servidor y se sincronizan en vivo entre la tienda web y las apps nativas. Tus vendedores ven los carritos de cliente en vivo, incluido lo que se ha atascado, y pueden actuar antes de que se enfríe. Todo el equipo de compras edita un carrito con cada cambio atribuido. Y el carrito avisa de un SKU que la cuenta ya compró hace poco, antes de enviar el pedido.")],
    p9h="Cómo dimensionar esto para tu empresa",
    p9a="No hay dos distribuidores que pierdan valor en las mismas proporciones, así que la versión honesta de esta página es una hoja de cálculo, no una promesa. Sustituye tus propias cifras; la aritmética es deliberadamente simple.",
    levers=[("Carritos recuperados", "Carritos iniciados al mes &times; porcentaje abandonado &times; valor medio del pedido &times; la parte que tus vendedores ahora rescatan porque por fin los ven."),
            ("Devoluciones evitadas", "Devoluciones al mes &times; parte causada por duplicado o artículo equivocado &times; tu costo totalmente cargado por devolución. Cuenta la mano de obra: una sola devolución consume el trabajo de ocho a diez pedidos normales."),
            ("Horas de vendedor liberadas", "Vendedores &times; horas semanales dedicadas a tomar y reteclear pedidos &times; costo horario cargado &times; 52. Cada hora que sale de la captura de pedidos es una hora disponible para vender."),
            ("Tamaño del pedido", "Valor medio del pedido &times; el aumento que esperas de tener el catálogo completo buscable en segundos, usuarios ilimitados y recompra desde cualquier dispositivo.")],
    p9n="Frente a esos cuatro, pon la tarifa de plataforma y el esfuerzo de implementación de tu propuesta. Si los dos primeros por sí solos no cubren el costo, no hace falta recurrir a los otros dos.",
    p7h="Preguntas que conviene hacer a cualquier proveedor",
    quest=["¿Cambia la tarifa de la plataforma cuando crece nuestro volumen de pedidos?",
           "¿Pueden nuestros vendedores ver el carrito de un cliente antes de que sea pedido?",
           "¿Sobrevive un carrito al cierre del navegador, a una batería agotada, a un cambio de dispositivo?",
           "¿Pueden varias personas del mismo cliente construir un pedido conjuntamente?",
           "¿Avisa el sistema cuando el mismo SKU ya se pidió hace poco?",
           "¿Se cobran como usuarios los vendedores de campo y el personal de nuestros clientes?",
           "¿Cuál es el tiempo de respuesta de búsqueda con nuestro catálogo real, no con uno de demostración?",
           "¿Las apps móviles son nativas o un sitio web dentro de una carcasa?",
           "¿Funciona el catálogo cuando un comprador no tiene señal?",
           "¿Cuándo empieza la facturación: en la firma o en el go-live?",
           "¿Qué pasa con nuestros datos e integraciones si nos vamos?"],
    ctah="Siguiente paso",
    ctap="Una demo personalizada sobre su propio catálogo, una auditoría breve del stack y un piloto de bajo riesgo con resultados medibles en semanas.",
    contact="app@rocketx.app",
    srch="Fuentes",
    src="Digital Commerce 360 / Departamento de Comercio de EE. UU. para los totales y el crecimiento del ecommerce B2B. Baymard Institute para la tasa de abandono de carrito, promediada en 50 estudios (2006-2025); esa cifra cubre todo el ecommerce y no está segmentada para B2B. Gartner para el tamaño del grupo de compra en una adquisición B2B compleja. Esfuerzo de gestión de devoluciones según los benchmarks de distribución de la B2B E-commerce Association. McKinsey B2B Pulse, novena encuesta anual a 3.942 responsables de decisión B2B en 13 países, para los valores de pedido digital. Sensor Tower, State of Mobile 2026, para la porción del tiempo móvil fuera del navegador; esta cifra cubre todo el uso del smartphone, no específicamente pedidos B2B. Boston Consulting Group con Google, «Mobile Marketing and the New B2B Buyer» (2017), para la porción de ingresos B2B del móvil. Benchmarks de retención de Airship para notificaciones. Los plazos de implementación reflejan benchmarks de mercado 2026 para proyectos B2B de mercado medio y varían según el alcance.",
    foot="RocketX LLC · app@rocketx.app · rocketx.app",
    pg="Página",
)

# ---------------------------------------------------------------- template
CSS = """
@page{size:A4;margin:17mm 16mm 15mm}
*{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#1D4ED8;--sky:#2563EB;--ink:#0B1526;--body:#3B4A63;--soft:#6B7C99;--line:#DDE4F0;--tint:#F4F7FC}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"Inter",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--body);font-size:9.6pt;line-height:1.6}
h1,h2,h3,.num,.stat b{font-family:"Space Grotesk","Inter",-apple-system,Helvetica,Arial,sans-serif}
.page{page-break-after:always;position:relative;min-height:245mm}
.page:last-child{page-break-after:auto}
/* cover */
.cover{display:flex;flex-direction:column;justify-content:center;min-height:243mm}
.cover .brand{display:flex;align-items:center;gap:9px;margin-bottom:56px}
.cover .brand img{width:26px;height:26px}
.cover .brand b{font-family:"Space Grotesk",sans-serif;font-size:15pt;color:var(--ink);letter-spacing:-.01em}
.kick{font-family:"IBM Plex Mono","SFMono-Regular",Consolas,monospace;font-size:7.6pt;letter-spacing:.24em;color:var(--sky);margin-bottom:16px}
.cover h1{font-size:30pt;line-height:1.1;color:var(--ink);letter-spacing:-.02em;max-width:150mm;font-weight:700}
.cover .sub{font-size:11.5pt;color:var(--soft);margin-top:20px;max-width:135mm;line-height:1.5}
.cover .meta{margin-top:52px;padding-top:18px;border-top:1px solid var(--line);font-size:9pt;color:var(--soft);display:flex;justify-content:space-between;gap:16px}
.cover .meta b{color:var(--ink);font-weight:600}
/* headings */
h2{font-size:17pt;color:var(--ink);letter-spacing:-.015em;line-height:1.2;margin-bottom:14px;font-weight:700}
.lede{font-size:10.4pt;color:var(--body);max-width:150mm;margin-bottom:26px;line-height:1.62}
h3{font-size:10.4pt;color:var(--ink);font-weight:600;margin-bottom:5px;line-height:1.35}
/* stats */
.stats{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line);border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:26px 0}
.stat{background:#fff;padding:20px 20px 18px}
.stat b{display:block;font-size:20pt;color:var(--blue);font-weight:700;letter-spacing:-.02em;line-height:1}
.stat span{display:block;font-size:8.6pt;color:var(--soft);margin-top:8px;line-height:1.48}
/* rows */
.rows{border-top:1px solid var(--line)}
.row{border-bottom:1px solid var(--line);padding:13px 0;display:grid;grid-template-columns:52mm 1fr;gap:14px;page-break-inside:avoid}
.row p{font-size:9.4pt;color:var(--body);line-height:1.55}
/* two-col capability list */
.caps{display:grid;grid-template-columns:1fr 1fr;gap:16px 20px;margin-top:22px}
.cap{page-break-inside:avoid}
.cap p{font-size:8.9pt;color:var(--soft);line-height:1.5}
/* numbered steps */
.step{display:grid;grid-template-columns:9mm 1fr;gap:11px;padding:12px 0;border-bottom:1px solid var(--line);page-break-inside:avoid}
.step .num{font-family:"IBM Plex Mono",monospace;font-size:8.4pt;color:var(--sky);padding-top:1px}
.step p{font-size:9.3pt;line-height:1.55}
/* questions */
.q{padding:10px 0 10px 20px;border-bottom:1px solid var(--line);position:relative;font-size:9.8pt;color:var(--ink);page-break-inside:avoid}
.q::before{content:"?";position:absolute;left:0;color:var(--sky);font-weight:700;font-family:"Space Grotesk",sans-serif}
/* callout */
.callout{background:var(--tint);border-left:3px solid var(--blue);border-radius:0 9px 9px 0;padding:20px 22px;margin-top:26px;page-break-inside:avoid}
.callout h3{margin-bottom:6px}
.callout p{font-size:9.6pt}
.callout .mail{display:inline-block;margin-top:11px;font-weight:600;color:var(--blue);font-size:10.4pt}
/* sources */
.src{margin-top:26px;padding-top:14px;border-top:1px solid var(--line)}
.src h3{font-family:"IBM Plex Mono",monospace;font-size:7.4pt;letter-spacing:.2em;text-transform:uppercase;color:var(--soft);font-weight:400;margin-bottom:7px}
.src p{font-size:7.6pt;color:var(--soft);line-height:1.55}
/* levers worksheet */
.lever{display:grid;grid-template-columns:44mm 1fr;gap:14px;padding:14px 0;border-bottom:1px solid var(--line);page-break-inside:avoid}
.lever h3{font-size:10.6pt;color:var(--blue)}
.lever p{font-size:9.4pt;line-height:1.55}
.closing{margin-top:22px;background:var(--tint);border-radius:9px;padding:16px 18px;font-size:9.6pt;page-break-inside:avoid}
/* running foot */
.foot{position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-between;font-size:7.4pt;color:#9AA8BF;border-top:1px solid var(--line);padding-top:7px}
"""

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def build(d):
    P = []
    # cover
    P.append(
      '<div class="page cover">'
      '<div class="brand"><img src="../assets/logo.png" alt=""><b>RocketX</b></div>'
      '<div class="kick">%s</div><h1>%s</h1><p class="sub">%s</p>'
      '<div class="meta"><span><b>%s</b></span><span>%s</span></div>'
      '</div>' % (esc(d["kicker"]), esc(d["title"]), esc(d["sub"]), esc(d["forwho"]), esc(d["date"])))

    # p1 market
    stats = "".join('<div class="stat"><b>%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in d["stats"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="stats">%s</div>'
             '<p class="lede" style="margin-bottom:0">%s</p></div>'
             % (esc(d["p1h"]), esc(d["p1a"]), stats, esc(d["p1b"])))

    # p2 hidden costs
    rows = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["costs"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["p2h"]), esc(d["p2a"]), rows))

    # p3 capabilities
    caps = "".join('<div class="cap"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["caps"])
    P.append('<div class="page"><h2>%s</h2><div class="caps">%s</div></div>' % (esc(d["p3h"]), caps))

    # p4 native
    nat = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["native"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["p4h"]), esc(d["p4a"]), nat))

    # p8 the cart (placed before the commercial terms - it is the differentiator)
    cart = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["cart"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["p8h"]), esc(d["p8a"]), cart))

    # p9 sizing worksheet
    lv = "".join('<div class="lever"><h3>%s</h3><p>%s</p></div>' % (esc(a), b) for a, b in d["levers"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div style="margin-top:8px">%s</div>'
             '<div class="closing">%s</div></div>'
             % (esc(d["p9h"]), esc(d["p9a"]), lv, esc(d["p9n"])))

    # p5 terms
    tr = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["terms"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["p5h"]), esc(d["p5a"]), tr))

    # p6 implementation
    st = "".join('<div class="step"><span class="num">%02d</span><div><h3>%s</h3><p>%s</p></div></div>'
                 % (i + 1, esc(a), esc(b)) for i, (a, b) in enumerate(d["steps"]))
    P.append('<div class="page"><h2>%s</h2><div style="margin-top:20px">%s</div></div>' % (esc(d["p6h"]), st))

    # p7 questions + CTA + sources
    qs = "".join('<div class="q">%s</div>' % esc(q) for q in d["quest"])
    P.append('<div class="page"><h2>%s</h2><div style="margin-top:20px">%s</div>'
             '<div class="callout"><h3>%s</h3><p>%s</p>'
             '<a class="mail" href="mailto:%s">%s</a></div>'
             '<div class="src"><h3>%s</h3><p>%s</p></div></div>'
             % (esc(d["p7h"]), qs, esc(d["ctah"]), esc(d["ctap"]),
                d["contact"], d["contact"], esc(d["srch"]), esc(d["src"])))

    pages = "\n".join(P)
    return ("""<!DOCTYPE html>
<html lang="%s"><head><meta charset="UTF-8"><title>%s</title>
<link rel="icon" href="../favicon.ico" sizes="any">
<link rel="icon" type="image/svg+xml" href="../assets/icon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="../assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<style>%s</style></head><body>
%s
</body></html>""" % (d["lang"], esc(d["doctitle"]), CSS, pages))

os.makedirs(OUT, exist_ok=True)
for lg, d in C.items():
    p = os.path.join(OUT, d["file"] + ".html")
    io.open(p, "w", encoding="utf-8").write(build(d))
    print("wrote", p)
