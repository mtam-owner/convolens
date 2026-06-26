from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]
PROCESSED_DIR = ROOT_DIR / "data" / "processed"


@st.cache_data(show_spinner="Loading conversation data...")
def load_conversations() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "conversations.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            "conversations.parquet was not found in data/processed."
        )

    return pd.read_parquet(file_path)


@st.cache_data(show_spinner="Loading message data...")
def load_messages() -> pd.DataFrame:
    file_path = PROCESSED_DIR / "messages.parquet"

    if not file_path.exists():
        raise FileNotFoundError(
            "messages.parquet was not found in data/processed."
        )

    return pd.read_parquet(file_path)