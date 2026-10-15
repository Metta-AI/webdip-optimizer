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

## A lower value margin for the pin guard (PIN_GUARD_VALUE_MARGIN 0.01 to 0.005)      sized 2026-10-15
**Mechanism:** the guard plays the plan without Sol's pins when Diplodocus rates it more than the margin higher on
16 fresh replies (castlereagh/press/service.py guarded_search).
**Read:** offline sizing only, no games. Calibration from `instruments/rank_noise.py`'s 300 phases (every pair of
candidate plans, 16-reply value gain against the gain against the others' actual orders): a 16-reply gain of 0.005
to 0.01 is worth +0.003 to +0.004 ex post, about 0.55 of the gain at every size. In v14's 56 seats, 127 guard
decisions fell in (0.005, 0.01] (2.3 a seat), so the lower margin would add about 0.008 of value a seat; v14's
dropped pins gave about twice their per-phase value as game score, so roughly +0.015 a game.
**Could see:** a 56-game paired run sees about 0.08; this is far below it.
**A next test needs:** to ride with a larger change, or a run of several hundred games; not worth one alone.

## Rank the last movement phase by the exact final score (not Diplodocus's value network)   tested 2026-10-15
**Mechanism:** Diplodocus's value network predicts our share as if the game went on; after the last movement phase
(autumn 1908) nothing follows, so the seat could rank plans by the exact score after adjudication (1 for 18 centres,
else SC² share) against Diplodocus's sampled replies (castlereagh/meta.py rank, with fastadj).
**Read:** offline only, no hosted games (`instruments/final_rank.py`, local Diplodocus server, 32 samples, 16
replies; ex post = the final score against the other powers' recorded orders, which matches results.json in 148
of 151 seats). Among Diplodocus's plans, the exact pick beats the value pick by +0.0075 ± 0.0029 a game (151 seats
of v7's league games and v13's and v14's paired run; 28 better, 111 same, 12 worse; +0.13 centres), most for large
powers (+0.015 at 14 or more centres). But the seat plays its press-guarded plan, not the raw pick: ranking that
plan beside Diplodocus's plans by the exact score, minus what the seat played, is -0.0047 ± 0.0033 for v14 (54
seats), +0.0009 ± 0.0060 for v7 (43) and +0.0205 ± 0.0083 for v13 (53, no pin guard). Blind replies miss what
press told the seat about the others' last orders.
**Could see:** about 0.006 a game at z 2 (v14's seats).
**A next test needs:** a seat that plays Diplodocus's raw pick in the last phase (no press, as when the key runs
dry), where the +0.0075 applies; for press seats, replies conditioned on press.

## Diplodocus may overrule the provinces Sol forbids outside an agreed DMZ (FORBID_GUARD)   tested 2026-10-15
**Mechanism:** the pin guard also plans without Sol's forbidden provinces that no accepted DAIDE DMZ covers, and
plays that plan when Diplodocus rates it more than 0.01 higher on 16 fresh replies (castlereagh/press/service.py
guarded_search; v17 = v15 plus FORBID_GUARD=1). Record: `experiments/2026-10-15-forbid-guard.md`.
**Read:** 56 hosted paired games against league-top5-2026-10-14 (Coworld 0.7.15): v17 minus v15 +0.055 ± 0.072 a
game, t 0.77, every game; +0.136 ± 0.081, t 1.68 in the 42 games without a wake timeout. The guard dropped forbids
3.7 times a seat; centres lost to allies fell from 0.32 to 0.16 a seat; wake timeouts 9 against 7.
**Could see:** about 0.14 a game at z 2 (paired SD 0.54).
**A next test needs:** about 96 pairs for t 1 at +0.055, planned before launch; or the variant that also drops
agreed DMZ provinces (policies commit 9dc114b alone), which frees about 96 more blocking phases of v14's 250.

