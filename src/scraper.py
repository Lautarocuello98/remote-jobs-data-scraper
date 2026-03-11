import requests
from src.config import BASE_URL, HEADERS, REQUEST_TIMEOUT


def fetch_jobs_page(url: str = BASE_URL) -> str:
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch jobs page: {exc}") from exc