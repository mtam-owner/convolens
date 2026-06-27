from pathlib import Path

import streamlit as st


ASSET_DIR = Path(__file__).resolve().parent / "assets"
CSS_FILE = ASSET_DIR / "style.css"


def load_css() -> None:
    if CSS_FILE.exists():
        st.markdown(
            f"<style>{CSS_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


st.set_page_config(
    page_title="ConvoLens",
    layout="wide",
)

load_css()

st.title("ConvoLens")

st.markdown(
    '<div class="section-caption">Conversation Intelligence Platform for Customer Support Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
ConvoLens is an end-to-end analytics platform designed to transform large-scale customer support conversations into actionable operational intelligence.

Built using Streamlit, Python and Plotly, the application combines conversation reconstruction, NLP-based feature engineering, business intelligence dashboards and an AI-ready analysis layer to support operational monitoring, customer experience analysis and support decision making.
"""
)

st.divider()

st.subheader("Available Workspaces")

col1, col2 = st.columns(2, gap="large")

with col1:

    st.markdown(
        """
<div class="workspace-card">
<div class="workspace-title">Executive Dashboard</div>

<div class="workspace-text">
Monitor conversation volume, operational workload, response performance, intent distribution and high-risk conversations through executive-level KPIs and trend analysis.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="workspace-card">
<div class="workspace-title">Conversation Intelligence</div>

<div class="workspace-text">
Explore emerging customer issues, intent trends, company benchmarking and conversation risk patterns through aggregated analytical visualisations.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with col2:

    st.markdown(
        """
<div class="workspace-card">
<div class="workspace-title">Conversation Explorer</div>

<div class="workspace-text">
Search, filter and investigate reconstructed conversations with detailed metadata, investigation signals and chronological conversation timelines.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="workspace-card">
<div class="workspace-title">AI Workspace</div>

<div class="workspace-text">
Prototype workspace demonstrating AI-assisted conversation interpretation, root-cause analysis and recommended support actions using a modular AI engine designed for future LLM integration.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.divider()

st.subheader("Technology Stack")

st.markdown(
"""
- **Programming:** Python
- **Framework:** Streamlit
- **Visualisation:** Plotly
- **Data Processing:** Pandas
- **Storage:** Apache Parquet
- **Natural Language Processing:** Rule-based NLP Feature Engineering
- **AI Architecture:** Modular AI analysis layer (LLM-ready)
"""
)