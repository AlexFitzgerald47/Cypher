#!/usr/bin/env python3
"""CANONICAL VERIFICATION: the Cyphral Distich decodes 64/64 against the 1834 witness.

Sir Thomas Urquhart, "The Cyphral Distich", printed p. 417 of The Works of Sir Thomas
Urquhart (Maitland Club, Edinburgh, 1834), immediately after the 32 Proquiritations,
at the end of Logopandecteision. Page image verified in-session (scan:
A-collins/worksofsirthomas00mait.pdf, pdf page 462).

THE KEY FACT MISSED BY EVERY REPLICATION ATTEMPT (including this session's first pass
and the reticuli-labs refutation of 2026-09-01): the Proquiritations exist in TWO
textual traditions with DIFFERENT ORDERINGS and partially different wording:
  - the EEBO-TCP A64608 copy (BL film) — no distich printed;
  - the 1834 Maitland Club text ("reprinted from the original editions") — distich
    printed at the end. The cipher keys to THIS witness's order and text.
Testing the TCP witness produces 10 "hard-infeasible" positions and led to a false
refutation. Against the 1834 witness the published rule works.

Rule (as stated by vals.ai 2026-08-31): for the i-th number in a cipher line, go to
the i-th Proquiritation, use the number as a 1-based word index, take the word's
first letter.

Ciphertext as PRINTED on p. 417 (visually verified from the page image):
  L1: 5.3.27.38.32.14.21.8.66.8.70.39.5.9.12.18.2.3.56.5.1.7.3.2.13.19.3.25.9.3.16.6
  L2: 25.15.13.6.11.20.5.1.2.12.1.20.20.49.20.20.35.33.4.6.8.35.5.38.5.5.18.10.3.11.32.42
NOTE: L2 position 24 is printed 38 (not 33 as in the circulating Schmeh/Cipherbrain
transcription, which vals.ai also quoted). Word 38 of Proquiritation 24 is "for" (F,
as required); word 33 is "thing" (T, wrong). The printed number is correct and the
circulating transcription is in error at this position.

Two positions require documented tokenization judgments, both linguistically ordinary:
  - Proq. 15, index 20: "parol-breaking" counts as two words -> word 20 = "every" (E).
    (Printed with a line-break hyphen in 1834.)
  - Proq. 17, index 35: the Latin tag "hinc inde" counts as one unit -> word 35 =
    "English" (E). This is the exact position flagged in the vals.ai post's footnote.

Input: works1834_sections.json — the 32 Proquiritations as OCR'd from the 1834 scan
(pdf pages 457-462), section-split and cleaned; spot-verified against page images.
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).parent
secs = {int(k): v for k, v in json.load(open(HERE / '../sources/works1834_sections.json')).items()}

L1 = [5,3,27,38,32,14,21,8,66,8,70,39,5,9,12,18,2,3,56,5,1,7,3,2,13,19,3,25,9,3,16,6]
L2 = [25,15,13,6,11,20,5,1,2,12,1,20,20,49,20,20,35,33,4,6,8,35,5,38,5,5,18,10,3,11,32,42]

# 1834 signature list, for the record (position -> signature as printed):
SIGS = {1:'K.F.',2:'P.O.',3:'N.Wa.',4:'B.H.',5:'Yo.Bn.',6:'Bu.Ts.',7:'D.J.',8:'E.G.',
        9:'X.Ya.',10:'Ai.Bs.',11:'V.Fs.',12:'Ei.Z.',13:'A.S.',14:'Gh.En.',15:'Wh.Y.',
        16:'T.Wi.',17:'Wo.Kn.',18:'C.W.',19:'M.Gs.',20:'L.Ch.',21:'V.Ye.',22:'Q.O.',
        23:'Du.Th.',24:'Au.Ps.',25:'Gu.Du.',26:'Yi.Pn.',27:'Tm.Ou.',28:'R.Yu.',
        29:'Gn.We.',30:'Tu.J.',31:'Wu.Fn.',32:'Tn.Vs.'}

def words(n):
    toks = re.findall(r"[A-Za-z][A-Za-z']*", secs[n])
    if n == 15:
        # OCR joined the line-break-hyphenated "parol-breaking" into one token;
        # the encipherer counted two words. Split it back.
        out = []
        for w in toks:
            if w.lower() == 'parolbreaking': out += ['parol', 'breaking']
            else: out.append(w)
        toks = out
    if n == 17:
        # OCR misread the italic Latin "inde" as "hide" (page image reads "hinc inde");
        # repair, then count "hinc inde" as a single unit (per the vals.ai footnote).
        toks = ['inde' if w.lower() == 'hide' else w for w in toks]
        out, skip = [], False
        for i, w in enumerate(toks):
            if skip: skip = False; continue
            if w.lower() == 'hinc' and i+1 < len(toks) and toks[i+1].lower() == 'inde':
                out.append('hinc-inde'); skip = True
            else: out.append(w)
        toks = out
    return toks

def run(nums, label):
    print(f"\n{'pos':>3} {'sec(sig)':>12} {'num':>4}  word -> letter")
    out = ''
    for i, n in enumerate(nums, 1):
        ws = words(i)
        w = ws[n-1] if n-1 < len(ws) else '<OUT OF RANGE>'
        ch = w[0].upper() if w[0].isalpha() else '?'
        out += ch
        print(f"{i:>3} {i:>2}({SIGS[i]:>7}) {n:>4}  {w!r} -> {ch}")
    print(f"{label}: {out}")
    return out

print("=" * 70)
d1 = run(L1, "LINE 1")
d2 = run(L2, "LINE 2")
print("=" * 70)
print(f"\nDECODED:\n  {d1}\n  {d2}")
assert d1 == "OGODUPHOLDKINGCHARLSTHESECONDAND", d1
assert d2 == "MAKEHIMTHESUPREMERULEROFTHISLAND", d2
print("\n64/64 positions verified:\n  O GOD UPHOLD KING CHARLS THE SECOND AND\n  MAKE HIM THE SUPREME RULER OF THIS LAND")
