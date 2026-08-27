# -*- coding: utf-8 -*-
"""Figures for the business-case decks.

Four illustrations, drawn as inline SVG on the deck's light palette. Every
label is passed in from the per-language content dict so the figures speak
the same language as the page they sit on. Nothing here is decorative: each
one carries an argument the surrounding prose otherwise has to state.
"""
CRMS = u"Salesforce, HubSpot …"
INK, BODY, SOFT, LINE, TINT = "#0B1526", "#3B4A63", "#6B7C99", "#DDE4F0", "#F4F7FC"
BLUE, SKY, GREEN, WARN = "#1D4ED8", "#2563EB", "#15803D", "#B45309"
SANS = 'font-family="Inter,Helvetica,Arial,sans-serif"'
DISP = 'font-family="Space Grotesk,Inter,sans-serif"'
MONO = 'font-family="IBM Plex Mono,monospace"'


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def T(x, y, s, txt, fill=BODY, anchor="start", weight="400", font=SANS, extra=""):
    return ('<text ' + font + ' x="' + str(round(x, 2)) + '" y="' + str(round(y, 2))
            + '" font-size="' + str(s) + '" fill="' + fill + '" text-anchor="' + anchor
            + '" font-weight="' + weight + '"' + extra + '>' + esc(txt) + '</text>')


def box(x, y, w, h, r=8, fill=TINT, stroke=LINE, sw="1"):
    return ('<rect x="' + str(round(x, 2)) + '" y="' + str(round(y, 2)) + '" width="' + str(round(w, 2))
            + '" height="' + str(round(h, 2)) + '" rx="' + str(r) + '" fill="' + fill
            + '" stroke="' + stroke + '" stroke-width="' + sw + '"/>')


def arrow(x1, y1, x2, y2, colour, sw="2", dash=""):
    d = 1 if x2 > x1 else -1
    da = ' stroke-dasharray="' + dash + '"' if dash else ""
    return ('<path d="M' + str(round(x1, 2)) + ' ' + str(round(y1, 2)) + 'H' + str(round(x2 - d * 9, 2))
            + '" fill="none" stroke="' + colour + '" stroke-width="' + sw + '" stroke-linecap="round"' + da + '/>'
            + '<path d="M' + str(round(x2, 2)) + ' ' + str(round(y2, 2)) + 'l' + str(-d * 9)
            + ' -5v10z" fill="' + colour + '"/>')


def wrap(txt, per):
    """Greedy wrap into lines of at most `per` characters."""
    out, cur = [], ""
    for w in str(txt).split():
        if cur and len(cur) + 1 + len(w) > per:
            out.append(cur); cur = w
        else:
            cur = w if not cur else cur + " " + w
    if cur:
        out.append(cur)
    return out


def svg(w, h, body, cls="fig"):
    return ('<svg class="' + cls + '" role="img" viewBox="0 0 ' + str(w) + ' ' + str(h)
            + '" xmlns="http://www.w3.org/2000/svg">' + body + '</svg>')


