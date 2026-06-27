import pandas as pd

from convolens.utils.paths import PROCESSED_DATA_DIR


def main() -> None:
    input_path = PROCESSED_DATA_DIR / "conversations_enriched.parquet"
    output_path = PROCESSED_DATA_DIR / "analytics.parquet"

    print("Loading enriched conversations...")
    df = pd.read_parquet(input_path)

    print("Building analytics table...")
    df["date"] = pd.to_datetime(df["start_time"]).dt.date
    df["month"] = pd.to_datetime(df["start_time"]).dt.to_period("M").astype(str)

    analytics = df[
        [
            "conversation_id",
            "company",
            "customer_id",
            "date",
            "month",
            "intent",
            "risk_level",
            "escalation_score",
            "message_count",
            "duration_minutes",
            "response_time_minutes",
            "conversation_word_count",
        ]
    ].copy()

    analytics.to_parquet(output_path, index=False)

    print("Analytics dataset completed.")
    print(f"Rows: {len(analytics):,}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()