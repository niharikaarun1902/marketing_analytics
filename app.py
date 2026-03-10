import math
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.layout import setup_page
from utils.data_loader import load_merged_data
from utils.metrics import summarize_kpis, platform_metrics, funnel_metrics, segment_metrics

setup_page()

df = load_merged_data()
kpis = summarize_kpis(df)

# --- KPI row ---
st.markdown("#### Key Metrics")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Campaigns", kpis["total_campaigns"])
c2.metric("Impressions", f"{kpis['total_impressions']:,}")
c3.metric("Clicks", f"{kpis['total_clicks']:,}")
c4.metric("CTR", f"{kpis['ctr']}%")
c5.metric("Conversions", f"{kpis['total_conversions']:,}")
c6.metric("Conv. Rate", f"{kpis['conversion_rate']}%")

st.markdown("")

# --- Row 2: Charts ---
left, right = st.columns(2, gap="large")

with left:
    st.markdown("#### Impressions by Platform")
    pm = platform_metrics(df)
    fig1 = px.bar(
        pm.sort_values("impressions", ascending=True),
        x="impressions",
        y="platform",
        orientation="h",
        text_auto=True,
        color="platform",
    )
    fig1.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="",
        height=280,
    )
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.markdown("#### Marketing Funnel")
    funnel = funnel_metrics(df)
    fig2 = go.Figure(go.Funnel(
        y=[s["stage"] for s in funnel],
        x=[s["value"] for s in funnel],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]),
    ))
    fig2.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Row 3: More detail ---
left2, mid2, right2 = st.columns(3, gap="large")

with left2:
    st.markdown("#### Campaigns by Content Type")
    ct_counts = df.groupby("content_type")["campaign_id"].count().reset_index()
    ct_counts.columns = ["Content Type", "Campaigns"]
    if ct_counts["Campaigns"].sum() > 0:
        ct_sorted = ct_counts.sort_values("Campaigns", ascending=False)
        labels = ct_sorted["Content Type"].tolist()
        values = ct_sorted["Campaigns"].tolist()
        fig3 = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.45,
            sort=False,
            textinfo="label",
            textposition="outside",
            textfont=dict(size=11),
            outsidetextfont=dict(size=11),
            marker=dict(colors=px.colors.qualitative.Set2),
        ))
        total = sum(values)
        cumsum = 0
        r = 0.35
        for val in values:
            center_angle = (cumsum + val / 2) / total * 360
            cumsum += val
            rad = math.radians(center_angle)
            x = 0.5 + r * math.sin(rad)
            y = 0.5 + r * math.cos(rad)
            fig3.add_annotation(
                x=x, y=y, text=str(int(val)), showarrow=False,
                xref="paper", yref="paper",
                font=dict(size=12, color="white"),
            )
        fig3.update_layout(
            margin=dict(l=60, r=60, t=40, b=100),
            height=380,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.15,
                xanchor="center",
                x=0.5,
                font=dict(size=11),
            ),
            showlegend=True,
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No campaign data to display.")

with mid2:
    st.markdown("#### Leads by Platform")
    fig4 = px.bar(
        pm.sort_values("leads_generated", ascending=False),
        x="platform",
        y="leads_generated",
        text_auto=True,
        color="platform",
    )
    fig4.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="",
        height=280,
    )
    st.plotly_chart(fig4, use_container_width=True)

with right2:
    st.markdown("#### Conversion Rate by Platform")
    fig5 = px.bar(
        pm.sort_values("conversion_rate", ascending=False),
        x="platform",
        y="conversion_rate",
        text_auto=True,
        color="platform",
    )
    fig5.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="%",
        height=280,
    )
    st.plotly_chart(fig5, use_container_width=True)

# --- Row 4: Audience segment ---
st.markdown("")
left4, right4 = st.columns(2, gap="large")

with left4:
    st.markdown("#### Campaigns by Audience Segment")
    seg_counts = df.groupby("audience_segment")["campaign_id"].count().reset_index()
    seg_counts.columns = ["Audience Segment", "Campaigns"]
    fig6 = px.bar(
        seg_counts.sort_values("Campaigns", ascending=False),
        x="Audience Segment",
        y="Campaigns",
        text_auto=True,
        color="Audience Segment",
    )
    fig6.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="",
        height=280,
    )
    st.plotly_chart(fig6, use_container_width=True)

with right4:
    st.markdown("#### Leads by Audience Segment")
    sm = segment_metrics(df)
    fig7 = px.bar(
        sm.sort_values("leads_generated", ascending=False),
        x="audience_segment",
        y="leads_generated",
        text_auto=True,
        color="audience_segment",
    )
    fig7.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="",
        height=280,
    )
    st.plotly_chart(fig7, use_container_width=True)

# --- Bottom quick-access ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.85rem;'>"
    "Use the navigation bar above to explore detailed analytics for each section."
    "</p>",
    unsafe_allow_html=True,
)
