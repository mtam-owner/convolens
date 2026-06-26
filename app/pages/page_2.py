from html import escape
from pathlib import Path

import pandas as pd
import streamlit as st

from convolens.services.data_loader import load_conversations, load_messages


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


def render_message(author: str, timestamp, text: str, inbound: bool) -> None:
    css_class = "customer" if inbound else "company"
    speaker = "Customer" if inbound else "Support"

    if pd.isna(timestamp):
        time_display = ""
    else:
        time_display = pd.to_datetime(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    st.markdown(
        f"""
        <div class="message-block {css_class}">
            <div class="message-header">
                <div class="message-author">{speaker} · {escape(str(author))}</div>
                <div class="message-time">{escape(time_display)}</div>
            </div>
            <div class="message-body">{escape(str(text))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Conversation Explorer",
    layout="wide",
)

load_css()

st.title("Conversation Explorer")
st.markdown(
    '<div class="section-caption">Internal review workspace for reconstructed customer support conversations</div>',
    unsafe_allow_html=True,
)

conversations = load_conversations()
messages = load_messages()

with st.sidebar:
    st.header("Filters")

    company_options = sorted(conversations["company"].dropna().unique().tolist())

    selected_companies = st.multiselect(
        "Company",
        options=company_options,
        default=[],
    )

    search_term = st.text_input("Search conversation text")

    min_messages, max_messages = st.slider(
        "Message count",
        min_value=int(conversations["message_count"].min()),
        max_value=min(100, int(conversations["message_count"].max())),
        value=(1, 20),
    )

    sort_option = st.selectbox(
        "Sort by",
        options=[
            "Most messages",
            "Longest duration",
            "Slowest response",
            "Most recent",
        ],
    )

filtered = conversations[
    conversations["message_count"].between(min_messages, max_messages)
].copy()

if selected_companies:
    filtered = filtered[filtered["company"].isin(selected_companies)]

if search_term:
    filtered = filtered[
        filtered["conversation_text"]
        .fillna("")
        .str.contains(search_term, case=False, regex=False)
    ]

sort_map = {
    "Most messages": ["message_count", "duration_minutes"],
    "Longest duration": ["duration_minutes", "message_count"],
    "Slowest response": ["response_time_minutes", "message_count"],
    "Most recent": ["start_time", "message_count"],
}

filtered = filtered.sort_values(sort_map[sort_option], ascending=False)

left, right = st.columns([1.05, 1.4], gap="large")

with left:
    st.subheader("Conversation Queue")
    st.markdown(
        f'<div class="section-caption">{len(filtered):,} conversations match the current filters</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No conversations match the current filters.")
        st.stop()

    queue = filtered[
        [
            "conversation_id",
            "company",
            "start_time",
            "message_count",
            "duration_minutes",
            "response_time_minutes",
        ]
    ].head(300).copy()

    queue["duration"] = queue["duration_minutes"].apply(format_seconds_from_minutes)
    queue["response_time"] = queue["response_time_minutes"].apply(
        format_seconds_from_minutes
    )

    display_queue = queue[
        [
            "conversation_id",
            "company",
            "start_time",
            "message_count",
            "duration",
            "response_time",
        ]
    ]

    st.dataframe(
        display_queue,
        use_container_width=True,
        hide_index=True,
    )

    selected_id = st.selectbox(
        "Select conversation",
        queue["conversation_id"].tolist(),
    )

selected = filtered[filtered["conversation_id"] == selected_id].iloc[0]

selected_messages = (
    messages[messages["conversation_id"] == selected_id]
    .sort_values(["created_at", "tweet_id"])
    .copy()
)

with right:
    st.subheader("Conversation Detail")

    meta1, meta2, meta3 = st.columns(3)

    with meta1:
        st.markdown('<div class="meta-label">Company</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{escape(str(selected["company"]))}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="meta-label">Customer ID</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{escape(str(selected["customer_id"]))}</div>',
            unsafe_allow_html=True,
        )

    with meta2:
        st.markdown('<div class="meta-label">Messages</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{int(selected["message_count"])}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="meta-label">Participants</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{int(selected["participant_count"])}</div>',
            unsafe_allow_html=True,
        )

    with meta3:
        st.markdown('<div class="meta-label">Duration</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{format_seconds_from_minutes(selected["duration_minutes"])}</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<div class="meta-label">Response Time</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="meta-value">{format_seconds_from_minutes(selected["response_time_minutes"])}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Conversation Transcript")

    for row in selected_messages.itertuples(index=False):
        render_message(
            author=row.author_id,
            timestamp=row.created_at,
            text=row.text,
            inbound=bool(row.inbound),
        )