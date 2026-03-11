import requests

from src.config import HEADERS, REQUEST_TIMEOUT


API_URL = "https://remoteok.com/api"


def fetch_jobs_data() -> list[dict]:
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch jobs data: {exc}") from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Failed to decode jobs API response as JSON.") from exc

    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format.")

    return data
