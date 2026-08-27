#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the RocketX business-case deck (print-optimised HTML) in EN/DE/ES.

No cash figures anywhere: commercial terms are described structurally
(flat fee vs GMV %, setup waived, billing at go-live). The one exception
is the fee-share curve on the terms page, which plots the fee as a
percentage of sales - no amount is printed, but one can be derived from
it, so that chart has to be revisited whenever pricing moves.
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
    forwho="For wholesale and distribution companies with $15–300M in revenue",
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
          ("Your brochures and video, in the buyer's pocket", "Publish existing print brochures as PDFs, product video and other rich content alongside the catalogue. It syncs into the native apps and still opens with no signal, so your showroom material travels with the buyer."),
          ("Wholesale first, and your consumer channel with it", "The product is built around wholesale ordering. If you also sell direct to consumers, that channel runs from the same catalogue and the same ERP feed rather than a second platform and a second set of product data."),
          ("Deep ERP and CRM integration", "RocketX sits in front of your ERP rather than replacing it. Products, customer-specific pricing and live stock flow out of NetSuite, SAP, Microsoft Dynamics or Epicor; carts, orders and approvals flow back. Standard connectors are included in every plan.")],
    p4h="Why the native app matters commercially",
    p4a="A responsive website and a native app are not the same product. For repeat wholesale ordering the difference shows up directly in order frequency.",
    native=[("Reordering is a habit, not a search", "Most B2B orders are repeat orders. A browser makes the buyer find a bookmark, load a site, and log in every time. An app is one tap, already signed in — friction removed from every reorder for the life of the account."),
            ("A permanent position on the buyer's phone", "Your icon sits on the home screen. Competitors have to be searched for and rediscovered."),
            ("Push reaches buyers that email does not", "Back-in-stock alerts, contract renewals, and reorder reminders arrive directly. Users who opt into push retain at two to three times the rate of those who do not."),
            ("The work happens away from a desk", "Buyers order from warehouse aisles, loading docks, and trade-show floors. Native camera access means barcode scanning and reorder from a shelf label."),
            ("It survives losing signal", "Steel-walled warehouses and rural routes kill reception. The catalog, pricing, cart, and your brochures and product video stay local and sync when the connection returns.")],
    p5h="How the commercial terms reduce risk",
    p5a="The structure of the agreement is designed so the platform proves itself before it costs anything. No amounts are quoted here — current pricing is on the website and in your proposal. The chart below shows only what the fee is worth as a share of your sales.",
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
    cart=[("A half-built order is invisible", "Roughly 70% of online carts are abandoned across ecommerce, and on most platforms nobody on your side can see one until it becomes an order. A stalled cart looks exactly like no cart at all, so the first time you learn it existed is when it never arrives."),
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
    # --- executive summary (page one after the cover)
    xsh="In one page",
    xsa="If you read nothing else: wholesale orders leak in the cart, on the phone, and in the returns bay. This is a proposal to stop that, with the platform proving itself before it costs anything.",
    xs=[('The problem', 'Your buyers assemble orders somewhere nobody on your side can see, in a browser tab they have to find and log into every time - while the work itself happens on a phone, in an aisle, at a loading dock. Carts die with the session, one person builds what six to ten people decide, and the duplicate nobody caught comes back as a return.'),
        ('What changes in the cart', 'Carts persist server-side and sync live across the web shop and the native apps. Your reps see live customer carts, including what has stalled, and can act before one goes cold. The whole buying team edits one order, every change attributed. And the cart flags a SKU the account already bought recently, before the order is placed.'),
        ("What changes on the buyer's phone", 'Your catalogue sits on the home screen, one tap from a reorder and already signed in, rather than behind a bookmark and a login. Push brings buyers back when stock returns or a contract is due, where email gets filtered. Barcode scanning reorders straight from a shelf label, and the catalogue is cached, so an aisle with no signal is still an aisle that can order. Your print brochures, product video and other rich content ride along in the same app, so the showroom material is with the buyer when the conversation happens. Native iOS and Android, not a website in a shell. Reordering stops being an errand and becomes a habit, which is where repeat revenue actually comes from.'),
        ('Why it is defensible', 'Unlimited SKUs and unlimited seats, never metered, never a percentage of your revenue. Standard ERP and CRM connectors included, with RocketX sitting in front of your systems of record rather than replacing them - and running alongside your existing web shop, so nothing is switched off.'),
        ('What it costs to try', 'Setup waived on annual plans. Billing starts at go-live, not at signature. A 30 to 45 day pilot with agreed measures before any longer commitment.'),
        ('The one-percent test', 'Set the platform fee in your proposal against one percent of your annual sales - or against the margin on one percent, if you prefer the conservative version. The only question left is whether better ordering is worth more than that to you. If it is, the rest of this document is detail rather than persuasion.')],
    # --- data, entities and compliance
    cmh='Two entities, two jurisdictions, one answer for each',
    cma="Security and data review is usually the slowest part of an evaluation. We avoided that by never asking you to accept European data sitting in America.",
    eu_f='For customers in the European Union',
    eu_h="You contract with RocketX Limited",
    us_f='For customers in the United States',
    us_h='You contract with RocketX LLC',
    ath='Attaches to the agreement, in both jurisdictions',
    cmn="Send this page to whoever runs your security review. We would rather answer the questionnaire in week one than in week nine.",
    eu=[("Counterparty", "An Irish company, incorporated and operating in the European Union under EU law, separate from the US entity."),
        ("Data residency", "Customer data stays in the European Union: storage, processing and backups. Nothing is replicated to the United States."),
        ("Certifications", "EU facilities certified to ISO/IEC 27001:2022 and BSI C5 Type 2."),
        ("GDPR", "Applies to the engagement directly. You are the controller of your customer and order data; we are the processor, acting on your documented instructions."),
        ("Transfer analysis", "Your counterparty is an EU company, so the review does not start with a Chapter V transfer question. That is usually where evaluations of US vendors lose a month."),
        ("Subprocessors", "Disclosed in full, with notice before any change and a contractual right to object.")],
    us=[("Counterparty", "RocketX LLC, the United States entity. Same platform, same commitments, governed where you are."),
        ("Data residency", "Customer data stays in the United States: storage, processing and backups. Nothing is replicated to the EU."),
        ("Certifications", "The same provider and the same operational controls. Facility attestations for the US sites are available on request."),
        ("State privacy law", "CCPA and CPRA, and the successor state statutes, are handled through the same written processing terms rather than a separate regime per state."),
        ("Security review", "Certifications, audit reports and hosting detail are provided on request and attach to the agreement."),
        ("Portability", "The same export and exit rights as EU customers. Nothing is withheld or downgraded by region.")],
    at=['Data processing agreement, with roles written down', 'Current subprocessor list, with change notice', 'Certifications, audit reports and hosting region', 'Uptime and support commitments, by tier', 'Retention, deletion and backup policy', 'Export in open formats, at any time and on exit'],
    nfh="Where we are not the right fit",
    nfa="Every vendor says they are right for you. Here is the short list of times we are not, so that it surfaces now rather than in month two of an implementation.",
    nf=[('You sell only to consumers', 'Most of the product is wholesale machinery a consumer catalogue never touches.'),
        ('Your catalogue is small and your orders are simple', 'A few dozen SKUs and single-line orders do not need this.'),
        ('You have no ERP and no plans for one', 'Much of the value here is two-way sync with a system of record.')],
    nfn='Selling both wholesale and direct is common, and it is not a limit here — the consumer channel runs from the same catalogue and the same ERP feed as the wholesale one.',
    # --- cost of delay, on the worksheet page
    cdh="What the wait costs",
    cd="Whatever the four levers add up to, they are annual. A quarter of deliberation costs a quarter of that number, and the leak does not pause while you evaluate. That is the honest argument for starting a pilot now rather than a procurement cycle in six months.",
    # --- time to live, on the implementation page
    tlh="How long before anyone actually uses it",
    tl=[("Adobe Commerce", "12&ndash;24 weeks", 100),
        ("BigCommerce Enterprise + B2B Edition", "10&ndash;20 weeks", 83),
        ("Shopify Plus (with agency and apps)", "8&ndash;16 weeks", 67),
        ("RocketX — live pilot", "4&ndash;6 weeks", 25)],
    tln="Competitor figures are typical mid-market benchmarks to go-live from 2026 platform and agency guides; scope moves them either way and ERP work is where they most often overrun. The RocketX figure is to a live pilot with a defined buyer group, not full rollout. On the alternatives billing usually starts well before anyone places an order. On ours it starts at go-live.",
    sbh="Nothing gets switched off",
    sba="The usual objection to a platform decision is that it means replacing one. This one does not. RocketX is deployed alongside what you run today, and both keep working.",
    sb=[("Your current web shop keeps running", "RocketX goes live beside it, not on top of it. Nothing is decommissioned to make room, and no catalogue has to be migrated before anyone can place an order."),
        ("Your buyers choose, not you", "Some move to the app in the first week. Some stay on the shop they already know. Both produce orders that land in the same ERP, in the same format, on the same terms, so nothing downstream has to change."),
        ("No cutover weekend", "There is no migration window and no order freeze. The failure mode that makes these projects frightening - a bad Sunday with the phones ringing on Monday - is not on the table, because there is nothing to cut over from."),
        ("Adoption becomes evidence", "Because both run at once, you can watch which one your buyers actually use. That is a better argument for or against us than anything in this document."),
        ("Retire the old system later, or never", "Nothing in the agreement sets a date for turning it off. If it still earns its keep in three years, keep it running.")],
    sbn="This is also the cheapest way to be wrong about us. If the pilot does not work, you switch nothing off, you have lost no orders, and the fallback is the system you were already using.",
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
    sub="Für Großhandel, Distribution und Fertigung: für alle, die prüfen, wie ihre Kunden bestellen.",
    forwho="Für Großhandel und Distribution mit 15–250 Mio. € Umsatz",
    date="Ausgabe 2026",
    p1h="Warum das Thema jetzt auf der Agenda steht",
    p1a="Der B2B-Einkauf geht online, während der B2B-Handel insgesamt stagniert. Das Wachstum kommt nicht von mehr Kunden. Es kommt daher, dass dieselben Kunden einen größeren Teil digital bestellen — und ihre Lieferanten danach auswählen, wie einfach das ist.",
    stats=[("509 Mrd. €", "B2B-Internethandel in Deutschland 2024 (Onlineshops & Marktplätze) — plus 7 % trotz Konjunkturflaute"),
           ("1,5 Bio. €", "gesamter deutscher B2B-E-Commerce inkl. EDI — knapp ein Viertel aller B2B-Umsätze läuft bereits online"),
           ("94 %", "der Smartphone-Zeit wird in Apps verbracht, nicht im Browser"),
           ("> 40 %", "des Umsatzes führender B2B-Unternehmen werden durch Mobile getrieben oder beeinflusst")],
    p1b="Die praktische Folge: Das Bestellerlebnis ist kein Backoffice-System mehr. Es ist die Oberfläche, an der Ihre Kunden Sie messen — und der Punkt, an dem sie entscheiden, ob sie nachbestellen oder woanders anrufen.",
    p2h="Was die heutige Lösung meist kostet",
    p2a="Die meisten mittelständischen Großhändler betreiben eines von drei Dingen. Ein in die Jahre gekommenes ERP-Portal. Eine allgemeine E-Commerce-Plattform, die jemand zum B2B-System umgebogen hat. Oder Auftragserfassung per Telefon und E-Mail. Jede Variante kostet Geld, das selten als Position auftaucht.",
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
          ("Ihre Broschüren und Videos in der Tasche des Einkäufers", "Veröffentlichen Sie vorhandene Printbroschüren als PDF, Produktvideos und weitere Rich-Media-Inhalte direkt neben dem Katalog. Alles synchronisiert in die nativen Apps und öffnet auch ohne Empfang — Ihr Showroom-Material reist mit dem Einkäufer."),
          ("Großhandel zuerst — und Ihr Endkundenkanal gleich mit", "Das Produkt ist um Großhandelsbestellungen herum gebaut. Verkaufen Sie zusätzlich direkt an Endkunden, läuft dieser Kanal aus demselben Katalog und derselben ERP-Anbindung — statt aus einer zweiten Plattform mit einem zweiten Satz Produktdaten."),
          ("Tiefe ERP- und CRM-Integration", "RocketX setzt sich vor Ihr ERP, statt es zu ersetzen. Produkte, kundenspezifische Preise und Live-Bestände fließen aus NetSuite, SAP, Microsoft Dynamics oder Epicor heraus; Warenkörbe, Bestellungen und Freigaben fließen zurück. Standard-Konnektoren sind in jedem Plan enthalten.")],
    p4h="Warum die native App wirtschaftlich zählt",
    p4a="Eine responsive Website und eine native App sind nicht dasselbe Produkt. Bei wiederkehrenden Großhandelsbestellungen zeigt sich der Unterschied direkt in der Bestellfrequenz.",
    native=[("Nachbestellen ist Gewohnheit, keine Suche", "Die meisten B2B-Bestellungen sind Wiederholungsbestellungen. Im Browser muss der Einkäufer jedes Mal das Lesezeichen finden, die Seite laden und sich anmelden. Eine App ist ein Fingertipp entfernt, bereits angemeldet — diese Reibung entfällt dauerhaft bei jeder Nachbestellung."),
            ("Ein fester Platz auf dem Telefon des Einkäufers", "Ihr Icon liegt auf dem Homescreen. Wettbewerber müssen jedes Mal neu gesucht werden."),
            ("Push erreicht Einkäufer, die E-Mail nicht erreicht", "Ist die Ware wieder da, läuft ein Vertrag aus oder steht eine Nachbestellung an — die Nachricht kommt direkt an. Wer Push aktiviert, bleibt zwei- bis dreimal so lange aktiv."),
            ("Gearbeitet wird nicht am Schreibtisch", "Einkäufer bestellen aus Lagergängen, von der Laderampe und vom Messestand. Nativer Kamerazugriff ermöglicht Barcode-Scan und Nachbestellung direkt vom Regaletikett."),
            ("Sie funktioniert auch ohne Empfang", "Hallen mit Stahlwänden und ländliche Touren kosten Empfang. Katalog, Preise, Warenkorb sowie Ihre Broschüren und Produktvideos bleiben lokal verfügbar und synchronisieren, sobald die Verbindung zurück ist.")],
    p5h="Wie die Vertragskonditionen das Risiko senken",
    p5a="Die Vertragsstruktur ist so angelegt, dass sich die Plattform beweist, bevor sie etwas kostet. Hier werden bewusst keine Beträge genannt — die aktuellen Preise finden Sie auf der Website und in Ihrem Angebot. Die Grafik unten zeigt lediglich, was die Gebühr als Anteil an Ihrem Umsatz ausmacht.",
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
    p8a="Die meisten Evaluationen vergleichen Kataloge und Checkout. Der Verlust entsteht woanders, weniger sichtbar: im Warenkorb. Zwischen dem Moment, in dem ein Einkäufer beginnt, und dem Moment, in dem jemand absendet.",
    cart=[("Eine halbfertige Bestellung ist unsichtbar", "Rund 70 % der Online-Warenkörbe brechen ab. Auf den meisten Plattformen sieht niemand auf Ihrer Seite einen Warenkorb, bevor daraus eine Bestellung wird. Ein stehengebliebener Warenkorb sieht aus wie gar kein Warenkorb. Sie erfahren von ihm erst, wenn er nie ankommt."),
          ("Warenkörbe sterben mit der Sitzung", "Browser-Warenkörbe hängen an Gerät und Sitzung. Ein im Lager unterbrochener Einkäufer findet einen leeren Korb vor und baut ihn telefonisch neu auf — oder lässt es."),
          ("Einer baut, was sechs bis zehn entscheiden", "Laut Gartner liegt eine komplexe B2B-Beschaffung in den Händen von sechs bis zehn Personen. Wenn nur eine davon den Warenkorb anfassen kann, wird die Bestellung per E-Mail zusammengetragen, abgetippt — und kommt unvollständig an."),
          ("Die übersehene Dopplung wird zur Retoure", "Wenn Kollegen beim selben Kunden die Bestellungen der anderen nicht sehen, wird dieselbe SKU zweimal bestellt. Das ist die teuerste Transaktion, die Sie erzeugen können."),
          ("Was RocketX stattdessen tut", "Warenkörbe werden serverseitig gespeichert und live zwischen Webshop und nativen Apps synchronisiert. Ihr Außendienst sieht laufende Kundenwarenkörbe samt allem, was stockt, und kann handeln, bevor die Sache kalt wird. Das gesamte Einkaufsteam arbeitet an einem Warenkorb, jede Änderung mit Name. Und der Warenkorb weist auf eine SKU hin, die das Konto kürzlich schon gekauft hat — vor dem Absenden.")],
    p9h="So bemessen Sie das für Ihr Unternehmen",
    p9a="Kein Distributor verliert Wert in denselben Anteilen wie ein anderer. Die ehrliche Fassung dieser Seite ist deshalb ein Rechenblatt statt eines Versprechens. Setzen Sie Ihre eigenen Zahlen ein; die Arithmetik ist bewusst einfach.",
    levers=[("Zurückgeholte Warenkörbe", "Warenkörbe pro Monat &times; Abbruchquote &times; durchschnittlicher Bestellwert &times; Anteil, den Ihr Außendienst jetzt rettet, weil er sie endlich sieht."),
            ("Vermiedene Retouren", "Retouren pro Monat &times; Anteil durch Dopplung oder falschen Artikel &times; Ihre vollbelasteten Kosten je Retoure. Rechnen Sie die Arbeitszeit mit: Eine einzige Retoure verschlingt den Aufwand von acht bis zehn normalen Bestellungen."),
            ("Freigesetzte Außendienststunden", "Mitarbeiter &times; Wochenstunden, um Aufträge anzunehmen und zu erfassen, &times; vollbelastete Stundenkosten &times; 52. Jede Stunde weniger Erfassung ist eine Stunde mehr Vertrieb."),
            ("Bestellgröße", "Durchschnittlicher Bestellwert &times; erwarteter Zuwachs dadurch, dass der vollständige Katalog in Sekunden durchsuchbar ist, Plätze unbegrenzt sind und von jedem Gerät nachbestellt werden kann.")],
    p9n="Diesen vier Posten stellen Sie Plattformgebühr und Implementierungsaufwand aus Ihrem Angebot gegenüber. Wenn schon die ersten beiden die Kosten nicht decken, brauchen Sie die anderen beiden nicht.",
    xsh="Auf einer Seite",
    xsa="Falls Sie nur eine Seite lesen: Großhandelsbestellungen versickern im Warenkorb, am Telefon und in der Retourenannahme. Dies ist ein Vorschlag, das zu beenden — wobei sich die Plattform beweist, bevor sie etwas kostet.",
    xs=[('Das Problem', "Ihre Einkäufer stellen Bestellungen dort zusammen, wo sie auf Ihrer Seite niemand sieht. In einem Browser-Tab, den sie jedes Mal suchen. In den sie sich jedes Mal neu anmelden. Und die Arbeit selbst passiert woanders: am Telefon, im Lagergang, an der Laderampe. Warenkörbe sterben mit der Sitzung. Einer baut, was sechs bis zehn entscheiden. Und die übersehene Dopplung kommt als Retoure zurück."),
        ('Was sich im Warenkorb ändert', 'Warenkörbe werden serverseitig gespeichert und synchronisieren live zwischen Webshop und nativen Apps. Ihr Außendienst sieht laufende Kundenwarenkörbe samt allem, was stockt, und kann handeln, bevor einer kalt wird. Das gesamte Einkaufsteam arbeitet an einer Bestellung, jede Änderung mit Namen. Und der Warenkorb weist auf eine SKU hin, die das Konto kürzlich schon gekauft hat - vor dem Absenden.'),
        ('Was sich auf dem Handy des Einkäufers ändert', "Ihr Katalog liegt auf dem Homescreen, einen Fingertipp von der Nachbestellung entfernt und bereits angemeldet — statt hinter Lesezeichen und Login. Push holt Einkäufer zurück, wenn Ware wieder da ist oder ein Vertrag ansteht: dort, wo der Filter die E-Mail schluckt. Der Barcode-Scan bestellt direkt vom Regaletikett nach. Der Katalog liegt lokal: Ein Gang ohne Empfang bleibt ein Gang, aus dem man bestellt. Ihre Printbroschüren, Produktvideos und weitere Rich-Media-Inhalte liegen in derselben App — das Showroom-Material ist beim Einkäufer, wenn das Gespräch läuft. Nativ für iOS und Android, keine Website in einer Hülle. So hört Nachbestellen auf, eine Besorgung zu sein, und wird zur Gewohnheit. Genau daher kommt wiederkehrender Umsatz."),
        ('Warum das haltbar ist', "Unbegrenzt viele SKUs und Plätze. Nie nach Menge berechnet, nie ein Prozentsatz Ihres Umsatzes. Standard-Konnektoren für ERP und CRM sind enthalten. RocketX setzt sich vor Ihre führenden Systeme, statt sie zu ersetzen. Und es läuft neben Ihrem bestehenden Webshop — Sie schalten nichts ab."),
        ('Was ein Versuch kostet', 'Setup bei Jahresplänen erlassen. Abrechnung ab Go-live, nicht ab Unterschrift. Ein 30- bis 45-tägiger Pilot mit vereinbarten Kennzahlen vor jeder längeren Bindung.'),
        ('Der Ein-Prozent-Test', 'Stellen Sie die Plattformgebühr aus Ihrem Angebot einem Prozent Ihres Jahresumsatzes gegenüber - oder der Marge auf ein Prozent, wenn Sie es konservativ rechnen wollen. Bleibt nur die Frage, ob Ihnen besseres Bestellen mehr wert ist als das. Wenn ja, ist der Rest dieses Dokuments Detail und keine Überzeugungsarbeit.')],
    cmh='Zwei Gesellschaften, zwei Rechtsräume, je eine klare Antwort',
    cma="Die Datenschutz- und Sicherheitsprüfung ist meist der langsamste Teil einer Evaluation. Wir haben das vermieden, indem europäische Daten gar nicht erst nach Amerika gehen.",
    eu_f='Für Kunden in der Europäischen Union',
    eu_h="Sie schließen mit der RocketX Limited ab",
    us_f='Für Kunden in den Vereinigten Staaten',
    us_h='Sie schließen mit der RocketX LLC ab',
    ath='Wird in beiden Rechtsräumen Vertragsbestandteil',
    cmn="Geben Sie diese Seite an Ihre Sicherheitsprüfung weiter. Den Fragebogen beantworten wir lieber in Woche eins als in Woche neun.",
    eu=[("Vertragspartner", "Eine irische Gesellschaft, gegründet und tätig in der Europäischen Union nach EU-Recht, getrennt von der US-Gesellschaft."),
        ("Datenstandort", "Kundendaten bleiben in der Europäischen Union: Speicherung, Verarbeitung, Backups. Keine Replikation in die USA."),
        ("Zertifizierungen", "EU-Rechenzentren mit ISO/IEC 27001:2022 und BSI C5 Typ 2."),
        ("DSGVO", "Gilt unmittelbar für die Zusammenarbeit. Sie sind Verantwortlicher für Ihre Kunden- und Bestelldaten; wir sind Auftragsverarbeiter und handeln auf Ihre dokumentierte Weisung."),
        ("Übermittlungsprüfung", "Ihr Vertragspartner ist ein EU-Unternehmen, die Prüfung beginnt also nicht mit einer Frage nach Kapitel V. Genau dort verlieren Evaluationen von US-Anbietern üblicherweise einen Monat."),
        ("Unterauftragsverarbeiter", "Vollständig offengelegt, mit Vorabmitteilung bei Änderungen und vertraglichem Widerspruchsrecht.")],
    us=[("Vertragspartner", "Die RocketX LLC, die US-Gesellschaft. Dieselbe Plattform, dieselben Zusagen, geltendes Recht an Ihrem Sitz."),
        ("Datenstandort", "Kundendaten bleiben in den Vereinigten Staaten: Speicherung, Verarbeitung, Backups. Keine Replikation in die EU."),
        ("Zertifizierungen", "Derselbe Anbieter, dieselben Betriebskontrollen. Nachweise der US-Rechenzentren stellen wir auf Anfrage bereit."),
        ("Datenschutz der Bundesstaaten", "CCPA und CPRA sowie die nachfolgenden Landesgesetze werden über dieselben schriftlichen Verarbeitungsbedingungen abgedeckt, nicht über ein eigenes Regime je Bundesstaat."),
        ("Sicherheitsprüfung", "Zertifizierungen, Prüfberichte und Angaben zum Hosting stellen wir auf Anfrage bereit; sie werden Vertragsbestandteil."),
        ("Portabilität", "Dieselben Export- und Ausstiegsrechte wie für EU-Kunden. Nach Region wird nichts zurückgehalten oder abgestuft.")],
    at=['Auftragsverarbeitungsvertrag mit schriftlich fixierten Rollen', 'Aktuelle Liste der Unterauftragsverarbeiter, mit Änderungsmitteilung', 'Zertifizierungen, Prüfberichte und Hosting-Region', 'Zusagen zu Verfügbarkeit und Support, nach Stufe', 'Aufbewahrungs-, Lösch- und Backup-Richtlinie', 'Export in offenen Formaten, jederzeit und beim Ausstieg'],
    nfh="Wofür wir nicht der Richtige sind",
    nfa="Jeder Anbieter sagt, er passe zu Ihnen. Hier die kurze Liste der Fälle, in denen wir es nicht tun — damit das jetzt herauskommt und nicht im zweiten Monat der Einführung.",
    nf=[('Sie verkaufen ausschließlich an Endkunden', 'Der größte Teil des Produkts ist Großhandels-Maschinerie, die ein Endkunden-Katalog nie berührt.'),
        ('Ihr Katalog ist klein und Ihre Bestellungen sind einfach', 'Ein paar Dutzend SKUs und einzeilige Bestellungen brauchen das hier nicht.'),
        ('Sie haben kein ERP und planen keines', 'Ein großer Teil des Werts liegt in der bidirektionalen Synchronisation mit einem führenden System.')],
    nfn="Großhandel und Direktverkauf an Endkunden nebeneinander: verbreitet, und hier keine Einschränkung. Der Endkundenkanal läuft aus demselben Katalog und derselben ERP-Anbindung wie das Großhandelsgeschäft.",
    cdh="Was das Warten kostet",
    cd="Was die vier Hebel auch ergeben — es sind Jahreswerte. Ein Quartal Bedenkzeit kostet ein Viertel davon, und das Leck pausiert nicht, während Sie prüfen. Das ist das ehrliche Argument dafür, jetzt einen Piloten zu starten statt in sechs Monaten einen Beschaffungsprozess.",
    tlh="Wie lange, bis es tatsächlich jemand benutzt",
    tl=[("Adobe Commerce", "12&ndash;24 Wochen", 100),
        ("BigCommerce Enterprise + B2B Edition", "10&ndash;20 Wochen", 83),
        ("Shopify Plus (mit Agentur und Apps)", "8&ndash;16 Wochen", 67),
        ("RocketX — Live-Pilot", "4&ndash;6 Wochen", 25)],
    tln="Die Wettbewerberwerte sind übliche Mittelstands-Benchmarks bis zum Go-live, aus Plattform- und Agentur-Leitfäden 2026. Der Umfang verschiebt sie in beide Richtungen. Am häufigsten überzieht die ERP-Arbeit. Der RocketX-Wert meint einen Live-Piloten mit definierter Einkäufergruppe, nicht den vollständigen Rollout. Bei den Alternativen beginnt die Abrechnung meist lange, bevor jemand bestellt. Bei uns beginnt sie mit dem Go-live.",
    sbh="Es wird nichts abgeschaltet",
    sba="Der übliche Einwand gegen eine Plattformentscheidung lautet, dass sie den Austausch einer Plattform bedeutet. Diese hier nicht. RocketX wird neben dem eingeführt, was Sie heute betreiben — beides läuft weiter.",
    sb=[("Ihr jetziger Webshop läuft weiter", "RocketX geht daneben live, nicht darüber. Nichts wird stillgelegt, um Platz zu machen, und kein Katalog muss migriert werden, bevor jemand bestellen kann."),
        ("Ihre Einkäufer entscheiden, nicht Sie", "Manche wechseln in der ersten Woche zur App. Manche bleiben bei dem Shop, den sie kennen. Beide erzeugen Bestellungen, die im selben ERP landen, im selben Format, zu denselben Konditionen — nachgelagert ändert sich also nichts."),
        ("Kein Umstellungswochenende", "Es gibt kein Migrationsfenster und keinen Bestellstopp. Der Fehlerfall, der solche Projekte fürchten lässt, steht gar nicht zur Debatte: ein schlechter Sonntag, am Montag klingeln die Telefone. Es gibt schlicht nichts umzustellen."),
        ("Nutzung wird zum Beweis", "Weil beides gleichzeitig läuft, können Sie beobachten, was Ihre Einkäufer tatsächlich verwenden. Das ist ein besseres Argument für oder gegen uns als alles in diesem Dokument."),
        ("Das Altsystem später abschalten — oder nie", "Nichts im Vertrag legt dafür ein Datum fest. Wenn es sich in drei Jahren noch rechnet, lassen Sie es laufen.")],
    sbn="Das ist zugleich die günstigste Art, sich in uns zu irren. Funktioniert der Pilot nicht, schalten Sie nichts ab, haben keine Bestellung verloren, und der Rückfallweg ist das System, das Sie ohnehin genutzt haben.",
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
    forwho="Para empresas mayoristas y de distribución de $15–300M de facturación",
    date="Edición 2026",
    p1h="Por qué está en la agenda ahora",
    p1a="Las compras B2B se han movido a lo digital mientras el comercio B2B total se mantiene plano. El crecimiento no viene de más clientes, sino de que los mismos clientes piden una porción mayor de forma digital — y eligen proveedor según lo fácil que resulte.",
    stats=[("$2,93 B", "Comercio electrónico B2B en EE. UU. en 2025, un 13% más mientras las ventas B2B totales se mantuvieron planas"),
           ("39%", "de los compradores B2B harán pedidos de más de $500K por autoservicio digital — frente al 28% dos años antes"),
           ("94%", "del tiempo en el móvil se pasa dentro de apps, no en el navegador"),
           (">40%", "de los ingresos de las principales empresas B2B es impulsado o influido por el móvil")],
    p1b="La consecuencia práctica: la experiencia de pedido ya no es un sistema de trastienda. Es la superficie por la que sus clientes le juzgan, y el punto en el que deciden si repiten o llaman a otro.",
    p2h="Lo que suele costar la solución actual",
    p2a="La mayoría de los mayoristas de mercado medio operan una de tres cosas. Un portal ERP envejecido. Una plataforma de comercio electrónico general forzada a hacer de B2B. O captura de pedidos por teléfono y correo. Cada una cuesta dinero que rara vez aparece como partida.",
    costs=[("Rendimiento del catálogo", "Las plataformas creadas para el comercio minorista se ralentizan con catálogos mayoristas. Los compradores abandonan la búsqueda y llaman a un vendedor, convirtiendo un pedido de autoservicio en uno atendido."),
           ("Licencias por usuario", "Cobrar por usuario significa racionar al equipo de almacén, a los vendedores y al personal del propio cliente. Quienes más usarían el sistema quedan fuera."),
           ("Comisiones sobre las ventas", "Las tarifas ligadas al volumen hacen que el costo de la plataforma suba justo cuando usted tiene éxito. El crecimiento se grava en vez de apoyarse."),
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
          ("Tus folletos y vídeos, en el bolsillo del comprador", "Publica tus folletos impresos como PDF, vídeos de producto y otro contenido enriquecido junto al catálogo. Se sincroniza con las apps nativas y sigue abriéndose sin señal, así que tu material de showroom viaja con el comprador."),
          ("Primero el mayoreo, y tu canal de consumo con él", "El producto está construido en torno al pedido mayorista. Si además vendes directo al consumidor, ese canal se alimenta del mismo catálogo y de la misma conexión con el ERP. Ni una segunda plataforma, ni un segundo juego de datos de producto."),
          ("Integración profunda con ERP y CRM", "RocketX se sitúa delante de tu ERP en lugar de reemplazarlo. Productos, precios por cliente y stock en vivo salen de NetSuite, SAP, Microsoft Dynamics o Epicor; carritos, pedidos y aprobaciones vuelven. Los conectores estándar están incluidos en todos los planes.")],
    p4h="Por qué la app nativa importa comercialmente",
    p4a="Un sitio web responsivo y una app nativa no son el mismo producto. En pedidos mayoristas recurrentes la diferencia se ve directamente en la frecuencia de pedido.",
    native=[("Recomprar es un hábito, no una búsqueda", "La mayoría de los pedidos B2B son repeticiones. En un navegador el comprador debe encontrar el marcador, cargar el sitio e iniciar sesión cada vez. Una app está a un toque, con la sesión iniciada — fricción eliminada en cada recompra, de forma permanente."),
            ("Una posición permanente en el teléfono del comprador", "Su icono queda en la pantalla de inicio. A la competencia hay que buscarla y redescubrirla."),
            ("Las notificaciones llegan donde el correo no", "Avisos de reposición, renovaciones de contrato y recordatorios de recompra llegan directamente. Quienes activan las notificaciones se retienen entre dos y tres veces más."),
            ("El trabajo ocurre lejos del escritorio", "Los compradores piden desde pasillos de almacén, muelles de carga y ferias. El acceso nativo a la cámara permite escanear códigos y recomprar desde la etiqueta del estante."),
            ("Sobrevive a la pérdida de señal", "Los almacenes con paredes de acero y las rutas rurales acaban con la cobertura. El catálogo, los precios, el carrito y tus folletos y vídeos de producto quedan en local y sincronizan al volver la conexión.")],
    p5h="Cómo las condiciones comerciales reducen el riesgo",
    p5a="La estructura del acuerdo está diseñada para que la plataforma se demuestre antes de costar nada. Aquí no se citan importes — los precios vigentes están en el sitio web y en su propuesta. El gráfico de abajo solo muestra cuánto representa la cuota como parte de tus ventas.",
    terms=[("Tarifa fija, nunca un porcentaje de las ventas", "El costo de la plataforma no sube porque su volumen de pedidos lo haya hecho. El crecimiento no se grava."),
           ("SKUs y usuarios ilimitados incluidos", "Nada se mide. Sin precios por usuario ni por SKU que negociar o racionar cuando crecen el catálogo y el equipo."),
           ("Tarifa de implantación e integración incluida en planes anuales", "Se elimina el costo de implementación que normalmente carga estos proyectos por adelantado."),
           ("La facturación empieza en la puesta en marcha, no en la firma", "No paga nada hasta que la plataforma esté en producción generando valor."),
           ("Piloto de 30–45 días con revisión conjunta de ROI", "Una ventana de evaluación definida con métricas acordadas, antes de un compromiso más largo."),
           ("Apps nativas e integraciones estándar incluidas", "No se venden como módulos adicionales sobre una licencia base.")],
    p6h="Cómo es la implementación",
    steps=[("1. Auditoría de los sistemas", "Mapeamos el catálogo actual, las reglas de precios, el ERP y el flujo de pedidos, e identificamos qué debe migrar y qué se queda."),
           ("2. Integración", "Se construye la sincronización bidireccional contra su ERP y CRM. Los conectores estándar cubren los sistemas principales; lo que exceda ese alcance se cotiza como un bloque de trabajo definido."),
           ("3. Ingesta del catálogo", "Se leen los PDFs, folletos y datos de producto existentes. Sin volver a teclear el catálogo."),
           ("4. Piloto", "Un piloto en vivo de 30–45 días con un grupo de compradores definido y métricas de éxito acordadas."),
           ("5. Puesta en marcha y revisión", "Despliegue completo, con revisión conjunta de ROI frente a las métricas acordadas en el piloto.")],
    p8h="Dónde se pierde realmente el pedido",
    p8a="Casi todas las evaluaciones comparan catálogos y proceso de pago. El dinero se escapa en un sitio menos visible: en el carrito, entre el momento en que un comprador empieza y el momento en que alguien envía.",
    cart=[("Un pedido a medio construir es invisible", "Alrededor del 70 % de los carritos online se abandonan, y en la mayoría de plataformas nadie de tu lado puede ver uno hasta que se convierte en pedido. Un carrito atascado se ve igual que ningún carrito: te enteras de que existía cuando nunca llega."),
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
    xsh="En una página",
    xsa="Si no lees nada más: los pedidos mayoristas se escapan en el carrito, por teléfono y en la zona de devoluciones. Esto es una propuesta para detenerlo, con la plataforma demostrándose antes de costar nada.",
    xs=[('El problema', "Tus compradores arman pedidos donde nadie de tu lado los ve: en una pestaña del navegador que deben encontrar y en la que deben identificarse cada vez. Y el trabajo ocurre en otro sitio — en un móvil, en un pasillo de almacén, en un muelle de carga. Los carritos mueren con la sesión. Una persona construye lo que deciden entre seis y diez. Y el duplicado que nadie vio vuelve como devolución."),
        ('Qué cambia en el carrito', 'Los carritos persisten en el servidor y se sincronizan en vivo entre la tienda web y las apps nativas. Tus vendedores ven los carritos de cliente en vivo, incluido lo que se ha atascado, y pueden actuar antes de que se enfríe. Todo el equipo de compras edita un solo pedido, con cada cambio atribuido. Y el carrito avisa de un SKU que la cuenta ya compró hace poco, antes de enviar.'),
        ('Qué cambia en el móvil del comprador', "Tu catálogo está en la pantalla de inicio, a un toque de la recompra y con la sesión ya iniciada. No detrás de un marcador y una contraseña. Las notificaciones devuelven al comprador cuando vuelve el stock o vence un contrato: justo ahí donde el correo se filtra. El escaneo de códigos recompra desde la etiqueta del estante. Y el catálogo queda en local: un pasillo sin cobertura sigue siendo un pasillo desde el que se pide. Tus folletos impresos, los vídeos de producto y otro contenido enriquecido viajan en la misma app, así que el material de showroom está con el comprador cuando llega la conversación. Nativo para iOS y Android, no un sitio web dentro de una carcasa. Recomprar deja de ser un recado y se vuelve un hábito. De ahí sale el ingreso recurrente."),
        ('Por qué se sostiene', "SKUs y usuarios ilimitados, nunca medidos, nunca un porcentaje de tus ingresos. Conectores estándar de ERP y CRM incluidos. RocketX se sitúa delante de tus sistemas de registro en lugar de reemplazarlos, y convive con tu tienda web actual: no se apaga nada."),
        ('Qué cuesta probarlo', 'Implantación incluida en planes anuales. La facturación empieza en la puesta en marcha, no en la firma. Un piloto de 30 a 45 días con métricas acordadas antes de cualquier compromiso más largo.'),
        ('La prueba del uno por ciento', "Pon la tarifa de plataforma de tu propuesta frente al uno por ciento de tus ventas anuales. O frente al margen sobre ese uno por ciento, si prefieres la versión conservadora. La única pregunta que queda es si pedir mejor vale más que eso para ti. Si es así, el resto de este documento es detalle, no persuasión.")],
    cmh='Dos entidades, dos jurisdicciones, una respuesta clara para cada una',
    cma="La revisión de seguridad y datos suele ser la parte más lenta de una evaluación. Lo evitamos no llevando nunca los datos europeos a América.",
    eu_f='Para clientes de la Unión Europea',
    eu_h="Contratas con RocketX Limited",
    us_f='Para clientes de Estados Unidos',
    us_h='Contratas con RocketX LLC',
    ath='Se adjunta al acuerdo, en ambas jurisdicciones',
    cmn="Pasa esta página a quien lleve tu revisión de seguridad. Preferimos responder el cuestionario en la semana uno y no en la nueve.",
    eu=[("Contraparte", "Una sociedad irlandesa, constituida y operativa en la Unión Europea bajo derecho de la UE, separada de la entidad estadounidense."),
        ("Ubicación de los datos", "Los datos de cliente permanecen en la Unión Europea: almacenamiento, procesamiento y copias de seguridad. No se replican a Estados Unidos."),
        ("Certificaciones", "Centros de datos de la UE con ISO/IEC 27001:2022 y BSI C5 Tipo 2."),
        ("RGPD", "Se aplica directamente a la relación. Tú eres el responsable de los datos de tus clientes y pedidos; nosotros somos el encargado y actuamos según tus instrucciones documentadas."),
        ("Análisis de transferencias", "Tu contraparte es una empresa de la UE, así que la revisión no empieza por una pregunta del Capítulo V. Ahí es donde las evaluaciones de proveedores estadounidenses suelen perder un mes."),
        ("Subencargados", "Divulgados por completo, con aviso previo a cualquier cambio y derecho contractual de objeción.")],
    us=[("Contraparte", "RocketX LLC, la entidad estadounidense. La misma plataforma, los mismos compromisos, con la ley de donde estás."),
        ("Ubicación de los datos", "Los datos de cliente permanecen en Estados Unidos: almacenamiento, procesamiento y copias de seguridad. No se replican a la UE."),
        ("Certificaciones", "El mismo proveedor y los mismos controles operativos. Las certificaciones de las instalaciones estadounidenses están disponibles a petición."),
        ("Privacidad estatal", "CCPA y CPRA, y las leyes estatales posteriores, se cubren con los mismos términos escritos de tratamiento, no con un régimen distinto por estado."),
        ("Revisión de seguridad", "Certificaciones, informes de auditoría y detalles de alojamiento se facilitan a petición y se adjuntan al acuerdo."),
        ("Portabilidad", "Los mismos derechos de exportación y salida que los clientes de la UE. No se retiene ni se rebaja nada por región.")],
    at=['Acuerdo de tratamiento de datos, con los roles por escrito', 'Lista vigente de subencargados, con aviso de cambios', 'Certificaciones, informes de auditoría y región de alojamiento', 'Compromisos de disponibilidad y soporte, por nivel', 'Política de retención, borrado y copias de seguridad', 'Exportación en formatos abiertos, en cualquier momento y al salir'],
    nfh="Dónde no somos la opción correcta",
    nfa="Todos los proveedores dicen que encajan contigo. Esta es la lista corta de casos en que no lo hacemos, para que salga ahora y no en el segundo mes de una implementación.",
    nf=[('Vendes únicamente a consumidores', 'La mayor parte del producto es maquinaria mayorista que un catálogo de consumo nunca toca.'),
        ('Tu catálogo es pequeño y tus pedidos simples', 'Unas docenas de SKUs y pedidos de una línea no necesitan esto.'),
        ('No tienes ERP ni planeas tenerlo', 'Buena parte del valor está en la sincronización bidireccional con un sistema de registro.')],
    nfn="Vender al por mayor y directo al consumidor a la vez es habitual. Aquí no supone una limitación: el canal de consumo se alimenta del mismo catálogo y de la misma conexión con el ERP que el mayorista.",
    cdh="Lo que cuesta esperar",
    cd="Sumen lo que sumen las cuatro palancas, son cifras anuales. Un trimestre de deliberación cuesta un trimestre de ese número, y la fuga no se detiene mientras evalúas. Ese es el argumento honesto para empezar un piloto ahora en vez de un ciclo de compras dentro de seis meses.",
    tlh="Cuánto tarda hasta que alguien lo usa de verdad",
    tl=[("Adobe Commerce", "12&ndash;24 semanas", 100),
        ("BigCommerce Enterprise + B2B Edition", "10&ndash;20 semanas", 83),
        ("Shopify Plus (con agencia y apps)", "8&ndash;16 semanas", 67),
        ("RocketX — piloto en vivo", "4&ndash;6 semanas", 25)],
    tln="Las cifras de competidores son referencias habituales de mercado medio hasta la puesta en marcha, según guías de plataformas y agencias de 2026. El alcance las mueve en ambos sentidos, y el trabajo de ERP es donde más se desbordan. La cifra de RocketX corresponde a un piloto en vivo con un grupo de compradores definido, no al despliegue completo. En las alternativas, la facturación suele empezar mucho antes de que alguien pida. En la nuestra empieza en la puesta en marcha.",
    sbh="No se apaga nada",
    sba="La objeción habitual a una decisión de plataforma es que implica reemplazar una. Esta no. RocketX se despliega junto a lo que ya operas, y ambos siguen funcionando.",
    sb=[("Tu tienda web actual sigue funcionando", "RocketX se pone en marcha al lado, no encima. No se da de baja nada para hacer sitio, y ningún catálogo tiene que migrarse antes de que alguien pueda pedir."),
        ("Eligen tus compradores, no tú", "Algunos pasan a la app la primera semana. Otros se quedan en la tienda que ya conocen. Ambos producen pedidos que llegan al mismo ERP, en el mismo formato y con las mismas condiciones, así que aguas abajo no cambia nada."),
        ("Sin fin de semana de migración", "No hay ventana de migración ni congelación de pedidos. El modo de fallo que hace temer estos proyectos — un domingo malo y los teléfonos sonando el lunes — no está sobre la mesa. No hay nada que migrar."),
        ("La adopción se convierte en evidencia", "Como ambos funcionan a la vez, puedes ver cuál usan realmente tus compradores. Ese es mejor argumento a favor o en contra nuestra que cualquier cosa en este documento."),
        ("Retira el sistema antiguo más tarde, o nunca", "Nada en el acuerdo fija una fecha para apagarlo. Si dentro de tres años sigue mereciendo la pena, déjalo funcionando.")],
    sbn="Esta es además la forma más barata de equivocarse con nosotros. Si el piloto no funciona, no apagas nada, no has perdido pedidos, y la alternativa es el sistema que ya estabas usando.",
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
           "¿Cuándo empieza la facturación: en la firma o en la puesta en marcha?",
           "¿Qué pasa con nuestros datos e integraciones si nos vamos?"],
    ctah="Siguiente paso",
    ctap="Una demo personalizada sobre su propio catálogo, una auditoría breve de los sistemas y un piloto de bajo riesgo con resultados medibles en semanas.",
    contact="app@rocketx.app",
    srch="Fuentes",
    src="Digital Commerce 360 / Departamento de Comercio de EE. UU. para los totales y el crecimiento del comercio electrónico B2B. Baymard Institute para la tasa de abandono de carrito, promediada en 50 estudios (2006-2025); esa cifra cubre todo el comercio electrónico y no está segmentada para B2B. Gartner para el tamaño del grupo de compra en una adquisición B2B compleja. Esfuerzo de gestión de devoluciones según las referencias de distribución de la B2B E-commerce Association. McKinsey B2B Pulse, novena encuesta anual a 3.942 responsables de decisión B2B en 13 países, para los valores de pedido digital. Sensor Tower, State of Mobile 2026, para la porción del tiempo móvil fuera del navegador; esta cifra cubre todo el uso del smartphone, no específicamente pedidos B2B. Boston Consulting Group con Google, «Mobile Marketing and the New B2B Buyer» (2017), para la porción de ingresos B2B del móvil. Referencias de retención de Airship para notificaciones. Los plazos de implementación reflejan referencias de mercado 2026 para proyectos B2B de mercado medio y varían según el alcance.",
    foot="RocketX LLC · app@rocketx.app · rocketx.app",
    pg="Página",
)

