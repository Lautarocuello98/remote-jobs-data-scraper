from bs4 import BeautifulSoup
from src.models import JobRecord


def parse_jobs(html: str) -> list[JobRecord]:
    soup = BeautifulSoup(html, "html.parser")
    jobs: list[JobRecord] = []

    rows = soup.select("tr.job")

    for row in rows:
        title_el = row.select_one("h2")
        company_el = row.select_one("h3")
        location_el = row.select_one(".location")
        tag_els = row.select(".tags h3")
        salary_el = row.select_one(".salary")
        date_el = row.select_one("time")
        link_el = row.get("data-href")

        title = title_el.get_text(strip=True) if title_el else ""
        company = company_el.get_text(strip=True) if company_el else ""
        location = location_el.get_text(strip=True) if location_el else "Remote"
        tags = ", ".join(tag.get_text(strip=True) for tag in tag_els) if tag_els else ""
        salary = salary_el.get_text(strip=True) if salary_el else None
        date_posted = date_el.get("datetime") if date_el else None

        if link_el and not link_el.startswith("http"):
            job_url = f"https://remoteok.com{link_el}"
        else:
            job_url = link_el or ""

        if not title or not company:
            continue

        jobs.append(
            JobRecord(
                title=title,
                company=company,
                location=location,
                tags=tags,
                salary=salary,
                date_posted=date_posted,
                job_url=job_url,
                source="RemoteOK",
            )
        )

    return jobs