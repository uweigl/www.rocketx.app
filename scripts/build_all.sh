#!/bin/bash
# Rebuild every generated artefact, then gate on the check suite's exit code.
# Piping check_site.py into tail hides its status, which is how a failing
# check once reached a commit.
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANGS="${LANGS:-en de es nl fr}"
python3 scripts/gen_deck.py >/dev/null
python3 scripts/gen_onepager.py >/dev/null
python3 scripts/gen_llms.py >/dev/null
python3 scripts/build_i18n_pages.py >/dev/null
python3 scripts/gen_404.py >/dev/null
python3 scripts/gen_calendar.py >/dev/null
for L in $LANGS; do
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=22000 \
    --print-to-pdf="assets/rocketx-business-case-$L.pdf" \
    "file://$PWD/deck/rocketx-business-case-$L.html" 2>/dev/null
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=18000 \
    --print-to-pdf="assets/rocketx-one-page-$L.pdf" \
    "file://$PWD/deck/rocketx-one-page-$L.html" 2>/dev/null
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=24000 \
    --print-to-pdf="assets/rocketx-calendar-$L.pdf" \
    "file://$PWD/deck/rocketx-calendar-$L.html" 2>/dev/null
done
python3 scripts/check_site.py
