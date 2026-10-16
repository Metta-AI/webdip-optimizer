#!/usr/bin/env python3
"""Board-level diagnosis of our seats: score by power, centre flows by year, takers, tiny games, endgame.

    python3 centre_flows.py DIR... --ours NAME[:vN] [--ours ...] [--label L] [--json OUT]

Every seat whose policy matches one of --ours is "ours". The other seats are "field". Games with a
pod_deleted seat of ours are dropped; exception-tainted seats (caught wake timeouts) are kept and flagged.
Final ownership after the last autumn is reconstructed from the last movement phase's adjudicated orders
(a unit that moved successfully, or stayed undislodged, owns the supply centre it stands on).
"""
import argparse
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
from opponent_profile import load_games  # noqa: E402

POWERS = ["England", "France", "Italy", "Germany", "Austria", "Turkey", "Russia"]
SUPPLY = {"EDI", "LON", "LVP", "BRE", "MAR", "PAR", "NAP", "ROM", "VEN", "BER", "KIE", "MUN", "BUD", "TRI", "VIE",
          "ANK", "CON", "SMY", "MOS", "SEV", "STP", "WAR", "NWY", "SWE", "DEN", "HOL", "BEL", "SPA", "POR", "TUN",
          "SER", "RUM", "BUL", "GRE"}


def year_of(turn):
    return 1901 + turn // 2


def matcher(specs):
    def ok(policy):
        for s in specs:
            if ":v" in s and policy == s:
                return True
            if ":v" not in s and (policy == s or policy.startswith(s + ":v")):
                return True
        return False
    return ok


def final_owners(game):
    """Supply-centre owners after the last adjudicated movement phase (retreats ignored)."""
    last = game.phases[-1]
    owners = dict(last["centers"])
    if last["turn"] % 2 == 0:
        return owners  # last phase is a spring: ownership does not change
    stand = {}
    for o in last["orders"]:
        if o["type"] == "move" and o["success"]:
            stand[o["to"]] = o["power"]
    for o in last["orders"]:
        moved = o["type"] == "move" and o["success"]
        if not moved and not o["dislodged"] and o["at"] not in stand:
            stand[o["at"]] = o["power"]
    supply = set(game.phases[0]["centers"]) | set(owners) | SUPPLY
    for prov, power in stand.items():
        if prov in supply:
            owners[prov] = power
    return owners


def mean_se(xs):
    if not xs:
        return None, None
    m = statistics.fmean(xs)
    se = statistics.stdev(xs) / math.sqrt(len(xs)) if len(xs) > 1 else None
    return m, se


