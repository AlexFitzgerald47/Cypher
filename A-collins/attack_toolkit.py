#!/usr/bin/env python3
"""Attack toolkit for 1918-22 IRA GHQ ciphertexts (run on triage/targets/*.txt).

Systems staged per Gillogly & Mahon's findings for the 1920s IRA (columnar transposition
with keyword keys dominant; Playfair and Vigenere secondary), which is the best prior for
Collins-era practice. Order of operations:
  1. replay: try every key in keys.txt (recovered from (a)-class pairs) on every target —
     keys were reused across a brigade for weeks.
  2. columnar: shotgun hill-climb over column counts 5-15 (Gillogly: line lengths 8-15 first).
  3. playfair: simulated annealing, English quadgrams + Irish-proper-noun bonus.
  4. vigenere: IoC period estimate + per-column frequency fit.
Scoring uses English quadgrams with a crib bonus for GHQ vocabulary.
"""
import argparse, itertools, math, pathlib, random, re
from collections import Counter

CRIBS = ["OC", "ADJT", "GHQ", "BDE", "BATT", "DUBLIN", "CORK", "ARMS", "AMMUNITION",
         "CHIEFOFSTAFF", "VOLUNTEER", "BRIGADE", "COLUMN", "RIFLES", "ENEMY", "RAID",
         "DESPATCH", "REPORT", "JANUARY", "FEBRUARY", "MARCH", "APRIL", "JUNE", "JULY"]

# --- quadgram model: expects english_quadgrams.txt ("ABCD 12345" lines) beside script;
# falls back to a small built-in model good enough for ranking.
def load_quadgrams():
    p = pathlib.Path(__file__).with_name('english_quadgrams.txt')
    q = {}
    if p.exists():
        for line in p.read_text().splitlines():
            g, c = line.split(); q[g] = int(c)
    else:  # minimal fallback from common English tetragrams
        common = """TION1000 THER900 NTHE800 THAT750 OFTH700 FTHE690 THES680 WITH660
        INTH650 ATIO630 OTHE560 TTHE530 DTHE520 INGT510 ETHE500 SAND490 STHE480 HERE460
        THEC450 MENT430 THEM420 RTHE410 THEP400 FROM390 THIS380 TING370 THEI360 NGTH350
        IONS340 ANDT330 EDTH320 OUGH300 ANCE290 COMP280 EMEN270""".split()
        for tok in common:
            q[tok[:4]] = int(tok[4:])
    tot = sum(q.values())
    floor = math.log10(0.01 / tot)
    return {g: math.log10(c / tot) for g, c in q.items()}, floor

QUAD, FLOOR = load_quadgrams()
def score(s):
    s = re.sub(r'[^A-Z]', '', s.upper())
    if len(s) < 8: return -1e9
    base = sum(QUAD.get(s[i:i+4], FLOOR) for i in range(len(s) - 3)) / (len(s) - 3)
    bonus = sum(0.05 for c in CRIBS if c in s)
    return base + bonus

# --- columnar transposition
def columnar_decrypt(ct, key_order):
    n = len(key_order); L = len(ct); rows = L // n; extra = L % n
    lens = [rows + (1 if i < extra else 0) for i in range(n)]  # fill by key order
    cols = {}; i = 0
    for k in sorted(range(n), key=lambda j: key_order[j]):
        cols[k] = ct[i:i + lens[k]]; i += lens[k]
    out = []
    idx = [0] * n
    for r in range(rows + (1 if extra else 0)):
        for c in range(n):
            if idx[c] < len(cols[c]):
                out.append(cols[c][idx[c]]); idx[c] += 1
    return ''.join(out)

def crack_columnar(ct, max_cols=15, restarts=60, iters=4000):
    best = (-1e9, None, None)
    for n in range(5, max_cols + 1):
        for _ in range(restarts):
            order = list(range(n)); random.shuffle(order)
            cur = score(columnar_decrypt(ct, order))
            for _ in range(iters):
                a, b = random.sample(range(n), 2)
                order[a], order[b] = order[b], order[a]
                ns = score(columnar_decrypt(ct, order))
                if ns >= cur: cur = ns
                else: order[a], order[b] = order[b], order[a]
            if cur > best[0]:
                best = (cur, n, order[:])
    return best

