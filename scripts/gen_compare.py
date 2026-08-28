#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the comparison pages - localized, and localized in substance.

Each market gets the three competitors its shortlists actually contain, not a
translation of the American ones: Shopware, Sana and Pepperi for Germany;
DJUST, Pepperi and Shopify for France; Mercado Libre Negocios, Yalo and Riqra
for Latin America; Sana, Orderchamp and Pepperi for the Netherlands. Every
competitor claim carries a public source - vendors' own pages, their own
communities, their own reviewers - and every page says plainly who the
competitor is right for. RocketX claims are limited to what the site already
claims elsewhere; the closing pilot sentence reuses the approved guarantee
clause of its language.
"""
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_footer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rocketx.app"

PREFIX = {"en": "compare", "de": "de/vergleich", "es": "es/comparativa",
          "nl": "nl/vergelijking", "fr": "fr/comparatif"}
SETS = {
 "en": ["shopify-b2b", "pepperi", "sana-commerce"],
 "de": ["shopware", "sana-commerce", "pepperi"],
 "es": ["mercado-libre", "yalo", "riqra"],
 "nl": ["sana-commerce", "orderchamp", "pepperi"],
 "fr": ["djust", "pepperi", "shopify-b2b"],
}

UI = {
 "en": dict(kick=u"/ COMPARED, WITH SOURCES", good=u"What %s genuinely does well",
            facts=u"The documented edges", shapes=u"The two shapes, side by side",
            fair=u"Where they are the right choice", back=u"&larr; The honest comparison",
            cta=u"The way to settle it is not a comparison page — ours included. It is a 30–45 day pilot against your own catalogue, with measures agreed up front. If the pilot misses them, you walk away owing nothing.",
            ctabtn=u"See the flat pricing", ctapdf=u"Business case (PDF)",
            note=u"Competitor information verified against the linked sources in August 2026; platforms change, and if anything here has gone stale, tell us and we will correct it. Also compared:",
            src=u"Source"),
 "de": dict(kick=u"/ VERGLICHEN, MIT QUELLEN", good=u"Was %s wirklich gut kann",
            facts=u"Die belegten Kanten", shapes=u"Die zwei Formen, nebeneinander",
            fair=u"Wo sie die richtige Wahl sind", back=u"&larr; Der ehrliche Vergleich",
            cta=u"Entschieden wird das nicht auf einer Vergleichsseite — unserer eingeschlossen. Sondern in einem Piloten von 30–45 Tagen an Ihrem eigenen Katalog, mit vorab vereinbarten Messgrößen. Verfehlt der Pilot sie, gehen Sie und zahlen nichts.",
            ctabtn=u"Zum Pauschalpreis", ctapdf=u"Business Case (PDF)",
            note=u"Wettbewerber-Angaben im August 2026 gegen die verlinkten Quellen geprüft; Plattformen ändern sich — ist hier etwas veraltet, sagen Sie es uns und wir korrigieren es. Ebenfalls verglichen:",
            src=u"Quelle"),
 "es": dict(kick=u"/ COMPARADOS, CON FUENTES", good=u"Lo que %s hace realmente bien",
            facts=u"Los datos documentados", shapes=u"Las dos formas, lado a lado",
            fair=u"Cuándo son la opción correcta", back=u"&larr; La comparación honesta",
            cta=u"Esto no se decide en una página de comparación — la nuestra incluida. Se decide en un piloto de 30–45 días sobre tu propio catálogo, con métricas acordadas de antemano. Si el piloto no las alcanza, te vas sin deber nada.",
            ctabtn=u"Ver la tarifa fija", ctapdf=u"Caso de negocio (PDF)",
            note=u"Información de competidores verificada contra las fuentes enlazadas en agosto de 2026; las plataformas cambian — si algo quedó desactualizado, dínoslo y lo corregimos. También comparados:",
            src=u"Fuente"),
 "nl": dict(kick=u"/ VERGELEKEN, MET BRONNEN", good=u"Wat %s echt goed doet",
            facts=u"De gedocumenteerde randen", shapes=u"De twee vormen, naast elkaar",
            fair=u"Wanneer zij de juiste keuze zijn", back=u"&larr; De eerlijke vergelijking",
            cta=u"Dit beslis je niet op een vergelijkingspagina — de onze meegerekend. Wel in een pilot van 30–45 dagen op je eigen catalogus, met vooraf afgesproken meetpunten. Haalt de pilot ze niet, dan stap je eruit en betaal je niets.",
            ctabtn=u"Bekijk de vaste prijs", ctapdf=u"Business case (pdf)",
            note=u"Concurrentie-informatie in augustus 2026 getoetst aan de gelinkte bronnen; platformen veranderen — is hier iets verouderd, zeg het en we corrigeren het. Ook vergeleken:",
            src=u"Bron"),
 "fr": dict(kick=u"/ COMPARÉS, AVEC SOURCES", good=u"Ce que %s fait vraiment bien",
            facts=u"Les faits documentés", shapes=u"Les deux formes, côte à côte",
            fair=u"Quand ils sont le bon choix", back=u"&larr; Le comparatif honnête",
            cta=u"Cela ne se tranche pas sur une page de comparaison — la nôtre comprise. Cela se tranche dans un pilote de 30 à 45 jours sur votre propre catalogue, avec des mesures convenues à l’avance. Si le pilote les manque, vous partez sans rien devoir.",
            ctabtn=u"Voir le forfait", ctapdf=u"Argumentaire (PDF)",
            note=u"Informations concurrents vérifiées contre les sources liées en août 2026 ; les plateformes évoluent — si un point est daté, dites-le-nous et nous corrigeons. Également comparés :",
            src=u"Source"),
}

# RocketX-side table cells per language, reused across pages
RX = {
 "en": dict(cart=u"Server-side, shared live across the team, visible to your reps",
            app=u"Native iOS &amp; Android, catalogue cached offline",
            fee=u"Flat monthly fee, published, never a percentage of revenue",
            beside=u"Your web shop keeps running — RocketX goes live beside it",
            pilot=u"30–45 day pilot with agreed measures — miss them, walk away owing nothing"),
 "de": dict(cart=u"Serverseitig, live im Team geteilt, für Ihren Außendienst sichtbar",
            app=u"Nativ für iOS &amp; Android, Katalog offline im Gerät",
            fee=u"Fester Monatspreis, veröffentlicht, nie ein Umsatzprozentsatz",
            beside=u"Ihr Webshop läuft weiter — RocketX geht daneben live",
            pilot=u"Pilot von 30–45 Tagen mit vereinbarten Messgrößen — verfehlt er sie, zahlen Sie nichts"),
 "es": dict(cart=u"En el servidor, compartido en vivo por el equipo, visible para tus vendedores",
            app=u"Nativo iOS y Android, catálogo en el dispositivo sin señal",
            fee=u"Tarifa mensual fija, publicada, nunca un porcentaje de tus ventas",
            beside=u"Tu canal actual sigue funcionando — RocketX arranca al lado",
            pilot=u"Piloto de 30–45 días con métricas acordadas — si no las alcanza, te vas sin deber nada"),
 "nl": dict(cart=u"Op de server, live gedeeld door het team, zichtbaar voor je buitendienst",
            app=u"Native iOS &amp; Android, catalogus offline op het toestel",
            fee=u"Vaste maandprijs, gepubliceerd, nooit een percentage van je omzet",
            beside=u"Je webshop blijft draaien — RocketX gaat ernaast live",
            pilot=u"Pilot van 30–45 dagen met afgesproken meetpunten — haalt hij ze niet, dan betaal je niets"),
 "fr": dict(cart=u"Côté serveur, partagé en direct par l’équipe, visible pour vos commerciaux",
            app=u"Natif iOS &amp; Android, catalogue en local hors connexion",
            fee=u"Forfait mensuel fixe, publié, jamais un pourcentage du chiffre d’affaires",
            beside=u"Votre boutique en ligne continue — RocketX démarre à côté",
            pilot=u"Pilote de 30 à 45 jours avec mesures convenues — s’il les manque, vous partez sans rien devoir"),
}


# where RocketX pulls ahead - the same claims the homepage and FAQ make,
# condensed: native apps, one experience online and offline, rich media,
# scanning, quality control in the cart, and speed the pilot then measures
EDGE_H = {
 "en": u"Where RocketX pulls ahead",
 "de": u"Wo RocketX vorn liegt",
 "es": u"Dónde RocketX va por delante",
 "nl": u"Waar RocketX voorop loopt",
 "fr": u"Là où RocketX prend l’avantage",
}
EDGE = {
 "en": [u"<b>A true native app experience:</b> iOS and Android apps built for B2B ordering — not a website wrapped in a shell.",
        u"<b>One experience online and offline:</b> catalogue, customer prices and cart are cached on the device and sync back the moment the connection returns.",
        u"<b>Rich media where the order happens:</b> print brochures as PDFs and product video live beside the catalogue — and still open with no signal.",
        u"<b>Barcode scanning into the cart:</b> point at the shelf or the box and the line is in the order.",
        u"<b>Quality checks before the order leaves:</b> the cart flags recent duplicates and attributes every change to a name and a timestamp.",
        u"<b>Orders come together faster:</b> search answers under a second at your real catalogue size, and the whole team builds one cart at once — the pilot measures the difference on your own numbers."],
 "de": [u"<b>Echtes natives App-Erlebnis:</b> iOS- und Android-Apps, gebaut für B2B-Bestellungen — keine Website in einer App-Hülle.",
        u"<b>Ein Erlebnis, online wie offline:</b> Katalog, Kundenpreise und Warenkorb liegen im Gerät und synchronisieren, sobald die Verbindung zurück ist.",
        u"<b>Rich Media direkt am Bestellvorgang:</b> Printbroschüren als PDF und Produktvideos liegen neben dem Katalog — und öffnen auch ohne Empfang.",
        u"<b>Barcode-Scan in den Warenkorb:</b> auf Regal oder Karton zielen, und die Position liegt in der Bestellung.",
        u"<b>Qualitätsprüfung vor dem Absenden:</b> Der Warenkorb meldet kürzliche Dopplungen und trägt zu jeder Änderung Name und Zeitstempel.",
        u"<b>Bestellungen entstehen schneller:</b> Die Suche antwortet unter einer Sekunde bei echter Kataloggröße, und das ganze Team baut gemeinsam an einem Warenkorb — der Pilot misst den Unterschied an Ihren eigenen Zahlen."],
 "es": [u"<b>Una experiencia nativa de verdad:</b> apps iOS y Android construidas para el pedido B2B — no una web envuelta en una app.",
        u"<b>Una sola experiencia, con y sin señal:</b> catálogo, precios por cliente y carrito viven en el dispositivo y sincronizan en cuanto vuelve la conexión.",
        u"<b>Rich media donde nace el pedido:</b> folletos en PDF y video de producto junto al catálogo — y se abren aun sin señal.",
        u"<b>Escaneo de código de barras al carrito:</b> apuntas al estante o a la caja y la línea queda en el pedido.",
        u"<b>Control de calidad antes de enviar:</b> el carrito avisa de duplicados recientes y atribuye cada cambio a un nombre y una hora.",
        u"<b>Los pedidos se arman más rápido:</b> la búsqueda responde en menos de un segundo con tu catálogo real y todo el equipo construye un mismo carrito — el piloto mide la diferencia con tus propios números."],
 "nl": [u"<b>Een echte native app-ervaring:</b> iOS- en Android-apps gebouwd voor B2B-bestellen — geen website in een app-schil.",
        u"<b>Eén ervaring, online én offline:</b> catalogus, klantprijzen en winkelwagen staan op het toestel en syncen zodra de verbinding terug is.",
        u"<b>Rich media waar de order ontstaat:</b> brochures als pdf en productvideo naast de catalogus — en ze openen ook zonder bereik.",
        u"<b>Barcode scannen zo de wagen in:</b> richt op schap of doos en de regel staat in de order.",
        u"<b>Kwaliteitscontrole vóór verzenden:</b> de winkelwagen meldt recente duplicaten en hangt aan elke wijziging een naam en tijdstempel.",
        u"<b>Orders komen sneller rond:</b> zoeken antwoordt binnen een seconde op je echte catalogusomvang en het hele team bouwt samen aan één wagen — de pilot meet het verschil op je eigen cijfers."],
 "fr": [u"<b>Une vraie expérience native :</b> des apps iOS et Android construites pour la commande B2B — pas un site web dans une coque.",
        u"<b>Une seule expérience, avec ou sans réseau :</b> catalogue, prix client et panier vivent sur l’appareil et se synchronisent dès que la connexion revient.",
        u"<b>Du rich media là où naît la commande :</b> brochures en PDF et vidéo produit à côté du catalogue — et elles s’ouvrent même sans signal.",
        u"<b>Le scan code-barres vers le panier :</b> visez l’étagère ou le carton, la ligne est dans la commande.",
        u"<b>Le contrôle qualité avant l’envoi :</b> le panier signale les doublons récents et attribue chaque modification à un nom et un horodatage.",
        u"<b>Les commandes se montent plus vite :</b> la recherche répond en moins d’une seconde sur votre vrai catalogue et toute l’équipe construit un même panier — le pilote mesure l’écart sur vos propres chiffres."],
}

CSS = u"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--panel:#0E1B33;--navy:#0B1526;--ice:#EDF2FB;--mist:#8FA1C4;
      --sky:#60A5FA;--blue:#2563EB;--line:#1E2E4C}
html{-webkit-text-size-adjust:100%}
body{background:var(--void);color:var(--ice);line-height:1.65;
     font-family:Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif}
a{color:var(--sky)}
.wrap{max-width:860px;margin:0 auto;padding:0 24px}
header{padding:24px 0;border-bottom:1px solid var(--line)}
header .wrap{display:flex;justify-content:space-between;align-items:center}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--ice);text-decoration:none}
.brand img{width:28px;height:28px;border-radius:7px}
.brand b{font-family:"Space Grotesk",Inter,sans-serif;font-size:16px}
header a.back{color:var(--mist);font-size:14px;text-decoration:none}
header a.back:hover{color:var(--sky)}
main{padding:48px 0 72px}
.kick{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:2.2px;
      color:var(--sky);margin-bottom:14px}
h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:clamp(27px,4.6vw,40px);
   line-height:1.12;letter-spacing:-1px;font-weight:600;max-width:24ch}
.lede{color:var(--mist);margin:18px 0 0;max-width:64ch;font-size:16.5px}
h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:21px;letter-spacing:-.4px;
   margin:44px 0 14px}
p{color:var(--mist);font-size:15.5px;margin-bottom:14px;max-width:70ch}
p strong{color:var(--ice)}
ul.facts{list-style:none;margin:14px 0}
ul.facts li{color:var(--mist);font-size:15px;padding:12px 0 12px 18px;
  border-left:3px solid var(--line);margin-bottom:10px;max-width:72ch}
ul.facts li b{color:var(--ice)}
ul.facts li .src{display:block;margin-top:5px;font-size:12.5px}
ul.edge{list-style:none;margin:14px 0}
ul.edge li{color:var(--mist);font-size:15px;padding:12px 0 12px 18px;
  border-left:3px solid var(--sky);margin-bottom:10px;max-width:72ch}
ul.edge li b{color:var(--ice)}
.tblwrap{overflow-x:auto}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14.5px}
th{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1.4px;
   text-transform:uppercase;color:var(--mist);text-align:left;padding:10px 12px}
td{padding:12px;border-top:1px solid var(--line);color:var(--mist);vertical-align:top}
td:first-child{color:var(--ice)}
.fair{border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin:30px 0;
      background:var(--panel)}
.fair h2{margin-top:0;font-size:17px}
.fair p{margin-bottom:0}
.ctabox{margin-top:44px;border:1px solid var(--line);border-radius:16px;
        padding:28px;background:var(--panel);text-align:center}
.ctabox p{margin:0 auto 18px;max-width:56ch}
.ctabox .cta{display:inline-block;background:var(--blue);color:#fff;padding:13px 26px;
        border-radius:9px;font-weight:600;text-decoration:none}
.ctabox .dl{display:inline-block;margin-left:18px;color:var(--mist);font-size:14px}
.note{font-size:12.5px;color:var(--mist);opacity:.85;margin-top:34px;max-width:74ch}
"""

