import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.filters import apply_sidebar_filters
from utils.metrics import content_type_metrics

st.title("Content Analysis")

df = apply_sidebar_filters()
ct = content_type_metrics(df)

# --- Engagement by content type ---
st.subheader("Engagement Metrics by Content Type")

fig = go.Figure()
fig.add_trace(go.Bar(name="Impressions", x=ct["content_type"], y=ct["impressions"]))
fig.add_trace(go.Bar(name="Clicks", x=ct["content_type"], y=ct["clicks"]))
fig.add_trace(go.Bar(name="Likes", x=ct["content_type"], y=ct["likes"]))
fig.update_layout(barmode="group", xaxis_title="Content Type", yaxis_title="Count")
st.plotly_chart(fig, width="stretch")

# --- Leads & Conversions ---
st.subheader("Leads & Conversions by Content Type")
col1, col2 = st.columns(2)

with col1:
    fig_leads = px.bar(
        ct.sort_values("leads_generated", ascending=True),
        x="leads_generated",
        y="content_type",
        orientation="h",
        text_auto=True,
        labels={"leads_generated": "Leads Generated", "content_type": ""},
    )
    fig_leads.update_layout(showlegend=False, title="Leads Generated")
    st.plotly_chart(fig_leads, width="stretch")

with col2:
    fig_conv = px.bar(
        ct.sort_values("conversions", ascending=True),
        x="conversions",
        y="content_type",
        orientation="h",
        text_auto=True,
        labels={"conversions": "Conversions", "content_type": ""},
    )
    fig_conv.update_layout(showlegend=False, title="Conversions")
    st.plotly_chart(fig_conv, width="stretch")

# --- Rates table ---
st.subheader("Content Type Performance Ranking")
ranking = ct[["content_type", "campaigns", "ctr", "conversion_rate", "lead_rate"]].sort_values(
    "conversion_rate", ascending=False
)
st.dataframe(
    ranking.rename(columns={
        "content_type": "Content Type",
        "campaigns": "Campaigns",
        "ctr": "CTR (%)",
        "conversion_rate": "Conv. Rate (%)",
        "lead_rate": "Lead Rate (%)",
    }),
    width="stretch",
    hide_index=True,
)

# --- Best performing callout ---
best = ct.loc[ct["conversion_rate"].idxmax()]
st.success(
    f"**Top-performing content type:** {best['content_type']} "
    f"with a {best['conversion_rate']}% conversion rate "
    f"across {int(best['campaigns'])} campaigns."
)