# --------------------------------------------------------------- 1. fee curve
def fig_fee(d):
    """Platform fee as a share of sales: RocketX falls, a percentage plan does not."""
    bands, fees = d["fg1_bands"], d["fg1_fees"]
    rmin, rmax = bands[0], bands[-1]
    dec, sp = d["fg1_dec"], d["fg1_sp"]
    CAP, RATE = d["fg1_cap"], 0.25

    def rx(r):
        for i in range(len(fees)):
            if r <= bands[i + 1] or i == len(fees) - 1:
                return fees[i] / (r * 10000.0)
        return 0

    def sh(r):
        return min(RATE, CAP / (r * 10000.0))

    top = max(rx(rmin), RATE) * 1.18
    ymax = round(top + 0.049, 1)
    X0, X1, Y0, Y1 = 104, 678, 32, 156

    def px(r):
        return X0 + (r - rmin) / float(rmax - rmin) * (X1 - X0)

    def py(v):
        return Y1 - v / ymax * (Y1 - Y0)

    def pct(v, dp=2):
        s = ("%." + str(dp) + "f") % v
        return s.replace(".", dec) + sp + "%"

    o = []
    # grid
    steps = int(round(ymax / 0.1))
    for i in range(steps + 1):
        v = i * 0.1
        o.append('<path d="M' + str(X0) + ' ' + str(round(py(v), 2)) + 'H' + str(X1)
                 + '" stroke="' + LINE + '" stroke-width="1"/>')
        o.append(T(X0 - 9, py(v) + 3.4, 9.5, pct(v, 1), SOFT, "end"))
    # sampled curves
    N = 240
    rs = [rmin + (rmax - rmin) * i / float(N) for i in range(N + 1)]
    # region where RocketX costs less
    cross = None
    for r in rs:
        if rx(r) < sh(r):
            cross = r; break
    if cross is not None:
        seg = [r for r in rs if r >= cross]
        up = " ".join(str(round(px(r), 2)) + "," + str(round(py(sh(r)), 2)) for r in seg)
        dn = " ".join(str(round(px(r), 2)) + "," + str(round(py(rx(r)), 2)) for r in reversed(seg))
        o.append('<polygon points="' + up + " " + dn + '" fill="#EFF5FF"/>')
    o.append('<polyline points="' + " ".join(str(round(px(r), 2)) + "," + str(round(py(sh(r)), 2)) for r in rs)
             + '" fill="none" stroke="' + SOFT + '" stroke-width="2" stroke-dasharray="6 4"/>')
    # RocketX drawn per tier so the step at each band edge stays visible
    for i in range(len(fees)):
        a, b = bands[i], bands[i + 1]
        pts = [a + (b - a) * k / 40.0 for k in range(41)]
        o.append('<polyline points="' + " ".join(str(round(px(r), 2)) + "," + str(round(py(rx(r)), 2)) for r in pts)
                 + '" fill="none" stroke="' + BLUE + '" stroke-width="2.8" stroke-linecap="round"/>')
        o.append('<circle cx="' + str(round(px(a), 2)) + '" cy="' + str(round(py(rx(a)), 2))
                 + '" r="3.4" fill="#fff" stroke="' + BLUE + '" stroke-width="2"/>')
    o.append('<circle cx="' + str(round(px(rmax), 2)) + '" cy="' + str(round(py(rx(rmax)), 2))
             + '" r="3.4" fill="' + BLUE + '"/>')
    # axes
    o.append('<path d="M' + str(X0) + ' ' + str(Y1) + 'H' + str(X1) + '" stroke="' + SOFT + '" stroke-width="1.4"/>')
    for r in bands:
        o.append('<path d="M' + str(round(px(r), 2)) + ' ' + str(Y1) + 'v6" stroke="' + SOFT + '" stroke-width="1.4"/>')
        o.append(T(px(r), Y1 + 19, 9.5, ("%g" % r).replace(".", dec), BODY, "middle"))
    # endpoint callouts
    o.append(T(px(rmin) + 9, py(rx(rmin)) - 8, 12, pct(rx(rmin)), BLUE, "start", "700", DISP))
    o.append(T(px(rmax) - 4, py(rx(rmax)) - 12, 12, pct(rx(rmax)), BLUE, "end", "700", DISP))
    # legend
    ly = Y1 + 52
    o.append('<path d="M' + str(X0) + ' ' + str(ly - 4) + 'h22" stroke="' + BLUE + '" stroke-width="2.8" stroke-linecap="round"/>')
    o.append(T(X0 + 29, ly, 10, d["fg1_rx"], INK, "start", "600"))
    o.append('<path d="M' + str(X0 + 190) + ' ' + str(ly - 4) + 'h22" stroke="' + SOFT
             + '" stroke-width="2" stroke-dasharray="6 4"/>')
    o.append(T(X0 + 219, ly, 10, d["fg1_sh"], BODY, "start", "500"))
    # axis titles
    o.append(T(X0, Y1 + 34, 9, d["fg1_x"], SOFT, "start"))
    o.append(T(0, 15, 9.5, d["fg1_y"], SOFT, "start"))
    h = Y1 + 68
    for i, ln in enumerate(wrap(d["fg1_n"], 148)):
        o.append(T(0, h + 12 + i * 11, 8.4, ln, SOFT, "start"))
        h2 = h + 12 + i * 11
    return svg(700, int(h2 + 8), "".join(o))


