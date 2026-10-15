#!/usr/bin/env python3
"""Whether ranking more of Diplodocus's sampled plans picks plans worth more, from fetched games.

For every movement phase of our seats (plan_regret.py's jobs), on a local Diplodocus server: one `samples` call for
64 joint actions; our power's distinct plans from the first 32 (the seat's META_SEEDS) and from all 64 are the two
candidate sets. One `values` call (16 replies, the seat's META_RANK_SAMPLES) scores every plan on the same replies,
and one ex post call scores them against the joint action the other powers actually played. Per phase: the ex post
value of the best-rated plan among all 64 minus that of the best among the first 32.

    seed_count.py DIR... --policy scott-pidip:v14 --version-id c124fe73 --server http://127.0.0.1:8001
        [--server ...] [--limit N] [--cache FILE]
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


def run(server, job):
    f = job["frame"]
    base = {"game_key": f"seeds-{job['episode']}", "country_id": job["country"], "end_year": 1908,
            "turn": job["turn"], "phase": "Diplomacy", "variant": f["variant"], "history": f["history"],
            "board": f["game"], "temperature": 0.75, "top_p": 0.95, "checkpoint": "diplodocus_low_rl_policy.ckpt"}
    samples = ask(server, {**base, "stage": "samples", "n": 64})["samples"].get(str(job["country"]), [])
    candidates, seen, first = [], set(), 0
    for k, plan in enumerate(samples):
        plan = [webdip(o) for o in plan]
        if sig(plan) not in seen:
            seen.add(sig(plan))
            candidates.append(plan)
        if k == 31:
            first = len(candidates)
    ante = ask(server, {**base, "stage": "values", "n": 16, "candidates": candidates})["values"]
    post = ask(server, {**base, "stage": "values", "n": 1, "candidates": candidates,
                        "opponents": [job["others"]]})["values"]
    return {"episode": job["episode"], "slot": job["slot"], "turn": job["turn"], "first32": first,
            "all64": len(candidates), "ante": ante, "post": post}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="+", type=Path)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--version-id", required=True)
    ap.add_argument("--server", action="append", required=True)
    ap.add_argument("--limit", type=int, default=0, help="at most N phases, spread over the games")
    ap.add_argument("--cache", type=Path)
    args = ap.parse_args()

    rows, done = [], set()
    if args.cache and args.cache.exists():
        rows = [json.loads(line) for line in args.cache.open()]
        done = {(r["episode"], r["slot"], r["turn"]) for r in rows}
    jobs = [j for d in args.dirs for ep in we.episode_dirs(d) for j in jobs_for(ep, args.policy, args.version_id)]
    if args.limit:
        jobs = jobs[::max(1, len(jobs) // args.limit)][:args.limit]
    jobs = [j for j in jobs if (j["episode"], j["slot"], j["turn"]) not in done]
    print(f"{len(jobs)} movement phases ({len(done)} cached)", file=sys.stderr)
    out = args.cache.open("a") if args.cache else None
    with ThreadPoolExecutor(2 * len(args.server)) as pool:
        for k, row in enumerate(pool.map(lambda ij: run(args.server[ij[0] % len(args.server)], ij[1]),
                                         enumerate(jobs))):
            rows.append(row)
            if out:
                out.write(json.dumps(row) + "\n")
                out.flush()
            if k % 25 == 24:
                print(f"  {k + 1} of {len(jobs)}", file=sys.stderr)

    rows = [r for r in rows if r["first32"] > 0]
    gain = []
    for r in rows:
        top32 = max(range(r["first32"]), key=lambda k: r["ante"][k])
        top64 = max(range(r["all64"]), key=lambda k: r["ante"][k])
        gain.append(r["post"][top64] - r["post"][top32])
    changed = sum(1 for g in gain if g != 0)
    print(f"{len(rows)} phases; distinct plans {statistics.mean(r['first32'] for r in rows):.1f} from 32 samples, "
          f"{statistics.mean(r['all64'] for r in rows):.1f} from 64; the pick changes in "
          f"{sum(1 for r in rows if max(range(r['all64']), key=lambda k: r['ante'][k]) >= r['first32'])}")
    print(f"ex post, best of 64 minus best of 32: {statistics.mean(gain):+.4f} ± "
          f"{statistics.stdev(gain) / len(gain) ** 0.5:.4f} a phase ({changed} phases differ ex post)")


if __name__ == "__main__":
    main()
