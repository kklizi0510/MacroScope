"""Offline fixtures are synthetic test inputs, never app data."""
from unittest.mock import patch
import pandas as pd
import pytest
from macroscope.catalog import FRED
from macroscope.data import DataError, fred, get_json, parse_world_bank, transform_fred, world_bank


def test_world_bank_null_and_order():
    frame = parse_world_bank([{}, [
        {"date": "2024", "value": None}, {"date": "2023", "value": 12},
    ]])
    assert frame.date.dt.year.tolist() == [2023, 2024]
    assert frame.value.isna().sum() == 1
    assert parse_world_bank([{}, None]).empty


def test_invalid_payload():
    with pytest.raises(DataError):
        parse_world_bank({"message": "error"})


def test_missing_month_does_not_create_false_growth():
    frame = pd.DataFrame({"date": ["2020-01-01", "2020-03-01"], "value": [100, 110]})
    assert transform_fred(frame, "CPI 环比").value.isna().all()
    assert transform_fred(frame, "非农就业月度变动").value.isna().all()


def test_growth_and_difference():
    dates = pd.date_range("2020-01-01", periods=13, freq="MS")
    frame = pd.DataFrame({"date": dates, "value": range(100, 113)})
    assert transform_fred(frame, "CPI 同比").value.iloc[-1] == pytest.approx(12)
    assert transform_fred(frame, "非农就业月度变动").value.iloc[-1] == 1


def test_fred_warmup_then_filter():
    payload = {"observations": [{"date": "2023-12-01", "value": "100"}, {"date": "2024-01-01", "value": "110"}]}
    with patch("macroscope.data.get_json", return_value=payload) as request:
        frame = fred(FRED["非农就业月度变动"], "非农就业月度变动", "2024-01-01", "2024-01-31", "test-only")
    assert frame.value.tolist() == [10]
    assert request.call_args.args[1]["observation_start"] < "2023-12-01"


def test_trade_balance_aligns_dates_without_filling():
    payloads = [[{}, [{"date": "2023", "value": 10}, {"date": "2024", "value": 20}]],
                [{}, [{"date": "2023", "value": 7}]]]
    with patch("macroscope.data.get_json", side_effect=payloads):
        frame = world_bank("CHN", "balance", 2023, 2024)
    assert frame.value.iloc[0] == 3
    assert pd.isna(frame.value.iloc[1])


def test_http_error_does_not_leak_key():
    import requests
    with patch("macroscope.data.requests.get", side_effect=requests.RequestException("secret-key")):
        with pytest.raises(DataError) as exc:
            get_json("https://example.invalid", {"api_key": "secret-key"})
    assert "secret-key" not in str(exc.value)


def test_no_key():
    with pytest.raises(DataError, match="FRED_API_KEY"):
        fred(FRED["初请失业金人数"], "初请失业金人数", "2024-01-01", "2024-02-01", "")