# ----------------------------------------------------- 2. parallel-run timeline
def fig_parallel(d):
    """A replacement project has one track and a switchover. This has two tracks."""
    X0, X1 = 150, 676
    o = []
    o.append(T(0, 14, 10.5, d["fg2_ha"], INK, "start", "700", DISP))
    # replacement: one track, one hard switchover
    ty = 40
    o.append('<rect x="' + str(X0) + '" y="' + str(ty - 11) + '" width="' + str(int((X1 - X0) * .62))
             + '" height="22" rx="11" fill="' + TINT + '" stroke="' + LINE + '"/>')
    o.append(T(X0 + 14, ty + 4, 9.6, d["fg2_old"], BODY))
    cx = X0 + (X1 - X0) * .62
    o.append('<rect x="' + str(round(cx, 2)) + '" y="' + str(ty - 11) + '" width="' + str(round(X1 - cx, 2))
             + '" height="22" rx="11" fill="#FFF7ED" stroke="#FDBA74"/>')
    o.append(T(round(cx) + 14, ty + 4, 9.6, d["fg2_new"], WARN))
    o.append('<path d="M' + str(round(cx, 2)) + ' ' + str(ty - 20) + 'v40" stroke="' + WARN + '" stroke-width="2"/>')
    o.append('<circle cx="' + str(round(cx, 2)) + '" cy="' + str(ty - 20) + '" r="4" fill="' + WARN + '"/>')
    o.append(T(round(cx), ty - 28, 9.4, d["fg2_cut"], WARN, "middle", "600"))
    o.append(T(0, ty + 4, 9.4, d["fg2_la"], SOFT))
    # rocketx: two tracks, no switchover anywhere
    o.append(T(0, 100, 10.5, d["fg2_hb"], INK, "start", "700", DISP))
    for i, (lab, col, fill, stroke) in enumerate([
            (d["fg2_t1"], BODY, TINT, LINE), (d["fg2_t2"], BLUE, "#EFF5FF", "#BFD4FF")]):
        y = 124 + i * 30
        o.append('<rect x="' + str(X0) + '" y="' + str(y - 11) + '" width="' + str(X1 - X0)
                 + '" height="22" rx="11" fill="' + fill + '" stroke="' + stroke + '"/>')
        o.append(T(X0 + 14, y + 4, 9.6, lab, col))
        o.append(T(0, y + 4, 9.4, d["fg2_l1"] if i == 0 else d["fg2_l2"], SOFT))
    o.append('<path d="M' + str(X0 - 8) + ' 106V168" stroke="' + LINE + '" stroke-width="1"/>')
    o.append(T(X1, 182, 9.4, d["fg2_n"], GREEN, "end", "600"))
    return svg(700, 196, "".join(o))


