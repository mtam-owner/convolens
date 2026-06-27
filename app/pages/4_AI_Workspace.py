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
    '<div class="section-caption">Prototype workspace for AI-assisted conversation interpretation and support recommendations</div>',
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

left, right = st.columns([1, 1.35], gap="large")

with left:
    st.subheader("Review Queue")
    st.markdown(
        f'<div class="section-caption">{len(filtered):,} conversations available for AI-assisted review</div>',
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
    st.subheader("AI-Assisted Interpretation")

    st.markdown("#### Summary")
    st.write(analysis["summary"])

    st.markdown("#### Customer Sentiment")
    st.write(analysis["sentiment"])

    st.markdown("#### Likely Root Cause")
    st.write(analysis["root_cause"])

    st.markdown("#### Suggested Next Action")
    st.write(analysis["suggested_action"])

    confidence = analysis["confidence"]

    st.markdown("#### Analysis Confidence")

    left, right = st.columns([5, 1])

    with left:
        st.progress(confidence)

    with right:
        st.markdown(
            f"""
            <div style="
                text-align:right;
                font-size:20px;
                font-weight:600;
                margin-top:2px;">
                {confidence:.0%}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader("Conversation Context")

    context1, context2, context3 = st.columns(3)

    with context1:
        st.markdown("**Company**")
        st.write(selected["company"])

    with context2:
        st.markdown("**Intent**")
        st.write(selected["intent"])

    with context3:
        st.markdown("**Risk Level**")
        st.write(selected["risk_level"])

    st.markdown("**Risk Reason**")
    st.write(selected["risk_reason"])

    st.markdown("**Conversation Text**")
    st.text_area(
        "Source conversation",
        selected["conversation_text"],
        height=260,
        label_visibility="collapsed",
    )

    st.divider()

    st.subheader("Implementation Note")
    st.info(
        "This portfolio version uses a local rule-based AI analysis layer. "
        "In a production deployment, the functions in `src/convolens/features/ai_analysis.py` "
        "can be replaced with an enterprise LLM provider such as Azure OpenAI, OpenAI, Gemini, "
        "Claude, or an internal model. No API keys or external calls are included in this public demo."
    )