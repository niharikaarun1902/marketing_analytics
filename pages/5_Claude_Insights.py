import math
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.layout import setup_page
from utils.filters import apply_filters
from utils.metrics import platform_metrics, content_type_metrics, segment_metrics, funnel_metrics
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

setup_page("Claude Insights")

content_col, filter_col = st.columns([3, 1], gap="large")

df = apply_filters(filter_col)

with content_col:
    st.markdown("### Claude-Style Intelligence Layer")

    tab_visual, tab_report = st.tabs(["Interactive Dashboard", "Detailed Report"])

    # ================================================================
    # TAB 1 — Interactive visual dashboard
    # ================================================================
    with tab_visual:
        # --- Top-line executive summary metrics ---
        total_campaigns = len(df)
        total_impressions = int(df["impressions"].sum())
        total_conversions = int(df["conversions"].sum())
        overall_rate = (total_conversions / total_impressions * 100) if total_impressions else 0

        bp = get_best_platform(df)
        bc = get_best_content_type(df)
        dropoff = get_biggest_dropoff(df)

        m1, m2, m3 = st.columns(3)
        m1.metric("Best Reach Platform", bp["best_reach"])
        m2.metric("Best Conversion Platform", bp["best_conversion_rate"])
        m3.metric("Funnel Efficiency", f"{overall_rate:.2f}%")

        m4, m5, m6 = st.columns(3)
        m4.metric("Biggest Drop-off Stage", dropoff["from_stage"])
        m5.metric("Drop-off Volume Lost", f"{dropoff['drop_absolute']:,}")
        m6.metric("Drop-off Percentage", f"{dropoff['drop_pct']}%")

        st.markdown("")

        # --- Platform comparison: reach vs conversion ---
        pm = platform_metrics(df)
        ct = content_type_metrics(df)

        left, right = st.columns(2)

        with left:
            st.markdown("#### Platform: Reach vs Conversion")
            fig_plat = go.Figure()
            fig_plat.add_trace(go.Bar(
                name="Impressions",
                x=pm["platform"], y=pm["impressions"],
                text=pm["impressions"].apply(lambda v: f"{v:,}"),
                textposition="outside", yaxis="y",
            ))
            fig_plat.add_trace(go.Bar(
                name="Conv. Rate (%)",
                x=pm["platform"], y=pm["conversion_rate"],
                text=pm["conversion_rate"].apply(lambda v: f"{v}%"),
                textposition="outside", yaxis="y2",
            ))
            fig_plat.update_layout(
                barmode="group", height=380,
                margin=dict(t=10, b=0),
                yaxis=dict(title="Impressions", showgrid=False),
                yaxis2=dict(title="Conv. Rate (%)", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", y=-0.15, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_plat, use_container_width=True)

        with right:
            st.markdown("#### Content: Reach vs Conversion")
            fig_cont = go.Figure()
            fig_cont.add_trace(go.Bar(
                name="Impressions",
                x=ct["content_type"], y=ct["impressions"],
                text=ct["impressions"].apply(lambda v: f"{v:,}"),
                textposition="outside", yaxis="y",
            ))
            fig_cont.add_trace(go.Bar(
                name="Conv. Rate (%)",
                x=ct["content_type"], y=ct["conversion_rate"],
                text=ct["conversion_rate"].apply(lambda v: f"{v}%"),
                textposition="outside", yaxis="y2",
            ))
            fig_cont.update_layout(
                barmode="group", height=380,
                margin=dict(t=10, b=0),
                yaxis=dict(title="Impressions", showgrid=False),
                yaxis2=dict(title="Conv. Rate (%)", overlaying="y", side="right", showgrid=False),
                legend=dict(orientation="h", y=-0.15, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_cont, use_container_width=True)

        st.markdown("#### Audience: Reach vs Conversion")
        sm = segment_metrics(df)
        fig_aud = go.Figure()
        fig_aud.add_trace(go.Bar(
            name="Impressions",
            x=sm["audience_segment"], y=sm["impressions"],
            text=sm["impressions"].apply(lambda v: f"{v:,}"),
            textposition="outside", yaxis="y",
        ))
        fig_aud.add_trace(go.Bar(
            name="Conv. Rate (%)",
            x=sm["audience_segment"], y=sm["conversion_rate"],
            text=sm["conversion_rate"].apply(lambda v: f"{v}%"),
            textposition="outside", yaxis="y2",
        ))
        fig_aud.update_layout(
            barmode="group", height=380,
            margin=dict(t=10, b=0),
            yaxis=dict(title="Impressions", showgrid=False),
            yaxis2=dict(title="Conv. Rate (%)", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", y=-0.15, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_aud, use_container_width=True)

        # --- Campaign classification breakdown ---
        st.markdown("#### Campaign Classification")
        classified = df.copy()
        classified["Theme"] = classified.apply(classify_campaign_theme, axis=1)
        classified["Intent"] = classified.apply(classify_campaign_intent, axis=1)
        classified["Funnel Stage"] = classified.apply(classify_funnel_stage, axis=1)

        cls1, cls2, cls3 = st.columns(3)
        def _add_pie_numbers(fig, values, r=0.32):
            total = sum(values)
            if total == 0:
                return
            cumsum = 0
            for val in values:
                center_angle = (cumsum + val / 2) / total * 360
                cumsum += val
                rad = math.radians(center_angle)
                x = 0.5 + r * math.sin(rad)
                y = 0.5 + r * math.cos(rad)
                fig.add_annotation(
                    x=x, y=y, text=str(int(val)), showarrow=False,
                    xref="paper", yref="paper",
                    font=dict(size=10, color="white"),
                )

        with cls1:
            theme_counts = classified["Theme"].value_counts().reset_index()
            theme_counts.columns = ["Theme", "Count"]
            theme_sorted = theme_counts.sort_values("Count", ascending=False)
            fig_theme = go.Figure(go.Pie(
                labels=theme_sorted["Theme"].tolist(),
                values=theme_sorted["Count"].tolist(),
                hole=0.4,
                sort=False,
                textinfo="label",
                textposition="outside",
                textfont=dict(size=10),
                marker=dict(colors=px.colors.qualitative.Set2),
            ))
            _add_pie_numbers(fig_theme, theme_sorted["Count"].tolist())
            fig_theme.update_layout(
                title="By Theme", height=300,
                margin=dict(t=40, b=80, l=50, r=50),
                legend=dict(orientation="h", y=-0.2, xanchor="center", x=0.5, font=dict(size=10)),
            )
            st.plotly_chart(fig_theme, use_container_width=True)

        with cls2:
            intent_counts = classified["Intent"].value_counts().reset_index()
            intent_counts.columns = ["Intent", "Count"]
            intent_sorted = intent_counts.sort_values("Count", ascending=False)
            fig_intent = go.Figure(go.Pie(
                labels=intent_sorted["Intent"].tolist(),
                values=intent_sorted["Count"].tolist(),
                hole=0.4,
                sort=False,
                textinfo="label",
                textposition="outside",
                textfont=dict(size=10),
                marker=dict(colors=px.colors.qualitative.Set2),
            ))
            _add_pie_numbers(fig_intent, intent_sorted["Count"].tolist())
            fig_intent.update_layout(
                title="By Intent", height=300,
                margin=dict(t=40, b=80, l=50, r=50),
                legend=dict(orientation="h", y=-0.2, xanchor="center", x=0.5, font=dict(size=10)),
            )
            st.plotly_chart(fig_intent, use_container_width=True)

        with cls3:
            stage_counts = classified["Funnel Stage"].value_counts().reset_index()
            stage_counts.columns = ["Funnel Stage", "Count"]
            stage_sorted = stage_counts.sort_values("Count", ascending=False)
            fig_stage = go.Figure(go.Pie(
                labels=stage_sorted["Funnel Stage"].tolist(),
                values=stage_sorted["Count"].tolist(),
                hole=0.4,
                sort=False,
                textinfo="label",
                textposition="outside",
                textfont=dict(size=10),
                marker=dict(colors=px.colors.qualitative.Set2),
            ))
            _add_pie_numbers(fig_stage, stage_sorted["Count"].tolist())
            fig_stage.update_layout(
                title="By Funnel Stage", height=300,
                margin=dict(t=40, b=80, l=50, r=50),
                legend=dict(orientation="h", y=-0.2, xanchor="center", x=0.5, font=dict(size=10)),
            )
            st.plotly_chart(fig_stage, use_container_width=True)

        # --- What's working / what needs attention ---
        st.markdown("---")
        w1, w2 = st.columns(2)
        with w1:
            st.success(
                f"**What's Working**\n\n"
                f"- **{bp['best_reach']}** leads in reach and visibility\n"
                f"- **{bp['best_conversion_rate']}** delivers the strongest conversion efficiency\n"
                f"- **{bc['best_leads']}** content generates the most leads\n"
                f"- **{bc['best_conversion_rate']}** content has the highest conversion rate"
            )
        with w2:
            st.warning(
                f"**What Needs Attention**\n\n"
                f"- Largest funnel drop-off: **{dropoff['from_stage']} → {dropoff['to_stage']}** "
                f"({dropoff['drop_pct']}%)\n"
                f"- Overall funnel efficiency is only **{overall_rate:.2f}%**\n"
                f"- High-reach channels are not always the highest converters\n"
                f"- Some content types drive awareness but underperform on lead quality"
            )

        # --- Recommendations as individual callouts ---
        st.markdown("---")
        st.markdown("#### Key Recommendations")
        rec_cols = st.columns(3)
        recs = [
            f"Double down on **{bp['best_conversion_rate']}** for conversion campaigns — highest ROI per lead.",
            f"Use **{bp['best_reach']}** as the primary awareness channel — consistently highest reach.",
            f"Scale **{bc['best_conversion_rate']}** content — strongest conversion rate for bottom-funnel strategy.",
            f"Pair **{bc['best_reach']}** content with stronger CTAs — high visibility but needs clearer conversion paths.",
            f"Focus on reducing the **{dropoff['from_stage']} → {dropoff['to_stage']}** drop-off to improve end-to-end conversion.",
        ]
        for i, rec in enumerate(recs):
            with rec_cols[i % 3]:
                st.info(rec)

    # ================================================================
    # TAB 2 — Detailed text report (original insights)
    # ================================================================
    with tab_report:
        st.markdown("#### Campaign Classification")
        classified = df.copy()
        classified["Theme"] = classified.apply(classify_campaign_theme, axis=1)
        classified["Intent"] = classified.apply(classify_campaign_intent, axis=1)
        classified["Funnel Stage"] = classified.apply(classify_funnel_stage, axis=1)

        st.dataframe(
            classified[
                ["campaign_id", "campaign_name", "platform", "content_type",
                 "Theme", "Intent", "Funnel Stage"]
            ].rename(columns={
                "campaign_id": "ID", "campaign_name": "Campaign",
                "platform": "Platform", "content_type": "Content Type",
            }),
            use_container_width=True, hide_index=True,
        )

        st.markdown("---")
        st.markdown("#### Platform Performance Summary")
        st.markdown(summarize_platform_performance(df))

        st.markdown("---")
        st.markdown("#### Content Performance Summary")
        st.markdown(summarize_content_performance(df))

        st.markdown("---")
        st.markdown("#### Funnel Diagnosis")
        st.markdown(identify_funnel_issue(df))

        st.markdown("---")
        st.markdown("#### Executive Recommendations")
        st.markdown(generate_founder_recommendations(df))

        st.markdown("---")
        st.markdown("#### Executive Summary Report")

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
            st.markdown("##### What is Working")
            bp = get_best_platform(df)
            bc = get_best_content_type(df)
            st.markdown(f"- **{bp['best_reach']}** leads in reach and visibility")
            st.markdown(f"- **{bp['best_conversion_rate']}** delivers the strongest conversion efficiency")
            st.markdown(f"- **{bc['best_leads']}** content generates the most leads")
            st.markdown(f"- **{bc['best_conversion_rate']}** content has the highest conversion rate")

        with col2:
            st.markdown("##### What Needs Attention")
            dropoff = get_biggest_dropoff(df)
            st.markdown(
                f"- Largest funnel drop-off: **{dropoff['from_stage']} → {dropoff['to_stage']}** "
                f"({dropoff['drop_pct']}%)"
            )
            st.markdown(f"- Overall funnel efficiency is only **{overall_rate:.2f}%**")
            st.markdown("- High-reach channels are not always the highest converters")
            st.markdown("- Some content types drive awareness but underperform on lead quality")
