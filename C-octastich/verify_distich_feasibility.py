#!/usr/bin/env python3
"""Independent feasibility test of the vals.ai Cyphral Distich claim.

Written independently of reticuli-labs' replicate_distich.py (their script was read
but this uses a different extraction path: XML-parse via ElementTree over regex).
Question tested: for cipher position i (1..32), the claimed method takes a word from
Proquiritation i and uses its FIRST LETTER. So the claimed plaintext letter at
position i must begin at least one word of Proquiritation i, under ANY index rule.
If it begins none, the claim is infeasible at that position regardless of convention.
"""
import re, sys, hashlib, unicodedata
import xml.etree.ElementTree as ET

PATH = sys.argv[1] if len(sys.argv) > 1 else "../sources/A64608.xml"
# Claimed plaintext (vals.ai 2026-08-31, via public X posts + refutation record):
P1 = "OGODUPHOLDKINGCHARLSTHESECONDAND"
P2 = "MAKEHIMTHESUPREMERULEROFTHISLAND"

raw = open(PATH, 'rb').read()
print("input sha256:", hashlib.sha256(raw).hexdigest())
data = raw.decode('utf-8')

# Parse XML properly. TCP P5-ish: <div type="part" n="1..32"> inside the Proquiritation section.
data_noent = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', data)
root = ET.fromstring(data_noent)

def itertext_clean(el):
    # drop <note> content? keep everything except nothing; EOLhyphen g-elements are empty tags
    return ''.join(el.itertext())

parts = {}
NS='{http://www.tei-c.org/ns/1.0}'
for div in root.iter(NS+'div'):
    if div.get('type') == 'part' and div.get('n') and div.get('n').isdigit():
        n = int(div.get('n'))
        if 1 <= n <= 32 and n not in parts:
            parts[n] = div

assert len(parts) == 32, f"found {len(parts)} parts, expected 32: {sorted(parts)}"

def words_of(div):
    txt = itertext_clean(div)
    txt = unicodedata.normalize('NFKD', txt)
    return re.findall(r"[A-Za-z][A-Za-z'æœ]*", txt)

def initials(div):
    return {w[0].upper() for w in words_of(div)}

print(f"{'pos':>3} {'#words':>6}  L1 need/ok   L2 need/ok")
inf1, inf2 = [], []
for i in range(1, 33):
    ws = words_of(parts[i]); ini = initials(parts[i])
    ok1, ok2 = P1[i-1] in ini, P2[i-1] in ini
    if not ok1: inf1.append((i, P1[i-1]))
    if not ok2: inf2.append((i, P2[i-1]))
    print(f"{i:>3} {len(ws):>6}   {P1[i-1]} {'ok' if ok1 else 'NO'}        {P2[i-1]} {'ok' if ok2 else 'NO'}")
print("\nLine1 infeasible:", inf1)
print("Line2 infeasible:", inf2)
print("total infeasible positions:", len(inf1)+len(inf2), "of 64")
