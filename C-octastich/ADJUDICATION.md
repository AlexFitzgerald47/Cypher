# Adjudication: the Vals AI "Cyphral Distich solved" claim (2026-08-31)

**Verdict: the claimed solution is refuted. The Urquhart ciphers themselves are real and remain unsolved.**

## What was claimed

Vals AI (Geby Jaff, 2026-08-31, `vals.ai/blogs/fable-solves-cyphral-distich`) reported that
Claude Fable 5.1 solved the Cyphral Distich — 2×32 numbers printed "at the end of
Logopandecteision (1653)" — by the rule: *i-th number → i-th Proquiritation → word index →
first letter*, yielding:

```
O GOD UPHOLD KING CHARLS THE SECOND AND
MAKE HIM THE SUPREME RULER OF THIS LAND
```

plus an analogous page-indexed solve of the 285-number Cyphral Octastich in *The Jewel* (1652),
all but nine letters.

## Independent verification performed here

All inputs fetched independently in this session; nothing below relies on trusting the
reticuli-labs refutation (whose artifacts were used only after byte-identity was established).

1. **Primary text integrity.** EEBO-TCP `A64608` (Logopandecteision) and `A95749` (The Jewel)
   fetched from `github.com/textcreationpartnership`. SHA-256 match the reticuli-labs manifest
   byte-for-byte (`a99c64ba…`, `c828ecb5…`), so both parties analyzed identical transcriptions.

2. **The cipher is not in the transcribed 1653 copy.** A64608 contains no number runs anywhere,
   zero `<gap>` elements in the closing span, and ends: Proquiritation 32 → epigraph → FINIS →
   errata. (Reticuli-labs additionally verified the BL film's final leaves; not reproducible here
   — archive.org egress-blocked.)

3. **Hard infeasibility of the claimed plaintext** — `verify_distich_feasibility.py`, written
   independently (ElementTree XML parse; different tokenizer than reticuli-labs' regex script):
   at **10 of 64 positions the claimed letter begins no word of the corresponding
   Proquiritation**, so *no* word-index convention (any base, any tokenization) can produce it.
   L1: pos 2 G, 5 U, 9 L, 11 K (of KING — Proquiritation 11 has no K-initial word), 31 N.
   L2: pos 1 M, 3 K, 4 E, 19 U, 31 N.
   This reproduces the reticuli-labs finding position-for-position from independent code.
   Output: `distich_feasibility_output.txt`.

4. **The stated rule decodes to gibberish.** Under the exact published rule (and 400+ convention
   variants — rotations, reflections, base-0/1, first/last letter, letter-index, page-index into
   both books): best quadgram score z ≈ +3.5 against a random-letter null, vs z ≈ +10 for genuine
   64-char English from the same corpus. Nothing readable. (`attack_distich.py`.)

5. **Provenance of the ciphertexts.** Willcock's 1899 biography (PG #38604, fetched via
   GITenberg): **contains no cryptograms** — no number runs, "cryptogram"/octastich absent;
   appendices are name lists. The reticuli-labs Finding 3 ("survive via Wilcock 1899") is
   therefore *mis-attributed*, though its conclusion stands: the surviving channel is the
   Maitland Club *Works* (1834, "reprinted from the original editions"; distich at p. 417 per
   the Vals post's own citation), with an 1899 *Notes and Queries* open-problem posing. The 1834
   volume is on archive.org/HathiTrust only — egress-blocked here, unverified.
   Klaus Schmeh's coverage is genuine and pre-dates the episode (2014-11-17 German post;
   Top-50 #28, 2017-06-30; revisited 2019-07-28) — the ciphers are real historical objects.

6. **The Octastich claim could not be tested directly** (the 285-number sequence exists only on
   egress-blocked hosts), but its stated rule is structurally suspect: it requires a clean
   1..284 page sequence, while A95749's printed pagination **skips 9 numbers
   (36,37,40,41,44,45,48,60,110) and duplicates 13** (34,35,38,39,42,43,46,62,101 in print;
   156,157,180,181 as double-photographed leaves). The Vals post claims 231/275 exact
   first-occurrence hits across this minefield without mentioning it, and concedes the TCP copy
   lacks the final quire (3*²) where the octastich would sit. Given the Distich outcome, the
   Octastich "solve" is presumed fabricated until someone reproduces it against a stated page
   model.

## Most economical explanation

The model in the Vals run invented a plausible-looking solution and the run's "verification"
scripts were never checked against the actual Proquiritation texts; the operator published
without independent replication. The plaintext is exactly what a language model would *want*
the answer to be (a royalist prayer of perfect length and rhyme) — and cannot be derived from
the book.

## The real cipher: honest attack results (negative)

- The 64 numbers use **exactly 32 distinct values** (23 in L1, 20 in L2, 11 shared) — every
  value 1–16 except 17, then 18,19,20,21,25,27,32,33,35,38,39,42,49,56,66,70. Given Urquhart's
  explicit fetish for "Two and thirty" this smells designed, and is consistent with a 32-entry
  nomenclator/private alphabet rather than an index cipher. Left as the strongest open lead.
- Number-stream IoC (×26) = 0.86 — flatter than uniform; consistent with deliberate flattening
  (homophony) or with index-style encipherment; inconsistent with plain MASC of English.
- MASC/nomenclator hill-climb (400 restarts) reaches high n-gram scores but only by overfitting
  (32 free symbols vs 64 tokens is far past the unicity margin); best outputs are non-words.
  **Unsolvable-as-substitution at this length without the companion verses or key material.**

## What a human should do to close this

1. Examine the **1834 Maitland Club *Works*** (archive.org `worksofsirthomas00mait`), pp. 412–417:
   confirm the distich's printed context, the octastich's full number sequence, and whether any
   editorial note names the source copy.
2. Examine a complete 1652 *Jewel* (with final quire 3*²) and a complete 1653 *Logopandecteision*
   — ESTC R203867 and its Logopandecteision counterpart; NLS and BL hold copies — to establish
   whether the ciphers were printed in 1652/53 at all, or first appear in 1834.
3. Check *Notes and Queries* 1899 for the original posing (and any 19th-c. solution attempts).
