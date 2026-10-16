#!/usr/bin/env python3
"""Do seat-years the governor left silent (search_only) go worse than talking seat-years of the same year and power?

    python3 silent_phases.py board_fg.json DIR --pvid 2fcc2040 --pvid 652c80f2

Joins centre_flows.py's per-seat flows with each seat log's `governor` levels. Also replays the governor's plan with the
low_reasoning factor set to 1.0 (what that level really cost) to count how many search_only phases would remain.
"""
import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from webdip_episodes import read_log, read_json_file  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("board")
ap.add_argument("dir")
ap.add_argument("--pvid", action="append", required=True)
a = ap.parse_args()
board = json.load(open(a.board))
by_seat = {(r["episode"], r["slot"]): r for r in board["rows"]}

levels = {}
plans = {}
costs = {}
for p in Path(a.dir).rglob("policy-logs/*.log"):
    if not any(p.name.startswith(v) for v in a.pvid):
        continue
    ep = p.parent.parent.name
    slot = int(p.name.split(".")[-2])
    rows = read_log(p)
    gov = {int(r["turn"]): r for r in rows if r.get("event") == "governor"}
    dec = {int(r["turn"]): r for r in rows if r.get("event") == "decision" and r.get("phase") == "Diplomacy"}
    levels[(ep, slot)] = {t: g["level"] for t, g in gov.items()}
    plans[(ep, slot)] = gov
    # phase cost: llm calls by wake turn
    pc = defaultdict(float)
    for r in rows:
        if r.get("event") == "llm_call" and r.get("wake"):
            pc[int(str(r["wake"]).split("-")[0])] += float(r.get("cost_usd") or 0)
    costs[(ep, slot)] = dict(pc)

pairs = defaultdict(list)  # (year, silent phases) -> list of (power, start, field_lost, net, next_field_lost)
for key, r in by_seat.items():
    lv = levels.get(key)
    if lv is None:
        continue
    for y in range(1902, 1908):
        f = r["flows"].get(str(y))
        nf = r["flows"].get(str(y + 1))
        if not f:
            continue
        silent = sum(1 for t in (2 * (y - 1901), 2 * (y - 1901) + 1) if lv.get(t) == "search_only")
        net = sum(f["gained"].values()) - sum(f["lost"].values())
        pairs[(y, silent)].append((r["power"], f["start"], f["lost"].get("field", 0), net,
                                   nf["lost"].get("field", 0) if nf else None,
                                   f["gained"].get("field", 0) + f["gained"].get("neutral", 0)))

print("## Seat-years by silent (search_only) movement phases in that year")
print("| year | silent phases | seat-years | start centres | lost to field | gained (field+neutral) | net | next year lost to field |")
print("|---|---|---|---|---|---|---|---|")
for (y, s) in sorted(pairs):
    v = pairs[(y, s)]
    m = lambda i: statistics.fmean(x[i] for x in v if x[i] is not None)
    print(f"| {y} | {s} | {len(v)} | {m(1):.2f} | {m(2):.2f} | {m(5):.2f} | {m(3):+.2f} | {m(4):.2f} |")

# matched comparison: within (year, power, start-centre band), silent>=1 minus silent==0
print("\n## Matched (same year, power, start centres within 1): seat-years with a silent phase minus talking ones")
diffs_lost, diffs_net, diffs_gain = [], [], []
cells = defaultdict(lambda: {0: [], 1: []})
for (y, s), v in pairs.items():
    for power, start, lost, net, nxt, gain in v:
        band = start // 2
        cells[(y, power, band)][1 if s else 0].append((lost, net, gain))
w_lost = w_net = w_gain = w = 0.0
var_net = 0.0
for k, c in cells.items():
    if c[0] and c[1]:
        n = min(len(c[0]), len(c[1]))
        dl = statistics.fmean(x[0] for x in c[1]) - statistics.fmean(x[0] for x in c[0])
        dn = statistics.fmean(x[1] for x in c[1]) - statistics.fmean(x[1] for x in c[0])
        dg = statistics.fmean(x[2] for x in c[1]) - statistics.fmean(x[2] for x in c[0])
        w_lost += n * dl; w_net += n * dn; w_gain += n * dg; w += n
        diffs_net.append((n, dn)); diffs_lost.append((n, dl))
