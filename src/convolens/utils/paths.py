from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample"

DOCS_DIR = ROOT_DIR / "docs"
OUTPUTS_DIR = ROOT_DIR / "outputs"
APP_DIR = ROOT_DIR / "app"