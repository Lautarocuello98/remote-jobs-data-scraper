from src.config import (
    DEFAULT_REQUEST_TIMEOUT,
    _parse_bool_env,
    _parse_csv_filter,
    _parse_positive_int,
    _parse_request_timeout,
)


def test_parse_request_timeout_returns_default_for_invalid_value():
    assert _parse_request_timeout("abc") == DEFAULT_REQUEST_TIMEOUT


def test_parse_request_timeout_returns_default_for_non_positive_value():
    assert _parse_request_timeout("0") == DEFAULT_REQUEST_TIMEOUT
    assert _parse_request_timeout("-10") == DEFAULT_REQUEST_TIMEOUT


def test_parse_request_timeout_accepts_positive_integer():
    assert _parse_request_timeout("45") == 45


def test_parse_csv_filter_normalizes_and_splits_values():
    assert _parse_csv_filter(" Python, backend,  Data ") == ["python", "backend", "data"]


def test_parse_positive_int_returns_none_for_invalid_values():
    assert _parse_positive_int(None) is None
    assert _parse_positive_int("0") is None
    assert _parse_positive_int("-1") is None
    assert _parse_positive_int("abc") is None


def test_parse_bool_env_supports_expected_literals():
    assert _parse_bool_env("true") is True
    assert _parse_bool_env("YES") is True
    assert _parse_bool_env("0") is False
    assert _parse_bool_env("off") is False
    assert _parse_bool_env("unknown", default=True) is True
