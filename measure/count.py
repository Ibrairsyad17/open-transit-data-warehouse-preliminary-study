"""Count the measurement runs for the four guesses in PLAN.md.

Reads the runs in measure/results/ and the archive check in
research/archive-coverage.csv. The first two runs are the evidence for the verdicts in
PROBLEM.md; the third is the check run, which kept its raw downloads, and the fourth a fresh run on
22 October 2026 from the laptop, for the newest numbers in the proposal. The five hand-checked feeds are in hand-checks.md;
they were checked by hand, so they aren't counted here.

Usage:
    python measure/count.py

Writes measure/counts.md and prints its table. Needs only Python 3.
"""
import csv
from pathlib import Path

HERE = Path(__file__).parent
RUNS = [  # (when, file in results/, the run 12 hours away that "running in the other" compares with)
    ("21:09 Jakarta, 7 Oct 2026", "2026-10-07T1410Z.csv", 1),
    ("09:01 Jakarta, 8 Oct 2026", "2026-10-08T0201Z.csv", 0),
    ("21:12 Jakarta, 8 Oct 2026, check run with raw downloads", "2026-10-08T1413Z.csv", 1),
    ("11:35 Jakarta, 22 Oct 2026, fresh run from the laptop with raw downloads", "2026-10-22T0435Z.csv", 2),
]
KEY_FIELDS = {"no_route_id": "Route", "no_trip_id": "Trip", "no_timestamp": "Timestamp"}
STALE_CUTOFF = 0.01  # the guess that the data has real errors is dropped below 1% (PLAN.md)


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def share(part, whole):
    digits = 2 if 0 < part / whole < 0.01 else 1
    return f"{part:,} of {whole:,} ({part / whole:.{digits}%})"


def count(rows, other_rows, all_feeds, archived):
    answered = [r for r in rows if r["vehicles"] != ""]
    running = [r for r in answered if int(r["vehicles"]) > 0]
    vehicles = sum(int(r["vehicles"]) for r in running)
    not_reached = all_feeds - len(answered)
    running_in_other = {r["mdb_id"] for r in other_rows if r["vehicles"] not in ("", "0")}

    def all_empty(r, key):
        return int(r[key]) == int(r["vehicles"])

    gaps = sum(any(all_empty(r, key) for key in KEY_FIELDS) for r in running)
    stale = sum(int(r["stale"]) for r in running)
    return {
        "Feeds tried": f"{len(rows)} of {all_feeds}",
        "No usable answer": len(rows) - len(answered),
        "Answered with no vehicles": len(answered) - len(running),
        "Sent vehicles": f"{len(running)} feeds, {vehicles:,} vehicles",
        "**Live data disappears, and nobody keeps the history**": "",
        "Feeds that sent vehicles and have a public archive": share(
            sum(r["mdb_id"] in archived for r in running), len(running)),
        "**Agencies fill in the same standard differently**": "",
        "Feeds that sent vehicles and left a key field empty for every vehicle": share(gaps, len(running)),
        **{f"{name} empty for every vehicle": sum(all_empty(r, key) for r in running)
           for key, name in KEY_FIELDS.items()},
        "The same, if every feed not reached had sent vehicles with nothing empty": share(
            gaps, len(running) + not_reached),
        "**The data has real errors**": "",
        "Vehicles over 65 seconds old": share(stale, vehicles),
        "Vehicles at (0, 0)": share(sum(int(r["zero_position"]) for r in running), vehicles),
        "For old vehicles to fall under 1%, the feeds not reached would need this many vehicles with no errors":
            f"more than {round(stale / STALE_CUTOFF) - vehicles:,}",
        "**Some data that looks broken isn't**": "",
        "Feeds empty in this run and running in the other": sum(
            r["vehicles"] == "0" and r["mdb_id"] in running_in_other for r in rows),
    }


def main():
    all_feeds = len(read(HERE / "feeds.csv"))
    archived = {r["mdb_id"] for r in read(HERE.parent / "research" / "archive-coverage.csv")
                if r["archive_status"] == "public archive"}
    runs = [read(HERE / "results" / name) for _, name, _ in RUNS]
    counts = [count(runs[i], runs[other], all_feeds, archived) for i, (_, _, other) in enumerate(RUNS)]

    table = ["| | " + " | ".join(when for when, _, _ in RUNS) + " |", "|---|" + "---|" * len(RUNS)]
    table += [f"| {key} | " + " | ".join(str(c[key]) for c in counts) + " |" for key in counts[0]]
    lines = [
        "# Counts from the runs",
        "",
        "Written by [`count.py`](count.py) from the runs in [`results/`](results/) and the archive check in "
        "[`../research/archive-coverage.csv`](../research/archive-coverage.csv). Don't edit by hand. "
        "Facts only: the guesses are judged in [`../PROBLEM.md`](../PROBLEM.md), on the first two runs. "
        "The third is the check run, which kept its raw downloads; it is compared with the 09:01 run, 12 hours "
        "earlier, for the feeds empty in one run and running in the other. The fourth is a fresh run from the laptop "
        "on 22 October 2026, for the newest numbers in the proposal; it is compared with the check run, the run "
        "furthest from it in the time of day.",
        "",
        f"Of all {all_feeds} feeds, {len(archived)} have a public archive. "
        "A key field is the route, the trip or the timestamp; a feed can leave more than one empty. "
        "The feeds not reached are the plain-`http://` feeds, which the first two runs didn't try, and those with "
        "no usable answer. The archive check is the one of 8 October 2026. "
        "The local time of each empty feed in the first two runs is in [`hand-checks.md`](hand-checks.md).",
        "",
        *table,
    ]
    out_file = HERE / "counts.md"
    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(table))
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
