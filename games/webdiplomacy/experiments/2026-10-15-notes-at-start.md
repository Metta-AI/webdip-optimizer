---
id: 2026-10-15-notes-at-start
policy: scott-pidip
baseline: scott-pidip:v15
candidate: scott-pidip:v18
status: proposed
hypothesis: >
  Sol spends about 11% less a game with no loss of play when its notes are rewritten at phase starts only, because
  in v7's league games it rewrote its one "strategy" note on 24.6 wakes a game (730 characters each, about a
  quarter of its $0.375 a game; $0.042 of that on press wakes), and a press wake's note is overwritten by the next
  phase start's, which sees the deals section, the referee facts and conversation(POWER).
  Policies commit b72e482 (castlereagh/press/player.py task_text, press/tools.py notes).
decision_rule: >
  A spend change cannot clear Scott's +0.03 bar, so its rule is Scott's to set before any run. Proposed:
  enter in place of v15 iff, over 50 or more clean paired games against v15, Sol's spend a seat falls by at least
  8% and the paired difference is above -0.03 a game with its 95% interval's lower end above -0.08, with
  0 rejected orders and failed calls no higher than v15's.
evals: []
cost: >
  As v14's test: about 56 full press games, about $0.37 of Sol a seat on the OpenRouter key (about $40) and about
  150 credits by the platform's estimate. Only worth running once the key's limit is raised.
artifacts: []
---

# Notes at phase starts only

## Context

`wd.py`-style read of the 25 v7 seats in `.runtime/artifacts/league-press` (2026-10-15 13:30Z): 1,946 Sol calls,
$9.38 ($0.375 a seat). Prices fitted from the calls (r² 1.0): $2.0 a million uncached prompt tokens, $0.1
cached, $2.5 cache writes, $10 completion. Cost shares: cache writes 44%, completion 42%, cached reads 14%; 88%
of prompt tokens are cached already. Of Sol's output characters, `notes` is 55% (24.6 calls a seat, 732
characters each), `commit_orders` 14%, `send_press` 7%, `search` 7%. Each note rewrites the single "strategy"
note with the whole state; the press task's text asks for it ("Note anything you will want at a later wake").

Cache writes are not a lever (same seats, 757 wakes, 2.5 calls a wake): every call writes its new suffix and the
next call in the wake reads it. 52% of the written tokens are each wake's briefing on its first call, 30% the
middle calls', and 27% the last call's (single-call wakes count in both), which nothing reads again. Not caching
the last call would bill those tokens at $2.0 instead of $2.5 a million: $0.009 a seat, 2% of spend.

## Predictions — pre-registered

- **If TRUE we expect:** `notes` calls on press wakes near 0, spend a seat down 8 to 12%, paired difference
  within noise of 0.
- **If FALSE we expect:** spend down less than 8% (Sol writes longer notes at phase starts), or the paired
  difference below -0.03 (the lost press-wake notes carried what later phases needed).

## Design

v18 (`ab275a32-7b1a-4812-8957-c31c0063c70c`, uploaded 16:16Z) is image `pidip:hybrid-notes`: local merge `aa7d544`
= v15 plus policies commit `b72e482`, `PRESS_NOTES_AT_START=1`, otherwise v15's settings.

Not yet run. Paired design as v14's (`run_ab.py`, 14 bodies x 4) against `league-top5-2026-10-14`, after one
short health game.
