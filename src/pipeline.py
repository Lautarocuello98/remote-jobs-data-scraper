from src.config import REQUIRED_DIRS
from src.scraper import fetch_jobs_page
from src.parser import parse_jobs
from src.cleaner import jobs_to_dataframe, clean_jobs_dataframe
from src.exporter import export_raw_csv, export_clean_csv, export_excel, export_json


def ensure_directories() -> None:
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)


def run_pipeline() -> None:
    ensure_directories()

    html = fetch_jobs_page()
    jobs = parse_jobs(html)

    raw_df = jobs_to_dataframe(jobs)
    clean_df = clean_jobs_dataframe(raw_df)

    export_raw_csv(raw_df)
    export_clean_csv(clean_df)
    export_excel(clean_df)
    export_json(clean_df)

    print(f"Pipeline completed successfully. Jobs scraped: {len(raw_df)}")