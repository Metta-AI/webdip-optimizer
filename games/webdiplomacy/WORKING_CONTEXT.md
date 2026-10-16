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
  clean league games: mean 0.512 (v7's league mean was 0.506). Round 60 (fetched about 00:00Z on 10-16, v15 in
  3): 1st as France 0.723 (16 centres), 1st as France 0.513 (11), 4th as Russia 0.081 (4). Two seats carry the
  "exception" taint, each one caught wake timeout (the seat played on); counting them, 10 league games: mean 0.490. Round 61 (fetched 01:05Z on 10-16): 1st as Germany 0.699 (15
  centres), 1st as England 0.563 (12; one caught wake timeout), 6th as Russia 0.047 (3); 0 rejected; 25 of 250
  calls failed, every one a 502 "LLM sidecar internal error" between 00:19 and 00:50Z (key not dry: $74 left at
  01:06Z; cause not found; the Mini Diplomacy farm ran on the same Modal account from about 00:15Z). 13 league
  games: mean 0.478. v15's league Russia: 0.106, 0.081, 0.047 (the diagnosis's Russia lead). Round 62 (01:28 to
  02:12Z, no taint): 1st in all three, solos as Austria (20 centres) and Turkey (18), England 0.527 (16); 0 rejected,
  0 exceptions, 0 of 233 calls failed, 2 HTTP errors. The farm ran on Modal through this round, so it did not
  cause round 61's 502s. 16 league games: mean 0.546. **The OpenRouter key ran out at 02:42Z on 10-16** (usage
  $463.65 against the $430 limit at 03:29Z, so charges kept landing past the limit; the v17 paired run cost more
  than estimated, with two of our seats in each game). Round 63 (02:40 to 03:23Z): 75 of 90 calls failed (74 HTTP
  403, 1 HTTP 402) after 02:42Z, so v15 played Diplodocus's orders without press: 1st as France 0.639 (15
  centres), Austria 0.078 (4 centres, tied 4th), Italy 0.043 (3 centres, tied 5th); 0 rejected, 0 exceptions.
  Raising the limit needs Scott's word and a broker request he approves (auto mode blocked preparing it at 03:3xZ;
  decision card posted in the thread: raise to $500, $550, or leave it). **Scott chose "Leave it" at 05:27Z on
  10-16**: the key stays dry and v15 plays without press; do not raise it or ask again unless he brings it up. Round 64 (fetched 04:41Z, no press, 0 of 62
  calls succeeded): solo as Turkey (1.0), 1st as Russia 0.308 (8 centres), Germany 0.090 (4, tied 4th). Without
  press so far, 6 games: mean 0.360 (with press, rounds 57 to 62: 0.546 over 16). Fetch the next rounds with `fetch_league.py press --policy
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
- v17 (forbid guard) is **inconclusive** on all 112 paired games: +0.029 ± 0.046 a game over v15, t 0.62 (first
  set +0.055, second about +0.002; record and open_levers.md). v15 stays the candidate and the entry. Scott at
  22:57Z on 10-15: "do whatever you think makes the most sense. goal is just to get the best possible bot
  submitted". The offline diagnosis (2026-10-16, 222 seats of this run, 56 of v14's, 12 league seats) found no
  lever likely to add +0.03 a game: the governor's mispriced levels and the guard skipped on press-wake
  re-commits are each about +0.005 to +0.008 (open_levers.md, sized 2026-10-16); Russia loses 4.72 ± 0.45 centres
  a game to the field against 1.3 to 3.0 for the others (n 32; v14's run had Russia at 0.425, n 8), a lead with no
  mechanism yet. So no paired run is planned; v15 stays. Any new paired run needs the key raised again. The key's usage counter lags: at 22:11Z it showed
  only $4 of the first set's $43, then climbed about $0.5 a minute. Key: limit raised to $430 at 23:05Z (Scott
  approved the broker request); at 00:13Z on 10-16 it showed $106.84 left, about $35 once both sets' charges
  land. Earlier: limit raised from $320 to $380 at 20:55Z ($74.81 left) on Scott's ask,
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
