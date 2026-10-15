---
id: 2026-10-15-forbid-guard
policy: scott-pidip
baseline: scott-pidip:v15
candidate: scott-pidip:v17
status: proposed
hypothesis: >
  The hybrid scores more when Diplodocus may also overrule the provinces Sol forbids on its own, because in v14's
  hosted games Sol forbade at least one province in 382 of our movement phases and the forbidden list blocked the plan
  Diplodocus alone rates best in 250 of them, where our played orders were worth 0.010 +/- 0.002 less after the
  phase (Diplodocus's value against the others' actual orders) than Diplodocus's plan; where the forbids did not
  block it, +0.003 +/- 0.003. v15's guard frees only our pinned orders: its free plan keeps every forbidden
  province. FORBID_GUARD (policies commits 9dc114b and e0f964f, castlereagh/press/service.py guarded_search) plans
  the free side without the forbidden provinces that no accepted DAIDE DMZ covers, plays it when Diplodocus rates it
  more than 0.01 higher on fresh replies, and tells Sol in the search report which forbids it dropped. Provinces in
  an accepted DMZ stay forbidden: in 120 of the 250 blocking phases Diplodocus's plan entered only forbids with no
  agreed DMZ (-0.010 +/- 0.003 a phase), in 96 only agreed DMZ provinces (-0.007 +/- 0.003).
decision_rule: >
  Scott's release bar against the current candidate: the forbid guard is put to Scott for entry iff it minus v15 is
  at least +0.03 a game with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected orders,
  failed calls no higher than v15's in the same games, wake timeouts no more than v15's, and a clean health game.
  Entry needs Scott's explicit go-ahead naming the version. Otherwise v15 stays the candidate and the lever goes to
  open_levers.md (inconclusive) or closed_levers.md (refuted, below -0.03 with t at least 1).
evals: []
cost: >
  As v14's test: one classic-press-short health game, then 56 full press games against league-top5-2026-10-14,
  both arms' Sol calls on Scott's OpenRouter key through the router endpoint (about $0.37 a seat, about $41) and
  the platform's estimate at create (about 80 to 190 credits). The key had $26 left at 12:41Z and v7's league games
  draw about $2.5 an hour, so this waits for Scott to raise the key's limit.
artifacts: []
---

# Forbid guard: Diplodocus may overrule the provinces Sol forbids on its own

## Context

Records checked: `closed_levers.md`, `open_levers.md` and `best_practices.md` say nothing about forbidden
provinces; v14 (`2026-10-15-v14-value-pin-guard`, confirmed, +0.132 a game over v13) freed pinned orders and
kept forbids; v15 (`2026-10-15-v15-guard-timing`) only moved the guard's timing.

`instruments/plan_regret.py` on v14's 56 hosted games (`.runtime/artifacts/2026-10-15-v14-value-pin-guard`, the
382 movement phases whose committed policy forbade a province; local Diplodocus server, 32 samples, 16 replies
ex ante, the others' actual orders ex post):

| Phases | Played minus Diplodocus alone, ex ante | Ex post | SE (ex post) |
|---|---|---|---|
| Diplodocus's best plan moves into a forbidden province (250) | -0.0192 | -0.0102 | 0.0021 |
| Forbids do not block it (132) | -0.0026 | +0.0029 | 0.0029 |
| 1 to 2 forbids (113) | -0.0065 | -0.0014 | 0.0030 |
| 3 or more forbids (269) | -0.0164 | -0.0075 | 0.0021 |

Of the 250 blocking phases, 162 (2.9 a seat) have an ex ante gap above the guard's 0.01 threshold, and there
Diplodocus's plan was worth 0.015 +/- 0.003 more ex post; in the other 88, 0.001. The same instrument put v13's
pin loss at -0.0047 a phase with 3 or more pins and v14's at -0.0017, and v14 then gained +0.132 a game, so a
per-phase value gap is a lower bound on the game effect, not an estimate of it.

**What these numbers cannot see.** A forbid is often half of a demilitarized-zone (DMZ) deal. Ex post is one draw of
the others' play in that phase; it does not see a neighbour retaliating later for a broken promise. Only the hosted
paired games can.

