"""Visualization helpers for synthetic umbrella pricing outputs."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"


def _save(fig, filename):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_price_distribution_by_carrier(df, filename="price_distribution_by_carrier.png"):
    fig, ax = plt.subplots(figsize=(10, 5.6))
    sample = df.sample(min(len(df), 60_000), random_state=42)
    sns.histplot(data=sample, x="simulated_price", hue="carrier", bins=45, stat="density", common_norm=False, alpha=0.35, ax=ax)
    ax.set_title("Simulated Personal Umbrella Price Distribution by Carrier")
    ax.set_xlabel("Simulated Annual Price")
    ax.set_ylabel("Density")
    return _save(fig, filename)


def plot_segment_comparison(df, filename="segment_price_comparison.png"):
    sample = df.groupby(["risk_segment", "carrier"], observed=True, as_index=False).agg(avg_price=("simulated_price", "mean"))
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    sns.barplot(data=sample, x="risk_segment", y="avg_price", hue="carrier", palette="Set2", ax=ax)
    ax.set_title("Average Simulated Price by Risk Segment")
    ax.set_xlabel("")
    ax.set_ylabel("Average Simulated Price")
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
