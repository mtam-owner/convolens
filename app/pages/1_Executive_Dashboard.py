from pathlib import Path

import pandas as pd
import streamlit as st

from convolens.components.cards import kpi_card
from convolens.services.data_loader import load_conversations
from convolens.visualization.dashboard import (
    conversation_length_distribution,
    conversation_volume_trend,
    response_time_distribution,
    risk_level_distribution,
    top_companies_chart,
    top_high_risk_companies,
)


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
CSS_FILE = ASSET_DIR / "style.css"


def load_css() -> None:
    if CSS_FILE.exists():
        st.markdown(
            f"<style>{CSS_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


def format_seconds_from_minutes(value) -> str:
    if pd.isna(value):
        return "No reply"

    total_seconds = int(round(float(value) * 60))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


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

    selected_risk_levels = st.multiselect(
        "Risk level",
        options=["High", "Medium", "Low"],
        default=[],
    )

    min_messages = st.slider(
        "Minimum messages",
        min_value=1,
        max_value=50,
        value=1,
    )

filtered = conversations[conversations["message_count"] >= min_messages].copy()

if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

if selected_risk_levels:
    filtered = filtered[filtered["risk_level"].isin(selected_risk_levels)]

st.subheader("Operational Overview")

total_conversations = len(filtered)
total_messages = filtered["message_count"].sum()

avg_response = filtered["response_time_minutes"].dropna().mean()
avg_escalation = filtered["escalation_score"].mean()

high_risk_count = (filtered["risk_level"] == "High").sum()
high_risk_rate = (
    high_risk_count / total_conversations * 100 if total_conversations > 0 else 0
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kpi_card("Conversations", f"{total_conversations:,}")

with col2:
    kpi_card("Messages", f"{total_messages:,}")

with col3:
    kpi_card("Average Response Time", format_seconds_from_minutes(avg_response))

with col4:
    kpi_card("High Risk Rate", f"{high_risk_rate:.1f}%")

with col5:
    kpi_card("Average Escalation", f"{avg_escalation:.3f}")

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
    st.plotly_chart(
        risk_level_distribution(filtered),
        use_container_width=True,
    )

st.divider()

st.subheader("Risk Concentration")

st.plotly_chart(
    top_high_risk_companies(filtered),
    use_container_width=True,
)

st.divider()

st.subheader("Operational Attention")

attention = (
    filtered.sort_values(
        ["escalation_score", "message_count", "duration_minutes"],
        ascending=False,
    )
    .head(20)
    [
        [
            "conversation_id",
            "company",
            "risk_level",
            "escalation_score",
            "risk_reason",
            "message_count",
            "duration_minutes",
            "response_time_minutes",
        ]
    ]
    .copy()
)

attention["escalation_score"] = attention["escalation_score"].round(3)
attention["duration"] = attention["duration_minutes"].apply(format_seconds_from_minutes)
attention["response_time"] = attention["response_time_minutes"].apply(
    format_seconds_from_minutes
)

attention = attention[
    [
        "conversation_id",
        "company",
        "risk_level",
        "escalation_score",
        "risk_reason",
        "message_count",
        "duration",
        "response_time",
    ]
]

attention.columns = [
    "Conversation ID",
    "Company",
    "Risk Level",
    "Escalation Score",
    "Risk Reason",
    "Messages",
    "Duration",
    "Response Time",
]

st.dataframe(
    attention,
    use_container_width=True,
    hide_index=True,
)