# Competitive Personal Umbrella Pricing and Market Benchmarking Simulator

## Overview

This repository is a fully synthetic portfolio project that simulates personal umbrella insurance pricing across multiple fictional carriers. It creates synthetic customer profiles, applies transparent fictional pricing behavior, benchmarks relative carrier positioning, and visualizes segment, geographic, and sensitivity patterns in a Streamlit dashboard.

## Business Problem

Pricing and product teams often need to understand how competitive position changes across customer segments, coverage limits, and geographies. This project recreates that analytical workflow with synthetic data only: no real carrier rates, no proprietary pricing rules, and no confidential business logic.

## Why This Project Matters

The project demonstrates how an analyst can turn a complex pricing comparison problem into a reproducible decision-support tool. It shows the mechanics of scenario generation, modular scoring, benchmarking, segment diagnostics, and executive-ready insight generation.

## Synthetic Data Design

The generator creates at least 100,000 fictional profiles with generic attributes such as region, synthetic state, coverage limit, number of vehicles, number of drivers, household size, prior claims, multi-policy indicator, home value band, credit score band, and urban/rural flag. The data includes realistic correlations, but every value is fabricated.

The repository includes a smaller committed sample so the GitHub project stays lightweight. Running the generation scripts locally recreates the full 100,000-profile synthetic dataset.

## Methodology

1. Generate synthetic personal umbrella profiles.
2. Calculate a transparent synthetic risk score.
3. Simulate prices for three fictional carriers.
4. Benchmark each carrier against the market average and a reference carrier.
5. Analyze price differences by segment, geography, coverage limit, and driver sensitivity.
6. Package the workflow as a Streamlit dashboard.

## Repository Structure

```text
umbrella-pricing-simulator/
├── README.md
├── requirements.txt
├── app.py
├── data/
├── notebooks/
├── outputs/
└── src/
```

## Dashboard Features

- KPI summary for average price, reference gap, and segment mix
- Carrier price distribution comparison
- Low / medium / high risk segment analysis
- Synthetic state-level geographic heatmap
- Coverage-limit sensitivity curves
- Tornado-style pricing driver analysis
- Automated benchmark insights
- Filtered data explorer and CSV download

## How to Run

```bash
pip install -r requirements.txt
python src/generate_synthetic_data.py
python src/pricing_engine.py
python scripts_generate_outputs.py
streamlit run app.py
```

## Example Insights

- Which fictional carrier has the lowest average simulated premium
- Which risk segment has the largest price separation across carriers
- Which synthetic state has the widest competitive spread
- Which pricing driver creates the largest simulated price movement
- Whether a carrier is aggressive in one segment but conservative in another

## Skills Demonstrated

- Synthetic data generation
- Insurance pricing analytics
- Multi-carrier benchmarking
- Segment-level diagnostics
- Geographic price variation analysis
- Sensitivity analysis
- Modular scoring engine design
- Streamlit dashboard development
- Product analytics storytelling

## Confidentiality Note

This project is built entirely with synthetic data and fictional pricing behavior. It does not contain proprietary employer data, real carrier logic, pricing formulas, rating tables, underwriting rules, regulatory filings, business rules, screenshots, URLs, customer information, or confidential information.

## Future Enhancements

- Add scenario upload support for user-defined synthetic profiles
- Add confidence intervals around benchmark gaps
- Add automated reconciliation checks across profile and pricing outputs
- Add a richer executive summary export
- Add more flexible sensitivity testing controls in the dashboard
