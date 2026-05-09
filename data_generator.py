"""
Data generator for AURA simulator.
Produces 90 days of synthetic app-usage logs and a weekly profile summary.
"""

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from app_catalog import APP_BY_NAME
from user_profile import sample_app

# ── Config ────────────────────────────────────────────────────────────────────
SEED = 42
START_DATE = datetime(2025, 1, 1)
NUM_DAYS = 90
ANOMALY_DAYS_PER_MONTH = 2          # 2 random anomaly days per calendar month
SESSIONS_PER_HOUR_MEAN = 2.5        # average app-open events per active hour
SESSIONS_PER_HOUR_STD  = 1.0

DATA_DIR    = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results"


def _pick_anomaly_days(start: datetime, num_days: int,
                       per_month: int, rng) -> dict[int, int]:
    """Return {day_index: anomaly_variant} for anomaly days across the window."""
    anomaly_map: dict[int, int] = {}
    months_seen: dict[tuple[int, int], list[int]] = {}

    for i in range(num_days):
        d = start + timedelta(days=i)
        key = (d.year, d.month)
        months_seen.setdefault(key, []).append(i)

    variant = 0
    for days_in_month in months_seen.values():
        chosen = rng.choice(days_in_month,
                            size=min(per_month, len(days_in_month)),
                            replace=False)
        for day_idx in chosen:
            anomaly_map[day_idx] = variant % 4
            variant += 1

    return anomaly_map


def generate_logs(seed: int = SEED) -> pd.DataFrame:
    """Generate 90 days of per-session usage logs and return as a DataFrame."""
    rng = np.random.default_rng(seed)
    anomaly_days = _pick_anomaly_days(START_DATE, NUM_DAYS,
                                      ANOMALY_DAYS_PER_MONTH, rng)
    records = []

    for day_idx in range(NUM_DAYS):
        date = START_DATE + timedelta(days=day_idx)
        dow  = date.weekday()   # 0=Mon … 6=Sun
        is_anomaly = day_idx in anomaly_days
        anomaly_variant = anomaly_days.get(day_idx, 0)

        # Simulate each hour of the day
        for hour in range(24):
            n_sessions = max(0, int(rng.normal(SESSIONS_PER_HOUR_MEAN,
                                               SESSIONS_PER_HOUR_STD)))
            for _ in range(n_sessions):
                app_name = sample_app(hour, dow, rng, is_anomaly, anomaly_variant)
                if app_name is None:
                    continue

                app = APP_BY_NAME[app_name]

                # Jitter session duration ±40% around the app's average
                raw_duration = app["avg_session_duration"]
                duration = max(10, int(rng.normal(raw_duration, raw_duration * 0.4)))

                # Random minute within the hour
                minute = int(rng.integers(0, 60))
                ts = date.replace(hour=hour, minute=minute, second=0)

                records.append({
                    "timestamp":        ts.strftime("%Y-%m-%d %H:%M:%S"),
                    "app_name":         app_name,
                    "category":         app["category"],
                    "session_duration":  duration,
                    "memory_mb":        app["avg_memory_mb"],
                    "day_of_week":      dow,
                    "hour":             hour,
                    "is_anomaly":       int(is_anomaly),
                })

    df = pd.DataFrame(records).sort_values("timestamp").reset_index(drop=True)
    return df


def generate_weekly_profile(df: pd.DataFrame) -> dict:
    """
    Summarise average sessions per (app, day_of_week, hour) slot.
    Returns a nested dict: {app_name: {dow_hour_key: avg_sessions}}.
    """
    grouped = (df.groupby(["app_name", "day_of_week", "hour"])
                 .size()
                 .reset_index(name="total_sessions"))

    # Normalise by number of weeks (~13 weeks for 90 days)
    num_weeks = NUM_DAYS / 7
    grouped["avg_sessions"] = grouped["total_sessions"] / num_weeks

    profile: dict = {}
    for _, row in grouped.iterrows():
        app  = row["app_name"]
        key  = f"dow{int(row['day_of_week'])}_h{int(row['hour'])}"
        profile.setdefault(app, {})[key] = round(row["avg_sessions"], 3)

    return profile


def save_data(df: pd.DataFrame, profile: dict) -> None:
    """Persist the logs CSV and weekly profile JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = DATA_DIR / "usage_logs.csv"
    df.to_csv(csv_path, index=False)
    print(f"  Saved usage logs  → {csv_path}  ({len(df):,} rows)")

    json_path = DATA_DIR / "weekly_profile.json"
    with open(json_path, "w") as f:
        json.dump(profile, f, indent=2)
    print(f"  Saved weekly profile → {json_path}")


if __name__ == "__main__":
    print("[data_generator] Generating logs …")
    df = generate_logs()
    profile = generate_weekly_profile(df)
    save_data(df, profile)
