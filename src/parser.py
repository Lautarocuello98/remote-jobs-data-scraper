from src.models import JobRecord


def parse_jobs(data: list[dict]) -> list[JobRecord]:
    jobs: list[JobRecord] = []

    for item in data:
        if not isinstance(item, dict):
            continue

        # suele venir una fila metadata al principio
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
                salary = f"{salary_min}-{salary_max}"
            else:
                salary = str(salary_min if has_min else salary_max)

        date_posted = item.get("date")
        job_url = (item.get("url") or "").strip()

        jobs.append(
            JobRecord(
                title=title,
                company=company,
                location=location,
                tags=tags,
                salary=salary,
                date_posted=str(date_posted) if date_posted else None,
                job_url=job_url,
                source="RemoteOK",
            )
        )

    return jobs
