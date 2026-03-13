from datetime import datetime, timedelta, timezone

from src.models import JobRecord


def _is_zero_salary_value(value: object) -> bool:
    try:
        return float(value) == 0.0
    except (TypeError, ValueError):
        return False


def _is_within_age_window(date_posted: str | None, max_job_age_days: int | None) -> bool:
    if max_job_age_days is None:
        return True

    if not date_posted:
        return False

    try:
        posted_dt = datetime.fromisoformat(date_posted.replace("Z", "+00:00"))
    except ValueError:
        return False

    if posted_dt.tzinfo is None:
        posted_dt = posted_dt.replace(tzinfo=timezone.utc)

    now_utc = datetime.now(timezone.utc)
    age = now_utc - posted_dt

    return timedelta(0) <= age <= timedelta(days=max_job_age_days)


def _matches_job_filters(
    job: JobRecord,
    keyword: str | None,
    tags_filter: list[str],
    location: str | None,
    only_remote_location: bool,
    max_job_age_days: int | None,
) -> bool:
    if keyword:
        searchable = " ".join([job.title, job.company, job.location, job.tags]).lower()
        if keyword not in searchable:
            return False

    if tags_filter:
        job_tags = {tag.strip().lower() for tag in job.tags.split(",") if tag.strip()}
        if not job_tags:
            return False
        if not any(tag in job_tags for tag in tags_filter):
            return False

    if location and location not in job.location.lower():
        return False

    if only_remote_location and "remote" not in job.location.lower():
        return False

    if not _is_within_age_window(job.date_posted, max_job_age_days):
        return False

    return True


def parse_jobs(
    data: list[dict],
    keyword: str | None = None,
    tags_filter: list[str] | None = None,
    location: str | None = None,
    only_remote_location: bool = False,
    max_job_age_days: int | None = None,
) -> list[JobRecord]:
    normalized_keyword = keyword.lower().strip() if keyword else None
    normalized_tags = [tag.lower().strip() for tag in (tags_filter or []) if tag and tag.strip()]
    normalized_location = location.lower().strip() if location else None

    jobs: list[JobRecord] = []

    for item in data:
        if not isinstance(item, dict):
            continue

        # API payload often includes a metadata row at the beginning
        title = (item.get("position") or "").strip()
        company = (item.get("company") or "").strip()

        if not title or not company:
            continue

        location = (item.get("location") or "Remote").strip()

        tags_raw = item.get("tags") or []
        if isinstance(tags_raw, list):
            tags = ", ".join(str(tag).strip() for tag in tags_raw if str(tag).strip())
        else:
            tags = str(tags_raw).strip()

        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")

        salary = None
        has_min = salary_min is not None
        has_max = salary_max is not None
        if has_min or has_max:
            if has_min and has_max:
                if not (_is_zero_salary_value(salary_min) and _is_zero_salary_value(salary_max)):
                    salary = f"{salary_min}-{salary_max}"
            else:
                salary_value = salary_min if has_min else salary_max
                if not _is_zero_salary_value(salary_value):
                    salary = str(salary_value)

        date_posted = item.get("date")
        job_url = (item.get("url") or "").strip()

        parsed_job = JobRecord(
            title=title,
            company=company,
            location=location,
            tags=tags,
            salary=salary,
            date_posted=str(date_posted) if date_posted else None,
            job_url=job_url,
            source="RemoteOK",
        )

        if _matches_job_filters(
            parsed_job,
            keyword=normalized_keyword,
            tags_filter=normalized_tags,
            location=normalized_location,
            only_remote_location=only_remote_location,
            max_job_age_days=max_job_age_days,
        ):
            jobs.append(parsed_job)

    return jobs
