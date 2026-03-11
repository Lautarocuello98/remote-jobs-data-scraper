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
