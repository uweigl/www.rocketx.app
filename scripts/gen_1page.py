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
# The letterhead mark and the signature are the LETTER's, not copies of them:
# assets/icon.svg is the same app icon printed on the letterhead, and
# scripts/signature.svg is lifted from the letter template. Someone scanning
# the QR has the letter in their hand, so the page has to look like it.
APP_ICON = io.open(os.path.join(ROOT, "assets", "icon.svg"),
                   encoding="utf-8").read().strip()
APP_ICON = re.sub(r'^<svg[^>]*>|</svg>$', '', APP_ICON).strip()
SIGNATURE = io.open(os.path.join(SP, "signature.svg"), encoding="utf-8").read().strip()
# WhatsApp is the primary tap, but US adoption among owner-operators of this
# generation is patchy, and the letter promises "call or text". This is the
# fallback for a reader who does not have the app - same digits, dialled.
TEL = "+1" + re.sub(r"\D", "", PHONE)

CSS = """
%(fonts)s
*{margin:0;padding:0;box-sizing:border-box}
/* the LETTER's palette, verbatim - white paper, the same ink and rule colour */
:root{--ink:#12182B;--body:#2B3550;--soft:#6A7896;--blue:#2563EB;--line:#DCE3F0;
      --wash:#F4F7FC;--biro:#1E3E96}
html{-webkit-text-size-adjust:100%%}
body{background:#fff;color:var(--body);font-family:'Inter',-apple-system,Helvetica,sans-serif;
     font-size:16px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:660px;margin:0 auto;padding:26px 22px 40px}
/* letterhead, as printed */
header{display:flex;align-items:center;gap:9px;padding-bottom:16px;border-bottom:1px solid var(--line)}
/* the mark is sized to the TEXT BLOCK, not to the wordmark alone. It was
   32px against a 45.8px block - added the tagline line and never resized
   the icon, so it read as a small badge beside a taller lockup. */
header svg.mark{width:42px;height:42px;flex:none;border-radius:9px}
.bn b{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:19px;color:var(--ink);
      display:block;line-height:1.05;letter-spacing:-.01em}
.bn i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:.19em;
      text-transform:uppercase;color:var(--blue)}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.2em;
         text-transform:uppercase;color:var(--blue);margin-top:26px}
h1{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:29px;line-height:1.16;
   color:var(--ink);letter-spacing:-.02em;margin-top:10px;text-wrap:balance}
.who{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.11em;
     text-transform:uppercase;color:var(--soft);margin-top:12px;line-height:1.55}
.lede{font-size:17px;line-height:1.56;color:var(--ink);margin-top:18px}
.rows{margin-top:26px}
.r{padding:16px 0;border-top:1px solid var(--line)}
.r h2{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:600;color:var(--blue);
      margin-bottom:5px;line-height:1.3}
.r p{font-size:15px;line-height:1.6}
.acts{margin-top:28px;display:flex;flex-direction:column;gap:11px}
.btn{display:flex;align-items:center;justify-content:center;gap:9px;min-height:54px;
     border-radius:12px;text-decoration:none;font-weight:600;font-size:16.5px;
     font-family:'Space Grotesk',sans-serif}
.btn.primary{background:var(--blue);color:#fff}
.btn.ghost{border:1px solid #C9D9F0;color:var(--ink);background:var(--wash)}
.btn svg{width:18px;height:18px;fill:currentColor}
.tel{display:block;text-align:center;margin-top:13px;padding:9px;color:var(--soft);
     text-decoration:none;font-size:14px}
/* the reader who is not ready to message but is ready to look. Below the
   buttons on purpose - the CTA gets first claim on the attention. */
.more{display:flex;align-items:center;justify-content:center;gap:7px;margin-top:4px;
      padding:11px;color:var(--blue);text-decoration:none;font-size:14.5px;font-weight:500}
.more svg{width:14px;height:14px;fill:currentColor}
footer a{color:var(--blue);text-decoration:none}
.dl{display:flex;flex-wrap:wrap;gap:9px}
.dl.top{margin-top:16px}
.dl.bottom{margin-top:26px;padding-top:22px;border-top:1px solid var(--line)}
.dl a{display:inline-flex;align-items:center;gap:8px;flex:1 1 220px;min-height:46px;
      padding:9px 13px;border:1px solid #C9D9F0;border-radius:10px;background:var(--wash);
      color:var(--ink);text-decoration:none;font-size:14.5px;line-height:1.25}
.dl a svg{width:15px;height:15px;fill:var(--blue);flex:none}
.dl a s{text-decoration:none;display:block;font-family:'IBM Plex Mono',monospace;
        font-size:10px;letter-spacing:.06em;color:var(--soft);margin-top:2px}
/* the sign-off, in the same biro blue as the letter */
.sign{margin-top:30px;padding-top:20px;border-top:1px solid var(--line)}
.sign p{font-size:15.5px;color:var(--body)}
.sign .ink{color:var(--biro);margin:6px 0 2px}
.sign .ink svg{display:block;width:150pt;max-width:74%%;height:auto}
.sign b{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px;color:var(--ink);display:block}
.sign i{font-style:normal;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
        letter-spacing:.17em;text-transform:uppercase;color:var(--blue);display:block;margin-top:2px}
footer{margin-top:30px;padding-top:16px;border-top:1px solid var(--line);
       font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.05em;
       color:var(--soft);line-height:1.7}
@media(min-width:620px){h1{font-size:34px}.acts{flex-direction:row}.btn{flex:1}}

/* MOTION - opt-in, never opt-out.
   Everything above is the resting state and is fully readable with no
   JavaScript and no animation at all. The script adds .anim to <html> only
   when the reader has not asked for reduced motion; every rule below is
   scoped to that class, so a failed script or a stalled connection costs a
   scanner nothing. The site's own .reveal does the opposite - starts at
   opacity:0 and waits - which leaves a blank page if the observer never
   fires. A page reached from a posted letter cannot afford that. */
.anim .rise{opacity:0;transform:translateY(14px);
            transition:opacity .55s cubic-bezier(.2,.7,.2,1),
                       transform .55s cubic-bezier(.2,.7,.2,1);
            transition-delay:calc(var(--i,0)*70ms)}
.anim .rise.in{opacity:1;transform:none}
/* the signature writes itself - the one flourish this page earns, because
   the reader is holding the letter it was signed on */
.anim .ink path{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);
                transition:stroke-dashoffset .62s cubic-bezier(.55,.1,.3,1);
                transition-delay:calc(var(--n)*150ms)}
.anim .ink.in path{stroke-dashoffset:0}
.anim .ink circle{opacity:0;transition:opacity .25s ease 1.15s}
.anim .ink.in circle{opacity:1}
.btn,.dl a{transition:transform .12s ease,box-shadow .2s ease,border-color .2s ease}
.btn:active,.dl a:active{transform:scale(.985)}
/* Every control gets the same feedback. The ghost button had none while the
   primary and the download cards both lifted - the second action on the page
   looked inert next to the first. */
.tel,.more,footer a{transition:color .18s ease}
@media(hover:hover){
  .dl a:hover{border-color:#9DBBEA;box-shadow:0 2px 10px rgba(37,99,235,.09)}
  .btn.primary:hover{box-shadow:0 4px 16px rgba(37,99,235,.28)}
  .btn.ghost:hover{border-color:#9DBBEA;background:#EBF2FC;
                   box-shadow:0 2px 10px rgba(37,99,235,.10)}
  .tel:hover{color:var(--ink)}
  .more:hover{color:#1B47B8}
  footer a:hover{text-decoration:underline}
}
.tel:active,.more:active{transform:scale(.985)}
/* an explicit focus ring: the browser default is fine but is not the page's
   blue, and on a white ground it reads as a stray artefact */
.btn:focus-visible,.dl a:focus-visible,.tel:focus-visible,
.more:focus-visible,footer a:focus-visible{
  outline:2px solid var(--blue);outline-offset:3px;border-radius:8px}
@media(prefers-reduced-motion:reduce){
  .anim .rise,.anim .ink path,.anim .ink circle{transition:none;opacity:1;
    transform:none;stroke-dashoffset:0}
}
"""

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s — RocketX</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico"><style>%(css)s</style></head>
<body><div class="wrap">
<header><svg class="mark" viewBox="0 0 64 64" aria-hidden="true">%(appicon)s</svg>
<span class="bn"><b>RocketX</b><i>Frictionless Ordering</i></span></header>
<div class="dl top">%(dl)s</div>
<div class="eyebrow rise" style="--i:0">%(xsh)s</div>
<h1 class="rise" style="--i:1">%(title)s</h1>
<div class="who rise" style="--i:2">%(who)s</div>
<p class="lede rise" style="--i:3">%(lede)s</p>
<div class="rows">%(rows)s</div>
<div class="acts rise">
  <a class="btn primary" href="%(walink)s" rel="noopener"><svg viewBox="0 0 24 24"><path d="%(waicon)s"/></svg>WhatsApp %(phone)s</a>
  <a class="btn ghost" href="mailto:%(email)s"><svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4.24-8 5.01-8-5.01V6.4l8 5.01 8-5.01v1.84z"/></svg>Email me</a>
