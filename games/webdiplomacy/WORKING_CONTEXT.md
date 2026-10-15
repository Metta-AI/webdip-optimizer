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
  against the league field; compare with v7's 0.506 a game below. Round 57 (19:27Z, 6 games, v15 in 3): our pod
  was deleted in 2 (seat_health disconnect at 1335 and 1338 s, the same minute, about 19:50Z; scores 0.019 and
  0.094); 5 of 42 seats in that round disconnected, most of them other entrants', so platform-side. The clean game:
  0.116, 5 centres, 0 rejected, 0 of 72 calls failed. Rounds now hold 6 games (12 before round 56); round 56 did
  not seat us. Round 58 (fetched 21:30Z, v15 in 3, no taint): Turkey 0.757 (16 centres, 1st of 7), Russia 0.106
  (4th), Germany 0.020 (6th); 0 rejected, 0 exceptions, 0 of 238 calls failed, 4 HTTP errors, $1.14 of model
  calls. Round 59 (fetched 22:41Z, v15 in 3, no taint): 1st in all three, solos as France and Germany (20 centres,
  1.0 each) and Italy 0.585 (12 centres); 0 rejected, 0 exceptions, 2 of 228 calls failed, 5 HTTP errors. So far 7
  clean league games: mean 0.512 (v7's league mean was 0.506). Fetch the next rounds with `fetch_league.py press --policy
  scott-pidip:v15 --rounds 3`.
- v16 (press-aware values, `experiments/2026-10-15-v16-press-aware-values.md`) is uploaded. Offline it moves the
  pick in 22 of 295 ally phases, no better against the real orders (-0.0006 +/- 0.0005 a phase): test v17 first. It needs the endpoint
  redeployed at policies commit 4f8590f or later (auto mode blocks a production deploy without Scott's word) and
  room on the OpenRouter key in the `diplodocus-router` Modal secret ($26 left at 12:41Z; the league entry uses
  about $2.5 an hour; a 56-game paired run about $44).
- Two candidates on v15, uploaded (inert), each waiting for key room: v17, the forbid
  guard (Diplodocus may overrule the provinces Sol forbids outside an agreed DMZ,
  `experiments/2026-10-15-forbid-guard.md`, local wiring clean), and v18, notes at phase starts only (spend about
  -11%, `experiments/2026-10-15-notes-at-start.md`, its decision rule is Scott's to set). v18's health request is
  written (`.runtime/requests/2026-10-15-v18-health.json`: 3 short games beside v15), not launched.
- v17 (forbid guard) read 22:10Z: **inconclusive**, +0.055 ± 0.072 a game over v15, t 0.77, 56 pairs (record and
  open_levers.md). v15 stays the candidate. At 22:21Z Scott was asked on a card: extend v17 by 56 games under a
  rule written first (recommended), test v18 instead, or pause. Either test needs the key raised about $50 first
  (a broker `openrouter.manage` request Scott approves in Slack). The key's usage counter lags: at 22:11Z it showed
  only $4 of the run's $43, then climbed about $0.5 a minute. Key: limit raised from $320 to $380 at 20:55Z ($74.81 left) on Scott's ask,
  through the token broker's `openrouter.manage` (one-run grant he approved in Slack; the key is named
  "foundry-artificer" on the company account). The league entry drew about $1.6 an hour from 12:41Z to 18:29Z,
  then about $0.4 an hour once rounds shrank to 6 games.
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
