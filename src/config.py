from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = BASE_DIR / "output"

RAW_CSV_PATH = RAW_DIR / "jobs_raw.csv"
CLEAN_CSV_PATH = PROCESSED_DIR / "remote_jobs_clean.csv"
OUTPUT_XLSX_PATH = OUTPUT_DIR / "remote_jobs.xlsx"
OUTPUT_JSON_PATH = OUTPUT_DIR / "remote_jobs.json"

DEFAULT_REQUEST_TIMEOUT = 20


def _parse_request_timeout(value: str | None, default: int = DEFAULT_REQUEST_TIMEOUT) -> int:
    if value is None:
        return default

    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return default

    return parsed if parsed > 0 else default


REQUEST_TIMEOUT = _parse_request_timeout(os.getenv("REQUEST_TIMEOUT"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

REQUIRED_DIRS = [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR]