C["nl"] = dict(
    lang="nl", file="rocketx-business-case-nl",
    doctitle="RocketX — De business case voor modern B2B-bestellen",
    kicker="INTERNE BESLUITVORMING",
    title="De business case voor modern B2B-bestellen",
    sub="Voor teams in groothandel, distributie en productie die bekijken hoe hun klanten bestellen.",
    forwho="Voor groothandel en distributie met 15–250 miljoen euro omzet",
    date="Editie 2026",
    xsh="Op één pagina",
    xsa="Als je maar één pagina leest: groothandelsorders lekken weg in de winkelwagen, aan de telefoon en bij de retourbalie. Dit is een voorstel om dat te stoppen — waarbij het platform zich bewijst voordat het iets kost.",
    xs=[("Het probleem", "Je inkopers stellen orders samen op een plek die niemand aan jouw kant ziet. In een browsertabblad dat ze elke keer moeten zoeken. Waarin ze elke keer opnieuw moeten inloggen. En het werk zelf gebeurt ergens anders: op een telefoon, in een magazijngang, op een laadperron. Winkelwagens sterven met de sessie. Eén persoon bouwt wat zes tot tien mensen beslissen. En de dubbele bestelling die niemand zag komt terug als retour."),
        ("Wat er verandert in de winkelwagen", "Winkelwagens blijven op de server bestaan en synchroniseren live tussen de webshop en de native apps. Je buitendienst ziet lopende klantwinkelwagens, inclusief wat vastloopt, en kan ingrijpen voordat er een afkoelt. Het hele inkoopteam werkt aan één order, elke wijziging op naam. En de winkelwagen meldt een SKU die het account kort geleden al kocht, vóór het verzenden."),
        ("Wat er verandert op de telefoon van de inkoper", "Je catalogus staat op het beginscherm, één tik van een nabestelling en al ingelogd. Niet achter een bladwijzer en een login. Push haalt inkopers terug wanneer voorraad terug is of een contract afloopt — daar waar mail wordt gefilterd. Barcodes scannen bestelt direct na vanaf een schaplabel. En de catalogus staat lokaal: een gang zonder bereik is nog steeds een gang waaruit je bestelt. Je gedrukte brochures, productvideo's en andere rijke content reizen mee in dezelfde app, zodat het showroommateriaal bij de inkoper is als het gesprek plaatsvindt. Native voor iOS en Android, geen website in een omhulsel. Zo houdt nabestellen op een klusje te zijn en wordt het een gewoonte. Daar komt herhaalomzet vandaan."),
        ("Waarom dit standhoudt", "Onbeperkt SKU's en onbeperkt plaatsen. Nooit per stuk afgerekend, nooit een percentage van je omzet. Standaardkoppelingen voor ERP en CRM zitten erbij. RocketX gaat vóór je bronsystemen staan in plaats van ze te vervangen. En het draait naast je bestaande webshop: er gaat niets uit."),
        ("Wat een poging kost", "Inrichtingskosten kwijtgescholden bij jaarplannen. Facturatie start bij livegang, niet bij ondertekening. Een pilot van 30 tot 45 dagen met afgesproken meetpunten voor elke langere verbintenis."),
        ("De één-procenttest", "Zet de platformkosten uit je offerte naast één procent van je jaaromzet — of naast de marge op één procent, als je het behoudend wilt rekenen. De enige vraag die overblijft is of beter bestellen je meer waard is dan dat. Zo ja, dan is de rest van dit document detail en geen overtuigingswerk.")],
    p1h="Waarom dit nu op tafel ligt",
    p1a="B2B-inkoop is online gegaan terwijl de groothandel als geheel nauwelijks groeit. De groei zit niet in meer klanten. Hij zit erin dat dezelfde klanten een groter deel digitaal bestellen — en hun leverancier kiezen op hoe makkelijk dat gaat.",
    stats=[("90.000", "groothandels in Nederland — de omzet van de sector groeide in 2025 met slechts 0,9%"),
           ("31%", "van de Nederlandse bedrijven vanaf tien werknemers verkoopt al elektronisch"),
           ("94%", "van de tijd op een telefoon wordt in apps doorgebracht, niet in een browser"),
           ("> 40%", "van de omzet bij toonaangevende B2B-bedrijven wordt door mobiel gedreven of beïnvloed")],
    p1b="De praktische gevolgtrekking: de bestelervaring is geen achterafsysteem meer. Het is het oppervlak waarop je klanten je beoordelen — en het moment waarop ze besluiten of ze nabestellen of iemand anders bellen.",
    p2h="Wat de huidige inrichting meestal kost",
    p2a="De meeste groothandels in het middensegment draaien op één van drie dingen. Een verouderd ERP-portaal. Een algemeen e-commerceplatform dat iemand tot B2B heeft omgebogen. Of orderinvoer per telefoon en mail. Elke variant kost geld dat zelden als post op een factuur staat.",
    costs=[("Catalogusprestaties", "Platformen die voor consumentenhandel zijn gebouwd worden traag bij groothandelscatalogi. Inkopers breken het zoeken af en bellen een vertegenwoordiger — een selfserviceorder wordt daarmee een bemande order."),
           ("Licenties per gebruiker", "Prijzen per gebruiker betekenen dat magazijn, buitendienst en de mensen bij je klant gerantsoeneerd worden. Precies wie het systeem het meest zou gebruiken, valt buiten de boot."),
           ("Vergoedingen over je omzet", "Kosten die aan je ordervolume hangen stijgen juist wanneer het goed gaat. Groei wordt belast in plaats van ondersteund."),
           ("Doorlooptijd van de implementatie", "B2B-trajecten in het middensegment op algemene platformen duren doorgaans vier tot acht maanden of langer tot livegang. Het integratiewerk loopt de hele rit mee op de factuur."),
           ("Handmatig cataloguswerk", "Productdata die met de hand worden bijgehouden over pdf\'s, spreadsheets en het ERP kosten doorlopend personeelstijd en lopen tóch achter.")],
    p3h="Wat RocketX verandert",
    caps=[("Onbeperkt SKU's, zoeken binnen een seconde", "Of de catalogus nu achthonderd SKU's telt of acht miljoen: filteren en bestellen in milliseconden — en nooit betalen per SKU. Prestaties die andere platformen op deze schaal niet halen."),
          ("Native iOS- en Android-apps", "Speciaal gebouwd voor B2B-bestellingen, geen ingepakte website. De hele catalogus in de zak van de inkoper."),
          ("Onbeperkt plaatsen en gebruikers", "Elke medewerker, vertegenwoordiger en geautoriseerde klant krijgt volledige toegang. Geen kosten per gebruiker, geen kosten per SKU, geen rantsoenering."),
          ("Realtime samenwerken in de winkelwagen", "Meerdere teamleden werken tegelijk in dezelfde winkelwagen, met elke handeling vastgelegd: wie, wat en wanneer."),
          ("Klantspecifieke prijzen", "Elke inkoper ziet automatisch zijn eigen afgesproken prijzen, staffels en contractvoorwaarden."),
          ("Live voorraad over alle magazijnen", "Actuele voorraad en beschikbaarheid, zodat inkopers niet meer bestellen wat niet geleverd kan worden."),
          ("Rechtstreeks bestellen vanuit pdf's", "AI leest bestaande brochures en catalogi zodat inkopers er direct uit bestellen — zonder opnieuw intikken."),
          ("Je brochures en video's, in de zak van de inkoper", "Publiceer bestaande gedrukte brochures als pdf, productvideo's en andere rijke content naast de catalogus. Het synchroniseert naar de native apps en opent ook zonder bereik, zodat je showroommateriaal met de inkoper meereist."),
          ("Eerst groothandel, je consumentenkanaal erbij", "Het product is gebouwd rond groothandelsbestellingen. Verkoop je daarnaast rechtstreeks aan consumenten, dan draait dat kanaal op dezelfde catalogus en dezelfde ERP-koppeling. Geen tweede platform, geen tweede set productdata."),
          ("Diepe ERP- en CRM-koppeling", "RocketX gaat vóór je ERP staan in plaats van het te vervangen. Producten, klantspecifieke prijzen en live voorraad gaan eruit, uit NetSuite, SAP, Microsoft Dynamics of Epicor; winkelwagens, orders en goedkeuringen gaan terug. Standaardkoppelingen zitten in elk plan.")],
    cmh="Twee vennootschappen, twee rechtsgebieden, per stuk één antwoord",
    cma="De toets op gegevens en beveiliging is meestal het traagste deel van een beoordeling. Wij vermeden dat door Europese gegevens nooit naar Amerika te brengen.",
    eu_f="Voor klanten in de Europese Unie",
    eu_h="Je contracteert met RocketX Limited",
    eu=[("Wederpartij", "Een Ierse vennootschap, opgericht en actief in de Europese Unie naar EU-recht, los van de Amerikaanse entiteit."),
        ("Datalocatie", "Klantgegevens blijven in de Europese Unie: opslag, verwerking en back-ups. Geen replicatie naar de Verenigde Staten."),
        ("Certificeringen", "EU-datacenters met ISO/IEC 27001:2022 en BSI C5 Type 2."),
        ("AVG", "Geldt rechtstreeks voor de samenwerking. Jij bent verwerkingsverantwoordelijke voor je klant- en ordergegevens; wij zijn verwerker en handelen op jouw gedocumenteerde instructie."),
        ("Doorgiftetoets", "Je wederpartij is een EU-vennootschap, dus de beoordeling begint niet met een vraag over hoofdstuk V. Precies daar verliezen trajecten met Amerikaanse leveranciers meestal een maand."),
        ("Subverwerkers", "Volledig openbaar gemaakt, met bericht vooraf bij wijziging en een contractueel recht van bezwaar.")],
    us_f="Voor klanten in de Verenigde Staten",
    us_h="Je contracteert met RocketX LLC",
    us=[("Wederpartij", "RocketX LLC, de Amerikaanse vennootschap. Hetzelfde platform, dezelfde toezeggingen, recht van je eigen vestigingsplaats."),
        ("Datalocatie", "Klantgegevens blijven in de Verenigde Staten: opslag, verwerking en back-ups. Geen replicatie naar de EU."),
        ("Certificeringen", "Dezelfde provider en dezelfde operationele controles. Attesten van de Amerikaanse faciliteiten zijn op aanvraag beschikbaar."),
        ("Privacywetgeving per staat", "CCPA en CPRA en de opvolgende staatswetten worden gedekt door dezelfde schriftelijke verwerkingsvoorwaarden, niet door een apart regime per staat."),
        ("Beveiligingstoets", "Certificeringen, auditrapporten en gegevens over hosting verstrekken we op verzoek; ze worden onderdeel van de overeenkomst."),
        ("Overdraagbaarheid", "Dezelfde export- en uittredingsrechten als EU-klanten. Er wordt per regio niets achtergehouden of afgezwakt.")],
    ath="Wordt in beide rechtsgebieden onderdeel van de overeenkomst",
    at=["Verwerkersovereenkomst met de rollen op papier",
        "Actuele lijst van subverwerkers, met bericht bij wijziging",
        "Certificeringen, auditrapporten en hostingregio",
        "Toezeggingen over beschikbaarheid en support, per niveau",
        "Bewaar-, verwijder- en back-upbeleid",
        "Export in open formaten, op elk moment en bij uittreding"],
    cmn="Geef deze pagina aan wie je beveiligingstoets doet. We beantwoorden de vragenlijst liever in week één dan in week negen.",
    p4h="Waarom de native app commercieel telt",
    p4a="Een responsieve website en een native app zijn niet hetzelfde product. Bij terugkerende groothandelsbestellingen zie je het verschil rechtstreeks terug in de bestelfrequentie.",
    native=[("Nabestellen is een gewoonte, geen zoektocht", "De meeste B2B-orders zijn herhaalorders. In een browser moet de inkoper elke keer de bladwijzer zoeken, de site laden en inloggen. Een app is één tik, al ingelogd — die wrijving verdwijnt bij elke nabestelling, blijvend."),
            ("Een vaste plek op de telefoon van de inkoper", "Je icoon staat op het beginscherm. Concurrenten moeten telkens opnieuw gezocht en gevonden worden."),
            ("Push bereikt inkopers die mail niet bereikt", "Meldingen over voorraad die terug is, contractverlengingen en nabestelmomenten komen rechtstreeks binnen. Gebruikers die push aanzetten blijven twee tot drie keer zo lang actief."),
            ("Het werk gebeurt niet achter een bureau", "Inkopers bestellen vanuit magazijngangen, van laadperrons en van de beursvloer. Native toegang tot de camera betekent barcodes scannen en nabestellen vanaf een schaplabel."),
            ("Hij overleeft het wegvallen van bereik", "Hallen met stalen wanden en landelijke routes kosten bereik. Catalogus, prijzen, winkelwagen en je brochures en productvideo's blijven lokaal en synchroniseren zodra de verbinding terug is.")],
    p8h="Waar de order werkelijk verloren gaat",
    p8a="De meeste beoordelingen vergelijken catalogi en afrekenen. Het geld lekt op een minder zichtbare plek weg: in de winkelwagen, tussen het moment waarop een inkoper begint en het moment waarop iemand verzendt.",
    cart=[("Een half opgebouwde order is onzichtbaar", "Ongeveer 70% van de online winkelwagens wordt verlaten. Op de meeste platformen kan niemand aan jouw kant er één zien voordat het een order wordt. Een vastgelopen winkelwagen ziet er precies zo uit als helemaal geen winkelwagen."),
          ("Winkelwagens sterven met de sessie", "Browserwinkelwagens hangen aan een apparaat en een sessie. Een inkoper die in het magazijn wordt onderbroken vindt een lege mand terug en bouwt hem telefonisch opnieuw op — of laat het."),
          ("Eén persoon bouwt wat zes tot tien beslissen", "Gartner legt een complexe B2B-aankoop bij zes tot tien mensen. Kan er maar één bij de winkelwagen, dan wordt de order per mail bijeengeraapt, overgetikt en komt hij onvolledig binnen."),
          ("De dubbele bestelling die niemand zag wordt een retour", "Als collega\'s bij dezelfde klant elkaars orders niet zien, wordt dezelfde SKU twee keer besteld. Dat is de duurste transactie die je kunt maken."),
          ("Wat RocketX in plaats daarvan doet", "Winkelwagens blijven op de server bestaan en synchroniseren live tussen webshop en native apps. Je buitendienst ziet lopende klantwinkelwagens inclusief wat vastloopt en kan ingrijpen voordat het afkoelt. Het hele inkoopteam werkt in één winkelwagen met elke wijziging op naam. En de winkelwagen wijst op een SKU die het account kort geleden al kocht, vóór het plaatsen.")],
    p9h="Hoe je dit voor je eigen bedrijf berekent",
    p9a="Geen twee distributeurs verliezen waarde in dezelfde verhoudingen. De eerlijke versie van deze pagina is daarom een rekenblad en geen belofte. Vul je eigen cijfers in; de rekensom is bewust simpel.",
    levers=[("Teruggehaalde winkelwagens", "Winkelwagens per maand &times; aandeel dat wordt verlaten &times; gemiddelde orderwaarde &times; het deel dat je buitendienst nu redt omdat hij ze eindelijk ziet."),
            ("Vermeden retouren", "Retouren per maand &times; het aandeel door een dubbele bestelling of verkeerd artikel &times; je volledig belaste kosten per retour. Reken de arbeid mee: één retour kost de afhandeling van acht tot tien normale orders."),
            ("Vrijgespeelde uren buitendienst", "Medewerkers &times; uren per week aan orders opnemen en overtikken &times; belaste uurkosten &times; 52. Elk uur dat uit orderinvoer verdwijnt is een uur dat naar verkopen kan."),
            ("Ordergrootte", "Gemiddelde orderwaarde &times; de stijging die je verwacht. De hele catalogus is in seconden doorzoekbaar, plaatsen zijn onbeperkt, en nabestellen kan vanaf elk apparaat.")],
    cdh="Wat wachten kost",
    cd="Wat de vier knoppen samen ook opleveren, het zijn jaarbedragen. Een kwartaal beraad kost een kwartaal van dat getal, en het lek pauzeert niet terwijl je aan het beoordelen bent. Dat is het eerlijke argument om nu een pilot te starten in plaats van over zes maanden een inkooptraject.",
    p9n="Tegenover die vier zet je de platformkosten en de implementatie-inspanning uit je offerte. Dekken de eerste twee alleen de kosten al niet, dan heb je de andere twee niet nodig.",
    sbh="Er wordt niets uitgezet",
    sba="Het gebruikelijke bezwaar tegen een platformbeslissing is dat er een platform vervangen moet worden. Bij deze niet. RocketX wordt ingevoerd naast wat je vandaag draait, en allebei blijven werken.",
    sb=[("Je huidige webshop blijft draaien", "RocketX gaat ernaast live, niet erbovenop. Er wordt niets uitgezet om ruimte te maken, en geen catalogus hoeft gemigreerd te worden voordat iemand kan bestellen."),
        ("Je inkopers kiezen, jij niet", "Sommigen stappen in de eerste week over op de app. Anderen blijven bij de shop die ze kennen. Beiden leveren orders die in hetzelfde ERP landen, in hetzelfde formaat, op dezelfde voorwaarden — stroomafwaarts verandert er dus niets."),
        ("Geen migratieweekend", "Er is geen migratievenster en geen bestelstop. De faalsituatie die zulke projecten eng maakt, is niet aan de orde: een slechte zondag en maandag rinkelende telefoons. Er valt simpelweg niets om te zetten."),
        ("Gebruik wordt het bewijs", "Omdat allebei tegelijk draaien, kun je zien wat je inkopers werkelijk gebruiken. Dat is een beter argument vóór of tegen ons dan wat dan ook in dit document."),
        ("Het oude systeem later uitzetten, of nooit", "Nergens in de overeenkomst staat daarvoor een datum. Verdient het over drie jaar nog zijn plek, dan laat je het draaien.")],
    sbn="Dit is meteen de goedkoopste manier om je in ons te vergissen. Werkt de pilot niet, dan zet je niets uit, ben je geen order kwijt, en is de terugval het systeem dat je toch al gebruikte.",
    p5h="Hoe de commerciële voorwaarden het risico verkleinen",
    p5a="De opzet van de overeenkomst is zo gemaakt dat het platform zich bewijst voordat het iets kost. Hier staan bewust geen bedragen — de actuele prijzen vind je op de website en in je offerte. De grafiek hieronder laat alleen zien wat de kosten als aandeel van je omzet betekenen.",
    terms=[("Vast tarief, nooit een percentage van je omzet", "De platformkosten stijgen niet omdat je ordervolume is gestegen. Groei wordt niet belast."),
           ("Onbeperkt SKU\'s en plaatsen inbegrepen", "Er wordt niets per stuk afgerekend. Geen prijzen per gebruiker of per SKU om over te onderhandelen of te rantsoeneren als catalogus en team groeien."),
           ("Inrichtings- en integratiekosten kwijtgescholden bij jaarplannen", "De implementatiekosten die zulke projecten normaal vooraf belasten, vervallen."),
           ("Facturatie start bij livegang, niet bij ondertekening", "Je betaalt niets tot het platform live staat en waarde levert."),
           ("Pilot van 30–45 dagen met gezamenlijke ROI-evaluatie", "Een afgebakende beoordelingsperiode met afgesproken maatstaven, vóór een langere verbintenis."),
           ("Native apps en standaardkoppelingen inbegrepen", "Niet verkocht als extra modules bovenop een basislicentie.")],
    p6h="Hoe de invoering verloopt",
    steps=[("1. Doorlichting van de systemen", "We brengen de bestaande catalogus, prijsregels, het ERP en de orderstroom in kaart en bepalen wat mee moet en wat blijft."),
           ("2. Koppeling", "De tweewegsynchronisatie wordt tegen je ERP en CRM gebouwd. Standaardkoppelingen dekken de grote systemen; alles daarbuiten wordt als afgebakend blok werk geoffreerd."),
           ("3. Catalogus inlezen", "Bestaande pdf\'s, brochures en productdata worden ingelezen. Geen handmatig overtikken van de catalogus."),
           ("4. Pilot", "Een live pilot van 30–45 dagen met een afgebakende groep inkopers en afgesproken succesmaatstaven."),
           ("5. Livegang en evaluatie", "Volledige uitrol, met een gezamenlijke ROI-evaluatie tegen de maatstaven die bij de pilot zijn afgesproken.")],
    tlh="Hoe lang duurt het voor iemand het echt gebruikt",
    tl=[("Adobe Commerce", "12&ndash;24 weken", 100),
        ("BigCommerce Enterprise + B2B Edition", "10&ndash;20 weken", 83),
        ("Shopify Plus (met bureau en apps)", "8&ndash;16 weken", 67),
        ("RocketX — live pilot", "4&ndash;6 weken", 25)],
    tln="De cijfers van concurrenten zijn gangbare benchmarks voor het middensegment tot livegang, uit platform- en bureaugidsen van 2026. De scope verschuift ze beide kanten op. Het ERP-werk loopt het vaakst uit. Het cijfer van RocketX gaat over een live pilot met een afgebakende groep inkopers, niet over de volledige uitrol. Bij de alternatieven begint de facturatie meestal ruim voordat iemand iets bestelt. Bij ons begint hij bij livegang.",
    nfh="Waar wij niet de juiste keuze zijn",
    nfa="Elke leverancier zegt dat hij bij je past. Dit is de korte lijst van gevallen waarin dat niet zo is, zodat het nu boven tafel komt en niet in maand twee van een invoering.",
    nf=[("Je verkoopt uitsluitend aan consumenten", "Het grootste deel van het product is groothandelsmachinerie waar een consumentencatalogus nooit aan komt."),
        ("Je catalogus is klein en je orders zijn eenvoudig", "Een paar dozijn SKU\'s en orders van één regel hebben dit niet nodig."),
        ("Je hebt geen ERP en bent er ook geen van plan", "Een groot deel van de waarde hier zit in tweewegsynchronisatie met een bronsysteem.")],
    nfn="Aan de groothandel én rechtstreeks verkopen is heel gewoon. Hier is het geen beperking: het consumentenkanaal draait op dezelfde catalogus en dezelfde ERP-koppeling als de groothandel.",
    p7h="Vragen die je elke leverancier zou moeten stellen",
    quest=["Verandert de platformvergoeding als ons ordervolume groeit?",
           "Kan onze buitendienst de winkelwagen van een klant zien voordat het een order wordt?",
           "Overleeft een winkelwagen een gesloten browser, een lege accu, een ander apparaat?",
           "Kunnen meerdere mensen bij dezelfde klant samen één order opbouwen?",
           "Waarschuwt het systeem als dezelfde SKU kort geleden al is besteld?",
           "Worden buitendienstmedewerkers en de mensen bij onze klanten als gebruikers gerekend?",
           "Hoe snel reageert het zoeken bij onze werkelijke catalogusgrootte, niet bij een democatalogus?",
           "Zijn de mobiele apps native of een website in een omhulsel?",
           "Werkt de catalogus als een inkoper geen bereik heeft?",
           "Wanneer start de facturatie — bij ondertekening of bij livegang?",
           "Wat gebeurt er met onze gegevens en koppelingen als we weggaan?"],
    ctah="Volgende stap",
    ctap="Een persoonlijke demo op je eigen catalogus. Een korte doorlichting van je systemen. En een pilot met weinig risico — meetbare resultaten binnen weken.",
    contact="app@rocketx.app",
    srch="Bronnen",
    src="CBS voor het aantal groothandels in Nederland, de omzetontwikkeling van de sector en het aandeel bedrijven met elektronische verkoop. Baymard Institute voor het verlatingspercentage van winkelwagens, gemiddeld over 50 studies (2006–2025); dat cijfer gaat over de hele e-commerce en is niet naar B2B uitgesplitst. Gartner voor de omvang van het inkoopteam bij een complexe B2B-aankoop. McKinsey B2B Pulse, negende jaarlijkse enquête onder 3.942 B2B-beslissers in 13 landen. Sensor Tower, State of Mobile 2026, voor het aandeel telefoontijd buiten de browser; dat cijfer gaat over al het telefoongebruik, niet specifiek over B2B-bestellingen. Boston Consulting Group met Google, „Mobile Marketing and the New B2B Buyer” (2017), voor het mobiele aandeel in de B2B-omzet. Afhandelingslast van retouren volgens de distributiebenchmarks van de B2B E-commerce Association. Doorlooptijden weerspiegelen marktbenchmarks 2026 voor B2B-trajecten in het middensegment en variëren met de scope.",
    foot="RocketX LLC · app@rocketx.app · rocketx.app",
    pg="Pagina",
)

