"""Summary statistics for the Southwest (WN) vs. American (AA) comparison.

Usage:  python analysis/summary_stats.py path/to/combined_airline_data.csv

Definitions
- Completed flight: not cancelled, not diverted, and has an arrival delay.
- Delayed flight: arrival delay of 15 minutes or more (the standard airline measure).
- Delay causes are only reported by BTS for flights delayed 15+ minutes.
"""
import sys
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

path = sys.argv[1] if len(sys.argv) > 1 else "combined_airline_data.csv"
df = pd.read_csv(path, low_memory=False, parse_dates=["FlightDate"])
df["Month"] = df["FlightDate"].dt.month

done = df[(df.Cancelled == 0) & (df.Diverted == 0) & df.ArrDelay.notna()]
late = done[done.ArrDelay >= 15]
g, gd = df.groupby("Reporting_Airline"), done.groupby("Reporting_Airline")

summary = pd.DataFrame({
    "flights": g.size(),
    "cancel_rate_%": g.Cancelled.mean() * 100,
    "divert_rate_%": g.Diverted.mean() * 100,
    "avg_dep_delay_min": gd.DepDelay.mean(),
    "avg_arr_delay_min": gd.ArrDelay.mean(),
    "median_arr_delay_min": gd.ArrDelay.median(),
    "arrivals_15plus_late_%": gd.ArrDelay.apply(lambda s: (s >= 15).mean() * 100),
    "avg_delay_when_15plus_min": late.groupby("Reporting_Airline").ArrDelay.mean(),
    "avg_taxi_out_min": gd.TaxiOut.mean(),
    "avg_taxi_in_min": gd.TaxiIn.mean(),
})
print("\n== Overall ==")
print(summary.round(2).T)

causes = ["CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]
tot = late.groupby("Reporting_Airline")[causes].sum()
print("\n== Share of delay minutes by cause (flights delayed 15+ min), % ==")
print((tot.div(tot.sum(axis=1), axis=0) * 100).round(1))

print("\n== Average arrival delay by month (min) ==")
print(done.groupby(["Month", "Reporting_Airline"]).ArrDelay.mean().unstack().round(1))
print("\n== Cancellation rate by month (%) ==")
print((df.groupby(["Month", "Reporting_Airline"]).Cancelled.mean().unstack() * 100).round(2))

print("\n== Hub concentration: share of departures from top 5 origin airports, % ==")
for a, d in df.groupby("Reporting_Airline"):
    s = d.Origin.value_counts(normalize=True)
    print(a, round(s.head(5).sum() * 100, 1), "| top 3:", {k: round(v * 100, 1) for k, v in s.head(3).items()},
          "| origin airports:", d.Origin.nunique())
