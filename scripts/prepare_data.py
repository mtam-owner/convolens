from convolens.data.load_data import load_raw_twitter_data
from convolens.data.process_conversations import prepare_message_table
from convolens.utils.paths import PROCESSED_DATA_DIR, RAW_DATA_DIR


def main() -> None:
    raw_file = RAW_DATA_DIR / "twcs.csv"
    output_file = PROCESSED_DATA_DIR / "messages_clean.csv"

    print("Loading raw Twitter support data...")
    raw_df = load_raw_twitter_data(raw_file)

    print(f"Raw rows: {len(raw_df):,}")

    print("Preparing clean message table...")
    messages = prepare_message_table(raw_df)

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    messages.to_csv(output_file, index=False)

    print(f"Clean messages saved to: {output_file}")
    print(f"Processed rows: {len(messages):,}")


if __name__ == "__main__":
    main()