</div>
<a class="tel" href="tel:%(tel)s">Not on WhatsApp? Call or text %(phone)s</a>
<a class="more" href="/#features">See what’s included, and how it works<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h12.2l-4.6-4.6L14 6l7 7-7 7-1.4-1.4 4.6-4.6H5z"/></svg></a>
<div class="sign rise">
<p>%(signoff)s</p>
<div class="ink"><svg viewBox="0 0 520 150" aria-label="Urban Weigl, signed">%(signature)s</svg></div>
<b>Urban Weigl</b><i>Founder, RocketX</i>
</div>
<div class="dl bottom">%(dl)s</div>
<footer>%(foot)s<br>%(legal)s</footer>
</div>
<script>
(function(){
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;   // leave it at rest
  var d = document, root = d.documentElement;
  // measure each signature stroke so it draws at its own true length
  var ink = d.querySelector(".ink");
  if (ink) {
    var paths = ink.querySelectorAll("path");
    for (var i = 0; i < paths.length; i++) {
      var L = 0;
      try { L = Math.ceil(paths[i].getTotalLength()); } catch (e) { L = 900; }
      paths[i].style.setProperty("--len", L);
      paths[i].style.setProperty("--n", i);
    }
  }
  root.className += " anim";
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    });
  }, {rootMargin: "0px 0px -8%% 0px", threshold: 0.08});
  d.querySelectorAll(".rise, .ink").forEach(function(el){ io.observe(el); });
  // anything already on screen reveals immediately rather than on first scroll
  requestAnimationFrame(function(){
    d.querySelectorAll(".rise, .ink").forEach(function(el){
      if (el.getBoundingClientRect().top < innerHeight) el.classList.add("in");
    });
  });
})();
</script>
</body></html>
"""


def build():
    d = gen_deck.C["en"]
    rows = "".join('<div class="r rise"><h2>%s</h2><p>%s</p></div>' % (esc(a), esc(b))
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
        "appicon": APP_ICON, "signature": SIGNATURE,
        "signoff": "Thank you for scanning the code in my letter. "
                   "If any of this is worth twenty minutes, the quickest way "
                   "to reach me is the button above.",
        "xsh": esc(d["xsh"]), "who": esc(d["forwho"]),
        "lede": esc(d["xsa"]), "rows": rows, "dl": dl,
        "walink": esc(WA_LINK), "waicon": WA_ICON, "phone": esc(PHONE),
        "tel": TEL, "email": EMAIL,
        # the deck's foot carries the address as plain text; make the domain
        # itself clickable rather than asking a reader to retype it
        "foot": re.sub(r"(www\.rocketx\.app)",
                       r'<a href="https://\1">\1</a>', esc(d["foot"])),
        "legal": "RocketX LLC · 30725 N Bright Angel Dr, Meadview, AZ 86444 · Business ID 25040687",
    }


if __name__ == "__main__":
    out = os.path.join(ROOT, "1page")
    if not os.path.isdir(out):
        os.makedirs(out)
    p = os.path.join(out, "index.html")
    io.open(p, "w", encoding="utf-8").write(build())
    print("  wrote 1page/index.html  %d bytes" % os.path.getsize(p))
