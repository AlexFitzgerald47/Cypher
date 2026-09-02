# Workstream A — The Collins Papers hunt

**Status: NO ACCESS (network egress). Premise verified; target corpus confirmed to exist and
to be unworked; crawl/triage/attack pipeline delivered ready-to-run for an unrestricted
environment.**

## What was established (via server-side search only; militaryarchives.ie is egress-blocked
from this session, as are archive.org, UCD digital, and every non-GitHub content host)

1. **The corpus exists and is online.** The Collins Papers: 6,000+ documents, 1918–early 1922,
   despatches between IRA GHQ (Collins, Mulcahy, Brugha, O'Sullivan) and Brigade/Battalion
   officers; file copies of outgoing plus received originals. Series IE-MA-CP-05 and
   IE-MA-CP-06 cover intelligence 1920–22. Free online since the Decade of Centenaries
   release.
2. **The premise of the hunt holds.** Gillogly & Mahon's *Decoding the IRA* (2008) attacked
   the UCD **Twomey papers, 1926–36** (columnar transposition dominant; ~300 encrypted
   documents; the residue was closed by Richard Bean in 2019 — Schmeh's Top-25 #4 marked
   solved 2019-08-08). No equivalent published cryptanalytic pass over the **1918–22**
   GHQ corpus was found in any search performed here.
3. **Ciphered material almost certainly exists in-period**: British raids (e.g., on Mulcahy's
   papers, 1920) captured "IRA codes and dispatches"; BMH witness statements discuss cipher
   use; GHQ circulars prescribed communication security. Whether the *digitized Collins
   Papers* include surviving ciphertext (vs. only decodes/plaintext file copies) could not be
   verified without site access — this is the first thing the crawler answers.

## Honest statement

No ciphertext was obtained, so no cryptanalysis was performed. Per the mission rule: nothing
was manufactured. The blocking condition is purely environmental (egress allowlist:
GitHub + package registries only).

## Pipeline delivered (this folder)

- `crawl_collins.py` — polite crawler for the Collins Papers online collection (and the
  Civil War Captured Documents / BMH when pointed at them): walks the catalogue, saves
  descriptor metadata, downloads PDFs, flags descriptor hits for
  cipher/cypher/code/key/undecipherable/Playfair/transposition, and samples non-hit files.
- `triage_ocr.py` — OCR (tesseract) + triage into (a) ciphertext-with-decrypt pairs,
  (b) ciphertext-only targets, (c) key sheets/instructions, using regexes for cipher blocks
  (letter-group runs, number-group runs, "in cypher", "decode(d)", key tables).
- `attack_toolkit.py` — the attacks staged for what Collins-era GHQ is likely to have used:
  keyword columnar transposition hill-climb (line lengths 8–15 first, per Gillogly's
  1920s findings), Playfair simulated annealing with English + Irish-proper-noun scoring,
  Vigenère via IoC/Kasiski; crib list preloaded ("O/C", "Adjt", "G.H.Q.", "Bde", "Dublin",
  "arms", "ammunition", "Chief of Staff", brigade names, month names).
  Key-reuse doctrine: recover keys from any (a)-class pair first and replay across the
  brigade/week before any blind attack.

Run order: `crawl_collins.py --index-url <collection url>` → `triage_ocr.py downloads/` →
`attack_toolkit.py triage/targets/`.

## What a human (or an unrestricted session) does next

1. Run the crawler against
   `https://www.militaryarchives.ie/en/online-collections/the-collins-papers-1917-1922`
   plus the Civil War Captured Documents series and the BMH.
2. If descriptor search yields zero cipher hits, sample ~200 PDFs across brigades/months
   anyway — catalogue descriptions are routinely silent about ciphertext.
3. Report results to Military Archives (contact via militaryarchives.ie) before publishing
   anything that names people/safe houses not already in the published record.

## Validation

`attack_toolkit.py` smoke-tested in-session: columnar round-trip exact; blind hill-climb
recovered a 91-letter GHQ-style synthetic plaintext exactly (7 columns, keyword MUNSTER);
Vigenère period/key recovery exact (key EIRE). `english_quadgrams.txt` generated from the
locally cached Willcock 1899 text (342k letters) — replace with a larger modern corpus table
when available. Playfair SA is standard but was not smoke-tested (compute budget).
