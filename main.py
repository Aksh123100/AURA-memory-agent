"""
AURA Simulator — entry point.
Run:  python simulator/main.py
"""

import sys
from pathlib import Path

# Allow imports from the simulator/ package regardless of CWD
sys.path.insert(0, str(Path(__file__).parent))

from data_generator import generate_logs, generate_weekly_profile, save_data
from visualize import generate_all_plots


def print_summary(df) -> None:
    import pandas as pd

    print("\n" + "=" * 52)
    print("  AURA Simulator — Data Summary")
    print("=" * 52)

    total_sessions = len(df)
    unique_apps    = df["app_name"].nunique()
    anomaly_days   = df[df["is_anomaly"] == 1]["timestamp"].apply(lambda t: t[:10] if isinstance(t, str) else str(t.date())).nunique()
    most_used_app  = df["app_name"].value_counts().idxmax()
    most_used_cnt  = df["app_name"].value_counts().max()

    # Peak usage hour — hour with most sessions across all days
    df2 = df.copy()
    df2["hour"] = df2["hour"].astype(int)
    peak_hour = df2.groupby("hour").size().idxmax()

    print(f"  Total sessions   : {total_sessions:,}")
    print(f"  Unique apps used : {unique_apps}")
    print(f"  Anomaly days     : {anomaly_days}")
    print(f"  Most used app    : {most_used_app}  ({most_used_cnt:,} sessions)")
    print(f"  Peak usage hour  : {peak_hour:02d}:00 – {peak_hour+1:02d}:00")
    print("=" * 52)

    # Top-5 apps by category
    print("\n  Sessions by category:")
    for cat, cnt in df["category"].value_counts().items():
        pct = cnt / total_sessions * 100
        print(f"    {cat:<18}  {cnt:>6,}  ({pct:.1f}%)")

    print("\n  Top 5 apps:")
    for app, cnt in df["app_name"].value_counts().head(5).items():
        print(f"    {app:<20}  {cnt:>6,}")
    print()


def main():
    print("=" * 52)
    print("  AURA Simulator starting …")
    print("=" * 52)

    # Step 1 — generate synthetic usage logs
    print("\n[1/3] Generating 90-day usage logs …")
    df = generate_logs()

    # Step 2 — save CSV + weekly profile JSON
    print("[2/3] Saving data …")
    profile = generate_weekly_profile(df)
    save_data(df, profile)

    # Step 3 — generate visualisation plots
    print("[3/3] Creating plots …")
    generate_all_plots(df)

    # Summary
    print_summary(df)
    print("All done!  Check data/ and results/ for outputs.\n")


if __name__ == "__main__":
    main()
