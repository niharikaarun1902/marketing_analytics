import streamlit as st
import pandas as pd
from utils.data_loader import load_merged_data


def apply_sidebar_filters() -> pd.DataFrame:
    """Load merged data and apply sidebar multiselect filters.
    Reusable across all pages so filters are consistent everywhere.
    """
    df = load_merged_data()

    st.sidebar.header("Filters")

    platforms = sorted(df["platform"].unique())
    selected_platforms = st.sidebar.multiselect(
        "Platform", platforms, default=platforms, key="filter_platform"
    )

    content_types = sorted(df["content_type"].unique())
    selected_content_types = st.sidebar.multiselect(
        "Content Type", content_types, default=content_types, key="filter_content_type"
    )

    segments = sorted(df["audience_segment"].unique())
    selected_segments = st.sidebar.multiselect(
        "Audience Segment", segments, default=segments, key="filter_audience_segment"
    )

    filtered = df[
        (df["platform"].isin(selected_platforms))
        & (df["content_type"].isin(selected_content_types))
        & (df["audience_segment"].isin(selected_segments))
    ]

    return filtered
