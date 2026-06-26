from pathlib import Path

import pandas as pd


def load_twitter_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load the raw Twitter Customer Support dataset.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(file_path)