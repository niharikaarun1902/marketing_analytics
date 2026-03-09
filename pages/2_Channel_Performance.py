import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import apply_sidebar_filters
from utils.metrics import platform_metrics

st.title("Channel Performance")

df = apply_sidebar_filters()
pm = platform_metrics(df)

# --- Grouped bar: impressions, clicks, leads ---
st.subheader("Engagement & Leads by Platform")

fig = go.Figure()
fig.add_trace(go.Bar(name="Impressions", x=pm["platform"], y=pm["impressions"]))
fig.add_trace(go.Bar(name="Clicks", x=pm["platform"], y=pm["clicks"]))
fig.add_trace(go.Bar(name="Leads", x=pm["platform"], y=pm["leads_generated"]))
fig.update_layout(barmode="group", xaxis_title="Platform", yaxis_title="Count")
st.plotly_chart(fig, width="stretch")

# --- Rate charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("CTR by Platform")
    fig_ctr = px.bar(
        pm.sort_values("ctr", ascending=True),
        x="ctr",
        y="platform",
        orientation="h",
        text_auto=True,
        labels={"ctr": "CTR (%)", "platform": ""},
    )
    fig_ctr.update_layout(showlegend=False)
    st.plotly_chart(fig_ctr, width="stretch")

with col2:
    st.subheader("Conversion Rate by Platform")
    fig_conv = px.bar(
        pm.sort_values("conversion_rate", ascending=True),
        x="conversion_rate",
        y="platform",
        orientation="h",
        text_auto=True,
        labels={"conversion_rate": "Conversion Rate (%)", "platform": ""},
    )
    fig_conv.update_layout(showlegend=False)
    st.plotly_chart(fig_conv, width="stretch")

# --- Summary table ---
st.subheader("Platform Summary")
display_cols = [
    "platform", "campaigns", "impressions", "clicks", "leads_generated",
    "qualified_leads", "conversions", "ctr", "conversion_rate", "lead_rate",
]
st.dataframe(
    pm[display_cols].rename(columns={
        "platform": "Platform",
        "campaigns": "Campaigns",
        "impressions": "Impressions",
        "clicks": "Clicks",
        "leads_generated": "Leads",
        "qualified_leads": "Qualified Leads",
        "conversions": "Conversions",
        "ctr": "CTR (%)",
        "conversion_rate": "Conv. Rate (%)",
        "lead_rate": "Lead Rate (%)",
    }),
    width="stretch",
    hide_index=True,
)
