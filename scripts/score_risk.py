import pandas as pd

from convolens.models.risk_scoring import score_conversation_risk
from convolens.utils.paths import PROCESSED_DATA_DIR


def main() -> None:
    input_path = PROCESSED_DATA_DIR / "conversations.parquet"
    output_path = PROCESSED_DATA_DIR / "conversations_scored.parquet"

    print("Loading conversations...")
    conversations = pd.read_parquet(input_path)

    print("Scoring complaint and escalation risk...")
    scored = score_conversation_risk(conversations)

    print("Saving scored conversations...")
    scored.to_parquet(output_path, index=False)

    print("Risk scoring completed.")
    print(f"Rows: {len(scored):,}")
    print(f"Saved to: {output_path}")
    print(scored["risk_level"].value_counts())


if __name__ == "__main__":
    main()