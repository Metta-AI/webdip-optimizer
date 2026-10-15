---
id: 2026-10-15-v11-hybrid-lighter-press
policy: scott-pidip
baseline: scott-pidip:v10
candidate: scott-pidip:v11
status: inconclusive
hypothesis: >
  The hybrid scores more with v9's lighter press than with v7's squeeze because v7 left about $0.11 of its $0.50
  a seat unspent (mean $0.388, max $0.459) under its call and wake limits (PRESS_REQUEST_LIMIT=4,
  PRESS_MAX_WAKES=3, debounce 20 to 40 s), while v9's press has no call or wake limits and its keep-starts
  governor (castlereagh/press/governor.py, GOVERNOR_KEEP_STARTS) spends the cap on press only while every later
  phase start stays covered; v9 with this press beat v5 by +0.076 a game (z 1.5, 54 pairs).
decision_rule: >
  Scott's release bar (pidip README, wave 2) against the current champion: v11 replaces v10 (or v7 if v10 does not
  land) iff v11 minus the baseline is at least +0.03 a game with t at least 1 over 50 or more clean paired games
  (paired.py), with 0 rejected orders, failed calls no higher than the baseline's in the same games (the platform's
  502s make the bar's 1% unreachable for any version; Scott entered v7 at 7.9%), spend at most $0.50 a seat by its
  governor's count, and a clean health game. Scott's direction (relayed 06:20Z on 2026-10-15): keep improving
  over the next 12 hours; his go-ahead for entries was "keep going with the follow ups with any fixes then land
  those asap once done". Otherwise the baseline stays and the press lever is recorded.
evals: [xreq_649ef829-0886-4f7b-bda7-bc762c147cd8, xreq_ad4afac1-7634-46f9-bbdf-f7d087ed02b2, xreq_cd4ed978-3528-4cc9-a81b-c0368843eca8, xreq_5b1d367c-456e-4283-8cfa-f77bf705c2f4, xreq_233e062e-37aa-468c-a741-9e96fec27cb1, xreq_f31b490b-7a4e-4646-aec7-ac08ba41ea6d, xreq_1bc985a2-799f-4bc3-8271-f5c32a6fcfc0, xreq_83683fe4-b887-44c1-b2bf-0a5a66a1de61, xreq_bb6ab88a-2840-4db2-a20f-13f66d175c36, xreq_f1a5a7ea-2bcb-417e-8662-b6308661a53c, xreq_2a219bdd-db3d-4efe-bc90-2af81a1cf1dd, xreq_90bbc7ed-5322-4cdf-90a0-43c393063bc5, xreq_4e0eb03e-65b2-4226-aea5-c0ea2bd49ee3, xreq_5897dfac-d964-421b-ba05-98de78de6333]
cost: 70 full press games (-n 5, 14 bodies) at a $0.50 cap; both arms' Sol calls bill to Scott's OpenRouter key
  through the router endpoint (v7 averaged $0.39 a seat, so about $55 for the run), plus the platform's credits.
artifacts: []
---

# v11: the hybrid with v9's lighter press

## Context

v11 is v10's code merged with the spend thread's branch at 124b445 (keep-starts, the phase-start cost curve and
the failed-start fix), built as `pidip:hybrid-lighter` with v9's four overrides
(`CAPTURE_REVIEW=0.67,PRESS_UPDATE_BRIEFINGS=1,GOVERNOR_KEEP_STARTS=1,GOVERNOR_RESERVE_USD=0.02`), the Diplodocus
switches (`META_SEEDS=32,META_RANK=1,SEARCH_PASSES=0`) and `PRESS_FALLBACK_MODEL=` (no Jev on the router route).
It drops v7's squeeze settings: call and wake limits, debounce, note limits, `PRESS_DEALS`, `PRESS_HISTORY`,
`PRESS_WAKE_GATE`, `PRESS_VERBOSITY=low` and the governor's prior. Uploaded 06:27Z (`aa575072`).

## Design

Paired, balanced (`run_ab.py`, 14 bodies x 5 = 70 games) against `league-top5-2026-10-14`, launched 06:30Z
(platform estimate 817.8 credits). No separate health game: v11's code is v10's plus the spend thread's
keep-starts governor, whose health v8 and v9 showed hosted, so health is read from the first paired games
(non-200s, rejected orders, phase starts completed, spend a seat).

## Result

Read 08:06Z on 2026-10-15, all 14 batches terminal (`paired.py`, `wd.py metrics`, `wd.py costs`).

- **Paired:** v11 minus v10 **-0.001 ± 0.051 a game, z -0.01, n = 67 clean pairs** (paired SD 0.414; 2 games
  dropped, one wake timeout logged as an exception in each arm).
- **Alone:** v11 0.298 a game (+0.182 ± 0.025 over par), 8.31 centres; v10 0.304 (+0.187 ± 0.031), 8.40 centres.
- **By power against par:** v11 below v10 at five powers (England -0.10, z -1.0), above at Russia (+0.11) and
  Turkey (+0.07); none at |z| over 1.2.
- **Telemetry:** 0 rejected orders either arm. Failed calls v11 94 of 5,823 (1.6%), v10 266 of 5,684 (4.7%).
- **Spend:** v11 $0.477 a seat (max $0.528; 15 of 70 seats over $0.50 by its own count), v10 $0.393 (max
  $0.447, none over). The keep-starts governor's $0.02 reserve did not hold the cap on this route, where the
  platform does not refuse calls.

## Verdict

**Inconclusive**, and not entered: no difference (z -0.01) over 67 pairs, while v11 spent $0.08 a seat more and
went over the $0.50 cap in 15 seats. The squeeze press v7 and v10 use stays. Entered in `open_levers.md`.
