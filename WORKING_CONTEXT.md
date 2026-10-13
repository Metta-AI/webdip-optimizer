# Working context — optimizer-wide

The live, one-screen state of what this optimizer is doing *right now*. Not a
log, not an archive: finished work lives in git history and the records; this
file is what a fresh agent reads to resume. Prune on read; reseed on pivot.

**Routing signal:** if "Current objective" below is empty, this optimizer has
not been onboarded — start with `docs/getting-started.md`. A recorded objective
means onboarding is done; never re-run it, never re-ask what's recorded here.

## Current objective

*(none — run onboarding)*

## Active games

- `games/webdiplomacy/`: webDiplomacy, installed 2026-10-13 by coworld-webdiplomacy `optimizer/install.sh`. Every tool and skill of the lab is listed under "Tool and skill index" in `games/webdiplomacy/AGENTS.md`

## Open threads

*(none)*

## Watched ids

*(eval batches, submissions, or anything else being monitored — with what to
do when each turns terminal)*

## Load-bearing facts

*(things a resuming agent must know that live nowhere else — keep short, move
anything durable to its proper home per the AGENTS.md state map)*

## Harness wiring

- Claude Code: wired by `optimizer/install.sh` on 2026-10-13. `CLAUDE.md` loads `AGENTS.md`
  (and `games/webdiplomacy/CLAUDE.md` the lab manual). Skills are linked in
  `.claude/skills/`; `.claude/settings.json` runs `rotate_lessons.sh` and the lab's
  `check_clis.py` and `check_coworld.py` at SessionStart, and both stop nudges at Stop. The IDE (`ide/`) adds
  `ide/ide hook <event>` at SessionStart, UserPromptSubmit, PostToolUse, Stop and SessionEnd
  (they hand the user's browser messages to the session and tell the page when it ends), a
  background waiter (`ide/ide hook Rewake`, marked `asyncRewake`) at the first four and at
  FileChanged (the IDE's chat file) that wakes an idle or interrupted session, the
  `webdip-ide` server in `.mcp.json`, and the `webdiplomacy-ide` skill link. The lab's `press-audit`, `opponent-profile` and
  `matchup-writeup` skills are linked in `.claude/skills/` too. Nothing to do.
- Any other runtime: not wired. Do the self-wiring step in `harness/README.md`
  and record it here.
