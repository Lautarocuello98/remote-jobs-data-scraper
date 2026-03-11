import pandas as pd
from src.cleaner import JOB_COLUMNS, clean_jobs_dataframe, jobs_to_dataframe


def test_clean_jobs_dataframe_removes_duplicates():
    df = pd.DataFrame([
        {
            "title": "Python Dev",
            "company": "Acme",
            "location": "Remote",
            "tags": "Python, API",
            "salary": "$100k",
            "date_posted": "2026-03-11",
            "job_url": "https://example.com/job1",
            "source": "RemoteOK",
        },
        {
            "title": "Python Dev",
            "company": "Acme",
            "location": "Remote",
            "tags": "Python, API",
            "salary": "$100k",
            "date_posted": "2026-03-11",
            "job_url": "https://example.com/job1",
            "source": "RemoteOK",
        },
    ])

    cleaned = clean_jobs_dataframe(df)

    assert len(cleaned) == 1


def test_jobs_to_dataframe_has_expected_columns_when_empty():
    df = jobs_to_dataframe([])

    assert df.empty
    assert list(df.columns) == JOB_COLUMNS
