"""Benchmarking utilities for synthetic carrier price comparisons."""

import pandas as pd


def compute_relative_price_position(df):
    """Add rank and relative gap fields within each profile."""
    out = df.copy()
    out["carrier_rank"] = out.groupby("profile_id")["simulated_price"].rank(method="dense")
    avg = out.groupby("profile_id")["simulated_price"].transform("mean")
    out["price_gap_to_market_avg"] = out["simulated_price"] - avg
    out["pct_gap_to_market_avg"] = out["price_gap_to_market_avg"] / avg
    return out


def compare_to_reference_carrier(df, reference="Carrier_A"):
    """Compare each carrier price to a reference carrier for the same profile."""
    ref = df[df["carrier"] == reference][["profile_id", "simulated_price"]].rename(columns={"simulated_price": "reference_price"})
    out = df.merge(ref, on="profile_id", how="left")
    out["price_gap_vs_reference"] = out["simulated_price"] - out["reference_price"]
    out["pct_gap_vs_reference"] = out["price_gap_vs_reference"] / out["reference_price"]
    return out


def segment_price_analysis(df, group_cols):
    """Summarize price by arbitrary segment columns."""
    return (
        df.groupby(group_cols + ["carrier"], as_index=False)
        .agg(profile_count=("profile_id", "nunique"), avg_price=("simulated_price", "mean"), median_price=("simulated_price", "median"))
    )


def geographic_price_analysis(df):
    """State-level carrier comparison."""
    return segment_price_analysis(df, ["region_code", "state_code"])


def coverage_level_comparison(df):
    """Coverage-limit comparison by carrier."""
    return segment_price_analysis(df, ["coverage_limit"])


def identify_underpriced_segments(df):
    """Find segments where a carrier prices below market average."""
    rel = compute_relative_price_position(df)
    return segment_price_analysis(rel, ["carrier", "coverage_limit", "urban_rural_flag"]).sort_values("avg_price").head(10)


def identify_overpriced_segments(df):
    """Find segments where a carrier prices above market average."""
    rel = compute_relative_price_position(df)
    return segment_price_analysis(rel, ["carrier", "coverage_limit", "urban_rural_flag"]).sort_values("avg_price", ascending=False).head(10)

