#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build 404.html.

A 404 can be served at any depth (/fr/whatever), so every link is root-absolute
and the language is read from the first path segment. The strip is drawn once
per language rather than reflowed at runtime: speech bubbles are sized to their
own text at build time, which is the one thing SVG will not do for you.
"""
import io, os, re

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "404.html")
LANGS = ["en", "de", "es", "nl", "fr"]
NB = u" "

# ---------------------------------------------------------------- the joke
# Not translated literally - each one is written to land in its own language.
STRIP = {
 "en": [u"The order page is gone.",
        u"Since when?",
        u"Since the redesign. We're down exactly 404 orders."],
 "de": [u"Die Bestellseite ist weg.",
        u"Seit wann?",
        u"Seit dem Relaunch. Uns fehlen genau 404 Bestellungen."],
 "es": [u"La página de pedidos no está.",
        u"¿Desde cuándo?",
        u"Desde el rediseño. Nos faltan exactamente 404 pedidos."],
 "nl": [u"De bestelpagina is weg.",
        u"Sinds wanneer?",
        u"Sinds de restyling. We missen precies 404 orders."],
 "fr": [u"La page de commande a disparu.",
        u"Depuis quand" + NB + u"?",
        u"Depuis la refonte. Il nous manque exactement 404 commandes."],
}
# Who speaks in each panel: the manager, the developer, the manager again.
SPEAKER = ["boss", "dev", "boss"]

UI = {
 "en": dict(h="This page was never ordered.",
            p="The link is broken or the page has moved. Nothing has been switched off "
              "&mdash; you are simply at an address that does not exist.",
            home="Back to the home page", deck="Business case (PDF)", one="One page (PDF)",
            alt="A three-panel office cartoon. A manager tells a developer the order page is "
                "gone. The developer asks since when. The manager answers: since the redesign, "
                "we are down exactly 404 orders."),
 "de": dict(h="Diese Seite wurde nie bestellt.",
            p="Der Link ist defekt oder die Seite ist umgezogen. Abgeschaltet wurde nichts "
              "&mdash; Sie sind schlicht auf einer Adresse, die es nicht gibt.",
            home="Zur Startseite", deck="Business Case (PDF)", one="Eine Seite (PDF)",
            alt="Ein Cartoon in drei Bildern. Ein Manager sagt einem Entwickler, die "
                "Bestellseite sei weg. Der Entwickler fragt, seit wann. Der Manager antwortet: "
                "seit dem Relaunch, uns fehlen genau 404 Bestellungen."),
 "es": dict(h="Esta página nunca se pidió.",
            p="El enlace está roto o la página se ha movido. No se ha apagado nada: "
              "simplemente estás en una dirección que no existe.",
            home="Volver al inicio", deck="Caso de negocio (PDF)", one="Una página (PDF)",
            alt="Una viñeta de oficina en tres partes. Un jefe le dice a un desarrollador que "
                "la página de pedidos no está. El desarrollador pregunta desde cuándo. El jefe "
                "responde: desde el rediseño, nos faltan exactamente 404 pedidos."),
 "nl": dict(h="Deze pagina is nooit besteld.",
            p="De link is stuk of de pagina is verhuisd. Er is niets uitgezet &mdash; je bent "
              "gewoon op een adres dat niet bestaat.",
            home="Terug naar de homepage", deck="Business case (pdf)", one="E&eacute;n pagina (pdf)",
            alt="Een kantoorcartoon in drie panelen. Een manager vertelt een ontwikkelaar dat de "
                "bestelpagina weg is. De ontwikkelaar vraagt sinds wanneer. De manager antwoordt: "
                "sinds de restyling, we missen precies 404 orders."),
 "fr": dict(h="Cette page n&rsquo;a jamais &eacute;t&eacute; command&eacute;e.",
            p="Le lien est cass&eacute; ou la page a &eacute;t&eacute; d&eacute;plac&eacute;e. "
              "Rien n&rsquo;a &eacute;t&eacute; d&eacute;branch&eacute;" + NB + ": vous &ecirc;tes "
              "simplement &agrave; une adresse qui n&rsquo;existe pas.",
            home="Retour &agrave; l&rsquo;accueil", deck="Argumentaire (PDF)", one="Une page (PDF)",
            alt="Un dessin de bureau en trois cases. Un manager annonce &agrave; une "
                "d&eacute;veloppeuse que la page de commande a disparu. Elle demande depuis quand. "
                "Le manager r&eacute;pond&nbsp;: depuis la refonte, il nous manque exactement 404 "
                "commandes."),
}

# ---------------------------------------------------------------- text fitting
# Inter at 15px: measured average advance is close to 0.515em for this copy.
def wrap(text, max_px, size=15.0, per_em=0.515):
    budget = int(max_px / (size * per_em))
    words, lines, cur = text.split(" "), [], ""
    for w in words:
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
PW, PH, GAP = 300, 250, 24          # panel box
FLOOR = 216
DESK_Y = 168                        # desk surface: the figure behind it reads as seated

def bubble(x, y, w, lines, tail_x, size=15.0):
    """Rounded speech bubble with a tail pointing down at whoever is talking."""
    lh = 19.0
    h = 16 + lh * len(lines)
    out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="11" fill="#fff" '
           'stroke="%s" stroke-width="2.2"/>' % (x, y, w, h, INK)]
    tx, ty = tail_x, y + h
    out.append('<path d="M%.1f %.1f l11 0 l-6 14 z" fill="#fff"/>' % (tx, ty - 1))
    out.append('<path d="M%.1f %.1f l-6 14 l11 -14" fill="none" stroke="%s" '
               'stroke-width="2.2" stroke-linejoin="round"/>' % (tx, ty - 1, INK))
    out.append('<rect x="%.1f" y="%.1f" width="12" height="3" fill="#fff"/>' % (tx - .5, ty - 2.5))
    for i, ln in enumerate(lines):
        out.append('<text x="%.1f" y="%.1f" font-family="Inter,Helvetica,Arial,sans-serif" '
                   'font-size="%.1f" fill="%s">%s</text>'
                   % (x + 14, y + 22 + i * lh, size, INK, esc(ln)))
    return "".join(out), h


def head(cx, cy, r, glasses):
    s = ['<circle cx="%d" cy="%d" r="%d" fill="#fff" stroke="%s" stroke-width="2.6"/>'
         % (cx, cy, r, INK)]
    if glasses:
        s.append('<circle cx="%d" cy="%d" r="5.4" fill="#fff" stroke="%s" stroke-width="2"/>'
                 % (cx - 6, cy - 2, INK))
        s.append('<circle cx="%d" cy="%d" r="5.4" fill="#fff" stroke="%s" stroke-width="2"/>'
                 % (cx + 6, cy - 2, INK))
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2"/>'
                 % (cx - 1, cy - 2, cx + 1, cy - 2, INK))
    s.append('<circle cx="%d" cy="%d" r="1.9" fill="%s"/>' % (cx - 6, cy - 2, INK))
    s.append('<circle cx="%d" cy="%d" r="1.9" fill="%s"/>' % (cx + 6, cy - 2, INK))
    # deadpan: a short flat line, never a smile
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
             'stroke-linecap="round"/>' % (cx - 4, cy + 8, cx + 4, cy + 8, INK))
    return "".join(s)


def manager(cx, base):
    """Standing, tie, arms slightly out. Three hairs so the silhouette reads."""
    hy = base - 86                      # head centre
    s = []
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx - 9, base, cx - 9, base - 28, INK))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx + 9, base, cx + 9, base - 28, INK))
    s.append('<path d="M%d %d q0 -36 %d -36 q%d 0 %d 36 z" fill="#fff" stroke="%s" '
             'stroke-width="2.6" stroke-linejoin="round"/>'
             % (cx - 21, base - 26, 21, 21, 21, INK))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx - 20, base - 54, cx - 35, base - 32, INK))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx + 20, base - 54, cx + 35, base - 38, INK))
    s.append('<path d="M%d %d l5 13 l-5 10 l-5 -10 z" fill="%s"/>' % (cx, base - 62, INK))
    s.append(head(cx, hy, 17, False))
    for dx, dy in ((-8, -13), (0, -16), (8, -13)):
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.2" '
                 'stroke-linecap="round"/>'
                 % (cx + dx, hy - 15, cx + dx + dx // 2, hy - 15 + dy, INK))
    return "".join(s)


def developer(cx, sit_y):
    """Seated: the torso stops at the desk edge, which the desk then covers."""
    hy = sit_y - 52
    s = ['<path d="M%d %d q0 -30 %d -30 q%d 0 %d 30 z" fill="#fff" stroke="%s" '
         'stroke-width="2.6" stroke-linejoin="round"/>'
         % (cx - 20, sit_y + 4, 20, 20, 20, INK)]
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx - 19, sit_y - 20, cx - 31, sit_y + 2, INK))
    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.6" '
             'stroke-linecap="round"/>' % (cx + 19, sit_y - 20, cx + 31, sit_y + 2, INK))
    s.append(head(cx, hy, 16, True))
    for dx in (-9, -3, 3, 9):           # a tidy fringe
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2" '
                 'stroke-linecap="round"/>' % (cx + dx, hy - 14, cx + dx, hy - 20, INK))
    return "".join(s)


def partition():
    """Cubicle wall behind, plus the floor line. Faint, so figures stay dominant."""
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
            % (x1, DESK_Y, x2 - x1, PAPER, INK,
               x1 + 8, DESK_Y + 9, x1 + 8, FLOOR, INK,
               x2 - 8, DESK_Y + 9, x2 - 8, FLOOR, INK))


def monitor(x, label):
    """Sits on the desk surface, screen facing the reader."""
    top = DESK_Y - 46
    s = ['<rect x="%d" y="%d" width="58" height="40" rx="4" fill="#fff" stroke="%s" '
         'stroke-width="2.4"/>' % (x, top, INK),
         '<rect x="%d" y="%d" width="20" height="5" rx="1" fill="%s"/>'
         % (x + 19, DESK_Y - 5, INK),
         '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>'
         % (x + 29, top + 40, x + 29, DESK_Y - 5, INK)]
    if label:
        s.append('<text x="%d" y="%d" text-anchor="middle" font-family="IBM Plex Mono,monospace" '
                 'font-size="16" font-weight="500" fill="%s">%s</text>'
                 % (x + 29, top + 25, INK, label))
    return "".join(s)


def panel(i, lines):
    """One framed panel: wall, figures, then the desk in front of them."""
    s = ['<rect x="1.4" y="1.4" width="%.1f" height="%.1f" rx="7" fill="%s" stroke="%s" '
         'stroke-width="2.8"/>' % (PW - 2.8, PH - 2.8, PAPER, INK),
         '<g clip-path="url(#clipP)">', partition()]
    if i == 1:
        s.append(developer(146, DESK_Y))
        s.append(desk(112, 268))
        s.append(monitor(196, "404"))
        tail = 140
    else:
        s.append(developer(206, DESK_Y))
        s.append(desk(172, 296))
        s.append(monitor(234, "404" if i == 0 else "0"))
        s.append(manager(74, FLOOR))
        tail = 68
    s.append("</g>")
    body, _h = bubble(16, 14, PW - 32, lines, tail)
    s.append(body)
    return "".join(s)


def strip_svg(lang):
    total_w = PW * 3 + GAP * 2
    out = ['<svg class="strip" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
           'role="img" aria-label="%s">' % (total_w, PH, UI[lang]["alt"]),
           '<defs><clipPath id="clipP"><rect x="3" y="3" width="%d" height="%d" rx="6"/>'
           '</clipPath></defs>' % (PW - 6, PH - 6)]
    for i in range(3):
        lines = wrap(STRIP[lang][i], PW - 32 - 28)
        out.append('<g transform="translate(%d 0)">%s</g>' % (i * (PW + GAP), panel(i, lines)))
    out.append("</svg>")
    return "".join(out)


# ---------------------------------------------------------------- page
CSS = u"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--navy:#0B1526;--panel:#0E1B33;--ice:#EDF2FB;--mist:#8FA1C4;
      --sky:#60A5FA;--blue:#2563EB;--line:#1E2E4C}
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
.strip{display:block;width:100%;height:auto;margin:34px 0 8px;
       border-radius:10px;filter:drop-shadow(0 18px 34px rgba(0,0,0,.5))}
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
@media(max-width:720px){
  .strip{margin-top:26px}
  main{padding-bottom:40px}
}
"""

