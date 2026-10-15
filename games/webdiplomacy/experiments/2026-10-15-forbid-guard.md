---
id: 2026-10-15-forbid-guard
policy: scott-pidip
baseline: scott-pidip:v15
candidate: scott-pidip:v17
status: inconclusive
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
evals: [xreq_62d3a239-76fd-4871-847b-8432fb22faee, xreq_3bf32806-f721-4920-88ad-b0b50d375645, xreq_eff92380-b6a5-45c6-9aac-43d45f452ffe, xreq_613b6496-0d1b-41ea-8e18-8e87b8f37bb1, xreq_bae3df49-7162-48cf-b71b-efe2473deb01, xreq_3dc4668a-8d18-4948-bc66-316aaefbe8d4, xreq_fda13835-1b9b-4eaa-8fde-4fed599673de, xreq_38a5354d-e083-4191-aa62-8163c7884206, xreq_4f939ee5-5c4a-4c76-b769-d561a6dceab4, xreq_783fb56f-9b00-4cb0-8eb0-87375591d35f, xreq_0483f36b-132a-4123-a317-12d3c13d4598, xreq_1c017bc1-211e-40b4-bbf5-af5dee2c452b, xreq_b261abd1-4706-479c-90f8-a62c3b6c685f, xreq_9f8ba685-20cb-433a-a80c-91d0642ab4aa]
cost: >
  As v14's test: three classic-press-short health games (3.5 credits by the platform's estimate at create), then 56
  full press games against league-top5-2026-10-14 (662.6 credits by the platform's estimate at create, 11.83 a game;
  v14's run was quoted 616.5), both arms' Sol calls on Scott's OpenRouter key through the router endpoint (about
  $0.37 a seat, about $41). Scott raised the key's limit to $380 at 20:55Z ($74.81 left then).
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
search and values call (in v14's 1,203 commits the guard ran in 942; 132 more had forbids and no pin of ours, so at
most 11% more guard runs); v15's timing change is what keeps those inside the wake's deadline, so wake timeouts are
in the rule.

## Result

Scott chose this as the next paired test (card, 18:24Z on 2026-10-15); the paired run waits for him to raise the
OpenRouter key's limit ($15.85 left at 20:46Z). The baseline v15 has been the league entry since 18:27Z.

Health games: `xreq_ffc01694-223b-47a5-bc81-fc912bfd59c0`, launched 20:47Z (3 classic-press-short games, v17 beside
v15, field league-top5-2026-10-14; 3.5 credits by the platform's estimate at create; Coworld 0.7.15). Launched
before the paired run because league spend fell to about $0.4 an hour once rounds shrank to 6 games. Read 21:12Z,
all 3 completed, no taint: v17 0 rejected orders, 0 exceptions, 0 of 160 model calls failed, 2 wakes at the time
limit, 4 HTTP 400s on the context poll mid-game; v15 in the same games 0, 0, 0 of 163, 2, and 1. The forbid guard
dropped forbids in 8 of 53 commits it judged (2 of 3 games), each on a value gain over 0.01. Health passes; Scott
raised the key's limit to $380 at 20:55Z, so the paired run follows.

Paired run launched 21:14Z: 14 batches, `-n 4` (56 games), ids in `evals`, artifacts in
`.runtime/artifacts/2026-10-15-forbid-guard`.

Read 22:10Z on 2026-10-15, all 56 games finished (none failed on the platform, no deleted pods). `paired.py`,
`wd.py metrics` and `seats`, `centre_losses.py --going-in`, and the seat logs' `press_commit` and `wake_error` lines.

- **Paired, every game (the rule's read, as v14's):** v17 minus v15 **+0.055 ± 0.072 a game, t 0.77, n = 56**
  (paired SD 0.54; `--keep-tainted`). v17 in the lower slot in 28 of 56. The "exception" taint here is both arms'
  own wake timeouts, caught by the seat, not an infrastructure failure.
- **Paired, clean games only:** +0.136 ± 0.081, t 1.68, n = 42. It drops the 14 games where either seat had a wake
  timeout (v17 in 8, v15 in 7, both in 1); v17 trailed by about 0.19 a game in those 14. Dropping games on an
  outcome both arms produce selects games, so this read is not the rule's.
- **By power (8 a cell, same power against par):** v17 ahead at Turkey +0.23, France +0.14, Italy +0.14, Austria
  +0.10, Germany +0.03; behind at England -0.13 and Russia -0.12; every |z| below 1.8.
- **Mechanism:** the guard judged 1,084 commits, 490 of them with forbids, and dropped forbids in 209 (3.7 a seat;
  the prediction said 1 to 3).
- **Allies:** centres lost to a power we called an ally the year before: v17 9 (0.16 a seat), v15 18 (0.32). Centres
  lost in all, 2.57 a seat against 3.20. The retaliation the FALSE prediction named did not show.
- **Telemetry:** 0 rejected orders either arm. Failed model calls v17 0 of 4,460, v15 1 of 4,483. Wake timeouts
  (`TimeoutError: pidip agent sent no 'done' ... by its deadline`; the bridge restarts the agent and the seat plays
  on) v17 9 of 1,375 wakes in 8 games, v15 7 of 1,474 in 7, all between 21:41Z and 21:59Z (game years 1905 to
  1908; every game started together, so this is game time as much as clock time). Wakes ended at the time limit:
  v17 51, v15 58. Spend by the seat logs: v17 $0.387 a seat, v15 $0.386.

## Verdict

**Inconclusive** against Scott's bar. +0.055 a game clears +0.03, but t 0.77 over 56 pairs is below 1; the
clean-only read (+0.136, t 1.68) has 42 pairs, under 50; and wake timeouts were 9 against v15's 7 (0.65% and 0.47%
of wakes), where the rule asks for no more than v15's. v15 stays the candidate and the lever goes to
`open_levers.md`. The prediction's mechanism held (forbids dropped 3.7 times a seat) and the feared cost did not
show (fewer centres lost to allies), so the lever is not refuted.

At this estimate and SD, t 1 needs about 96 pairs, 40 more games than this run. This rule planned no extension,
so a second set would be a rule written after seeing data: write it into a new rule first, with the read on the
full total only.
