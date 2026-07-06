"""Generate sample output assets for the portfolio repository."""

from pathlib import Path

from src.benchmarking import compare_to_reference_carrier, compute_relative_price_position, geographic_price_analysis
from src.generate_synthetic_data import generate_profiles
from src.pricing_engine import simulate_all_carriers
from src.segmentation import bucket_profiles, compute_segment_statistics
from src.sensitivity_analysis import generate_tornado_style_data
from src.visualization import (
    plot_geographic_heatmap,
    plot_price_distribution_by_carrier,
    plot_price_trends_by_coverage,
    plot_segment_comparison,
    plot_sensitivity_tornado,
)


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"


def main():
    DATA_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    profiles = generate_profiles(100_000)
    pricing = simulate_all_carriers(profiles)
    pricing = bucket_profiles(compute_relative_price_position(compare_to_reference_carrier(pricing)))
    pricing_export_cols = [
        "profile_id",
        "region_code",
        "state_code",
        "coverage_limit",
        "num_vehicles",
        "num_drivers",
        "prior_claim_count",
        "youth_driver_flag",
        "multi_policy_flag",
        "home_value_band",
        "credit_score_band",
        "urban_rural_flag",
        "carrier",
        "risk_score",
        "simulated_price",
    ]
    profiles.to_csv(DATA_DIR / "synthetic_profiles.csv", index=False)
    pricing[pricing_export_cols].to_csv(DATA_DIR / "simulated_pricing.csv", index=False)
    geographic_price_analysis(pricing).to_csv(DATA_DIR / "benchmark_summary.csv", index=False)
    geographic_price_analysis(pricing).to_csv(OUTPUT_DIR / "benchmark_summary_table.csv", index=False)
    plot_price_distribution_by_carrier(pricing)
    plot_segment_comparison(pricing)
    plot_geographic_heatmap(pricing)
    plot_sensitivity_tornado(generate_tornado_style_data(pricing))
    plot_price_trends_by_coverage(pricing)
    print("Generated synthetic data and output charts.")


if __name__ == "__main__":
    main()