# ------------------------------------------------------- 3. ERP/CRM integration
def fig_integration(dg, d):
    """Ported from the site: RocketX sits in front of the systems of record."""
    LX, LW, CX, CW, RX, RW = 2, 168, 258, 184, 530, 168
    TOP, H = 14, 176
    GAP = CX - (LX + LW) - 12
    LIM_L, LIM_C, LIM_R = LW - 32, CW - 18, RW - 32
    o = []
    o.append(box(LX, TOP, LW, H, 10))
    o.append(box(RX, TOP, RW, H, 10))
    o.append(box(CX, TOP + 6, CW, H - 12, 12, BLUE, "#1E40AF"))
    mx = lambda n: ' data-max="' + str(n) + '"'
    o.append(T(LX + 13, TOP + 20, 7.4, dg["dg.lh"], SKY, "start", "400", MONO, ' letter-spacing="0.8"' + mx(LIM_L)))
    o.append(T(RX + 13, TOP + 20, 7.4, dg["dg.rh"], SKY, "start", "400", MONO, ' letter-spacing="0.8"' + mx(LIM_R)))
    o.append(T(LX + 14, TOP + 40, 7.6, dg["dg.erp"], SOFT, "start", "400", MONO, ' letter-spacing="1"'))
    for i, n in enumerate(["SAP", "NetSuite", "Microsoft Dynamics", "Epicor"]):
        o.append('<circle cx="' + str(LX + 18) + '" cy="' + str(TOP + 51 + i * 18) + '" r="2.2" fill="' + SOFT + '"/>')
        o.append(T(LX + 27, TOP + 54 + i * 18, 9.2, n, INK, "start", "400", SANS, mx(LIM_L)))
    o.append(T(LX + 14, TOP + 140, 7.6, dg["dg.crm"], SOFT, "start", "400", MONO, ' letter-spacing="1"'))
    o.append('<circle cx="' + str(LX + 18) + '" cy="' + str(TOP + 153) + '" r="2.2" fill="' + SOFT + '"/>')
    o.append(T(LX + 27, TOP + 156, 9.2, CRMS, INK, "start", "400", SANS, mx(LIM_L)))
    for i, k in enumerate(("dg.d1", "dg.d2", "dg.d3")):
        o.append('<circle cx="' + str(RX + 18) + '" cy="' + str(TOP + 51 + i * 22) + '" r="2.2" fill="' + SOFT + '"/>')
        o.append(T(RX + 27, TOP + 54 + i * 22, 9.2, dg[k], INK, "start", "400", SANS, mx(LIM_R)))
    o.append('<path d="M' + str(RX + 14) + ' ' + str(TOP + 134) + 'H' + str(RX + RW - 14) + '" stroke="' + LINE + '"/>')
    for i, ln in enumerate(wrap(dg["dg.rn"], 25)):
        o.append(T(RX + 14, TOP + 150 + i * 11, 8.4, ln, BODY, "start", "400", SANS, mx(LIM_R)))
    mid = CX + CW / 2.0
    o.append(T(mid, TOP + 30, 13, "RocketX", "#fff", "middle", "700", DISP))
    for i, ln in enumerate(wrap(dg["dg.cs"], 32)):
        o.append(T(mid, TOP + 44 + i * 10, 8.0, ln, "#C7DBFF", "middle", "400", SANS, mx(LIM_C)))
    o.append('<path d="M' + str(CX + 16) + ' ' + str(TOP + 68) + 'H' + str(CX + CW - 16) + '" stroke="#4B7BE8"/>')
    yy = TOP + 84
    for k in ("dg.c1", "dg.c2", "dg.c3", "dg.c4"):
        for ln in wrap(dg[k], 38):
            o.append(T(mid, yy, 8.0, ln, "#EAF2FF", "middle", "400", SANS, mx(LIM_C)))
            yy += 10
        yy += 3
    o.append(arrow(LX + LW + 6, TOP + 56, CX - 4, TOP + 56, SKY))
    o.append(arrow(CX + CW + 6, TOP + 56, RX - 4, TOP + 56, SKY))
    o.append(arrow(RX - 4, TOP + 150, CX + CW + 6, TOP + 150, GREEN))
    o.append(arrow(CX - 4, TOP + 150, LX + LW + 6, TOP + 150, GREEN))
    for x, y, k1, k2, col in ((LX + LW + 8, TOP + 40, "dg.fa1", "dg.fa2", SKY),
                              (CX + CW + 8, TOP + 40, "dg.fb1", "dg.fb2", SKY),
                              (CX + CW + 8, TOP + 168, "dg.fc1", "dg.fc2", GREEN),
                              (LX + LW + 8, TOP + 168, "dg.fd1", "dg.fd2", GREEN)):
        o.append(T(x, y, 7.4, dg[k1], col, "start", "600", SANS, mx(GAP)))
        o.append(T(x, y + 9, 7.4, dg[k2], col, "start", "600", SANS, mx(GAP)))
    h = TOP + H + 16
    for i, ln in enumerate(wrap(d["fg3_n"], 140)):
        o.append(T(0, h + i * 11, 8.4, ln, SOFT))
        h2 = h + i * 11
    return svg(700, int(h2 + 8), "".join(o))


