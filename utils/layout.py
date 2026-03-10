import streamlit as st

PAGES = [
    ("Home", "app.py"),
    ("Overview", "pages/1_Overview.py"),
    ("Channels", "pages/2_Channel_Performance.py"),
    ("Content", "pages/3_Content_Analysis.py"),
    ("Funnel", "pages/4_Funnel_Analysis.py"),
    ("Insights", "pages/5_Claude_Insights.py"),
    ("Audience", "pages/7_Audience_Segments.py"),
    ("Ask AI", "pages/6_Chat.py"),
]


def setup_page(title: str = "AI-Driven Marketing Analytics") -> None:
    """Call at the top of every page to apply shared styling and nav."""
    try:
        st.set_page_config(
            page_title=title,
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="collapsed",
        )
    except st.errors.StreamlitAPIException:
        pass

    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
    _render_nav()


def _render_nav() -> None:
    cols = st.columns([2] + [1] * (len(PAGES) - 1) + [2])
    with cols[0]:
        st.markdown(
            "<span style='font-weight:800; font-size:1.1rem; color:#2E8B57; "
            "letter-spacing:-0.5px; white-space:nowrap;'>"
            "Marketing Analytics</span>",
            unsafe_allow_html=True,
        )
    for i, (label, page) in enumerate(PAGES):
        with cols[i + 1]:
            st.page_link(page, label=label)
    st.markdown(
        "<hr style='margin:0.3rem 0 1.5rem 0; border:none; "
        "border-top:2px solid #2E8B57;'>",
        unsafe_allow_html=True,
    )


_GLOBAL_CSS = """
<style>
/* ---------- Hide default sidebar nav ---------- */
[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ---------- Top nav links ---------- */
div[data-testid="stHorizontalBlock"] a[data-testid="stPageLink-NavLink"] {
    font-weight: 600;
    font-size: 0.82rem;
    color: #2E8B57 !important;
    border: 1.5px solid transparent;
    border-radius: 6px;
    padding: 0.3rem 0.5rem;
    transition: all 0.15s ease;
    white-space: nowrap;
}
div[data-testid="stHorizontalBlock"] a[data-testid="stPageLink-NavLink"]:hover {
    background-color: #2E8B57;
    color: #fff !important;
    border-color: #2E8B57;
}
div[data-testid="stHorizontalBlock"] a[data-testid="stPageLink-NavLink"]:hover * {
    color: #fff !important;
}

/* ---------- "Ask AI" highlight (last nav link) ---------- */
div[data-testid="stHorizontalBlock"] > div:last-child a[data-testid="stPageLink-NavLink"] {
    border: 2px solid #2E8B57 !important;
    background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%) !important;
    color: #fff !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 6px rgba(46, 139, 87, 0.3);
    padding: 0.3rem 2rem !important;
}
div[data-testid="stHorizontalBlock"] > div:last-child a[data-testid="stPageLink-NavLink"] * {
    color: #fff !important;
}
div[data-testid="stHorizontalBlock"] > div:last-child a[data-testid="stPageLink-NavLink"]:hover {
    background: linear-gradient(135deg, #236B43 0%, #2E8B57 100%) !important;
    box-shadow: 0 3px 10px rgba(46, 139, 87, 0.45);
}

/* ---------- KPI metric cards ---------- */
div[data-testid="stMetric"] {
    background: #F0FFF0;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    border-left: 4px solid #2E8B57;
}
div[data-testid="stMetric"] label {
    color: #555 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #2E8B57 !important;
    font-weight: 800 !important;
}

/* ---------- General polish ---------- */
h1, h2, h3 { color: #1E1E1E; }
h1 { font-weight: 800 !important; }
.stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
"""
