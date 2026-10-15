---
id: 2026-10-15-v13-retry-waits
policy: scott-pidip
baseline: scott-pidip:v12
candidate: scott-pidip:v13
status: confirmed
hypothesis: >
  v13 loses fewer calls than v12 when the sidecar's 502s come in bursts, because from 07:13Z a retry within 5 s
  of a 502 failed every time (0 of 256) while one 5 to 8 s later succeeded 134 of 135; v13 waits 6 s then 12 s
  (pidip/agent.mjs baseDelayMs 6000; castlereagh/config.py META_RETRY_DELAYS_S) where v12 waited 4 s and 8 s
  (Diplodocus calls once after 4 s).
decision_rule: >
  Robustness only; play is unchanged. v13 may follow v12 into the league iff three classic-press-short games with
  v13 and v12 both seated show v13 with 0 rejected orders, 0 exceptions, failed calls no higher than v12's and
  Diplodocus orders in its retreat and build phases. Entry needs Scott's word naming v13 (card at 09:14Z).
evals: [xreq_0e1c4ba5-e6a1-4ec9-9be1-4f570cc1aad9]
cost: 3 classic-press-short games, 32.6 credits by the platform's estimate at create (09:15Z)
artifacts: []
---

# v13: v12 with 6 s and 12 s waits before retrying a sidecar 502

## Context

Policies repo commit 61db092, merged into `local/hybrid-luna` at bdbb591 (`bot/` = v12's plus 61db092); image
`pidip:hybrid-adjust2`, v12's overrides. Uploaded 08:13Z (`f212ded3`).

## Result

Read 09:37Z, three games, all completed, no taint. v13: 0 rejected orders, 0 exceptions, 0 of 152 model calls
failed, Diplodocus orders in 10 of 10 retreat and build phases, 58 press wakes ok and 4 at their call limit. v12
in the same games: 0 of 146 failed, 6 of 6 Diplodocus phases. The platform returned no 502s to either seat in
these games, so the longer wait was not exercised.

## Verdict

**Confirmed** as healthy against the rule: clean, and no worse than v12. The retry benefit itself is untested here
(no 502s met); the evidence for the wait length is the 07:13 to 08:06Z seat logs above.