# ---------------------------------------------------------------------------
# competitor pages: P_[(lang, slug)]
# ---------------------------------------------------------------------------
P_ = {}

def page(lang, slug, name, title, desc, lede, good, facts, table, fair):
    P_[(lang, slug)] = dict(name=name, title=title, desc=desc, lede=lede,
                            good=good, facts=facts, table=table, fair=fair)

# ---------------- EN (unchanged in substance) ----------------
page("en", "shopify-b2b", u"Shopify B2B",
 u"RocketX vs Shopify B2B — an honest comparison for wholesalers",
 u"Where Shopify's B2B features end and where a dedicated wholesale ordering platform begins: order-size ceilings, shared carts, native apps, offline — with sources.",
 u"Shopify is superb at what it was built for. The question for a wholesaler is narrower: is the B2B on top of it shaped like your order flow? Here is the comparison we would want to read, with every claim sourced.",
 u"World-class checkout and hosting, an enormous app ecosystem, and since April 2026 the core B2B primitives — company accounts, per-customer catalogs, quantity rules, net terms — are included on every plan. For a brand selling mostly direct-to-consumer with a wholesale side channel, Shopify B2B is often enough, and we say so to prospects for whom that is true.",
 [(u"<b>Orders cap at 500 line items</b> (200 on draft orders) — above that the order fails. A stocking wholesale order in parts, fashion or cosmetics can cross that line routinely.",
   u"Shopify Help Center — B2B considerations", u"https://help.shopify.com/en/manual/b2b/getting-started/considerations"),
  (u"<b>Carts are per-device and per-browser.</b> One buyer building an order for a manager to approve — the everyday shape of wholesale buying — has, in Shopify's own community words, “no out-of-the-box solution”. The thread has been open since July 2025.",
   u"Shopify Community — shared carts across devices", u"https://community.shopify.com/t/how-do-your-b2b-customers-share-carts-or-use-carts-across-multiple-devices/551949"),
  (u"<b>No native buyer app, no offline catalogue.</b> Shopify's B2B solutions page describes a responsive web storefront; a buyer in a warehouse aisle with no signal is not part of the model.",
   u"Shopify Plus — B2B solutions page", u"https://www.shopify.com/plus/solutions/b2b-ecommerce"),
  (u"<b>Above a negotiable GMV threshold, Plus switches to a variable platform fee</b> — analyses cite ~0.25% of monthly GMV on 3-year terms, capped around $40k/month. The flat fee quietly becomes a share of your growth.",
   u"Shopify Plus pricing + independent analysis", u"https://www.brokenrubik.com/blog/shopify-plus-pricing-guide")],
 [(u"Cart", u"Per device, per browser", "cart"),
  (u"Buyer mobile", u"Responsive web", "app"),
  (u"Pricing shape", u"$2,300–2,500/mo, then a variable fee above a GMV threshold", "fee"),
  (u"Your web shop", u"Is the platform", "beside"),
  (u"Trying it", u"Self-serve trial (retail-shaped)", "pilot")],
 u"Choose Shopify if you are primarily a DTC brand with a modest wholesale side, order sizes stay comfortably under the caps, and your buyers order at desks. Those businesses are well served — and are not who RocketX is built for.")

