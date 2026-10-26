from unittest.mock import patch
import pandas as pd
from streamlit.testing.v1 import AppTest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_home_offline():
    # Explicit test fixture; never shipped as a dataset or used as fallback.
    fixture = pd.DataFrame({"date": pd.to_datetime(["2023-01-01"]), "value": [1.0]})
    with patch("macroscope.ui.cached_world_bank", return_value=fixture):
        app = AppTest.from_file(ROOT / "app.py").run(timeout=30)
    assert not app.exception
    assert len(app.get("plotly_chart")) == 1


def test_us_no_key():
    fixture = pd.DataFrame({"date": pd.to_datetime(["2023-01-01"]), "value": [1.0]})
    with patch("macroscope.ui.key", return_value=""), patch("macroscope.ui.cached_world_bank", return_value=fixture):
        app = AppTest.from_file(ROOT / "app.py").run(timeout=30)
        app.switch_page("pages/1_US_Economy.py").run(timeout=30)
    assert not app.exception
    assert app.info


def test_home_network_failure():
    from macroscope.data import DataError
    with patch("macroscope.ui.cached_world_bank", side_effect=DataError("离线测试")):
        app = AppTest.from_file(ROOT / "app.py").run(timeout=30)
    assert not app.exception
    assert len(app.warning) == 3
