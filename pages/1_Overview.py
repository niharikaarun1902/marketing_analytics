import streamlit as st
import plotly.express as px
from utils.filters import apply_sidebar_filters
from utils.metrics import summarize_kpis

st.title("Campaign Overview")

df = apply_sidebar_filters()
kpis = summarize_kpis(df)

# --- KPI row 1 ---
st.subheader("Key Performance Indicators")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Campaigns", kpis["total_campaigns"])
c2.metric("Total Impressions", f"{kpis['total_impressions']:,}")
c3.metric("Total Clicks", f"{kpis['total_clicks']:,}")
c4.metric("CTR", f"{kpis['ctr']}%")

# --- KPI row 2 ---
c5, c6, c7, c8 = st.columns(4)
c5.metric("Total Leads", f"{kpis['total_leads']:,}")
c6.metric("Qualified Leads", f"{kpis['total_qualified_leads']:,}")
c7.metric("Total Conversions", f"{kpis['total_conversions']:,}")
c8.metric("Conversion Rate", f"{kpis['conversion_rate']}%")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Campaigns by Platform")
    platform_counts = df.groupby("platform")["campaign_id"].count().reset_index()
    platform_counts.columns = ["Platform", "Campaigns"]
    fig1 = px.bar(
        platform_counts,
        x="Platform",
        y="Campaigns",
        color="Platform",
        text_auto=True,
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, width="stretch")

with col_right:
    st.subheader("Campaigns by Content Type")
    ct_counts = df.groupby("content_type")["campaign_id"].count().reset_index()
    ct_counts.columns = ["Content Type", "Campaigns"]
    fig2 = px.bar(
        ct_counts,
        x="Content Type",
        y="Campaigns",
        color="Content Type",
        text_auto=True,
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, width="stretch")
