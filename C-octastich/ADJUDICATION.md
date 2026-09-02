# Adjudication: the Vals AI "Cyphral Distich solved" claim (2026-08-31)

**FINAL VERDICT: the Vals solution is CORRECT — verified 64/64 against the distich-bearing
witness. The public refutation (reticuli-labs, 2026-09-01) and this session's own first-pass
"refutation" were both wrong, for an instructive reason: two textual traditions of the
Proquiritations exist, with different orderings and partially different wording, and every
replication attempt tested the wrong one.**

This file supersedes the earlier version of this adjudication (preserved in git history at
commit 13fb67f), which concluded "refuted." The reversal is documented step by step in
WORKLOG.md; the decisive evidence arrived when the 1834 Maitland Club scan was added to the
repo and its Proquiritations were compared against EEBO-TCP.

## The two witnesses

| | EEBO-TCP A64608 (BL film copy, 1653) | Maitland Club *Works* 1834, pp. 412–417 |
|---|---|---|
| Distich printed? | **No** — Proq. 32 → epigraph → FINIS | **Yes** — p. 417, after Proq. 32, with companion verse |
| Proquiritation order | its own | **different permutation** (e.g. TCP #7 "K.F." is 1834 #1; TCP #23 is 1834 #2) |
| Wording | variant | variant (e.g. TCP1 "…not in his life-time be neglected by the State…" vs 1834 #13 "…shall not in his life-time have his just demands denied by that authority…") |

The 1834 edition prints "from the original editions" — its source copy of Logopandecteision
carried both the distich and this ordering. The permutation mapping between witnesses was
established by the paragraph signatures (each Proquiritation is signed with initials:
K.F., P.O., N.Wa., …), independently of any plaintext hypothesis.

## Why the refutations failed

The reticuli-labs replication (and this session's first pass, from independent code) tested
the published rule against the **TCP** ordering and text, and correctly found the claimed
plaintext infeasible at 10 of 64 positions there — including "no K-initial word in
Proquiritation 11." All of that is true **of the wrong witness**. Under the 1834 ordering,
position 11 is the "V.Fs." paragraph (TCP #8), whose word 70 is "knavish" — supplying the K
of KING. The infeasibility argument was sound arithmetic on unsound premises.

## The verified solution

Rule (exactly as Vals stated): *i-th number → i-th Proquiritation (1834 order) → 1-based
word index → first letter.*

```
O GOD UPHOLD KING CHARLS THE SECOND AND
MAKE HIM THE SUPREME RULER OF THIS LAND
```

`verify_distich_1834.py` prints the full 64-position derivation
(`distich_1834_verification.txt`); 62/64 positions decode with a plain tokenizer, and the
final two resolve with ordinary, documented judgments:

- **L2 pos 15** (Proq. 15, index 20): "parol-breaking" counts as two words → "every" (E).
- **L2 pos 17** (Proq. 17, index 35): Latin "hinc inde" counts as one unit → "English" (E)
  — the precise position the Vals post's footnote flagged.

Additionally, one **printed-number correction to the circulating record**: L2 position 24 is
printed **38** on p. 417 (page image verified), not 33 as in the Schmeh/Cipherbrain
transcription that Vals quoted. Word 38 of Proq. 24 is "for" (F, required); word 33 is
"thing" (T). The printed book is right and the transcription is wrong. (Note: this means the
Vals post quoted an input containing an error its own claimed plaintext contradicts —
sloppy presentation, but immaterial to the solve's correctness.)

Blind reproduction: a subagent given only the scan, the printed numbers, and the rule — not
the expected plaintext — independently derived the same message (61/64 strict, 64/64 under
the hyphen-compound convention + "hinc inde" unit) and judged the rule confirmed:
`blind_reproduction_report.md`. It also identified a third convention-resolved position
this file's first draft passed over silently (L1 pos 19: "church-man" as two words →
"looked" → L), because the canonical script's tokenizer splits hyphenated compounds by
default — the same single convention resolving all of L1-19 and L2-15.

## Historical note

The cipher self-describes accurately: "For if upon this Cyphral Distich look / An honest
skilful man, he'll therein finde / His own heart's wishes, and the Author's minde." A
royalist prayer for Charles II, printed in 1653 London under the Commonwealth — a treasonable
sentiment Urquhart could only publish enciphered. The odd pseudo-initials signing each
Proquiritation (Wh.Y., X.Ya., Ei.Z., …) remain unexplained — they are not needed for the
decode, and may be a second layer or a red herring; flagged as an open question.

## What remains open

1. **The Cyphral Octastich** (285 numbers, *The Jewel* 1652): present in NEITHER the TCP
   copy of the Jewel (A95749) NOR anywhere in the 1834 Works (searched in full — the only
   number run in 470 pages is the distich). Its ciphertext survives via Schmeh's record,
   whose source remains unlocated; given the distich outcome, the analogous Vals page-index
   solve is now plausible but must be tested against the right witness — first find the
   printing that carries it, then establish which pagination it keys to.
2. **Which 1653 issue carried the distich**: the TCP/BL copy lacks it; the 1834 editors'
   source copy had it. A census of surviving Logopandecteision copies (ESTC) would locate
   the variant issue.
3. The signature initials (64 tokens across 32 signatures) — meaning unknown.
