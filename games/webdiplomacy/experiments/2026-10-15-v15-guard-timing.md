---
id: 2026-10-15-v15-guard-timing
policy: scott-pidip
baseline: scott-pidip:v14
candidate: scott-pidip:v15
status: running
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
