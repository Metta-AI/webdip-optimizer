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
  press so far, 6 games: mean 0.360 (with press, rounds 57 to 62: 0.546 over 16). Round 65 (watch at 06:33Z, no
  press, Austria in all three): 0.000 (eliminated, 7th), 0.047 (6th), 0.062 (4th); 0 rejected, 0 exceptions.
  Every game counted (round 57's pod-deleted games included): with press 0.492 over 18, without 0.252 over 9,
  difference 0.24 ± 0.15 (z 1.6; powers not balanced). Field at 06:35Z: kutuzov:v108 0.159 over 3 seats (above v15
  in both shared games); new entrants astra-press:v1 and kutuzov:v109 seated in round 66; Bodhisattva:v3 0.215 over
  26 is the best non-v15 entrant. Watch at 09:33Z, rounds 66 to 68 (no press, 0 rejected, 0 exceptions; one
  pod_deleted seat in round 67, kept): 1st in 6 of 9 (0.734, 0.124 2nd, 0.462, 0.340 2nd, 0.571, 0.583, 0.068 5th,
  0.616, 0.424), mean 0.436, so 18 games without press: mean 0.344. Field at 09:40Z: kutuzov iterates fast
  (v108 0.159 over 3, v109 0.208 over 6, v110 0.217 over 3); Bodhisattva:v4 entered (0.091 over 3);
  astra-press:v1 0.113 over 9 (beat v15 once, 0.42 to 0.34); v15 0.464 over 30. Watch at 12:33Z, rounds 69 and
  70 (no press, 0 rejected, 0 exceptions): solos in two (1.0, 1.0), 1st with 0.621 and 0.744, 5th 0.086, 7th 0.0;
  mean 0.575, so 24 games without press: mean 0.402. Field at 12:35Z: new comax-webdip:v31 and kutuzov:v111; no
  entrant other than v15 above 0.24 (co-gas-webdiplomacy-relh:v23 0.236 over 27). Watch at 15:33Z, rounds 71 to
  73 (no press, 0 rejected, 0 exceptions, 1 HTTP error in round 71): 0.649 1st, 0.181 3rd, 0.645 1st, 0.110 4th,
  0.000 (Germany: our pod was deleted 2080 s into 2800 s of play, already down to 1 centre by 1906), 0.370 tied 1st,
  0.333 1st, 0.250 tied 1st, 0.018 6th; mean 0.284 (0.320 over the 8 without the dead pod), so 33 games without
  press: mean 0.370. Key at 15:35Z: usage $545.15 against the $430 limit, flat to 15:41Z (usage_daily $122.38);
  every v15 call in rounds 63 to 73 got 403 or 402, so the $81 added since 03:29Z is late-posted charges (inferred:
  most likely the v17 paired run). Field at 15:35Z (field.py's last 30 seats): no new entrants or versions; v15 0.381;
  co-gas-webdiplomacy-relh:v23 0.249 (won two round-72 games with 0.531 and 0.471; v15 ahead of it in 11 of 17
  shared games since round 64); Bodhisattva:v3 0.217 over 12. Watch at 18:33Z, rounds 74 and 75 (no press, 0
  rejected, 0 exceptions): solos as France and Italy (1.0, 1.0), 0.376 tied 1st, 0.151 3rd, 0.134 3rd, 0.083 6th;
  mean 0.457, so 39 games without press: mean 0.383. Key unchanged ($545.15, dry). Field at 18:35Z (last 27 seats):
  new grievous:v8 (James Botts, first seated in round 76, no results yet) and kutuzov:v112 (0.093 over 3, tied v15
  once at 0.134); v15 0.421, co-gas-webdiplomacy-relh:v23 0.263, everyone else at or below 0.26. Watch at 21:33Z,
  rounds 76 and 77 (no press, 0 rejected, 0 exceptions; v15's pod deleted in round 77's ereq_d75f54a4, held its last 6
  movement phases): 0.202 2nd, 0.219 2nd, 0.571 1st, 0.131 3rd, 0.083 5th (dead pod), solo as France (1.0); mean
  0.368, so 45 games without press: mean 0.381. Key unchanged. Field at 21:35Z: **grievous:v8 (James Botts) 0.318
  over its first 6 seats** (0.012, 0.526, 0.333, 0.645, 0.354, 0.040), second to v15 (0.406 over 27); beside v15 it
  won 0.526 to 0.131 (round 77, clean), 0.333 to 0.083 (round 77, our pod deleted), lost 0.040 to 0.219 (round 76).
  Reported to Scott; profile it if it stays above 0.25. Also new: nancy-dip:v4, sovereign:v3 (A-aron), no results
  yet; co-gas-webdiplomacy-relh:v23 0.260. Watch at 00:33Z on 10-17, rounds 78 and 79 (no press, 0 rejected, 0
  exceptions, no taint beyond llm_failing): 0.084 5th, 0.042 6th, 0.140 3rd, 0.590 1st, 0.102 4th, 0.517 1st; mean
  0.246, so 51 games without press: mean 0.365. Key: usage $545.15, usage_daily 0; `limit_reset` is monthly, so the
  $430 limit should give room again from 2026-11-01 (inferred from that key setting; tell Scott when calls succeed). Field
  at 00:35Z (last 27 seats): v15 0.333, co-gas-webdiplomacy-relh:v23 0.279 over 24 (v15 ahead 14, behind 8 since
  round 64), grievous:v8 0.244 over 12 (3 and 3 against v15), new co-gas-webdiplomacy-independent-relh:v4 0.210 over
  3 (1 and 1), new sovereign:v6 0.153 over 3, sovereign:v3 0.170 over 3, nancy-dip:v4 0.036 over 6, new comax-pidip:v1
  (no results yet). Reported to Scott (v15 under 0.25 on 6 new games; lead over the field narrowed). Watch at
  03:33Z on 10-17, rounds 80 and 81 (no press, 0 rejected, 0 exceptions, 3 HTTP errors): 0.325 2nd, 0.000 7th
  (Russia, eliminated), 0.117 4th, 0.045 6th, 0.522 1st, 0.108 5th; mean 0.186. Rounds 78 to 81: 0.216 over 12 (sd
  0.21) against 0.390 over 42 in rounds 64 to 77 (sd 0.34): -0.174 +/- 0.080, z -2.2, split chosen after seeing the
  data. 57 games without press: mean 0.346. Field at 03:35Z: co-gas-webdiplomacy-relh:v23 0.302 over 21 now above
  v15 0.288 over 30, but it has shared no game with v15 since round 77 (v15 ahead 14, behind 8 in 22 shared; in
  those games co-gas 0.196, v15 0.363); grievous:v8 0.247 over 17; sovereign:v6 0.229 over 8; Bodhisattva:v4 0.210
  over 29 (top score in 3 of v15's last 6); comax-pidip:v1 0.189 over 6. Reported to Scott. Look at the 12 weak
  games (rounds 78 to 81 against 64 to 77): the power draw predicts 0.375 (v15's by-power means over all 54), so not
  the draw; v15 scored lower beside every opponent seen 4+ times in both periods, so not one rival; centres by year
  match to 1902 (4.4, 4.9) then stall (1908: 6.6 against 8.8; 10+ centres at the end in 4 of 12 against 19 of 42);
  top scorer in v15's games: v15 3 of 12 against 20 of 42, Bodhisattva:v4 4 of 12. No single mechanism; may be
  noise plus a stronger field. No change proposed. Fetch the next rounds with `fetch_league.py press --policy
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

- Scheduled task "webDiplomacy league watch" (`trig_013iSjSE55tZvYUXn7hzk5BW`, every 3 hours from 06:32Z on 10-16):
  reads v15's new league rounds and compares the field with the newest `.runtime/monitor/field-*.json` (baseline
  05:30Z on 10-16). Scott, 05:27Z: "leave it for now and we just monitor to see if the meta changes". Round 65 (running
  at 05:30Z) seats a new entrant, kutuzov:v108 (Andre von Auto, the suvorov author), in place of suvorov:v21.

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
