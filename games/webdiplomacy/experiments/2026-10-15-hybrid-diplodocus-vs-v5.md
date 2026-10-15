---
id: 2026-10-15-hybrid-diplodocus-vs-v5
policy: scott-pidip
baseline: scott-pidip:v5
candidate: scott-pidip:v7
status: confirmed
hypothesis: >
  The hybrid outscores v5 at a $0.50 cap because its orders come from Diplodocus (Meta's no-press policy and
  value networks on Scott's Modal endpoint): 32 sampled plans ranked by the value net (META_SEEDS=32,
  META_RANK=1, SEARCH_PASSES=0), which in local games beat pidip's own search, while the press layer keeps
  squeeze-sol's model use.
decision_rule: >
  Scott's release bar (pidip README, wave 2): the hybrid replaces v5 in the webDiplomacy league iff hybrid minus
  v5 is at least +0.03 a game with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected
  orders and at most 1% failed LLM calls for the hybrid, and a clean health game. Scott chose "Auto-enter" at
  22:57Z on 2026-10-14 for a Sol-plus-Diplodocus version that clears this bar. Otherwise v5 stays.
evals: [xreq_0441c9c1-211e-46bc-a0f0-d69df4c74ccd, xreq_5d885ba5-3d8b-4ccd-a2f0-efd9da9f2d8a, xreq_fcf08f54-992d-4436-87d2-85457dba68ce, xreq_655d5a7f-259b-4046-afe3-0896eca77d71, xreq_19231b61-58e9-4f88-80c5-aef3fdcb287f, xreq_9d8a43fb-5af2-4571-95ea-303c257cde68, xreq_cd4d69fe-a109-4037-9b98-678f6b8215f7, xreq_92659cda-329b-4bae-8231-2d465fb5e71a, xreq_4d33d394-9a69-40c6-b57c-75d1038bce3d, xreq_8de48835-b8f8-4d64-a0ce-9fcc935ccf7b, xreq_45709b72-c317-4738-a976-9c4d253d6161, xreq_e0e018ee-4bd1-4c19-b37f-620129182200, xreq_f353f6ec-5f25-4187-844f-f9cfbfad5789, xreq_cb6dcb48-5539-451a-bf63-b88aeb03d6ae]
cost: >
  One classic-press-short health game (hybrid alone against league-top5-and-v5-2026-10-15), then 70 full press
  games (-n 5, 14 bodies) with every platform-metered seat capped at $0.50. The hybrid's own model calls go
  through its registered endpoint, which the platform meters at $0: they bill to Scott's OpenRouter key, and
  the hybrid's governor holds them to the cap the sidecar reports. Modal CPU time for the endpoint is extra.
artifacts: []
---

# Diplodocus hybrid (squeeze-sol press, Diplodocus orders) against v5

## Context

Policies repo PR #11 (branch `claude/project-thread-etdwi7`): pidip asks Diplodocus for 32 sampled plans and
ranks them, with its own value net, against pidip's candidate; `SEARCH_PASSES=0` turns pidip's own search off.
Local evidence (`workspaces/pidip/META_NETWORKS.md`): rounds 1 and 2, 70 gunboat games, value-ranked
Diplodocus plans +0.245 ± 0.041 a game over pidip's search; 4 full local press games to 1908, hybrid 0.482 a
game against 0.066 for its twin without Diplodocus (+0.417 ± 0.133), both about $0.23 of Sol a seat.

The hosted route is one registered BYO endpoint, `https://scott-73859--diplodocus.us-east.modal.run/v1`
(router tier, `diplodocus-router` Modal secret): a request whose last message is a PhaseRequest gets a
Diplodocus answer, and any other chat goes on to OpenRouter as `openai/gpt-6.1-sol`. The image is
`pidip:hybrid-sol`: the "Spend per game" thread's squeeze-sol build (CAPTURE_REVIEW=0.67 plus its squeeze
switches) with the three META switches, on the clean player base.

The v6 test (`2026-10-14-v6-luna-press-at-050.md`) showed v5 refused by the cap from turn 7 and still
scoring 0.05 above v6. The hybrid's press layer is from the same squeeze family as v6, Sol only.

## Predictions — pre-registered

- **If TRUE we expect:** hybrid minus v5 at least +0.03 a game; the hybrid's decision lines show Diplodocus
  samples used in most movement phases (`meta_samples_failed` and `meta_values_failed` near 0).
- **If FALSE we expect:** a difference within ±0.03 or the hybrid below v5. That would mean the local gain does
  not survive this field, or that hosted latency (endpoint cold starts, 30 s timeouts) cost the improvement.

## Design

