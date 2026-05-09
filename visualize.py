"""
Visualisation module for AURA simulator.
Produces three plots and saves them to results/.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")   # headless — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

RESULTS_DIR = Path(__file__).parent.parent / "results"
DAY_LABELS  = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _load(csv_path: Path | str | None = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = Path(__file__).parent.parent / "data" / "usage_logs.csv"
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    return df


# ── Plot 1: Heatmap — app usage by hour vs day of week ───────────────────────

def plot_heatmap(df: pd.DataFrame) -> None:
    pivot = (df.groupby(["day_of_week", "hour"])
               .size()
               .unstack(fill_value=0))

    # Ensure all 24 hours are present
    pivot = pivot.reindex(columns=range(24), fill_value=0)

    fig, ax = plt.subplots(figsize=(14, 5))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd", origin="upper")

    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(24)], rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels([DAY_LABELS[i] for i in pivot.index])

    plt.colorbar(im, ax=ax, label="Total sessions")
    ax.set_title("App Usage Heatmap — Hour vs Day of Week", fontsize=13, pad=12)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")

    plt.tight_layout()
    out = RESULTS_DIR / "plot1_heatmap.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Saved → {out}")


# ── Plot 2: Top-10 most-used apps bar chart ───────────────────────────────────

def plot_top_apps(df: pd.DataFrame) -> None:
    top10 = df["app_name"].value_counts().head(10)

    # Colour bars by category
    cat_colors = {
        "Work":    "#4A90D9",
        "Social":  "#E07B4F",
        "Utility": "#5EAD7E",
        "Gaming":  "#9B59B6",
    }
    from app_catalog import APP_BY_NAME
    colors = [cat_colors.get(APP_BY_NAME[a]["category"], "#888") for a in top10.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top10.index[::-1], top10.values[::-1], color=colors[::-1], edgecolor="white")

    ax.set_xlabel("Total Sessions (90 days)")
    ax.set_title("Top 10 Most-Used Apps", fontsize=13, pad=12)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Value labels on bars
    for bar, val in zip(bars, top10.values[::-1]):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=9)

    # Legend for categories
    from matplotlib.patches import Patch
    legend_handles = [Patch(color=c, label=cat) for cat, c in cat_colors.items()]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=9)

    plt.tight_layout()
    out = RESULTS_DIR / "plot2_top_apps.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  Saved → {out}")


# ── Plot 3: Daily usage pattern for one sample week ───────────────────────────

def plot_weekly_pattern(df: pd.DataFrame) -> None:
    # Pick the first full Mon–Sun week in the dataset
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Find first Monday
    first_monday = None
    for date in sorted(df["date"].unique()):
        if pd.Timestamp(date).weekday() == 0:
            first_monday = date
            break

    week_dates = [first_monday + pd.Timedelta(days=i) for i in range(7)]
    week_df = df[df["date"].isin(week_dates)]

    # Count sessions per (date, hour)
    pivot = (week_df.groupby(["date", "hour"])
                    .size()
                    .unstack(fill_value=0)
                    .reindex(week_dates, fill_value=0))
    pivot = pivot.reindex(columns=range(24), fill_value=0)

    fig, axes = plt.subplots(7, 1, figsize=(12, 14), sharex=True)
    palette = plt.cm.tab10.colors

    for i, (date, row) in enumerate(pivot.iterrows()):
        ax = axes[i]
        ax.bar(range(24), row.values, color=palette[i % 10], edgecolor="white", width=0.8)
        ax.set_ylabel(DAY_LABELS[i], rotation=0, labelpad=32, va="center", fontsize=9)
        ax.set_ylim(0, max(pivot.values.max() + 1, 5))
        ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True, nbins=4))
        ax.spines[["top", "right"]].set_visible(False)

    axes[-1].set_xticks(range(24))
    axes[-1].set_xticklabels([f"{h:02d}h" for h in range(24)], rotation=45, ha="right", fontsize=8)
    axes[-1].set_xlabel("Hour of Day")
    fig.suptitle("Daily App-Open Events — Sample Week", fontsize=13, y=1.01)
    fig.text(0.02, 0.5, "Sessions per Hour", va="center", rotation="vertical", fontsize=10)

    plt.tight_layout()
    out = RESULTS_DIR / "plot3_weekly_pattern.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved → {out}")


def generate_all_plots(df: pd.DataFrame | None = None) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if df is None:
        df = _load()
    print("[visualize] Generating plots …")
    plot_heatmap(df)
    plot_top_apps(df)
    plot_weekly_pattern(df)
    print("[visualize] Done.")


if __name__ == "__main__":
    generate_all_plots()
