from datetime import datetime, timedelta, timezone

from src.parser import parse_jobs


def test_parse_jobs_returns_list():
    sample_payload = [
        {"id": 0, "date": "2026-03-11T00:00:00+00:00"},
        {
            "position": "Python Developer",
            "company": "Test Company",
            "location": "Worldwide",
            "tags": ["Python", "Backend"],
            "salary_min": 60000,
            "salary_max": 90000,
            "date": "2026-03-11T00:00:00+00:00",
            "url": "https://remoteok.com/remote-jobs/test-job",
        },
    ]

    jobs = parse_jobs(sample_payload)

    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"
    assert jobs[0].company == "Test Company"
    assert jobs[0].location == "Worldwide"
    assert jobs[0].tags == "Python, Backend"
    assert jobs[0].salary == "60000-90000"


def test_parse_jobs_handles_zero_salary_values():
    sample_payload = [
        {
            "position": "Junior Python Developer",
            "company": "Acme",
            "salary_min": 0,
            "salary_max": 50000,
            "url": "https://remoteok.com/remote-jobs/junior-python-dev",
        }
    ]

    jobs = parse_jobs(sample_payload)

    assert len(jobs) == 1
    assert jobs[0].salary == "0-50000"


def test_parse_jobs_maps_zero_to_zero_salary_to_none():
    sample_payload = [
        {
            "position": "Support Engineer",
            "company": "Acme",
            "salary_min": 0,
            "salary_max": 0,
            "url": "https://remoteok.com/remote-jobs/support-engineer",
        }
    ]

    jobs = parse_jobs(sample_payload)

    assert len(jobs) == 1
    assert jobs[0].salary is None


def test_parse_jobs_applies_keyword_tag_and_location_filters():
    sample_payload = [
        {
            "position": "Python Backend Developer",
            "company": "Acme",
            "location": "Remote - US",
            "tags": ["Python", "Backend"],
            "url": "https://remoteok.com/remote-jobs/python-backend",
        },
        {
            "position": "Frontend Engineer",
            "company": "Acme",
            "location": "Berlin",
            "tags": ["JavaScript", "React"],
            "url": "https://remoteok.com/remote-jobs/frontend-engineer",
        },
    ]

    jobs = parse_jobs(
        sample_payload,
        keyword="python",
        tags_filter=["backend"],
        location="remote",
    )

    assert len(jobs) == 1
    assert jobs[0].title == "Python Backend Developer"


def test_parse_jobs_only_remote_location_filter():
    sample_payload = [
        {
            "position": "Data Engineer",
            "company": "Acme",
            "location": "Remote",
            "url": "https://remoteok.com/remote-jobs/data-engineer",
        },
        {
            "position": "Data Engineer Onsite",
            "company": "Acme",
            "location": "New York",
            "url": "https://remoteok.com/remote-jobs/data-engineer-onsite",
        },
    ]

    jobs = parse_jobs(sample_payload, only_remote_location=True)

    assert len(jobs) == 1
    assert jobs[0].location == "Remote"


def test_parse_jobs_filters_by_max_job_age_days():
    now = datetime.now(timezone.utc)
    recent = (now - timedelta(days=1)).isoformat()
    old = (now - timedelta(days=20)).isoformat()

    sample_payload = [
        {
            "position": "Recent Job",
            "company": "Acme",
            "date": recent,
            "url": "https://remoteok.com/remote-jobs/recent",
        },
        {
            "position": "Old Job",
            "company": "Acme",
            "date": old,
            "url": "https://remoteok.com/remote-jobs/old",
        },
    ]

    jobs = parse_jobs(sample_payload, max_job_age_days=7)

    assert len(jobs) == 1
    assert jobs[0].title == "Recent Job"
