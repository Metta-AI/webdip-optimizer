---
id: 2026-10-15-v15-press-aware-values
policy: scott-pidip
baseline: scott-pidip:v14 if its record confirms, else scott-pidip:v13
candidate: scott-pidip:v15 (built on the baseline with META_RANK_PRESS=1 as its one change)
status: planned
hypothesis: >
  The hybrid scores more when Diplodocus's value network ranks our plans against replies conditioned on the press
  policy, because today it ranks them against fresh no-press Diplodocus samples, which have every power attack us
  as often as a no-press player would, and Sol's allies attack us far less: in v12's hosted run, powers Sol marked
  "ally" moved or supported into our units or centres in 9% of the phases they bordered us (84 of 893), against
  27% for "neutral", 47% with no stance and 65% for "hostile". Sol's trust for allies averaged 0.81, and
  apply_press keeps an ally's attack in about 1 - trust of the samples, so the conditioned replies match the
  realised rate. Policies commit 312bdfb: META_RANK_PRESS sends this phase's Diplodocus samples with the policy
  applied (opponent_model.apply_press) as the values stage's `opponents`.
decision_rule: >
  Scott's release bar against the baseline: v15 is put to Scott for entry iff v15 minus baseline is at least +0.03
  a game with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected orders, failed calls no
  higher than the baseline's in the same games, spend at most $0.50 a seat by its governor's count, and a clean
  health game. Entry needs Scott's explicit go-ahead naming the version.
evals: []
cost: >
  As v14's test: three short health games, then 56 to 70 full press games; about $0.39 of Sol a seat on Scott's
  OpenRouter key. Needs the key's limit raised: it had $76 left at 10:47Z before v14's run took about $44.
artifacts: []
---

# v15: Diplodocus ranks plans against the replies Sol's deals predict

## Context

Ally attack rates: `tools/press_audit.py extract` on the 59 finished games of
`.runtime/artifacts/2026-10-15-v12-diplodocus-adjust` (118 seats, v12 and v10), each movement phase's committed
policy against the adjudicated orders. "Contact" = the power had a unit next to one of our units or centres;
"attacked" = it ordered a move or a supported move into one of them.

| Sol's stance | Contact phases | Attacked us | Rate |
|---|---|---|---|
| ally (mean trust 0.81) | 893 | 84 | 0.09 |
| neutral | 309 | 84 | 0.27 |
| none given | 1,523 | 713 | 0.47 |
| hostile | 2,212 | 1,443 | 0.65 |

The server change is backward compatible: a values call without `opponents` samples as before. The endpoint
needs a `modal deploy` with policies commit 312bdfb (or later) before the health game; a seat sending `opponents`
to the old server is not refused, its field is ignored, so the server log's `opponents` count (commit 4f8590f) is
the check.

Local wiring check (`/home/user/dipwork/rankpress/wiring2`, one game to 1902 on the new server code, the press
seat driven by `tools/meta/fake_llm.py`, every power an ally at trust 0.8): 16 values calls carried 16
press-conditioned replies, the floor's 4 carried none, the plain Diplodocus seat's 4 carried none; 0 rejected
orders, 0 exceptions, 0 server errors.
