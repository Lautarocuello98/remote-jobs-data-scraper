from src.config import DEFAULT_REQUEST_TIMEOUT, _parse_request_timeout


def test_parse_request_timeout_returns_default_for_invalid_value():
    assert _parse_request_timeout("abc") == DEFAULT_REQUEST_TIMEOUT


def test_parse_request_timeout_returns_default_for_non_positive_value():
    assert _parse_request_timeout("0") == DEFAULT_REQUEST_TIMEOUT
    assert _parse_request_timeout("-10") == DEFAULT_REQUEST_TIMEOUT


def test_parse_request_timeout_accepts_positive_integer():
    assert _parse_request_timeout("45") == 45
