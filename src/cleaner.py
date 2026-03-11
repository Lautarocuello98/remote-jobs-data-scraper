import pandas as pd
from src.models import JobRecord


def jobs_to_dataframe(jobs: list[JobRecord]) -> pd.DataFrame:
    return pd.DataFrame([job.to_dict() for job in jobs])


def clean_jobs_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    cleaned = df.copy()

    text_columns = ["title", "company", "location", "tags", "salary", "job_url", "source"]
    for col in text_columns:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].fillna("").astype(str).str.strip()

    cleaned["location"] = cleaned["location"].replace("", "Remote")
    cleaned["source"] = cleaned["source"].replace("", "RemoteOK")

    cleaned = cleaned.drop_duplicates(subset=["title", "company", "job_url"])
    cleaned = cleaned.sort_values(by=["company", "title"]).reset_index(drop=True)

    return cleaned