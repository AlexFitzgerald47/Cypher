#!/usr/bin/env python3
"""Structural analysis of the Powers cryptogram (encrypted dedication, The Gold Bug
Variations, 1991). Ciphertext verified identical across three independent quotations
of Schmeh's record (2015 DE post, 2017 EN post, Modern Novel page - via search snippets).
"""
import math
from collections import Counter

CT = "RLS CMW DJP RFP J?O CEP JJN PRG ZTS MCJ JEH BLM CRR PLC JCM MEP JNH JDM RBS J?H BJP PJP SCB TLC KES REP RCP DTH I?H CRB JSB SDG"
T = CT.split()
print("triplets:", len(T))
assert len(T) == 32

# 1) '?' distribution — cipher vs initials discriminator
qpos = [(i+1, t.index('?')) for i, t in enumerate(T) if '?' in t]
print("'?' occurrences (triplet#, char-slot 0/1/2):", qpos)
print("-> all '?' in middle slot: consistent with unknown/absent MIDDLE names;")
print("   no letter-substitution cipher would lose exactly the middle symbol.")

# 2) positional letter statistics
for slot, name in [(0,'first'),(1,'middle'),(2,'last')]:
    c = Counter(t[slot] for t in T if t[slot] != '?')
    print(f"{name}-slot: {dict(c.most_common())}")

# First-slot should match US given-name initial frequencies if initials.
# Rough US given-name initial distribution (1950s-80s cohorts, SSA top names):
# J,R,M,D,C,K,S,T dominate. Observed first-slot:
first = Counter(t[0] for t in T)
common_name_initials = set('JRMDCKSTBP')
frac = sum(v for k, v in first.items() if k in common_name_initials) / 32
print(f"share of first letters in common given-name initials JRMDCKSTBP: {frac:.0%}")

# 3) Family-cluster arithmetic (documented: father Richard Franklin Powers,
#    mother Donna Powers nee Belik, author is 4th of 5 children)
pfinal = [(i+1, t) for i, t in enumerate(T) if t[2] == 'P']
print("P-final triplets:", pfinal)
print(f"count={len(pfinal)}; Powers nuclear family (2 parents + 5 children) = 7;")
print("RFP matches father 'Richard Franklin Powers' EXACTLY (position 4);")
print("DJP adjacent at position 3 matches mother Donna (middle init. unconfirmed).")

# binomial: P(>=8 of 32 triplets end in 'P') if last letters ~ US surname initials
# US surname initial freq for P ~ 4.8% (census-derived approximation)
p = 0.048
from math import comb
tail = sum(comb(32,k) * p**k * (1-p)**(32-k) for k in range(len(pfinal), 33))
print(f"P(>= {len(pfinal)} P-final | random surnames): {tail:.2e}  -> strong family cluster")

# 4) closing signature
print("\npositions 31-32: JSB SDG = 'Johann Sebastian Bach, Soli Deo Gloria' —")
print("SDG is precisely how Bach signed his scores; a closing doxology, not a person.")

# 5) codon-reading sanity check (for completeness): can triplets be codons?
bases = set('ACGTU')
codonish = [t for t in T if set(t.replace('?','A')) <= bases]
print("\ntriplets composed only of A/C/G/T/U letters:", codonish, "-> codon reading dead on arrival")

# 6) amino-acid 3-letter code check
aa3 = {'ALA','ARG','ASN','ASP','CYS','GLN','GLU','GLY','HIS','ILE','LEU','LYS','MET','PHE','PRO','SER','THR','TRP','TYR','VAL'}
print("triplets matching amino-acid 3-letter codes:", [t for t in T if t in aa3])
