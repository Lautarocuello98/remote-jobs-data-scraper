from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.config import HEADERS, REQUEST_TIMEOUT


JOBSBOARD_URL = "https://remoteok.com/?action=get_jobs&premium=0&regular=1"


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(str(value).replace("\xa0", " ").split())


def _drop_emoji_prefix(value: str) -> str:
    if " " not in value:
        return value

    first_word, remainder = value.split(" ", 1)
    if len(first_word) == 1 and not first_word.isalnum():
        return remainder.strip()

    return value


def _parse_jobsboard_html(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr.job[data-id]")

    jobs: list[dict] = []
    for row in rows:
        title_elem = row.select_one("h2[itemprop='title']")
        company_elem = row.select_one("h3[itemprop='name']")
        if not title_elem or not company_elem:
            continue

        title = _normalize_text(title_elem.get_text())
        company = _normalize_text(company_elem.get_text())
        if not title or not company:
            continue

        location_elem = row.select_one("div.location")
        location_text = _normalize_text(location_elem.get_text() if location_elem else "")
        location = _drop_emoji_prefix(location_text) or "Remote"

        tags: list[str] = []
        for tag_elem in row.select("td.tags .tag h3"):
            tag = _normalize_text(tag_elem.get_text())
            if tag:
                tags.append(tag)

        salary_elem = row.select_one("div.salary")
        salary_text = _normalize_text(salary_elem.get_text() if salary_elem else "")
        salary = _drop_emoji_prefix(salary_text) or None

        date_elem = row.select_one("time[datetime]")
        date_posted = date_elem.get("datetime", "").strip() if date_elem else None
        if date_posted == "":
            date_posted = None

        url_candidate = (row.get("data-url") or row.get("data-href") or "").strip()
        if not url_candidate:
            url_elem = row.select_one("a[itemprop='url']")
            url_candidate = (url_elem.get("href") if url_elem else "") or ""
        job_url = urljoin("https://remoteok.com", url_candidate).strip()

        jobs.append(
            {
                "position": title,
                "company": company,
                "location": location,
                "tags": tags,
                "salary": salary,
                "date": date_posted,
                "url": job_url,
            }
        )

    return jobs


def fetch_jobs_data() -> list[dict]:
    request_headers = {
        **HEADERS,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    try:
        response = requests.get(JOBSBOARD_URL, headers=request_headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch jobs data: {exc}") from exc

    data = _parse_jobsboard_html(response.text)
    if not data:
        raise RuntimeError("Unexpected jobsboard response format.")

    return data