page("en", "pepperi", u"Pepperi",
 u"RocketX vs Pepperi — an honest comparison for wholesalers",
 u"Pepperi is the closest product shape to RocketX: native apps, offline, field sales. The differences are reliability, pricing transparency and what the cart is — with sources.",
 u"Pepperi deserves respect: 1,000+ customers, true native iOS and Android apps, offline order-taking for field reps. It is the closest shape to RocketX on the market — which is exactly why the differences are worth stating precisely.",
 u"A mature field-sales suite: rep order-taking on tablets, trade promotions, SAP Business One integration, two decades of wholesale domain knowledge across food, beauty and consumer goods. If your model is rep-led van sales with deep trade-promotion mechanics, Pepperi has features RocketX does not try to match.",
 [(u"<b>Offline is Pepperi's most-praised feature — and sync reliability is its most-repeated complaint.</b> Recent reviews describe crashes, freezes and resync failures during store visits, and update-related downtime.",
   u"Capterra — Pepperi reviews", u"https://www.capterra.com/p/146870/Pepperi/reviews/"),
  (u"<b>The public pricing page is gone</b> — both URL variants return 404 since the 2024 private-equity acquisition. Third-party sources describe per-user licences plus modules plus implementation, with real mid-market costs reported at $20,000–50,000+/year.",
   u"WizCommerce — Pepperi pricing analysis", u"https://wizcommerce.com/blog/pepperi-pricing/"),
  (u"<b>Support is time-zone bound,</b> reviewers report, with slower Android parity and a back office one French reviewer calls “vieillissant et catastrophiquement lent”.",
   u"Capterra / G2 — Pepperi reviews", u"https://www.g2.com/products/pepperi/reviews")],
 [(u"Native apps, offline", u"Yes — its real strength", "app"),
  (u"Sync model", u"Device-led; reviewers report resync failures mid-visit", "cart"),
  (u"Pricing", u"Unpublished; per-user licences + modules", "fee"),
  (u"Trying it", u"Demo, then sales cycle", "pilot")],
 u"Choose Pepperi if your business is rep-driven van sales with heavy trade-promotion needs and you have the implementation partner its setup expects. If the centre of your problem is buyers and reps building orders together — reliably, offline, at a predictable price — that is the problem RocketX was built around.")

page("en", "sana-commerce", u"Sana Commerce",
 u"RocketX vs Sana Commerce — an honest comparison for wholesalers",
 u"Sana's real-time ERP coupling is its strength and its constraint. Where that architecture helps, where it binds, and how a beside-your-shop platform differs — with sources.",
 u"Sana Commerce made a clear architectural bet: the webstore reads and writes your ERP directly, in real time. Where that bet pays off it pays well. The honest comparison is about what the same bet costs.",
 u"If you run SAP or Microsoft Dynamics and want the storefront to be a pure window onto the ERP — prices, stock, customer terms, live — Sana's integration depth is its deserved reputation, and its case-study library shows real results at real manufacturers.",
 [(u"<b>SAP and Microsoft Dynamics only.</b> Sana's architecture requires one of two ERP families; every wholesaler on anything else is out of scope by design.",
   u"Sana Commerce — homepage", u"https://www.sana-commerce.com/"),
  (u"<b>The coupling cuts both ways:</b> reviewers report that customisation must route through the ERP, storefront performance depends on ERP web services, custom features take months, and upgrades break customer-specific work.",
   u"PeerSpot — Sana Commerce pros and cons", u"https://www.peerspot.com/products/sana-commerce-pros-and-cons"),
  (u"<b>“They only check cases twice a week”</b> — the same support-cadence complaint appears verbatim on two independent review platforms, alongside reports that support is effectively English-only for non-English markets.",
   u"G2 / TrustRadius — Sana Commerce reviews", u"https://www.trustradius.com/products/sana-commerce/reviews?qs=pros-and-cons"),
  (u"<b>Pricing is quote-only</b> across all three tiers — no number appears anywhere on the pricing page.",
   u"Sana Commerce — pricing page", u"https://www.sana-commerce.com/pricing/")],
 [(u"ERP scope", u"SAP and Microsoft Dynamics, exclusively", "beside"),
  (u"Buyer mobile", u"Responsive web", "app"),
  (u"Cart", u"Individual web sessions", "cart"),
  (u"Pricing", u"Quote-only", "fee"),
  (u"Trying it", u"Demo, then sales cycle", "pilot")],
 u"Choose Sana if you are committed to SAP or Dynamics, want the storefront to be the ERP's mirror, and your buyers order at desks on the web. If your buyers order from aisles and cars, your team builds orders together, or your ERP is not on Sana's list — that is the gap RocketX fills, without asking you to replace anything.")

