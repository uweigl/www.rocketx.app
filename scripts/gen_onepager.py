# -*- coding: utf-8 -*-
"""One-page summary (assets/rocketx-one-page-*.pdf), generated from the deck's own content so the two cannot
drift. Run gen_deck.py first, then print these to assets/ with headless Chrome."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "deck")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
import gen_deck
ROCKET = io.open(os.path.join(ROOT, "assets", "rocket_path.txt")).read().strip()
esc = gen_deck.esc

CSS = """
@page{size:A4;margin:14mm 15mm 12mm}
*{margin:0;padding:0;box-sizing:border-box}
:root{--blue:#1D4ED8;--sky:#2563EB;--ink:#0B1526;--body:#3B4A63;--soft:#6B7C99;--line:#DDE4F0;--tint:#F4F7FC}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:"Inter",-apple-system,Helvetica,Arial,sans-serif;color:var(--body);font-size:9.45pt;line-height:1.5}
h1,h2,h3,.brand b{font-family:"Space Grotesk","Inter",Helvetica,sans-serif}
.sheet{min-height:271mm;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between;padding-bottom:9px;border-bottom:2px solid var(--ink)}
.brand{display:flex;align-items:center;gap:8px}
.brand svg{width:19px;height:19px}
.brand b{font-size:14pt;color:var(--ink);letter-spacing:-.01em}
.tag{font-family:"IBM Plex Mono",monospace;font-size:7.2pt;letter-spacing:.2em;text-transform:uppercase;color:var(--sky)}
h1{font-size:20pt;line-height:1.14;color:var(--ink);letter-spacing:-.02em;margin-top:15px;max-width:158mm}
.who{font-family:"IBM Plex Mono",monospace;font-size:7.4pt;letter-spacing:.13em;text-transform:uppercase;color:var(--soft);margin-top:9px}
.lede{font-size:10.6pt;line-height:1.48;color:var(--body);margin-top:12px;max-width:170mm}
.rows{margin-top:13px;border-top:1px solid var(--line)}
.r{display:grid;grid-template-columns:39mm 1fr;gap:13px;padding:9px 0;border-bottom:1px solid var(--line);page-break-inside:avoid}
.r h3{font-size:9.2pt;color:var(--blue);font-weight:600;line-height:1.32}
.r p{font-size:9.2pt;line-height:1.47}
.cta{margin-top:18px;background:var(--tint);border:1px solid #C9D9F0;border-radius:9px;padding:11px 14px;display:flex;
     align-items:center;justify-content:space-between;gap:16px}
.cta h3{font-size:10pt;color:var(--ink);margin-bottom:2px}
.cta p{font-size:9pt;color:var(--body);max-width:118mm}
.cta a{font-family:"Space Grotesk",sans-serif;font-size:10pt;font-weight:700;color:#fff;background:var(--blue);
       border-radius:7px;padding:8px 14px;text-decoration:none;white-space:nowrap}
.foot{margin-top:auto;padding-bottom:0;display:flex;justify-content:space-between;font-size:7.4pt;color:#9AA8BF;
      border-top:1px solid var(--line);padding-top:6px}
"""

MORE = {"en": "Full 14-page business case at rocketx.app",
        "de": "Vollständiger Business Case, 14 Seiten, auf rocketx.app",
        "es": "Caso de negocio completo, 14 páginas, en rocketx.app",
        "nl": "Volledige business case, 14 pagina’s, op rocketx.app"}

def build(d):
    rows = "".join('<div class="r"><h3>%s</h3><p>%s</p></div>' % (esc(a), esc(b)) for a, b in d["xs"])
    return """<!DOCTYPE html><html lang="%s"><head><meta charset="UTF-8"><title>%s</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<style>%s</style></head><body><div class="sheet">
<div class="top"><div class="brand"><svg viewBox="0 0 100 100"><path d="%s" fill="#1D4ED8" fill-rule="evenodd"/></svg><b>RocketX</b></div>
<div class="tag">%s</div></div>
<h1>%s</h1>
<div class="who">%s</div>
<p class="lede">%s</p>
<div class="rows">%s</div>
<div class="cta"><div><h3>%s</h3><p>%s</p></div><a href="mailto:%s">%s</a></div>
<div class="foot"><span>%s</span><span>%s</span></div>
</div></body></html>""" % (
      d["lang"], esc(d["doctitle"]), CSS, ROCKET, esc(d["xsh"]).upper(),
      esc(d["title"]), esc(d["forwho"]), esc(d["xsa"]), rows,
      esc(d["ctah"]), esc(d["ctap"]), d["contact"], d["contact"],
      esc(d["foot"]), esc(MORE[d["lang"]]))

for lg, d in gen_deck.C.items():
    p = os.path.join(OUT, "rocketx-one-page-%s.html" % lg)
    io.open(p, "w", encoding="utf-8").write(build(d))
    print("  wrote", os.path.basename(p))
