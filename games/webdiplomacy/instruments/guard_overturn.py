#!/usr/bin/env python3
"""Pin-guard verdicts that a later commit in the same phase overturned, and what the guard is worth on re-commits.

    python3 guard_overturn.py DIR --pvid 2fcc2040 [--pvid 652c80f2]

Part 1: phases whose last commit skipped the guard (time or values) after an earlier commit in that phase had
dropped own pins: do the played orders match the earlier free plan, and does the last commit re-pin a dropped pin?
Part 2: every judged re-commit (not the phase's first commit), split by whether an earlier commit dropped pins and
whether it re-pins a dropped one: drop rate and the guard's ex ante value per commit. Never prints message text.
"""
import argparse
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from webdip_episodes import read_log  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("dir", type=Path)
ap.add_argument("--pvid", action="append", required=True)
a = ap.parse_args()

seats = 0
c = Counter()
gains, overlap = [], []
res = defaultdict(list)
skipped_final = Counter()
for pv in a.pvid:
    for p in a.dir.rglob(f"policy-logs/{pv}*.log"):
        rows = read_log(p)
        seats += 1
        commits = defaultdict(list)
        for r in rows:
            if r.get("event") == "press_commit":
                commits[int(r["turn"])].append(r)
        for t, cs in commits.items():
            last = cs[-1]
            g = last.get("pin_guard")
            if g and g.get("skipped"):
                prior_drop = any((x.get("pin_guard") or {}).get("dropped") for x in cs[:-1])
                skipped_final["after an earlier drop" if prior_drop else "no earlier drop"] += 1
            for i, x in enumerate(cs):
                if i == 0:
                    continue
                gx = x.get("pin_guard")
                if not gx or "free_value" not in gx:
                    continue
                earlier_drop = any((y.get("pin_guard") or {}).get("dropped") for y in cs[:i])
                key = "after an earlier drop" if earlier_drop else "no earlier drop"
                pins_then = set()
                for y in cs[:i]:
                    pins_then |= set((y.get("pin_guard") or {}).get("dropped_orders") or [])
                pins_now = set((x.get("press_policy") or {}).get("require_orders") or [])
                if earlier_drop and pins_then & pins_now:
                    key += ", re-pins a dropped pin"
                res[key].append((gx["free_value"] - gx["pinned_value"], bool(gx.get("dropped"))))
            if not (g and g.get("skipped")):
                continue
            drops = [x for x in cs[:-1] if (x.get("pin_guard") or {}).get("dropped")]
            if not drops:
                continue
            d = drops[-1]
            dg = d["pin_guard"]
            free_orders = set(d["orders"])
            final_orders = set(last["orders"])
            pins_then = set(dg.get("dropped_orders") or [])
            pins_now = set((last.get("press_policy") or {}).get("require_orders") or [])
            same_free = final_orders == free_orders
            c["cases"] += 1
            c["final orders == earlier free plan"] += same_free
            c["final re-pins every earlier dropped pin"] += bool(pins_then) and pins_then <= pins_now
            c["final re-pins some earlier dropped pin"] += bool(pins_then & pins_now)
            c["forbids changed since the drop"] += (set((d.get("press_policy") or {}).get("forbid_moves_into") or [])
                                                    != set((last.get("press_policy") or {}).get("forbid_moves_into") or []))
            if not same_free:
                gains.append(dg["free_value"] - dg["pinned_value"])
                overlap.append(len(final_orders & free_orders) / max(1, len(free_orders)))

print(f"seat logs {seats}")
print(f"skipped last commits: {dict(skipped_final)}; per seat {sum(skipped_final.values())/seats:.2f}")
print("\n## Part 1: last commit skipped the guard after an earlier commit dropped pins")
print(f"  {dict(c)}; per seat {c['cases']/seats:.2f}")
if gains:
    se = statistics.stdev(gains) / math.sqrt(len(gains))
    print(f"  earlier drop's free-minus-pinned value where the played orders differ from that free plan: n {len(gains)}, "
          f"mean {statistics.fmean(gains):+.4f} (SE {se:.4f}), median {sorted(gains)[len(gains)//2]:+.4f}; "
          f"sum per seat {sum(gains)/seats:.4f}")
    print(f"  share of played orders shared with the earlier free plan: {statistics.fmean(overlap):.3f}")
print("\n## Part 2: judged re-commits (not the phase's first commit)")
for k, v in sorted(res.items()):
    g = [x[0] for x in v]
    dr = [x for x in v if x[1]]
    se = statistics.stdev(g) / math.sqrt(len(g))
    print(f"  {k}: n {len(v)}, drop rate {len(dr)/len(v):.2f}, mean free-pinned {statistics.fmean(g):+.4f} (SE {se:.4f}), "
          f"mean gain when dropped {statistics.fmean(x[0] for x in dr) if dr else 0:+.4f}, "
          f"guard value per commit {sum(x[0] for x in dr)/len(v):.4f}")