# ---------------- DE ----------------
page("de", "shopware", u"Shopware",
 u"RocketX vs Shopware B2B — ein ehrlicher Vergleich für den Großhandel",
 u"Shopware ist der deutsche Standard für den Shop. Die Frage für Großhändler ist eine andere: Wie bestellt Ihr Kunde — am Schreibtisch oder im Gang ohne Empfang? Mit Quellen.",
 u"Shopware ist zu Recht der deutsche Platzhirsch: offene Plattform, riesiges Agentur-Ökosystem, veröffentlichte Preise. Der ehrliche Vergleich handelt nicht vom Shop — sondern davon, wie Großhandelsbestellungen wirklich entstehen.",
 u"Ein exzellenter, offener Shop aus Deutschland: veröffentlichte Preise ab 600 €/Monat, DSGVO-Selbstverständnis, über tausend zertifizierte Agenturen. Wer einen neuen Webshop baut, hat mit Shopware eine erstklassige Grundlage — das bestreiten wir nicht, wir setzen daneben an.",
 [(u"<b>B2B ist ein Baustein der oberen Pläne:</b> Die B2B Components (Firmenkonten, Angebote, Freigaben, Bestelllisten) gibt es erst ab Evolve — veröffentlicht „ab 2.400 €/Monat“. Die ältere B2B Suite wird als Teil der Components abgelöst.",
   u"Shopware — Preise", u"https://www.shopware.com/de/preise/"),
  (u"<b>Kein natives Einkäufer-Erlebnis:</b> Shopware liefert einen Web-Storefront. Eine native iOS/Android-App mit Offline-Katalog für Ihre Kunden und Ihren Außendienst ist nicht Teil des Produkts — der Gang ohne Empfang bleibt ein verlorener Bestellmoment.",
   u"Shopware — Produktseiten (Stand August 2026)", u"https://www.shopware.com/de/produkte/"),
  (u"<b>Serverseitig geteilte Warenkörbe, die Ihr Außendienst live sieht,</b> sind kein beworbenes Konzept — der Warenkorb gehört der Browser-Sitzung des einzelnen Nutzers.",
   u"Shopware — Produkt- und Entwicklerdokumentation", u"https://docs.shopware.com/"),
  (u"<b>Die Fair-Use-Grenze:</b> Ab 1 Mio. € externem Jahresumsatz verlangt die Fair Use Policy den Wechsel aus dem kostenlosen Community-Plan in einen Bezahlplan — die Kostenkurve hängt damit doch am Umsatz.",
   u"Shopware — Fair Use Policy (März 2025)", u"https://www.shopware.com/de/fair-use-policy/")],
 [(u"Warenkorb", u"Browser-Sitzung des einzelnen Nutzers", "cart"),
  (u"Einkäufer mobil", u"Responsiver Web-Storefront", "app"),
  (u"B2B-Funktionen", u"Ab Evolve, „ab 2.400 €/Monat“", "fee"),
  (u"Ihr Webshop", u"Ist die Plattform — Aufbau oder Migration", "beside"),
  (u"Ausprobieren", u"Projekt mit Agentur", "pilot")],
 u"Wählen Sie Shopware, wenn Sie einen neuen, hochgradig anpassbaren Webshop bauen wollen und Ihre Einkäufer am Schreibtisch bestellen. Wenn Ihre Bestellungen dagegen in Gängen, Lagern und beim Kunden vor Ort entstehen — und Ihr bestehender Shop bleiben soll, wie er ist — dann ist das die Lücke, für die RocketX gebaut wurde.")

page("de", "sana-commerce", u"Sana Commerce",
 u"RocketX vs Sana Commerce — ein ehrlicher Vergleich für den Großhandel",
 u"Sanas Echtzeit-ERP-Kopplung ist Stärke und Fessel zugleich. Wo die Architektur trägt, wo sie bindet — mit Quellen.",
 u"Sana Commerce hat eine klare Architektur-Wette gemacht: Der Webstore liest und schreibt Ihr ERP direkt, in Echtzeit. Wo diese Wette aufgeht, geht sie gut auf. Der ehrliche Vergleich handelt davon, was dieselbe Wette kostet.",
 u"Wer SAP oder Microsoft Dynamics fährt und den Storefront als reines Fenster ins ERP will — Preise, Bestände, Kundenkonditionen, live —, bekommt bei Sana zu Recht gerühmte Integrationstiefe, belegt mit einer Fallstudien-Bibliothek echter Industrie- und Handelsunternehmen.",
 [(u"<b>Nur SAP und Microsoft Dynamics.</b> Sanas Architektur setzt eine der beiden ERP-Familien voraus; jeder Großhändler auf einem anderen System ist per Design außen vor.",
   u"Sana Commerce — Startseite", u"https://www.sana-commerce.com/"),
  (u"<b>Die Kopplung schneidet in beide Richtungen:</b> Anpassungen laufen durchs ERP, die Storefront-Performance hängt an ERP-Webservices, individuelle Features dauern Monate, Updates brechen Kundenspezifisches — so die eigenen Rezensenten.",
   u"PeerSpot — Sana Commerce Pros und Cons", u"https://www.peerspot.com/products/sana-commerce-pros-and-cons"),
  (u"<b>„Sie prüfen Tickets nur zweimal pro Woche“</b> — dieselbe Support-Klage steht wortgleich auf zwei unabhängigen Bewertungsplattformen; dazu Berichte, der Support sei faktisch nur auf Englisch zu haben.",
   u"G2 / TrustRadius — Sana-Commerce-Bewertungen", u"https://www.trustradius.com/products/sana-commerce/reviews?qs=pros-and-cons"),
  (u"<b>Preise nur auf Anfrage,</b> über alle drei Stufen — keine Zahl auf der Preisseite.",
   u"Sana Commerce — Preisseite", u"https://www.sana-commerce.com/pricing/")],
 [(u"ERP-Spektrum", u"Ausschließlich SAP und Microsoft Dynamics", "beside"),
  (u"Einkäufer mobil", u"Responsiver Web-Storefront", "app"),
  (u"Warenkorb", u"Einzelne Web-Sitzungen", "cart"),
  (u"Preis", u"Nur auf Anfrage", "fee"),
  (u"Ausprobieren", u"Demo, dann Vertriebszyklus", "pilot")],
 u"Wählen Sie Sana, wenn Sie fest auf SAP oder Dynamics stehen, den Storefront als Spiegel des ERP wollen und Ihre Einkäufer am Schreibtisch im Web bestellen. Bestellen Ihre Kunden aus Gängen und Autos, arbeitet Ihr Team gemeinsam an Bestellungen, oder steht Ihr ERP nicht auf Sanas Liste — dann füllt RocketX genau diese Lücke, ohne dass Sie irgendetwas ersetzen müssen.")