DLICON = ('<svg aria-hidden="true" viewBox="0 0 24 24">'
          '<path d="M12 16l-5-5 1.4-1.4L11 12.2V4h2v8.2l2.6-2.6L17 11z"/>'
          '<path d="M5 18h14v2H5z"/></svg>')


def build():
    blocks = []
    for l in LANGS:
        u = UI[l]
        blocks.append(
            u'<div class="l l-%s" hidden>'
            u'<div class="code">ERROR 404</div>'
            u'<h1>%s</h1>'
            u'<p class="lede">%s</p>'
            u'%s'
            u'<div class="btns">'
            u'<a class="cta" href="/%s">%s</a>'
            u'<a class="dl" href="/assets/rocketx-business-case-%s.pdf" download>%s<span>%s</span></a>'
            u'<span class="sep" aria-hidden="true">&middot;</span>'
            u'<a class="dl" href="/assets/rocketx-one-page-%s.pdf" download>%s<span>%s</span></a>'
            u'</div></div>'
            % (l, u["h"], u["p"], strip_svg(l),
               "" if l == "en" else l + "/", u["home"],
               l, DLICON, u["deck"], l, DLICON, u["one"]))

    html = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>404 &mdash; RocketX</title>
<meta name="robots" content="noindex,follow"/>
<link rel="icon" href="/favicon.ico"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&amp;family=Inter:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap"/>
<style>%s</style>
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">
<img src="/assets/logo.png" alt="" width="500" height="500"/><b>RocketX</b></a></div></header>
<main><div class="wrap">
%s
</div></main>
<footer><div class="wrap">RocketX &middot; Frictionless Ordering &middot; rocketx.app</div></footer>
<script>
(function(){
  var supported=%s;
  var seg=location.pathname.split('/').filter(Boolean)[0];
  var l=supported.indexOf(seg)>-1?seg:null;
  if(!l){
    var nav=(navigator.languages||[navigator.language||'en']);
    for(var i=0;i<nav.length&&!l;i++){
      var c=String(nav[i]).slice(0,2).toLowerCase();
      if(supported.indexOf(c)>-1)l=c;
    }
  }
  l=l||'en';
  document.documentElement.lang=l;
  var el=document.querySelector('.l-'+l)||document.querySelector('.l-en');
  el.hidden=false;
})();
</script>
</body>
</html>
""" % (CSS.strip(), "\n".join(blocks),
       "[" + ",".join('"%s"' % l for l in LANGS) + "]")
    io.open(OUT, "w", encoding="utf-8").write(html)
    return html


if __name__ == "__main__":
    h = build()
    print("wrote 404.html (%.1f KB, %d languages)" % (len(h.encode("utf-8")) / 1024.0, len(LANGS)))
