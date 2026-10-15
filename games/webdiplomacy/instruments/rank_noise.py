#!/usr/bin/env python3
"""Whether ranking Diplodocus's plans on more sampled replies picks plans worth more, from fetched games.

For every movement phase of our seats (plan_regret.py's jobs), on a local Diplodocus server:

- `samples`: 32 joint actions; our power's distinct plans are the candidates (the seat's META_RANK candidates).
- `values` three times on fresh replies: n=16 twice (A, B: the seat's META_RANK_SAMPLES) and n=64 (C).
- `values` ex post: each candidate against the joint action the other powers actually played.

Per phase: the ex post value of the plan each ranking picks, how often A and B pick the same plan, and each call's
seconds (the price on the endpoint). Rank on more replies pays if top(C) beats top(A) ex post over many phases.

    rank_noise.py DIR... --policy scott-pidip:v14 --version-id c124fe73 --server http://127.0.0.1:8001
        [--server ...] [--limit N] [--cache FILE]
"""
import argparse
import json
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diplodocus_fit import ask  # noqa: E402
from plan_regret import jobs_for, sig, we, webdip  # noqa: E402

N_LARGE = 64


def run(server, job):
    f = job["frame"]
    base = {"game_key": f"rank-{job['episode']}", "country_id": job["country"], "end_year": 1908,
            "turn": job["turn"], "phase": "Diplomacy", "variant": f["variant"], "history": f["history"],
            "board": f["game"], "temperature": 0.75, "top_p": 0.95, "checkpoint": "diplodocus_low_rl_policy.ckpt"}
    samples = ask(server, {**base, "stage": "samples", "n": 32})["samples"].get(str(job["country"]), [])
    candidates, seen = [], set()
    for plan in samples:
        plan = [webdip(o) for o in plan]
        if sig(plan) not in seen:
            seen.add(sig(plan))
            candidates.append(plan)
    out = {"episode": job["episode"], "slot": job["slot"], "turn": job["turn"], "candidates": len(candidates)}
    for name, n in (("a", 16), ("b", 16), ("c", N_LARGE)):
        start = time.monotonic()
        out[name] = ask(server, {**base, "stage": "values", "n": n, "candidates": candidates})["values"]
        out[f"{name}_s"] = round(time.monotonic() - start, 2)
    out["post"] = ask(server, {**base, "stage": "values", "n": 1, "candidates": candidates,
                               "opponents": [job["others"]]})["values"]
    return out


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

    rows = [r for r in rows if r["candidates"] > 1]

    def top(values):
        return max(range(len(values)), key=lambda k: values[k])

    def mean_se(xs):
        return statistics.mean(xs), statistics.stdev(xs) / len(xs) ** 0.5

    print(f"{len(rows)} phases with 2 or more distinct plans; candidates a phase "
          f"{statistics.mean(r['candidates'] for r in rows):.1f}")
    print(f"A and B (16 replies each) pick the same plan in {sum(top(r['a']) == top(r['b']) for r in rows)} "
          f"of {len(rows)}")
    for label, pick in (("A, 16 replies", lambda r: top(r["a"])),
                        ("A+B pooled, 32 replies", lambda r: top([x + y for x, y in zip(r["a"], r["b"])])),
                        (f"C, {N_LARGE} replies", lambda r: top(r["c"]))):
        m, se = mean_se([r["post"][pick(r)] - r["post"][top(r["a"])] for r in rows])
        print(f"| {label} | ex post minus A's pick {m:+.4f} ± {se:.4f} |")
    gap16 = [abs(r["a"][top(r["a"])] - r["b"][top(r["a"])]) for r in rows]
    print(f"A's top plan: |A value - B value| mean {statistics.mean(gap16):.4f} (the noise in one 16-reply value)")
    for name in ("a", "c"):
        print(f"values call seconds, {name}: median {statistics.median(r[name + '_s'] for r in rows):.1f}")


if __name__ == "__main__":
    main()
