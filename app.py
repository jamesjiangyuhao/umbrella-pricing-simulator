"""Streamlit dashboard for the synthetic umbrella pricing simulator."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.benchmarking import compare_to_reference_carrier, compute_relative_price_position, geographic_price_analysis
from src.generate_synthetic_data import generate_profiles
from src.pricing_engine import simulate_all_carriers
from src.reporting import format_insights
from src.segmentation import bucket_profiles, compute_segment_statistics
from src.sensitivity_analysis import generate_tornado_style_data


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


@st.cache_data
def load_data():
    DATA_DIR.mkdir(exist_ok=True)
    profile_path = DATA_DIR / "synthetic_profiles.csv"
    pricing_path = DATA_DIR / "simulated_pricing.csv"
    if not profile_path.exists():
        generate_profiles().to_csv(profile_path, index=False)
    if not pricing_path.exists():
        simulate_all_carriers(pd.read_csv(profile_path)).to_csv(pricing_path, index=False)
    df = pd.read_csv(pricing_path)
    df = bucket_profiles(compute_relative_price_position(compare_to_reference_carrier(df)))
    return df


st.set_page_config(page_title="Competitive Personal Umbrella Pricing Simulator", layout="wide")
st.title("Competitive Personal Umbrella Pricing Simulator")
st.caption("Synthetic portfolio project for multi-carrier pricing simulation, competitive benchmarking, and segment-level decision support.")

df = load_data()
with st.sidebar:
    carriers = st.multiselect("Carrier", sorted(df["carrier"].unique()), default=sorted(df["carrier"].unique()))
    states = st.multiselect("State", sorted(df["state_code"].unique()), default=sorted(df["state_code"].unique()))
    limits = st.multiselect("Coverage limit", ["1M", "2M", "5M"], default=["1M", "2M", "5M"])
    segments = st.multiselect("Risk segment", ["Low Risk", "Medium Risk", "High Risk"], default=["Low Risk", "Medium Risk", "High Risk"])

view = df[df["carrier"].isin(carriers) & df["state_code"].isin(states) & df["coverage_limit"].isin(limits) & df["risk_segment"].astype(str).isin(segments)]

st.header("Overview")
st.write("This dashboard uses fully synthetic profiles and fictional carrier behavior to study relative price position across coverage limits, geographies, and risk segments.")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Profiles", f"{view['profile_id'].nunique():,}")
k2.metric("Average Price", f"${view['simulated_price'].mean():,.0f}")
k3.metric("Lowest Avg Carrier", view.groupby("carrier")["simulated_price"].mean().idxmin())
k4.metric("Avg Gap vs Reference", f"{view['pct_gap_vs_reference'].mean() * 100:,.1f}%")

st.header("Carrier Comparison")
st.plotly_chart(px.box(view, x="carrier", y="simulated_price", color="carrier", points=False), use_container_width=True)

st.header("Segment Analysis")
seg = view.groupby(["risk_segment", "carrier"], observed=True, as_index=False).agg(avg_price=("simulated_price", "mean"), profiles=("profile_id", "nunique"))
st.plotly_chart(px.bar(seg, x="risk_segment", y="avg_price", color="carrier", barmode="group", hover_data=["profiles"]), use_container_width=True)

st.header("Geographic Analysis")
geo = geographic_price_analysis(view)
st.plotly_chart(px.density_heatmap(geo, x="carrier", y="state_code", z="avg_price", histfunc="avg", color_continuous_scale="YlGnBu"), use_container_width=True)

st.header("Coverage Sensitivity")
coverage = view.groupby(["coverage_limit", "carrier"], as_index=False).agg(avg_price=("simulated_price", "mean"))
st.plotly_chart(px.line(coverage, x="coverage_limit", y="avg_price", color="carrier", markers=True), use_container_width=True)

st.header("Sensitivity Analysis")
tornado = generate_tornado_style_data(view)
top_driver = tornado.groupby("driver", as_index=False)["price_spread"].mean().sort_values("price_spread", ascending=False)
st.plotly_chart(px.bar(top_driver, x="price_spread", y="driver", orientation="h"), use_container_width=True)

st.header("Benchmark Insights")
for insight in format_insights(view):
    st.write(f"- {insight}")

st.header("Data Explorer")
st.dataframe(view.head(1000), use_container_width=True)
st.download_button("Download filtered pricing data", view.to_csv(index=False), "filtered_simulated_pricing.csv", "text/csv")

