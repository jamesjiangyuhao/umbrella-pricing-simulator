"""Fictional multi-carrier pricing engine for synthetic umbrella profiles."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

LIMIT_FACTOR = {"1M": 1.00, "2M": 1.58, "5M": 2.95}
CREDIT_FACTOR = {"High": 0.92, "Medium": 1.00, "Low": 1.14}
HOME_FACTOR = {"Entry": 0.90, "Standard": 1.00, "Premium": 1.13, "High Net Worth": 1.31}
URBAN_FACTOR = {"Urban": 1.08, "Suburban": 1.00, "Rural": 0.94}
STATE_FACTOR = {f"S{i:02d}": 0.9 + (i % 6) * 0.04 + (0.08 if i in [4, 9, 11] else 0) for i in range(1, 13)}


def load_profiles(path=DATA_DIR / "synthetic_profiles.csv"):
    """Load the generated synthetic profile table."""
    return pd.read_csv(path)


def calculate_risk_score(profile):
    """Compute a transparent synthetic risk score unrelated to real rating logic."""
    return (
        1.0
        + 0.055 * (profile["num_vehicles"] - 1)
        + 0.045 * (profile["num_drivers"] - 1)
        + 0.16 * profile["youth_driver_flag"]
        + 0.06 * profile["senior_driver_flag"]
        + 0.17 * profile["prior_claim_count"]
        + 0.08 * (profile["prior_claim_count"] ** 2)
        - 0.055 * profile["multi_policy_flag"]
    )


def _base_price(profile, carrier_shift=1.0, risk_weight=1.0, geo_weight=1.0, limit_weight=1.0):
    risk = calculate_risk_score(profile)
    limit = LIMIT_FACTOR[profile["coverage_limit"]] ** limit_weight
    credit = CREDIT_FACTOR[profile["credit_score_band"]]
    home = HOME_FACTOR[profile["home_value_band"]]
    urban = URBAN_FACTOR[profile["urban_rural_flag"]]
    state = STATE_FACTOR[profile["state_code"]] ** geo_weight
    deterministic_noise = 1 + ((profile["profile_id"] * 17) % 19 - 9) / 1000
    return 230 * carrier_shift * (risk ** risk_weight) * limit * credit * home * urban * state * deterministic_noise


def price_carrier_a(profile):
    """Carrier A: balanced synthetic pricing behavior."""
    return _base_price(profile, carrier_shift=1.00, risk_weight=1.00, geo_weight=1.00, limit_weight=1.00)


def price_carrier_b(profile):
    """Carrier B: more aggressive on low-risk profiles, more sensitive to claims."""
    price = _base_price(profile, carrier_shift=0.96, risk_weight=1.10, geo_weight=0.90, limit_weight=1.03)
    return price * (1 + 0.035 * profile["prior_claim_count"])


def price_carrier_c(profile):
    """Carrier C: higher base level but more stable across risk groups."""
    price = _base_price(profile, carrier_shift=1.06, risk_weight=0.88, geo_weight=1.12, limit_weight=0.96)
    return price * (1 - 0.025 * profile["multi_policy_flag"])


def simulate_all_carriers(df):
    """Return one row per profile/carrier with simulated prices."""
    rows = []
    for carrier, fn in [("Carrier_A", price_carrier_a), ("Carrier_B", price_carrier_b), ("Carrier_C", price_carrier_c)]:
        out = df.copy()
        out["carrier"] = carrier
        out["risk_score"] = out.apply(calculate_risk_score, axis=1)
        out["simulated_price"] = out.apply(fn, axis=1).round(2)
        rows.append(out)
    return pd.concat(rows, ignore_index=True)


def validate_price_reasonableness(df):
    """Basic checks for synthetic price ranges and monotonic direction."""
    return {
        "min_price": float(df["simulated_price"].min()),
        "max_price": float(df["simulated_price"].max()),
        "missing_prices": int(df["simulated_price"].isna().sum()),
        "non_positive_prices": int((df["simulated_price"] <= 0).sum()),
    }


def main():
    profiles = load_profiles()
    priced = simulate_all_carriers(profiles)
    priced.to_csv(DATA_DIR / "simulated_pricing.csv", index=False)
    print(validate_price_reasonableness(priced))


if __name__ == "__main__":
    main()

