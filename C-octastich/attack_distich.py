#!/usr/bin/env python3
"""Genuine bounded attack on the (real, unsolved) Cyphral Distich.

Ciphertext: 2 lines x 32 numbers (recorded by Klaus Schmeh/Cipherbrain; identical in
vals.ai post and reticuli-labs record).

Approach A: enumerate book-internal decoding conventions (the Urquhart-style
hypothesis family), decode, score with a quadgram model trained on the two books'
own text (17th-c English incl. Urquhart's idiolect), compare to a null distribution.

Approach B: treat the 64 numbers as nomenclator/substitution tokens; simulated-
annealing MASC solve; report best candidates with honest significance caveats.
"""
import json, math, random, re
from collections import Counter

L1 = [5,3,27,38,32,14,21,8,66,8,70,39,5,9,12,18,2,3,56,5,1,7,3,2,13,19,3,25,9,3,16,6]
L2 = [25,15,13,6,11,20,5,1,2,12,1,20,20,49,20,20,35,33,4,6,8,35,5,33,5,5,18,10,3,11,32,42]
NUMS = L1 + L2

C = json.load(open('corpus.json'))
proq = {int(k): v for k, v in C['proq'].items()}
jewel_pages = {int(k): v for k, v in C['jewel_pages'].items()}
logo_pages = {int(k): v for k, v in C['logo_pages'].items()}

# ---------- quadgram model from the books themselves ----------
def book_text():
    words = []
    for i in sorted(proq): words += proq[i]
    for d in (logo_pages, jewel_pages):
        for k in sorted(d): 
            for occ in d[k]: words += occ
    return re.sub(r"[^a-z]", "", "".join(w.lower() for w in words))

TXT = book_text()
print("LM corpus letters:", len(TXT))
Q = Counter(TXT[i:i+4] for i in range(len(TXT)-3))
TOT = sum(Q.values())
FLOOR = math.log10(0.01 / TOT)
LOGP = {g: math.log10(c / TOT) for g, c in Q.items()}
def score(s):
    s = re.sub(r"[^a-z]", "", s.lower())
    if len(s) < 4: return -999
    return sum(LOGP.get(s[i:i+4], FLOOR) for i in range(len(s)-3)) / (len(s)-3)

# null distribution for 64-letter strings drawn with English letter freqs from TXT
letters = "abcdefghijklmnopqrstuvwxyz"
lfreq = Counter(TXT)
lpop, lw = zip(*[(ch, lfreq[ch]) for ch in letters])
random.seed(42)
null = []
for _ in range(3000):
    s = "".join(random.choices(lpop, weights=lw, k=64))
    null.append(score(s))
null.sort()
import statistics
NMEAN, NSD = statistics.mean(null), statistics.pstdev(null)
def z(sc): return (sc - NMEAN) / NSD
print(f"null quadgram score mean={NMEAN:.3f} sd={NSD:.3f} max={null[-1]:.3f}")
# reference: score of actual English from the corpus
ref = [score(TXT[i:i+64]) for i in range(0, 3000*64, 64) if i+64 < len(TXT)][:200]
print(f"real-English 64-char windows: mean={statistics.mean(ref):.3f} (z={z(statistics.mean(ref)):.1f})")

# ---------- Approach A: convention grid ----------
def occ_words(d, n, which=0):
    """word list for printed page n; which selects among duplicate printed pages"""
    if n in d and which < len(d[n]): return d[n][which]
    return None

results = []
def try_conv(name, fn):
    out = []
    for i, n in enumerate(NUMS, 1):
        li = (i-1) // 32 + 1
        pos = (i-1) % 32 + 1
        ch = fn(li, pos, n)
        out.append(ch if ch else '?')
    s = "".join(out)
    known = s.replace('?', '')
    if len(known) >= 40:  # require most positions to decode
        results.append((score(known), s.count('?'), name, s))

def word_letter(ws, idx, base, last):
    j = idx - base
    if ws and 0 <= j < len(ws):
        w = ws[j]
        return (w[-1] if last else w[0]).lower()
    return None

def letter_at(ws, idx, base):
    if not ws: return None
    s = re.sub(r"[^a-z]", "", "".join(w.lower() for w in ws))
    j = idx - base
    return s[j] if 0 <= j < len(s) else None

