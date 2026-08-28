#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 404.html.

A 404 can be served at any depth (/fr/whatever), so every link is root-absolute
and the language is read from the first path segment.

Ten strips in five languages is 150 panels. Drawing each one would produce a
600 KB error page, so the figures are defined once in <defs> and placed with
<use>; only the dialogue travels as data. Lines are wrapped here rather than in
the browser, because that is the one thing SVG will not do for you.

The first strip renders statically in English so the page still reads with no
JavaScript; the script then picks one of the ten at random and swaps the text.
"""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "404.html")
LANGS = ["en", "de", "es", "nl", "fr"]
CAL_YEAR = 2027                   # gen_calendar reads this, so the label matches the file
NB = u" "

# ---------------------------------------------------------------- the jokes
# Written per language rather than translated line by line - a punchline that
# survives a literal translation usually was not one. Each maps to something the
# site actually argues: logins, percentage fees, carts that die with the tab,
# aisles with no signal, approval chains, static PDFs, slow search, stock drift,
# and nothing being switched off.
STRIPS = [
 dict(screens=["404", "404", "0"], text={
  "en": [u"The order page is gone.", u"Since when?",
         "Since the redesign. We’re down exactly 404 orders."],
  "de": [u"Die Bestellseite ist weg.", u"Seit wann?",
         u"Seit dem Relaunch. Uns fehlen genau 404 Bestellungen."],
  "es": [u"La página de pedidos no está.", u"¿Desde cuándo?",
         u"Desde el rediseño. Nos faltan exactamente 404 pedidos."],
  "nl": [u"De bestelpagina is weg.", u"Sinds wanneer?",
         u"Sinds de restyling. We missen precies 404 orders."],
  "fr": [u"La page de commande a disparu.", u"Depuis quand" + NB + u"?",
         u"Depuis la refonte. Il nous manque exactement 404 commandes."]}),

 dict(screens=["LOGIN", "LOGIN", "LOGIN"], text={
  "en": [u"Customers cannot find the catalogue.", u"It is behind the login.",
         u"So is the login."],
  "de": [u"Kunden finden den Katalog nicht.", u"Der liegt hinter dem Login.",
         u"Das Login auch."],
  "es": [u"Los clientes no encuentran el catálogo.", u"Está detrás del acceso.",
         u"El acceso también."],
  "nl": [u"Klanten kunnen de catalogus niet vinden.", u"Die zit achter de login.",
         u"De login ook."],
  "fr": [u"Les clients ne trouvent pas le catalogue.",
         u"Il est derrière l’identification.", u"L’identification aussi."]}),

 dict(screens=["%", "%", "%"], text={
  "en": [u"The new platform takes a percentage of revenue.",
         u"So it costs more when we sell more?", u"They call it a partnership."],
  "de": [u"Die neue Plattform nimmt einen Prozentsatz vom Umsatz.",
         u"Sie kostet also mehr, wenn wir mehr verkaufen?",
         u"Man nennt das eine Partnerschaft."],
  "es": [u"La nueva plataforma cobra un porcentaje de los ingresos.",
         u"¿Cuesta más si vendemos más?", u"Lo llaman una alianza."],
  "nl": [u"Het nieuwe platform pakt een percentage van de omzet.",
         u"Dus het kost meer als we meer verkopen?", u"Ze noemen het een partnerschap."],
  "fr": [u"La nouvelle plateforme prend un pourcentage du chiffre d’affaires.",
         u"Elle coûte donc plus cher si nous vendons plus" + NB + u"?",
         u"Ils appellent cela un partenariat."]}),

 dict(screens=[u"—", u"—", u"—"], text={
  "en": [u"The buyer wanted to reorder from the warehouse.",
         u"There is no signal in the warehouse.", u"We told him to step outside."],
  "de": [u"Der Einkäufer wollte aus dem Lager nachbestellen.",
         u"Im Lager gibt es keinen Empfang.",
         u"Wir haben ihm gesagt, er soll rausgehen."],
  "es": [u"El comprador quería reponer desde el almacén.",
         u"En el almacén no hay cobertura.", u"Le dijimos que saliera fuera."],
  "nl": [u"De inkoper wilde bijbestellen vanuit het magazijn.",
         u"In het magazijn is geen bereik.", u"We zeiden dat hij naar buiten moest."],
  "fr": [u"L’acheteur voulait réassortir depuis l’entrepôt.",
         u"Il n’y a pas de réseau dans l’entrepôt.",
         u"Nous lui avons dit de sortir."]}),

 dict(screens=["6", "6", "6"], text={
  "en": [u"Why did one order take nine emails?", u"Six people had to approve it.",
         u"And who approved the six people?"],
  "de": [u"Warum brauchte eine Bestellung neun E-Mails?",
         u"Sechs Leute mussten sie freigeben.",
         u"Und wer hat die sechs Leute freigegeben?"],
  "es": [u"¿Por qué un pedido necesitó nueve correos?",
         u"Seis personas tenían que aprobarlo.",
         u"¿Y quién aprobó a las seis personas?"],
  "nl": [u"Waarom kostte één order negen mails?",
         u"Zes mensen moesten hem goedkeuren.",
         u"En wie heeft die zes mensen goedgekeurd?"],
  "fr": [u"Pourquoi une commande a-t-elle demandé neuf courriels" + NB + u"?",
         u"Six personnes devaient la valider.",
         u"Et qui a validé les six personnes" + NB + u"?"]}),

 dict(screens=["1", "1", "0"], text={
  "en": [u"The cart empties when they close the tab.", u"That is how sessions work.",
         u"Then that is how revenue works."],
  "de": [u"Der Warenkorb ist leer, wenn sie den Tab schließen.",
         u"So funktionieren Sitzungen.", u"Dann funktioniert der Umsatz eben auch so."],
  "es": [u"El carrito se vacía al cerrar la pestaña.",
         u"Así funcionan las sesiones.", u"Entonces así funcionan los ingresos."],
  "nl": [u"De winkelwagen is leeg als ze het tabblad sluiten.", u"Zo werken sessies.",
         u"Dan werkt de omzet ook zo."],
  "fr": [u"Le panier se vide quand ils ferment l’onglet.",
         u"C’est ainsi que fonctionnent les sessions.",
         u"Alors le chiffre d’affaires aussi."]}),

 dict(screens=["PDF", "PDF", "PDF"], text={
  "en": [u"We sent the buyer a ninety-page PDF catalogue.", u"Can he order from it?",
         u"He can print it."],
  "de": [u"Wir haben dem Einkäufer einen 90-seitigen PDF-Katalog geschickt.",
         u"Kann er daraus bestellen?", u"Er kann ihn ausdrucken."],
  "es": [u"Le mandamos al comprador un catálogo PDF de noventa páginas.",
         u"¿Puede pedir desde ahí?", u"Puede imprimirlo."],
  "nl": [u"We stuurden de inkoper een pdf-catalogus van negentig pagina’s.",
         u"Kan hij daaruit bestellen?", u"Hij kan hem afdrukken."],
  "fr": [u"Nous avons envoyé à l’acheteur un catalogue PDF de quatre-vingt-dix pages.",
         u"Peut-il commander depuis ce document" + NB + u"?", u"Il peut l’imprimer."]}),

 dict(screens=["4s", "4s", "4s"], text={
  "en": [u"Sales says the search is too slow.", u"Four seconds. A rounding error.",
         u"Then round it down."],
  "de": [u"Der Vertrieb sagt, die Suche sei zu langsam.",
         u"Vier Sekunden. Ein Rundungsfehler.", u"Dann runden Sie ab."],
  "es": [u"Ventas dice que la búsqueda es lenta.",
         u"Cuatro segundos. Un error de redondeo.", u"Pues redondea hacia abajo."],
  "nl": [u"Verkoop zegt dat het zoeken te traag is.",
         u"Vier seconden. Een afrondingsfout.", u"Rond het dan naar beneden af."],
  "fr": [u"Les commerciaux disent que la recherche est lente.",
         u"Quatre secondes. Une erreur d’arrondi.",
         u"Alors arrondissez vers le bas."]}),

 dict(screens=["ERP", "ERP", "ERP"], text={
  "en": [u"The ERP and the web shop disagree on stock.", u"Which one is right?",
         u"Whichever one the customer did not see."],
  "de": [u"ERP und Webshop sind sich beim Bestand nicht einig.", u"Welches stimmt?",
         u"Das, welches der Kunde nicht gesehen hat."],
  "es": [u"El ERP y la tienda no coinciden en el stock.",
         u"¿Cuál tiene razón?", u"El que el cliente no vio."],
  "nl": [u"Het ERP en de webshop zijn het oneens over de voorraad.", u"Welke klopt?",
         u"Die de klant niet gezien heeft."],
  "fr": [u"L’ERP et la boutique en ligne ne s’accordent pas sur le stock.",
         u"Lequel a raison" + NB + u"?", u"Celui que le client n’a pas vu."]}),

 dict(screens=["OLD", "OLD", "OLD"], text={
  "en": [u"The migration is finished.", u"And the old system?",
         u"Still running. Nobody would switch it off."],
  "de": [u"Die Migration ist abgeschlossen.", u"Und das alte System?",
         u"Läuft noch. Niemand wollte es abschalten."],
  "es": [u"La migración ha terminado.", u"¿Y el sistema antiguo?",
         u"Sigue funcionando. Nadie quiso apagarlo."],
  "nl": [u"De migratie is klaar.", u"En het oude systeem?",
         u"Draait nog. Niemand wilde het uitzetten."],
  "fr": [u"La migration est terminée.", u"Et l’ancien système" + NB + u"?",
         u"Il tourne encore. Personne n’a voulu le débrancher."]}),

 dict(screens=["?", "?", "?"], text={
  "en": [u"A customer called to ask what he ordered last time.",
         u"Can he not look it up?", u"Neither can we."],
  "de": [u"Ein Kunde hat angerufen und gefragt, was er zuletzt bestellt hat.",
         u"Kann er das nicht nachsehen?", u"Wir auch nicht."],
  "es": [u"Un cliente llam\u00f3 para preguntar qu\u00e9 pidi\u00f3 la \u00faltima vez.",
         u"\u00bfNo puede consultarlo?", u"Nosotros tampoco."],
  "nl": [u"Een klant belde om te vragen wat hij vorige keer besteld had.",
         u"Kan hij dat niet opzoeken?", u"Wij ook niet."],
  "fr": [u"Un client a appel\u00e9 pour demander ce qu\u2019il avait command\u00e9.",
         u"Il ne peut pas le consulter\u00a0?", u"Nous non plus."]}),

 dict(screens=["@", "@", "0"], text={
  "en": [u"We emailed every buyer about the restock.", u"How many opened it?",
         u"The spam filter did."],
  "de": [u"Wir haben allen Eink\u00e4ufern eine E-Mail zum Nachschub geschickt.",
         u"Wie viele haben sie ge\u00f6ffnet?", u"Der Spamfilter."],
  "es": [u"Mandamos un correo a todos los compradores sobre la reposici\u00f3n.",
         u"\u00bfCu\u00e1ntos lo abrieron?", u"El filtro de spam."],
  "nl": [u"We mailden alle inkopers over de nieuwe voorraad.",
         u"Hoeveel hebben hem geopend?", u"Het spamfilter."],
  "fr": [u"Nous avons \u00e9crit \u00e0 tous les acheteurs au sujet du r\u00e9assort.",
         u"Combien l\u2019ont ouvert\u00a0?", u"Le filtre antispam."]}),
]

UI = {
 "en": dict(h="This page was never ordered.",
            p="The link is broken or the page has moved. Nothing has been switched off "
              "&mdash; you are simply at an address that does not exist.",
            home="Back to the home page", deck="Business case (PDF)", one="One page (PDF)",
            cal="2027 calendar (PDF)", altp="A three-panel office cartoon."),
 "de": dict(h="Diese Seite wurde nie bestellt.",
            p="Der Link ist defekt oder die Seite ist umgezogen. Abgeschaltet wurde nichts "
              "&mdash; Sie sind schlicht auf einer Adresse, die es nicht gibt.",
            home="Zur Startseite", deck="Business Case (PDF)", one="Eine Seite (PDF)",
            cal="Kalender 2027 (PDF)", altp="Ein Cartoon in drei Bildern."),
 "es": dict(h="Esta p&aacute;gina nunca se pidi&oacute;.",
            p="El enlace est&aacute; roto o la p&aacute;gina se ha movido. No se ha apagado "
              "nada: simplemente est&aacute;s en una direcci&oacute;n que no existe.",
            home="Volver al inicio", deck="Caso de negocio (PDF)", one="Una p&aacute;gina (PDF)",
            cal="Calendario 2027 (PDF)", altp="Una viñeta de oficina en tres partes."),
 "nl": dict(h="Deze pagina is nooit besteld.",
            p="De link is stuk of de pagina is verhuisd. Er is niets uitgezet &mdash; je bent "
              "gewoon op een adres dat niet bestaat.",
            home="Terug naar de homepage", deck="Business case (pdf)",
            one="E&eacute;n pagina (pdf)", cal="Kalender 2027 (pdf)", altp="Een kantoorcartoon in drie panelen."),
 "fr": dict(h="Cette page n&rsquo;a jamais &eacute;t&eacute; command&eacute;e.",
            p="Le lien est cass&eacute; ou la page a &eacute;t&eacute; d&eacute;plac&eacute;e. "
              "Rien n&rsquo;a &eacute;t&eacute; d&eacute;branch&eacute;&nbsp;: vous &ecirc;tes "
              "simplement &agrave; une adresse qui n&rsquo;existe pas.",
            home="Retour &agrave; l&rsquo;accueil", deck="Argumentaire (PDF)",
            one="Une page (PDF)", cal="Calendrier 2027 (PDF)", altp="Un dessin de bureau en trois cases."),
}

# ---------------------------------------------------------------- text fitting
# Inter at 15px: the average advance across this copy sits close to 0.515em.
def wrap(text, max_px, size=15.0, per_em=0.515):
    budget = int(max_px / (size * per_em))
    lines, cur = [], ""
    for w in text.split(" "):
        trial = (cur + " " + w).strip()
        if len(trial) <= budget or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- drawing
INK = "#12233F"
PAPER = "#F7F2E6"
FAINT = "#9AA6BA"
PW, PH, GAP = 300, 250, 24
FLOOR = 216
DESK_Y = 168
BX, BY, BW = 16, 10, 268          # speech-bubble box
LH = 18.0                         # line height inside a bubble
TAIL_H = 12                       # how far the tail drops below the bubble
# per panel: developer x, desk span, monitor x, does the manager appear
LAYOUT = [(206, "deskA", 234, True), (146, "deskB", 196, False), (206, "deskA", 234, True)]
TAIL = [68, 140, 68]              # bubble tail: manager, developer, manager


def head(cx, cy, r, glasses):
    s = ['<circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="%s" stroke-width="2.6"/>'
         % (cx, cy, r, INK)]
    if glasses:
        for dx in (-6, 6):
            s.append('<circle cx="%d" cy="%d" r="5.4" fill="#fff" stroke="%s" '
                     'stroke-width="2"/>' % (cx + dx, cy - 2, INK))
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>'
                 % (cx - 1, cy - 2, cx + 1, cy - 2, INK))
    for dx in (-6, 6):
        s.append('<circle cx="%d" cy="%d" r="1.9" fill="%s"/>' % (cx + dx, cy - 2, INK))
    # deadpan: a flat line, never a smile
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
             'stroke-linecap="round"/>' % (cx - 4, cy + 8, cx + 4, cy + 8, INK))
    return "".join(s)


def manager():
    """Standing, tie, three hairs. Drawn about the origin so <use> can place it."""
    hy = -86
    s = []
    for dx in (-9, 9):
        s.append('<line x1="%d" y1="0" x2="%d" y2="-28" stroke="%s" stroke-width="2.6" '
                 'stroke-linecap="round"/>' % (dx, dx, INK))
    s.append('<path d="M-21 -26 q0 -36 21 -36 q21 0 21 36 z" fill="#fff" stroke="%s" '
             'stroke-width="2.6" stroke-linejoin="round"/>' % INK)
    s.append('<line x1="-20" y1="-54" x2="-35" y2="-32" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % INK)
    s.append('<line x1="20" y1="-54" x2="35" y2="-38" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % INK)
    s.append('<path d="M0 -62 l5 13 l-5 10 l-5 -10 z" fill="%s"/>' % INK)
    s.append(head(0, hy, 17, False))
    for dx, dy in ((-8, -13), (0, -16), (8, -13)):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" '
                 'stroke-linecap="round"/>' % (dx, hy - 15, dx + dx // 2, hy - 15 + dy, INK))
    return "".join(s)


def developer():
    """Seated: the torso stops at the desk edge, which the desk then covers."""
    hy = -52
    s = ['<path d="M-20 4 q0 -30 20 -30 q20 0 20 30 z" fill="#fff" stroke="%s" '
         'stroke-width="2.6" stroke-linejoin="round"/>' % INK]
    s.append('<line x1="-19" y1="-20" x2="-31" y2="2" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % INK)
    s.append('<line x1="19" y1="-20" x2="31" y2="2" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % INK)
    s.append(head(0, hy, 16, True))
    for dx in (-9, -3, 3, 9):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
                 'stroke-linecap="round"/>' % (dx, hy - 14, dx, hy - 20, INK))
    return "".join(s)


def partition():
    return ('<path d="M14 %d h272 v-82 h-272 z" fill="none" stroke="%s" stroke-width="2" '
            'opacity=".4"/>'
            '<line x1="150" y1="%d" x2="150" y2="%d" stroke="%s" stroke-width="2" opacity=".4"/>'
            '<line x1="0" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>'
            % (DESK_Y - 6, FAINT, DESK_Y - 6, DESK_Y - 88, FAINT, FLOOR, PW, FLOOR, INK))


def desk(x1, x2):
    """Opaque slab drawn after the figure, so the figure sits behind it."""
    return ('<rect x="%d" y="%d" width="%d" height="9" rx="2" fill="%s" stroke="%s" '
            'stroke-width="2.4"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>'
            '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>'
            % (x1, DESK_Y, x2 - x1, PAPER, INK, x1 + 8, DESK_Y + 9, x1 + 8, FLOOR, INK,
               x2 - 8, DESK_Y + 9, x2 - 8, FLOOR, INK))


def monitor_art():
    """Screen at the origin; the label is written in by the script."""
    return ('<rect x="0" y="0" width="58" height="40" rx="4" fill="#fff" stroke="%s" '
            'stroke-width="2.4"/>'
            '<rect x="19" y="41" width="20" height="5" rx="1" fill="%s"/>'
            '<line x1="29" y1="40" x2="29" y2="41" stroke="%s" stroke-width="2.4"/>'
            % (INK, INK, INK))


def static_bubble(lines, tail_x):
    """Rendered for the first strip so the page still reads without JavaScript."""
    h = 16 + LH * len(lines)
    ty = BY + h
    out = ['<rect x="%d" y="%d" width="%d" height="%.1f" rx="11" fill="#fff" stroke="%s" '
           'stroke-width="2.2"/>' % (BX, BY, BW, h, INK),
           '<path d="M%d %.1f l11 0 l-6 %d z" fill="#fff"/>' % (tail_x, ty - 1, TAIL_H),
           '<path d="M%d %.1f l-6 %d l11 -%d" fill="none" stroke="%s" stroke-width="2.2" '
           'stroke-linejoin="round"/>' % (tail_x, ty - 1, TAIL_H, TAIL_H, INK),
           '<rect x="%.1f" y="%.1f" width="12" height="3" fill="#fff"/>'
           % (tail_x - .5, ty - 2.5)]
    for i, ln in enumerate(lines):
        out.append('<text x="%d" y="%.1f" font-size="15" fill="%s">%s</text>'
                   % (BX + 14, BY + 22 + i * LH, INK, esc(ln)))
    return "".join(out)


def strip_svg():
    """One skeleton: art placed by <use>, dialogue filled in per strip."""
    total_w = PW * 3 + GAP * 2
    o = ['<svg id="strip" class="strip" viewBox="0 0 %d %d" '
         'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="">' % (total_w, PH),
         '<defs><clipPath id="clipP"><rect x="3" y="3" width="%d" height="%d" rx="6"/>'
         '</clipPath>' % (PW - 6, PH - 6),
         '<g id="mgr">%s</g><g id="dev">%s</g><g id="part">%s</g>'
         % (manager(), developer(), partition()),
         '<g id="deskA">%s</g><g id="deskB">%s</g><g id="mon">%s</g>'
         % (desk(172, 296), desk(112, 268), monitor_art()),
         '</defs>']
    first = STRIPS[0]
    for i, (dev_cx, deskid, mon_x, has_mgr) in enumerate(LAYOUT):
        o.append('<g transform="translate(%d 0)">' % (i * (PW + GAP)))
        o.append('<rect x="1.4" y="1.4" width="%.1f" height="%.1f" rx="7" fill="%s" '
                 'stroke="%s" stroke-width="2.8"/>' % (PW - 2.8, PH - 2.8, PAPER, INK))
        o.append('<g clip-path="url(#clipP)">')
        o.append('<use href="#part"/>')
        o.append('<use href="#dev" x="%d" y="%d"/>' % (dev_cx, DESK_Y))
        o.append('<use href="#%s"/>' % deskid)
        o.append('<use href="#mon" x="%d" y="%d"/>' % (mon_x, DESK_Y - 46))
        o.append('<text class="scr" id="scr%d" x="%d" y="%d" text-anchor="middle" '
                 'font-size="16" fill="%s">%s</text>'
                 % (i, mon_x + 29, DESK_Y - 21, INK, esc(first["screens"][i])))
        if has_mgr:
            o.append('<use href="#mgr" x="74" y="%d"/>' % FLOOR)
        o.append('</g>')
        o.append('<g class="bub" id="bub%d">%s</g>'
                 % (i, static_bubble(wrap(first["text"]["en"][i], BW - 28), TAIL[i])))
        o.append('</g>')
    o.append('</svg>')
    return "".join(o)


# ---------------------------------------------------------------- page
CSS = u"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--ice:#EDF2FB;--mist:#8FA1C4;--sky:#60A5FA;--blue:#2563EB;--line:#1E2E4C}
html{-webkit-text-size-adjust:100%}
body{background:var(--void);color:var(--ice);line-height:1.6;
     font-family:Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;
     min-height:100vh;display:flex;flex-direction:column}
a{color:inherit;text-decoration:none}
.wrap{width:100%;max-width:1000px;margin:0 auto;padding:0 24px}
header{padding:26px 0}
.brand{display:inline-flex;align-items:center;gap:10px}
.brand img{width:30px;height:30px;border-radius:8px;display:block}
.brand b{font-family:"Space Grotesk",Inter,sans-serif;font-size:17px;letter-spacing:-.4px}
main{flex:1;display:flex;align-items:center;padding:16px 0 56px}
.code{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:2.4px;
      color:var(--sky);margin-bottom:14px}
h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:clamp(28px,5vw,44px);
   line-height:1.12;letter-spacing:-1px;font-weight:600;max-width:16ch}
.lede{color:var(--mist);margin-top:14px;max-width:56ch;font-size:16px}
.strip{display:block;width:100%;height:auto;margin:34px 0 8px;border-radius:10px;
       filter:drop-shadow(0 18px 34px rgba(0,0,0,.5))}
.strip text{font-family:Inter,Helvetica,Arial,sans-serif}
.strip .scr{font-family:"IBM Plex Mono",monospace;font-weight:500}
.btns{display:flex;flex-wrap:wrap;gap:14px 18px;align-items:center;margin-top:26px}
.cta{background:var(--blue);color:#fff;padding:13px 24px;border-radius:9px;font-weight:600;
     font-size:15px;transition:background .25s}
.cta:hover{background:#1D4ED8}
.dl{display:inline-flex;align-items:center;gap:8px;font-size:14px;color:var(--mist);
    transition:color .25s}
.dl:hover{color:var(--sky)}
.dl svg{width:15px;height:15px;fill:currentColor;flex:none}
.sep{color:var(--line);user-select:none}
footer{border-top:1px solid var(--line);padding:18px 0;color:var(--mist);font-size:13px}
@media(max-width:720px){.strip{margin-top:26px}main{padding-bottom:40px}}
"""

