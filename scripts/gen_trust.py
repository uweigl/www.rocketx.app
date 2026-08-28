#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the trust pages, one per language, at each market's natural path.

Nearly every sentence is taken verbatim from the deck's compliance page and
the FAQ - the claims that were already written, reviewed and printed. The page
invents nothing: no SLA number, no penetration-test cadence, no certification
of RocketX itself appears here until those facts exist. What a security
reviewer gets is the residency, the entities, the facility certifications, the
subprocessor commitment and the exit rights - and an address that answers
questionnaires.
"""
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_deck
import faq
import gen_legal
import site_footer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rocketx.app"

PATHS = {"en": "trust", "de": "de/sicherheit", "es": "es/seguridad",
         "nl": "nl/beveiliging", "fr": "fr/securite"}

NB = u" "
AP = u"’"

T = {
 "en": dict(
  title=u"Security & Trust — RocketX",
  h1=u"Security & Trust",
  intro=u"Short answers to the questions a security review asks first — and the same commitments in both jurisdictions.",
  web_h=u"This website",
  web=u"It practices the same restraint: no trackers, no cookies, fonts served from this domain. Details in the <a href='/privacy/'>privacy notice</a>.",
  ask_h=u"Ask directly",
  ask=u"Security questionnaires and audit questions: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. We answer them ourselves.",
  agr_h=u"What the agreement puts in writing",
  users_h=u"Named users, attributable actions",
  users=u"Seats and users are unlimited on every plan, with no per-user charges — so there is never a commercial reason for shared logins. Several people can work the same cart at once, and every change is attributed to a named person and timestamped.",
  gxp_h=u"For regulated industries",
  gxp=u"Pharmaceutical and life-science wholesalers assess suppliers against 21 CFR Part 11 and EU Annex 11. The properties those assessments look for first — unique named accounts, attributed and timestamped changes, written retention and deletion policy, a current subprocessor list — are described above, in the contract, or both. We support supplier-qualification audits, and validation against your own SOPs happens where it belongs: in the pilot, against agreed measures. We do not claim a certification we do not hold.",
  label=u"Security"),
 "de": dict(
  title=u"Sicherheit & Vertrauen — RocketX",
  h1=u"Sicherheit & Vertrauen",
  intro=u"Kurze Antworten auf die Fragen, die eine Sicherheitsprüfung zuerst stellt — mit denselben Zusagen in beiden Rechtsräumen.",
  web_h=u"Diese Website",
  web=u"Sie übt dieselbe Zurückhaltung: keine Tracker, keine Cookies, Schriften von dieser Domain. Details in der <a href='/de/datenschutz/'>Datenschutzerklärung</a>.",
  ask_h=u"Direkt fragen",
  ask=u"Sicherheitsfragebögen und Audit-Fragen: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Wir beantworten sie selbst.",
  agr_h=u"Was der Vertrag schriftlich festhält",
  users_h=u"Benannte Nutzer, zurechenbare Aktionen",
  users=u"Plätze und Nutzer sind in jedem Plan unbegrenzt, ohne Gebühr pro Nutzer — es gibt also nie einen kommerziellen Grund für geteilte Logins. Mehrere Personen arbeiten gleichzeitig am selben Warenkorb, und jede Änderung ist einer benannten Person zugeordnet und mit Zeitstempel versehen.",
  gxp_h=u"Für regulierte Branchen",
  gxp=u"Pharma- und Life-Science-Großhändler prüfen Lieferanten gegen 21 CFR Part 11 und EU-Annex 11. Die Eigenschaften, nach denen diese Prüfungen zuerst fragen — eindeutige benannte Konten, zugeordnete und zeitgestempelte Änderungen, schriftliche Aufbewahrungs- und Löschrichtlinie, eine aktuelle Subprozessoren-Liste — stehen oben, im Vertrag oder an beiden Stellen. Wir unterstützen Lieferantenqualifizierungs-Audits, und die Validierung gegen Ihre eigenen SOPs findet dort statt, wo sie hingehört: im Piloten, gegen vereinbarte Messgrößen. Eine Zertifizierung, die wir nicht besitzen, behaupten wir nicht.",
  label=u"Sicherheit"),
 "es": dict(
  title=u"Seguridad y confianza — RocketX",
  h1=u"Seguridad y confianza",
  intro=u"Respuestas breves a lo primero que pregunta una revisión de seguridad — con los mismos compromisos en ambas jurisdicciones.",
  web_h=u"Este sitio",
  web=u"Practica la misma contención: sin rastreadores, sin cookies, fuentes servidas desde este dominio. Detalles en el <a href='/es/privacidad/'>aviso de privacidad</a>.",
  ask_h=u"Pregunta directamente",
  ask=u"Cuestionarios de seguridad y preguntas de auditoría: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Los respondemos nosotros.",
  agr_h=u"Lo que el contrato deja por escrito",
  users_h=u"Usuarios con nombre, acciones atribuibles",
  users=u"Los puestos y usuarios son ilimitados en todos los planes, sin cargo por usuario — así que nunca hay un motivo comercial para compartir credenciales. Varias personas trabajan el mismo carrito a la vez, y cada cambio queda atribuido a una persona con nombre y con marca de tiempo.",
  gxp_h=u"Para industrias reguladas",
  gxp=u"Los mayoristas farmacéuticos y de ciencias de la vida evalúan a sus proveedores frente a 21 CFR Part 11 y el Anexo 11 de la UE. Las propiedades que esas evaluaciones buscan primero — cuentas únicas con nombre, cambios atribuidos y con marca de tiempo, política escrita de retención y borrado, lista vigente de subencargados — están arriba, en el contrato o en ambos. Apoyamos auditorías de calificación de proveedores, y la validación frente a tus propios SOP ocurre donde corresponde: en el piloto, contra métricas acordadas. No afirmamos ninguna certificación que no tengamos.",
  label=u"Seguridad"),
 "nl": dict(
  title=u"Beveiliging & vertrouwen — RocketX",
  h1=u"Beveiliging & vertrouwen",
  intro=u"Korte antwoorden op wat een securityreview het eerst vraagt — met dezelfde toezeggingen in beide rechtsgebieden.",
  web_h=u"Deze site",
  web=u"Hij betracht dezelfde terughoudendheid: geen trackers, geen cookies, lettertypen vanaf dit domein. Details in de <a href='/nl/privacy/'>privacyverklaring</a>.",
  ask_h=u"Vraag het direct",
  ask=u"Securityvragenlijsten en auditvragen: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. We beantwoorden ze zelf.",
  agr_h=u"Wat het contract zwart-op-wit zet",
  users_h=u"Benoemde gebruikers, toerekenbare acties",
  users=u"Plaatsen en gebruikers zijn onbeperkt in elk plan, zonder kosten per gebruiker — er is dus nooit een commerciële reden voor gedeelde logins. Meerdere mensen werken tegelijk in dezelfde winkelwagen, en elke wijziging is toegeschreven aan een benoemde persoon en voorzien van een tijdstempel.",
  gxp_h=u"Voor gereguleerde sectoren",
  gxp=u"Farmaceutische en life-science-groothandels toetsen leveranciers aan 21 CFR Part 11 en EU-Annex 11. De eigenschappen waar die toetsen het eerst naar vragen — unieke benoemde accounts, toegeschreven en tijdgestempelde wijzigingen, schriftelijk bewaar- en verwijderbeleid, een actuele lijst van subverwerkers — staan hierboven, in het contract of allebei. We ondersteunen leverancierskwalificatie-audits, en validatie tegen je eigen SOP's gebeurt waar die hoort: in de pilot, tegen afgesproken meetpunten. Een certificering die we niet hebben, claimen we niet.",
  label=u"Beveiliging"),
 "fr": dict(
  title=u"Sécurité et confiance — RocketX",
  h1=u"Sécurité et confiance",
  intro=u"Des réponses brèves aux premières questions d" + AP + u"une revue de sécurité — avec les mêmes engagements dans les deux juridictions.",
  web_h=u"Ce site",
  web=u"Il pratique la même retenue" + NB + u": pas de traceurs, pas de cookies, des polices servies depuis ce domaine. Les détails sont dans la <a href='/fr/confidentialite/'>politique de confidentialité</a>.",
  ask_h=u"Demandez directement",
  ask=u"Questionnaires de sécurité et questions d" + AP + u"audit" + NB + u": <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Nous y répondons nous-mêmes.",
  agr_h=u"Ce que le contrat met par écrit",
  users_h=u"Utilisateurs nommés, actions attribuables",
  users=u"Les postes et utilisateurs sont illimités dans chaque plan, sans frais par utilisateur — il n’y a donc jamais de raison commerciale de partager des identifiants. Plusieurs personnes travaillent le même panier en même temps, et chaque modification est attribuée à une personne nommée et horodatée.",
  gxp_h=u"Pour les industries réglementées",
  gxp=u"Les grossistes pharmaceutiques et des sciences de la vie évaluent leurs fournisseurs au regard du 21 CFR Part 11 et de l’annexe 11 de l’UE. Les propriétés que ces évaluations recherchent d’abord — comptes nommés uniques, modifications attribuées et horodatées, politique écrite de conservation et de suppression, liste à jour des sous-traitants — figurent ci-dessus, au contrat, ou aux deux. Nous accompagnons les audits de qualification fournisseur, et la validation face à vos propres SOP se fait là où elle a sa place : dans le pilote, contre des mesures convenues. Nous ne revendiquons aucune certification que nous ne détenons pas.",
  label=u"Sécurité"),
}

# which deck rows compose the page: (eu row index, us row index or None)
THEMES = [(0, 0), (1, 1), (2, 2), (3, 3), (5, None), (None, 4)]


def build(lang):
    d = T[lang]
    C = gen_deck.C[lang]
    secs = []
    for eu_i, us_i in THEMES:
        head = C["eu"][eu_i][0] if eu_i is not None else C["us"][us_i][0]
        parts = []
        # the deck's own rule: the home jurisdiction leads (en/es contract US-first)
        pair = (("us", us_i), ("eu", eu_i)) if lang in ("en", "es") \
            else (("eu", eu_i), ("us", us_i))
        for jur, idx in pair:
            if idx is not None:
                parts.append(u'<p><span class="jur">%s</span> %s</p>'
                             % (jur.upper(), C[jur][idx][1]))
        if eu_i is not None and us_i is None:
            parts = [u"<p>%s</p>" % C["eu"][eu_i][1]]
        if eu_i is None:
            parts = [u"<p>%s</p>" % C["us"][us_i][1]]
        secs.append(u"<h2>%s</h2>\n%s" % (head, u"\n".join(parts)))
    secs.append(u"<h2>%s</h2>\n<p>%s</p>" % (d["users_h"], d["users"]))
    agr = u"".join(u"<li>%s</li>" % it for it in C["at"])
    secs.append(u"<h2>%s</h2>\n<ul class=\"agr\">%s</ul>" % (d["agr_h"], agr))
    secs.append(u"<h2>%s</h2>\n<p>%s</p>" % (d["gxp_h"], d["gxp"]))
    secs.append(u"<h2>%s</h2>\n<p>%s</p>" % (d["web_h"], d["web"]))
    secs.append(u"<h2>%s</h2>\n<p>%s</p>" % (d["ask_h"], d["ask"]))

    alts = u"\n".join(
        u'<link rel="alternate" hreflang="%s" href="%s/%s/"/>' % (l, SITE, p)
        for l, p in PATHS.items())
    alts += u'\n<link rel="alternate" hreflang="x-default" href="%s/%s/"/>' % (SITE, PATHS["en"])

    html = u"""<!doctype html>
