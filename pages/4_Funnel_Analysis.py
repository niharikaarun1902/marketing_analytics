import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import funnel_metrics
from utils.insights import get_biggest_dropoff

setup_page("Funnel Analysis")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)
funnel = funnel_metrics(df)

with content_col:
    st.markdown("### Funnel Analysis")

    st.markdown("#### Marketing Funnel")
    fig = go.Figure(go.Funnel(
        y=[s["stage"] for s in funnel],
        x=[s["value"] for s in funnel],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]),
    ))
    fig.update_layout(funnelmode="stack", margin=dict(t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Stage-to-Stage Progression")
    progression_data = []
    for i in range(len(funnel) - 1):
        current = funnel[i]
        next_stage = funnel[i + 1]
        retained_pct = (next_stage["value"] / current["value"] * 100) if current["value"] else 0
        drop_pct = 100 - retained_pct
        progression_data.append({
            "From": current["stage"],
            "To": next_stage["stage"],
            "Retained": f"{retained_pct:.1f}%",
            "Drop-off": f"{drop_pct:.1f}%",
            "Volume Change": f"{current['value']:,} → {next_stage['value']:,}",
        })

    st.dataframe(pd.DataFrame(progression_data), use_container_width=True, hide_index=True)

    dropoff = get_biggest_dropoff(df)
    st.warning(
        f"**Biggest drop-off:** {dropoff['from_stage']} → {dropoff['to_stage']} "
        f"({dropoff['drop_pct']}% loss, {dropoff['drop_absolute']:,} volume lost). "
        f"This is the primary area to optimize."
    )

    st.markdown("---")
    st.markdown("#### Funnel by Platform")
    platforms = sorted(df["platform"].unique())
    selected = st.selectbox("Select platform", ["All"] + platforms)

    subset = df if selected == "All" else df[df["platform"] == selected]
    sub_funnel = funnel_metrics(subset)
    fig2 = go.Figure(go.Funnel(
        y=[s["stage"] for s in sub_funnel],
        x=[s["value"] for s in sub_funnel],
        textposition="inside",
        textinfo="value+percent initial",
    ))
    fig2.update_layout(title=f"Funnel: {selected}", margin=dict(t=40, b=0))
    st.plotly_chart(fig2, use_container_width=True)