# ---------------------------------------------------------------- template

# ---------------------------------------------------------------- figures
import sys, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deck_figs

def _site_dg():
    """Diagram labels live in index.html, so the deck cannot drift from the site."""
    src = io.open(os.path.join(os.path.dirname(OUT), "index.html"), encoding="utf-8").read()
    all_ = json.loads(re.search(r"const I18N=(\{.*?\});\n", src, re.S).group(1))
    return dict((L, dict((k, v) for k, v in all_[L].items() if k.startswith("dg."))) for L in all_)

DG = _site_dg()

FIGTXT = {
"en": dict(
  fg1_bands=[15, 50, 120, 300], fg1_fees=[64800, 91800, 129600], fg1_cap=480000,
  fg1_dec=".", fg1_sp="",
  fg1_rx="RocketX, annual plan",
  fg1_sh="A percentage-of-sales plan, 0.25%",
  fg1_x="annual sales running through the platform ($M)",
  fg1_y="platform fee as a share of those sales",
  fg1_n="Percentage line: Shopify Plus variable platform fee, 0.25% of online sales above roughly $1M a month, capped at $40,000 a month - hence the flat section and then the bend. RocketX steps down at each band, so the fee falls as you grow rather than tracking you upward.",
  fg2_ha="A replacement project", fg2_la="one track",
  fg2_old="your current system, still the only one that works",
  fg2_new="the new one, live", fg2_cut="cutover weekend, week 12-24",
  fg2_hb="RocketX, deployed alongside", fg2_l1="track 1", fg2_l2="track 2",
  fg2_t1="your existing web shop - nothing is switched off",
  fg2_t2="RocketX web shop and native apps - live in weeks",
  fg2_n="No switchover point exists, so there is nothing to fail on a Monday.",
  fg3_n="Standard connectors are included in every plan. Work beyond standard scope is quoted as a defined block before it starts.",
  fg4_a="order started", fg4_b="order submitted", fg4_gap="~70% never arrives",
  fg4_inv="and on most platforms nobody on your side can see any of it",
  fg4_c1="the cart dies with the session",
  fg4_c2="one person builds what six to ten people decide",
  fg4_c3="the duplicate nobody caught becomes a return"),
"de": dict(
  fg1_bands=[15, 45, 105, 250], fg1_fees=[54000, 75600, 108000], fg1_cap=480000,
  fg1_dec=",", fg1_sp=" ",
  fg1_rx="RocketX, Jahresplan",
  fg1_sh="Umsatzbeteiligung, 0,25 %",
  fg1_x="Jahresumsatz \u00fcber die Plattform (Mio. \u20ac)",
  fg1_y="Plattformgeb\u00fchr als Anteil an diesem Umsatz",
  fg1_n="Prozentlinie: Shopify Plus, variable Plattformgeb\u00fchr von 0,25 % des Online-Umsatzes oberhalb von rund 1 Mio. pro Monat, gedeckelt bei 40.000 pro Monat - daher der flache Teil und dann der Knick. RocketX sinkt mit jeder Stufe, die Geb\u00fchr f\u00e4llt also mit Ihrem Wachstum, statt mitzuwachsen.",
  fg2_ha="Ein Abl\u00f6seprojekt", fg2_la="ein Strang",
  fg2_old="Ihr jetziges System, weiterhin das einzige, das l\u00e4uft",
  fg2_new="das neue, live", fg2_cut="Umstellungswochenende, Woche 12-24",
  fg2_hb="RocketX, parallel ausgerollt", fg2_l1="Strang 1", fg2_l2="Strang 2",
  fg2_t1="Ihr bestehender Webshop - nichts wird abgeschaltet",
  fg2_t2="RocketX Webshop und native Apps - in Wochen live",
  fg2_n="Es gibt keinen Umstellungspunkt, also nichts, was am Montag scheitern kann.",
  fg3_n="Standard-Konnektoren sind in jedem Plan enthalten. Arbeiten \u00fcber den Standardumfang hinaus werden vorab als definiertes Paket angeboten.",
  fg4_a="Bestellung begonnen", fg4_b="Bestellung abgeschickt", fg4_gap="~70 % kommen nie an",
  fg4_inv="und auf den meisten Plattformen sieht davon auf Ihrer Seite niemand etwas",
  fg4_c1="der Warenkorb stirbt mit der Sitzung",
  fg4_c2="einer baut, was sechs bis zehn entscheiden",
  fg4_c3="die \u00fcbersehene Dublette wird zur Retoure"),
"es": dict(
  fg1_bands=[15, 50, 120, 300], fg1_fees=[64800, 91800, 129600], fg1_cap=480000,
  fg1_dec=",", fg1_sp=" ",
  fg1_rx="RocketX, plan anual",
  fg1_sh="Plan por porcentaje de ventas, 0,25 %",
  fg1_x="ventas anuales a trav\u00e9s de la plataforma ($M)",
  fg1_y="cuota de plataforma como parte de esas ventas",
  fg1_n="L\u00ednea de porcentaje: Shopify Plus, tarifa variable de plataforma del 0,25 % de las ventas online por encima de aproximadamente 1M al mes, con tope de 40.000 al mes - de ah\u00ed el tramo plano y luego el quiebre. RocketX baja en cada tramo, as\u00ed que la cuota cae seg\u00fan creces en vez de seguirte hacia arriba.",
  fg2_ha="Un proyecto de sustituci\u00f3n", fg2_la="una v\u00eda",
  fg2_old="tu sistema actual, todav\u00eda el \u00fanico que funciona",
  fg2_new="el nuevo, en marcha", fg2_cut="fin de semana de migraci\u00f3n, semana 12-24",
  fg2_hb="RocketX, desplegado en paralelo", fg2_l1="v\u00eda 1", fg2_l2="v\u00eda 2",
  fg2_t1="tu tienda web actual - no se apaga nada",
  fg2_t2="tienda web y apps nativas de RocketX - en marcha en semanas",
  fg2_n="No existe un punto de migraci\u00f3n, as\u00ed que no hay nada que pueda fallar un lunes.",
  fg3_n="Los conectores est\u00e1ndar est\u00e1n incluidos en todos los planes. El trabajo fuera del alcance est\u00e1ndar se cotiza como un bloque definido antes de empezar.",
  fg4_a="pedido iniciado", fg4_b="pedido enviado", fg4_gap="~70 % nunca llega",
  fg4_inv="y en la mayor\u00eda de plataformas nadie de tu lado ve nada de esto",
  fg4_c1="el carrito muere con la sesi\u00f3n",
  fg4_c2="una persona arma lo que deciden seis a diez",
  fg4_c3="el duplicado que nadie vio acaba en devoluci\u00f3n"),
"nl": dict(
  fg1_bands=[15, 45, 105, 250], fg1_fees=[54000, 75600, 108000], fg1_cap=480000,
  fg1_dec=",", fg1_sp="",
  fg1_rx="RocketX, jaarplan",
  fg1_sh="Percentage van de omzet, 0,25%",
  fg1_x="jaaromzet via het platform (mln \u20ac)",
  fg1_y="platformkosten als aandeel van die omzet",
  fg1_n="Percentagelijn: Shopify Plus, variabele platformkosten van 0,25% van de online omzet boven ongeveer 1 mln per maand, met een plafond van 40.000 per maand - vandaar het vlakke deel en dan de knik. RocketX zakt bij elke schijf, dus de kosten dalen naarmate je groeit in plaats van mee te stijgen.",
  fg2_ha="Een vervangingsproject", fg2_la="\u00e9\u00e9n spoor",
  fg2_old="je huidige systeem, nog steeds het enige dat werkt",
  fg2_new="het nieuwe, live", fg2_cut="omschakelweekend, week 12-24",
  fg2_hb="RocketX, ernaast uitgerold", fg2_l1="spoor 1", fg2_l2="spoor 2",
  fg2_t1="je bestaande webshop - er wordt niets uitgezet",
  fg2_t2="RocketX-webshop en native apps - binnen weken live",
  fg2_n="Er is geen omschakelmoment, dus er is niets dat op maandag kan misgaan.",
  fg3_n="Standaardkoppelingen zitten in elk plan. Werk buiten de standaardscope wordt vooraf als een afgebakend blok geoffreerd.",
  fg4_a="bestelling gestart", fg4_b="bestelling verstuurd", fg4_gap="~70% komt nooit aan",
  fg4_inv="en op de meeste platforms ziet niemand aan jouw kant er iets van",
  fg4_c1="de winkelwagen sterft met de sessie",
  fg4_c2="\u00e9\u00e9n iemand bouwt wat zes tot tien beslissen",
  fg4_c3="het gemiste duplicaat wordt een retour"),
}
for _l, _kv in FIGTXT.items():
    C[_l].update(_kv)

