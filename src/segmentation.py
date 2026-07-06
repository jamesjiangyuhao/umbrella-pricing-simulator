"""Risk segmentation helpers."""

import pandas as pd


def define_risk_segments(df):
    """Assign low, medium, and high synthetic risk segments."""
    out = df.copy()
    q1, q2 = out["risk_score"].quantile([0.4, 0.78])
    out["risk_segment"] = pd.cut(out["risk_score"], bins=[-1, q1, q2, 99], labels=["Low Risk", "Medium Risk", "High Risk"])
    return out


def bucket_profiles(df):
    """Create broader profile buckets used in reporting."""
    out = define_risk_segments(df)
    out["household_complexity"] = pd.cut(out["num_drivers"] + out["num_vehicles"], bins=[0, 4, 7, 20], labels=["Simple", "Moderate", "Complex"])
    return out


def compute_segment_statistics(df):
    """Summarize carrier pricing by risk segment."""
    out = bucket_profiles(df)
    return out.groupby(["risk_segment", "carrier"], observed=True, as_index=False).agg(
        profile_count=("profile_id", "nunique"),
        avg_price=("simulated_price", "mean"),
        avg_risk_score=("risk_score", "mean"),
    )


def compare_segments_across_carriers(df):
    """Pivot segment pricing for side-by-side comparison."""
    stats = compute_segment_statistics(df)
    return stats.pivot(index="risk_segment", columns="carrier", values="avg_price").reset_index()