# --- Playfair (simulated annealing)
def pf_decrypt(ct, sq):
    pos = {ch: divmod(i, 5) for i, ch in enumerate(sq)}
    out = []
    for i in range(0, len(ct) - 1, 2):
        a, b = ct[i], ct[i+1]
        ra, ca = pos[a]; rb, cb = pos[b]
        if ra == rb: out += [sq[ra*5 + (ca-1) % 5], sq[rb*5 + (cb-1) % 5]]
        elif ca == cb: out += [sq[((ra-1) % 5)*5 + ca], sq[((rb-1) % 5)*5 + cb]]
        else: out += [sq[ra*5 + cb], sq[rb*5 + ca]]
    return ''.join(out)

def crack_playfair(ct, restarts=40, iters=20000):
    ct = re.sub(r'[^A-Z]', '', ct.upper()).replace('J', 'I')
    if len(ct) % 2: ct = ct[:-1]
    alpha = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
    best = (-1e9, None)
    for _ in range(restarts):
        sq = list(alpha); random.shuffle(sq)
        cur = score(pf_decrypt(ct, sq)); T = 0.2
        for it in range(iters):
            a, b = random.sample(range(25), 2)
            sq[a], sq[b] = sq[b], sq[a]
            ns = score(pf_decrypt(ct, sq))
            if ns > cur or random.random() < math.exp((ns - cur) / max(T, 1e-9)):
                cur = ns
            else:
                sq[a], sq[b] = sq[b], sq[a]
            T *= 0.9997
        if cur > best[0]: best = (cur, ''.join(sq))
    return best

# --- Vigenere
def crack_vigenere(ct, max_period=12):
    ct = re.sub(r'[^A-Z]', '', ct.upper())
    EN = [8.2,1.5,2.8,4.3,12.7,2.2,2.0,6.1,7.0,0.15,0.77,4.0,2.4,6.7,7.5,1.9,0.095,6.0,6.3,9.1,2.8,0.98,2.4,0.15,2.0,0.074]
    def chi(col, shift):
        c = Counter((ord(ch) - 65 - shift) % 26 for ch in col); n = len(col)
        return sum((c.get(i, 0)/n*100 - EN[i])**2 / EN[i] for i in range(26))
    best = (-1e9, None, None)
    for p in range(1, max_period + 1):
        key = ''
        for i in range(p):
            col = ct[i::p]
            key += chr(65 + min(range(26), key=lambda s: chi(col, s)))
        pt = ''.join(chr((ord(c) - 65 - (ord(key[i % p]) - 65)) % 26 + 65) for i, c in enumerate(ct))
        sc = score(pt)
        if sc > best[0]: best = (sc, key, pt[:120])
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('targets', help='dir of OCR .txt files (triage/targets)')
    ap.add_argument('--keys', default='keys.txt', help='recovered keys to replay first')
    a = ap.parse_args()
    for f in sorted(pathlib.Path(a.targets).glob('*.txt')):
        raw = f.read_text()
        # extract the densest letter-group block as ciphertext
        blocks = re.findall(r'(?:\b[A-Z]{3,5}\b[ .,\n]*){6,}', raw)
        if not blocks:
            print(f'{f.name}: no ciphertext block found'); continue
        ct = re.sub(r'[^A-Z]', '', max(blocks, key=len))
        print(f'\n== {f.name} ({len(ct)} letters) ==')
        kp = pathlib.Path(a.keys)
        if kp.exists():
            for key in kp.read_text().split():
                order = sorted(range(len(key)), key=lambda i: (key[i], i))
                pt = columnar_decrypt(ct, order)
                if score(pt) > -3.5:
                    print(f'  KEY REPLAY HIT [{key}]: {pt[:100]}')
        sc, n, order = crack_columnar(ct)
        print(f'  columnar best (cols={n}, score={sc:.2f}): {columnar_decrypt(ct, order)[:100]}')
        sc, sq = crack_playfair(ct)
        print(f'  playfair best (score={sc:.2f}, square={sq}): {pf_decrypt(ct.replace("J","I"), sq)[:100]}')
        sc, key, pt = crack_vigenere(ct)
        print(f'  vigenere best (key={key}, score={sc:.2f}): {pt}')

if __name__ == '__main__':
    main()
