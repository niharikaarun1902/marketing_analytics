import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import segment_metrics

setup_page("Audience Segments")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)
sm = segment_metrics(df)

with content_col:
    st.markdown("### Audience Segment Deep-Dive")
    st.caption("Which audience segments convert best and deserve more investment.")

    # --- Top metrics ---
    best_reach_row = sm.loc[sm["impressions"].idxmax()]
    best_conv_row = sm.loc[sm["conversion_rate"].idxmax()]
    best_qual_row = sm.loc[sm["qualified_rate"].idxmax()]

    _card = (
        "<div style='background:#F0FFF0; border-left:4px solid #2E8B57; "
        "border-radius:10px; padding:1rem 1.2rem; height:100%;'>"
        "<p style='color:#555; font-size:0.82rem; font-weight:600; "
        "text-transform:uppercase; letter-spacing:0.3px; margin:0 0 0.3rem 0;'>{label}</p>"
        "<p style='color:#2E8B57; font-size:1.3rem; font-weight:800; "
        "margin:0; line-height:1.3;'>{value}</p>"
        "</div>"
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            _card.format(label="Best Reach", value=best_reach_row["audience_segment"]),
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            _card.format(label="Best Conversion Rate", value=best_conv_row["audience_segment"]),
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            _card.format(label="Best Lead Quality", value=best_qual_row["audience_segment"]),
            unsafe_allow_html=True,
        )

    st.markdown("")

    # --- Grouped bar: impressions, clicks, leads by segment ---
    st.markdown("#### Engagement & Leads by Segment")
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Impressions", x=sm["audience_segment"], y=sm["impressions"]))
    fig.add_trace(go.Bar(name="Clicks", x=sm["audience_segment"], y=sm["clicks"]))
    fig.add_trace(go.Bar(name="Leads", x=sm["audience_segment"], y=sm["leads_generated"]))
    fig.update_layout(barmode="group", xaxis_title="", yaxis_title="Count", margin=dict(t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    # --- Conversion rate ranked ---
    left, right = st.columns(2)

    with left:
        st.markdown("#### Conversion Rate by Segment")
        fig_conv = px.bar(
            sm.sort_values("conversion_rate", ascending=True),
            x="conversion_rate", y="audience_segment", orientation="h", text_auto=True,
            labels={"conversion_rate": "Conv. Rate (%)", "audience_segment": ""},
        )
        fig_conv.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig_conv, use_container_width=True)

    with right:
        st.markdown("#### Qualified Lead Rate by Segment")
        fig_qual = px.bar(
            sm.sort_values("qualified_rate", ascending=True),
            x="qualified_rate", y="audience_segment", orientation="h", text_auto=True,
            labels={"qualified_rate": "Qualified Rate (%)", "audience_segment": ""},
        )
        fig_qual.update_layout(showlegend=False, margin=dict(t=10, b=0))
        st.plotly_chart(fig_qual, use_container_width=True)

    # --- Heatmap: segment vs platform ---
    st.markdown("#### Segment vs Platform Performance")
    st.caption("Conversion rate by audience segment and platform. Darker = higher conversion rate.")
    cross = df.groupby(["audience_segment", "platform"]).agg(
        conversions=("conversions", "sum"),
        leads=("leads_generated", "sum"),
    ).reset_index()
    cross["conv_rate"] = cross.apply(
        lambda r: round(r["conversions"] / r["leads"] * 100, 2) if r["leads"] else 0.0, axis=1
    )
    pivot = cross.pivot(index="audience_segment", columns="platform", values="conv_rate").fillna(0)
    fig_heat = px.imshow(
        pivot, text_auto=True,
        labels=dict(x="Platform", y="Segment", color="Conv. Rate (%)"),
        color_continuous_scale="Greens",
        aspect="auto",
    )
    fig_heat.update_layout(margin=dict(t=10, b=0), height=350)
    st.plotly_chart(fig_heat, use_container_width=True)

    # --- Summary table ---
    st.markdown("#### Segment Summary")
    display_cols = [
        "audience_segment", "campaigns", "impressions", "clicks",
        "leads_generated", "qualified_leads", "conversions",
        "ctr", "conversion_rate", "qualified_rate",
    ]
    st.dataframe(
        sm[display_cols].rename(columns={
            "audience_segment": "Segment", "campaigns": "Campaigns",
            "impressions": "Impressions", "clicks": "Clicks",
            "leads_generated": "Leads", "qualified_leads": "Qualified",
            "conversions": "Conversions", "ctr": "CTR (%)",
            "conversion_rate": "Conv. Rate (%)", "qualified_rate": "Qual. Rate (%)",
        }),
        use_container_width=True, hide_index=True,
    )