# ------------------------------------------------------------- 4. lost-order funnel
def fig_funnel(d):
    """Between order started and order submitted there is a gap nobody can see."""
    X0, X1 = 10, 690
    TOP, BH = 30, 78
    keep = 0.30
    o = []
    lw, rw = 132, 132
    o.append('<rect x="' + str(X0) + '" y="' + str(TOP) + '" width="' + str(lw) + '" height="' + str(BH)
             + '" rx="6" fill="#DCE8FB" stroke="#BFD4FF"/>')
    rh = BH * keep
    ry = TOP + (BH - rh) / 2.0
    o.append('<rect x="' + str(X1 - rw) + '" y="' + str(round(ry, 2)) + '" width="' + str(rw) + '" height="'
             + str(round(rh, 2)) + '" rx="6" fill="' + BLUE + '"/>')
    o.append('<polygon points="' + str(X0 + lw) + ',' + str(TOP) + ' ' + str(X1 - rw) + ',' + str(round(ry, 2))
             + ' ' + str(X1 - rw) + ',' + str(round(ry + rh, 2)) + ' ' + str(X0 + lw) + ',' + str(TOP + BH)
             + '" fill="#F1F5FB" stroke="' + SOFT + '" stroke-width="1.2" stroke-dasharray="5 4"/>')
    o.append(T(X0 + lw / 2.0, TOP - 12, 9.6, d["fg4_a"], INK, "middle", "600"))
    o.append(T(X1 - rw / 2.0, TOP - 12, 9.6, d["fg4_b"], INK, "middle", "600"))
    mid = (X0 + lw + X1 - rw) / 2.0
    o.append(T(mid, TOP + 34, 11.5, d["fg4_gap"], WARN, "middle", "700", DISP))
    for i, ln in enumerate(wrap(d["fg4_inv"], 46)):
        o.append(T(mid, TOP + 50 + i * 11, 9, ln, BODY, "middle"))
    cy = TOP + BH + 30
    w = (X1 - X0 - 24) / 3.0
    for i, k in enumerate(("fg4_c1", "fg4_c2", "fg4_c3")):
        x = X0 + i * (w + 12)
        o.append('<path d="M' + str(round(x, 2)) + ' ' + str(cy) + 'v34" stroke="' + SOFT + '" stroke-width="2"/>')
        for j, ln in enumerate(wrap(d[k], 34)):
            o.append(T(x + 10, cy + 12 + j * 12, 8.8, ln, BODY))
    return svg(700, int(cy + 50), "".join(o))

