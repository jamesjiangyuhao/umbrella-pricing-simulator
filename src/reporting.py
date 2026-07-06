"""Text insight generation for the synthetic pricing dashboard."""

import pandas as pd


def generate_executive_summary(df):
    avg = df.groupby("carrier")["simulated_price"].mean().sort_values()
    return f"{avg.index[0]} has the lowest average simulated premium, while {avg.index[-1]} has the highest."


def identify_best_price_position(df):
    ranks = df.groupby("carrier")["carrier_rank"].mean().sort_values()
    return ranks.index[0]


def identify_risk_segments(df):
    return df.groupby("risk_segment", observed=True)["simulated_price"].mean().sort_values(ascending=False)


def generate_pricing_recommendation(df):
    geo = df.groupby(["state_code", "carrier"])["simulated_price"].mean().reset_index()
    spread = geo.groupby("state_code")["simulated_price"].agg(lambda s: s.max() - s.min()).sort_values(ascending=False)
    return f"Review competitive positioning in {spread.index[0]}, where the simulated carrier spread is largest."


def format_insights(df):
    best = identify_best_price_position(df)
    stable = df.groupby("carrier")["simulated_price"].std().sort_values().index[0]
    segment = identify_risk_segments(df).index[0]
    return [
        generate_executive_summary(df),
        f"{best} most often holds the strongest relative price position.",
        f"{stable} is the most stable carrier across the simulated profile mix.",
        f"{segment} profiles carry the highest average simulated price.",
        generate_pricing_recommendation(df),
    ]

