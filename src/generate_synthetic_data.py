"""Generate synthetic umbrella insurance profiles for portfolio analysis."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def generate_profiles(n_profiles=100_000, random_state=42):
    """Create a deterministic synthetic profile table."""
    rng = np.random.default_rng(random_state)
    state_codes = [f"S{i:02d}" for i in range(1, 13)]
    region_map = {
        "S01": "Region 1", "S02": "Region 1", "S03": "Region 2", "S04": "Region 2",
        "S05": "Region 3", "S06": "Region 3", "S07": "Region 4", "S08": "Region 4",
        "S09": "Region 5", "S10": "Region 5", "S11": "Region 5", "S12": "Region 2",
    }
    state = rng.choice(state_codes, size=n_profiles, p=[0.06, 0.07, 0.08, 0.09, 0.1, 0.1, 0.08, 0.08, 0.09, 0.09, 0.08, 0.08])
    region = np.array([region_map[s] for s in state])
    coverage_limit = rng.choice(["1M", "2M", "5M"], size=n_profiles, p=[0.58, 0.3, 0.12])
    urban = rng.choice(["Urban", "Suburban", "Rural"], size=n_profiles, p=[0.38, 0.42, 0.2])
    credit = rng.choice(["Low", "Medium", "High"], size=n_profiles, p=[0.18, 0.47, 0.35])
    home_value = rng.choice(["Entry", "Standard", "Premium", "High Net Worth"], size=n_profiles, p=[0.23, 0.43, 0.25, 0.09])

    base_household = rng.poisson(1.8, size=n_profiles) + 1
    household_size = np.clip(base_household + (home_value == "High Net Worth").astype(int), 1, 7)
    num_drivers = np.clip(household_size - rng.binomial(1, 0.25, size=n_profiles), 1, 6)
    num_vehicles = np.clip(num_drivers + rng.binomial(2, 0.42, size=n_profiles) + (home_value == "High Net Worth").astype(int), 1, 8)
    youth_driver_flag = rng.binomial(1, np.clip(0.06 + 0.035 * (household_size - 2), 0.03, 0.22))
    senior_driver_flag = rng.binomial(1, np.where(household_size <= 2, 0.16, 0.08))
    prior_claim_count = rng.poisson(0.18 + 0.08 * youth_driver_flag + 0.05 * (num_vehicles > 3), size=n_profiles)
    prior_claim_count = np.clip(prior_claim_count, 0, 4)
    multi_policy_flag = rng.binomial(1, np.where(home_value == "High Net Worth", 0.72, 0.54))

    df = pd.DataFrame({
        "profile_id": np.arange(1, n_profiles + 1),
        "region_code": region,
        "state_code": state,
        "coverage_limit": coverage_limit,
        "num_vehicles": num_vehicles,
        "num_drivers": num_drivers,
        "household_size": household_size,
        "youth_driver_flag": youth_driver_flag,
        "senior_driver_flag": senior_driver_flag,
        "prior_claim_count": prior_claim_count,
        "multi_policy_flag": multi_policy_flag,
        "home_value_band": home_value,
        "credit_score_band": credit,
        "urban_rural_flag": urban,
    })
    return df


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    profiles = generate_profiles()
    profiles.to_csv(DATA_DIR / "synthetic_profiles.csv", index=False)
    print(f"Wrote {len(profiles):,} profiles to {DATA_DIR / 'synthetic_profiles.csv'}")


if __name__ == "__main__":
    main()

