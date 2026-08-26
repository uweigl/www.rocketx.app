# -*- coding: utf-8 -*-
"""Score DE/ES/NL copy against each market's own doctrine of forceful prose."""
import io, re, json, sys, os
os.chdir(os.path.expanduser("~/Downloads/rocketx-site3"))

s = io.open("index.html", encoding="utf-8").read()
I = json.loads(re.search(r'const I18N=(\{.*?\});\n', s, re.S).group(1))

def strip(t):
    t = re.sub(r'<[^>]+>', '', str(t))
    return re.sub(r'&[a-z]+;|&#\d+;', ' ', t)

def sents(t):
    return [x.strip() for x in re.split(r'(?<=[.!?])\s+', t) if len(x.split()) > 2]

# --- Schneider: the Substantivstil is the enemy; verbs and short main clauses win
NOM = re.compile(r'\b\w{4,}(ung|ungen|heit|keit|tion|tionen|ismus|nahme|barkeit)\b', re.I)
PASS = re.compile(r'\b(wird|werden|wurde|wurden)\b\s+(?:\w+\s+){0,4}\w+(?:t|en)\b', re.I)
# --- Grijelmo: borrowed words and hollow abstractions drain the connotation
ANGL = re.compile(r'\b(performance|workflow|engagement|feedback|target|core|meeting|'
                  r'business|pipeline|dashboard|marketplace|retail|partner|deal)\b', re.I)
VAC_ES = re.compile(r'\b(soluci[oó]n(?:es)?|optimizaci[oó]n|sinergia|robusto|potente|innovador[a]?|'
                    r'l[ií]der|integral|eficiencia|experiencia de usuario)\b', re.I)
# --- Renkema: bondigheid, and the tangconstructie he explicitly warns about
LOAN_NL = re.compile(r'\b(performance|workflow|engagement|feedback|dashboard|business|'
                     r'solution|challenge|target|team-?lead|manager|tooling)\b', re.I)

def audit(lang, items):
    rows = []
    for k, v in items:
        t = strip(v)
        ws = t.split()
        if len(ws) < 6 or k.endswith(".src") or k in ("dg.alt","dg.lead") or ".q" in k:
            continue  # citations, alt text and quotes are not style targets
        ss = sents(t)
        longest = max((len(x.split()) for x in ss), default=0)
        avg = sum(len(x.split()) for x in ss) / float(len(ss) or 1)
        score, why = 0, []
        if lang == "de":
            n = len(NOM.findall(t))
            p = len(PASS.findall(t))
            dens = n / float(len(ws)) * 100
            # the rule is about sentences, not noun-phrase labels
            if dens > 8 and len(ws) >= 14: score += dens - 8; why.append("%.0f%% nominal" % dens)
            if p: score += p * 4; why.append("%d passive" % p)
            if longest > 22: score += (longest - 22) * 1.4; why.append("%dw sentence" % longest)
            cm = max((x.count(",") for x in ss), default=0)
            if cm >= 3: score += (cm - 2) * 3; why.append("%d commas" % cm)
        elif lang == "es":
            a = len(ANGL.findall(t)); vv = len(VAC_ES.findall(t))
            if a: score += a * 5; why.append("%d anglicism" % a)
            if vv: score += vv * 4; why.append("%d vague" % vv)
            if longest > 26: score += (longest - 26) * 1.3; why.append("%dw sentence" % longest)
        else:
            lo = len(LOAN_NL.findall(t))
            if lo: score += lo * 5; why.append("%d loanword" % lo)
            if longest > 20: score += (longest - 20) * 1.6; why.append("%dw sentence" % longest)
            if avg > 17: score += (avg - 17) * 1.5; why.append("avg %.0fw" % avg)
        if score > 0:
            rows.append((score, k, ", ".join(why), t[:112]))
    rows.sort(reverse=True)
    return rows

for lang in ("de", "es", "nl"):
    rows = audit(lang, sorted(I[lang].items()))
    print("\n===== SITE %s — %d flagged =====" % (lang.upper(), len(rows)))
    for sc, k, why, t in rows[:12]:
        print("  %5.1f  %-11s %-28s %s" % (sc, k, why, t))
