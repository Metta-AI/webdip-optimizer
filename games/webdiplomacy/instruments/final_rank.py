#!/usr/bin/env python3
"""Whether ranking Diplodocus's plans by the exact final score in a game's last movement phase picks plans worth
more than ranking them by Diplodocus's value network, from fetched games.

The value network predicts our share of the final score as if the game went on. After the last movement phase (the
autumn of the end year, or the autumn a solo ends the game) nothing follows, so the score is known once the moves
are adjudicated: 1 for 18 or more centres, 0 if another power has 18, else our centres squared over the survivors'
sum. For our seats' last movement phase, on a local Diplodocus server that takes `opponents`:

- `samples`: 32 joint actions; the orders we played and our power's distinct plans are the candidates, samples 0-15
  of the other powers the replies.
- `values` with those replies as `opponents`: the value network's pick among Diplodocus's plans (the seat's
  META_RANK pick with no pins or forbidden provinces).
- exact: each candidate against the same 16 replies, adjudicated by castlereagh's fastadj (convoys approximated,
  retreats not played; a centre goes to the unit standing on it after the moves); the pick with the highest mean
  final score among Diplodocus's plans, and among those plans and the orders we played (what a seat could do in its
  last phase: rank its committed orders beside Diplodocus's plans by the exact score).
- ex post: each candidate, and the orders we played, against the other powers' recorded orders. Moves are
  simultaneous and no phase follows, so that is the final score the seat would have had, up to press (another
  message could have changed someone's orders) and retreats. `fidelity` compares the played orders' ex post score
  with results.json.

    final_rank.py DIR... --policy scott-pidip:v7 --version-id 044a0425 --server http://127.0.0.1:8001
        [--server ...] [--cache FILE]
"""
import argparse
import json
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diplodocus_fit import ask  # noqa: E402
from plan_regret import jobs_for, sig, we, webdip  # noqa: E402

from castlereagh import fastadj  # noqa: E402  (plan_regret puts the lab's castlereagh on the path)

REPLIES = 16
SOLO = 18


class Board:
    """The last movement phase's board, adjudicated by fastadj with every other unit holding unless ordered."""

    def __init__(self, frame):
        variant, board = frame["variant"], frame["game"]
        self.parent = {t["id"]: t["coastParentID"] for t in variant["territories"]}
        supply = {t["id"] for t in variant["territories"] if t["supply"]}
        self.owner = {t["terrID"]: t["ownerCountryID"] for t in board["territories"] if t["terrID"] in supply}
        self.units = [u for u in board["units"] if not u.get("retreating")]

    def score(self, orders, me):
        p = self.parent
        by_prov = {p[o["terrID"]]: o for o in orders}
        convoys = {(p[o["terrID"]], p[o["fromTerrID"]], p[o["toTerrID"]]) for o in orders
                   if o["type"] == "Convoy" and o["fromTerrID"] and o["toTerrID"]}
        fu, fo = [], []
        for u in self.units:
            prov = p[u["terrID"]]
            fu.append((int(u["countryID"]), prov, u["type"]))
            o = by_prov.get(prov)
            kind = o["type"] if o else "Hold"
            if kind == "Move":
                dst = p[o["toTerrID"]]
                ok = o["viaConvoy"] != "Yes" or any(c[1] == prov and c[2] == dst for c in convoys)
                fo.append(("M", dst) if ok else ("H",))
            elif kind == "Support hold":
                fo.append(("SH", p[o["toTerrID"]]))
            elif kind == "Support move":
                fo.append(("SM", p[o["fromTerrID"]], p[o["toTerrID"]]))
            else:
                fo.append(("H",))
        moved, dislodged = fastadj.adjudicate(fu, fo)
        occupied = {}
        for (country, prov, _), o, mv, dl in zip(fu, fo, moved, dislodged):
            if not dl:
                occupied[o[1] if mv else prov] = country
        counts = {}
        for terr, owner in self.owner.items():
            owner = occupied.get(p[terr], owner)
            if owner:
                counts[int(owner)] = counts.get(int(owner), 0) + 1
        if max(counts.values()) >= SOLO:
            return float(counts.get(me, 0) >= SOLO), counts.get(me, 0)
        return counts.get(me, 0) ** 2 / sum(v * v for v in counts.values()), counts.get(me, 0)


def last_jobs(ep, policy, version_id):
    """plan_regret's job for each of our seats' last movement phase, when the game finished after it."""
    episode = we.read_json_file(ep / "episode.json")
    replay_path = we.first_existing(ep, we.REPLAY_NAMES)
    if policy not in we.seat_policies(ep, episode).values() or replay_path is None or not replay_path.stat().st_size:
        return []
    replay = we.read_json_file(replay_path)
    results = we.read_json_file(we.first_existing(ep, we.RESULTS_NAMES))
    phases = replay[-1]["history"]["phases"]
    if phases[-1]["phase"] != "Finished":
        return []
    last = max(int(p["turn"]) for p in phases if p["phase"] == "Diplomacy")
    if last % 2 != 1:
        return []
    return [{**j, "actual": results["scores"][j["slot"]]} for j in jobs_for(ep, policy, version_id)
            if j["turn"] == last]