page("de", "pepperi", u"Pepperi",
 u"RocketX vs Pepperi — ein ehrlicher Vergleich für den Großhandel",
 u"Pepperi ist die ähnlichste Produktform am Markt: native Apps, offline, Außendienst. Die Unterschiede: Zuverlässigkeit, Preistransparenz und was der Warenkorb ist — mit Quellen.",
 u"Pepperi verdient Respekt: 1.000+ Kunden, echte native iOS- und Android-Apps, Offline-Auftragserfassung für den Außendienst. Es ist die ähnlichste Form zu RocketX am Markt — genau deshalb lohnt es sich, die Unterschiede präzise zu benennen.",
 u"Eine reife Außendienst-Suite: Auftragserfassung auf dem Tablet, Trade Promotions, SAP-Business-One-Integration, zwei Jahrzehnte Branchenwissen von Lebensmitteln bis Kosmetik. Wer im Kern Van-Sales mit tiefer Promotion-Mechanik fährt, findet bei Pepperi Funktionen, die RocketX gar nicht nachbauen will.",
 [(u"<b>Offline ist Pepperis meistgelobtes Merkmal — und die Sync-Zuverlässigkeit die häufigste Klage.</b> Aktuelle Bewertungen beschreiben Abstürze, Einfrieren und gescheiterte Resyncs mitten im Kundenbesuch, dazu Ausfallzeiten nach Updates.",
   u"Capterra — Pepperi-Bewertungen", u"https://www.capterra.com/p/146870/Pepperi/reviews/"),
  (u"<b>Die öffentliche Preisseite ist verschwunden</b> — beide URL-Varianten liefern seit der Private-Equity-Übernahme 2024 einen 404. Drittquellen beschreiben Nutzerlizenzen plus Module plus Implementierung; real berichtete Mittelstandskosten: 20.000–50.000+ $ pro Jahr.",
   u"WizCommerce — Analyse der Pepperi-Preise", u"https://wizcommerce.com/blog/pepperi-pricing/"),
  (u"<b>Support an Zeitzonen gebunden,</b> berichten Rezensenten, dazu langsamere Android-Parität und ein Backoffice, das ein französischer Rezensent „vieillissant et catastrophiquement lent“ nennt.",
   u"Capterra / G2 — Pepperi-Bewertungen", u"https://www.g2.com/products/pepperi/reviews")],
 [(u"Native Apps, offline", u"Ja — die echte Stärke", "app"),
  (u"Sync-Modell", u"Gerätegeführt; Rezensenten berichten Resync-Ausfälle im Termin", "cart"),
  (u"Preis", u"Unveröffentlicht; Nutzerlizenzen + Module", "fee"),
  (u"Ausprobieren", u"Demo, dann Vertriebszyklus", "pilot")],
 u"Wählen Sie Pepperi, wenn Ihr Geschäft Rep-getriebener Van-Sales mit schwerer Promotion-Mechanik ist und Sie den Implementierungspartner haben, den das Setup erwartet. Liegt der Kern Ihres Problems darin, dass Einkäufer und Außendienst gemeinsam Bestellungen bauen — zuverlässig, offline, zu einem planbaren Preis —, dann ist das genau das Problem, um das RocketX gebaut wurde.")

# ---------------- ES (Latin America) ----------------
page("es", "mercado-libre", u"Mercado Libre Negocios",
 u"RocketX vs Mercado Libre Negocios — una comparación honesta para mayoristas",
 u"El marketplace más grande de la región entró al B2B. La pregunta para un mayorista: ¿vender en el canal de otro, con sus comisiones, o tener el propio? Con fuentes.",
 u"Mercado Libre Negocios es real y crece rápido: millones de compradores habilitados, facturación integrada, financiamiento de Mercado Pago. La comparación honesta no es «cuál es mejor» — son dos cosas distintas: su marketplace, o tu propio canal.",
 u"Alcance instantáneo que nadie más tiene en la región: millones de compradores empresariales habilitados, facturación integrada, logística rápida y financiamiento con Mercado Pago. Para liquidar inventario o captar clientes nuevos que no te conocen, el marketplace funciona — y puede convivir con tu canal propio.",
 [(u"<b>La comisión es el modelo:</b> la tasa de comisión efectiva del marketplace llegó a 21,3 % de cada venta en el segundo trimestre de 2025, con tablas por categoría y país y, en Argentina, recargos por provincia.",
   u"Análisis de resultados de Mercado Libre (Q2 2025)", u"https://www.thewolfofharcourtstreet.com/p/mercadolibre-q2-2025-earnings-analysis"),
  (u"<b>El enojo de los vendedores es público:</b> «se llevan el 20 % o más de cada operación», resumía iProfesional en 2025 tras las subas de tarifas; en Reclame Aqui (Brasil) hay hilos titulados «Taxas abusivas».",
   u"iProfesional / Reclame Aqui", u"https://www.reclameaqui.com.br/mercado-livre/taxas-abusivas-nao-vale-mais-a-pena-vender-no-mercado-livre_C5-w-0VyE03sd5o7/"),
  (u"<b>Es el canal de ellos, no el tuyo:</b> tus clientes compran en Mercado Libre, con la marca, las reglas y los datos del marketplace — no en tu catálogo, con tus precios negociados por cliente y tu vendedor mirando el carrito.",
   u"Digital Commerce 360 — expansión de Mercado Libre Negocios", u"https://www.digitalcommerce360.com/2025/09/23/mercado-libre-negocios-expands-b2b/"),
  (u"<b>Las tarifas cambian unilateralmente:</b> subas de comisiones anunciadas con semanas de aviso y sin negociación — el costo de tu canal lo decide el marketplace, no tu contrato.",
   u"MyContador — análisis de comisiones de Mercado Libre", u"https://blog.mycontador.com.ar/mercado-libre-encarece-comisiones-como-afecta-a-las-pymes/")],
 [(u"Modelo", u"Marketplace: comisión por venta, hasta ~21 % efectivo", "fee"),
  (u"El cliente", u"Del marketplace, con sus reglas y sus datos", "beside"),
  (u"Carrito", u"El del marketplace, individual", "cart"),
  (u"App móvil", u"La de Mercado Libre, con tu competencia al lado", "app"),
  (u"Probar", u"Publicar y pagar comisión desde la primera venta", "pilot")],
 u"Usa Mercado Libre Negocios para lo que hace bien: alcanzar compradores que aún no te conocen. Para tus clientes de siempre — los que ya te compran cada semana — cada venta por el marketplace convierte margen tuyo en comisión de ellos. RocketX es para ese canal propio: tu catálogo, tus precios por cliente, tu vendedor viendo el carrito, por una tarifa fija que no crece con tus ventas.")

page("es", "yalo", u"Yalo",
 u"RocketX vs Yalo — una comparación honesta para mayoristas",
 u"Yalo industrializó el pedido por WhatsApp a escala de Coca-Cola FEMSA. La pregunta honesta: ¿tu problema es conversar con un millón de tienditas, o darle a tu cliente mayorista un catálogo, precios y un carrito compartido? Con fuentes.",
 u"En América Latina, WhatsApp es el canal comercial por defecto — y Yalo es quien mejor lo industrializó. La comparación honesta no es contra WhatsApp: es sobre qué forma tiene tu venta mayorista.",
 u"Escala probada en comercio conversacional: Coca-Cola FEMSA digitalizó más de un millón de tienditas con Yalo, con cientos de miles enviando pedidos mensuales por WhatsApp; su lista de clientes incluye a las grandes marcas de consumo de la región. Para marcas masivas que atienden millones de puntos de venta pequeños, es la referencia de la categoría.",
 [(u"<b>Está hecho para el tramo marca→tiendita:</b> agentes de IA que sugieren un pedido corto en un chat. El flujo mayorista completo — catálogo grande, precios negociados por cliente, carrito que arma un equipo — no es la forma del producto.",
   u"Yalo — sitio y casos de clientes", u"https://www.yalo.ai/"),
  (u"<b>Precio empresarial, sin cifras públicas:</b> venta enterprise por proyecto, sin página de precios — el modelo opuesto a una tarifa fija publicada.",
   u"Yalo — sitio (agosto 2026)", u"https://www.yalo.ai/pricing"),
  (u"<b>Un chat no es un catálogo:</b> en la conversación no hay búsqueda instantánea sobre miles de referencias, ni carrito visible para tu vendedor, ni catálogo offline en la bodega sin señal.",
   u"Yalo — descripción de producto", u"https://www.yalo.ai/product")],
 [(u"Canal", u"WhatsApp: conversación guiada por IA", "cart"),
  (u"Catálogo", u"Sugerencias dentro del chat", "app"),
  (u"Precio", u"Enterprise, no publicado", "fee"),
  (u"Tu canal actual", u"El pedido se muda al chat", "beside"),
  (u"Probar", u"Proyecto enterprise", "pilot")],
 u"Elige Yalo si eres una marca de consumo masivo y tu problema es conversar con cientos de miles de tienditas. Si eres un mayorista o distribuidor cuyos clientes arman pedidos grandes — en pasillos, bodegas y rutas, a veces sin señal — ese es el problema para el que está hecho RocketX. Y conviven: WhatsApp para avisar, RocketX para pedir.")

