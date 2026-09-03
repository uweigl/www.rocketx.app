# -*- coding: utf-8 -*-
"""The landing page behind the QR code on the mailed letter (/1page).

The letter's QR used to point straight at rocketx-one-page-en.pdf. A 133 KB
PDF opening in a phone viewer is a dead end: no tap targets, no next step, and
unreadable at letter size on a handset. This is the same content as a page.

IT IS NOT A COPY. Every word is read from gen_deck.C["en"] - the same source
gen_onepager.py builds the PDF from - so the page and the PDF cannot drift.
Change the deck copy and both change on the next build. check_site.py asserts
the two agree, so forgetting to rebuild fails the gate rather than shipping a
stale page.
"""
import io, os, re, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SP)
os.chdir(ROOT)
import gen_deck

esc = gen_deck.esc
ROCKET = io.open(os.path.join(ROOT, "assets", "rocket_path.txt")).read().strip()
FONTS = io.open(os.path.join(SP, "fonts_css.txt"), encoding="utf-8").read().strip()
ONEPAGER = "/assets/rocketx-one-page-en.pdf"
BIZCASE  = "/assets/rocketx-business-case-en.pdf"


def pdf_pages(path):
    """Page count read from the PDF itself - never typed by hand.

    The site once advertised "8 pages" for months after the deck grew to 14;
    check_site.py exists partly because of that. Deriving it here means the
    label cannot outlive the file it describes."""
    return len(re.findall(rb"/Type\s*/Page[^s]",
                          io.open(os.path.join(ROOT, path.lstrip("/")), "rb").read()))
EMAIL = "urban@rocketx.app"          # the letter is signed by Urban, not the desk

# The US contact, taken whole from the homepage's own WACFG so it cannot drift:
# the wa.me href and the display number come from the same place the site
# footer already uses. Tapping the number opens WhatsApp rather than dialling -
# it is the channel this number is actually published on.
_idx = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_wa = re.search(r"WACFG=\{en:\{h:'([^']*)',t:'([^']*)'\}", _idx)
WA_HREF, PHONE = _wa.group(1), _wa.group(2)
# a prefilled first line: the reader has just scanned a letter, and saying so
# saves them explaining who they are
WA_LINK = WA_HREF + "?text=" + quote(
    "Hi Urban - I scanned the code in your letter.")
WA_ICON = io.open(os.path.join(SP, "wa_path.txt"), encoding="utf-8").read().strip()

