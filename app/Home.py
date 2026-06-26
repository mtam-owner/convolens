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
    '<div class="section-caption">AI Conversation Intelligence Platform for Customer Support Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    ConvoLens transforms customer support conversations into operational insight.

    The current version includes an executive analytics dashboard and a conversation investigation workspace.
    """
)

st.markdown("### Available Workspaces")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="workspace-card">
            <div class="workspace-title">Executive Dashboard</div>
            <div class="workspace-text">
                Monitor support volume, response performance, company-level workload and conversations requiring operational attention.
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
                Search, filter and inspect reconstructed customer support conversations for internal review.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )