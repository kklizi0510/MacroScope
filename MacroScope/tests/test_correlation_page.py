from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    return pd.DataFrame({"date": pd.date_range("2020-01-01", periods=6, freq="YS"), "value": np.arange(6, dtype=float) ** 2})


def test_cross_country_without_fred_key():
    with patch("macroscope.ui.cached_world_bank", return_value=fixture()) as wb, patch("macroscope.ui.key", return_value=""), patch("macroscope.ui.cached_fred") as fred:
        app = AppTest.from_file(ROOT / "app.py").run()
        app.switch_page("pages/2_Correlation.py").run()
        app.selectbox(key="corr_x_source").select("WB").run()
        app.selectbox(key="corr_y_source").select("WB").run()
        app.selectbox(key="corr_y_country").select("日本").run()
        wb.reset_mock()
        app.button(key="corr_run").click().run()
        assert not app.exception
        assert len(app.get("plotly_chart")) == 1
        assert wb.call_count == 2
        assert wb.call_args_list[0].args[0] == "CHN"
        assert wb.call_args_list[1].args[0] == "JPN"
        fred.assert_not_called()


def test_reject_same_selection_before_fetch():
    with patch("macroscope.ui.cached_world_bank", return_value=fixture()), patch("macroscope.ui.cached_fred") as fred:
        app = AppTest.from_file(ROOT / "app.py").run()
        app.switch_page("pages/2_Correlation.py").run()
        app.selectbox(key="corr_y_indicator").select("CPI 同比").run()
        app.button(key="corr_run").click().run()
        assert not app.exception
        assert any("请选择两条不同" in item.value for item in app.warning)
        fred.assert_not_called()


def test_missing_fred_key_before_fetch():
    with patch("macroscope.ui.cached_world_bank", return_value=fixture()), patch("macroscope.ui.key", return_value=""), patch("macroscope.ui.cached_fred") as fred:
        app = AppTest.from_file(ROOT / "app.py").run()
        app.switch_page("pages/2_Correlation.py").run()
        app.button(key="corr_run").click().run()
        assert not app.exception
        assert any("FRED_API_KEY" in item.value for item in app.warning)
        fred.assert_not_called()
