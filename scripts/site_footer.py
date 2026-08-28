# -*- coding: utf-8 -*-
"""The site footer, rendered statically per language for the auxiliary pages.

The main page builds its footer with JavaScript - i18n keys, per-language
contact config, language-gated legal links. The auxiliary pages (privacy,
trust, impressum, mentions, comparisons) have no scripts, so they get the same
footer baked at build time: tagline, the market's contact channels, LinkedIn,
the calendar, and the legal cluster with a one-click path to every legal page
this language owes its readers.

One source for the variable parts: the tagline comes from the deck footer via
gen_calendar.tagline, the paths mirror the maps in index.html.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_calendar

PRIV = {"en": "privacy", "de": "de/datenschutz", "es": "es/privacidad",
        "nl": "nl/privacy", "fr": "fr/confidentialite"}
TRUST = {"en": "trust", "de": "de/sicherheit", "es": "es/seguridad",
         "nl": "nl/beveiliging", "fr": "fr/securite"}
PRIV_LBL = {"en": u"Privacy", "de": u"Datenschutz", "es": u"Privacidad",
            "nl": u"Privacy", "fr": u"Confidentialité"}
TRUST_LBL = {"en": u"Security", "de": u"Sicherheit", "es": u"Seguridad",
             "nl": u"Beveiliging", "fr": u"Sécurité"}
CAL_LBL = {"en": u"2027 calendar (PDF)", "de": u"Kalender 2027 (PDF)",
           "es": u"Calendario 2027 (PDF)", "nl": u"Kalender 2027 (pdf)",
           "fr": u"Calendrier 2027 (PDF)"}
WA = {"en": ("https://wa.me/18294997677", u"+1 (829) 499-7677"),
      "de": ("https://wa.me/4986774099628", u"08677 / 4099628")}

MAIL_SVG = ('<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 '
            '.9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4.24-8 '
            '5.01-8-5.01V6.4l8 5.01 8-5.01v1.84z"/></svg>')
WA_SVG = ('<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297'
          '-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-'
          '.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883'
          '-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-'
          '.347.446-.52.149-.174.198-.298.297-.497.1-.198.05-.371-.025-.52-.075-.149'
          '-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57'
          '-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065'
          ' 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694'
          '.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694'
          '.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87'
          ' 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86'
          ' 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988'
          ' 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8'
          '.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 '
          '2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 '
          '1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-'
          '8.413"/></svg>')
LI_SVG = ('<svg aria-hidden="true" viewBox="0 0 24 24"><path d="M20.45 20.45h-3.56v'
          '-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3'
          '.41v1.56h.05c.48-.9 1.63-1.85 3.36-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM'
          '5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.55'
          'V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 '
          '24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg>')

CSS = u"""
.sfoot{border-top:1px solid var(--line);padding:34px 0 30px;color:var(--mist);font-size:14px}
.sfoot .row{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;margin-bottom:12px}
.sfoot a{color:var(--mist);text-decoration:none;display:inline-flex;align-items:center;gap:7px}
.sfoot a:hover{color:var(--sky)}
.sfoot svg{width:15px;height:15px;fill:currentColor}
.sfoot .sep{color:var(--line);user-select:none}
.sfoot .cop{font-size:13px}
"""

SEP = u'<span class="sep" aria-hidden="true">·</span>'


def footer_html(lang, with_style=True):
    home = "/" if lang == "en" else "/%s/" % lang
    tagline = gen_calendar.tagline(lang)
    contact = [u'<a href="mailto:app@rocketx.app">%sapp@rocketx.app</a>' % MAIL_SVG]
    if lang in WA:
        href, txt = WA[lang]
        contact.append(SEP)
        contact.append(u'<a aria-label="WhatsApp" href="%s" rel="noopener" '
                       u'target="_blank">%s%s</a>' % (href, WA_SVG, txt))
    legal = [u'<a href="/%s/">%s</a>' % (PRIV[lang], PRIV_LBL[lang]), SEP,
             u'<a href="/%s/">%s</a>' % (TRUST[lang], TRUST_LBL[lang])]
    if lang == "de":
        legal += [SEP, u'<a href="/de/impressum/">Impressum</a>']
    if lang == "fr":
        legal += [SEP, u'<a href="/fr/mentions-legales/">Mentions légales</a>']
    style = (u'<style>' + CSS.strip() + u'</style>') if with_style else u''
    return style + (u'<footer class="sfoot"><div class="wrap">'
            u'<div class="row"><a href="%s"><b>RocketX</b></a>%s<span>%s</span>%s%s</div>'
            u'<div class="row">'
            u'<a href="https://www.linkedin.com/company/rocketxapp" rel="noopener" '
            u'target="_blank">%sLinkedIn</a>%s'
            u'<a download href="/assets/rocketx-calendar-%s.pdf">%s</a></div>'
            u'<div class="row cop">© 2001–2026 RocketX %s %s</div>'
            u'</div></footer>'
            % (home, SEP, tagline, SEP, u"".join(contact),
               LI_SVG, SEP, lang, CAL_LBL[lang],
               SEP, u" ".join(legal)))
