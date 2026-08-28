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
  label=u"Security"),
 "de": dict(
  title=u"Sicherheit & Vertrauen — RocketX",
  h1=u"Sicherheit & Vertrauen",
  intro=u"Kurze Antworten auf die Fragen, die eine Sicherheitsprüfung zuerst stellt — mit denselben Zusagen in beiden Rechtsräumen.",
  web_h=u"Diese Website",
  web=u"Sie übt dieselbe Zurückhaltung: keine Tracker, keine Cookies, Schriften von dieser Domain. Details in der <a href='/de/datenschutz/'>Datenschutzerklärung</a>.",
  ask_h=u"Direkt fragen",
  ask=u"Sicherheitsfragebögen und Audit-Fragen: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Wir beantworten sie selbst.",
  label=u"Sicherheit"),
 "es": dict(
  title=u"Seguridad y confianza — RocketX",
  h1=u"Seguridad y confianza",
  intro=u"Respuestas breves a lo primero que pregunta una revisión de seguridad — con los mismos compromisos en ambas jurisdicciones.",
  web_h=u"Este sitio",
  web=u"Practica la misma contención: sin rastreadores, sin cookies, fuentes servidas desde este dominio. Detalles en el <a href='/es/privacidad/'>aviso de privacidad</a>.",
  ask_h=u"Pregunta directamente",
  ask=u"Cuestionarios de seguridad y preguntas de auditoría: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Los respondemos nosotros.",
  label=u"Seguridad"),
 "nl": dict(
  title=u"Beveiliging & vertrouwen — RocketX",
  h1=u"Beveiliging & vertrouwen",
  intro=u"Korte antwoorden op wat een securityreview het eerst vraagt — met dezelfde toezeggingen in beide rechtsgebieden.",
  web_h=u"Deze site",
  web=u"Hij betracht dezelfde terughoudendheid: geen trackers, geen cookies, lettertypen vanaf dit domein. Details in de <a href='/nl/privacy/'>privacyverklaring</a>.",
  ask_h=u"Vraag het direct",
  ask=u"Securityvragenlijsten en auditvragen: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. We beantwoorden ze zelf.",
  label=u"Beveiliging"),
 "fr": dict(
  title=u"Sécurité et confiance — RocketX",
  h1=u"Sécurité et confiance",
  intro=u"Des réponses brèves aux premières questions d" + AP + u"une revue de sécurité — avec les mêmes engagements dans les deux juridictions.",
  web_h=u"Ce site",
  web=u"Il pratique la même retenue" + NB + u": pas de traceurs, pas de cookies, des polices servies depuis ce domaine. Les détails sont dans la <a href='/fr/confidentialite/'>politique de confidentialité</a>.",
  ask_h=u"Demandez directement",
  ask=u"Questionnaires de sécurité et questions d" + AP + u"audit" + NB + u": <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Nous y répondons nous-mêmes.",
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
        if eu_i is not None:
            parts.append(u'<p><span class="jur">EU</span> %s</p>' % C["eu"][eu_i][1])
        if us_i is not None:
            parts.append(u'<p><span class="jur">US</span> %s</p>' % C["us"][us_i][1])
        if eu_i is not None and us_i is None:
            parts = [u"<p>%s</p>" % C["eu"][eu_i][1]]
        if eu_i is None:
            parts = [u"<p>%s</p>" % C["us"][us_i][1]]
        secs.append(u"<h2>%s</h2>\n%s" % (head, u"\n".join(parts)))
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
