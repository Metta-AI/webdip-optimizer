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