**Which forbids cost the value** (a rerun with the plan's forbidden provinces recorded, 2026-10-15 16:00Z: 247 of
382 phases block Diplodocus's plan, -0.0094 +/- 0.0023, the first run's number within noise). An accepted DMZ here
is any DAIDE `YES (PRP ...)` with a DMZ clause, either way, in our seat's press up to that phase; 54% of the
forbidden provinces were in one. Deals made in plain English are not seen, so "not agreed" is an upper bound.

| Diplodocus's plan enters | Phases | Ex post | SE | Guard would fire (ex ante gap > 0.01) |
|---|---|---|---|---|
| only forbids with no agreed DMZ | 120 | -0.0104 | 0.0032 | 80 |
| only agreed DMZ provinces | 96 | -0.0066 | 0.0034 | 52 |
| both | 31 | -0.0141 | 0.0079 | 25 |
| no forbidden province | 135 | +0.0036 | 0.0022 | 15 |

So the candidate drops only the forbids no accepted DMZ covers: it frees the 120 phases (and part of the 31) at no
broken promise. Dropping agreed DMZs too (9dc114b alone) would also free the 96, at the cost the value cannot see;
that variant is one line away if this one confirms. The other side keeps these deals: in the same 56 seats our
roster logged 379 accepted DMZs and 11 breaches of one (`talker_breach`), so our side of a DMZ buys something.

## Predictions — pre-registered

- **If TRUE we expect:** the guard drops forbids in 1 to 3 phases a seat (the press_commit `pin_guard` lines'
  `dropped_forbids`), the paired difference over v15 is +0.03 a game or more, and centres lost to powers we called
  allies (`centre_losses.py --going-in`) rise by no more than the gain.
- **If FALSE we expect:** the paired difference is within noise of 0 or below it, with more centres lost to former
  allies in the years after a dropped forbid (the retaliation the value cannot see).

## Design

v17 (`652c80f2-e4d6-4895-a2cd-52e26364022d`, uploaded 16:15Z) is image `pidip:hybrid-dmzguard`: local merge
`c255277` = v15 plus policies commits `9dc114b` and `e0f964f`, `FORBID_GUARD=1`, otherwise v15's settings.

One short health game (the candidate beside v15), then `run_ab.py` paired, 14 bodies x 4, against
`league-top5-2026-10-14`, as v14's test. Same router endpoint and model as v15.

Local wiring checks before upload ($0, no language model). First, 9dc114b alone: `tools/meta/fake_llm.py --forbid
BEL,HOL,DEN,SWE,NWY,RUM,SER,GRE,BUL,SPA,POR,TUN` behind the local sidecar, one seat of the candidate against six
search seats, local Diplodocus server, `end_year=1902` (`/home/user/dipwork/rankpress/forbidguard`, 15:00Z on
2026-10-15). The guard judged all 4 commits (`forbids: 12` in each `pin_guard` line) and played the free plan in
one, Autumn 1902 (free value 0.0960 against 0.0847 guarded): England ordered F NTH - DEN and F MAO - SPA/SC, both
forbidden, and the replay shows them played. The commit's search report told the agent which pins and forbids it
dropped and why. 0 rejected orders in the 3 decision lines (the last phase's orders read from the replay; the game
ended before its decision line), 0 exceptions, wakes up to 10.4 s. Then the candidate image, same setup with
`end_year=1903` (`/home/user/dipwork/rankpress/dmzguard`, about 16:10Z): the guard judged 6 commits and played the free
plan in 2, 0 rejected orders in 14 decision lines, 0 exceptions. No seat there makes DAIDE deals, so the agreed-DMZ
path is covered by `tests/test_talker.py` (the roster records PIE and TYS from an accepted DMZ), not by the game.

Risks: the guard now also runs when Sol forbids provinces and pins nothing of ours, so more commits run its second
search and values call; v15's timing change is what keeps those inside the wake's deadline, so wake timeouts are in
the rule.

## Result

Not yet run.

## Verdict

Not yet run.
