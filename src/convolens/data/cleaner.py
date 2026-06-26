from __future__ import annotations

import pandas as pd


def clean_messages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize the raw Twitter messages.

    This function performs only structural cleaning.
    It does NOT perform NLP preprocessing.
    """

    messages = df.copy()

    # Parse timestamp
    messages["created_at"] = pd.to_datetime(
        messages["created_at"],
        format="%a %b %d %H:%M:%S %z %Y",
        errors="coerce",
        utc=True,
    )

    # Standardize text
    messages["text"] = (
        messages["text"]
        .fillna("")
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

    # Ensure IDs remain integers where possible
    # tweet_id is always an integer
    messages["tweet_id"] = messages["tweet_id"].astype("int64")

    # Parent tweet ID (nullable integer)
    messages["in_response_to_tweet_id"] = (
        pd.to_numeric(
            messages["in_response_to_tweet_id"],
            errors="coerce",
        )
        .astype("Int64")
    )

    # Keep response tweet IDs as strings because one tweet can have multiple replies
    messages["response_tweet_id"] = (
        messages["response_tweet_id"]
        .fillna("")
        .astype(str)
    )

    # Sort chronologically
    messages = (
        messages
        .sort_values("created_at")
        .reset_index(drop=True)
    )

    return messages