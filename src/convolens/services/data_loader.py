from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"


@st.cache_data(show_spinner="Loading conversation data...")
@st.cache_data(show_spinner="Loading conversation data...")
def load_conversations() -> pd.DataFrame:
    enriched_path = PROCESSED_DIR / "conversations_enriched.parquet"
    scored_path = PROCESSED_DIR / "conversations_scored.parquet"
    base_path = PROCESSED_DIR / "conversations.parquet"

    if enriched_path.exists():
        return pd.read_parquet(enriched_path)

    if scored_path.exists():
        return pd.read_parquet(scored_path)

    if base_path.exists():
        return pd.read_parquet(base_path)

    raise FileNotFoundError("No conversation dataset found in data/processed.")


@st.cache_data(show_spinner="Loading message data...")
def load_messages() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "messages.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            "messages.parquet was not found in data/processed."
        )

    return pd.read_parquet(file_path)

@st.cache_data(show_spinner="Loading analytics data...")
def load_analytics() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "analytics.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            "analytics.parquet was not found in data/processed."
        )

    return pd.read_parquet(file_path)