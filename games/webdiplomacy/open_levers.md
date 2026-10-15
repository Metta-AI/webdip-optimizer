# Tested, no result yet — webDiplomacy

Levers that were built and measured and ended **inconclusive**: |z| < 2, so
neither confirmed nor refuted. They are not closed, and `closed_levers.md` is the
wrong place for them (it holds only what the numbers killed). They are listed here
because an experiment record that ends "inconclusive" otherwise leaves no trace
where the next proposal looks, and the next agent proposes the same idea again.

Read this file with `closed_levers.md` before proposing anything. An entry here
tells you two things about a new idea in the same family:

- **A prior on the size.** Size the new test for the effect the last one showed
  (`tools/sizing.py --effect`), or do not run it.
- **What a second try must add.** A stronger dose of the same lever is a fair
  test only with a reason to expect a larger effect. Several small readings of
  the same sign, each inside the noise, are not that reason: three same-sign
  results at |z| < 1 happen by chance one time in four.

This file ships with no entries: an entry is one lab's measurement against one
field. Add your own when a record closes inconclusive; move an entry to
`closed_levers.md` when a later test refutes it, and delete it when one confirms it.

Format (the block below is an example of the fields, not an entry):

```
## <lever name>                                    tested YYYY-MM-DD
**Mechanism:** <what the change was, and the setting or code location>
**Read:** <the measured difference with n, SE and z, the field set, and whether the mechanism fired>
**Could see:** <the smallest effect that run could have shown>
**A next test needs:** <what would make another run worth its games>
```

---

## Luna for press wakes, with the spend squeeze, at a $0.50 cap        tested 2026-10-15
**Mechanism:** scott-pidip v6: press wakes on `openai/gpt-6-luna`, phase starts on Sol, governor budget read
from the sidecar's `GET /spend` (the "Spend per game" thread's branch at 658d18b).
**Read:** v6 minus v5 -0.052 a game, SE 0.043, z -1.2, 47 clean pairs against `league-top5-2026-10-14`,
every seat capped at $0.50. The mechanism fired: v5 was refused from turn 7 in all 49 seats; v6 spent $0.24.
Record `experiments/2026-10-14-v6-luna-press-at-050.md`.
**Could see:** about 0.09 at z = 2.
**A next test needs:** a version that spends near the cap with Sol's commit detail (v6 fixed orders in 59% of
phases against v5's 89%), or a reason to expect late-game press to matter more than this field shows.

## v9's lighter press on the Diplodocus hybrid                       tested 2026-10-15
**Mechanism:** the hybrid with v9's press (no call or wake limits, update briefings, keep-starts governor with the
phase-start cost curve, `GOVERNOR_RESERVE_USD=0.02`) instead of v7's squeeze (call limit 4, 3 wakes, 20 to 40 s
debounce, notes, deals and history sections).
**Measured:** v11 minus v10 -0.001 ± 0.051 a game, z -0.01, n = 67 pairs against `league-top5-2026-10-14`;
v11 spent $0.477 a seat against $0.393 and went over $0.50 in 15 of 70 seats
(`2026-10-15-v11-hybrid-lighter-press`).
**A second try must add:** a reason the extra press spend changes orders when Diplodocus already ranks them; and a
governor that holds $0.50 on a route the platform does not cap.


## More sampled replies when Diplodocus ranks our plans (META_RANK_SAMPLES 16 to 64)    tested 2026-10-15
**Mechanism:** the seat plays the plan Diplodocus's value network rates best, averaged over META_RANK_SAMPLES
sampled replies of the others (castlereagh/meta.py values). More replies lower the noise in each plan's value.
**Read:** offline only, no hosted games (`instruments/rank_noise.py` on 300 movement phases of v14's paired run,
local Diplodocus server, 13.1 distinct plans a phase). Two independent 16-reply rankings pick the same plan in
178 of 300 phases, but where they differ the two picks are 0.002 apart (median) in 64-reply value. Picking on 64
replies instead of 16: -0.0006 ± 0.0010 a phase ex post (value after the phase against the others' actual
orders); 32 replies: -0.0004 ± 0.0007. Ranking itself pays: the 16-reply pick beats the average candidate by
+0.0078 ± 0.0013. A 64-reply values call took 12.6 s against 3.7 s (median, local CPU).
**Could see:** about 0.002 a phase at z 2.
**A next test needs:** a reason to expect value noise costs games (it did not show here), and room on the
endpoint for 3.4 times the values time; not worth hosted games on this read.

## More of Diplodocus's sampled plans as candidates (META_SEEDS 32 to 64)            tested 2026-10-15
**Mechanism:** the seat ranks our power's distinct plans among META_SEEDS sampled joint actions
(castlereagh/meta.py); more samples give more candidates.
**Read:** offline only, no hosted games (`instruments/seed_count.py` on 300 movement phases of v14's paired run,
local Diplodocus server). 32 samples gave 13.4 distinct plans, 64 gave 19.0; ranked on one 16-reply values call,
the pick changed in 47 of 300 phases and was worth +0.0006 ± 0.0005 a phase ex post (value after the phase
against the others' actual orders). The samples call doubles and the values call grows about 40%.
**Could see:** about 0.001 a phase at z 2.
**A next test needs:** a cheaper endpoint, or a reason the extra plans matter more than this read shows; not worth
hosted games on it.
