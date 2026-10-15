#!/usr/bin/env python3
"""What our played movement orders were worth against what Diplodocus alone would have played, from fetched games.

For every movement phase of our seats, rebuilt from the replay frame and sent to a local Diplodocus server
(`diplodocus/server/local.py` at policies commit 312bdfb or later, which takes `opponents`):

- `samples`: 32 joint actions; our power's plans are the candidates, plus the orders we played.
- `values` ex ante: each candidate against 16 replies the server samples. The best sample is what a seat with
  Diplodocus and no press constraints (no pins, no forbidden provinces) would have played.
- `values` ex post: each candidate against the one joint action the other powers actually played.

Per phase: played minus Diplodocus-alone, ex ante and ex post (Diplodocus's value for us after the phase, the
expected share of the final score), split by the press policy our seat committed (pins on our own units,
forbidden provinces, from the seat log's decision line) and by game year. Ex post is one draw of the others' play:
read means over many phases. Neither number sees what a broken promise costs later.

    plan_regret.py DIR... --policy scott-pidip:v7 --version-id 044a0425 --server http://127.0.0.1:8001
        [--server ...] [--cache FILE] [--json]
"""
import argparse
import json
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import webdip_episodes as we  # noqa: E402
from diplodocus_fit import ask  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "players" / "castlereagh"))
from castlereagh.dipmap import ABBREVIATION  # noqa: E402


def webdip(o):
    return {"type": o["type"], "terrID": int(o["terrID"]), "toTerrID": int(o["toTerrID"] or 0),
            "fromTerrID": int(o["fromTerrID"] or 0),
            "viaConvoy": "Yes" if o.get("viaConvoy") in (True, "Yes") else "No"}


def sig(plan):
    return tuple(sorted((o["type"], o["terrID"], o["toTerrID"], o["fromTerrID"]) for o in plan))


def decisions(rows):
    """{turn: press policy} from the seat's movement decision lines."""
    return {int(r["turn"]): r.get("press_policy") or {} for r in rows
            if r.get("event") == "decision" and r.get("phase") == "Diplomacy"}


def jobs_for(ep, policy, version_id):
    episode = we.read_json_file(ep / "episode.json") if (ep / "episode.json").exists() else {}
    results_path, replay_path = we.first_existing(ep, we.RESULTS_NAMES), we.first_existing(ep, we.REPLAY_NAMES)
    if results_path is None or replay_path is None:
        return []
    results, replay = we.read_json_file(results_path), we.read_json_file(replay_path)
    countries = [int(c) for c in results["countries"]]
    logs = we.seat_log_paths(ep)
    played = {int(p["turn"]): p["orders"] for p in replay[-1]["history"]["phases"] if p["phase"] == "Diplomacy"}
    jobs = []
    for slot, name in we.seat_policies(ep, episode).items():
        path = logs.get(slot)
        if name != policy or path is None or version_id not in path.name:
            continue
        policies = decisions(we.read_log(path))
        seen = set()
        for frame in replay:
            turn = int(frame["lifecycle"]["turn"])
            if frame["lifecycle"]["phase"] != "Diplomacy" or turn not in played or turn in seen:
                continue
            seen.add(turn)
            me = countries[slot]
            ours = [webdip(o) for o in played[turn] if int(o["countryID"]) == me]
            if not ours:
                continue
            others = defaultdict(list)
            for o in played[turn]:
                if int(o["countryID"]) != me:
                    others[str(int(o["countryID"]))].append(webdip(o))
            jobs.append({"episode": ep.name, "slot": slot, "country": me, "turn": turn, "frame": frame,
                         "ours": ours, "others": dict(others), "policy": policies.get(turn)})
    return jobs