<html lang="%s">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%s</title>
<meta name="description" content="%s"/>
<link rel="canonical" href="%s/%s/"/>
%s
<link rel="icon" href="/favicon.ico"/>
<style>%s
%s
.agr{list-style:none;margin:6px 0}
.agr li{color:var(--mist);font-size:15px;padding:7px 0 7px 26px;position:relative;max-width:68ch}
.agr li:before{content:'\\2713';position:absolute;left:2px;color:var(--sky)}
.jur{font-family:"IBM Plex Mono",monospace;font-size:10px;letter-spacing:1.5px;
  color:var(--sky);border:1px solid var(--line);border-radius:5px;padding:2px 7px;
  margin-right:9px;vertical-align:1px}
</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="/%s"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
</div></header>
<main><div class="wrap">
<h1>%s</h1>
<p class="intro">%s</p>
%s
</div></main>
___SFOOT___
</body>
</html>
""" % (lang, d["title"], d["intro"].replace('"', "&quot;"), SITE, PATHS[lang],
       alts, gen_legal.FONTS, gen_legal.CSS.strip(),
       "" if lang == "en" else lang + "/",
       d["h1"], d["intro"], u"\n".join(secs))
    html = html.replace("___SFOOT___", site_footer.footer_html(lang))
    outdir = os.path.join(ROOT, PATHS[lang])
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    for lang in ("en", "de", "es", "nl", "fr"):
        print("wrote %s" % os.path.relpath(build(lang), ROOT))
