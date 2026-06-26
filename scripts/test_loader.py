from convolens.data import (
    clean_messages,
    load_twitter_data,
    validate_dataset,
)
from convolens.utils.paths import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
)


def main():

    df = load_twitter_data(
        RAW_DATA_DIR / "twcs.csv"
    )

    validate_dataset(df)

    messages = clean_messages(df)

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        PROCESSED_DATA_DIR /
        "messages.parquet"
    )

    messages.to_parquet(
        output_path,
        index=False,
    )

    print("Dataset loaded successfully.")
    print(f"Rows: {len(messages):,}")
    print(f"Columns: {len(messages.columns)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()