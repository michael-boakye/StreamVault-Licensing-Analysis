from pathlib import Path

# Identify the project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define data locations
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

# Input files
ID_LIST_PATH = DATA_DIR / "id_list.csv"
EXTRACTION_LOG_PATH = DATA_DIR / "extraction_log.csv"

# Output directory
OUTPUT_DIR = PROJECT_ROOT / "out"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)