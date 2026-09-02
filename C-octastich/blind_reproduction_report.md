# Blind reproduction report (independent subagent)

Protocol: a fresh subagent was given ONLY (a) the 1834 scan, (b) the ciphertext numbers as
printed on p. 417, (c) the decoding rule — NOT the expected plaintext, and with explicit
instructions not to read this repo's derivation files and not to pattern-complete. It
extracted the 32 paragraphs itself, decoded programmatically, and visually verified every
used word index (full counts for all long indices) against high-zoom page renders.

## Result

Strict decode: 61/64 positions unambiguous, reading
`OGODUPHOLDKINGCHARUSTHESECONDAND / MAKEHIMTHESUPRWMCRULEROFTHISLAND`
with three tokenization-ambiguous positions, each resolved by the printed page:

- L1 pos 19 (para 19, idx 56): mid-line compound "church-man" as two words → "looked" → L
- L2 pos 15 (para 15, idx 20): "parol-breaking" as two words → "every" → E
- L2 pos 17 (para 17, idx 35): Latin "hinc inde" as one unit → "English" → E

The single convention "hyphenated compounds count as two words" resolves exactly the two
positions it touches and disturbs no other used index (verified exhaustively: after-ages,
life-time, time-server(s), country-men, well-principled, unlawfully-acquired all fall after
their paragraphs' used indices). "Hinc inde" as one unit is the position the vals.ai
footnote flagged.

Verdict quoted: "The rule is confirmed. … The chance of 61 exact letter matches arising
from an incorrect rule is nil."

Final plaintext, independently derived:

    O GOD UPHOLD KING CHARLS THE SECOND AND
    MAKE HIM THE SUPREME RULER OF THIS LAND

Full position-by-position table preserved below.

## Subagent's derivation tables

Line 1: 5→of(o), 3→grant(g), 27→of(o), 38→desire(d), 32→uprightness(u), 14→part(p),
21→him(h), 8→of(o), 66→latitude(l), 8→dwells(d), 70→knavish(k), 39→in(i), 5→name(n),
9→greatest(g), 12→culpable(c), 18→hitherto(h), 2→Author(a), 3→reasons(r),
56→looked(l)*, 5→Scotland(s), 1→That(t), 7→his(h), 3→exemplary(e), 2→sublime(s),
13→ease(e), 19→commerce(c), 3→overthrow(o), 25→not(n), 9→deserveth(d), 3→are(a),
16→noble(n), 6→desire(d)

Line 2: 25→much(m), 15→a(a), 13→kept(k), 6→equity(e), 11→hath(h), 20→is(i), 5→meerly(m),
1→That(t), 2→he(h), 12→expansed(e), 1→Seeing(s), 20→usually(u), 20→paid(p), 49→race(r),
20→every(e)*, 20→made(m), 35→English(e)*, 33→relished(r), 4→unwillingness(u), 6→less(l),
8→ecclesiastical(e), 35→reach(r), 5→of(o), 38→for(f), 5→the(t), 5→have(h), 18→into(i),
10→sustained(s), 3→love(l), 11→actually(a), 32→none(n), 42→duely(d)

(* = the three convention-resolved positions above)
