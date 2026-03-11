from src.parser import parse_jobs


def test_parse_jobs_returns_list():
    sample_html = """
    <table>
        <tr class="job" data-href="/l/test-job">
            <td class="company">
                <h3>Test Company</h3>
                <h2>Python Developer</h2>
                <div class="location">Worldwide</div>
                <div class="tags">
                    <h3>Python</h3>
                    <h3>Backend</h3>
                </div>
                <div class="salary">$60k-$90k</div>
                <time datetime="2026-03-11"></time>
            </td>
        </tr>
    </table>
    """

    jobs = parse_jobs(sample_html)

    assert len(jobs) == 1
    assert jobs[0].title == "Python Developer"
    assert jobs[0].company == "Test Company"
    assert jobs[0].location == "Worldwide"