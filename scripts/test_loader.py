from convolens.data import load_twitter_data, validate_dataset
from convolens.utils.paths import RAW_DATA_DIR

df = load_twitter_data(RAW_DATA_DIR / "twcs.csv")

validate_dataset(df)

print("Dataset loaded successfully.")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")