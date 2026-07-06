"""Visualization helpers for synthetic umbrella pricing outputs."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
CARRIER_PALETTE = {
    "Carrier_A": "#4f7ecb",
    "Carrier_B": "#d9904f",
    "Carrier_C": "#5a9b73",
}
CARRIER_LABELS = {
    "Carrier_A": "Carrier A",
    "Carrier_B": "Carrier B",
    "Carrier_C": "Our Portfolio",
}


def _save(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_price_distribution_by_carrier(df, filename="price_distribution_by_carrier.png"):
    fig, ax = plt.subplots(figsize=(10, 5.6))
    bins = np.arange(400, 2001, 100)
    bucket_labels = [f"${int(start)}-${int(end)}" for start, end in zip(bins[:-1], bins[1:])]
    x = np.arange(len(bucket_labels))
    offsets = {"Carrier_A": -0.27, "Carrier_B": 0, "Carrier_C": 0.27}
    for carrier, carrier_df in df.groupby("carrier"):
        clipped = carrier_df["simulated_price"]
        counts, _ = np.histogram(clipped, bins=bins)
        percentages = counts / len(carrier_df) * 100
        color = CARRIER_PALETTE.get(carrier, "#2563eb")
        ax.bar(
            x + offsets.get(carrier, 0),
            percentages,
            width=0.25,
            label=CARRIER_LABELS.get(carrier, carrier),
            color=color,
            alpha=0.86,
        )
    ax.set_title("Simulated Personal Umbrella Price Distribution by Carrier")
    ax.set_xlabel("Simulated Annual Price Bucket")
    ax.set_ylabel("Percentage of Portfolio")
    ax.set_ylim(bottom=0)
    ax.set_xticks(x)
    ax.set_xticklabels(bucket_labels, rotation=35, ha="right")
    ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0f}%")
    ax.legend(title="")
    ax.grid(axis="y", alpha=0.25)
    return _save(fig, filename)


def plot_segment_comparison(df, filename="segment_price_comparison.png"):
    sample = df.groupby(["risk_segment", "carrier"], observed=True, as_index=False).agg(avg_price=("simulated_price", "mean"))
    sample["carrier_label"] = sample["carrier"].map(CARRIER_LABELS).fillna(sample["carrier"])
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    palette = {CARRIER_LABELS[key]: value for key, value in CARRIER_PALETTE.items()}
    sns.barplot(data=sample, x="risk_segment", y="avg_price", hue="carrier_label", palette=palette, ax=ax)
    ax.set_title("Average Simulated Price by Risk Segment")
    ax.set_xlabel("")
    ax.set_ylabel("Average Simulated Price")
    ax.set_ylim(400, max(620, sample["avg_price"].max() + 20))
    ax.legend(title="")
    return _save(fig, filename)


def plot_geographic_heatmap(df, filename="geographic_price_heatmap.png"):
    state_avg = df.groupby(["state_code", "carrier"], as_index=False).agg(avg_price=("simulated_price", "mean"))
    pivot = state_avg.pivot(index="state_code", columns="carrier", values="avg_price")
    fig, ax = plt.subplots(figsize=(8.5, 6.2))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("State-Level Average Simulated Price by Carrier")
    ax.set_xlabel("")
    ax.set_ylabel("Synthetic State")
    return _save(fig, filename)


def plot_sensitivity_tornado(tornado_df, filename="sensitivity_tornado_chart.png"):
    top = tornado_df.groupby("driver", as_index=False)["price_spread"].mean().sort_values("price_spread")
    fig, ax = plt.subplots(figsize=(9, 5.3))
    ax.barh(top["driver"], top["price_spread"], color="#2563eb")
    ax.set_title("Synthetic Pricing Driver Sensitivity")
    ax.set_xlabel("Average Price Spread Across Levels")
    ax.set_ylabel("")
    return _save(fig, filename)


def plot_price_trends_by_coverage(df, filename="price_trend_simulation.png"):
    trend = df.groupby(["coverage_limit", "carrier"], as_index=False).agg(avg_price=("simulated_price", "mean"))
    order = ["1M", "2M", "5M"]
    trend["coverage_limit"] = pd.Categorical(trend["coverage_limit"], order, ordered=True)
    trend = trend.sort_values("coverage_limit")
    fig, ax = plt.subplots(figsize=(9, 5.2))
    sns.lineplot(data=trend, x="coverage_limit", y="avg_price", hue="carrier", marker="o", linewidth=2.5, ax=ax)
    ax.set_title("Coverage Limit Sensitivity by Carrier")
    ax.set_xlabel("Coverage Limit")
    ax.set_ylabel("Average Simulated Price")
    return _save(fig, filename)


def plot_relative_price_position(df, filename="relative_price_position.png"):
    rel = df.groupby("carrier", as_index=False).agg(avg_rank=("carrier_rank", "mean"), avg_gap=("pct_gap_to_market_avg", "mean"))
    fig, ax = plt.subplots(figsize=(8, 4.8))
    sns.barplot(data=rel, x="carrier", y="avg_gap", palette="viridis", ax=ax)
    ax.axhline(0, color="#111827", linewidth=1)
    ax.set_title("Average Price Gap Versus Market Average")
    ax.set_xlabel("")
    ax.set_ylabel("Average Percent Gap")
    return _save(fig, filename)
