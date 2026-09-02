# WORKLOG

## 2026-09-02T19:50Z — Session start
- Repo empty; created workstream folders A-collins, B-powers, C-octastich, sources/.
- Plan: read Vals post + Schmeh #28 first (C context), Schmeh #22 (B), then crawl Military Archives catalogue (A). C is most tractable (pure computation vs EEBO-TCP); A is highest upside but crawl-heavy; B needs the exact ciphertext first.

## 2026-09-02T~20:05Z — Workstream C pivots to adjudication
- Network policy: only GitHub raw + package registries reachable. vals.ai, scienceblogs.de, web.archive.org, militaryarchives.ie, quod.lib.umich.edu, gutenberg.org, cipherbrain.de ALL egress-blocked. WebSearch (server-side) works.
- Fetched EEBO-TCP A64608 (Logopandecteision 1653) + A95749 (The Jewel 1652) from textcreationpartnership GitHub. sha256 of both matches the manifest in reticuli-labs/panel-artifacts distich-refutation (independent fetch, byte-identical).
- INDEPENDENT CHECK 1: neither TCP text contains any long number run; A64608 has zero <gap> elements in the final span; the Cyphral Distich is NOT printed at the end of Logopandecteision per TCP.
- INDEPENDENT CHECK 2 (verify_distich_feasibility.py, own code, ElementTree path): the claimed plaintext "O GOD UPHOLD KING CHARLS..." is HARD-INFEASIBLE at 10/64 positions — the needed letter begins no word of the corresponding Proquiritation (L1: pos 2 G, 5 U, 9 L, 11 K, 31 N; L2: pos 1 M, 3 K, 4 E, 19 U, 31 N). Matches reticuli-labs finding position-for-position.
- VERDICT so far: the 2026-08-31 Vals "solve" does not replicate against the primary text. Workstream C reframed: adjudicate fully (incl. Octastich), then treat the REAL Urquhart ciphers as the open target.
- Next: obtain the 285-number Octastich sequence (Cipherbrain blocked; try HN Algolia API, X, Willcock 1899 mirrors on GitHub), verify The Jewel pagination claims, check the 5 'duplicate page' gaps in A95749.

## 2026-09-02T~20:15Z — Provenance established; B ciphertext recovered
- Willcock 1899 (PG #38604, fetched via GITenberg mirror `Sir-Thomas-Urquhart-of-Cromartie-Knight_38604`): contains NO cryptograms, no number runs, no "Notes and Queries" — refutation's Finding 3 mis-attributes the survival channel. Likely true channel: Works of Sir Thomas Urquhart, Maitland Club 1834 ("reprinted from the original editions"), Proquiritations pp.412-417, distich p.417 (per Vals citation). 1834 Works only on archive.org/HathiTrust — egress-blocked, cannot verify directly.
- Schmeh's Urquhart entries are genuine + pre-2026: 2014-11-17 "Wer knackt dieses verschlüsselte Distichon?", 2017-06-30 Top50 #28, 2019-07-28 revisited. The ciphers are real open problems; only the Vals SOLUTION is refuted.
- Reconciling hypothesis for all absences: distich/octastich sat on final leaves/quires present in only some copies (Vals itself says TCP Jewel copy lacks final quire 3*2); 1834 editors had complete copies. Untestable here without page images (all image hosts blocked).
- The Jewel pagination (A95749): printed numbers 1..284 but 9 numbers skipped (36,37,40,41,44,45,48,60,110) and 13 duplicated (34,35,38,39,42,43,46,62,101,+scan-dups 156,157,180,181). Any "word index into page k" decode must state how it handles this; Vals post silent => additional strike against the Octastich claim. Octastich numbers themselves unobtainable under egress policy (needed: 1834 Works p.[?] or Schmeh transcription).
- B: Powers cryptogram ciphertext recovered via two independent search snippets, identical: 32 triplets "RLS CMW DJP RFP J?O CEP JJN PRG ZTS MCJ JEH BLM CRR PLC JCM MEP JNH JDM RBS J?H BJP PJP SCB TLC KES REP RCP DTH I?H CRB JSB SDG" (?'s = unknown middle letters at triplets 5,20,29). Powers (per Schmeh record): "can be broken using a codex found in the final third of the book". Herman & Lernout call it a "motto". Prior hypotheses: initials of names; DJP+RFP = parents Donna/Richard Powers; JSB=Bach; SDG=Soli Deo Gloria.

## 2026-09-02T~20:45Z — A and B closed out
- B: ciphertext triple-verified via snippets; typology QUANTIFIED (all '?' middle-slot; 94% name-initial first letters; 8x P-final cluster p~1e-4; RFP = Richard Franklin Powers exact; JSB+SDG = Bach's score signature). Prior art found: NCL article (Gale A159331538) had proposed RLS=Robert L. Schneider + sibling readings — my work is verification/quantification, not first discovery. Codon/aa readings eliminated computationally. Status PARTIAL.
- A: premise verified (no published pass on 1918-22; Gillogly/Mahon=1926-36, Bean closed 2019). Site egress-blocked; delivered crawl/OCR-triage/attack pipeline instead; columnar+vigenere crackers validated on synthetics. Status NO ACCESS.
- Next: REPORT.md, disclosure drafts, commit, push.
