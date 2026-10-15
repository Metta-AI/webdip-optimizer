#!/usr/bin/env python3
"""How well Diplodocus's sampled joint actions predict what the field actually ordered, from fetched games.

For every movement phase of every game with one of our seats, rebuilds the seat's `samples` request from the
replay frame (public `variant`, `game`, `history`), asks a local Diplodocus server for N joint actions, and
compares each other power's sampled orders with the orders the replay's history shows it played:

- order fit: per unit, the share of samples that gave the unit the order it played;
- attacks on us: per power in contact with us (a unit bordering one of our units or centres), the share of
  samples in which it moves or supports a move into one of our provinces, against whether it did.

Rows are split by our press stance toward that power in that phase (the seat log's committed policy) and by the
power's policy. The server is the pidip README's local one (`diplodocus/server/local.py`), keyed `sidecar`.

    diplodocus_fit.py DIR... --policy scott-pidip --server http://127.0.0.1:8001 [--server ...] [--n 32]
        [--limit-games N] [--cache FILE] [--json]

Counts, not causes. The samples are Diplodocus's no-press policy at the seat's sampling settings (temperature
0.75, top-p 0.95), the same draws the seat ranks its plans against.
"""
import argparse
import json
import sys
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import webdip_episodes as we  # noqa: E402

POWER_NAMES = {1: "ENGLAND", 2: "FRANCE", 3: "ITALY", 4: "GERMANY", 5: "AUSTRIA", 6: "TURKEY", 7: "RUSSIA"}


def key(o):
    return o["type"], int(o["terrID"]), int(o.get("toTerrID") or 0), int(o.get("fromTerrID") or 0)


