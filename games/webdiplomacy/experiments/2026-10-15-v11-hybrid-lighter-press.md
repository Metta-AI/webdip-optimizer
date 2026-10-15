---
id: 2026-10-15-v11-hybrid-lighter-press
policy: scott-pidip
baseline: scott-pidip:v10
candidate: scott-pidip:v11
status: proposed
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
evals: []
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

## Result

## Verdict
