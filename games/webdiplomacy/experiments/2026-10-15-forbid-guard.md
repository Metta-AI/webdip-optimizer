---
id: 2026-10-15-forbid-guard
policy: scott-pidip
baseline: scott-pidip:v15
candidate: n/a (image pidip:hybrid-forbidguard, local merge dc5c8a0 = v15 plus policies commit 9dc114b, FORBID_GUARD=1; built, not uploaded)
status: proposed
hypothesis: >
  The hybrid scores more when Diplodocus may also overrule the provinces Sol forbids, because in v14's hosted games
  Sol forbade at least one province in 382 of our movement phases and the forbidden list blocked the plan
  Diplodocus alone rates best in 250 of them, where our played orders were worth 0.010 +/- 0.002 less after the
  phase (Diplodocus's value against the others' actual orders) than Diplodocus's plan; where the forbids did not
  block it, +0.003 +/- 0.003. v15's guard frees only our pinned orders: its free plan keeps every forbidden
  province. FORBID_GUARD (policies commit 9dc114b, castlereagh/press/service.py guarded_search) plans the free side
  without forbid_moves_into too, plays it when Diplodocus rates it more than 0.01 higher on fresh replies, and tells
  Sol in the search report which forbids it dropped.
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

# Forbid guard: Diplodocus may overrule Sol's forbidden provinces

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

**What these numbers cannot see.** A forbid is often half of a demilitarized-zone deal. Ex post is one draw of the
others' play in that phase; it does not see a neighbour retaliating later for a broken promise. Only the hosted
paired games can.

## Predictions — pre-registered

- **If TRUE we expect:** the guard drops forbids in 1 to 3 phases a seat (the press_commit `pin_guard` lines'
  `dropped_forbids`), the paired difference over v15 is +0.03 a game or more, and centres lost to powers we called
  allies (`centre_losses.py --going-in`) rise by no more than the gain.
- **If FALSE we expect:** the paired difference is within noise of 0 or below it, with more centres lost to former
  allies in the years after a dropped forbid (the retaliation the value cannot see).

## Design

One short health game (the candidate beside v15), then `run_ab.py` paired, 14 bodies x 4, against
`league-top5-2026-10-14`, as v14's test. Same router endpoint and model as v15.

Local wiring check before upload ($0, no language model): `tools/meta/fake_llm.py --forbid
BEL,HOL,DEN,SWE,NWY,RUM,SER,GRE,BUL,SPA,POR,TUN` behind the local sidecar, one seat of the candidate against six
search seats, local Diplodocus server, `end_year=1902` (`/home/user/dipwork/rankpress/forbidguard`, 15:00Z on
2026-10-15). The guard judged all 4 commits (`forbids: 12` in each `pin_guard` line) and played the free plan in
one, Autumn 1902 (free value 0.0960 against 0.0847 guarded): England ordered F NTH - DEN and F MAO - SPA/SC, both
forbidden, and the replay shows them played. The commit's search report told the agent which pins and forbids it
dropped and why. 0 rejected orders in the 3 decision lines (the last phase's orders read from the replay; the game
ended before its decision line), 0 exceptions, wakes up to 10.4 s.

Risks: the guard now also runs when Sol forbids provinces and pins nothing of ours, so more commits run its second
search and values call; v15's timing change is what keeps those inside the wake's deadline, so wake timeouts are in
the rule.

## Result

Not yet run.

## Verdict

Not yet run.
