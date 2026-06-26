import gc

import pandas as pd

from convolens.data import (
    add_conversation_ids,
    build_conversation_table,
    clean_messages,
    load_twitter_data,
    validate_dataset,
)
from convolens.utils.paths import PROCESSED_DATA_DIR, RAW_DATA_DIR


def main():
    raw_path = RAW_DATA_DIR / "twcs.csv"
    messages_path = PROCESSED_DATA_DIR / "messages.parquet"
    conversations_path = PROCESSED_DATA_DIR / "conversations.parquet"

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading raw data...")
    raw = load_twitter_data(raw_path)
    validate_dataset(raw)

    print("Cleaning messages...")
    messages = clean_messages(raw)
    del raw
    gc.collect()

    print("Adding conversation IDs...")
    messages = add_conversation_ids(messages)

    print("Saving messages...")
    messages.to_parquet(messages_path, index=False)

    print("Building conversations...")
    conversations = build_conversation_table(messages)

    print("Saving conversations...")
    conversations.to_parquet(conversations_path, index=False)

    print("Pipeline completed.")
    print(f"Messages: {len(messages):,}")
    print(f"Conversations: {len(conversations):,}")
    print(f"Messages saved to: {messages_path}")
    print(f"Conversations saved to: {conversations_path}")


if __name__ == "__main__":
    main()