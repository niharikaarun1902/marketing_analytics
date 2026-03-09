import streamlit as st
from utils.filters import apply_sidebar_filters

st.set_page_config(
    page_title="AI-Driven Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("AI-Driven Marketing Workflow Analytics")
st.markdown(
    "A prototype analytics dashboard that models the full marketing workflow — "
    "from campaign planning and simulated publishing to engagement tracking, "
    "lead generation, funnel analysis, and Claude-style intelligence."
)

df = apply_sidebar_filters()

st.markdown("---")
st.subheader("Quick Snapshot")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Campaigns", len(df))
col2.metric("Total Impressions", f"{int(df['impressions'].sum()):,}")
col3.metric("Total Clicks", f"{int(df['clicks'].sum()):,}")
col4.metric("Total Conversions", f"{int(df['conversions'].sum()):,}")

st.info("Use the **sidebar** to filter data across all pages. Navigate using the pages in the sidebar.")