# ------------------------------------------------- 5. digital share of ordering
def fig_share(d):
    """One market's own digital-ordering share. Every number is that edition's,
    because the German and Dutch pages cite German and Dutch sources."""
    share, prev = d["fg5_share"], d.get("fg5_prev")
    X0, X1, BY, BH = 0, 700, 84, 68
    o = []
    o.append(T(0, 16, 12, d["fg5_t"], INK, "start", "700", DISP))
    for i, ln in enumerate(wrap(d["fg5_lbl"], 110)):
        o.append(T(0, 38 + i * 13, 9.2, ln, SOFT))
    o.append('<rect x="0" y="' + str(BY) + '" width="700" height="' + str(BH)
             + '" rx="8" fill="' + TINT + '" stroke="' + LINE + '"/>')
    w = 700 * share / 100.0
    o.append('<rect x="0" y="' + str(BY) + '" width="' + str(round(w, 1)) + '" height="' + str(BH)
             + '" rx="8" fill="' + BLUE + '"/>')
    lab = ("%g" % share).replace(".", d["fg1_dec"]) + d["fg1_sp"] + "%"
    inside = w > 120
    o.append(T(w - 14 if inside else w + 14, BY + BH / 2.0 + 7, 20,
               lab, "#fff" if inside else BLUE, "end" if inside else "start", "700", DISP))
    if prev:
        px = 700 * prev / 100.0
        o.append('<path d="M' + str(round(px, 1)) + ' ' + str(BY - 8) + 'V' + str(BY + BH + 8)
                 + '" stroke="#93B4E8" stroke-width="1.6" stroke-dasharray="4 3"/>')
        plab = ("%g" % prev).replace(".", d["fg1_dec"]) + d["fg1_sp"] + "%"
        o.append(T(round(px, 1) + 6, BY - 12, 9, plab + " " + d["fg5_prevlbl"], SOFT, "start", "600"))
    y = BY + BH + 30
    o.append('<path d="M0 ' + str(y - 12) + 'H700" stroke="' + LINE + '"/>')
    for i, ln in enumerate(wrap(d["fg5_meanwhile"], 104)):
        o.append(T(0, y + 6 + i * 14, 10, ln, BODY))
        yy = y + 4 + i * 13
    for i, ln in enumerate(wrap(d["fg5_n"], 140)):
        o.append(T(0, yy + 22 + i * 11, 8.2, ln, SOFT))
        h2 = yy + 22 + i * 11
    return svg(700, int(h2 + 10), "".join(o))


# ------------------------------------------------------ 6. reorder path, two ways
def fig_path(d):
    """Five steps in a browser against two in the app. The lanes are drawn to the
    same scale so the shorter one simply stops earlier."""
    CW, GAP = 130, 12
    o = []
    def lane(y, title, steps, colour, fill, stroke, note=None):
        o.append(T(0, y, 11, title, INK, "start", "700", DISP))
        for i, st in enumerate(steps):
            x = i * (CW + GAP)
            o.append('<rect x="' + str(x) + '" y="' + str(y + 12) + '" width="' + str(CW)
                     + '" height="52" rx="9" fill="' + fill + '" stroke="' + stroke + '"/>')
            for j, ln in enumerate(wrap(st, 17)):
                o.append(T(x + CW / 2.0, y + 36 + j * 12 - (len(wrap(st, 17)) - 1) * 6, 9,
                           ln, colour, "middle", "500", SANS, ' data-max="' + str(CW - 14) + '"'))
            if i < len(steps) - 1:
                cx = x + CW + GAP / 2.0
                o.append('<path d="M' + str(round(cx - 3, 1)) + ' ' + str(y + 33) + 'l4 5l-4 5" '
                         'fill="none" stroke="' + SOFT + '" stroke-width="1.6" '
                         'stroke-linecap="round" stroke-linejoin="round"/>')
        if note:
            x = len(steps) * (CW + GAP) + 4
            o.append(T(x, y + 42, 9.6, note, GREEN, "start", "600"))
    lane(16, d["fg6_a"], d["fg6_asteps"], BODY, TINT, LINE)
    lane(114, d["fg6_b"], d["fg6_bsteps"], "#12377F", "#EFF5FF", "#BFD4FF", d["fg6_note"])
    h = 196
    for i, ln in enumerate(wrap(d["fg6_n"], 140)):
        o.append(T(0, h + i * 11, 8.4, ln, SOFT))
        h2 = h + i * 11
    return svg(700, int(h2 + 10), "".join(o))
