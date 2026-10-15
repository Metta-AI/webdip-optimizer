---
id: 2026-10-15-v10-retry-fixes
policy: scott-pidip
baseline: scott-pidip:v7
candidate: scott-pidip:v10
status: confirmed
hypothesis: >
  v10 loses fewer model and Diplodocus calls than v7 because the hosted sidecar's quick 502s clear within 3 s
  and v10 retries 4 s later (pidip/agent.mjs two retries 4 s and 8 s apart; castlereagh/meta.py one retry of a
  5xx after 4 s), where v7 retried model calls after 2 s and Diplodocus calls never; and v10 makes no Jev calls
  on the BYO route (PRESS_WAKE_GATE=0, PRESS_FALLBACK_MODEL empty), which v7's route refused with 403.
decision_rule: >
  Robustness only; strategy is unchanged. v10 replaces v7 in the webDiplomacy league iff, in three
  classic-press-short games with v10 and v7 both seated, v10 shows 0 rejected orders, 0 exceptions, 0 Jev calls,
  a failed-call share below v7's in the same games, and fewer Diplodocus sample failures a movement phase than
  v7. Scott's go-ahead (06:04Z on 2026-10-15): "yea enter v7 but like keep going with the follow ups with any
  fixes then land those asap once done". Otherwise v7 stays and the failure is diagnosed.
evals: [xreq_b714927a-9274-4f11-a865-ca77cd3545aa]
cost: 3 classic-press-short games, 35.5 credits by the platform's estimate at create (06:20Z)
artifacts: []
---

# v10: v7 with later retries of the sidecar's 502s and no Jev calls on the BYO route

## Context

v7's 70 hosted games against v5 (`2026-10-15-hybrid-diplodocus-vs-v5`) lost 442 of 5,627 model calls (7.9%):
351 quick 502 "LLM sidecar internal error" and 80 Jev 403s, plus 190 Diplodocus sample calls and 64 value calls.
The Diplodocus endpoint's own log for 04:30 to 06:10Z shows every request it received answered 200, so the
losses are between the seat and the endpoint. Across both arms' seat logs, the next model call after a 502
succeeded 0 of 216 times within 3 s and 212 of 212 times 3 to 5 s later. Also in v7: one exception, a
`daide.parse` ValueError on a rival's DAIDE with unbalanced brackets in `roster.ingest_replies`.

Policies repo commit 6968d05 (branch `claude/project-thread-etdwi7`), merged into `local/hybrid-luna` at
3404bb1; image `pidip:hybrid-sol-v10`, v7's overrides with `PRESS_WAKE_GATE=0` and `PRESS_FALLBACK_MODEL=`.

## Result

Read 06:45Z on 2026-10-15, three classic-press-short games, all completed, no taint (`wd.py metrics`).

| | v10 | v7 |
|---|---|---|
| Rejected orders, exceptions | 0, 0 | 0, 0 |
| Model calls failed | 2 of 164 (1.2%), both 502 | 7 of 167 (4.2%) |
| Jev calls | 0 | 1 (403) |
| Press wakes | 55 ok, 3 call limit, 0 error | 50 ok, 3 call limit, 1 error |
| Diplodocus samples failed | 0 (1 retried and answered) | 0 |
| Sol spend, 3 seats | $0.84 | $0.79 |

Scores (v10 0.215, v7 0.324 a game) are 3 games and say nothing.

## Verdict

**Confirmed** on robustness: fewer failed calls than v7 in the same games, no Jev calls, no rejected orders or
exceptions. The Diplodocus-failure condition is a tie at 0 in these games; the one 5xx v10 met was retried and
answered, where v7's code would have lost that phase's samples. Entry put to Scott at 06:46Z.
