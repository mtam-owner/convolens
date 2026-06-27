import pandas as pd

from convolens.features.intent import enrich_with_intent
from convolens.utils.paths import PROCESSED_DATA_DIR


def main() -> None:
    input_path = PROCESSED_DATA_DIR / "conversations_scored.parquet"
    output_path = PROCESSED_DATA_DIR / "conversations_enriched.parquet"

    print("Loading scored conversations...")
    conversations = pd.read_parquet(input_path)

    print("Adding intent labels...")
    enriched = enrich_with_intent(conversations)

    print("Saving enriched conversations...")
    enriched.to_parquet(output_path, index=False)

    print("Intent enrichment completed.")
    print(f"Rows: {len(enriched):,}")
    print(f"Saved to: {output_path}")
    print(enriched["intent"].value_counts())


if __name__ == "__main__":
    main()