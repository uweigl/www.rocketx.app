RocketX site
============

Layout
------
  index.html                  the site (English). All copy for all three
                              languages lives in the I18N object near the
                              bottom; the language selector swaps it in place.
  de/index.html               pre-rendered German page   ) generated - do not
  es/index.html               pre-rendered Spanish page  ) edit by hand
  assets/                     images, video, favicons, og-image, the PDFs
  deck/                       source HTML for the business-case PDFs (generated)
  scripts/                    build and check tooling
  robots.txt, sitemap.xml     crawler directives, incl. named AI crawlers
  site.webmanifest            PWA / home-screen metadata

After editing index.html
------------------------
  python3 scripts/build_i18n_pages.py    regenerate de/ and es/
  python3 scripts/check_site.py          verify everything still holds

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
  The German edition of the deck uses German market data (ECC Koeln), not the
  US figures. Prices appear nowhere in the PDFs by design, so they do not go
  stale; current pricing lives on the site and in the proposal.

  Fonts load from Google Fonts. Everything else is local.
