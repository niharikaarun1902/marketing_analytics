import streamlit as st
from utils.filters import apply_sidebar_filters
from utils.insights import get_best_platform, get_best_content_type, get_biggest_dropoff
from utils.claude_layer import (
    classify_campaign_theme,
    classify_campaign_intent,
    classify_funnel_stage,
    summarize_platform_performance,
    summarize_content_performance,
    identify_funnel_issue,
    generate_founder_recommendations,
)

st.title("Claude-Style Intelligence Layer")
st.markdown(
    "This page generates rule-based, plain-English insights from the campaign data — "
    "modeled after what a Claude-powered analytics assistant would produce."
)

df = apply_sidebar_filters()

# --- Campaign classification ---
st.subheader("Campaign Classification")
classified = df.copy()
classified["Theme"] = classified.apply(classify_campaign_theme, axis=1)
classified["Intent"] = classified.apply(classify_campaign_intent, axis=1)
classified["Funnel Stage"] = classified.apply(classify_funnel_stage, axis=1)

display_cols = [
    "campaign_id", "campaign_name", "platform", "content_type",
    "Theme", "Intent", "Funnel Stage",
]
st.dataframe(
    classified[display_cols].rename(columns={
        "campaign_id": "ID",
        "campaign_name": "Campaign",
        "platform": "Platform",
        "content_type": "Content Type",
    }),
    width="stretch",
    hide_index=True,
)

st.markdown("---")

# --- Platform summary ---
st.subheader("Platform Performance Summary")
st.markdown(summarize_platform_performance(df))

st.markdown("---")

# --- Content summary ---
st.subheader("Content Performance Summary")
st.markdown(summarize_content_performance(df))

st.markdown("---")

# --- Funnel diagnosis ---
st.subheader("Funnel Diagnosis")
st.markdown(identify_funnel_issue(df))

st.markdown("---")

# --- Executive recommendations ---
st.subheader("Executive Recommendations")
st.markdown(generate_founder_recommendations(df))

# --- Structured summary block ---
st.markdown("---")
st.subheader("Executive Summary Report")

st.markdown("### Overview")
total_campaigns = len(df)
total_conversions = int(df["conversions"].sum())
total_impressions = int(df["impressions"].sum())
overall_rate = (total_conversions / total_impressions * 100) if total_impressions else 0
st.markdown(
    f"Across **{total_campaigns} published campaigns**, the marketing program generated "
    f"**{total_impressions:,} impressions** and **{total_conversions} conversions** "
    f"for an overall funnel efficiency of **{overall_rate:.2f}%**. "
    f"Performance varies significantly across platforms and content types, "
    f"creating clear opportunities for optimization."
)

col1, col2 = st.columns(2)
with col1:
    st.markdown("### What is Working")
    bp = get_best_platform(df)
    bc = get_best_content_type(df)
    st.markdown(f"- **{bp['best_reach']}** leads in reach and visibility")
    st.markdown(f"- **{bp['best_conversion_rate']}** delivers the strongest conversion efficiency")
    st.markdown(f"- **{bc['best_leads']}** content generates the most leads")
    st.markdown(f"- **{bc['best_conversion_rate']}** content has the highest conversion rate")

with col2:
    st.markdown("### What Needs Attention")
    dropoff = get_biggest_dropoff(df)
    st.markdown(
        f"- Largest funnel drop-off: **{dropoff['from_stage']} → {dropoff['to_stage']}** "
        f"({dropoff['drop_pct']}%)"
    )
    st.markdown(f"- Overall funnel efficiency is only **{overall_rate:.2f}%**")
    st.markdown("- High-reach channels are not always the highest converters")
    st.markdown("- Some content types drive awareness but underperform on lead quality")
