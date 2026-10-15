# Version log — castlereagh

Maps every uploaded version of this policy to the one change it carries.
**The row is mandatory before anything else happens after an upload** —
an unlogged version is a hole in the campaign's memory. Honest caveats
("NOT proven better — the A/B was contaminated") are valuable entries.

Validation states: `unvalidated` → `validated` / `refuted` (by a recorded
experiment) → `submitted` (with the decision record appended below the row).

Each upload is one mode (`--policy search|press`); log both modes' uploads as separate rows.

| Version | Policy version id | Uploaded (UTC) | The one change (and its mechanism) | Runtime config | Validation | Notes |
|---|---|---|---|---|---|---|
| v0 | (not uploaded) | — | The starter policy as shipped: the Default search, plus the press harness with its neutral default soul and two reference skills. | `CASTLEREAGH_POLICY=press` (default) or `search` | unvalidated in your field (the golden test pins the search's orders; nothing here was measured against your opponents) | The baseline every later row is compared with. |

## Submission decision records

Appended by `submit` when a version enters a league — the evidence that
justified it, the human's recorded go-ahead, and the rollback plan.

### 2026-10-15 06:05Z: scott-pidip:v7 enters league_1bccc63d (classic press) in place of v5

- **Acting player:** macromackie (`ply_5b832230-f519-4af8-adda-bb3e02349b7d`, the account default). **League:**
  `league_1bccc63d-cd0a-47d7-92d7-e762797b5f1c`, classic press, 3-minute phases, ends 1908. **Version:**
  `scott-pidip:v7` (`044a0425-e107-456a-83d7-765b9ad25cc9`), the Diplodocus hybrid (squeeze-sol press, Diplodocus
  orders through the router endpoint). Source: policies repo branch `local/hybrid-luna` at 43104c1.
- **Evidence:** experiment `2026-10-15-hybrid-diplodocus-vs-v5` (confirmed): v7 minus v5 +0.141 ± 0.045 a game,
  z 3.13, n = 63 clean pairs; v7 ahead at all seven powers; spend $0.388 a seat (max $0.459). Two bar conditions
  missed to the letter: 7.9% failed calls (platform 502s, which hit v5 too, and Jev 403s on the BYO route) and one
  rejected-orders flag that the replay shows is false.
- **Go-ahead:** Scott, 06:04Z on 2026-10-15, chose "Enter v7 now" on the card "Enter v7, the Diplodocus hybrid, in
  the league in place of v5?", then wrote: "yea enter v7 but like keep going with the follow ups with any fixes
  then land those asap once done".
- **Placed:** `sub_4e128c27`, membership `lpm_f5264e77`, competing/active and champion at 06:06Z; v5 benched.
- **Rollback:** resubmit `scott-pidip:v5` (`9263a7b8-ff15-4634-bec1-9a22484d5d44`) to the same league as
  macromackie: `coworld submit scott-pidip:v5 --league league_1bccc63d-cd0a-47d7-92d7-e762797b5f1c --no-open-browser`.

### 2026-10-15 18:27Z: scott-pidip:v15 enters league_1bccc63d (classic press) in place of v7

- **Acting player:** macromackie (`ply_5b832230-f519-4af8-adda-bb3e02349b7d`). **League:**
  `league_1bccc63d-cd0a-47d7-92d7-e762797b5f1c`, classic press, 3-minute phases, ends 1908. **Version:**
  `scott-pidip:v15` (`2fcc2040-f729-4486-93cd-56d115621faa`), image `pidip:hybrid-pinguard2`: v14 (Diplodocus pin
  guard) with the guard bounded by the wake's time left. Source: `local/hybrid-luna` at 82fc3c3 (policies commit
  3700a2b on top of v14's).
- **Evidence:** v10 the retry fixes over v7 (`2026-10-15-v10-retry-fixes`, confirmed), v12 minus v10 +0.089
  a game, t 1.46, n = 54 (`2026-10-15-v12-diplodocus-adjust`, confirmed), v13 the retry waits
  (`2026-10-15-v13-retry-waits`, confirmed), v14 minus v13 +0.132 a game, t 1.99, n = 56 clean pairs, 0 rejected
  orders, failed calls below v13's (`2026-10-15-v14-value-pin-guard`, confirmed against Scott's +0.03 bar). v15
  plays as v14 when the guard runs; its 3 classic-press-short health games beside v14 (`xreq_39bb7446`) had 0
  rejected orders, 0 exceptions, 0 of 181 model calls failed, 0 timed-out wakes (`2026-10-15-v15-guard-timing`,
  confirmed). v15 also carries the fix for v7's turn-0 crash on rival DAIDE (6 of v7's league games). No paired
  run of v15 against v7 itself: the chain v7 to v10 to v12 to v13 to v14 is measured step by step.
- **Known weaknesses:** a values call that misses the wake's bound plays the pinned plan (1 of 41 in the health
  games); the guard keeps every province Sol forbids (v17's lever); Sol spends about $0.375 a seat on the
  OpenRouter key, which had $17.76 left at 18:05Z.
- **Go-ahead:** Scott, 18:24Z on 2026-10-15, chose "Enter v15" on the card "Enter v15 (v14 plus the press-wake
  timing fix) in the league in place of v7?", then wrote in the project chat: "ok i left some comments tell tit to
  keep going idk what is bets but like whatever it thinkgs make sense i trust".
- **Placed:** `sub_45b39127`, membership `lpm_9647eb8d`, competing/active and champion at 18:27:54Z; v7
  (`lpm_f5264e77`) benched.
- **Rollback:** resubmit `scott-pidip:v7` (`044a0425-e107-456a-83d7-765b9ad25cc9`) as macromackie:
  `coworld submit scott-pidip:v7 --league league_1bccc63d-cd0a-47d7-92d7-e762797b5f1c --player
  ply_5b832230-f519-4af8-adda-bb3e02349b7d --no-open-browser`.
