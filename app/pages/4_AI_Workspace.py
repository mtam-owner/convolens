from pathlib import Path

import streamlit as st

from convolens.features.ai_analysis import analyse_conversation
from convolens.services.data_loader import load_conversations


ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"
CSS_FILE = ASSET_DIR / "style.css"


def load_css() -> None:
    if CSS_FILE.exists():
        st.markdown(
            f"<style>{CSS_FILE.read_text()}</style>",
            unsafe_allow_html=True,
        )


st.set_page_config(
    page_title="AI Workspace",
    layout="wide",
)

load_css()

st.title("AI Workspace")
st.markdown(
    '<div class="section-caption">AI-assisted conversation interpretation and recommended support actions</div>',
    unsafe_allow_html=True,
)

conversations = load_conversations()

with st.sidebar:
    st.header("Conversation Selection")

    risk_level = st.selectbox(
        "Risk level",
        ["High", "Medium", "Low"],
    )

    intent_options = sorted(conversations["intent"].dropna().unique().tolist())

    selected_intent = st.selectbox(
        "Intent",
        ["All"] + intent_options,
    )

filtered = conversations[conversations["risk_level"] == risk_level].copy()

if selected_intent != "All":
    filtered = filtered[filtered["intent"] == selected_intent]

filtered = filtered.sort_values(
    ["escalation_score", "message_count"],
    ascending=False,
)

left, right = st.columns([1, 1.3], gap="large")

with left:
    st.subheader("Conversation Queue")
    st.markdown(
        f'<div class="section-caption">{len(filtered):,} conversations available for AI review</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No conversations match the selected filters.")
        st.stop()

    queue = filtered[
        [
            "conversation_id",
            "company",
            "intent",
            "risk_level",
            "escalation_score",
            "message_count",
        ]
    ].head(300).copy()

    queue["escalation_score"] = queue["escalation_score"].round(3)

    st.dataframe(
        queue.rename(
            columns={
                "conversation_id": "Conversation",
                "company": "Company",
                "intent": "Intent",
                "risk_level": "Risk",
                "escalation_score": "Score",
                "message_count": "Messages",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

    selected_id = int(
        st.selectbox(
            "Select conversation",
            queue["conversation_id"].tolist(),
        )
    )

selected = filtered[filtered["conversation_id"] == selected_id].iloc[0]
analysis = analyse_conversation(selected)

with right:
    st.subheader("AI Analysis")

    st.markdown("#### Conversation Summary")
    st.write(analysis["summary"])

    st.markdown("#### Customer Sentiment")
    st.write(analysis["sentiment"])

    st.markdown("#### Likely Root Cause")
    st.write(analysis["root_cause"])

    st.markdown("#### Suggested Next Action")
    st.write(analysis["suggested_action"])

    st.markdown("#### Confidence")
    st.progress(analysis["confidence"])

    st.divider()

    st.subheader("Source Context")

    st.markdown(f"**Company:** {selected['company']}")
    st.markdown(f"**Intent:** {selected['intent']}")
    st.markdown(f"**Risk Level:** {selected['risk_level']}")
    st.markdown(f"**Risk Reason:** {selected['risk_reason']}")