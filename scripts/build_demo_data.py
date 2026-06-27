import pandas as pd

from convolens.utils.paths import PROCESSED_DATA_DIR


OUTPUT_DIR = PROCESSED_DATA_DIR.parent / "demo"

OUTPUT_DIR.mkdir(exist_ok=True)


TARGET_PER_GROUP = 30


def main():

    print("Loading datasets...")

    conversations = pd.read_parquet(
        PROCESSED_DATA_DIR / "conversations_enriched.parquet"
    )

    messages = pd.read_parquet(
        PROCESSED_DATA_DIR / "messages.parquet"
    )

    analytics = pd.read_parquet(
        PROCESSED_DATA_DIR / "analytics.parquet"
    )

    print("Selecting representative conversations...")

    demo_conversations = (
        conversations.sort_values(
            [
                "risk_level",
                "intent",
                "message_count",
                "escalation_score",
            ],
            ascending=[True, True, False, False],
        )
        .groupby(
            ["risk_level", "intent"],
            group_keys=False,
        )
        .head(TARGET_PER_GROUP)
        .reset_index(drop=True)
    )

    ids = set(demo_conversations["conversation_id"])

    demo_messages = (
        messages[messages["conversation_id"].isin(ids)]
        .sort_values(["conversation_id", "created_at"])
        .reset_index(drop=True)
    )

    demo_analytics = (
        analytics[analytics["conversation_id"].isin(ids)]
        .reset_index(drop=True)
    )

    print()

    print(f"Conversations : {len(demo_conversations):,}")
    print(f"Messages      : {len(demo_messages):,}")
    print(f"Analytics     : {len(demo_analytics):,}")

    demo_conversations.to_parquet(
        OUTPUT_DIR / "conversations.parquet",
        index=False,
    )

    demo_messages.to_parquet(
        OUTPUT_DIR / "messages.parquet",
        index=False,
    )

    demo_analytics.to_parquet(
        OUTPUT_DIR / "analytics.parquet",
        index=False,
    )

    print()
    print(f"Saved demo dataset to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()