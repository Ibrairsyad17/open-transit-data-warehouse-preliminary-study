"""Take one snapshot of many GTFS-Realtime vehicle position feeds and measure their quality.

feeds.csv lists the official, active, keyless VehiclePositions feeds in the Mobility
Database catalog as of 7 October 2026.

Usage:
    pip install -r measure/requirements.txt
    python measure/snapshot.py
    python measure/snapshot.py --recount <UTC time>

Writes measure/results/<UTC time>.csv (one row per feed), saves every download exactly as
received in measure/raw/<UTC time>/, and prints a summary. --recount counts a saved run
again from its raw downloads and names any feed whose counts differ from the saved ones.
The first two runs, 2026-10-07T1410Z and 2026-10-08T0201Z, saved no raw downloads.
"""
import argparse
import csv
import statistics
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from google.transit import gtfs_realtime_pb2

HERE = Path(__file__).parent
USER_AGENT = "open-transit-data-warehouse/0.1 (thesis research; +https://github.com/Ibrairsyad17/open-transit-data-warehouse)"
TIMEOUT_S = 20
STALE_AFTER_S = 65  # MobilityData validator rule W008: older than 65 seconds

COLUMNS = [
    "mdb_id", "country", "city", "provider", "official", "url", "fetched_at_utc",
    "http_status", "error", "bytes", "header_age_s", "vehicles", "no_position",
    "zero_position", "no_trip_id", "no_route_id", "trip_but_no_route", "no_timestamp", "stale",
]


def measure(feed):
    """Download one feed. Returns its row and the download as received (None if nothing came)."""
    row = {k: feed[k] for k in ("mdb_id", "country", "city", "provider", "official", "url")}
    now = time.time()
    # to the microsecond, so a recount from the raw download gets the same counts
    row["fetched_at_utc"] = datetime.fromtimestamp(now, timezone.utc).isoformat(timespec="microseconds")

    request = urllib.request.Request(feed["url"], headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
            row["http_status"] = response.status
            body = response.read()
    except urllib.error.HTTPError as e:
        row["http_status"] = e.code
        row["error"] = f"HTTP {e.code}"
        return row, None
    except Exception as e:  # an unreachable feed is a result, not a crash
        row["error"] = f"{type(e).__name__}: {e}"[:200]
        return row, None

    count(row, body, now)
    return row, body


def count(row, body, now):
    """Fill in a feed's counts from one download made at `now` (Unix time)."""
    row["bytes"] = len(body)
    message = gtfs_realtime_pb2.FeedMessage()
    try:
        message.ParseFromString(body)
    except Exception as e:
        row["error"] = f"not GTFS-Realtime: {e}"[:200]
        return

    if message.header.timestamp:
        row["header_age_s"] = round(now - message.header.timestamp)
    vehicles = [entity.vehicle for entity in message.entity if entity.HasField("vehicle")]
    row["vehicles"] = len(vehicles)
    row["no_position"] = sum(not v.HasField("position") for v in vehicles)
    row["zero_position"] = sum(
        v.HasField("position") and v.position.latitude == 0 and v.position.longitude == 0
        for v in vehicles
    )
    row["no_trip_id"] = sum(not v.trip.trip_id for v in vehicles)
    row["no_route_id"] = sum(not v.trip.route_id for v in vehicles)
    row["trip_but_no_route"] = sum(bool(v.trip.trip_id) and not v.trip.route_id for v in vehicles)
    row["no_timestamp"] = sum(not v.timestamp for v in vehicles)
    row["stale"] = sum(bool(v.timestamp) and now - v.timestamp > STALE_AFTER_S for v in vehicles)


def recount(stamp, results_dir, raw_dir):
    with open(results_dir / f"{stamp}.csv", newline="", encoding="utf-8") as f:
        saved = list(csv.DictReader(f))
    if not (raw_dir / stamp).is_dir():
        print(f"No raw downloads were saved for {stamp}.")
        return
    recounted, differ, missing = 0, [], []
    for old in saved:
        raw_file = raw_dir / stamp / f"{old['mdb_id']}.pb"
        if not raw_file.exists():
            if old["bytes"]:
                missing.append(old["mdb_id"])
            continue
        new = {}
        count(new, raw_file.read_bytes(), datetime.fromisoformat(old["fetched_at_utc"]).timestamp())
        recounted += 1
        if any(str(value) != old[key] for key, value in new.items()):
            differ.append(old["mdb_id"])
    print(f"Recounted {recounted} feeds from their raw downloads. Feeds whose counts differ: {len(differ)}")
    for mdb_id in differ:
        print(f"  differs: {mdb_id}")
    for mdb_id in missing:
        print(f"  raw download missing: {mdb_id}")


def summarize(rows):
    answered = [r for r in rows if "vehicles" in r]
    running = [r for r in answered if r["vehicles"] > 0]
    total = sum(r["vehicles"] for r in running)

    def share(key):
        return sum(r[key] for r in running) / total if total else 0

    def feeds_where(test):
        return [r for r in running if test(r)]

    stale_shares = [r["stale"] / r["vehicles"] for r in running]
    all_missing_route = feeds_where(lambda r: r["trip_but_no_route"] == r["vehicles"])
    some_missing_route = feeds_where(lambda r: 0 < r["trip_but_no_route"] < r["vehicles"])
    zero_position = feeds_where(lambda r: r["zero_position"] > 0)

    print(f"Feeds tried:                 {len(rows)}")
    print(f"  no usable answer:          {len(rows) - len(answered)}")
    print(f"  answered with 0 vehicles:  {len(answered) - len(running)}")
    print(f"  answered with vehicles:    {len(running)} ({total} vehicles)")
    if not running:
        return
    print(f"Stale vehicles (>{STALE_AFTER_S} s):     {share('stale'):.1%} overall, "
          f"median feed {statistics.median(stale_shares):.1%}, worst feed {max(stale_shares):.1%}")
    print(f"Vehicles at (0, 0):          {share('zero_position'):.1%} ({len(zero_position)} feeds)")
    print(f"Trip ID but no route ID:     every vehicle in {len(all_missing_route)} feeds, "
          f"some vehicles in {len(some_missing_route)} feeds")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--feeds", type=Path, default=HERE / "feeds.csv")
    parser.add_argument("--out", type=Path, default=HERE / "results")
    parser.add_argument("--raw", type=Path, default=HERE / "raw")
    parser.add_argument("--recount", metavar="UTC_TIME", help="recount a saved run, named by its file in results/")
    args = parser.parse_args()
    if args.recount:
        recount(args.recount, args.out, args.raw)
        return

    with open(args.feeds, newline="", encoding="utf-8") as f:
        feeds = list(csv.DictReader(f))
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(measure, feeds))
    rows = [row for row, _ in results]

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%MZ")
    args.out.mkdir(parents=True, exist_ok=True)
    out_file = args.out / f"{stamp}.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    raw_dir = args.raw / stamp
    raw_dir.mkdir(parents=True, exist_ok=True)
    for row, body in results:
        if body is not None:
            (raw_dir / f"{row['mdb_id']}.pb").write_bytes(body)

    summarize(rows)
    print(f"Saved: {out_file}")
    print(f"Raw downloads: {raw_dir}")


if __name__ == "__main__":
    main()
