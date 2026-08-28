#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the privacy pages, one per language, at each market's natural path.

The page says only what is true of this site today: no cookies, no analytics,
no tracking, fonts served from this domain, one localStorage key for the
language, server logs at the host, and the contact form delivered through
MailerSend. If the site ever gains a tracker, this page is the checklist of
claims that must change with it.

The German Impressum is generated too (representative: Urban Weigl; email
plus the contact form supply the two fast contact channels the ECJ requires,
so no phone number is needed). The French mentions legales remain deliberately
ungenerated: the LCEN names a phone number explicitly, and publishing them
incomplete would be worse than their absence.
"""
import io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rocketx.app"

PATHS = {"en": "privacy", "de": "de/datenschutz", "es": "es/privacidad",
         "nl": "nl/privacy", "fr": "fr/confidentialite"}

T = {
 "en": dict(
  title=u"Privacy — RocketX",
  h1=u"Privacy",
  updated=u"Last updated: 28 August 2026",
  intro=u"This site is built to know as little about you as possible. What follows is everything it does process, in full.",
  s=[
   (u"Who is responsible",
    u"RocketX LLC, 30725 N Bright Angel Dr., Meadview, AZ 86444, United States. For anything in this notice: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
   (u"What this site does not do",
    u"No analytics, no advertising, no tracking pixels, no fingerprinting, and no cookies. Fonts are served from this domain — opening this site sends no request to Google or any other third party."),
   (u"What your browser stores",
    u"One value in your browser's localStorage: your language choice (<code>rx-lang</code>), so the site opens in your language next time. It never leaves your device and you can clear it in your browser at any time."),
   (u"Server logs",
    u"This site is delivered by Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, USA), which processes technical connection data (IP address, request, timestamp) to serve and protect the site. Legal basis, where the GDPR applies: legitimate interest in operating the site securely, Art. 6(1)(f)."),
   (u"The contact form",
    u"If you send the quote or demo form, we process what you enter — name, email, company, message — solely to answer you. Delivery runs through MailerSend Inc. as our email processor. Legal basis: taking steps prior to a contract at your request, Art. 6(1)(b). We keep the correspondence as long as the conversation is live, then as required by commercial record-keeping law."),
   (u"Your rights",
    u"Where the GDPR applies, you can ask us for access, rectification, erasure, restriction, portability, and you can object to processing based on legitimate interest. Write to <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. You can also complain to your local supervisory authority."),
  ]),
 "de": dict(
  title=u"Datenschutzerklärung — RocketX",
  h1=u"Datenschutzerklärung",
  updated=u"Stand: 28. August 2026",
  intro=u"Diese Website ist so gebaut, dass sie so wenig wie möglich über Sie erfährt. Es folgt vollständig, was sie verarbeitet.",
  s=[
   (u"Verantwortlicher",
    u"RocketX LLC, 30725 N Bright Angel Dr., Meadview, AZ 86444, USA. Für alle Anliegen zu dieser Erklärung: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
   (u"Was diese Website nicht tut",
    u"Keine Analyse-Tools, keine Werbung, keine Tracking-Pixel, kein Fingerprinting, keine Cookies. Schriften werden von dieser Domain ausgeliefert — beim Aufruf geht keine Anfrage an Google oder andere Dritte."),
   (u"Was Ihr Browser speichert",
    u"Ein Wert im localStorage Ihres Browsers: Ihre Sprachwahl (<code>rx-lang</code>), damit die Seite beim nächsten Besuch in Ihrer Sprache öffnet. Der Wert verlässt Ihr Gerät nicht und lässt sich jederzeit im Browser löschen."),
   (u"Server-Logs",
    u"Ausgeliefert wird die Website von Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, USA); dabei werden technische Verbindungsdaten (IP-Adresse, Anfrage, Zeitstempel) zum Betrieb und Schutz der Seite verarbeitet. Rechtsgrundlage: berechtigtes Interesse am sicheren Betrieb, Art. 6 Abs. 1 lit. f DSGVO."),
   (u"Das Kontaktformular",
    u"Wenn Sie das Angebots- oder Demo-Formular senden, verarbeiten wir Ihre Angaben — Name, E-Mail, Unternehmen, Nachricht — ausschließlich zur Beantwortung. Der Versand läuft über MailerSend Inc. als E-Mail-Auftragsverarbeiter. Rechtsgrundlage: vorvertragliche Maßnahmen auf Ihre Anfrage, Art. 6 Abs. 1 lit. b DSGVO. Die Korrespondenz speichern wir für die Dauer des Vorgangs, danach nach handelsrechtlichen Aufbewahrungspflichten."),
   (u"Ihre Rechte",
    u"Sie haben die Rechte auf Auskunft, Berichtigung, Löschung, Einschränkung und Datenübertragbarkeit sowie ein Widerspruchsrecht gegen Verarbeitung auf Basis berechtigten Interesses. Schreiben Sie an <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Daneben besteht ein Beschwerderecht bei einer Datenschutz-Aufsichtsbehörde."),
  ]),
 "es": dict(
  title=u"Privacidad — RocketX",
  h1=u"Privacidad",
  updated=u"Última actualización: 28 de agosto de 2026",
  intro=u"Este sitio está hecho para saber lo menos posible de ti. Lo que sigue es todo lo que procesa, sin omisiones.",
  s=[
   (u"Responsable",
    u"RocketX LLC, 30725 N Bright Angel Dr., Meadview, AZ 86444, Estados Unidos. Para cualquier tema de este aviso: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
   (u"Lo que este sitio no hace",
    u"Sin analítica, sin publicidad, sin píxeles de seguimiento, sin fingerprinting y sin cookies. Las fuentes se sirven desde este dominio: abrir el sitio no envía ninguna petición a Google ni a otros terceros."),
   (u"Lo que guarda tu navegador",
    u"Un único valor en localStorage: tu idioma (<code>rx-lang</code>), para que el sitio abra en tu idioma la próxima vez. No sale de tu dispositivo y puedes borrarlo cuando quieras."),
   (u"Registros del servidor",
    u"El sitio lo entrega Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, EE. UU.), que procesa datos técnicos de conexión (IP, petición, fecha y hora) para servir y proteger el sitio."),
   (u"El formulario de contacto",
    u"Si envías el formulario de cotización o demo, procesamos lo que escribes — nombre, email, empresa, mensaje — solo para responderte. El envío pasa por MailerSend Inc. como procesador de correo. Conservamos la correspondencia mientras la conversación siga viva y después según las obligaciones mercantiles."),
   (u"Tus derechos",
    u"Puedes pedir acceso, rectificación, supresión, limitación y portabilidad, y oponerte al tratamiento basado en interés legítimo, escribiendo a <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
  ]),
 "nl": dict(
  title=u"Privacy — RocketX",
  h1=u"Privacy",
  updated=u"Laatst bijgewerkt: 28 augustus 2026",
  intro=u"Deze site is zo gebouwd dat hij zo min mogelijk over je weet. Hieronder staat alles wat hij verwerkt, volledig.",
  s=[
   (u"Verantwoordelijke",
    u"RocketX LLC, 30725 N Bright Angel Dr., Meadview, AZ 86444, Verenigde Staten. Voor alles rond deze verklaring: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
   (u"Wat deze site niet doet",
    u"Geen analytics, geen advertenties, geen trackingpixels, geen fingerprinting en geen cookies. Lettertypen worden vanaf dit domein geleverd — het openen van de site stuurt geen verzoek naar Google of andere derden."),
   (u"Wat je browser opslaat",
    u"Eén waarde in localStorage: je taalkeuze (<code>rx-lang</code>), zodat de site de volgende keer in jouw taal opent. Die verlaat je apparaat niet en je kunt hem altijd wissen."),
   (u"Serverlogs",
    u"De site wordt geleverd door Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, VS), dat technische verbindingsgegevens (IP-adres, verzoek, tijdstip) verwerkt om de site te leveren en te beschermen. Grondslag: gerechtvaardigd belang bij veilige exploitatie, art. 6 lid 1 sub f AVG."),
   (u"Het contactformulier",
    u"Stuur je het offerte- of demoformulier, dan verwerken we wat je invult — naam, e-mail, bedrijf, bericht — uitsluitend om te antwoorden. De bezorging loopt via MailerSend Inc. als e-mailverwerker. Grondslag: precontractuele maatregelen op jouw verzoek, art. 6 lid 1 sub b AVG. We bewaren de correspondentie zolang het gesprek loopt, daarna volgens de wettelijke bewaarplichten."),
   (u"Je rechten",
    u"Je hebt recht op inzage, rectificatie, wissing, beperking en overdraagbaarheid, en je kunt bezwaar maken tegen verwerking op basis van gerechtvaardigd belang: <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Klagen kan bij de Autoriteit Persoonsgegevens."),
  ]),
 "fr": dict(
  title=u"Confidentialité — RocketX",
  h1=u"Confidentialité",
  updated=u"Dernière mise à jour : 28 août 2026",
  intro=u"Ce site est conçu pour en savoir le moins possible sur vous. Voici, sans omission, tout ce qu’il traite.",
  s=[
   (u"Responsable du traitement",
    u"RocketX LLC, 30725 N Bright Angel Dr., Meadview, AZ 86444, États-Unis. Pour toute question sur cette notice : <a href='mailto:app@rocketx.app'>app@rocketx.app</a>."),
   (u"Ce que ce site ne fait pas",
    u"Pas d’outil d’analyse, pas de publicité, pas de pixel de suivi, pas d’empreinte numérique, pas de cookies. Les polices sont servies depuis ce domaine : ouvrir le site n’envoie aucune requête à Google ni à un autre tiers."),
   (u"Ce que votre navigateur conserve",
    u"Une seule valeur en localStorage : votre langue (<code>rx-lang</code>), pour que le site s’ouvre dans votre langue la prochaine fois. Elle ne quitte pas votre appareil et se supprime à tout moment dans le navigateur."),
   (u"Journaux du serveur",
    u"Le site est délivré par Cloudflare, Inc. (101 Townsend St, San Francisco, CA 94107, États-Unis), qui traite des données techniques de connexion (adresse IP, requête, horodatage) pour servir et protéger le site. Base légale : intérêt légitime à une exploitation sûre, art. 6, par. 1, f du RGPD."),
   (u"Le formulaire de contact",
    u"Si vous envoyez le formulaire de devis ou de démonstration, nous traitons ce que vous saisissez — nom, email, société, message — uniquement pour vous répondre. L’acheminement passe par MailerSend Inc., notre sous-traitant d’envoi d’emails. Base légale : mesures précontractuelles à votre demande, art. 6, par. 1, b du RGPD. Nous conservons la correspondance le temps de l’échange, puis selon les obligations commerciales de conservation."),
   (u"Vos droits",
    u"Vous disposez des droits d’accès, de rectification, d’effacement, de limitation et de portabilité, et d’un droit d’opposition au traitement fondé sur l’intérêt légitime : <a href='mailto:app@rocketx.app'>app@rocketx.app</a>. Vous pouvez aussi saisir la CNIL."),
  ]),
}

FONTS = io.open(os.path.join(ROOT, "scripts", "fonts_css.txt"), encoding="utf-8").read().strip()

CSS = u"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--panel:#0E1B33;--ice:#EDF2FB;--mist:#8FA1C4;--sky:#60A5FA;--line:#1E2E4C}
body{background:var(--void);color:var(--ice);line-height:1.7;
     font-family:Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif}
a{color:var(--sky)}
.wrap{max-width:760px;margin:0 auto;padding:0 24px}
header{padding:24px 0;border-bottom:1px solid var(--line)}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--ice);text-decoration:none}
.brand img{width:28px;height:28px;border-radius:7px}
.brand b{font-family:"Space Grotesk",Inter,sans-serif;font-size:16px}
main{padding:46px 0 72px}
h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:clamp(26px,4vw,36px);
   letter-spacing:-.8px;font-weight:600}
.upd{color:var(--mist);font-size:13px;margin:8px 0 22px}
.intro{color:var(--mist);font-size:16px;max-width:60ch}
h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:18px;letter-spacing:-.3px;
   margin:34px 0 8px}
p{color:var(--mist);font-size:15px;max-width:68ch}
code{font-family:"IBM Plex Mono",monospace;font-size:13px;color:var(--ice)}
footer{border-top:1px solid var(--line);padding:18px 0;color:var(--mist);font-size:13px}
"""


