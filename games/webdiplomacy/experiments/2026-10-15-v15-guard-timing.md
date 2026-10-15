---
id: 2026-10-15-v15-guard-timing
policy: scott-pidip
baseline: scott-pidip:v14
candidate: scott-pidip:v15
status: confirmed
hypothesis: >
  v15 loses fewer press wakes to the wake deadline than v14, because v14's timed-out wakes (1.5% of press wakes in
  its hosted run) were the pin guard's free search and values call starting late in a wake whose commit already
  took long under test load (commit median 11 s, max 58 s), and v15 bounds the guard by the wake's time left: it
  skips the guard with under PIN_GUARD_RESERVE_S (10 s) to spare and passes the remainder to the values call as
  its timeout, with no retry. Replaying v14's 263 guard firings against that bound keeps 254 of them.
decision_rule: >
  Robustness only; the guard's choice is unchanged when it runs. v15 may follow v14 into the league iff three
  classic-press-short games with v15 and v14 both seated show v15 with 0 rejected orders, 0 exceptions, failed
  calls no higher than v14's, no more timed-out wakes than v14, and the guard firing (pin_guard lines with a
  value verdict) in most movement phases with pins. Entry needs Scott's word naming v15.
evals: [xreq_39bb7446-f368-4fbd-b077-25cad6003a35]
cost: 3 classic-press-short games, 32.9 credits by the platform's estimate at create (12:16Z)
artifacts: []
---

# v15: v14 with the pin guard bounded by the wake's time left

## Context

Policies commit 3700a2b (`castlereagh/press/player.py` passes `wake_deadline - now - PIN_GUARD_RESERVE_S` to
`guarded_search`; `meta.ask` takes a timeout and then does not retry), merged into `local/hybrid-luna` at 82fc3c3
(`bot/` = v14's plus 3700a2b); image `pidip:hybrid-pinguard2`, v14's overrides. Uploaded 12:14Z.

Health games: `xreq_39bb7446`, launched 12:16Z, fetched to `.runtime/artifacts/2026-10-15-v15-health`. Short games
carry light endpoint load, so they check wiring and health; the timeout rate is a property of loaded paired runs.

## Result

Read 12:41Z, three games, all completed, no taint. v15: 0 rejected orders, 0 exceptions, 0 of 181 model calls
failed, Diplodocus orders in 23 of 23 movement phases (value net changed the pick in 22) and its retreat and build
phases, 62 press wakes ok, 4 at their call limit, 0 timed out. The guard judged 40 commits by value and skipped 1
whose values call did not answer inside the bound (it played the pinned plan); 26 pins dropped, 120 kept. v14 in
the same games: 0 of 169 failed, 64 wakes ok, 5 at the call limit, 0 timed out, 36 commits judged. Values calls took
3.3 s median and 8.7 s at most for v15 (light load), so the bound was not tested hard here.

## Verdict

**Confirmed** as healthy against the rule: clean, and no worse than v14 on every count. Whether it removes the 1.5%
of timed-out wakes is a property of loaded runs; the evidence for the bound is the replay of v14's 263 guard
firings (254 kept).
