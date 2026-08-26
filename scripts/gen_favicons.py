#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a complete favicon set from the RocketX rocket mark.

Small icons need optical scaling: a faithful downscale of logo.png is
illegible at 16px because the rocket sits inside a lot of padding.
"""
import io, os, struct, subprocess, sys

ROOT = os.path.expanduser("~/Downloads/rocketx-site3")
OUT = os.path.join(ROOT, "assets")
SP = "/private/tmp/claude-502/-Users-whiterabbit-Downloads-rocketx-site3/a968dd59-c54d-4ecc-802b-a8af62f96d8c/scratchpad"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# rocket glyph in a 100x100 box; porthole is a hole (evenodd)
ROCKET = 'M36.00 42.00L37.50 32.50L42.00 21.50L43.00 21.00L46.00 15.50L48.50 13.50L48.50 12.50L51.00 12.50L55.50 18.00L58.00 23.50L59.00 24.00L63.00 36.50L63.50 51.50L60.50 64.50L40.00 65.00L39.00 64.00L37.00 57.00L36.00 42.00Z M43.00 75.00L44.00 72.00L48.00 69.00L51.50 69.00L55.50 71.50L56.50 73.50L56.00 78.50L50.00 87.50L45.00 81.00L43.00 75.00Z M25.50 51.00L26.00 47.50L28.50 41.50L32.50 37.00L33.50 37.00L32.50 47.00L34.00 58.50L27.50 58.50L26.00 56.50L25.50 51.00Z M65.50 57.50L67.00 50.50L67.00 37.00L70.50 40.50L73.00 45.00L74.00 49.00L74.00 55.00L73.50 57.50L72.00 58.50L66.00 58.50L65.50 57.50Z M45.50 43.00L48.00 39.50L51.50 39.50L54.00 42.00L54.00 45.00L52.00 47.50L49.50 48.00L46.50 46.50L45.50 43.00Z'
# at 16px the detailed glyph collapses into an arrow; a bolder single
# outline with flared fins stays legible on the 16px pixel grid
BOLD = ("M50 6 C60 19 66.5 36 66.5 51.5 L66.5 60 L79 74 L79 86 L64.5 77.5 L60 88 L40 88 "
        "L35.5 77.5 L21 86 L21 74 L33.5 60 L33.5 51.5 C33.5 36 40 19 50 6 Z")
BOLD_BB = (21.0, 6.0, 79.0, 88.0)

BB = (25.5, 12.5, 73.5, 87.0)          # bbox of the traced logo shape
GW, GH = BB[2] - BB[0], BB[3] - BB[1]

def svg(size, frac, radius_frac, flat=False, simplify=False):
    """frac = glyph height as a fraction of the frame; radius_frac = corner radius."""
    bb, gw, gh = (BOLD_BB, BOLD_BB[2]-BOLD_BB[0], BOLD_BB[3]-BOLD_BB[1]) if simplify else (BB, GW, GH)
    k = (size * frac) / gh
    tx = (size - gw * k) / 2.0 - bb[0] * k
    ty = (size - gh * k) / 2.0 - bb[1] * k
    r = size * radius_frac
    bg = ('<rect width="%g" height="%g" rx="%g" fill="#1D4ED8"/>' % (size, size, r) if flat
          else '<rect width="%g" height="%g" rx="%g" fill="url(#g)"/>' % (size, size, r))
    # at 16px the porthole and fin notches turn to noise; drop the hole
    d = BOLD if simplify else ROCKET
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%g" height="%g" viewBox="0 0 %g %g">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#5AA0FF"/><stop offset=".55" stop-color="#2563EB"/>'
            '<stop offset="1" stop-color="#1436A8"/></linearGradient></defs>'
            '%s<g transform="translate(%.4f %.4f) scale(%.6f)">'
            '<path d="%s" fill="#FFFFFF" fill-rule="evenodd"/></g></svg>'
            % (size, size, size, size, bg, tx, ty, k, d))

def render(svg_text, size, path):
    """Render an SVG at exactly size x size px (top-left of a big window, then crop)."""
    html = ('<body style="margin:0;background:transparent;display:flex;align-items:center;'
            'justify-content:center;height:700px">'
            '<div style="width:%dpx;height:%dpx;flex:none">%s</div></body>' % (size, size, svg_text))
    h = os.path.join(SP, "_icon.html")
    io.open(h, "w", encoding="utf-8").write(html)
    shot = os.path.join(SP, "_icon_full.png")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--default-background-color=00000000",
                    "--hide-scrollbars", "--virtual-time-budget=4000",
                    "--window-size=700,700", "--screenshot=" + shot, "file://" + h],
                   capture_output=True)
    subprocess.run(["sips", "--cropToHeightWidth", str(size), str(size),
                    shot, "--out", path], capture_output=True)
    return os.path.exists(path)

# ---------------------------------------------------------------- build PNGs
# rounded-tile icons for browser tabs; larger glyph at smaller sizes
SPECS = [
    ("favicon-16.png",       16, 0.78, 0.20, True),
    ("favicon-32.png",       32, 0.74, 0.20, False),
    ("favicon-48.png",       48, 0.72, 0.20, False),
    ("favicon-64.png",       64, 0.70, 0.20, False),
    # iOS masks its own corners -> full bleed square, glyph inset
    ("apple-touch-icon.png", 180, 0.62, 0.0, False),
    # Android maskable: keep the glyph inside the central 80% safe zone
    ("icon-192.png",         192, 0.56, 0.0, False),
    ("icon-512.png",         512, 0.56, 0.0, False),
]
made = []
for name, size, frac, rad, simp in SPECS:
    p = os.path.join(OUT, name)
    ok = render(svg(size, frac, rad, flat=False, simplify=simp), size, p)
    made.append((name, size, ok, os.path.getsize(p) if ok else 0))
    print("  %-24s %4dpx  %s" % (name, size, "ok" if ok else "FAILED"))

# scalable icon for modern browsers
io.open(os.path.join(OUT, "icon.svg"), "w", encoding="utf-8").write(svg(64, 0.70, 0.20))
print("  icon.svg                 vector  ok")

# ---------------------------------------------------------------- favicon.ico
def build_ico(png_paths, out):
    imgs = [io.open(p, "rb").read() for p in png_paths]
    n = len(imgs)
    hdr = struct.pack("<HHH", 0, 1, n)
    off = 6 + 16 * n
    entries, blob = b"", b""
    for p, data in zip(png_paths, imgs):
        sz = int(os.path.basename(p).split("-")[1].split(".")[0])
        entries += struct.pack("<BBBBHHII", sz if sz < 256 else 0, sz if sz < 256 else 0,
                               0, 0, 1, 32, len(data), off)
        off += len(data)
        blob += data
    io.open(out, "wb").write(hdr + entries + blob)

ico_src = [os.path.join(OUT, f) for f in ("favicon-16.png", "favicon-32.png", "favicon-48.png")]
ico_path = os.path.join(ROOT, "favicon.ico")
build_ico(ico_src, ico_path)
print("  favicon.ico              16/32/48  %d bytes" % os.path.getsize(ico_path))

# ---------------------------------------------------------------- manifest
man = {
  "name": "RocketX", "short_name": "RocketX",
  "description": "Frictionless B2B ordering for wholesale and distribution.",
  "icons": [
    {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
    {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}
  ],
  "theme_color": "#05080F", "background_color": "#05080F", "display": "standalone", "start_url": "."
}
import json
io.open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8").write(json.dumps(man, indent=2))
print("  site.webmanifest         ok")