# family 1: section = rot/reflect of position; index = number
for off in range(32):
    for refl in (0, 1):
        for base in (0, 1):
            for last in (0, 1):
                def fn(li, pos, n, off=off, refl=refl, base=base, last=last):
                    p = (32 - pos + 1) if refl else pos
                    sec = (p - 1 + off) % 32 + 1
                    return word_letter(proq.get(sec), n, base, last)
                try_conv(f"proq sec=pos rot{off} refl{refl} base{base} {'last' if last else 'first'}", fn)
# family 2: letter-index into section
for off in range(32):
    for refl in (0,1):
        for base in (0,1):
            def fn(li, pos, n, off=off, refl=refl, base=base):
                p = (32 - pos + 1) if refl else pos
                sec = (p - 1 + off) % 32 + 1
                return letter_at(proq.get(sec), n, base)
            try_conv(f"proq letteridx rot{off} refl{refl} base{base}", fn)
# family 3: swap roles — section = number (mod 32), index = position
for base in (0,1):
    for last in (0,1):
        def fn(li, pos, n, base=base, last=last):
            sec = (n - 1) % 32 + 1
            return word_letter(proq.get(sec), pos, base, last)
        try_conv(f"proq sec=num idx=pos base{base} {'last' if last else 'first'}", fn)
# family 4: pages of each book; page = number, index = position (and vice versa)
for dname, d in (("logo", logo_pages), ("jewel", jewel_pages)):
    for base in (0,1):
        for last in (0,1):
            def fn(li, pos, n, d=d, base=base, last=last):
                return word_letter(occ_words(d, n), pos, base, last)
            try_conv(f"{dname} page=num idx=pos base{base} {'last' if last else 'first'}", fn)
            def fn2(li, pos, n, d=d, base=base, last=last):
                k = pos if li == 1 else 32 + pos
                return word_letter(occ_words(d, k), n, base, last)
            try_conv(f"{dname} page=globalpos idx=num base{base} {'last' if last else 'first'}", fn2)
# family 5: per-line restart on pages: page = pos (line2 also pos), idx = num
for dname, d in (("logo", logo_pages), ("jewel", jewel_pages)):
    for base in (0,1):
        def fn(li, pos, n, d=d, base=base):
            return word_letter(occ_words(d, pos), n, base, 0)
        try_conv(f"{dname} page=pos idx=num base{base} first", fn)

results.sort(reverse=True)
print(f"\n=== Approach A: {len(results)} scored conventions; top 15 ===")
for sc, q, name, s in results[:15]:
    print(f"z={z(sc):+5.1f} ?={q:2d} {name:48s} {s}")

# ---------- Approach B: substitution/nomenclator ----------
# 64 tokens; distinct symbols:
syms = sorted(set(NUMS))
print(f"\n=== Approach B ===\ndistinct symbols: {len(syms)} over 64 tokens")
cnt = Counter(NUMS)
print("most common:", cnt.most_common(8))
# IoC of the number stream
N = len(NUMS)
ioc = sum(c*(c-1) for c in cnt.values()) / (N*(N-1)) * 26
print(f"IoC (x26): {ioc:.2f}  (English MASC ~1.7x26/26≈1.73; flat homophonic ->26/len)")
# MASC hill-climb: map each distinct symbol to a letter, maximize quadgram score
best_overall = (-999, None, None)
for restart in range(400):
    random.seed(1000+restart)
    m = {s: random.choice(letters) for s in syms}
    cur = score("".join(m[n] for n in NUMS))
    for it in range(2000):
        s1 = random.choice(syms); old = m[s1]; m[s1] = random.choice(letters)
        ns = score("".join(m[n] for n in NUMS))
        if ns >= cur: cur = ns
        else: m[s1] = old
    if cur > best_overall[0]:
        best_overall = (cur, dict(m), "".join(m[n] for n in NUMS))
sc, m, txt = best_overall
print(f"MASC hill-climb best: z={z(sc):+.1f}")
print("L1:", txt[:32]); print("L2:", txt[32:])
print("NOTE: 64 tokens is far below unicity distance for 47-symbol substitution;")
print("a high z here does NOT validate a solve — it must read as a meaningful distich.")
