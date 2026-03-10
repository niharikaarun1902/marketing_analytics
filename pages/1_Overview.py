import streamlit as st
import plotly.express as px
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import summarize_kpis

setup_page("Overview")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)
kpis = summarize_kpis(df)

with content_col:
    st.markdown("### Campaign Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Campaigns", kpis["total_campaigns"])
    c2.metric("Total Impressions", f"{kpis['total_impressions']:,}")
    c3.metric("Total Clicks", f"{kpis['total_clicks']:,}")
    c4.metric("CTR", f"{kpis['ctr']}%")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Total Leads", f"{kpis['total_leads']:,}")
    c6.metric("Qualified Leads", f"{kpis['total_qualified_leads']:,}")
    c7.metric("Total Conversions", f"{kpis['total_conversions']:,}")
    c8.metric("Conversion Rate", f"{kpis['conversion_rate']}%")

    st.markdown("")

    col_left, col_mid, col_right = st.columns(3)

    with col_left:
        st.markdown("#### Campaigns by Platform")
        platform_counts = df.groupby("platform")["campaign_id"].count().reset_index()
        platform_counts.columns = ["Platform", "Campaigns"]
        fig1 = px.bar(
            platform_counts, x="Platform", y="Campaigns",
            color="Platform", text_auto=True,
        )
        fig1.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with col_mid:
        st.markdown("#### Campaigns by Content Type")
        ct_counts = df.groupby("content_type")["campaign_id"].count().reset_index()
        ct_counts.columns = ["Content Type", "Campaigns"]
        fig2 = px.bar(
            ct_counts, x="Content Type", y="Campaigns",
            color="Content Type", text_auto=True,
        )
        fig2.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        st.markdown("#### Campaigns by Audience Segment")
        seg_counts = df.groupby("audience_segment")["campaign_id"].count().reset_index()
        seg_counts.columns = ["Audience Segment", "Campaigns"]
        fig3 = px.bar(
            seg_counts, x="Audience Segment", y="Campaigns",
            color="Audience Segment", text_auto=True,
        )
        fig3.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)
