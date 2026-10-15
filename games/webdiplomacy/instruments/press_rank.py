#!/usr/bin/env python3
"""Whether ranking Diplodocus's plans against press-conditioned replies (v16's META_RANK_PRESS) picks plans worth
more against what the other powers actually played, from fetched games.

For every movement phase of our seats whose committed press policy names an ally (plan_regret.py's jobs), on a
local Diplodocus server that takes `opponents`: one `samples` call for 32 joint actions; our power's distinct
plans are the candidates, and samples 0-15 of the other powers are the replies. Two `values` calls score every
candidate against those 16 replies: as sampled (raw), and with the seat's apply_press step for allies (each move or
support-move of an ally into a province of ours becomes a hold with probability = our trust in that ally; default
trust 0.7, as castlereagh/press/service.py). Promised orders (expected_orders) are not applied. A third call scores
the candidates against the joint action actually played (ex post). Per phase: the ex post value of the
press-ranked pick minus the raw-ranked pick, split by whether an ally actually moved or supported into our
provinces that phase.

    press_rank.py DIR... --policy scott-pidip:v14 --version-id c124fe73 --server http://127.0.0.1:8000
        [--server ...] [--limit N] [--cache FILE]
"""
import argparse
import json
import random
import statistics
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diplodocus_fit import POWER_NAMES, ask  # noqa: E402
from plan_regret import jobs_for, sig, we, webdip  # noqa: E402

DEFAULT_TRUST = 0.7
REPLIES = 16


def run(server, job):
    f = job["frame"]
    me, policy = job["country"], job["policy"]
    parent = {t["id"]: t["coastParentID"] for t in f["variant"]["territories"]}
    supply = {t["id"] for t in f["variant"]["territories"] if t["supply"]}
    ours = {parent[u["terrID"]] for u in f["game"]["units"] if int(u["countryID"]) == me}
    ours |= {parent[t["terrID"]] for t in f["game"]["territories"]
             if t["terrID"] in supply and t.get("ownerCountryID") and int(t["ownerCountryID"]) == me}
    trust = {c: min(max(float((policy.get("trust") or {}).get(name, DEFAULT_TRUST)), 0.0), 1.0)
             for c, name in POWER_NAMES.items() if (policy.get("stances") or {}).get(name) == "ally"}

    def into_ours(o):
        return o["type"] in ("Move", "Support move") and o["toTerrID"] and parent[int(o["toTerrID"])] in ours

    base = {"game_key": f"pressrank-{job['episode']}", "country_id": me, "end_year": 1908,
            "turn": job["turn"], "phase": "Diplomacy", "variant": f["variant"], "history": f["history"],
            "board": f["game"], "temperature": 0.75, "top_p": 0.95, "checkpoint": "diplodocus_low_rl_policy.ckpt"}
    samples = {int(c): plans for c, plans in ask(server, {**base, "stage": "samples", "n": 32})["samples"].items()}
    candidates, seen = [], set()
    for plan in samples.get(me, []):
        plan = [webdip(o) for o in plan]
        if sig(plan) not in seen:
            seen.add(sig(plan))
            candidates.append(plan)
    rng = random.Random(f"{job['episode']}:{job['slot']}:{job['turn']}")
    raw, press, holds = [], [], 0
    for j in range(REPLIES):
        joint_raw, joint_press = {}, {}
        for c, plans in samples.items():
            if c == me or len(plans) <= j:
                continue
            orders = [webdip(o) for o in plans[j]]
            joint_raw[str(c)] = orders
            joint_press[str(c)] = [
                {"type": "Hold", "terrID": o["terrID"], "toTerrID": 0, "fromTerrID": 0, "viaConvoy": "No"}
                if c in trust and into_ours(o) and rng.random() < trust[c] else o for o in orders]
            holds += sum(a != b for a, b in zip(orders, joint_press[str(c)]))
        raw.append(joint_raw)
        press.append(joint_press)
    out = {"episode": job["episode"], "slot": job["slot"], "turn": job["turn"], "candidates": len(candidates),
           "allies": len(trust), "press_holds": holds,
           "ally_attacked": any(into_ours(o) for c in trust for o in job["others"].get(str(c), []))}
    for name, replies in (("raw", raw), ("press", press)):
        out[name] = ask(server, {**base, "stage": "values", "n": REPLIES, "candidates": candidates,
                                 "opponents": replies})["values"]
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
    jobs = [j for d in args.dirs for ep in we.episode_dirs(d) for j in jobs_for(ep, args.policy, args.version_id)
            if "ally" in ((j["policy"] or {}).get("stances") or {}).values()]
    if args.limit:
        jobs = jobs[::max(1, len(jobs) // args.limit)][:args.limit]
    jobs = [j for j in jobs if (j["episode"], j["slot"], j["turn"]) not in done]
    print(f"{len(jobs)} movement phases with an ally ({len(done)} cached)", file=sys.stderr)
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

    groups = defaultdict(list)
    for r in rows:
        d = r["post"][top(r["press"])] - r["post"][top(r["raw"])]
        groups["all"].append((d, top(r["press"]) != top(r["raw"])))
        groups["an ally attacked us" if r["ally_attacked"] else "no ally attacked us"].append(
            (d, top(r["press"]) != top(r["raw"])))
    print(f"ally orders into our provinces turned into holds: {statistics.mean(r['press_holds'] for r in rows):.1f} "
          f"a phase over {REPLIES} replies; phases with none: {sum(r['press_holds'] == 0 for r in rows)}")
    print("| phases | n | picks differ | ex post, press-ranked minus raw-ranked | SE |\n|---|---|---|---|---|")
    for g, v in groups.items():
        ds = [d for d, _ in v]
        se = statistics.stdev(ds) / len(ds) ** 0.5 if len(ds) > 1 else float("nan")
        print(f"| {g} | {len(v)} | {sum(c for _, c in v)} | {statistics.mean(ds):+.4f} | {se:.4f} |")


if __name__ == "__main__":
    main()