page("es", "riqra", u"Riqra",
 u"RocketX vs Riqra — una comparación honesta para mayoristas",
 u"Riqra es el análogo regional accesible: e-commerce B2B para distribuidores desde ~99 US$ al mes. La comparación honesta es de tamaño de problema. Con fuentes.",
 u"Nos gusta que exista Riqra: valida, con precios publicados y sin comisiones, que el pedido B2B de la región merece software propio. La comparación honesta es sobre el tamaño del problema que cada uno resuelve.",
 u"Un producto regional sensato: catálogos y precios por cliente para fabricantes, distribuidores y mayoristas en Perú, México y la región, con planes publicados desde ~99–199 US$ al mes y sin comisiones. Para una distribuidora que empieza a digitalizar su toma de pedidos, es un primer paso legítimo.",
 [(u"<b>Es la gama de entrada:</b> los listados de terceros lo sitúan «desde 500 US$ al año» — uno o dos órdenes de magnitud por debajo del segmento de 15–300 M US$ de facturación, con la profundidad que ese precio permite.",
   u"Capterra — Riqra", u"https://www.capterra.com/p/240457/Riqra/"),
  (u"<b>La web es el producto:</b> el corazón es una tienda B2B web; el catálogo nativo offline en el teléfono del comprador y el carrito compartido en vivo visible para tu vendedor no son el centro de la forma.",
   u"Riqra — sitio", u"https://en.riqra.com/"),
  (u"<b>Entrar es contratar:</b> el modelo de entrada es suscribirse a un plan — no un piloto de 30–45 días con métricas acordadas y salida sin costo si no se alcanzan.",
   u"Riqra — planes y precios", u"https://en.riqra.com/pricing")],
 [(u"Segmento", u"Pymes y distribuidoras en digitalización inicial", "beside"),
  (u"App del comprador", u"Tienda B2B web", "app"),
  (u"Carrito", u"Sesión individual del comprador", "cart"),
  (u"Precio", u"Publicado, desde ~99 US$/mes", "fee"),
  (u"Probar", u"Contratar un plan", "pilot")],
 u"Elige Riqra si estás dando el primer paso desde el cuaderno y WhatsApp hacia un catálogo en línea, con un presupuesto de entrada. Cuando el problema es de otra escala — miles de referencias con búsqueda instantánea, equipos que arman un pedido juntos, vendedores en ruta sin señal, y un piloto que se juzga con métricas antes de comprometerte — esa es la liga en la que juega RocketX.")

# ---------------- NL ----------------
page("nl", "sana-commerce", u"Sana Commerce",
 u"RocketX vs Sana Commerce — een eerlijke vergelijking voor de groothandel",
 u"De Rotterdamse standaard voor SAP- en Dynamics-shops: waar de realtime ERP-koppeling helpt, waar hij knelt — met bronnen.",
 u"Sana Commerce — uit Rotterdam — deed een heldere architectuurgok: de webstore leest en schrijft je ERP rechtstreeks, in realtime. Waar die gok loont, loont hij goed. De eerlijke vergelijking gaat over wat dezelfde gok kost.",
 u"Draai je SAP of Microsoft Dynamics en wil je de storefront als puur venster op het ERP — prijzen, voorraad, klantcondities, live — dan is Sana's integratiediepte terecht zijn reputatie, met een bibliotheek aan klantcases met echte cijfers.",
 [(u"<b>Alleen SAP en Microsoft Dynamics.</b> Sana's architectuur vereist één van twee ERP-families; elke groothandel op iets anders valt per ontwerp buiten de boot.",
   u"Sana Commerce — homepage", u"https://www.sana-commerce.com/"),
  (u"<b>De koppeling snijdt twee kanten op:</b> maatwerk loopt via het ERP, storefront-prestaties hangen aan ERP-webservices, eigen features duren maanden en upgrades breken klantspecifiek werk — aldus de eigen reviewers.",
   u"PeerSpot — Sana Commerce pros en cons", u"https://www.peerspot.com/products/sana-commerce-pros-and-cons"),
  (u"<b>„Ze checken tickets maar twee keer per week”</b> — dezelfde supportklacht staat woordelijk op twee onafhankelijke reviewplatforms; daarnaast melden reviewers dat support feitelijk Engelstalig is.",
   u"G2 / TrustRadius — Sana-reviews", u"https://www.trustradius.com/products/sana-commerce/reviews?qs=pros-and-cons"),
  (u"<b>Prijzen alleen op aanvraag,</b> over alle drie de tiers — nergens een bedrag op de prijspagina.",
   u"Sana Commerce — prijspagina", u"https://www.sana-commerce.com/pricing/")],
 [(u"ERP-bereik", u"Uitsluitend SAP en Microsoft Dynamics", "beside"),
  (u"Inkoper mobiel", u"Responsive web", "app"),
  (u"Winkelwagen", u"Losse websessies", "cart"),
  (u"Prijs", u"Alleen op aanvraag", "fee"),
  (u"Proberen", u"Demo, dan salestraject", "pilot")],
 u"Kies Sana als je vastzit aan SAP of Dynamics, de storefront een spiegel van het ERP moet zijn en je inkopers achter een bureau in de browser bestellen. Bestellen jouw klanten vanuit gangpaden en bussen, bouwt je team samen aan orders, of staat je ERP niet op Sana's lijst — dan is dat precies het gat dat RocketX vult, zonder dat je iets hoeft te vervangen.")

page("nl", "orderchamp", u"Orderchamp",
 u"RocketX vs Orderchamp — een eerlijke vergelijking voor de groothandel",
 u"Het Amsterdamse platform draaide in 2025 van marktplaats naar B2B-software. De commissiegeschiedenis en de kleine lettertjes — met bronnen.",
 u"Orderchamp kent de Nederlandse markt en maakte in april 2025 een verstandige draai: van pure marktplaats naar B2B-bestelsoftware. De eerlijke vergelijking gaat over wat er van het commissiemodel overbleef — en voor wie het gebouwd is.",
 u"Lokaal, snel en toegankelijk: een Amsterdams team, koppelingen met Exact Online en andere Nederlandse standaardsystemen, AI die e-mail- en Excel-orders omzet, en een salesapp voor reps. Voor merken en kleinere groothandels is het een logische eerste digitaliseringsstap — met marktplaatsbereik erbij.",
 [(u"<b>De commissiegeschiedenis:</b> als marktplaats rekende Orderchamp doorlopende commissie plus een ontdekkingsfee op eerste orders — tot zo'n 25 % totaal; op zelf uitgenodigde klanten gold 0 % alleen de eerste maanden, daarna alsnog commissie — ook op klanten die je aantoonbaar al jaren had.",
   u"Orderchamp helpcenter (gearchiveerd, oktober 2025)", u"https://web.archive.org/web/2025/https://support.orderchamp.com/hc/en-150/articles/360016984018"),
  (u"<b>Het nieuwe model is deels ondoorzichtig:</b> een vast maandabonnement plus commissies in volumetiers waarvan de percentages niet publiek staan — je moet ernaar vragen.",
   u"Orderchamp helpcenter — commissiemodel", u"https://support.orderchamp.com/hc/en-150/articles/360016984018"),
  (u"<b>Gebouwd voor een ander segment:</b> de eigen positionering mikt op merken en handelaren in het lagere middensegment — één tot twee ordes van grootte onder de groothandel van 15–250 mln. € waarvoor RocketX is gebouwd.",
   u"Emerce — Orderchamp wordt B2B-platform (april 2025)", u"https://www.emerce.nl/nieuws/orderchamp-breidt-uit-marktplaats-volwaardig-b2b-ecommerceplatform")],
 [(u"Model", u"Abonnement + commissietiers (percentages niet publiek)", "fee"),
  (u"Segment", u"Merken en kleinere handelaren", "beside"),
  (u"Inkoper mobiel", u"Web; salesapp voor reps", "app"),
  (u"Winkelwagen", u"Sessie van de individuele inkoper", "cart"),
  (u"Proberen", u"Abonnement afsluiten", "pilot")],
 u"Kies Orderchamp als je een merk of compacte groothandel bent die de eerste digitaliseringsstap zet en het marktplaatsbereik meepakt. Draai je 15 tot 250 miljoen omzet, met duizenden artikelen, teams die samen orders bouwen en een buitendienst zonder bereik — dan speelt je probleem in de klasse waarvoor RocketX is gebouwd: vaste, gepubliceerde prijs, nooit een percentage, ook niet in kleine lettertjes.")

