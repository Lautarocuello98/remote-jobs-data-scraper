import pytest
import requests

import src.scraper as scraper


class _HtmlResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    def raise_for_status(self) -> None:
        return None


SAMPLE_JOBSBOARD_HTML = """
<table id="jobsboard">
  <tbody>
    <tr class="job" data-id="123" data-url="/remote-jobs/test-job">
      <td class="company position company_and_position">
        <a itemprop="url" href="/remote-jobs/test-job">
          <h2 itemprop="title">Python Developer</h2>
        </a>
        <span itemprop="hiringOrganization">
          <h3 itemprop="name">Test Company</h3>
        </span>
        <div class="location">Worldwide</div>
        <div class="salary">$100k - $120k</div>
      </td>
      <td class="tags">
        <div class="tag"><h3>Python</h3></div>
        <div class="tag"><h3>Backend</h3></div>
      </td>
      <td class="time">
        <time datetime="2026-03-13T00:00:00+00:00">today</time>
      </td>
    </tr>
  </tbody>
</table>
"""


def test_fetch_jobs_data_raises_runtime_error_on_request_failure(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException("network error")

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    with pytest.raises(RuntimeError, match="Failed to fetch jobs data"):
        scraper.fetch_jobs_data()


def test_fetch_jobs_data_raises_runtime_error_on_invalid_jobsboard_html(monkeypatch):
    def fake_get(*args, **kwargs):
        return _HtmlResponse("<html><body>No jobs here</body></html>")

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    with pytest.raises(RuntimeError, match="Unexpected jobsboard response format"):
        scraper.fetch_jobs_data()


def test_fetch_jobs_data_parses_jobsboard_html(monkeypatch):
    def fake_get(*args, **kwargs):
        return _HtmlResponse(SAMPLE_JOBSBOARD_HTML)

    monkeypatch.setattr(scraper.requests, "get", fake_get)

    jobs = scraper.fetch_jobs_data()

    assert len(jobs) == 1
    assert jobs[0]["position"] == "Python Developer"
    assert jobs[0]["company"] == "Test Company"
    assert jobs[0]["location"] == "Worldwide"
    assert jobs[0]["tags"] == ["Python", "Backend"]
    assert jobs[0]["salary"] == "$100k - $120k"
    assert jobs[0]["date"] == "2026-03-13T00:00:00+00:00"
    assert jobs[0]["url"] == "https://remoteok.com/remote-jobs/test-job"