def build(lang):
    d = T[lang]
    body = u"".join(u"<h2>%s</h2>\n<p>%s</p>\n" % (h, p) for h, p in d["s"])
    html = u"""<!doctype html>
<html lang="%s">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%s</title>
<meta name="robots" content="noindex,follow"/>
<link rel="canonical" href="%s/%s/"/>
<link rel="icon" href="/favicon.ico"/>
<style>%s
%s</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="/%s"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
</div></header>
<main><div class="wrap">
<h1>%s</h1>
<p class="upd">%s</p>
<p class="intro">%s</p>
%s
</div></main>
<footer><div class="wrap">RocketX &middot; rocketx.app</div></footer>
</body>
</html>
""" % (lang, d["title"], SITE, PATHS[lang], FONTS, CSS.strip(),
       "" if lang == "en" else lang + "/",
       d["h1"], d["updated"], d["intro"], body)
    outdir = os.path.join(ROOT, PATHS[lang])
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


IMPRESSUM = dict(
 title=u"Impressum — RocketX",
 h1=u"Impressum",
 body=u"""
<h2>Angaben gemäß §&nbsp;5 DDG</h2>
<p>RocketX LLC<br/>
Gesellschaft mit beschränkter Haftung (Limited Liability Company) nach dem
Recht des US-Bundesstaats Arizona<br/>
30725 N Bright Angel Dr.<br/>
Meadview, AZ 86444<br/>
Vereinigte Staaten von Amerika</p>
<h2>Vertretungsberechtigter</h2>
<p>Urban Weigl</p>
<h2>Kontakt</h2>
<p>Telefon: +49 15678 191538<br/>
E-Mail: <a href="mailto:app@rocketx.app">app@rocketx.app</a><br/>
Daneben erreichen Sie uns unmittelbar über das Kontaktformular auf dieser
Website.</p>
<h2>Vertragspartner für Kunden in der EU</h2>
<p>RocketX Limited<br/>
Registriert in Irland, Company No. 344153<br/>
Derrylahan, Ballyhaunis, Co. Mayo, F35 W667, Irland</p>
<h2>Verantwortlich im Sinne des §&nbsp;18 Abs.&nbsp;2 MStV</h2>
<p>Urban Weigl, Anschrift wie oben.</p>
<h2>Hinweis</h2>
<p>Dieses Angebot richtet sich ausschließlich an Unternehmen (B2B). Eine
Umsatzsteuer-Identifikationsnummer nach §&nbsp;27a UStG besteht nicht.</p>
""")


