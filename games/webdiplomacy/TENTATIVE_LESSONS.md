# Tentative lessons — session buffer (webDiplomacy lab)

This session's candidate lessons about this game and this lab. Buffer eagerly
and candidly; most will be noise, and that's fine — recurrence across sessions
graduates a lesson into this lab's `best_practices.md` (via `lessons-review`).

If a session genuinely produced no lessons, write nothing.

---

- 2026-10-15: launching 56 full press games at once (14 batches of 4, Coworld 0.7.14) failed 3 games within
  4 minutes with `error_type: player_never_started` ("Kubernetes did not start every player process before the
  game's player-connect timeout", all 7 slots "never scheduled"); the other 53 started. Infrastructure taint, cost
  $0.045 each. Size a launch that must reach N clean games with a few spare, or launch in sets.
- 2026-10-15: a policy refused by the spend cap from mid-game (v5, all model calls refused from turn 7 in every
  seat) still scored +0.05 over a version that never ran out (v6). Running out of model budget late cost less
  than this lab expected; check how much late-game press is worth before paying to keep it.
- 2026-10-15: scoring our played movement orders against Diplodocus's own best plan, with Diplodocus's value
  after the phase against the others' actual orders (`instruments/plan_regret.py`), located the leaks for $0: pins
  (fixed by v14, +0.13 a game hosted) and forbidden provinces (v17). The same ex-post read showed three
  sample-count and ranking levers worth under 0.001 a phase. Run it before buying hosted games for an order-side
  idea.
- 2026-10-15: half of Sol's forbidden provinces sit in a DAIDE DMZ it accepted, and partners broke those deals 11
  times against 379 accepted. Split forbids by whether a deal backs them before letting anything overrule them.