def run(server, job):
    f = job["frame"]
    base = {"game_key": f"regret-{job['episode']}", "country_id": job["country"], "end_year": 1908,
            "turn": job["turn"], "phase": "Diplomacy", "variant": f["variant"], "history": f["history"],
            "board": f["game"], "temperature": 0.75, "top_p": 0.95, "checkpoint": "diplodocus_low_rl_policy.ckpt"}
    samples = ask(server, {**base, "stage": "samples", "n": 32})["samples"].get(str(job["country"]), [])
    candidates, seen = [job["ours"]], {sig(job["ours"])}
    for plan in samples:
        plan = [webdip(o) for o in plan]
        if sig(plan) not in seen:
            seen.add(sig(plan))
            candidates.append(plan)
    ante = ask(server, {**base, "stage": "values", "n": 16, "candidates": candidates})["values"]
    post = ask(server, {**base, "stage": "values", "n": 1, "candidates": candidates,
                        "opponents": [job["others"]]})["values"]
    top = max(range(1, len(candidates)), key=lambda k: ante[k]) if len(candidates) > 1 else 0
    policy = job["policy"]
    territories = {t["id"]: t for t in f["variant"]["territories"]}
    province = {i: ABBREVIATION[territories[t["coastParentID"]]["name"]] for i, t in territories.items()}
    forbidden = set(policy.get("forbid_moves_into") or []) if policy else set()
    unit_terrs = {o["terrID"] for o in job["ours"]}
    return {"episode": job["episode"], "slot": job["slot"], "turn": job["turn"], "year": 1901 + job["turn"] // 2,
            "units": len(job["ours"]), "candidates": len(candidates),
            "played_in_samples": sig(job["ours"]) in {sig([webdip(o) for o in p]) for p in samples},
            "ante_played": ante[0], "ante_top": ante[top], "post_played": post[0], "post_top": post[top],
            "post_best": max(post[1:]) if len(post) > 1 else post[0],
            "committed": policy is not None and bool(policy),
            "pins": len(policy.get("require_orders") or []) if policy else 0,
            "forbids": len(policy.get("forbid_moves_into") or []) if policy else 0,
            "allies": sum(1 for s in (policy.get("stances") or {}).values() if s == "ally") if policy else 0,
            "forbids_bind": any(o["type"] == "Move" and province[o["toTerrID"]] in forbidden
                                for o in candidates[top]),
            "unit_terrs": len(unit_terrs)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="+", type=Path)
    ap.add_argument("--policy", required=True, help="NAME:vN as episode.json names it")
    ap.add_argument("--version-id", required=True, help="prefix of the version id in our seat log file names")
    ap.add_argument("--server", action="append", required=True)
    ap.add_argument("--cache", type=Path)
    ap.add_argument("--with-forbids", action="store_true", help="only phases whose policy forbade a province")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows, done = [], set()
    if args.cache and args.cache.exists():
        for line in args.cache.open():
            r = json.loads(line)
            rows.append(r)
            done.add((r["episode"], r["slot"], r["turn"]))
    jobs = [j for d in args.dirs for ep in we.episode_dirs(d) for j in jobs_for(ep, args.policy, args.version_id)
            if (j["episode"], j["slot"], j["turn"]) not in done
            and (not args.with_forbids or (j["policy"] or {}).get("forbid_moves_into"))]
    print(f"{len(jobs)} movement phases ({len(done)} cached)", file=sys.stderr)
    out = args.cache.open("a") if args.cache else None
    with ThreadPoolExecutor(2 * len(args.server)) as pool:
        for k, row in enumerate(pool.map(lambda ij: run(args.server[ij[0] % len(args.server)], ij[1]),
                                         enumerate(jobs))):
            rows.append(row)
            if out:
                out.write(json.dumps(row) + "\n")
                out.flush()
            if k % 50 == 49:
                print(f"  {k + 1} of {len(jobs)}", file=sys.stderr)

    def table(group):
        agg = defaultdict(list)
        for r in rows:
            agg[group(r)].append(r)
        out = {}
        for g, rs in sorted(agg.items(), key=lambda kv: str(kv[0])):
            n = len(rs)
            ante = [r["ante_played"] - r["ante_top"] for r in rs]
            post = [r["post_played"] - r["post_top"] for r in rs]
            se = (sum((x - sum(post) / n) ** 2 for x in post) / max(n - 1, 1)) ** 0.5 / n ** 0.5
            out[str(g)] = {"phases": n, "played_minus_alone_ante": round(sum(ante) / n, 4),
                           "played_minus_alone_post": round(sum(post) / n, 4), "post_se": round(se, 4),
                           "hindsight_gap": round(sum(r["post_best"] - r["post_played"] for r in rs) / n, 4)}
        return out

    report = {"all": table(lambda r: "all"),
              "by_pins": table(lambda r: "no commit" if not r["committed"] else
                               "0 pins" if r["pins"] == 0 else "1-2 pins" if r["pins"] <= 2 else "3+ pins"),
              "by_forbids": table(lambda r: "no commit" if not r["committed"] else
                                  "0 forbids" if r["forbids"] == 0 else "1-2 forbids" if r["forbids"] <= 2
                                  else "3+ forbids"),
              "by_forbids_binding": table(lambda r: "no forbids" if not r["forbids"] else
                                          "Diplodocus alone moves into a forbidden province" if r.get("forbids_bind")
                                          else "forbids do not bind"),
              "by_year": table(lambda r: r["year"])}
    if args.json:
        print(json.dumps(report, indent=1))
        return
    for name, t in report.items():
        print(f"\n## {name}\n\n| group | phases | played - Diplodocus alone, ex ante | ex post | ± SE | hindsight gap |")
        print("|---|---|---|---|---|---|")
        for g, v in t.items():
            print(f"| {g} | {v['phases']} | {v['played_minus_alone_ante']:+.4f} | "
                  f"{v['played_minus_alone_post']:+.4f} | {v['post_se']:.4f} | {v['hindsight_gap']:.4f} |")


if __name__ == "__main__":
    main()
