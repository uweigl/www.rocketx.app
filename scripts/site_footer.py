# -*- coding: utf-8 -*-
"""The site footer for the auxiliary pages - identical by construction.

Instead of imitating the homepage footer, this module extracts it: the real
<footer class="site"> markup and its CSS rules are read from index.html and
transformed per language at build time. Whatever the homepage footer looks
like, the auxiliary pages look the same, because they are the same - with the
JavaScript behaviour (language-aware hrefs, per-market contact, gated legal
links) resolved statically for one language.
"""
import io, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRIV = {"en": "privacy", "de": "de/datenschutz", "es": "es/privacidad",
        "nl": "nl/privacy", "fr": "fr/confidentialite"}
TRUST = {"en": "trust", "de": "de/sicherheit", "es": "es/seguridad",
         "nl": "nl/beveiliging", "fr": "fr/securite"}
WA = {"en": ("https://wa.me/18294997677", u"+1 (829) 499-7677"),
      "de": ("https://wa.me/4986774099628", u"08677 / 4099628")}

_SRC = io.open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
_I18N = json.loads(re.search(r"const I18N=(\{.*?\});\n", _SRC, re.S).group(1))
_FOOT = re.search(r'<footer class="site">.*?</footer>', _SRC, re.S).group(0)

# every stylesheet rule that styles the footer or the pieces it uses
_RULES = []
for _m in re.finditer(r"[^{}]*\{[^{}]*\}", _SRC):
    _r = _m.group(0)
    _sel = _r.split("{", 1)[0]
    if ("footer.site" in _sel
            or _sel.strip() in (".logo", ".logo img", ".sep")):
        _RULES.append(_r.strip())
# the footer depends on environment the homepage provides globally: the wrap
# metrics and the --display variable. Scope copies of both to the footer so the
# auxiliary pages render it identically, whatever their own containers do.
_WRAP = re.search(r"\n\.wrap\{([^}]*)\}", _SRC).group(1)
_DISP = re.search(r"--display:([^;]*);", _SRC).group(1)
CSS = ("\n".join(_RULES)
       + "\nfooter.site .wrap{%s}" % _WRAP
       + "\nfooter.site{--display:%s}" % _DISP
       + "\nfooter.site a{color:inherit;text-decoration:none}")


def footer_html(lang, with_style=True):
    d = _I18N[lang]
    f = _FOOT

    # resolve every data-i18n text the footer carries
    def put_i18n(m):
        key = m.group(1)
        val = d.get(key, _I18N["en"].get(key, ""))
        return m.group(0).split(">", 1)[0].replace(
            ' data-i18n="%s"' % key, "") + ">" + val + "<"
    f = re.sub(r'<(?:span|a)[^>]*data-i18n="([\w.]+)"[^>]*>[^<]*<',
               lambda m: put_i18n(m), f)

    # language-aware hrefs the homepage sets with JavaScript
    f = f.replace('href="privacy/"', 'href="/%s/"' % PRIV[lang])
    f = f.replace('href="/trust/"', 'href="/%s/"' % TRUST[lang])
    f = re.sub(r'href="assets/rocketx-calendar-[a-z]+\.pdf"',
               'href="/assets/rocketx-calendar-%s.pdf"' % lang, f)
    f = f.replace('src="assets/logo.png"', 'src="/assets/logo.png"')
    f = f.replace('href="#top"', 'href="%s"' % ("/" if lang == "en" else "/%s/" % lang))

    # gated legal links: keep only the one this language owns, visible
    if lang == "de":
        f = f.replace("<a data-impressum hidden ", "<a data-impressum ")
    else:
        f = re.sub(r'<a data-impressum hidden[^>]*>[^<]*</a>', "", f)
    if lang == "fr":
        f = f.replace("<a data-mentions hidden ", "<a data-mentions ")
    else:
        f = re.sub(r'<a data-mentions hidden[^>]*>[^<]*</a>', "", f)

    # per-market contact: resolve the WhatsApp config statically
    if lang in WA:
        href, txt = WA[lang]
        f = re.sub(r'href="https://wa\.me/\d+"', 'href="%s"' % href, f)
        f = re.sub(r'<span class="wanum">[^<]*</span>',
                   '<span class="wanum">%s</span>' % txt, f)
        f = f.replace(' data-wa hidden', ' data-wa').replace(" data-wa ", " ")
        f = f.replace('<span class="sep" aria-hidden="true" data-wa> ',
                      '<span class="sep" aria-hidden="true"> ')
    else:
        f = re.sub(r'<a[^>]*data-wa[^>]*>.*?</a>', "", f, flags=re.S)
        f = re.sub(r'<span class="sep"[^>]*data-wa[^>]*>[^<]*</span>', "", f)

    # loading tweaks that only make sense on the long homepage
    f = f.replace(' loading="lazy" decoding="async"', "")

    style = ("<style>" + CSS + "</style>") if with_style else ""
    return style + f
