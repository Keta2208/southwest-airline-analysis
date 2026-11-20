# Southwest vs. American Airlines: Competitive Performance

A course project (IDS 567, Business Visualization, UIC) that benchmarks Southwest Airlines (WN) against American Airlines (AA) on a year of U.S. flight data, with a focus on delays. The data is prepared in Python and explored in Tableau.

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

## Notes on the data

- `OnTime` is 1 when the arrival delay is 0 minutes or less (the flight arrived on time or early). It is stricter than the usual airline standard of arriving within 15 minutes of schedule; the 15-minute flag is kept as `ArrivalDelay15`.
- The cleaned Southwest file has no cancelled or diverted flights, because those flights have no delay values and are removed in the cleaning step. Cancellation and diversion counts are in the combined file.
- Delays below -60 minutes are treated as invalid and removed.

## Run it yourself

```
pip install -r requirements.txt
```

1. Download the 12 monthly BTS files for 2024 into one folder.
2. Open notebook 01, set `path`, and run it to create the combined file.
3. Open notebook 02, set `path`, and run it to create the cleaned Southwest file.
4. Open the `.twbx` in Tableau (Desktop or Public) to explore the dashboards.

## Tools

Python (pandas, NumPy) · Tableau · Google Colab
