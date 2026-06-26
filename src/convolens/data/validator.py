from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {
    "tweet_id",
    "author_id",
    "inbound",
    "created_at",
    "text",
    "response_tweet_id",
    "in_response_to_tweet_id",
}


def validate_schema(df: pd.DataFrame) -> None:
    """
    Validate that the dataset contains all required columns.
    """

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing)}"
        )


def validate_duplicates(df: pd.DataFrame) -> None:
    """
    Ensure tweet IDs are unique.
    """

    duplicate_count = df["tweet_id"].duplicated().sum()

    if duplicate_count:
        raise ValueError(
            f"Found {duplicate_count:,} duplicate tweet IDs."
        )


def validate_dataset(df: pd.DataFrame) -> None:
    """
    Run all dataset validation checks.
    """

    validate_schema(df)
    validate_duplicates(df)