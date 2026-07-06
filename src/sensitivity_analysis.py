"""Synthetic sensitivity analysis for the pricing simulator."""

import pandas as pd


def compute_sensitivity_to_coverage_limit(df):
    return df.groupby(["carrier", "coverage_limit"], as_index=False).agg(avg_price=("simulated_price", "mean"))


def compute_sensitivity_to_prior_claims(df):
    return df.groupby(["carrier", "prior_claim_count"], as_index=False).agg(avg_price=("simulated_price", "mean"))


def compute_sensitivity_to_credit_score(df):
    return df.groupby(["carrier", "credit_score_band"], as_index=False).agg(avg_price=("simulated_price", "mean"))


def generate_tornado_style_data(df):
    """Rank simple price spreads by driver for each carrier."""
    rows = []
    drivers = ["coverage_limit", "prior_claim_count", "credit_score_band", "home_value_band", "urban_rural_flag", "youth_driver_flag"]
    for carrier, cdf in df.groupby("carrier"):
        for driver in drivers:
            means = cdf.groupby(driver)["simulated_price"].mean()
            rows.append({"carrier": carrier, "driver": driver, "price_spread": means.max() - means.min()})
    return pd.DataFrame(rows).sort_values(["carrier", "price_spread"], ascending=[True, False])


def summarize_price_drivers(df):
    data = generate_tornado_style_data(df)
    return data.groupby("driver", as_index=False)["price_spread"].mean().sort_values("price_spread", ascending=False)

