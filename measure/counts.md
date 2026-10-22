# Counts from the runs

Written by [`count.py`](count.py) from the runs in [`results/`](results/) and the archive check in [`../research/archive-coverage.csv`](../research/archive-coverage.csv). Don't edit by hand. Facts only: the guesses are judged in [`../PROBLEM.md`](../PROBLEM.md), on the first two runs. The third is the check run, which kept its raw downloads; it is compared with the 09:01 run, 12 hours earlier, for the feeds empty in one run and running in the other. The fourth is a fresh run from the laptop on 22 October 2026, for the newest numbers in the proposal; it is compared with the check run, the run furthest from it in the time of day.

Of all 330 feeds, 4 have a public archive. A key field is the route, the trip or the timestamp; a feed can leave more than one empty. The feeds not reached are the plain-`http://` feeds, which the first two runs didn't try, and those with no usable answer. The archive check is the one of 8 October 2026. The local time of each empty feed in the first two runs is in [`hand-checks.md`](hand-checks.md).

| | 21:09 Jakarta, 7 Oct 2026 | 09:01 Jakarta, 8 Oct 2026 | 21:12 Jakarta, 8 Oct 2026, check run with raw downloads | 11:35 Jakarta, 22 Oct 2026, fresh run from the laptop with raw downloads |
|---|---|---|---|---|
| Feeds tried | 317 of 330 | 317 of 330 | 330 of 330 | 330 of 330 |
| No usable answer | 64 | 61 | 72 | 24 |
| Answered with no vehicles | 69 | 118 | 66 | 83 |
| Sent vehicles | 184 feeds, 13,431 vehicles | 138 feeds, 4,227 vehicles | 192 feeds, 19,324 vehicles | 223 feeds, 14,298 vehicles |
| **Live data disappears, and nobody keeps the history** |  |  |  |  |
| Feeds that sent vehicles and have a public archive | 4 of 184 (2.2%) | 4 of 138 (2.9%) | 4 of 192 (2.1%) | 1 of 223 (0.45%) |
| **Agencies fill in the same standard differently** |  |  |  |  |
| Feeds that sent vehicles and left a key field empty for every vehicle | 23 of 184 (12.5%) | 34 of 138 (24.6%) | 28 of 192 (14.6%) | 35 of 223 (15.7%) |
| Route empty for every vehicle | 20 | 32 | 24 | 32 |
| Trip empty for every vehicle | 5 | 3 | 7 | 3 |
| Timestamp empty for every vehicle | 1 | 0 | 1 | 2 |
| The same, if every feed not reached had sent vehicles with nothing empty | 23 of 261 (8.8%) | 34 of 212 (16.0%) | 28 of 264 (10.6%) | 35 of 247 (14.2%) |
| **The data has real errors** |  |  |  |  |
| Vehicles over 65 seconds old | 1,433 of 13,431 (10.7%) | 655 of 4,227 (15.5%) | 2,225 of 19,324 (11.5%) | 1,502 of 14,298 (10.5%) |
| Vehicles at (0, 0) | 4 of 13,431 (0.03%) | 2 of 4,227 (0.05%) | 12 of 19,324 (0.06%) | 25 of 14,298 (0.17%) |
| For old vehicles to fall under 1%, the feeds not reached would need this many vehicles with no errors | more than 129,869 | more than 61,273 | more than 203,176 | more than 135,902 |
| **Some data that looks broken isn't** |  |  |  |  |
| Feeds empty in this run and running in the other | 39 | 66 | 37 | 40 |