def score_of(counts, me):
    """Sum-of-squares score from {power: centres} (no solo)."""
    if any(c >= 18 for c in counts.values()):
        return 1.0 if counts.get(me, 0) >= 18 else 0.0
    tot = sum(c * c for c in counts.values())
    return counts.get(me, 0) ** 2 / tot if tot else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dirs", nargs="+")
    ap.add_argument("--ours", action="append", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--family", action="append", help="policies that count as siblings (default: --ours)")
    ap.add_argument("--json")
    a = ap.parse_args()
    ours = matcher(a.ours)
    fam = matcher(a.family or a.ours)
    games, dropped = load_games([Path(d) for d in a.dirs], "classic-press")
    rows = []
    fidelity = Counter()
    field_by_power = defaultdict(list)
    for g in games:
        seats = {s.slot: s for s in g.seats}
        our_seats = [s for s in g.seats if ours(s.policy)]
        family_seats = [s for s in g.seats if fam(s.policy)]
        if not our_seats:
            continue
        if any("pod_deleted" in s.taint for s in family_seats):
            dropped["our pod deleted"] += 1
            continue
        pol_of_power = {s.power.upper(): s.policy for s in g.seats}
        finals = {s.power.upper(): (s.final_centers or 0) for s in g.seats}
        fo = final_owners(g)
        recon = Counter(fo.values())
        for p, c in finals.items():
            fidelity["match" if recon.get(p, 0) == c else "miss"] += 1
        for s in g.seats:
            if not fam(s.policy):
                field_by_power[s.power].append(s.score)
        # ownership snapshots: start of each spring movement phase, plus final
        spring = {year_of(ph["turn"]): ph["centers"] for ph in g.phases if ph["turn"] % 2 == 0}
        last_year = year_of(g.phases[-1]["turn"])
        snaps = dict(spring)
        snaps[last_year + 1] = fo
        for s in our_seats:
            me = s.power.upper()
            sib = [x for x in family_seats if x is not s]
            sib_power = sib[0].power.upper() if sib else None
            flows = {}
            for y in range(1901, last_year + 1):
                before, after = snaps.get(y), snaps.get(y + 1)
                if before is None or after is None:
                    continue
                gained, lost = Counter(), Counter()
                for prov, owner in after.items():
                    if owner == me and before.get(prov) != me:
                        prev = before.get(prov)
                        gained["neutral" if prev is None else ("sibling" if prev == sib_power else "field")] += 1
                for prov, owner in before.items():
                    if owner == me and after.get(prov) != me:
                        taker = after.get(prov)
                        lost[("sibling" if taker == sib_power else "field") if taker else "none"] += 1
                takers = Counter(after.get(prov) for prov, owner in before.items() if owner == me and after.get(prov) not in (me, None))
                flows[y] = {"gained": dict(gained), "lost": dict(lost),
                            "takers": {t: n for t, n in takers.items()},
                            "takers_policy": {pol_of_power.get(t, "?"): n for t, n in takers.items()},
                            "start": sum(1 for o in before.values() if o == me)}
            # elasticity: +1 centre taken from the largest field survivor; -1 centre given to the largest field survivor
            counts = {p: c for p, c in finals.items() if c > 0}
            base = score_of(counts, me)
            field_alive = {p: c for p, c in counts.items() if p != me and p != sib_power}
            plus = minus = None
            if field_alive and counts.get(me, 0) > 0 and s.score < 1.0 and not any(c >= 18 for c in counts.values()):
                big = max(field_alive, key=lambda p: field_alive[p])
                c2 = dict(counts); c2[me] += 1; c2[big] -= 1
                c2 = {p: c for p, c in c2.items() if c > 0}
                plus = score_of(c2, me) - base
                c3 = dict(counts); c3[me] -= 1; c3[big] += 1
                c3 = {p: c for p, c in c3.items() if c > 0}
                minus = base - score_of(c3, me)
            traj = [s.centers_by_year.get(y) for y in range(1901, 1909)]
            rows.append({
                "episode": g.episode, "slot": s.slot, "policy": s.policy, "power": s.power, "score": s.score,
                "final": s.final_centers, "solo": s.solo, "taint": s.taint, "traj": traj,
                "sibling": sib[0].policy if sib else None, "sibling_power": sib[0].power if sib else None,
                "sibling_score": sib[0].score if sib else None, "sibling_solo": bool(sib and sib[0].solo),
                "field_solo": any(x.solo and not fam(x.policy) for x in g.seats),
                "flows": flows, "plus1": plus, "minus1": minus,
            })
    out = {"rows": rows, "dropped": dict(dropped), "fidelity": dict(fidelity),
           "field_par": {p: statistics.fmean(v) for p, v in field_by_power.items() if v}}
    report(out, a.label)
    if a.json:
        Path(a.json).write_text(json.dumps(out))


def report(out, label):
    rows = out["rows"]
    print(f"# {label}: {len(rows)} seats of ours; dropped {out['dropped']}; final-owner reconstruction {out['fidelity']}")
    par = out["field_par"]
    print("\n## By power (score, SE, par = field seats at that power in these games)")
    print("| power | n | score | SE | par | final SC | SC<=3 | elim | solo | sibling solo | field solo |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for p in POWERS + ["ALL"]:
        rs = [r for r in rows if p == "ALL" or r["power"] == p]
        if not rs:
            continue
        m, se = mean_se([r["score"] for r in rs])
        se = se or 0.0
        fm, _ = mean_se([r["final"] or 0 for r in rs])
        tiny = sum(1 for r in rs if (r["final"] or 0) <= 3)
        elim = sum(1 for r in rs if (r["final"] or 0) == 0)
        solo = sum(1 for r in rs if r["solo"])
        ss = sum(1 for r in rs if r["sibling_solo"])
        fs = sum(1 for r in rs if r["field_solo"])
        pp = par.get(p) if p != "ALL" else statistics.fmean(par.values())
        print(f"| {p} | {len(rs)} | {m:.3f} | {se:.3f} | {pp:.3f} | {fm:.2f} | {tiny} | {elim} | {solo} | {ss} | {fs} |")
    # flows by year
    print("\n## Centre flows per seat-year (mean per seat; gains from neutral/field/sibling, losses to field/sibling)")
    print("| year | seats | start | +neutral | +field | +sibling | -field | -sibling | net | net SE |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for y in range(1901, 1909):
        fr = [r["flows"][str(y)] if str(y) in r["flows"] else r["flows"].get(y) for r in rows]
        fr = [f for f in fr if f]
        if not fr:
            continue
        g = lambda k, sub: statistics.fmean(f[k].get(sub, 0) for f in fr)
        nets = [sum(f["gained"].values()) - sum(f["lost"].values()) for f in fr]
        m, se = mean_se(nets)
        st = statistics.fmean(f["start"] for f in fr)
        se = se or 0.0
        print(f"| {y} | {len(fr)} | {st:.2f} | {g('gained','neutral'):.2f} | {g('gained','field'):.2f} | "
              f"{g('gained','sibling'):.2f} | {g('lost','field'):.2f} | {g('lost','sibling'):.2f} | {m:+.2f} | {se:.2f} |")
    pl = [r["plus1"] for r in rows if r["plus1"] is not None]
    mi = [r["minus1"] for r in rows if r["minus1"] is not None]
    if pl:
        m1, s1 = mean_se(pl)
        m2, s2 = mean_se(mi)
        print(f"\nScore value of one final centre (taken from / given to the largest field survivor): "
              f"+1 centre {m1:+.4f} (SE {s1:.4f}, n {len(pl)}); -1 centre {-m2:+.4f} (SE {s2:.4f}, n {len(mi)})")


if __name__ == "__main__":
    main()
