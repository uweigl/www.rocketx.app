#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the comparison pages: /compare/<slug>/.

Three honest, sourced comparisons against the vendors a shortlist actually
contains. English only for now - buyers in every market search these vendor
names in English - and linked from the comparison section in all five
languages, labelled as English.

Every competitor claim carries a public source, most of them the vendor's own
documentation or reviews in the vendor's own communities. The pages follow the
site's honest-comparison ethos: each one says plainly who the competitor is
right for. RocketX claims on these pages are limited to what the site already
claims elsewhere.
"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import site_footer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.rocketx.app"
SLUGS = ["shopify-b2b", "pepperi", "sana-commerce"]

CSS = u"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--void:#05080F;--panel:#0E1B33;--navy:#0B1526;--ice:#EDF2FB;--mist:#8FA1C4;
      --sky:#60A5FA;--blue:#2563EB;--line:#1E2E4C}
html{-webkit-text-size-adjust:100%}
body{background:var(--void);color:var(--ice);line-height:1.65;
     font-family:Inter,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif}
a{color:var(--sky)}
.wrap{max-width:860px;margin:0 auto;padding:0 24px}
header{padding:24px 0;border-bottom:1px solid var(--line)}
header .wrap{display:flex;justify-content:space-between;align-items:center}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--ice);text-decoration:none}
.brand img{width:28px;height:28px;border-radius:7px}
.brand b{font-family:"Space Grotesk",Inter,sans-serif;font-size:16px}
header a.back{color:var(--mist);font-size:14px;text-decoration:none}
header a.back:hover{color:var(--sky)}
main{padding:48px 0 72px}
.kick{font-family:"IBM Plex Mono",monospace;font-size:12px;letter-spacing:2.2px;
      color:var(--sky);margin-bottom:14px}
h1{font-family:"Space Grotesk",Inter,sans-serif;font-size:clamp(27px,4.6vw,40px);
   line-height:1.12;letter-spacing:-1px;font-weight:600;max-width:24ch}
.lede{color:var(--mist);margin:18px 0 0;max-width:64ch;font-size:16.5px}
h2{font-family:"Space Grotesk",Inter,sans-serif;font-size:21px;letter-spacing:-.4px;
   margin:44px 0 14px}
p{color:var(--mist);font-size:15.5px;margin-bottom:14px;max-width:70ch}
p strong{color:var(--ice)}
ul.facts{list-style:none;margin:14px 0}
ul.facts li{color:var(--mist);font-size:15px;padding:12px 0 12px 18px;
  border-left:3px solid var(--line);margin-bottom:10px;max-width:72ch}
ul.facts li b{color:var(--ice)}
ul.facts li .src{display:block;margin-top:5px;font-size:12.5px}
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:14.5px}
th{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:1.4px;
   text-transform:uppercase;color:var(--mist);text-align:left;padding:10px 12px}
td{padding:12px;border-top:1px solid var(--line);color:var(--mist);vertical-align:top}
td:first-child{color:var(--ice);white-space:nowrap}
tr.rx td{color:var(--ice)}
.fair{border:1px solid var(--line);border-radius:14px;padding:20px 24px;margin:30px 0;
      background:var(--panel)}
.fair h2{margin-top:0;font-size:17px}
.fair p{margin-bottom:0}
.ctabox{margin-top:44px;border:1px solid var(--line);border-radius:16px;
        padding:28px;background:var(--panel);text-align:center}
.ctabox p{margin:0 auto 18px;max-width:56ch}
.ctabox .cta{display:inline-block;background:var(--blue);color:#fff;padding:13px 26px;
        border-radius:9px;font-weight:600;text-decoration:none}
