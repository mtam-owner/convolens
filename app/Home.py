from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA = ROOT_DIR / "data" / "processed" / "conversations.parquet"


@st.cache_data
def load_conversations() -> pd.DataFrame:
    return pd.read_parquet(PROCESSED_DATA)


st.set_page_config(
    page_title="ConvoLens",
    page_icon="💬",
    layout="wide",
)

st.title("ConvoLens")
st.caption("AI Conversation Intelligence Platform for Customer Support Analytics")

if not PROCESSED_DATA.exists():
    st.error(
        "Processed data not found. Please place conversations.parquet inside data/processed/."
    )
    st.stop()

conversations = load_conversations()

st.subheader("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Conversations", f"{len(conversations):,}")
col2.metric("Messages", f"{conversations['message_count'].sum():,}")
col3.metric(
    "Avg Messages",
    f"{conversations['message_count'].mean():.1f}",
)
col4.metric(
    "Avg Duration",
    f"{conversations['duration_minutes'].mean():.1f} min",
)

st.divider()

st.subheader("Conversation Explorer")

search_term = st.text_input("Search conversation text")

min_messages, max_messages = st.slider(
    "Message count range",
    min_value=int(conversations["message_count"].min()),
    max_value=int(conversations["message_count"].max()),
    value=(
        int(conversations["message_count"].min()),
        min(20, int(conversations["message_count"].max())),
    ),
)

filtered = conversations[
    conversations["message_count"].between(min_messages, max_messages)
]

if search_term:
    filtered = filtered[
        filtered["conversation_text"]
        .fillna("")
        .str.contains(search_term, case=False, regex=False)
    ]

st.write(f"Showing **{len(filtered):,}** conversations")

preview_cols = [
    "conversation_id",
    "start_time",
    "message_count",
    "customer_message_count",
    "company_message_count",
    "duration_minutes",
    "conversation_word_count",
]

st.dataframe(
    filtered[preview_cols].head(100),
    use_container_width=True,
)

st.subheader("Conversation Preview")

if len(filtered) > 0:
    selected_id = st.selectbox(
        "Select a conversation",
        filtered["conversation_id"].head(500).tolist(),
    )

    selected = filtered[
        filtered["conversation_id"] == selected_id
    ].iloc[0]

    st.markdown(f"**Conversation ID:** {selected['conversation_id']}")
    st.markdown(f"**Messages:** {selected['message_count']}")
    st.markdown(f"**Duration:** {selected['duration_minutes']:.1f} minutes")

    st.text_area(
        "Conversation text",
        selected["conversation_text"],
        height=350,
    )
else:
    st.info("No conversations match the selected filters.")