CSS = """
@page{size:A4;margin:17mm 16mm 15mm}
*{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#1D4ED8;--sky:#2563EB;--ink:#0B1526;--body:#3B4A63;--soft:#6B7C99;--line:#DDE4F0;--tint:#F4F7FC}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"Inter",-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:var(--body);font-size:9.6pt;line-height:1.6}
h1,h2,h3,.num,.stat b{font-family:"Space Grotesk","Inter",-apple-system,Helvetica,Arial,sans-serif}
.page{page-break-after:always;position:relative;min-height:245mm}
.fig{display:block;width:100%;height:auto;margin-top:12px;page-break-inside:avoid}
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
.closing{margin-top:13px;background:var(--tint);border-radius:9px;padding:12px 14px;font-size:9.3pt;page-break-inside:avoid}
/* jurisdiction tracks */
.juris{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.jcol{border:1px solid var(--line);border-radius:9px;padding:13px 14px;page-break-inside:avoid}
.jcol:first-child{background:var(--tint);border-color:#C9D9F0}
.jflag{font-family:"IBM Plex Mono",monospace;font-size:7.2pt;letter-spacing:.16em;text-transform:uppercase;color:var(--blue);margin-bottom:4px}
.jcol h3{font-size:11pt;margin-bottom:9px}
.jrow{padding:5px 0;border-top:1px solid var(--line)}
.jrow:first-of-type{border-top:0;padding-top:2px}
.jrow b{display:block;font-size:8.6pt;color:var(--ink);font-weight:600}
.jrow span{display:block;font-size:8.5pt;color:var(--body);line-height:1.4;margin-top:2px}
.attach{margin-top:10px;border-top:1px solid var(--line);padding-top:8px}
.attach h3{font-family:"IBM Plex Mono",monospace;font-size:7.4pt;letter-spacing:.18em;text-transform:uppercase;color:var(--soft);font-weight:400;margin-bottom:5px}
.attach ul{display:grid;grid-template-columns:1fr 1fr;gap:2px 18px;list-style:none}
.attach li{font-size:8.5pt;color:var(--body);padding-left:12px;position:relative;line-height:1.32}
.attach li::before{content:"✓";position:absolute;left:0;color:var(--blue);font-weight:700}
/* exec summary */
.xs{display:grid;grid-template-columns:40mm 1fr;gap:14px;padding:10px 0;border-bottom:1px solid var(--line);page-break-inside:avoid}
.xs h3{font-size:10.4pt;color:var(--blue)}
.xs p{font-size:9.4pt;line-height:1.55}
/* time-to-live bars */
.tl{margin-top:14px}
.tlrow{margin-bottom:11px;page-break-inside:avoid}
.tllbl{display:flex;justify-content:space-between;font-size:9pt;margin-bottom:4px}
.tllbl b{font-weight:600;color:var(--ink)}
.tllbl span{font-family:"IBM Plex Mono",monospace;color:var(--soft);font-size:8.4pt}
.tlrail{height:7px;background:#E8EEF8;border-radius:99px;overflow:hidden}
.tlfill{height:100%;border-radius:99px;background:#C3D3EA}
.tlrow.rx .tlfill{background:var(--blue)}
.tlrow.rx .tllbl b{color:var(--blue)}
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

    # executive summary - the page a forwarded deck actually gets read
    xs = "".join('<div class="xs"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["xs"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["xsh"]), esc(d["xsa"]), xs))

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
    P.append('<div class="page"><h2>%s</h2><div class="caps">%s</div>%s</div>'
             % (esc(d["p3h"]), caps, deck_figs.fig_integration(DG[d["lang"]], d)))

    # p4 native
    nat = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["native"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div></div>'
             % (esc(d["p4h"]), esc(d["p4a"]), nat))

    # p8 the cart (placed before the commercial terms - it is the differentiator)
    cart = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["cart"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div>%s</div>'
             % (esc(d["p8h"]), esc(d["p8a"]), cart, deck_figs.fig_funnel(d)))

    # p9 sizing worksheet
    lv = "".join('<div class="lever"><h3>%s</h3><p>%s</p></div>' % (esc(a), b) for a, b in d["levers"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div style="margin-top:8px">%s</div>'
             '<div class="closing"><h3 style="margin-bottom:5px">%s</h3>%s</div>'
             '<div class="closing" style="margin-top:12px">%s</div></div>'
             % (esc(d["p9h"]), esc(d["p9a"]), lv, esc(d["cdh"]), esc(d["cd"]), esc(d["p9n"])))

    # runs alongside - the objection this whole category triggers
    sb = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["sb"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div>%s'
             '<div class="closing">%s</div></div>'
             % (esc(d["sbh"]), esc(d["sba"]), sb, deck_figs.fig_parallel(d), esc(d["sbn"])))

    # p5 terms
    tr = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["terms"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div>%s</div>'
             % (esc(d["p5h"]), esc(d["p5a"]), tr, deck_figs.fig_fee(d)))

    # p6 implementation
    st = "".join('<div class="step"><span class="num">%02d</span><div><h3>%s</h3><p>%s</p></div></div>'
                 % (i + 1, esc(a), esc(b)) for i, (a, b) in enumerate(d["steps"]))
    tl = "".join('<div class="tlrow%s"><div class="tllbl"><b>%s</b><span>%s</span></div>'
                 '<div class="tlrail"><div class="tlfill" style="width:%d%%"></div></div></div>'
                 % (" rx" if i == len(d["tl"]) - 1 else "", esc(a), b, w)
                 for i, (a, b, w) in enumerate(d["tl"]))
    P.append('<div class="page"><h2>%s</h2><div style="margin-top:20px">%s</div>'
             '<h3 style="margin-top:26px;font-size:12pt">%s</h3><div class="tl">%s</div>'
             '<p style="font-size:7.6pt;color:var(--soft);line-height:1.55;margin-top:12px">%s</p></div>'
             % (esc(d["p6h"]), st, esc(d["tlh"]), tl, esc(d["tln"])))

    # data, entities, compliance - split by jurisdiction
    def jcol(flag, head, rows, cls):
        r = "".join('<div class="jrow"><b>%s</b><span>%s</span></div>' % (esc(a), esc(b)) for a, b in rows)
        return ('<div class="jcol %s"><div class="jflag">%s</div><h3>%s</h3>%s</div>'
                % (cls, esc(flag), esc(head), r))
    # English and Spanish lead with the US entity, since that is where those
    # readers contract; German and Dutch lead with the EU one.
    order = ("us", "eu") if d["lang"] in ("en", "es") else ("eu", "us")
    juris = ('<div class="juris">'
             + "".join(jcol(d[c + "_f"], d[c + "_h"], d[c], c) for c in order) + '</div>')
    att = "".join('<li>%s</li>' % esc(x) for x in d["at"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p>%s'
             '<div class="attach"><h3>%s</h3><ul>%s</ul></div>'
             '<div class="closing">%s</div></div>'
             % (esc(d["cmh"]), esc(d["cma"]), juris, esc(d["ath"]), att, esc(d["cmn"])))

    # where we are not the right fit
    nf = "".join('<div class="row"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["nf"])
    P.append('<div class="page"><h2>%s</h2><p class="lede">%s</p><div class="rows">%s</div>'
             '<div class="closing">%s</div></div>'
             % (esc(d["nfh"]), esc(d["nfa"]), nf, esc(d["nfn"])))

    # p7 questions + CTA + sources
    qs = "".join('<div class="q">%s</div>' % esc(q) for q in d["quest"])
    P.append('<div class="page"><h2>%s</h2><div style="margin-top:20px">%s</div>'
             '<div class="callout"><h3>%s</h3><p>%s</p>'
             '<a class="mail" href="mailto:%s">%s</a></div>'
             '<div class="src"><h3>%s</h3><p>%s</p></div></div>'
             % (esc(d["p7h"]), qs, esc(d["ctah"]), esc(d["ctap"]),
                d["contact"], d["contact"], esc(d["srch"]), esc(d["src"])))

    # running foot: the CSS and the per-language strings existed but were never emitted,
    # so a 14-page document had no page numbers to refer to in a meeting
    total = len(P)
    P = [p[: p.rfind("</div>")] + '<div class="foot"><span>%s</span><span>%s %d / %d</span></div>'
         % (esc(d["foot"]), esc(d["pg"]), i + 1, total) + p[p.rfind("</div>"):]
         for i, p in enumerate(P)]
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

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for lg, d in C.items():
        p = os.path.join(OUT, d["file"] + ".html")
        io.open(p, "w", encoding="utf-8").write(build(d))
        print("wrote", p)