page("nl", "pepperi", u"Pepperi",
 u"RocketX vs Pepperi — een eerlijke vergelijking voor de groothandel",
 u"Pepperi is de meest verwante productvorm: native apps, offline, buitendienst. De verschillen: betrouwbaarheid, prijstransparantie en wat de winkelwagen is — met bronnen.",
 u"Pepperi verdient respect: 1.000+ klanten, echte native iOS- en Android-apps, offline orderopname voor de buitendienst. Het is de meest verwante vorm op de markt — precies daarom loont het de verschillen scherp te benoemen.",
 u"Een volwassen buitendienst-suite: orderopname op tablets, trade promotions, SAP Business One-integratie, twintig jaar domeinkennis van food tot beauty. Draait jouw model op rep-gedreven van-sales met zware promotiemechaniek, dan heeft Pepperi functies die RocketX niet eens probeert na te bouwen.",
 [(u"<b>Offline is Pepperi's meest geprezen feature — en syncbetrouwbaarheid de meest herhaalde klacht.</b> Recente reviews beschrijven crashes, bevriezingen en mislukte resyncs midden in winkelbezoeken, plus downtime na updates.",
   u"Capterra — Pepperi-reviews", u"https://www.capterra.com/p/146870/Pepperi/reviews/"),
  (u"<b>De publieke prijspagina is weg</b> — beide URL-varianten geven sinds de private-equity-overname van 2024 een 404. Derde bronnen beschrijven gebruikerslicenties plus modules plus implementatie; gerapporteerde middenmarktkosten: 20.000–50.000+ $ per jaar.",
   u"WizCommerce — Pepperi-prijsanalyse", u"https://wizcommerce.com/blog/pepperi-pricing/"),
  (u"<b>Support is tijdzonegebonden,</b> melden reviewers, met tragere Android-pariteit en een backoffice dat een Franse reviewer „vieillissant et catastrophiquement lent” noemt.",
   u"Capterra / G2 — Pepperi-reviews", u"https://www.g2.com/products/pepperi/reviews")],
 [(u"Native apps, offline", u"Ja — de echte kracht", "app"),
  (u"Syncmodel", u"Apparaatgestuurd; reviewers melden resync-uitval tijdens bezoeken", "cart"),
  (u"Prijs", u"Niet gepubliceerd; gebruikerslicenties + modules", "fee"),
  (u"Proberen", u"Demo, dan salestraject", "pilot")],
 u"Kies Pepperi als je bedrijf rep-gedreven van-sales is met zware promotiebehoeften en je de implementatiepartner hebt die de setup verwacht. Zit de kern van je probleem in inkopers en reps die samen orders bouwen — betrouwbaar, offline, tegen een voorspelbare prijs — dan is dat het probleem waar RocketX omheen is gebouwd.")

# ---------------- FR ----------------
page("fr", "djust", u"DJUST",
 u"RocketX vs DJUST — un comparatif honnête pour le commerce de gros",
 u"La plateforme B2B française qui monte : références solides, pas de prix publics, pas d’application native. Ce qui la sépare de RocketX — avec sources.",
 u"DJUST mérite le respect : une équipe issue de Mirakl et des références françaises sérieuses dans la distribution et le négoce. Le comparatif honnête porte sur la forme du projet : rebâtir votre commerce, ou installer un canal à côté.",
 u"Une plateforme headless « made in France » pensée pour les ETI : automatisation du cycle de vente B2B, devis, paiements, synchronisation ERP/CRM, des déploiements annoncés en quelques semaines et des levées de fonds pour accélérer sur l’IA. Pour rebâtir un commerce B2B web complet avec un éditeur français, c’est un candidat légitime.",
 [(u"<b>Pas de prix publics :</b> tarification sur demande, entretien commercial obligatoire — le modèle inverse d’un forfait publié.",
   u"DJUST — site (août 2026)", u"https://www.djust.io/"),
  (u"<b>Ni application native, ni hors-ligne :</b> le site ne mentionne ni app iOS/Android pour vos acheteurs, ni catalogue consultable sans réseau — l’allée sans signal et la tournée restent hors du modèle.",
   u"DJUST — pages produit", u"https://www.djust.io/fr"),
  (u"<b>Une plateforme qui remplace :</b> DJUST devient le socle de votre commerce — un projet de re-plateforme — là où RocketX démarre à côté de votre boutique existante, sans rien débrancher.",
   u"DJUST — positionnement produit", u"https://www.djust.io/fr"),
  (u"<b>Une base d’avis publics encore mince :</b> les références sont réelles, la profondeur d’avis clients publics ne l’est pas encore — à peine une poignée d’avis sur G2.",
   u"G2 — DJUST", u"https://www.g2.com/products/djust/reviews")],
 [(u"Forme du projet", u"Re-plateforme : DJUST devient le socle", "beside"),
  (u"Acheteur mobile", u"Web responsive", "app"),
  (u"Panier", u"Sessions web individuelles", "cart"),
  (u"Prix", u"Sur demande", "fee"),
  (u"Essayer", u"Démo, puis cycle commercial", "pilot")],
 u"Choisissez DJUST si votre projet est de rebâtir tout votre commerce B2B sur un socle headless français, avec l’accompagnement projet que cela suppose. Si vos commandes naissent dans les allées, les réserves et les tournées — parfois sans réseau — et que votre boutique actuelle doit rester en place, c’est exactement l’espace pour lequel RocketX est construit.")

page("fr", "pepperi", u"Pepperi",
 u"RocketX vs Pepperi — un comparatif honnête pour le commerce de gros",
 u"Pepperi est la forme produit la plus proche : applications natives, hors-ligne, force de vente terrain. Les différences : fiabilité, transparence tarifaire, et ce qu’est le panier — avec sources.",
 u"Pepperi mérite le respect : plus de 1 000 clients, de vraies applications natives iOS et Android, la prise de commande hors-ligne pour les commerciaux terrain — y compris des références beauté. C’est la forme la plus proche de RocketX sur le marché — raison de plus pour nommer précisément les différences.",
 u"Une suite terrain mûre : prise de commande sur tablette, promotions commerciales, intégration SAP Business One, vingt ans de métier de l’agroalimentaire à la beauté. Si votre modèle est la vente en tournée à mécanique promotionnelle lourde, Pepperi a des fonctions que RocketX ne cherche pas à égaler.",
 [(u"<b>Le hors-ligne est la qualité la plus louée de Pepperi — et la fiabilité de synchronisation sa plainte la plus répétée.</b> Les avis récents décrivent plantages, gels et resynchronisations échouées en pleine visite client, plus des interruptions après mises à jour.",
   u"Capterra — avis Pepperi", u"https://www.capterra.com/p/146870/Pepperi/reviews/"),
  (u"<b>La page tarifs publique a disparu</b> — les deux variantes d’URL renvoient un 404 depuis le rachat par un fonds en 2024. Les sources tierces décrivent licences par utilisateur, modules et implémentation ; coûts réels rapportés en milieu de marché : 20 000–50 000+ $ par an.",
   u"WizCommerce — analyse des tarifs Pepperi", u"https://wizcommerce.com/blog/pepperi-pricing/"),
  (u"<b>Un support lié aux fuseaux horaires,</b> rapportent les avis, une parité Android plus lente, et un back-office qu’un avis français qualifie de « vieillissant et catastrophiquement lent ».",
   u"Capterra / G2 — avis Pepperi", u"https://www.g2.com/products/pepperi/reviews")],
 [(u"Apps natives, hors-ligne", u"Oui — sa vraie force", "app"),
  (u"Modèle de synchro", u"Piloté par l’appareil ; resynchronisations échouées rapportées en visite", "cart"),
  (u"Prix", u"Non publié ; licences par utilisateur + modules", "fee"),
  (u"Essayer", u"Démo, puis cycle commercial", "pilot")],
 u"Choisissez Pepperi si votre activité est la vente en tournée pilotée par les commerciaux, à forte mécanique promotionnelle, avec le partenaire d’implémentation que son installation suppose. Si le cœur de votre problème est que acheteurs et commerciaux construisent les commandes ensemble — de façon fiable, hors-ligne, à prix prévisible — c’est le problème autour duquel RocketX est construit.")