def run(server, job):
    f, me = job["frame"], job["country"]
    b = Board(f)
    base = {"game_key": f"final-{job['episode']}", "country_id": me, "end_year": 1908, "turn": job["turn"],
            "phase": "Diplomacy", "variant": f["variant"], "history": f["history"], "board": f["game"],
            "temperature": 0.75, "top_p": 0.95, "checkpoint": "diplodocus_low_rl_policy.ckpt"}
    samples = {int(c): plans for c, plans in ask(server, {**base, "stage": "samples", "n": 32})["samples"].items()}
    candidates, seen = [job["ours"]], {sig(job["ours"])}
    for plan in samples.get(me, []):
        plan = [webdip(o) for o in plan]
        if sig(plan) not in seen:
            seen.add(sig(plan))
            candidates.append(plan)
    replies = [{str(c): [webdip(o) for o in plans[j]] for c, plans in samples.items() if c != me and len(plans) > j}
               for j in range(REPLIES)]
    value = ask(server, {**base, "stage": "values", "n": REPLIES, "candidates": candidates,
                         "opponents": replies})["values"]
    exact = [statistics.mean(b.score(plan + [o for orders in r.values() for o in orders], me)[0] for r in replies)
             for plan in candidates]
    others = [o for orders in job["others"].values() for o in orders]
    post = [b.score(plan + others, me) for plan in candidates]
    played = post[0]
    return {"episode": job["episode"], "slot": job["slot"], "turn": job["turn"], "candidates": len(candidates),
            "value": value, "exact": [round(x, 5) for x in exact], "post": [round(s, 5) for s, _ in post],
            "post_centres": [c for _, c in post], "played": round(played[0], 5), "played_centres": played[1],
            "actual": job["actual"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="+", type=Path)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--version-id", required=True)
    ap.add_argument("--server", action="append", required=True)
    ap.add_argument("--cache", type=Path)
    args = ap.parse_args()

    rows, done = [], set()
    if args.cache and args.cache.exists():
        rows = [json.loads(line) for line in args.cache.open()]
        done = {(r["episode"], r["slot"]) for r in rows}
    jobs = [j for d in args.dirs for ep in we.episode_dirs(d) for j in last_jobs(ep, args.policy, args.version_id)
            if (j["episode"], j["slot"]) not in done]
    print(f"{len(jobs)} last movement phases ({len(done)} cached)", file=sys.stderr)
    out = args.cache.open("a") if args.cache else None
    with ThreadPoolExecutor(2 * len(args.server)) as pool:
        for row in pool.map(lambda ij: run(args.server[ij[0] % len(args.server)], ij[1]), enumerate(jobs)):
            rows.append(row)
            if out:
                out.write(json.dumps(row) + "\n")
                out.flush()

    def top(xs):
        return max(range(len(xs)), key=lambda k: (xs[k], -k))

    rows = [r for r in rows if r["candidates"] > 1]  # candidate 0 is the orders we played

    def top_plans(xs):  # Diplodocus's plans only
        return 1 + top(xs[1:])

    fidelity = sum(abs(r["played"] - r["actual"]) < 0.005 for r in rows)
    print(f"{len(rows)} seats; the played orders' ex post score matches results.json in {fidelity}")
    diffs = {"exact pick minus value pick": [r["post"][top_plans(r["exact"])] - r["post"][top_plans(r["value"])]
                                             for r in rows],
             "value pick minus played": [r["post"][top_plans(r["value"])] - r["played"] for r in rows],
             "exact pick minus played": [r["post"][top_plans(r["exact"])] - r["played"] for r in rows],
             "exact pick with the played orders as a candidate, minus played": [r["post"][top(r["exact"])] - r["played"]
                                                                               for r in rows]}
    differ = sum(top_plans(r["exact"]) != top_plans(r["value"]) for r in rows)
    print(f"the exact and value picks differ in {differ} of {len(rows)} seats")
    print("| final score, ex post | mean a seat | SE | better / same / worse |\n|---|---|---|---|")
    for label, d in diffs.items():
        se = statistics.stdev(d) / len(d) ** 0.5 if len(d) > 1 else float("nan")
        print(f"| {label} | {statistics.mean(d):+.4f} | {se:.4f} | "
              f"{sum(x > 1e-9 for x in d)} / {sum(abs(x) <= 1e-9 for x in d)} / {sum(x < -1e-9 for x in d)} |")
    exact_solo = sum(r["post_centres"][top_plans(r["exact"])] >= SOLO for r in rows)
    value_solo = sum(r["post_centres"][top_plans(r["value"])] >= SOLO for r in rows)
    played_solo = sum(r["played_centres"] >= SOLO for r in rows)
    print(f"solos (18+ centres ex post): played {played_solo}, value pick {value_solo}, exact pick {exact_solo}")


if __name__ == "__main__":
    main()
