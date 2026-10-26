from pathlib import Path
from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from macroscope.periods import latest_five_years


def test_annual_latest_five_observation_years():
    frame = pd.DataFrame({"date": pd.date_range("2015-01-01", "2026-01-01", freq="YS"),
                          "value": [1.] * 11 + [None], "frequency": "年度"})
    result = latest_five_years(frame)
    assert result.date.dt.year.tolist() == [2021, 2022, 2023, 2024, 2025]


def test_monthly_latest_sixty_months():
    frame = pd.DataFrame({"date": pd.date_range("2015-01-01", "2026-09-01", freq="MS")})
    frame["value"] = 1.
    frame["frequency"] = "月度"
    result = latest_five_years(frame)
    assert len(result) == 60
    assert result.date.min() == pd.Timestamp("2021-10-01")
    assert result.date.max() == pd.Timestamp("2026-09-01")


def test_empty_and_missing_only():
    frame = pd.DataFrame({"date": pd.to_datetime(["2026-01-01"]), "value": [None]})
    assert latest_five_years(frame).equals(frame)
    assert latest_five_years(frame.iloc[:0]).empty


def test_default_window_and_custom_option():
    fixture = pd.DataFrame({"date": pd.date_range("2015-01-01", "2025-01-01", freq="YS"), "value": 1.})
    root = Path(__file__).resolve().parents[1]
    with patch("macroscope.ui.cached_world_bank", return_value=fixture):
        app = AppTest.from_file(root / "app.py").run()
        assert not app.exception
        assert app.radio(key="period_mode").value == "latest5"
        assert len(app.date_input) == 0
        displayed = app.dataframe[0].value
        assert len(displayed) == 15  # five years for each of three countries
        assert displayed["观测期"].dt.year.min() == 2021
        assert displayed["观测期"].dt.year.max() == 2025
        assert any("中美日宏观经济数据看板" in item.value for item in app.markdown)
        app.radio(key="period_mode").set_value("custom").run()
        assert not app.exception
        assert len(app.date_input) == 2
