from pathlib import Path

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[3]

PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DEMO_DIR = ROOT_DIR / "data" / "demo"


@st.cache_data(show_spinner="Loading conversation data...")
def load_conversations() -> pd.DataFrame:
    candidates = [
        PROCESSED_DIR / "conversations_enriched.parquet",
        PROCESSED_DIR / "conversations_scored.parquet",
        PROCESSED_DIR / "conversations.parquet",
        DEMO_DIR / "conversations.parquet",
    ]

    for file_path in candidates:
        if file_path.exists():
            return pd.read_parquet(file_path)

    raise FileNotFoundError(
        "No conversation dataset found in data/processed or data/demo."
    )


@st.cache_data(show_spinner="Loading message data...")
def load_messages() -> pd.DataFrame:
    candidates = [
        PROCESSED_DIR / "messages.parquet",
        DEMO_DIR / "messages.parquet",
    ]

    for file_path in candidates:
        if file_path.exists():
            return pd.read_parquet(file_path)

    raise FileNotFoundError(
        "No message dataset found in data/processed or data/demo."
    )


@st.cache_data(show_spinner="Loading analytics data...")
def load_analytics() -> pd.DataFrame:
    candidates = [
        PROCESSED_DIR / "analytics.parquet",
        DEMO_DIR / "analytics.parquet",
    ]

    for file_path in candidates:
        if file_path.exists():
            return pd.read_parquet(file_path)

    raise FileNotFoundError(
        "No analytics dataset found in data/processed or data/demo."
    )