DLICON = ('<svg aria-hidden="true" viewBox="0 0 24 24">'
          '<path d="M12 16l-5-5 1.4-1.4L11 12.2V4h2v8.2l2.6-2.6L17 11z"/>'
          '<path d="M5 18h14v2H5z"/></svg>')


def build():
    data = dict((l, [[wrap(s["text"][l][i], BW - 28) for i in range(3)] for s in STRIPS])
                for l in LANGS)
    screens = [s["screens"] for s in STRIPS]

    heads, acts = [], []
    for l in LANGS:
        u = UI[l]
        hide = "" if l == "en" else " hidden"
        heads.append(u'<div class="l l-%s"%s><div class="code">ERROR 404</div><h1>%s</h1>'
                     u'<p class="lede">%s</p></div>' % (l, hide, u["h"], u["p"]))
        acts.append(
            u'<div class="l l-%s"%s><div class="btns">'
            u'<a class="cta" href="/%s">%s</a>'
            u'<a class="dl" href="/assets/rocketx-business-case-%s.pdf" download>%s<span>%s</span></a>'
            u'<span class="sep" aria-hidden="true">&middot;</span>'
            u'<a class="dl" href="/assets/rocketx-one-page-%s.pdf" download>%s<span>%s</span></a>'
            u'<span class="sep" aria-hidden="true">&middot;</span>'
            u'<a class="dl" href="/assets/rocketx-calendar-%s.pdf" download>%s<span>%s</span></a>'
            u'</div></div>'
            % (l, hide, "" if l == "en" else l + "/", u["home"],
               l, DLICON, u["deck"], l, DLICON, u["one"], l, DLICON, u["cal"]))

    import site_footer  # lazy: site_footer -> gen_calendar -> gen_404 would cycle at module load
    foots = u'<style>' + site_footer.CSS.strip() + u'</style>' + u"\n".join(
        u'<div class="l l-%s"%s>%s</div>' % (
            l, "" if l == "en" else " hidden",
            site_footer.footer_html(l, with_style=False))
        for l in LANGS)

    html = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>404 &mdash; RocketX</title>
