# Southwest vs. American Airlines: Competitive Performance

A course project (IDS 567, Business Visualization, UIC) that benchmarks Southwest Airlines (WN) against American Airlines (AA) on a full year of U.S. flight data, with a focus on delays. The data is prepared in Python and explored in Tableau.

## Key findings (2024, 2.4M flights)

Southwest operated 1,419,419 flights and American 984,306. Across the year, Southwest was the more reliable airline on every delay measure.

| Measure | Southwest (WN) | American (AA) |
|---|---|---|
| Average arrival delay | 5.1 min | 15.3 min |
| Flights arriving 15+ min late | 20.6% | 26.1% |
| Average delay, when 15+ min late | 54 min | 86 min |
| Average departure delay | 11.7 min | 20.6 min |
| Cancellation rate | 0.83% | 1.55% |
| Average taxi-out / taxi-in | 13.8 / 5.7 min | 18.5 / 9.9 min |

**1. The gap is in the long delays, not the typical flight.** The median arrival is early for both airlines (-5 min for Southwest, -4 min for American). The difference comes from the tail: when American flights run late, they run late for much longer (86 min vs. 54 min on average), which pulls its average up.

**2. American's traffic is concentrated in a few hubs; Southwest's is spread out.** American's top 5 departure airports carry 46.7% of its flights (DFW alone is 16.9%, then CLT at 12.9%). Southwest's top 5 carry 28.0%, and its busiest airport (DEN) is 6.8%. The two networks look as expected for a hub-and-spoke and a point-to-point carrier. American's busiest hub, DFW, averaged a 24.8-minute departure delay across 162,559 completed flights. American also spends more time taxiing, which is consistent with congestion at its large hubs. This is a pattern in the data, not proof of cause.

**3. A late aircraft is the largest source of delay for both airlines.** Among flights delayed 15+ minutes, late-arriving aircraft account for 51.8% of Southwest's delay minutes and 48.5% of American's. Carrier-caused delay is next (27.8% vs. 32.9%). Weather is small for both (2.4% vs. 5.4%), and security delay is under 0.5%. Delays that start with one flight carry over to the next, so the delay-recovery side of operations matters as much as the initial delay.

**4. Both airlines are worst in summer and best in the fall.** Average arrival delay peaks in May and July (American 30-32 min, Southwest 12-13 min, with June also high) and is lowest in October and November (American 2-3 min; Southwest slightly early). American's average delay is higher than Southwest's in every month of the year. Thursdays, Fridays and Sundays are the worst days for both.

**5. Cancellations are the one area where Southwest is not ahead year-round.** Southwest's yearly cancellation rate is lower, but in January its rate (3.09%) was nearly double American's (1.61%), and in October it was also higher (1.30% vs. 0.88%). American's cancellations are highest in May and August (3.46% and 2.86%).

*These are descriptive results for one year of data. They show how the two airlines differ, not why.*

## Data

- **Source:** U.S. Bureau of Transportation Statistics (BTS), *Reporting Carrier On-Time Performance*, all of 2024 (12 monthly files). This is public data, available at [transtats.bts.gov](https://www.transtats.bts.gov/).
- **Not included:** the raw monthly files and the combined file (`combined_airline_data.csv`, about 300 MB) are too large for GitHub. Download the 12 monthly files from BTS and run notebook 01 to rebuild it.
- **Included:** `data/southwest_cleaned_data.xlsx` (the cleaned Southwest-only data, 154,922 flights) and `data/field_lookup_table.xlsx` (a description of each BTS field).

## Workflow

| Step | File | What it does |
|---|---|---|
| 1 | `notebooks/01_combine_airline_csvs.ipynb` | Merges the 12 monthly files, keeps the needed columns, and filters to WN and AA. Output: `combined_airline_data.csv`, the Tableau data source. |
| 2 | `notebooks/02_clean_southwest_data.ipynb` | Cleans the Southwest-only data: selects columns, fixes data types, adds `OnTime` and `TotalDelay`, removes impossible delay values, renames columns, and exports the cleaned file. |
| 3 | `tableau/Southwest_airline_visualization_Final.twbx` | Tableau workbook with 4 dashboards and 12 worksheets: arrival and departure delay views, delay percentages, security delay, a network view, a summary table, and animated stories on departure vs. arrival delay and on taxi-in vs. departure delay. |
| 4 | `analysis/summary_stats.py` | Recalculates the numbers in the key findings above from the combined file. |

## Notes on the data

- **Definitions used in the findings:** a flight is *completed* if it was not cancelled or diverted and has an arrival delay; it is *delayed* if it arrived 15 or more minutes late (the standard airline measure). Delay causes are only reported by BTS for flights delayed 15+ minutes.
- In the cleaned Southwest file (notebook 02), `OnTime` is 1 when the arrival delay is 0 minutes or less (on time or early). That is stricter than the 15-minute standard, so the two numbers differ.
- The cleaned Southwest file has no cancelled or diverted flights, because those flights have no delay values and are removed in the cleaning step. Cancellation and diversion counts come from the combined file.
- Delays below -60 minutes are treated as invalid and removed in notebook 02.

## Run it yourself

```
pip install -r requirements.txt
```

1. Download the 12 monthly BTS files for 2024 into one folder.
2. Open notebook 01, set `path`, and run it to create the combined file.
3. Open notebook 02, set `path`, and run it to create the cleaned Southwest file.
4. Run `python analysis/summary_stats.py combined_airline_data.csv` to reproduce the findings.
5. Open the `.twbx` in Tableau (Desktop or Public) to explore the dashboards.

## Tools

Python (pandas, NumPy) · Tableau · Google Colab