if w:
    mean_net = w_net / w
    # crude SE: weighted spread of cell differences
    sd = math.sqrt(sum(n * (d - mean_net) ** 2 for n, d in diffs_net) / w)
    se = sd / math.sqrt(len(diffs_net))
    mean_lost = w_lost / w
    sdl = math.sqrt(sum(n * (d - mean_lost) ** 2 for n, d in diffs_lost) / w)
    print(f"cells {len(diffs_net)}, weight {w:.0f}: net {mean_net:+.3f} (SE about {se:.3f}); lost to field {mean_lost:+.3f} "
          f"(SE about {sdl/math.sqrt(len(diffs_lost)):.3f}); gained {w_gain/w:+.3f}")

# seat-level: number of silent phases vs final score, power-adjusted
print("\n## Seat level: silent phases in 1902-1905 vs final score (power mean removed)")
pm = defaultdict(list)
for r in board["rows"]:
    pm[r["power"]].append(r["score"])
pmean = {p: statistics.fmean(v) for p, v in pm.items()}
xs, ys = [], []
for key, r in by_seat.items():
    lv = levels.get(key)
    if lv is None:
        continue
    xs.append(sum(1 for t in range(2, 10) if lv.get(t) == "search_only"))
    ys.append(r["score"] - pmean[r["power"]])
mx, my = statistics.fmean(xs), statistics.fmean(ys)
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)
r_ = cov / (statistics.pstdev(xs) * statistics.pstdev(ys))
print(f"seats {len(xs)}, mean silent phases 1902-1905 {mx:.2f}, r with power-adjusted score {r_:+.3f} (|r| < {2/math.sqrt(len(xs)):.2f} is noise)")
for k in range(0, 9):
    sub = [y for x, y in zip(xs, ys) if x == k]
    if sub:
        print(f"  {k} silent: {len(sub)} seats, power-adjusted score {statistics.fmean(sub):+.3f}")

# governor replay with the low_reasoning factor at 1.0
print("\n## Governor replay: low_reasoning priced at what it cost (factor 1.0 instead of 0.6)")
silent_now = silent_new = 0
left_now = []
for key, gov in plans.items():
    pc = costs[key]
    turns = sorted(gov)
    if not turns:
        continue
    budget = gov[turns[0]]["budget_usd"]
    # talking-phase cost for this seat: mean of observed talking phases by year
    talk = [pc.get(t, 0.0) for t in turns if gov[t]["level"] != "search_only" and pc.get(t, 0) > 0]
    mean_talk = statistics.fmean(talk) if talk else 0.025
    stop = gov[turns[0]]["stop_at_usd"]
    spent, est, observed = 0.0, 0.025, 0
    for t in turns:
        phases = max(1, (1908 - (1901 + t // 2)) * 2 + (2 - t % 2))
        allow = (stop - spent) / phases
        level = "full" if est <= allow else ("few_wakes" if est * 0.7 <= allow else "search_only")
        silent_now += gov[t]["level"] == "search_only"
        if level == "search_only":
            silent_new += 1
            continue
        cost = pc.get(t, 0.0) if gov[t]["level"] != "search_only" else mean_talk
        if level == "few_wakes":
            cost *= 0.7
        spent += cost
        est = cost / (0.7 if level == "few_wakes" else 1.0) if not observed else 0.5 * cost / (0.7 if level == "few_wakes" else 1.0) + 0.5 * est
        observed += 1
    left_now.append(stop - sum(pc.values()))
print(f"search_only phases as played {silent_now}; in the replay {silent_new} (seats {len(plans)})")
print(f"left below the stop at game end as played: mean ${statistics.fmean(left_now):.3f}")