def ask(server, request):
    body = {"model": "diplodocus-policy", "messages": [{"role": "user", "content": json.dumps(request)}]}
    req = urllib.request.Request(server.rstrip("/") + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": "Bearer sidecar"})
    with urllib.request.urlopen(req, timeout=300) as response:
        return json.loads(json.load(response)["choices"][0]["message"]["content"])


def our_stances(rows):
    """{turn: {POWER: stance}} from the seat's decision lines (the policy committed at the phase's end)."""
    out = {}
    for r in rows:
        if r.get("event") == "decision" and r.get("phase") == "Diplomacy":
            out[int(r["turn"])] = (r.get("press_policy") or {}).get("stances") or {}
    return out


def phases(ep, policy):
    """One job per movement phase of each of our seats in the episode."""
    episode = we.read_json_file(ep / "episode.json") if (ep / "episode.json").exists() else {}
    results_path, replay_path = we.first_existing(ep, we.RESULTS_NAMES), we.first_existing(ep, we.REPLAY_NAMES)
    if results_path is None or replay_path is None:
        return []
    results, replay = we.read_json_file(results_path), we.read_json_file(replay_path)
    policies = we.seat_policies(ep, episode)
    logs = we.seat_log_paths(ep)
    countries = [int(c) for c in results["countries"]]
    by_country = {countries[s]: p for s, p in policies.items()}
    played = {int(p["turn"]): p["orders"] for p in replay[-1]["history"]["phases"] if p["phase"] == "Diplomacy"}
    jobs = []
    for slot, name in policies.items():
        if not name.startswith(policy):
            continue
        stances = our_stances(we.read_log(logs.get(slot)))
        seen = set()
        for frame in replay:
            life = frame["lifecycle"]
            turn = int(life["turn"])
            if life["phase"] != "Diplomacy" or turn not in played or turn in seen:
                continue
            seen.add(turn)
            jobs.append({"episode": ep.name, "country": countries[slot], "turn": turn, "frame": frame,
                         "played": played[turn], "stances": stances.get(turn, {}), "policies": by_country})
    return jobs


def measure(job, answer):
    frame, me = job["frame"], job["country"]
    variant, game = frame["variant"], frame["game"]
    parent = {t["id"]: t["coastParentID"] for t in variant["territories"]}
    borders = defaultdict(set)
    for t in variant["territories"]:
        for b in t["borders"]:
            borders[parent[t["id"]]].add(parent[b["id"]])
    supply = {t["id"] for t in variant["territories"] if t["supply"]}
    ours = {parent[u["terrID"]] for u in game["units"] if int(u["countryID"]) == me}
    ours |= {parent[t["terrID"]] for t in game["territories"]
             if t["terrID"] in supply and t.get("ownerCountryID") and int(t["ownerCountryID"]) == me}
    near = ours | {p for o in ours for p in borders[o]}

    def attacks(orders):
        return any(o["type"] in ("Move", "Support move") and o.get("toTerrID")
                   and parent[int(o["toTerrID"])] in ours for o in orders)

    rows = []
    samples = {int(c): plans for c, plans in answer["samples"].items()}
    for c, plans in samples.items():
        if c == me:
            continue
        actual = [o for o in job["played"] if int(o["countryID"]) == c]
        if not actual or not plans:
            continue
        units = {int(o["terrID"]): key(o) for o in actual}
        hit = sum(sum(1 for plan in plans if any(key(s) == k for s in plan if int(s["terrID"]) == t)) / len(plans)
                  for t, k in units.items()) / len(units)
        contact = any(parent[int(o["terrID"])] in near for o in actual)
        power = POWER_NAMES[c]
        rows.append({"episode": job["episode"], "turn": job["turn"], "power": power,
                     "policy": job["policies"].get(c, "?"), "stance": job["stances"].get(power, "none"),
                     "units": len(units), "fit": hit, "contact": contact,
                     "sampled_attack": sum(attacks(p) for p in plans) / len(plans), "attacked": attacks(actual)})
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dirs", nargs="+", type=Path)
    ap.add_argument("--policy", required=True, help="our policy name prefix, e.g. scott-pidip")
    ap.add_argument("--server", action="append", required=True)
    ap.add_argument("--n", type=int, default=32)
    ap.add_argument("--limit-games", type=int, default=0)
    ap.add_argument("--cache", type=Path, help="JSON lines of measured rows; read first, appended to")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    done, rows = set(), []
    if args.cache and args.cache.exists():
        for line in args.cache.open():
            r = json.loads(line)
            rows.append(r)
            done.add((r["episode"], r["turn"]))
    eps = [ep for d in args.dirs for ep in we.episode_dirs(d)]
    if args.limit_games:
        eps = eps[:args.limit_games]
    jobs = [j for ep in eps for j in phases(ep, args.policy) if (j["episode"], j["turn"]) not in done]
    print(f"{len(jobs)} movement phases to sample ({len(done)} cached)", file=sys.stderr)

    def run(i_job):
        i, job = i_job
        f = job["frame"]
        request = {"stage": "samples", "game_key": f"fit-{job['episode']}", "country_id": job["country"],
                   "end_year": 1908, "turn": job["turn"], "phase": "Diplomacy", "variant": f["variant"],
                   "history": f["history"], "board": f["game"], "n": args.n, "temperature": 0.75, "top_p": 0.95,
                   "checkpoint": "diplodocus_low_rl_policy.ckpt"}
        return measure(job, ask(args.server[i % len(args.server)], request))

    out = args.cache.open("a") if args.cache else None
    with ThreadPoolExecutor(2 * len(args.server)) as pool:
        for k, new in enumerate(pool.map(run, enumerate(jobs))):
            rows += new
            if out:
                for r in new:
                    out.write(json.dumps(r) + "\n")
                out.flush()
            if k % 50 == 49:
                print(f"  {k + 1} of {len(jobs)}", file=sys.stderr)
    if out:
        out.close()

    def table(group):
        agg = defaultdict(lambda: [0, 0.0, 0, 0.0, 0])
        for r in rows:
            a = agg[group(r)]
            a[0] += 1
            a[1] += r["fit"]
            if r["contact"]:
                a[2] += 1
                a[3] += r["sampled_attack"]
                a[4] += r["attacked"]
        return {g: {"phases": a[0], "order_fit": round(a[1] / a[0], 3), "contact_phases": a[2],
                    "sampled_attack_rate": round(a[3] / a[2], 3) if a[2] else None,
                    "actual_attack_rate": round(a[4] / a[2], 3) if a[2] else None}
                for g, a in sorted(agg.items(), key=lambda kv: -kv[1][0])}

    report = {"by_stance": table(lambda r: r["stance"]), "by_policy": table(lambda r: r["policy"]),
              "all": table(lambda r: "all")}
    if args.json:
        print(json.dumps(report, indent=1))
        return
    for name, t in report.items():
        print(f"\n## {name}\n\n| group | phases | order fit | contact phases | sampled attack | actual attack |")
        print("|---|---|---|---|---|---|")
        for g, v in t.items():
            print(f"| {g} | {v['phases']} | {v['order_fit']} | {v['contact_phases']} | "
                  f"{v['sampled_attack_rate']} | {v['actual_attack_rate']} |")


if __name__ == "__main__":
    main()
