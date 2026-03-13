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


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = str(value).strip()
    return normalized or None


def _parse_positive_int(value: str | None) -> int | None:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return None

    try:
        parsed = int(normalized)
    except ValueError:
        return None

    return parsed if parsed > 0 else None


def _parse_csv_filter(value: str | None) -> list[str]:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return []

    values: list[str] = []
    for item in normalized.split(","):
        parsed_item = item.strip().lower()
        if parsed_item:
            values.append(parsed_item)

    return values


def _parse_bool_env(value: str | None, default: bool = False) -> bool:
    normalized = _normalize_optional_text(value)
    if normalized is None:
        return default

    lowered = normalized.lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False

    return default


REQUEST_TIMEOUT = _parse_request_timeout(os.getenv("REQUEST_TIMEOUT"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)
JOB_KEYWORD = _normalize_optional_text(os.getenv("JOB_KEYWORD"))
JOB_LOCATION = _normalize_optional_text(os.getenv("JOB_LOCATION"))
JOB_TAGS = _parse_csv_filter(os.getenv("JOB_TAGS"))
ONLY_REMOTE_LOCATION = _parse_bool_env(os.getenv("ONLY_REMOTE_LOCATION"), default=False)
MAX_JOB_AGE_DAYS = _parse_positive_int(os.getenv("MAX_JOB_AGE_DAYS"))

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

REQUIRED_DIRS = [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR]
