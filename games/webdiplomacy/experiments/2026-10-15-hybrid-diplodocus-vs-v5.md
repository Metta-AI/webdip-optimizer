---
id: 2026-10-15-hybrid-diplodocus-vs-v5
policy: scott-pidip
baseline: scott-pidip:v5
candidate: scott-pidip:v7
status: proposed
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
evals: []
cost: >
  One classic-press-short health game (hybrid alone against league-top5-and-v5-2026-10-15), then 56 full press
  games (-n 4, 14 bodies) with every platform-metered seat capped at $0.50. The hybrid's own model calls go
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
errors. Then the paired, balanced design (`run_ab.py`, 14 bodies x 4) against `league-top5-2026-10-14`,
`--llm-budget-usd 3.5`.

Health game: `xreq_2647f478-bc8c-4a70-b2c3-7542e926f7ac` (launched 04:05Z on 2026-10-15; platform estimate 14.9
credits), fetched to `.runtime/artifacts/2026-10-15-hybrid-diplodocus-vs-v5-health`.

Confound: the hybrid's spend is held by its own governor, not by the sidecar. If the governor's count misses
the router's `usage.cost`, the hybrid may spend more than $0.50 a seat; the health game checks that against the
OpenRouter key's usage.

## Result

## Verdict