CSS = """
%(fonts)s
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--panel:#0E1B33;--blue:#2563EB;--sky:#60A5FA;--ice:#EDF2FB;
      --mist:#8FA1C4;--line:rgba(96,165,250,.16)}
html{-webkit-text-size-adjust:100%%}
body{background:var(--void);color:var(--mist);font-family:'Inter',-apple-system,Helvetica,sans-serif;
     font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:640px;margin:0 auto;padding:26px 20px 40px}
header{display:flex;align-items:center;gap:10px;padding-bottom:18px;border-bottom:1px solid var(--line)}
header svg{width:30px;height:30px;flex:none}
.bn b{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:19px;color:var(--ice);
      display:block;line-height:1.1;letter-spacing:-.01em}
.bn i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.19em;
      text-transform:uppercase;color:var(--sky)}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
         text-transform:uppercase;color:var(--sky);margin-top:26px}
h1{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:29px;line-height:1.16;
   color:var(--ice);letter-spacing:-.02em;margin-top:10px;text-wrap:balance}
.who{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.11em;
     text-transform:uppercase;color:var(--mist);margin-top:12px;line-height:1.55}
.lede{font-size:17px;line-height:1.55;color:var(--ice);margin-top:18px}
.rows{margin-top:26px;display:flex;flex-direction:column;gap:0}
.r{padding:16px 0;border-top:1px solid var(--line)}
.r h2{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:600;color:var(--sky);
      margin-bottom:5px;line-height:1.3}
.r p{font-size:15px;line-height:1.58}
.acts{margin-top:30px;display:flex;flex-direction:column;gap:11px}
.btn{display:flex;align-items:center;justify-content:center;gap:9px;min-height:54px;
     border-radius:12px;text-decoration:none;font-weight:600;font-size:16.5px;
     font-family:'Space Grotesk',sans-serif}
.btn.primary{background:var(--blue);color:#fff}
.btn.ghost{border:1px solid rgba(96,165,250,.42);color:var(--ice)}
.btn svg{width:18px;height:18px;fill:currentColor}
.dl{display:flex;flex-wrap:wrap;gap:9px}
.dl.top{margin-top:16px}
.dl.bottom{margin-top:26px;padding-top:22px;border-top:1px solid var(--line)}
.dl a{display:inline-flex;align-items:center;gap:8px;flex:1 1 220px;min-height:46px;
      padding:9px 13px;border:1px solid rgba(96,165,250,.3);border-radius:10px;
      color:var(--ice);text-decoration:none;font-size:14.5px;line-height:1.25}
.dl a svg{width:15px;height:15px;fill:var(--sky);flex:none}
.dl a s{text-decoration:none;display:block;font-family:'IBM Plex Mono',monospace;
        font-size:10px;letter-spacing:.06em;color:var(--mist);margin-top:2px}
footer{margin-top:34px;padding-top:16px;border-top:1px solid var(--line);
       font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.05em;
       color:#6C7C9C;line-height:1.7}
@media(min-width:620px){h1{font-size:34px}.acts{flex-direction:row}.btn{flex:1}}
"""

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s — RocketX</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico"><style>%(css)s</style></head>
<body><div class="wrap">
<header><svg viewBox="0 0 100 100" aria-hidden="true"><path d="%(rocket)s" fill="#2563EB" fill-rule="evenodd"/></svg>
<span class="bn"><b>RocketX</b><i>Frictionless Ordering</i></span></header>
<div class="dl top">%(dl)s</div>
<div class="eyebrow">%(xsh)s</div>
<h1>%(title)s</h1>
<div class="who">%(who)s</div>
<p class="lede">%(lede)s</p>
<div class="rows">%(rows)s</div>
<div class="acts">
  <a class="btn primary" href="%(walink)s" rel="noopener"><svg viewBox="0 0 24 24"><path d="%(waicon)s"/></svg>WhatsApp %(phone)s</a>
  <a class="btn ghost" href="mailto:%(email)s"><svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4.24-8 5.01-8-5.01V6.4l8 5.01 8-5.01v1.84z"/></svg>Email me</a>
</div>
<div class="dl bottom">%(dl)s</div>
<footer>%(foot)s<br>%(legal)s</footer>
</div></body></html>
"""


def build():
    d = gen_deck.C["en"]
    rows = "".join('<div class="r"><h2>%s</h2><p>%s</p></div>' % (esc(a), esc(b))
                   for a, b in d["xs"])
    css = CSS % {"fonts": FONTS}
    arrow = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
             '<path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>')
    dl = "".join(
        '<a href="%s" download>%s<span>%s<s>PDF &middot; %d page%s</s></span></a>'
        % (href, arrow, esc(label), n, "" if n == 1 else "s")
        for href, label, n in (
            (ONEPAGER, "This page as a PDF", pdf_pages(ONEPAGER)),
            (BIZCASE, "The full business case", pdf_pages(BIZCASE)),
        ))
    return PAGE % {
        "title": esc(d["title"]), "desc": esc(d["xsa"])[:180], "css": css,
        "rocket": ROCKET, "xsh": esc(d["xsh"]), "who": esc(d["forwho"]),
        "lede": esc(d["xsa"]), "rows": rows, "dl": dl,
        "walink": esc(WA_LINK), "waicon": WA_ICON, "phone": esc(PHONE), "email": EMAIL,
        "foot": esc(d["foot"]),
        "legal": "RocketX LLC · 30725 N Bright Angel Dr, Meadview, AZ 86444 · Business ID 25040687",
    }


if __name__ == "__main__":
    out = os.path.join(ROOT, "1page")
    if not os.path.isdir(out):
        os.makedirs(out)
    p = os.path.join(out, "index.html")
    io.open(p, "w", encoding="utf-8").write(build())
    print("  wrote 1page/index.html  %d bytes" % os.path.getsize(p))
