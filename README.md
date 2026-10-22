# Preliminary study of 330 official GTFS-Realtime feeds, October 2026

Appendix A of the thesis proposal *Designing and Building a Data Warehouse for Monitoring Public Transport Data Quality Based on GTFS-Realtime with the Kimball Lifecycle Methodology*, by Ibrahim Irsad, Fazila Azizah Ahmad and Salsabila Rafa Ginta Beru Bangun, Bina Nusantara University, 2026, with the data and scripts behind it. The 330 official, active and keyless GTFS-Realtime vehicle-position feeds of the Mobility Database were downloaded and counted four times in October 2026, and five feeds that looked broken were checked by hand against their agencies' schedules.

The appendix, in English in [`appendix-a-en.pdf`](appendix-a-en.pdf) and in Bahasa Indonesia in [`lampiran-a-id.pdf`](lampiran-a-id.pdf), describes the study, what it found, and every file and column here. The same files are archived on Zenodo, at https://doi.org/10.5281/zenodo.23569618.

| File | What it holds |
|---|---|
| `appendix-a-en.pdf`, `lampiran-a-id.pdf` | Appendix A, in English and in Bahasa Indonesia |
| `measure/feeds.csv` | The 330 feeds, with their ID in the catalog, country, city, agency and address |
| `measure/results/` | One CSV file per run, with one row per feed, named by when the run started in UTC |
| `measure/counts.md` | Every count in the appendix's table of the runs, written by `count.py` |
| `measure/hand-checks.md` | The five feeds checked by hand, and the 105 feeds empty in one run and running in the other |
| `research/archive-coverage.csv` | The check of 8 October 2026 for a public archive of each feed |
| `measure/snapshot.py` | Downloads each feed once, counts what is in it and writes a file to `results/` |
| `measure/count.py` | Writes `counts.md` from the files in `results/` and the archive check |
| `measure/requirements.txt` | The one package `snapshot.py` needs to read GTFS-Realtime |

## Checking the numbers

`python measure/count.py`, run in this folder, writes `measure/counts.md` again from the four files in `measure/results/` and `research/archive-coverage.csv`, with Python 3 alone. `python measure/snapshot.py` makes a new run, after `pip install -r measure/requirements.txt`.

## What is left out

The raw downloads of the runs of 8 and 22 October 2026, which recount to the same numbers, aren't included, since each agency's license has to be read before its data is shared again. Some links in `counts.md` and `hand-checks.md` point to files of the project that aren't here; what they say that matters here is in the appendix.

## Citing it

Irsad, I., Ahmad, F. A., & Bangun, S. R. G. B. (2026). *Preliminary study of 330 official GTFS-Realtime vehicle position feeds, October 2026* (Version 1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23569618

[`CITATION.cff`](CITATION.cff) gives the same to GitHub's Cite this repository.

## License

[Creative Commons Attribution 4.0 International](LICENSE).
