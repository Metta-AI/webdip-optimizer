#!/usr/bin/env python3
"""Does the governor's low_reasoning level change what a model call costs? Calls grouped by the level of their phase.

    python3 governor_calls.py DIR --pvid 2fcc2040 [--pvid 652c80f2]

Each llm_call's phase is the turn in its wake id ("<turn>-<n>-<kind>"); the level is that turn's governor line.
Prints calls, reasoning tokens, completion tokens, cost per call and per phase, and how many calls carried a
reasoning_effort. Also the planned allowance against the realised spend of each level. Never prints message text.
"""
import argparse
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from webdip_episodes import read_log  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("dir", type=Path)
ap.add_argument("--pvid", action="append", required=True)
a = ap.parse_args()

calls = defaultdict(list)
phase_cost = defaultdict(list)
plan = defaultdict(list)
effort_set = 0
total = 0
for pv in a.pvid:
    for p in a.dir.rglob(f"policy-logs/{pv}*.log"):
        rows = read_log(p)
        gov = {int(r["turn"]): r for r in rows if r.get("event") == "governor"}
        per_turn = defaultdict(float)
        for r in rows:
            if r.get("event") != "llm_call" or not r.get("wake"):
                continue
            t = int(str(r["wake"]).split("-")[0])
            lv = gov[t]["level"] if t in gov else "no governor line"
            calls[lv].append(r)
            per_turn[t] += float(r.get("cost_usd") or 0)
            total += 1
            effort_set += r.get("reasoning_effort") is not None
        for t, g in gov.items():
            if g["level"] != "search_only":
                phase_cost[g["level"]].append(per_turn.get(t, 0.0))
                plan[g["level"]].append(g["allowance_usd"] / g["full_estimate_usd"] if g["full_estimate_usd"] else None)


def ms(xs):
    return f"{statistics.fmean(xs):.4f} (SE {statistics.stdev(xs)/math.sqrt(len(xs)):.4f})" if len(xs) > 1 else "n/a"


print(f"llm calls {total}; calls carrying a reasoning_effort: {effort_set}")
print("| level of the phase | calls | reasoning tokens per call | completion tokens per call | cost per call $ | phases | cost per phase $ |")
print("|---|---|---|---|---|---|---|")
for lv, cs in sorted(calls.items()):
    rt = [float(c.get("reasoning_tokens") or 0) for c in cs]
    ct = [float(c.get("completion_tokens") or 0) for c in cs]
    cu = [float(c.get("cost_usd") or 0) for c in cs]
    pc = phase_cost.get(lv, [])
    print(f"| {lv} | {len(cs)} | {statistics.fmean(rt):.1f} | {statistics.fmean(ct):.0f} | {ms(cu)} | {len(pc)} | {ms(pc) if pc else 'n/a'} |")
