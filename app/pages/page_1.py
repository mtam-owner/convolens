from pathlib import Path

import streamlit as st

from convolens.components.cards import kpi_card
from convolens.services.data_loader import load_conversations
from convolens.visualization.dashboard import (
    conversation_length_distribution,
    conversation_volume_trend,
    response_time_distribution,
    top_companies_chart,
)


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
CSS_FILE = ASSET_DIR / "style.css"


def load_css() -> None:
    if CSS_FILE.exists():
        st.markdown(
            f"<style>{CSS_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide",
)

load_css()

st.title("Executive Dashboard")
st.markdown(
    '<div class="section-caption">Operational overview of customer support conversations</div>',
    unsafe_allow_html=True,
)

conversations = load_conversations()

with st.sidebar:
    st.header("Filters")

    company_options = sorted(conversations["company"].dropna().unique().tolist())

    selected_companies = st.multiselect(
        "Company",
        options=company_options,
        default=[],
    )

    min_messages = st.slider(
        "Minimum messages",
        min_value=1,
        max_value=50,
        value=1,
    )

filtered = conversations[conversations["message_count"] >= min_messages]

if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

st.subheader("Operational Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card("Conversations", f"{len(filtered):,}")

with col2:
    kpi_card("Messages", f"{filtered['message_count'].sum():,}")

with col3:
    avg_response = filtered["response_time_minutes"].dropna().mean()
    kpi_card("Average Response Time", f"{avg_response:.1f} min")

with col4:
    avg_length = filtered["message_count"].mean()
    kpi_card("Average Length", f"{avg_length:.1f} messages")

st.divider()

st.subheader("Conversation Volume")
st.plotly_chart(
    conversation_volume_trend(filtered),
    use_container_width=True,
)

st.divider()

st.subheader("Operational Performance")

left, right = st.columns(2)

with left:
    st.plotly_chart(
        top_companies_chart(filtered),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        response_time_distribution(filtered),
        use_container_width=True,
    )

left, right = st.columns(2)

with left:
    st.plotly_chart(
        conversation_length_distribution(filtered),
        use_container_width=True,
    )

with right:
    st.markdown("#### Operational Attention")

    attention = (
        filtered.sort_values(
            ["message_count", "duration_minutes"],
            ascending=False,
        )
        .head(20)
        [
            [
                "conversation_id",
                "company",
                "message_count",
                "duration_minutes",
                "response_time_minutes",
                "participant_count",
            ]
        ]
    )

    st.dataframe(
        attention,
        use_container_width=True,
        hide_index=True,
    )