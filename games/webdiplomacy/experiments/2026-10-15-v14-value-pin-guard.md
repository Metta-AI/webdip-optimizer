---
id: 2026-10-15-v14-value-pin-guard
policy: scott-pidip
baseline: scott-pidip:v13
candidate: scott-pidip:v14
status: running
hypothesis: >
  The hybrid scores more when Diplodocus may override the orders Sol writes for its own units, because Sol pins
  most of them: in v12's 848 hosted movement decisions Sol's committed `require_orders` covered 54% of our units,
  every unit in 378 (45%), and only about 38% of those pins name a unit our own outgoing proposals named that turn.
  Pinned orders bypass the Diplodocus-ranked plans (castlereagh/search_moves.py constrain), and Diplodocus's plans
  beat pidip's search by +0.25 a game locally. v14 turns on PIN_GUARD with the value test (policies commit
  4798892, press/service.py guarded_search): each commit also plans without the pins on our own play (a support
  or convoy of another power's unit stays pinned, forbidden provinces stay), and one values call on fresh sampled
  replies plays the free plan when Diplodocus rates it more than 0.01 higher.
decision_rule: >
  Scott's release bar against the current candidate: v14 is put to Scott for entry iff v14 minus v13 is at least
  +0.03 a game with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected orders, failed
  calls no higher than v13's in the same games, spend at most $0.50 a seat by its governor's count, and a clean
  health game. Entry needs Scott's explicit go-ahead naming the version. Scott's direction (relayed 06:20Z on
  2026-10-15): keep improving over the next 12 hours, using Diplodocus more effectively. Otherwise v13 stays the
  candidate and the lever is recorded.
evals: [xreq_8038f5ff-fa26-48cb-8314-5675624e915d, xreq_8e00475f-9c4f-4ec9-9d4e-3f6909357ee9, xreq_cab1bb67-cb54-4630-bf50-89ec9720a6c8, xreq_9034c9c2-5dab-4a1c-9ad6-b6563ec4ca30, xreq_db80a873-dd67-479d-ad3d-eb70c9f04ebf, xreq_c22f45cb-8c7d-4d0e-b976-16a3d7cb223e, xreq_102c5b26-08f3-4bdc-90c5-967cf96e6937, xreq_d9160f13-8b40-4c87-98de-eaebfb88c4de, xreq_fd99f754-2e03-455e-abea-ffa059a68fd3, xreq_e53300a7-9e62-46a4-89b5-36340e3e3e43, xreq_a83cad1c-7482-49e6-8e40-2120d9e39561, xreq_f3cad515-2130-414d-a5cf-63aa0d99df2a, xreq_0e45a818-f514-4723-943d-ac7afe2d8c7c, xreq_12a48935-74c1-48ea-8550-870f9ffc1d6d]
cost: >
  Three classic-press-short health games (v14 beside v13), then 56 to 70 full press games at a $0.50 cap; both
  arms' Sol calls bill to Scott's OpenRouter key through the router endpoint (about $0.39 a seat). The key had
  $79.89 left of its $320 limit at 10:00Z, and v7's league games draw on it too (about 3 a hour).
artifacts: []
---

# v14: Diplodocus may override Sol's orders for our own units

## Context

The pin guard is closed for pidip's own search (`workspaces/pidip/README.md` "What we learned": flat in paired
games). That guard compared pidip's hand-written search score. Here both plans are Diplodocus-ranked and
Diplodocus's value network judges them on replies it did not choose them on, so the mechanism differs; this
reopens the lever for the hybrid only.

Measured on v12's hosted run (`.runtime/artifacts/2026-10-15-v12-diplodocus-adjust`, its `decision` lines'
`press_policy`): 2,697 of 5,009 unit orders pinned; 378 of 848 movement decisions with every unit pinned, 244
with none. Of 2,697 pins, 1,028 (38%) name a unit that our DAIDE proposals that turn also named (XDO clauses);
the rest are Sol's own tactics (holds, support-holds of our units, moves). Sol is told after the fact when the
guard drops its pins (`pin_guard` line in the commit result).

Code: policies `claude/project-thread-etdwi7` at 4798892 (`meta.values`, `PIN_GUARD_VALUE_MARGIN = 0.01`), merged
into `local/hybrid-luna` at 9b93656. Image `pidip:hybrid-pinguard` = v13's overrides plus `PIN_GUARD=1`. One
change against v13. The pidip test suite passes (77 tests).

Local screen before this (`/home/user/dipwork/adjust/screen7`, 7 no-press games, 2 seats an arm): 64 Diplodocus
plans a move (S64) 0.158 a game, a 2x deeper value check (R32) 0.162, the base 0.169. No signal; neither was taken
to hosted games.

## Predictions — pre-registered

- **If TRUE we expect:** v14 minus v13 at least +0.03 a game; the guard drops pins in at least a fifth of the
  commits that pin our own play (`pin_guard_dropped` on the decision trace, `pin_guard` on `press_commit`).
- **If FALSE we expect:** a difference within ±0.03 or v14 below. That would mean Sol's tactical pins carry
  information the value network lacks (press: who will really attack), or that dropped pins cost alliances (allies
  attacking us more after we broke a pinned move).

## Design

Health first: `xreq_dd8b823d-0f4b-496e-9414-9534628e79b1` (3 classic-press-short games, v14 beside v13, field
`league-top5-2026-10-14`, launched 10:22Z). Then the paired, balanced design (`run_ab.py`, 14 bodies, `-n 4` or
`-n 5` as the key allows) against `league-top5-2026-10-14`, `--llm-budget-usd 3.5`. The one read is on the whole run.

Health result (read 10:47Z): three games to 1904, 0 rejected orders and 0 exceptions for either arm, 0 of 340
model calls failed, $1.65 for the six seats by the governors' count. v14's guard judged 43 commits that pinned our
own play and played the free plan in 11 (26%); value gains of the free plan ranged -0.005 to +0.112, most 0
(the free plan matched the pinned one). Each seat logged one or two upstream HTTP 400s at a phase end (v13 too;
seen since v7's health game). 0 values calls failed.

Paired run launched 10:48Z: 14 batches, `-n 4` (56 games; platform estimate 616.5 credits). Four a body, not
five, because the OpenRouter key had $76 left and v7's league games draw on it; `run_ab.py --add-set` adds 14
more if the clean pairs fall short of 50.
