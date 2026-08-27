RocketX site
============

Layout
------
  index.html                  the site (English). All copy for all five
                              languages lives in the I18N object near the
                              bottom; the language selector swaps it in place.
  de/ es/ nl/ fr/             pre-rendered German, Spanish, Dutch and French
                              pages, each with its own llms.txt  ) generated -
                              404.html                            ) do not edit
                              the error page, all five languages  ) by hand
  assets/                     images, video, favicons, og-image, the PDFs
  deck/                       source HTML for the business-case PDFs (generated)
  scripts/                    build and check tooling
  robots.txt, sitemap.xml     crawler directives, incl. named AI crawlers
  site.webmanifest            PWA / home-screen metadata

After editing index.html
------------------------
  ./scripts/build_all.sh                 regenerate everything, then check

That script is the one to use: it rebuilds the localised pages, the decks,
the one-pagers, llms.txt and 404.html, prints every PDF, and ends on
check_site.py with set -e, so a failing check cannot reach a commit.

Both are quick. check_site.py exits non-zero on failure, so it can gate a
deploy. It verifies translation completeness, HTML structure, asset
references, SEO metadata, and cross-document claims - including that the
page count the site advertises for the PDF actually matches the PDF, which
is the kind of thing that drifts silently.

After editing the business case
-------------------------------
  python3 scripts/gen_deck.py            rebuild deck/*.html from the content
                                         dictionaries inside that script
  then print each to PDF (headless Chrome), e.g.:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --disable-gpu --no-pdf-header-footer --virtual-time-budget=20000 \
    --print-to-pdf=assets/rocketx-business-case-en.pdf \
    deck/rocketx-business-case-en.html
  then run check_site.py again - it will catch a stale page-count claim.

Notes
-----
  Each edition uses its own market data: ECC Koeln for German, CBS for Dutch,
  INSEE, Eurostat and FEVAD for French, and dollar figures are converted at
  about 1.17 $/EUR and disclosed in the source notes. Prices appear nowhere in the PDFs by design, so they do not go
  stale; current pricing lives on the site and in the proposal.

  Fonts load from Google Fonts. Everything else is local.
