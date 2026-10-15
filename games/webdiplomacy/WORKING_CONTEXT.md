# Working context — webDiplomacy lab

The live, one-screen state of this lab *right now*. Not a log: finished work
lives in git history, the version logs, and the experiment records. Prune on
read; reseed on pivot.

## Current objective

Keep Scott's league entry strongest with Diplodocus (Meta's networks on Scott's Modal endpoint) choosing the
orders and Sol doing the press. The entry is `scott-pidip:v15` (champion since 2026-10-15 18:27Z, membership
`lpm_9647eb8d`; v7 benched, rollback in VERSION_LOG's decision record). Replace it only with a version that clears Scott's release bar (pidip README) or, for a
health-only change, with clean health games; enter only with his go-ahead naming the version.

## Open threads

- v15 entered at 18:27Z on Scott's "Enter v15" (18:24Z). Its first league rounds are the first read of v15 alone
  against the league field; compare with v7's 0.506 a game below.
- v16 (press-aware values, `experiments/2026-10-15-v16-press-aware-values.md`) is uploaded. Offline it moves the
  pick in 22 of 295 ally phases, no better against the real orders (-0.0006 +/- 0.0005 a phase): test v17 first. It needs the endpoint
  redeployed at policies commit 4f8590f or later (auto mode blocks a production deploy without Scott's word) and
  room on the OpenRouter key in the `diplodocus-router` Modal secret ($26 left at 12:41Z; the league entry uses
  about $2.5 an hour; a 56-game paired run about $44).
- Two candidates on v15, uploaded (inert) and not yet health-checked, each waiting for key room: v17, the forbid
  guard (Diplodocus may overrule the provinces Sol forbids outside an agreed DMZ,
  `experiments/2026-10-15-forbid-guard.md`, local wiring clean), and v18, notes at phase starts only (spend about
  -11%, `experiments/2026-10-15-notes-at-start.md`, its decision rule is Scott's to set). Health requests are
  written (`.runtime/requests/2026-10-15-v17-health.json`, `-v18-`: 3 short games each beside v15), not launched.
- Scott chose v17 (18:24Z) for the next paired test once the key has room: health request first, then
  `run_ab.py --record 2026-10-15-forbid-guard --a scott-pidip:v17 --b scott-pidip:v15 --field-set
  league-top5-2026-10-14 -n 4`. Key: limit still $320, $16.76 left at 18:29Z (told Scott); the league entry
  averaged about $1.6 an hour from 12:41Z.
- Endpoint load: during a paired run the live entry's values calls slow from about 4 s to 14 s at p90 (league seat
  logs by hour); max_containers is 8.

## Watched ids

None.

## Load-bearing facts

- v7 in the league, rounds 47 to 55 (to 17:14Z): 0.506 a game over 38 clean games, +0.39 ± 0.05 over par, solo 16%
  (`wd.py metrics .runtime/artifacts/league-press --policy scott-pidip:v7`). Its 6 exception games are a rival's
  DAIDE with an unclosed bracket crashing the reply parser at turn 0 (fixed in 6968d05, in v15); the seat plays on.
  Its 22 failed Diplodocus calls all fell between 06:33 and 07:57Z, the sidecar's 502 window; 0 in 375 movement
  decisions since round 49.
- When the OpenRouter key runs dry the entry keeps playing Diplodocus's orders, silent: a local game of v15's image
  with every Sol call answered 402 (`/home/user/dipwork/rankpress/keydry`, 2026-10-15, ended 18:46Z, end_year 1902) made
  1 call a wake with no retry, 0 rejected orders, 0 exceptions, and saved Ready at each lock. Its strength without
  press is not measured.
- Launching 56 games at once lost 3 to `player_never_started`; plan a few spare games over a bar's minimum.
- Sol's analysis tools (predict, evaluate, assess_deal) and search reports use pidip's DumbBot opponent samples,
  not Diplodocus (META_OPP is off); Sol calls predict/evaluate/assess_deal under once a game (v14 run).
