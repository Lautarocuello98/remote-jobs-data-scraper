from src.config import (
    REQUIRED_DIRS,
    JOB_KEYWORD,
    JOB_TAGS,
    JOB_LOCATION,
    ONLY_REMOTE_LOCATION,
    MAX_JOB_AGE_DAYS,
)
from src.scraper import fetch_jobs_data
from src.parser import parse_jobs
from src.cleaner import jobs_to_dataframe, clean_jobs_dataframe
from src.exporter import export_raw_csv, export_clean_csv, export_excel, export_json


def ensure_directories() -> None:
    for directory in REQUIRED_DIRS:
        directory.mkdir(parents=True, exist_ok=True)


def _format_active_filters() -> str:
    active_filters: list[str] = []

    if JOB_KEYWORD:
        active_filters.append(f"keyword='{JOB_KEYWORD}'")
    if JOB_TAGS:
        active_filters.append(f"tags={JOB_TAGS}")
    if JOB_LOCATION:
        active_filters.append(f"location='{JOB_LOCATION}'")
    if ONLY_REMOTE_LOCATION:
        active_filters.append("only_remote_location=True")
    if MAX_JOB_AGE_DAYS is not None:
        active_filters.append(f"max_job_age_days={MAX_JOB_AGE_DAYS}")

    return ", ".join(active_filters) if active_filters else "none"


def run_pipeline() -> None:
    ensure_directories()

    data = fetch_jobs_data()
    print(f"Records fetched: {len(data)}")
    print(f"Active filters: {_format_active_filters()}")

    jobs = parse_jobs(
        data,
        keyword=JOB_KEYWORD,
        tags_filter=JOB_TAGS,
        location=JOB_LOCATION,
        only_remote_location=ONLY_REMOTE_LOCATION,
        max_job_age_days=MAX_JOB_AGE_DAYS,
    )
    print(f"Jobs parsed: {len(jobs)}")

    raw_df = jobs_to_dataframe(jobs)
    print(f"Raw rows: {len(raw_df)}")

    clean_df = clean_jobs_dataframe(raw_df)
    print(f"Clean rows: {len(clean_df)}")

    export_raw_csv(raw_df)
    export_clean_csv(clean_df)
    export_excel(clean_df)
    export_json(clean_df)

    print("Pipeline completed successfully.")
