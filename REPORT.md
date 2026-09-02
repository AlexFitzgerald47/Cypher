# REPORT — Unsolved-cipher hunt, 2026-09-02

## BLUF

**The mission's premise was false, and proving that is the headline result.** The Vals AI
"Fable 5.1 solved the Cyphral Distich" claim (2026-08-31) — the result this task was built
on — **does not replicate and is refuted from primary sources**: the claimed plaintext is
hard-impossible at 10 of 64 positions against the actual text of Urquhart's 32
Proquiritations, and the cipher isn't even printed in the transcribed 1653 book. The
Urquhart ciphers themselves are real and remain unsolved; my own bounded attack on the
genuine Distich came back clean-negative, with one new structural lead. Workstream B
(Powers cryptogram) produced a solid partial: it is an abbreviated dedication, not a
cipher, with the type established quantitatively and ~10 of 32 entries anchored.
Workstream A (Collins Papers) was environmentally blocked — this session's network
egress allows GitHub and package registries only — so it ships as a verified-premise
survey plus a validated, ready-to-run pipeline. No solve is claimed anywhere; nothing
was manufactured.

A hard environmental note up front: `vals.ai`, `scienceblogs.de`, `archive.org`,
`militaryarchives.ie`, HathiTrust, Gutenberg, and every other content host were
egress-blocked. Everything below was built from GitHub-hosted primary sources
(EEBO-TCP XMLs, a GITenberg mirror of Willcock 1899, the reticuli-labs artifact cache)
plus server-side web-search snippets. Every input is cached under `sources/` with
hashes logged.

---

## Workstream C — Urquhart (ran first; it adjudicates the premise)

**Status: the Vals solution is REFUTED; the real ciphers are OPEN.**
Full detail: `C-octastich/ADJUDICATION.md`; scripts `verify_distich_feasibility.py`,
`attack_distich.py`, outputs alongside.

- Independently fetched EEBO-TCP A64608 (*Logopandecteision*, 1653) and A95749 (*The
  Jewel*, 1652); SHA-256 byte-identical to the files used by the independent
  reticuli-labs refutation (so both analyses ran on the same text, fetched separately).
- **My own code** (different parser and tokenizer from reticuli-labs') reproduces their
  central finding position-for-position: at positions L1 {2,5,9,11,31} and L2
  {1,3,4,19,31} the claimed letter (G,U,L,K,N / M,K,E,U,N) **begins no word of the
  corresponding Proquiritation** — no word-index convention can yield "O GOD UPHOLD KING
  CHARLS…". Proquiritation 11 contains no K-initial word at all; "KING" is unspellable.
- The stated rule itself, plus 408 convention variants (rotations, reflections, bases,
  first/last letter, letter-index, page-index into both books), never exceeds quadgram
  z≈+3.5 vs z≈+10 for genuine English of the same length. Gibberish throughout.
- Provenance: the ciphers do not appear in the TCP transcriptions of either 1652/53 book,
  nor anywhere in Willcock's 1899 biography (checked in full — this also corrects the
  reticuli-labs claim that Willcock is the survival channel). The surviving channel is
  the Maitland Club *Works* (1834), per the Vals post's own citation (p. 417) — on
  egress-blocked hosts, unverified here. Klaus Schmeh's coverage (2014/2017/2019) is
  genuine; the ciphers are real open problems.
- The Octastich "solve" could not be tested directly (the 285-number sequence exists only
  on blocked hosts) but its stated rule assumes a clean 1..284 pagination; the actual
  *Jewel* skips 9 printed page numbers and duplicates 13, which the Vals account never
  mentions. Presumed fabricated pending someone reproducing it against a stated page model.
- Genuine attack on the real Distich (negative, honestly logged): number-stream IoC×26 =
  0.86 (flattened — consistent with homophony or indexing, not plain MASC); substitution
  hill-climbing overfits at this length (64 tokens, 32 symbols) and yields non-words.
  **New structural observation**: the 64 numbers use **exactly 32 distinct values** —
  given Urquhart's explicit "no number like Two and thirty" flourish, a 32-entry
  nomenclator table is the strongest open hypothesis. The companion verses (uncollected
  here) and the 1834 printing are the missing key material.

**Confidence**: refutation — high (two independent codebases, identical primary text,
hash-verified; the one unavoidable reliance is TCP's transcription fidelity, which
reticuli-labs spot-checked against the BL film). Octastich fabrication — inferred, not
proven.

**Human next step**: pull the 1834 Maitland Club *Works* (archive.org
`worksofsirthomas00mait`), pp. 412–417, for the distich's printed context and the
octastich's numbers; check a complete 1652 *Jewel* (final quire 3*²; ESTC R203867) and
*Notes & Queries* 1899.

---

## Workstream B — The Powers cryptogram (Schmeh #22)

**Status: PARTIAL.** Full detail: `B-powers/FINDINGS.md`; script `analyze_powers.py`.

- Ciphertext (32 triplets, `RLS CMW DJP RFP J?O … JSB SDG`) verified identical across
  three independent quotations of Schmeh's record.
- **It is not a cipher; it is 32 sets of person-initials** (an abbreviated dedication):
  all three `?` fall in the middle slot (no letter cipher loses exactly the middle
  symbol); 94% of first letters are common given-name initials; **8 triplets end in P**
  (p≈10⁻⁴ if random) matching the documented Powers family — father **R**ichard
  **F**ranklin **P**owers = RFP exactly, mother Donna (née Belik) = DJP adjacent, and
  Powers is the fourth of five children. JSB SDG closes the list exactly as Bach signed
  his scores (*Soli Deo Gloria*). Codon and amino-acid-code readings are computationally
  dead (no triplet is ACGTU-only; none is an aa code).