page("fr", "shopify-b2b", u"Shopify B2B",
 u"RocketX vs Shopify B2B — un comparatif honnête pour le commerce de gros",
 u"Où s’arrête le B2B de Shopify et où commence une plateforme de commande de gros : plafonds de commande, paniers partagés, applications natives, hors-ligne — avec sources.",
 u"Shopify excelle dans ce pour quoi il a été construit. La question, pour un grossiste, est plus étroite : le B2B posé dessus a-t-il la forme de votre flux de commande ? Voici le comparatif que nous voudrions lire, chaque affirmation sourcée.",
 u"Un checkout et un hébergement de classe mondiale, un écosystème d’applications immense, et depuis avril 2026 les primitives B2B — comptes entreprise, catalogues par client, règles de quantité, délais de paiement — incluses sur tous les plans. Pour une marque surtout B2C avec un canal de gros d’appoint, Shopify B2B suffit souvent — et nous le disons aux prospects concernés.",
 [(u"<b>Les commandes plafonnent à 500 lignes</b> (200 en commande provisoire) — au-delà, la commande échoue. Une commande de réassort en pièces détachées, mode ou cosmétique franchit ce seuil couramment.",
   u"Centre d’aide Shopify — considérations B2B", u"https://help.shopify.com/en/manual/b2b/getting-started/considerations"),
  (u"<b>Les paniers sont par appareil et par navigateur.</b> Un acheteur qui monte une commande pour validation par un responsable — la forme quotidienne de l’achat de gros — n’a, selon les mots de la communauté Shopify elle-même, « pas de solution prête à l’emploi ». Le fil est ouvert depuis juillet 2025.",
   u"Communauté Shopify — paniers partagés", u"https://community.shopify.com/t/how-do-your-b2b-customers-share-carts-or-use-carts-across-multiple-devices/551949"),
  (u"<b>Ni app native pour l’acheteur, ni catalogue hors-ligne.</b> La page B2B de Shopify décrit une vitrine web responsive ; l’acheteur dans une allée d’entrepôt sans signal ne fait pas partie du modèle.",
   u"Shopify Plus — solutions B2B", u"https://www.shopify.com/plus/solutions/b2b-ecommerce"),
  (u"<b>Au-delà d’un seuil de volume négociable, Plus bascule sur une commission variable</b> — les analyses citent ~0,25 % du volume mensuel en engagement 3 ans, plafonnée vers 40 k$/mois. Le forfait devient discrètement une part de votre croissance.",
   u"Tarifs Shopify Plus + analyse indépendante", u"https://www.brokenrubik.com/blog/shopify-plus-pricing-guide")],
 [(u"Panier", u"Par appareil, par navigateur", "cart"),
  (u"Acheteur mobile", u"Web responsive", "app"),
  (u"Forme du prix", u"2 300–2 500 $/mois, puis commission variable au-delà d’un seuil", "fee"),
  (u"Votre boutique", u"Est la plateforme", "beside"),
  (u"Essayer", u"Essai en libre-service (taillé B2C)", "pilot")],
 u"Choisissez Shopify si vous êtes d’abord une marque B2C avec un canal de gros modeste, des commandes confortablement sous les plafonds, et des acheteurs qui commandent au bureau. Ces entreprises sont bien servies — et ce ne sont pas elles pour qui RocketX est construit.")


def li(ui, text, src_label, src_url):
    return (u'<li>%s<span class="src">%s: <a href="%s" rel="noopener nofollow" '
            u'target="_blank">%s</a></span></li>' % (text, ui["src"], src_url, src_label))


def build(lang, slug):
    d = P_[(lang, slug)]
    ui = UI[lang]
    rx = RX[lang]
    facts = u"".join(li(ui, t, sl, su) for t, sl, su in d["facts"])
    rows = u"".join(u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, rx[key])
                    for a, b, key in d["table"])
    others = [s2 for s2 in SETS[lang] if s2 != slug]
    other_links = u" · ".join(u'<a href="/%s/%s/">%s</a>'
                              % (PREFIX[lang], o, P_[(lang, o)]["name"]) for o in others)
    # hreflang: the same competitor across the languages that carry it
    alts = u"\n".join(
        u'<link rel="alternate" hreflang="%s" href="%s/%s/%s/"/>' % (l2, SITE, PREFIX[l2], slug)
        for l2 in ("en", "de", "es", "nl", "fr") if (l2, slug) in P_)
    xd = "en" if ("en", slug) in P_ else lang
    alts += u'\n<link rel="alternate" hreflang="x-default" href="%s/%s/%s/"/>' % (
        SITE, PREFIX[xd], slug)
    home = "/#compare" if lang == "en" else "/%s/#compare" % lang

    html = u"""<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%(title)s</title>
<meta name="description" content="%(desc)s"/>
<link rel="canonical" href="%(site)s/%(prefix)s/%(slug)s/"/>
%(alts)s
<link rel="icon" href="/favicon.ico"/>
<style>/* fonts are self-hosted: no request leaves this domain */
%(fonts)s</style>
<style>%(css)s</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="%(homeroot)s"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
<a class="back" href="%(home)s">%(back)s</a>
</div></header>
<main><div class="wrap">
<div class="kick">%(kick)s</div>
<h1>RocketX vs %(name)s</h1>
<p class="lede">%(lede)s</p>

<h2>%(good_h)s</h2>
<p>%(good)s</p>

<h2>%(facts_h)s</h2>
<ul class="facts">%(facts)s</ul>

<h2>%(shapes)s</h2>
<div class="tblwrap"><table>
<thead><tr><th></th><th>%(name)s</th><th>RocketX</th></tr></thead>
<tbody>%(rows)s</tbody>
</table></div>

<h2>%(edge_h)s</h2>
<ul class="edge">%(edge)s</ul>

<div class="fair" data-fair>
<h2>%(fair_h)s</h2>
<p>%(fair)s</p>
</div>

<div class="ctabox">
<p>%(cta)s</p>
<a class="cta" href="%(pricing)s">%(ctabtn)s</a>
<a class="dl" download href="/assets/rocketx-business-case-%(lang)s.pdf">%(ctapdf)s</a>
</div>

<p class="note">%(note)s %(other_links)s.</p>
</div></main>
___SFOOT___
</body>
</html>
""" % dict(lang=lang, title=d["title"], desc=d["desc"], site=SITE,
           prefix=PREFIX[lang], slug=slug, alts=alts,
           fonts=io.open(os.path.join(ROOT, "scripts", "fonts_css.txt"),
                         encoding="utf-8").read().strip(),
           css=CSS.strip(),
           homeroot="/" if lang == "en" else "/%s/" % lang,
           home=home, back=ui["back"], kick=ui["kick"], name=d["name"],
           lede=d["lede"], good_h=ui["good"] % d["name"], good=d["good"],
           facts_h=ui["facts"], facts=facts, shapes=ui["shapes"], rows=rows,
           edge_h=EDGE_H[lang],
           edge=u"".join(u"<li>%s</li>" % e for e in EDGE[lang]),
           fair_h=ui["fair"], fair=d["fair"], cta=ui["cta"],
           pricing="/#pricing" if lang == "en" else "/%s/#pricing" % lang,
           ctabtn=ui["ctabtn"], ctapdf=ui["ctapdf"], note=ui["note"],
           other_links=other_links)
    html = html.replace("___SFOOT___", site_footer.footer_html(lang))
    outdir = os.path.join(ROOT, PREFIX[lang], slug)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


# kept for older imports: the English set
SLUGS = SETS["en"]

if __name__ == "__main__":
    for _lang in ("en", "de", "es", "nl", "fr"):
        for _slug in SETS[_lang]:
            print("wrote %s" % os.path.relpath(build(_lang, _slug), ROOT))