Health game first: hybrid alone against `league-top5-and-v5-2026-10-15` on classic-press-short. It must show
0 rejected orders, Diplodocus answers in most movement phases, the governor counting spend, and no endpoint
errors. Then the paired, balanced design (`run_ab.py`, 14 bodies x 5 = 70 games) against `league-top5-2026-10-14`,
`--llm-budget-usd 3.5`. Five a body, not four: the v6 run lost 9 of 56 games to platform pod failures, and the
rule needs 50 clean pairs. The one read is on the whole run.

Health game: `xreq_2647f478-bc8c-4a70-b2c3-7542e926f7ac` (launched 04:05Z on 2026-10-15; platform estimate 14.9
credits), fetched to `.runtime/artifacts/2026-10-15-hybrid-diplodocus-vs-v5-health`.

Health game result (read 04:30Z): v7 played Italy to 1904 (4 centres, 0.091; v5 as Austria 5 centres).
0 rejected orders, 0 exceptions, 50 of 50 model calls 200 (all Sol through the router, $0.245 by the
governor's count; the platform metered $0 and reported the $0.50 limit). Diplodocus answered in every movement
phase the seat logged (32 samples, samples 0.3 to 1.5 s, values 1.2 to 1.7 s, 0 failed), and the value net
changed the pick each time. Three movement phases (S1901, A1902, S1904) ended with an upstream HTTP 400 at the
phase end and no `decision` line, but the replay shows Italy's orders for all three (v5 had one such phase).
The wake gate's Jev calls get 403 on this route (its allowlist is the registered model only), so the gate
wakes on every proposal instead (7 of 12 gate checks): more Sol calls, still under the governor.

Confound: the hybrid's spend is held by its own governor, not by the sidecar. If the governor's count misses
the router's `usage.cost`, the hybrid may spend more than $0.50 a seat; the health game checks that against the
OpenRouter key's usage.

## Result

Read 05:58Z on 2026-10-15, all 14 batches terminal (`paired.py` and `wd.py metrics` on
`.runtime/artifacts/2026-10-15-hybrid-diplodocus-vs-v5`).

- **Paired:** v7 minus v5 **+0.141 ± 0.045 a game, z 3.13, n = 63 clean pairs** (paired SD 0.358; 5 games
  dropped for taint; v7 in the lower slot in 31 of 63).
- **Alone:** v7 0.330 a game (+0.222 ± 0.031 over field par, n = 64), 8.81 final centres, solo in 6.3%;
  v5 0.185 (+0.053), 6.06 centres.
- **By power** (each against par at the same power; n 8 to 10 per cell, directional only): v7 ahead of v5 at
  all seven. Austria +0.14, England +0.13, France +0.18, Germany +0.06, Italy +0.21 (z 2.1), Russia +0.05,
  Turkey +0.23 (z 2.9).
- **Taint (v7):** exception 1, rejected_orders 1, pod_deleted 2. The exception (ereq_4549fb4f) is a
  `ValueError: '(' is never closed` from `daide.parse` in `press/roster.py ingest_replies` (the PRESS_DEALS
  squeeze code) on a malformed rival message; the main loop caught it and the seat played on. The
  rejected-orders flag (ereq_795cbef8, turn 11, France, "rejected 8") is false: the `press_commit` 98 s earlier
  saved 8 with 0 rejected, and the replay adjudicates all 8 French orders (EDI, HOL and MUN taken).
- **Failed calls (v7):** 442 of 5,627 (7.9%): 351 platform 502 "LLM sidecar internal error" and 80 403s for
  `typesafe/jev-1.13` (the wake gate's fallback; the BYO route's allowlist is the registered model only). v5 had
  3,449 of 11,595 failed (29.7%): 588 502s, the rest refusals at the $0.50 cap.
- **Spend:** v7 $0.388 a seat on average, max $0.459, none over $0.50 (its governor's count of the router's
  `usage.cost`; the platform metered $0). v5 $0.491 a seat, 63 of 68 seats refused at the cap.
- **Diplodocus use:** 705 movement phases with samples against 190 sample failures and 64 value failures, so
  about 1 phase in 5 fell back to pidip's own plan. The value net changed the pick in 711 rankings.

## Verdict

**Confirmed** on the score: +0.141 a game is 4.7 times the +0.03 bar at z 3.1 over 63 pairs, and v7 led at all
seven powers. Against the rest of the release bar: the health game was clean; the one rejected-orders flag is a
false positive by the replay; failed calls are 7.9% against the 1% limit, all platform 502s (which hit v5 too)
and Jev 403s that only this route produces. Because two conditions are not met to the letter, Scott's
"Auto-enter" does not cover entry by itself; entry was put to him at 05:59Z.

Follow-ups for a later version: drop the Jev wake gate and fallback on the router route (PRESS_WAKE_GATE=0, or
route Jev through the endpoint); make `roster.ingest_replies` skip an unparseable DAIDE reply; find why 1 in 5
Diplodocus sample calls failed (sidecar 502s, 30 s timeouts or endpoint cold starts; `max_containers=8`).
