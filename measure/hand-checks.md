# Hand checks (step 2)

Facts only. Judging the guesses happens in step 4.

## 1. Five broken-looking feeds

**How they were picked** (rule fixed before looking at any of them): a feed looks broken when a key field (route, trip or timestamp) is empty for every vehicle in at least one of the two runs. 38 feeds did. Take the largest such feed per country, then the 5 largest of those.

**How they were checked:** each live feed was downloaded again on 8 Oct 2026 at 09:22–09:24 Jakarta, and its IDs were looked up in the agency's official schedule file (GTFS). Brest had no vehicles at that hour, so its row uses the 21:09 run.

| Feed | Empty for every vehicle | What we found | Really missing? |
|---|---|---|---|
| HSL, Helsinki (Finland) | trip ID | Every vehicle has route, direction, start date and start time. Together they match exactly one scheduled trip for 361 of 384 vehicles (94%). The other 23 use route codes (such as `100HA`) that aren't in the public schedule | No, it's somewhere else (for 94%) |
| ZTP Kraków trams (Poland) | route ID | 5 of the 6 live trip IDs are in the official schedule, which gives their routes (16, 22, 70, 74). One isn't. Only 6 trams were running at 04:22 local time | No, it's somewhere else (for 5 of 6) |
| Brest métropole (France) | vehicle timestamp | None of the 107 vehicles has its own timestamp. The feed has one timestamp for the whole download, 58 seconds old | Partly: only a feed-wide time is left |
| BAS.MY Kota Bharu (Malaysia) | route ID | All 59 live trip IDs are in the official schedule, which gives their routes (D10, D11, …). One of the 60 vehicles had no trip ID. The catalog doesn't link this feed to its schedule, so they were matched by provider name | No, it's somewhere else |
| Aomori City Transport (Japan) | route ID | All 36 live trip IDs are in the official schedule, which gives their routes (A1 国道・古川線, …) | No, it's somewhere else |

**Schedule files used:**
- Kraków trams: `https://gtfs.ztp.krakow.pl/GTFS_KRK_T.zip`
- Kota Bharu: `https://api.data.gov.my/gtfs-static/mybas-kota-bharu`
- Aomori: `https://api-public.odpt.org/api/v4/files/odpt/AomoriCity/AllLines.zip?date=current`
- HSL: `https://files.mobilitydatabase.org/mdb-865/latest.zip`, MobilityData's copy, because HSL's own link is plain `http://`, which this cloud environment blocks

## 2. Feeds that were empty in one run and running in the other

105 feeds. Local time comes from each feed's time zone, found from its schedule's map area in the catalog.

| Feeds | Country | At 21:09 Jakarta | At 09:01 Jakarta |
|---:|---|---|---|
| 50 | France | running, 16:09 local | empty, 04:01 local |
| 39 | Japan | empty, 23:10 local | running, 11:01 local |
| 4 | Spain | running, 16:09 local | empty, 04:01 local |
| 4 | Canada | running, 07:09–08:09 local | empty, 19:01–20:01 local |
| 3 | United States | running, 08:10–10:10 local | empty, 20:01–22:01 local |
| 1 | Hungary | running, 16:10 local | empty, 04:01 local |
| 3 | France | running | empty. The catalog's map area for these points outside France, so their local time is unknown |
| 1 | unknown | running | empty. No map area in the catalog |
