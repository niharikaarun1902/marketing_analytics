import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import content_type_metrics

setup_page("Content Analysis")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)
ct = content_type_metrics(df)

with content_col:
    st.markdown("### Content Analysis")

    st.markdown("#### Engagement Metrics by Content Type")
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Impressions", x=ct["content_type"], y=ct["impressions"]))
    fig.add_trace(go.Bar(name="Clicks", x=ct["content_type"], y=ct["clicks"]))
    fig.add_trace(go.Bar(name="Likes", x=ct["content_type"], y=ct["likes"]))
    fig.update_layout(barmode="group", xaxis_title="", yaxis_title="Count",
                      margin=dict(t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Leads & Conversions by Content Type")
    col1, col2 = st.columns(2)

    with col1:
        fig_leads = px.bar(
            ct.sort_values("leads_generated", ascending=True),
            x="leads_generated", y="content_type", orientation="h", text_auto=True,
            labels={"leads_generated": "Leads Generated", "content_type": ""},
        )
        fig_leads.update_layout(showlegend=False, title="Leads Generated",
                                margin=dict(t=30, b=0))
        st.plotly_chart(fig_leads, use_container_width=True)

    with col2:
        fig_conv = px.bar(
            ct.sort_values("conversions", ascending=True),
            x="conversions", y="content_type", orientation="h", text_auto=True,
            labels={"conversions": "Conversions", "content_type": ""},
        )
        fig_conv.update_layout(showlegend=False, title="Conversions",
                               margin=dict(t=30, b=0))
        st.plotly_chart(fig_conv, use_container_width=True)

    st.markdown("#### Content Type Performance Ranking")
    ranking = ct[["content_type", "campaigns", "ctr", "conversion_rate", "lead_rate"]].sort_values(
        "conversion_rate", ascending=False
    )
    st.dataframe(
        ranking.rename(columns={
            "content_type": "Content Type", "campaigns": "Campaigns",
            "ctr": "CTR (%)", "conversion_rate": "Conv. Rate (%)",
            "lead_rate": "Lead Rate (%)",
        }),
        use_container_width=True, hide_index=True,
    )

    best = ct.loc[ct["conversion_rate"].idxmax()]
    st.success(
        f"**Top-performing content type:** {best['content_type']} "
        f"with a {best['conversion_rate']}% conversion rate "
        f"across {int(best['campaigns'])} campaigns."
    )
