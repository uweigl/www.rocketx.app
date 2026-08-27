#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the twelve-month calendar, one comic strip per month.

The strips, the figures and the line wrapping all come from gen_404, so a joke
fixed in one place is fixed in both and the calendar cannot drift from the page
it is downloaded from.

Month and weekday names are hardcoded rather than taken from the C locale,
which is not reliably installed and would silently fall back to English. The
week starts on Sunday for the US edition and on Monday everywhere else.
"""
import calendar as pycal
import io, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_404 as g4
import gen_deck


def tagline(lang):
    """The middle of the PDF footer chosen for every document:
    'RocketX - Frictionless Ordering - rocketx.app'. Deriving it here means
    the calendar cannot drift from the deck and one-pager again."""
    parts = [p.strip() for p in gen_deck.C[lang]["foot"].split(u"\u00b7")]
    assert len(parts) == 3 and parts[0] == "RocketX", parts
    return parts[1]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "deck")
YEAR = g4.CAL_YEAR                # defined in gen_404 so the link label matches
LANGS = g4.LANGS

MONTHS = {
 "en": ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"],
 "de": ["Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"],
 "es": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
 "nl": ["Januari", "Februari", "Maart", "April", "Mei", "Juni",
        "Juli", "Augustus", "September", "Oktober", "November", "December"],
 "fr": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
}
# in display order, matching FIRSTDAY below
WEEKDAYS = {
 "en": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
 "de": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
 "es": ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"],
 "nl": ["ma", "di", "wo", "do", "vr", "za", "zo"],
 "fr": ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"],
}
FIRSTDAY = {"en": 6, "de": 0, "es": 0, "nl": 0, "fr": 0}   # 6 = Sunday, 0 = Monday

COVER = {
 "en": dict(t="Twelve months of<br/>B2B ordering",
            s="One page a month, and a small piece of the truth about how wholesale "
              "orders actually get placed. Every scene in here is a real complaint, "
              "lightly rearranged."),
 "de": dict(t="Zwölf Monate<br/>B2B-Bestellen",
            s="Ein Blatt pro Monat und jeweils ein kleines Stück Wahrheit darüber, wie "
              "Großhandelsbestellungen wirklich zustande kommen. Jede Szene hier ist eine "
              "echte Beschwerde, nur leicht umgestellt."),
 "es": dict(t="Doce meses de<br/>pedidos B2B",
            s="Una hoja al mes y un pequeño trozo de verdad sobre cómo se hacen realmente "
              "los pedidos mayoristas. Cada escena es una queja real, apenas reordenada."),
 "nl": dict(t="Twaalf maanden<br/>B2B-bestellen",
            s="Eén blad per maand en steeds een klein stuk waarheid over hoe "
              "groothandelsorders echt tot stand komen. Elke scène is een echte klacht, "
              "licht herschikt."),
 "fr": dict(t="Douze mois de<br/>commande B2B",
            s="Une page par mois, et à chaque fois un petit morceau de vérité sur la façon "
              "dont les commandes de gros se passent réellement. Chaque scène est une "
              "plainte authentique, à peine réarrangée."),
}

CSS = u"""
@page{size:A4;margin:14mm 14mm 12mm}
*{margin:0;padding:0;box-sizing:border-box}
:root{--ink:#0B1526;--body:#3B4A63;--soft:#6B7C99;--line:#DDE4F0;--tint:#F4F7FC;
      --blue:#1D4ED8;--sky:#2563EB;--paper:#F7F2E6}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:Inter,Helvetica,Arial,sans-serif;color:var(--body);font-size:10pt;
     line-height:1.5;-webkit-font-smoothing:antialiased}
.page{page-break-after:always;position:relative;min-height:262mm;display:flex;
      flex-direction:column}
.page:last-child{page-break-after:auto}