<meta name="robots" content="noindex,follow"/>
<link rel="icon" href="/favicon.ico"/>
<style>/* fonts are self-hosted: no request leaves this domain */\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url('/assets/fonts/ibmplexmono-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url('/assets/fonts/ibmplexmono-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;src:url('/assets/fonts/ibmplexmono-500-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;src:url('/assets/fonts/ibmplexmono-500-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url('/assets/fonts/inter-400-600-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url('/assets/fonts/inter-400-600-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400 700;font-display:swap;src:url('/assets/fonts/spacegrotesk-400-700-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400 700;font-display:swap;src:url('/assets/fonts/spacegrotesk-400-700-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}</style>
<style>%s</style>
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">
<img src="/assets/logo.png" alt="" width="500" height="500"/><b>RocketX</b></a></div></header>
<main><div class="wrap">
%s
%s
%s
</div></main>
___SFOOT___
<script>
(function(){
  var LANGS=%s, DATA=%s, SCREENS=%s, ALT=%s;
  var TAIL=%s, BX=%d, BY=%d, BW=%d, LH=%s, TH=%d, INK='%s';

  var seg=location.pathname.split('/').filter(Boolean)[0];
  var l=LANGS.indexOf(seg)>-1?seg:null;
  if(!l){
    var nav=navigator.languages||[navigator.language||'en'];
    for(var i=0;i<nav.length&&!l;i++){
      var c=String(nav[i]).slice(0,2).toLowerCase();
      if(LANGS.indexOf(c)>-1)l=c;
    }
  }
  l=l||'en';
  document.documentElement.lang=l;
  if(l!=='en'){
    [].forEach.call(document.querySelectorAll('.l-en'),function(e){e.hidden=true;});
    [].forEach.call(document.querySelectorAll('.l-'+l),function(e){e.hidden=false;});
  }

  var NS='http://www.w3.org/2000/svg';
  function el(n,a){var e=document.createElementNS(NS,n);
    for(var k in a)e.setAttribute(k,a[k]);return e;}

  var panels=DATA[l]||DATA.en;
  var n=Math.floor(Math.random()*panels.length);
  var strip=panels[n];

  for(var p=0;p<3;p++){
    var g=document.getElementById('bub'+p);
    while(g.firstChild)g.removeChild(g.firstChild);
    var lines=strip[p], h=16+LH*lines.length, tx=TAIL[p], ty=BY+h;
    g.appendChild(el('rect',{x:BX,y:BY,width:BW,height:h,rx:11,fill:'#fff',
      stroke:INK,'stroke-width':2.2}));
    g.appendChild(el('path',{d:'M'+tx+' '+(ty-1)+' l11 0 l-6 '+TH+' z',fill:'#fff'}));
    g.appendChild(el('path',{d:'M'+tx+' '+(ty-1)+' l-6 '+TH+' l11 -'+TH,fill:'none',
      stroke:INK,'stroke-width':2.2,'stroke-linejoin':'round'}));
    g.appendChild(el('rect',{x:tx-0.5,y:ty-2.5,width:12,height:3,fill:'#fff'}));
    for(var i=0;i<lines.length;i++){
      var t=el('text',{x:BX+14,y:BY+22+i*LH,'font-size':15,fill:INK});
      t.appendChild(document.createTextNode(lines[i]));
      g.appendChild(t);
    }
    var s=document.getElementById('scr'+p), lab=SCREENS[n][p];
    s.textContent=lab;
    s.setAttribute('font-size', lab.length>3?12:16);
  }

  var said=strip.map(function(x){return x.join(' ');}).join(' ');
  document.getElementById('strip').setAttribute('aria-label', ALT[l]+' '+said);
})();
</script>
</body>
</html>
""" % (CSS.strip(), "\n".join(heads), strip_svg(), "\n".join(acts),
       json.dumps(LANGS), json.dumps(data, ensure_ascii=False),
       json.dumps(screens, ensure_ascii=False),
       json.dumps(dict((l, UI[l]["altp"]) for l in LANGS), ensure_ascii=False),
       json.dumps(TAIL), BX, BY, BW, LH, TAIL_H, INK)
    html = html.replace("___SFOOT___", foots)
    io.open(OUT, "w", encoding="utf-8").write(html)
    return html


if __name__ == "__main__":
    h = build()
    print("wrote 404.html (%.1f KB, %d strips x %d languages)"
          % (len(h.encode("utf-8")) / 1024.0, len(STRIPS), len(LANGS)))
