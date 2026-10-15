---
id: 2026-10-15-v16-press-aware-values
policy: scott-pidip
baseline: scott-pidip:v15 if its health record confirms, else scott-pidip:v14
candidate: scott-pidip:v16 (pidip:hybrid-rankpress2, v15 with META_RANK_PRESS=1 as its one change; uploaded 12:33Z)
status: proposed
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
  Scott's release bar against the baseline: v16 is put to Scott for entry iff v16 minus baseline is at least +0.03
  a game with t at least 1 over 50 or more clean paired games (paired.py), with 0 rejected orders, failed calls no
  higher than the baseline's in the same games, spend at most $0.50 a seat by its governor's count, and a clean
  health game. Entry needs Scott's explicit go-ahead naming the version.
evals: []
cost: >
  As v14's test: three short health games, then 56 to 70 full press games; about $0.39 of Sol a seat on Scott's
  OpenRouter key. Needs the key's limit raised: it had $76 left at 10:47Z before v14's run took about $44.
artifacts: []
---

# v16: Diplodocus ranks plans against the replies Sol's deals predict

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

League check of the mechanism (`instruments/diplodocus_fit.py`, 12:58Z): the 79 fetched league games with one
of our seats (v5 and v7), every movement phase's `samples` request rebuilt from the replay and sent to the local
server (32 joint actions, the seat's settings), each other power's samples against the orders it played.
"Contact" = one of its units borders one of our units or centres; "attack" = a move or supported move into one.

| Our stance at the phase | Power-phases in contact | Diplodocus samples attack us | Actually attacked us |
|---|---|---|---|
| ally | 770 | 0.207 | 0.051 |
| neutral | 109 | 0.288 | 0.202 |
| none given | 1,925 | 0.393 | 0.344 |
| hostile | 972 | 0.492 | 0.542 |
| all | 3,776 | 0.377 | 0.331 |

Today's ranking replies have allies attack four times as often as they do; with trust 0.8, apply_press brings
the 0.207 to about 0.04. The samples give the order a unit played 0.32 of their weight on average, alike for
every field policy (0.30 to 0.34).

Offline check of the pick (`instruments/press_rank.py`, 16:46Z): 300 movement phases of v14's paired run whose
committed policy named an ally (295 with two or more plans), local server. Our distinct plans from 32 samples,
ranked on samples 0-15 of the others as sampled and again with the seat's apply_press step for allies (promised
orders not applied), then scored against what the others actually played:

| Phases | n | Picks differ | Ex post, press-ranked minus raw-ranked | SE |
|---|---|---|---|---|
| all | 295 | 22 | -0.0006 | 0.0005 |
| no ally attacked us | 275 | 16 | -0.0006 | 0.0005 |
| an ally attacked us | 20 | 6 | +0.0004 | 0.0010 |

Press conditioning turned 2.1 ally orders a phase (of 16 replies) into holds, none at all in 212 of 295 phases,
and the value network's pick moved in 22. Where it moved, the press-ranked plan did no better against the real
orders (-0.002 +/- 0.002 over the 83 phases where it fired). Allies attacked us in 6.8% of these phases. So the
mechanism is real (Diplodocus over-predicts ally attacks) but on this read it barely changes our orders. This is
an offline proxy, not a verdict; it is a reason to test v17 (`2026-10-15-forbid-guard`) before this one when the
key allows one paired run.