def build_impressum():
    d = IMPRESSUM
    html = u"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%s</title>
<meta name="robots" content="noindex,follow"/>
<link rel="canonical" href="%s/de/impressum/"/>
<link rel="icon" href="/favicon.ico"/>
<style>%s
%s</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="/de/"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
</div></header>
<main><div class="wrap">
<h1>%s</h1>
%s
<p><a href="/de/datenschutz/">Datenschutzerklärung</a></p>
</div></main>
<footer><div class="wrap">RocketX &middot; rocketx.app</div></footer>
</body>
</html>
""" % (d["title"], SITE, FONTS, CSS.strip(), d["h1"], d["body"])
    outdir = os.path.join(ROOT, "de", "impressum")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


MENTIONS = dict(
 title=u"Mentions légales — RocketX",
 h1=u"Mentions légales",
 body=u"""
<h2>Éditeur du site</h2>
<p>RocketX LLC<br/>
Société à responsabilité limitée (Limited Liability Company) de droit de
l’État de l’Arizona, États-Unis<br/>
30725 N Bright Angel Dr., Meadview, AZ 86444, États-Unis<br/>
Téléphone : +49 15678 191538<br/>
Email : <a href="mailto:app@rocketx.app">app@rocketx.app</a></p>
<h2>Directeur de la publication</h2>
<p>Urban Weigl</p>
<h2>Cocontractant pour les clients de l’Union européenne</h2>
<p>RocketX Limited<br/>
Société immatriculée en Irlande, Company No. 344153<br/>
Derrylahan, Ballyhaunis, Co. Mayo, F35 W667, Irlande</p>
<h2>Hébergeur</h2>
<p>Cloudflare, Inc.<br/>
101 Townsend St, San Francisco, CA 94107, États-Unis<br/>
Téléphone : +1 888 993 5273</p>
""")


def build_mentions():
    d = MENTIONS
    html = u"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%s</title>
<meta name="robots" content="noindex,follow"/>
<link rel="canonical" href="%s/fr/mentions-legales/"/>
<link rel="icon" href="/favicon.ico"/>
<style>%s
%s</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="/fr/"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
</div></header>
<main><div class="wrap">
<h1>%s</h1>
%s
<p><a href="/fr/confidentialite/">Politique de confidentialité</a></p>
</div></main>
<footer><div class="wrap">RocketX &middot; rocketx.app</div></footer>
</body>
</html>
""" % (d["title"], SITE, FONTS, CSS.strip(), d["h1"], d["body"])
    outdir = os.path.join(ROOT, "fr", "mentions-legales")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    for lang in ("en", "de", "es", "nl", "fr"):
        p = build(lang)
        print("wrote %s" % os.path.relpath(p, ROOT))
    print("wrote %s" % os.path.relpath(build_impressum(), ROOT))
    print("wrote %s" % os.path.relpath(build_mentions(), ROOT))