.ctabox .dl{display:inline-block;margin-left:18px;color:var(--mist);font-size:14px}
footer{border-top:1px solid var(--line);padding:18px 0;color:var(--mist);font-size:13px}
.note{font-size:12.5px;color:var(--mist);opacity:.85;margin-top:34px;max-width:74ch}
"""


def li(text, src_label, src_url):
    return (u'<li>%s<span class="src">Source: <a href="%s" rel="noopener nofollow" '
            u'target="_blank">%s</a></span></li>' % (text, src_url, src_label))


PAGES = {
 "shopify-b2b": dict(
  title=u"RocketX vs Shopify B2B — an honest comparison for wholesalers",
  desc=u"Where Shopify's B2B features end and where a dedicated wholesale ordering platform begins: order-size ceilings, shared carts, native apps, offline — with sources.",
  h1=u"RocketX vs Shopify B2B",
  lede=u"Shopify is superb at what it was built for. The question for a wholesaler is narrower: is the B2B on top of it shaped like your order flow? Here is the comparison we would want to read, with every claim sourced.",
  good_h=u"What Shopify genuinely does well",
  good=u"World-class checkout and hosting, an enormous app ecosystem, and since April 2026 the core B2B primitives — company accounts, per-customer catalogs, quantity rules, net terms — are included on every plan. For a brand selling mostly direct-to-consumer with a wholesale side channel, Shopify B2B is often enough, and we say so to prospects for whom that is true.",
  facts_h=u"The documented edges, from Shopify's own pages",
  facts=[
   (u"<b>Orders cap at 500 line items</b> (200 on draft orders) — above that the order fails. A stocking wholesale order in parts, fashion or cosmetics can cross that line routinely.",
    u"Shopify Help Center — B2B considerations", u"https://help.shopify.com/en/manual/b2b/getting-started/considerations"),
   (u"<b>Carts are per-device and per-browser.</b> One buyer building an order for a manager to approve — the everyday shape of wholesale buying — has, in Shopify's own community words, “no out-of-the-box solution”. The thread has been open since July 2025.",
    u"Shopify Community — shared carts across devices", u"https://community.shopify.com/t/how-do-your-b2b-customers-share-carts-or-use-carts-across-multiple-devices/551949"),
   (u"<b>No native buyer app, no offline catalogue.</b> Shopify's B2B solutions page describes a responsive web storefront; a buyer in a warehouse aisle with no signal is not part of the model.",
    u"Shopify Plus — B2B solutions page", u"https://www.shopify.com/plus/solutions/b2b-ecommerce"),
   (u"<b>Above a negotiable GMV threshold, Plus switches to a variable platform fee</b> — analyses cite ~0.25% of monthly GMV on 3-year terms, capped around $40k/month. The flat fee quietly becomes a share of your growth.",
    u"Shopify Plus pricing + independent analysis", u"https://www.brokenrubik.com/blog/shopify-plus-pricing-guide"),
   (u"<b>Below Plus, active B2B catalogs cap at three</b> — per-customer negotiated pricing at wholesale scale effectively requires the Plus tier.",
    u"SparkLayer — Shopify B2B on all plans", u"https://www.sparklayer.io/blog/2026/04/03/shopify-b2b-all-plans/"),
  ],
  table=[
   (u"Order size", u"500 line items max (200 on drafts)", u"Built for stocking orders; no published order ceiling on any tier"),
   (u"Cart", u"Per device, per browser", u"Server-side, shared live across the team, visible to your reps"),
   (u"Buyer mobile", u"Responsive web", u"Native iOS &amp; Android, catalogue cached offline"),
   (u"Pricing shape", u"$2,300–2,500/mo, then a variable fee above a GMV threshold", u"Flat monthly fee, published, never a percentage of revenue"),
   (u"Your web shop", u"Is the platform", u"Keeps running — RocketX goes live beside it"),
  ],
  fair=u"Choose Shopify if you are primarily a DTC brand with a modest wholesale side, order sizes stay comfortably under the caps, and your buyers order at desks. Those businesses are well served — and are not who RocketX is built for.",
 ),
 "pepperi": dict(
  title=u"RocketX vs Pepperi — an honest comparison for wholesalers",
  desc=u"Pepperi is the closest product shape to RocketX: native apps, offline, field sales. The differences are reliability, pricing transparency and what the cart is — with sources.",
  h1=u"RocketX vs Pepperi",
  lede=u"Pepperi deserves respect: 1,000+ customers, true native iOS and Android apps, offline order-taking for field reps. It is the closest shape to RocketX on the market — which is exactly why the differences are worth stating precisely.",
  good_h=u"What Pepperi genuinely does well",
  good=u"A mature field-sales suite: rep order-taking on tablets, trade promotions, SAP Business One integration, two decades of wholesale domain knowledge across food, beauty and consumer goods. If your model is rep-led van sales with deep trade-promotion mechanics, Pepperi has features RocketX does not try to match.",
  facts_h=u"The documented edges, from Pepperi's own reviewers",
  facts=[
   (u"<b>Offline is Pepperi's most-praised feature — and sync reliability is its most-repeated complaint.</b> Recent reviews describe crashes, freezes and resync failures during store visits, and update-related downtime. Offline that cannot sync back is a lost order with extra steps.",
    u"Capterra — Pepperi reviews", u"https://www.capterra.com/p/146870/Pepperi/reviews/"),
   (u"<b>The public pricing page is gone</b> — both URL variants return 404 since the 2024 private-equity acquisition. Third-party sources describe per-user licences plus modules plus implementation, with real mid-market costs reported at $20,000–50,000+/year before you know it.",
    u"WizCommerce — Pepperi pricing analysis", u"https://wizcommerce.com/blog/pepperi-pricing/"),
   (u"<b>Support is time-zone bound,</b> reviewers report, with slower Android parity and a back office one French reviewer calls “vieillissant et catastrophiquement lent”.",
    u"Capterra / G2 — Pepperi reviews", u"https://www.g2.com/products/pepperi/reviews"),
  ],
  table=[
   (u"Native apps, offline", u"Yes — its real strength", u"Yes — catalogue, pricing, cart and your brochures cached locally"),
   (u"Sync model", u"Device-led; reviewers report resync failures mid-visit", u"Server-side carts: every change lands on the server as it happens"),
   (u"Who shares a cart", u"Rep-centric ordering", u"Buyers and reps work one live cart together, every change named"),
   (u"Pricing", u"Unpublished; per-user licences + modules", u"Flat monthly fee, published, unlimited SKUs and seats"),
   (u"Trying it", u"Demo, then sales cycle", u"30–45 day pilot with agreed measures — miss them, walk away owing nothing"),
  ],
  fair=u"Choose Pepperi if your business is rep-driven van sales with heavy trade-promotion needs and you have the implementation partner its setup expects. If the centre of your problem is buyers and reps building orders together — reliably, offline, at a predictable price — that is the problem RocketX was built around.",
 ),
 "sana-commerce": dict(
  title=u"RocketX vs Sana Commerce — an honest comparison for wholesalers",
  desc=u"Sana's real-time ERP coupling is its strength and its constraint. Where that architecture helps, where it binds, and how a beside-your-shop platform differs — with sources.",
  h1=u"RocketX vs Sana Commerce",
  lede=u"Sana Commerce made a clear architectural bet: the webstore reads and writes your ERP directly, in real time. Where that bet pays off it pays well. The honest comparison is about what the same bet costs.",
  good_h=u"What Sana genuinely does well",
  good=u"If you run SAP or Microsoft Dynamics and want the storefront to be a pure window onto the ERP — prices, stock, customer terms, live — Sana's integration depth is its deserved reputation, and its case-study library shows real results at real manufacturers.",
  facts_h=u"The documented edges, from Sana's own pages and reviewers",
  facts=[
   (u"<b>SAP and Microsoft Dynamics only.</b> Sana's architecture requires one of two ERP families; every wholesaler on anything else is out of scope by design.",
    u"Sana Commerce — homepage", u"https://www.sana-commerce.com/"),
   (u"<b>The coupling cuts both ways:</b> reviewers report that customisation must route through the ERP, storefront performance depends on ERP web services, custom features take months, and upgrades break customer-specific work.",
    u"PeerSpot — Sana Commerce pros and cons", u"https://www.peerspot.com/products/sana-commerce-pros-and-cons"),
   (u"<b>“They only check cases twice a week”</b> — the same support-cadence complaint appears verbatim on two independent review platforms, alongside reports that support is effectively English-only for non-English markets.",
    u"G2 / TrustRadius — Sana Commerce reviews", u"https://www.trustradius.com/products/sana-commerce/reviews?qs=pros-and-cons"),
   (u"<b>No native buyer app in the current product.</b> Sana Commerce Cloud is a web storefront; the offline mobile app exists only in legacy 9.0 documentation as a sales-agent tool.",
    u"Sana Commerce 9.0 documentation — Sana Mobile", u"https://help.sana-commerce.com/sana-commerce-90/user_guide/sana-mobile-app/introduction"),
   (u"<b>Pricing is quote-only</b> across all three tiers — no number appears anywhere on the pricing page.",
    u"Sana Commerce — pricing page", u"https://www.sana-commerce.com/pricing/"),
  ],
  table=[
   (u"ERP scope", u"SAP and Microsoft Dynamics, exclusively", u"Standard connectors: SAP, NetSuite, Microsoft Dynamics, Epicor"),
   (u"Architecture", u"Storefront reads/writes the ERP live", u"Runs beside your systems of record — and beside your existing web shop"),
   (u"Buyer mobile", u"Responsive web", u"Native iOS &amp; Android, offline catalogue incl. your brochures and video"),
   (u"Cart", u"Individual web sessions", u"Server-side shared carts your reps can see and join"),
   (u"Pricing", u"Quote-only", u"Flat monthly fee, published, never a percentage of revenue"),
  ],
  fair=u"Choose Sana if you are committed to SAP or Dynamics, want the storefront to be the ERP's mirror, and your buyers order at desks on the web. If your buyers order from aisles and cars, your team builds orders together, or your ERP is not on Sana's list — that is the gap RocketX fills, without asking you to replace anything.",
 ),
}


def build(slug):
    d = PAGES[slug]
    facts = u"".join(li(t, sl, su) for t, sl, su in d["facts"])
    rows = u"".join(
        u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (a, b, c)
        for a, b, c in d["table"])
    other = [s for s in SLUGS if s != slug]
    html = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>%(title)s</title>
<meta name="description" content="%(desc)s"/>
<link rel="canonical" href="%(site)s/compare/%(slug)s/"/>
<link rel="icon" href="/favicon.ico"/>
<style>/* fonts are self-hosted: no request leaves this domain */\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url('/assets/fonts/ibmplexmono-400-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:400;font-display:swap;src:url('/assets/fonts/ibmplexmono-400-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;src:url('/assets/fonts/ibmplexmono-500-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'IBM Plex Mono';font-style:normal;font-weight:500;font-display:swap;src:url('/assets/fonts/ibmplexmono-500-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url('/assets/fonts/inter-400-600-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'Inter';font-style:normal;font-weight:400 600;font-display:swap;src:url('/assets/fonts/inter-400-600-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}\n@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400 700;font-display:swap;src:url('/assets/fonts/spacegrotesk-400-700-latin-ext.woff2') format('woff2');unicode-range:U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF}\n@font-face{font-family:'Space Grotesk';font-style:normal;font-weight:400 700;font-display:swap;src:url('/assets/fonts/spacegrotesk-400-700-latin.woff2') format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}</style>
<style>%(css)s</style>
</head>
<body>
<header><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo.png" alt=""/><b>RocketX</b></a>
<a class="back" href="/#compare">&larr; The honest comparison</a>
</div></header>
<main><div class="wrap">
<div class="kick">/ COMPARED, WITH SOURCES</div>
<h1>%(h1)s</h1>
<p class="lede">%(lede)s</p>

<h2>%(good_h)s</h2>
<p>%(good)s</p>

<h2>%(facts_h)s</h2>
<ul class="facts">%(facts)s</ul>

<h2>The two shapes, side by side</h2>
<table>
<thead><tr><th></th><th>%(name)s</th><th>RocketX</th></tr></thead>
<tbody>%(rows)s</tbody>
</table>

<div class="fair">
<h2>Where they are the right choice</h2>
<p>%(fair)s</p>
</div>

<div class="ctabox">
<p>The way to settle it is not a comparison page — ours included. It is a 30–45 day pilot against your own catalogue, with measures agreed up front. If the pilot misses them, you walk away owing nothing.</p>
<a class="cta" href="/#pricing">See the flat pricing</a>
<a class="dl" href="/assets/rocketx-business-case-en.pdf" download>Business case (PDF)</a>
</div>

<p class="note">Competitor information verified against the linked sources in August 2026; platforms change, and if anything here has gone stale, tell us and we will correct it. Also compared: <a href="/compare/%(o1)s/">%(on1)s</a> · <a href="/compare/%(o2)s/">%(on2)s</a>.</p>
</div></main>
___SFOOT___
</body>
</html>
""" % dict(title=d["title"], desc=d["desc"], site=SITE, slug=slug, css=CSS.strip(),
           h1=d["h1"], lede=d["lede"], good_h=d["good_h"], good=d["good"],
           facts_h=d["facts_h"], facts=facts, rows=rows,
           name=d["h1"].replace("RocketX vs ", ""), fair=d["fair"],
           o1=other[0], on1=PAGES[other[0]]["h1"].replace("RocketX vs ", ""),
           o2=other[1], on2=PAGES[other[1]]["h1"].replace("RocketX vs ", ""))
    html = html.replace("___SFOOT___", site_footer.footer_html("en"))
    outdir = os.path.join(ROOT, "compare", slug)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    p = os.path.join(outdir, "index.html")
    io.open(p, "w", encoding="utf-8").write(html)
    return p


if __name__ == "__main__":
    for slug in SLUGS:
        p = build(slug)
        print("wrote %s (%d KB)" % (os.path.relpath(p, ROOT),
                                    os.path.getsize(p) // 1024))
