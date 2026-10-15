---
id: 2026-10-15-v12-diplodocus-adjust
policy: scott-pidip
baseline: scott-pidip:v10
candidate: scott-pidip:v12
status: running
hypothesis: >
  The hybrid scores more when Diplodocus's policy network chooses its retreats and builds because those phases
  still come from DumbBot's centre-value heuristics (castlereagh/search.py SearchBot.choose, dumbbot.py
  _retreats and _adjustments), and the build mix and placement set up the next year's movement, where the
  Diplodocus-ranked orders already play; v12 asks the server's policy stage instead (META_ADJUST,
  castlereagh/meta.py adjust) and keeps DumbBot when the call fails or an order is not legal.
decision_rule: >
  Scott's release bar against the current champion: v12 replaces it iff v12 minus v10 is at least +0.03 a game
  with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected orders, failed calls no
  higher than v10's in the same games, spend at most $0.50 a seat by its governor's count, and Diplodocus orders
  in at least 90% of v12's retreat and build phases (meta_adjust against meta_adjust_illegal and
  meta_policy_failed). Health is read from the first paired games. Scott's direction (relayed 06:20Z on
  2026-10-15): keep improving over the next 12 hours, using Diplodocus more effectively. Otherwise the champion
  stays and the lever is recorded.
evals: [xreq_812a7309-cfaa-4cab-9aa9-477ca8ecc9f8, xreq_d91f14ea-5fd2-4f22-8ee6-cace5b503b01, xreq_78db0eed-db55-48af-8c76-84b302808991, xreq_42c222d7-3cb2-4576-971a-220251100570, xreq_75691f05-703a-4857-9bac-cacad935e439, xreq_f543f918-bbcc-444a-a574-c3a3e149581a, xreq_b998e86f-8cdc-4eb6-b7ba-204ca3b41501, xreq_1051f557-98b6-4f36-b547-9d8d266e0909, xreq_1838b3de-6585-4bb2-a561-a66166431e97, xreq_3c156917-f7e2-4954-b9c1-43f5f44cad30, xreq_bf88f9e0-833f-46f7-b05a-6d716a60b5f0, xreq_b3a44f68-847e-4fce-a426-4468577c4af8, xreq_6c5c6f8f-90cd-4178-aa8a-ae393285a1b8, xreq_1c99e1f2-7d27-42c8-a156-759d67da39d7]
cost: 70 full press games (-n 5, 14 bodies) at a $0.50 cap; both arms' Sol calls bill to Scott's OpenRouter key
  through the router endpoint (about $0.39 a seat, so about $55), plus the platform's credits.
artifacts: []
---

# v12: Diplodocus chooses the hybrid's retreats and builds

## Context

Policies repo commit f6ab41c (`META_ADJUST`), merged with v10's code in `local/hybrid-luna` at 1e66141; image
`pidip:hybrid-adjust`, v10's overrides plus `META_ADJUST=1`. One change against v10.

Local check (`/home/user/dipwork/adjust`, 7 no-press games to 1908 on the local CPU server; pidip's search seats
with v7's Diplodocus settings, three seats with `META_ADJUST=1` and three without, one plain pidip control):
Diplodocus played 87 of 89 build phases and 70 of 70 retreat phases for the adjust seats (2 builds fell back to
DumbBot as not legal; 0 failed calls), 0 rejected orders, policy calls 0.1 to 0.6 s. Adjust seats 0.183 a game
against 0.148 without (+0.035; 21 seat-games each, own bots only). Local runs are a wiring check, not a verdict.

## Design

Paired, balanced (`run_ab.py`, 14 bodies x 5 = 70 games) against `league-top5-2026-10-14`, launched 07:13Z
(platform estimate 859.9 credits). Health is read from the first paired games.

## Result

## Verdict
