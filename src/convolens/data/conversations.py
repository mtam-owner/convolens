from __future__ import annotations

import pandas as pd


def _build_parent_lookup(messages: pd.DataFrame) -> dict[int, int | None]:
    parent_lookup: dict[int, int | None] = {}

    tweet_ids = messages["tweet_id"].to_numpy()
    parent_ids = messages["in_response_to_tweet_id"].to_numpy()

    for tweet_id, parent_id in zip(tweet_ids, parent_ids):
        tweet_id = int(tweet_id)

        if pd.isna(parent_id):
            parent_lookup[tweet_id] = None
        else:
            parent_lookup[tweet_id] = int(parent_id)

    return parent_lookup


def _find_root_tweet(
    tweet_id: int,
    parent_lookup: dict[int, int | None],
    root_cache: dict[int, int],
) -> int:
    if tweet_id in root_cache:
        return root_cache[tweet_id]

    path = []
    current_id = tweet_id

    while True:
        if current_id in root_cache:
            root_id = root_cache[current_id]
            break

        parent_id = parent_lookup.get(current_id)

        if parent_id is None:
            root_id = current_id
            break

        path.append(current_id)
        current_id = parent_id

    root_cache[tweet_id] = root_id

    for item in path:
        root_cache[item] = root_id

    return root_id


def add_conversation_ids(messages: pd.DataFrame) -> pd.DataFrame:
    output = messages.copy()

    parent_lookup = _build_parent_lookup(output)
    root_cache: dict[int, int] = {}

    output["conversation_id"] = [
        _find_root_tweet(int(tweet_id), parent_lookup, root_cache)
        for tweet_id in output["tweet_id"].to_numpy()
    ]

    output["conversation_id"] = output["conversation_id"].astype("int64")

    return output


def build_conversation_table(messages: pd.DataFrame) -> pd.DataFrame:
    required_columns = {
        "conversation_id",
        "tweet_id",
        "author_id",
        "inbound",
        "created_at",
        "text",
    }

    missing = required_columns - set(messages.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    working = messages[
        [
            "conversation_id",
            "tweet_id",
            "author_id",
            "inbound",
            "created_at",
            "text",
        ]
    ].copy()

    working = working.sort_values(
        ["conversation_id", "created_at", "tweet_id"],
        kind="mergesort",
    )

    working["speaker"] = working["inbound"].map(
        {
            True: "Customer",
            False: "Company",
        }
    )

    working["message_line"] = (
        working["speaker"].astype(str)
        + ": "
        + working["text"].fillna("").astype(str)
    )

    grouped = working.groupby("conversation_id", sort=False)

    conversations = grouped.agg(
        start_time=("created_at", "min"),
        end_time=("created_at", "max"),
        message_count=("tweet_id", "count"),
        customer_message_count=("inbound", "sum"),
        participant_count=("author_id", "nunique"),
        conversation_text=("message_line", "\n".join),
    ).reset_index()

    conversations["company_message_count"] = (
        conversations["message_count"] - conversations["customer_message_count"]
    )

    conversations["duration_minutes"] = (
        conversations["end_time"] - conversations["start_time"]
    ).dt.total_seconds() / 60

    conversations["conversation_word_count"] = (
        conversations["conversation_text"].fillna("").str.split().str.len()
    )

    return conversations[
        [
            "conversation_id",
            "start_time",
            "end_time",
            "duration_minutes",
            "message_count",
            "customer_message_count",
            "company_message_count",
            "participant_count",
            "conversation_word_count",
            "conversation_text",
        ]
    ]