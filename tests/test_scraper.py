import pytest
import requests

import src.scraper as scraper


class _InvalidJsonResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> list[dict]:
        raise ValueError("invalid json")


class _NonListJsonResponse:
    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return {"status": "ok"}


def test_fetch_jobs_data_raises_runtime_error_on_request_failure(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException("network error")

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    with pytest.raises(RuntimeError, match="Failed to fetch jobs data"):
        scraper.fetch_jobs_data()


def test_fetch_jobs_data_raises_runtime_error_on_invalid_json(monkeypatch):
    def fake_get(*args, **kwargs):
        return _InvalidJsonResponse()

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    with pytest.raises(RuntimeError, match="decode jobs API response as JSON"):
        scraper.fetch_jobs_data()


def test_fetch_jobs_data_raises_runtime_error_on_non_list_json(monkeypatch):
    def fake_get(*args, **kwargs):
        return _NonListJsonResponse()

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    with pytest.raises(RuntimeError, match="Unexpected API response format"):
        scraper.fetch_jobs_data()