- Prior art credited: Schmeh (2015/2017) recorded the initials hypothesis; a *Notes on
  Contemporary Literature* article (Gale A159331538) proposed RLS = Robert L. Schneider
  (Powers's Illinois teacher) and sibling readings (PJP/MEP/BJP/REP/RCP). Powers
  reportedly said the dedication "can be broken using a codex found in the final third
  of the book."
- 22 of 32 identities remain open. This is prosopography now, not cryptanalysis: the
  plaintext is not recoverable from the ciphertext alone (initials are lossy), only from
  the book's final-third list or from Powers.

**Human next step**: a copy of the 1991 Morrow edition (final third — find the name
list/codex), the NCL article in full, and/or a letter to Powers (draft below).

---

## Workstream A — The Collins Papers (1918–22 IRA GHQ)

**Status: NO ACCESS — pipeline delivered.** Full detail: `A-collins/STATUS.md`.

- Premise verified by search: the corpus (6,000+ despatches, incl. intelligence series
  IE-MA-CP-05/06) is online and free; no published cryptanalytic pass exists for
  1918–22 (Gillogly & Mahon 2008 = the 1926–36 Twomey papers; Richard Bean closed their
  residue in 2019). In-period cipher use is documented (captured Mulcahy papers, BMH
  statements).
- militaryarchives.ie is egress-blocked here; no document could be fetched, so **no
  ciphertext was obtained and none is claimed**.
- Delivered instead: `crawl_collins.py` (catalogue crawler + descriptor cipher-term
  flagging), `triage_ocr.py` (OCR + four-way triage: pairs / targets / key sheets /
  plain), `attack_toolkit.py` (key-replay first, then columnar hill-climb, Playfair SA,
  Vigenère — with GHQ crib vocabulary). Columnar and Vigenère attacks validated on
  synthetic GHQ-style traffic in-session (exact recovery).

---

## Given another day

1. **Re-run workstream A from an unrestricted network.** It remains the highest-upside
   target; the pipeline is ready and the first hour would answer whether digitized
   ciphertext survives in the Collins Papers.
2. Pull the 1834 *Works* octastich numbers and run the page-model test against A95749
   under every defensible pagination convention — that definitively settles the second
   half of the Vals claim and might genuinely open the octastich (the real one).
3. Collect the Urquhart companion verses (1834 printing) and test the 32-value
   nomenclator lead on the Distich.
4. Powers: obtain the book; check the final third for the codex.

---

## Draft disclosure notes

### To Klaus Schmeh (Cipherbrain)

> Subject: Vals AI "Cyphral Distich solved" claim — refutation from primary sources
>
> Klaus — the 2026-08-31 vals.ai claim that Claude Fable 5.1 solved Urquhart's Cyphral
> Distich (your Top-50 #28) does not replicate. Against the EEBO-TCP transcription of
> Logopandecteision (A64608), the claimed plaintext is impossible at 10 of 64 positions:
> the required letter begins no word of the corresponding Proquiritation under any word-index
> convention (e.g. the K of "KING": Proquiritation 11 contains no K-initial word). The
> distich is also absent from the end of the transcribed 1653 copy. An independent
> replication (reticuli-labs, 2026-09-01, github.com/reticuli-labs/panel-artifacts)
> reaches the same result from different code; I verified both on hash-identical primary
> text with a third implementation. One correction to the record: Willcock 1899 contains
> neither cryptogram (checked in full text) — the survival channel appears to be the
> Maitland Club Works (1834), p. 417, which I could not access. If you can post the
> octastich numbers from your 2017 transcription (and Kent Ramliden's counts), the
> analogous page-index claim for The Jewel can be tested mechanically — the 1652 book's
> printed pagination skips 9 numbers and duplicates 13, which the claim silently ignores.
> Scripts and derivations: [repo link].

### To Military Archives Ireland — only if/when workstream A produces results

> Subject: Systematic survey of enciphered material in the Collins Papers
>
> A Chairde — I am running a systematic cryptanalytic survey of the digitized Collins
> Papers (1918–22) for enciphered despatches, in the spirit of Mahon & Gillogly's
> *Decoding the IRA* (which covered the 1926–36 Twomey papers). Before publishing any
> recovered plaintext I will share results with the Archives, and will withhold anything
> naming individuals or locations not already in the published record. Could you confirm
> whether the digitization captured any cipher annexes or key sheets catalogued
> separately from the despatch files (esp. IE-MA-CP-05/06)?

*(Not sent — nothing was produced; retained for when the crawl runs.)*

### To Richard Powers (via publisher/agent)

> Subject: The Gold Bug Variations dedication — a partial reading, seeking confirmation
>
> Dear Mr. Powers — the encrypted dedication of The Gold Bug Variations is listed among
> Klaus Schmeh's top unsolved cryptograms. Analysis strongly supports 32 sets of
> person-initials: the three question marks fall only in middle position, eight triplets
> end in P (your parents Richard Franklin and Donna Powers as RFP/DJP, plus siblings),
> and JSB SDG closes the list as Bach closed his scores. You reportedly said it can be
> broken with a codex in the final third of the book. Would you be willing to confirm
> the reading, or simply confirm which in-book list is the codex? A short confirmation
> would let the cryptographic record close a 35-year-old entry.

---

## Repository map

```
WORKLOG.md                  — timestamped decisions and dead ends
sources/                    — cached primary sources (hashes in WORKLOG/ADJUDICATION)
C-octastich/                — adjudication + verification + attack (Urquhart)
B-powers/                   — findings + analysis script (Powers)
A-collins/                  — status + crawl/triage/attack pipeline (Collins Papers)
```
