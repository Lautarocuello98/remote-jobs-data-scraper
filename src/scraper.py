import requests

from src.config import HEADERS, REQUEST_TIMEOUT


API_URL = "https://remoteok.com/api"


def fetch_jobs_data() -> list[dict]:
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise RuntimeError("Unexpected API response format.")

        return data

    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to fetch jobs data: {exc}") from exc