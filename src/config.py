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

BASE_URL = "https://remoteok.com/remote-dev-jobs"
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

MAX_PAGES = int(os.getenv("MAX_PAGES", "1"))

REQUIRED_DIRS = [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR]