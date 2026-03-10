import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import platform_metrics

setup_page("Channel Performance")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)
pm = platform_metrics(df)

with content_col:
    st.markdown("### Channel Performance")

    st.markdown("#### Engagement & Leads by Platform")
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Impressions", x=pm["platform"], y=pm["impressions"]))
    fig.add_trace(go.Bar(name="Clicks", x=pm["platform"], y=pm["clicks"]))
    fig.add_trace(go.Bar(name="Leads", x=pm["platform"], y=pm["leads_generated"]))
    fig.update_layout(barmode="group", xaxis_title="", yaxis_title="Count",
                      margin=dict(t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### CTR by Platform")
        fig_ctr = px.bar(
            pm.sort_values("ctr", ascending=True),
            x="ctr", y="platform", orientation="h", text_auto=True,
            labels={"ctr": "CTR (%)", "platform": ""},
        )
        fig_ctr.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig_ctr, use_container_width=True)

    with col2:
        st.markdown("#### Conversion Rate by Platform")
        fig_conv = px.bar(
            pm.sort_values("conversion_rate", ascending=True),
            x="conversion_rate", y="platform", orientation="h", text_auto=True,
            labels={"conversion_rate": "Conv. Rate (%)", "platform": ""},
        )
        fig_conv.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig_conv, use_container_width=True)

    st.markdown("#### Platform Summary")
    display_cols = [
        "platform", "campaigns", "impressions", "clicks", "leads_generated",
        "qualified_leads", "conversions", "ctr", "conversion_rate", "lead_rate",
    ]
    st.dataframe(
        pm[display_cols].rename(columns={
            "platform": "Platform", "campaigns": "Campaigns",
            "impressions": "Impressions", "clicks": "Clicks",
            "leads_generated": "Leads", "qualified_leads": "Qualified Leads",
            "conversions": "Conversions", "ctr": "CTR (%)",
            "conversion_rate": "Conv. Rate (%)", "lead_rate": "Lead Rate (%)",
        }),
        use_container_width=True, hide_index=True,
    )
