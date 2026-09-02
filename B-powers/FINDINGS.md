# Workstream B — The Powers cryptogram (Schmeh Top-50 #22)

**Status: PARTIAL — cryptogram type established beyond reasonable doubt; ~10 of 32 entries
identified with documentary support; full mapping requires the book's final third or Powers
himself. This is not a cipher; it is an abbreviated dedication.**

## Ciphertext (verified)

32 letter-triplets, printed as the dedication page of Richard Powers, *The Gold Bug
Variations* (Morrow, 1991); transcription identical across three independent quotations of
Klaus Schmeh's record (Cipherbrain 2015-04-19 DE, 2017-08-27 EN Top-50 #22, and The Modern
Novel's page — all retrieved via search snippets; the sites themselves are egress-blocked here):

```
RLS CMW DJP RFP J?O CEP JJN PRG
ZTS MCJ JEH BLM CRR PLC JCM MEP
JNH JDM RBS J?H BJP PJP SCB TLC
KES REP RCP DTH I?H CRB JSB SDG
```

(printed as four lines of eight; `?` = a missing middle character in triplets 5, 20, 29)

## Type determination (analyze_powers.py)

1. **Every `?` sits in the middle slot** (5: J?O, 20: J?H, 29: I?H). No letter-level cipher
   loses exactly the middle symbol of a group; a list of people whose middle initials the
   author didn't know (or who lack middle names) does exactly this.
2. **First-slot letters are given-name initials**: 94% fall in {J,R,M,D,C,K,S,T,B,P}; J alone
   appears 8×. Middle-slot is flat. Last-slot clusters like surnames.
3. **The family cluster is decisive.** 8 of 32 triplets end in P
   (P(≥8) ≈ 1×10⁻⁴ if last letters were random surnames): DJP, RFP, CEP, MEP, BJP, PJP, REP,
   RCP. Documented: Powers's father was **Richard Franklin Powers = RFP exactly**; his mother
   **Donna Powers (née Belik) = DJP** adjacent at position 3; Powers is the **fourth of five
   children** (two older sisters, an older brother, a younger brother) — parents + five
   siblings ≈ the P-cluster.
4. **JSB SDG at positions 31–32** = Johann Sebastian Bach + *Soli Deo Gloria* — the exact
   double signature Bach wrote at the end of his scores. The dedication closes the way Bach
   closed the Goldberg manuscript. (JSB long recognized; the SDG reading makes the pair a
   closing doxology rather than two dedicatees.)
5. **Genetic readings are dead on arrival**: no triplet is composed of A/C/G/T/U only; none
   matches an amino-acid three-letter code. The codon look is typographic homage, not mechanism.

## Prior art (credit where due)

- Klaus Schmeh (2015, 2017) recorded the ciphertext and the initials hypothesis (incl.
  DJP/RFP = parents, JSB = Bach).
- An article in *Notes on Contemporary Literature* ("Deciphering the code in Richard Powers's
  The Gold Bug Variations", Gale doc A159331538; full text egress-blocked here, recovered via
  snippets) proposed **RLS = Robert L. Schneider**, the University of Illinois teacher
  (1954–88) who, per Powers's Paris Review interview, convinced him literature was "the
  perfect place for someone who wanted the aerial view" — and sibling readings PJP
  (Patricia/"Peggy"), MEP (Maureen), BJP (Bob), REP/RCP (Robert) Powers.
- Powers has reportedly said the dedication "can be broken using a codex found in the final
  third of the book" (via Schmeh's record; primary source unverified here).
- Luc Herman & Geert Lernout treat the 32 groups as a "motto" (unsolved) in the academic
  literature.

## What this session adds

- Independent triple-verification of the transcription; quantification of the initials
  evidence (items 1–3 above); elimination of codon/amino-acid mechanisms; the SDG-doxology
  structural reading; documentary anchoring of RFP (father's full name) and the
  family-cluster arithmetic.
- Candidate consistent with the novel's subject worth checking: **RLS = Robert Louis
  Sinsheimer** (molecular biologist) is *formally* possible but the Schneider identification
  fits Powers's documented "personal landmarks" practice better.
- **J?O**: initials pattern-match the novel's own narrator **Jan O'Deigh** (no middle name —
  she is fictional), and Powers based the librarian character partly on one of his sisters.
  A self-referential dedicatee would be very Powers. Speculative; flagged, not claimed.

## What remains open (22 of 32)

CMW, CEP*, JJN, PRG, ZTS, MCJ, JEH, BLM, CRR, PLC, JCM, JNH, JDM, RBS, J?H, SCB, TLC, KES,
DTH, I?H, CRB (*CEP is P-final but no sibling name is documented for it).

## How a human closes this

1. Open a copy of the 1991 Morrow edition; in the final third look for the "codex" Powers
   mentioned — a passage listing full names (an in-novel acknowledgments; plausibly around
   the "Today in History" register or Jan's year-end lists). Map the 32 triplets against it.
2. Cross-check the *Notes on Contemporary Literature* article (Gale A159331538) in full.
3. Ask Powers. He is alive, answers scholarly mail, and confirmed the thing is breakable.
   Draft disclosure letter is in `../REPORT.md`.
