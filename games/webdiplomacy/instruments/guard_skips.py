#!/usr/bin/env python3
"""The pin guard on the commit that set each phase's orders: judged, skipped (time or values), or no own pins.

    python3 guard_skips.py DIR --pvid 2fcc2040 [--pvid 652c80f2]

For each movement phase of our seats, the last press_commit before the decision line (the orders that played,
unless a later floor or failure intervened) and the wake it came from. Never prints message text.
"""
import argparse
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from webdip_episodes import read_log  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("dir")
ap.add_argument("--pvid", action="append", required=True)
a = ap.parse_args()

final_status = Counter()
final_status_by_year = defaultdict(Counter)
by_kind = defaultdict(Counter)
gains_judged = []
gains_dropped = []
allowed = defaultdict(list)
commit_ms = []
skip_left = []
pinned_ms_skip = []
values_ms = []
for p in Path(a.dir).rglob("policy-logs/*.log"):
    if not any(p.name.startswith(v) for v in a.pvid):
        continue
    rows = read_log(p)
    wake_kind = {}
    wake_allowed = {}
    current_wake = None
    last_commit = {}
    for r in rows:
        e = r.get("event")
        if e == "wake_start":
            current_wake = r["wake"]
            wake_kind[current_wake] = r["kind"]
            wake_allowed[current_wake] = r["seconds_allowed"]
            allowed[r["kind"]].append(r["seconds_allowed"])
        elif e == "wake":
            current_wake = None
        elif e == "press_commit":
            t = int(r["turn"])
            g = r.get("pin_guard")
            kind = wake_kind.get(current_wake, "?")
            if g is None:
                st = "no own pins"
            elif g.get("skipped"):
                st = f"skipped ({g['skipped']})"
                pinned_ms_skip.append(g.get("pinned_ms"))
            elif g.get("dropped"):
                st = "dropped pins"
            else:
                st = "kept pins"
            by_kind[kind][st] += 1
            if g is not None and "free_value" in g:
                gains_judged.append(g["free_value"] - g["pinned_value"])
                if g.get("dropped"):
                    gains_dropped.append(g["free_value"] - g["pinned_value"])
            last_commit[t] = (st, kind)
    for t, (st, kind) in last_commit.items():
        final_status[st] += 1
        final_status_by_year[1901 + t // 2][st] += 1

print("## Every commit's guard outcome, by the wake it came from")
for k, c in by_kind.items():
    tot = sum(c.values())
    print(f"  {k}: {tot} commits; " + ", ".join(f"{s} {n} ({n/tot:.0%})" for s, n in c.most_common()))
print("\n## The last commit of each phase (the orders that played)")
tot = sum(final_status.values())
print("  " + ", ".join(f"{s} {n} ({n/tot:.1%})" for s, n in final_status.most_common()))
for y in sorted(final_status_by_year):
    c = final_status_by_year[y]
    t = sum(c.values())
    print(f"  {y}: {t} phases; " + ", ".join(f"{s} {n}" for s, n in c.most_common()))
print("\n## Judged commits: free minus pinned value")
gj = gains_judged
print(f"  n {len(gj)}, mean {statistics.fmean(gj):+.4f}; dropped n {len(gains_dropped)} mean gain {statistics.fmean(gains_dropped):+.4f}; "
      f"drop rate {len(gains_dropped)/len(gj):.1%}")
print(f"  expected value lost per skipped final commit at the judged drop rate and mean dropped gain: "
      f"{len(gains_dropped)/len(gj)*statistics.fmean(gains_dropped):.4f}")
print("\n## Wake seconds allowed")
for k, v in allowed.items():
    v = sorted(v)
    print(f"  {k}: n {len(v)}, median {v[len(v)//2]:.0f} s, p10 {v[len(v)//10]:.0f} s, p90 {v[9*len(v)//10]:.0f} s")
ps = sorted(x for x in pinned_ms_skip if x is not None)
if ps:
    print(f"  pinned search ms in skipped commits: median {ps[len(ps)//2]}, p90 {ps[9*len(ps)//10]}")