/* cover */
.cover{background:var(--ink);margin:-14mm -14mm -12mm;padding:34mm 24mm 20mm;
       min-height:271mm;color:#EDF2FB;justify-content:space-between}
.cover .mark{display:flex;align-items:center;gap:11px}
.cover .mark img{width:34px;height:34px;border-radius:9px;display:block}
.cover .mark b{font-family:"Space Grotesk",Inter,sans-serif;font-size:19pt;
               letter-spacing:-.5px}
.cover h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:40pt;line-height:1.06;
          letter-spacing:-1.6px;font-weight:600;margin-top:16mm}
.cover .yr{font-family:"IBM Plex Mono",monospace;font-size:13pt;letter-spacing:6px;
           color:#60A5FA;margin-bottom:7mm}
.cover p{color:#8FA1C4;font-size:11pt;max-width:104mm;margin-top:9mm}
.cover .foot{display:flex;justify-content:space-between;align-items:baseline;
             border-top:1px solid #1E2E4C;padding-top:6mm;color:#8FA1C4;font-size:9pt}

/* month */
.mhead{display:flex;justify-content:space-between;align-items:baseline;
       border-bottom:2px solid var(--ink);padding-bottom:4mm}
.mhead h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:27pt;color:var(--ink);
          letter-spacing:-1px;font-weight:600;line-height:1}
.mhead .yr{font-family:"IBM Plex Mono",monospace;font-size:12pt;color:var(--soft);
           letter-spacing:4px}
.strip{display:block;width:100%;height:auto;margin:7mm 0 8mm}
.strip text{font-family:Inter,Helvetica,Arial,sans-serif}
.strip .scr{font-family:"IBM Plex Mono",monospace;font-weight:500}
.grid{flex:1;display:grid;grid-template-columns:repeat(7,1fr);
      grid-template-rows:auto;grid-auto-rows:1fr;border-top:1px solid var(--line);
      border-left:1px solid var(--line)}
.grid div{border-right:1px solid var(--line);border-bottom:1px solid var(--line);
          padding:2.5mm 3mm;font-size:12pt;color:var(--ink);font-weight:500}
.grid .wd{background:var(--tint);color:var(--soft);font-size:8.5pt;font-weight:600;
          letter-spacing:1.2px;text-transform:uppercase;text-align:center;padding:2mm 0}
.grid .off{background:#FCFDFE}
.grid .we{color:var(--soft)}
.mfoot{border-top:1px solid var(--line);margin-top:6mm;padding-top:4mm;
       display:flex;justify-content:space-between;color:var(--soft);font-size:8.5pt}
.mfoot b{color:var(--ink);font-weight:600}
"""


def defs_block():
    """Figures defined once per document; every month places them with <use>."""
    return (u'<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
            u'<defs><clipPath id="clipP"><rect x="3" y="3" width="%d" height="%d" rx="6"/>'
            u'</clipPath>'
            u'<g id="mgr">%s</g><g id="dev">%s</g><g id="part">%s</g>'
            u'<g id="deskA">%s</g><g id="deskB">%s</g><g id="mon">%s</g>'
            u'</defs></svg>'
            % (g4.PW - 6, g4.PH - 6, g4.manager(), g4.developer(), g4.partition(),
               g4.desk(172, 296), g4.desk(112, 268), g4.monitor_art()))


def strip_svg(idx, lang):
    """One strip with its dialogue baked in - print has no script to run."""
    st = g4.STRIPS[idx]
    total_w = g4.PW * 3 + g4.GAP * 2
    said = " ".join(" ".join(st["text"][lang][i] for i in range(3)).split())
    o = [u'<svg class="strip" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" '
         u'role="img" aria-label="%s %s">'
         % (total_w, g4.PH, g4.UI[lang]["altp"], g4.esc(said))]
    for i, (dev_cx, deskid, mon_x, has_mgr) in enumerate(g4.LAYOUT):
        o.append(u'<g transform="translate(%d 0)">' % (i * (g4.PW + g4.GAP)))
        o.append(u'<rect x="1.4" y="1.4" width="%.1f" height="%.1f" rx="7" fill="%s" '
                 u'stroke="%s" stroke-width="2.8"/>'
                 % (g4.PW - 2.8, g4.PH - 2.8, g4.PAPER, g4.INK))
        o.append(u'<g clip-path="url(#clipP)">')
        o.append(u'<use href="#part"/>')
        o.append(u'<use href="#dev" x="%d" y="%d"/>' % (dev_cx, g4.DESK_Y))
        o.append(u'<use href="#%s"/>' % deskid)
        o.append(u'<use href="#mon" x="%d" y="%d"/>' % (mon_x, g4.DESK_Y - 46))
        lab = st["screens"][i]
        o.append(u'<text class="scr" x="%d" y="%d" text-anchor="middle" font-size="%d" '
                 u'fill="%s">%s</text>'
                 % (mon_x + 29, g4.DESK_Y - 21, 12 if len(lab) > 3 else 16,
                    g4.INK, g4.esc(lab)))
        if has_mgr:
            o.append(u'<use href="#mgr" x="74" y="%d"/>' % g4.FLOOR)
        o.append(u'</g>')
        lines = g4.wrap(st["text"][lang][i], g4.BW - 28)
        o.append(u'<g>%s</g>' % g4.static_bubble(lines, g4.TAIL[i]))
        o.append(u'</g>')
    o.append(u'</svg>')
    return "".join(o)


def month_grid(lang, month):
    cal = pycal.Calendar(firstweekday=FIRSTDAY[lang])
    weeks = cal.monthdayscalendar(YEAR, month)
    # which display columns are the weekend, given where the week starts
    weekend = set()
    for col in range(7):
        wd = (FIRSTDAY[lang] + col) % 7        # 0 = Monday .. 6 = Sunday
        if wd >= 5:
            weekend.add(col)
    cells = [u'<div class="wd">%s</div>' % w for w in WEEKDAYS[lang]]
    for wk in weeks:
        for col, day in enumerate(wk):
            if day == 0:
                cells.append(u'<div class="off"></div>')
            else:
                cls = " we" if col in weekend else ""
                cells.append(u'<div class="%s">%d</div>' % (cls.strip(), day))
    return u'<div class="grid">%s</div>' % "".join(cells)


def build(lang):
    c = COVER[lang]
    pages = [
      u'<section class="page cover">'
      u'<div><div class="mark"><img src="../assets/logo.png" alt=""/><b>RocketX</b></div>'
      u'<h1>%s</h1></div>'
      u'<div><div class="yr">%d</div>'
      u'<p>%s</p></div>'
      u'<div class="foot"><span>%s</span><span>rocketx.app</span></div>'
      u'</section>' % (c["t"], YEAR, c["s"], tagline(lang))
    ]
    for m in range(1, 13):
        pages.append(
          u'<section class="page">'
          u'<div class="mhead"><h2>%s</h2><div class="yr">%d</div></div>'
          u'%s%s'
          u'<div class="mfoot"><span><b>RocketX</b> &middot; %s</span>'
          u'<span>rocketx.app</span></div>'
          u'</section>'
          % (MONTHS[lang][m - 1], YEAR, strip_svg(m - 1, lang),
             month_grid(lang, m), tagline(lang)))

    html = u"""<!doctype html>
<html lang="%s">
<head>
<meta charset="utf-8"/>
<title>RocketX %d</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&amp;family=Inter:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap"/>
<style>%s</style>
</head>
<body>
%s
%s
</body>
</html>
""" % (lang, YEAR, CSS.strip(), defs_block(), "\n".join(pages))
    p = os.path.join(OUTDIR, "rocketx-calendar-%s.html" % lang)
    io.open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    if len(g4.STRIPS) < 12:
        sys.exit("need 12 strips for 12 months, have %d" % len(g4.STRIPS))
    for l in LANGS:
        print("wrote %s" % os.path.basename(build(l)))
