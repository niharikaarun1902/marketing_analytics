import streamlit as st
import pandas as pd
from utils.data_loader import load_merged_data


def apply_filters(container) -> pd.DataFrame:
    """Load merged data and render filters inside *container*.

    Parameters
    ----------
    container : streamlit column / container / sidebar
        The Streamlit container where the filter widgets will be rendered.
    """
    df = load_merged_data()

    with container:
        st.markdown(
            "<h4 style='color:#2E8B57; margin-bottom:0.5rem;'>Filters</h4>",
            unsafe_allow_html=True,
        )

        platforms = sorted(df["platform"].unique())
        selected_platforms = st.multiselect(
            "Platform", platforms, default=platforms, key="filter_platform"
        )

        content_types = sorted(df["content_type"].unique())
        selected_content_types = st.multiselect(
            "Content Type", content_types, default=content_types, key="filter_content_type"
        )

        segments = sorted(df["audience_segment"].unique())
        selected_segments = st.multiselect(
            "Audience Segment", segments, default=segments, key="filter_audience_segment"
        )

    filtered = df[
        (df["platform"].isin(selected_platforms))
        & (df["content_type"].isin(selected_content_types))
        & (df["audience_segment"].isin(selected_segments))
    ]

    return filtered
