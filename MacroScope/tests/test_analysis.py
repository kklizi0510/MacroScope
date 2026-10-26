from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from macroscope.analysis import describe, align_pair, coefficients


def test_describe_valid_missing_and_sample_std():
    frame = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=4),
                          "series": ["A"] * 4, "value": [1., 2., 3., np.nan]})
    row = describe(frame).iloc[0]
    assert row["count"] == 3 and row["missing"] == 1
    assert row["mean"] == row["median"] == 2
    assert row["std"] == 1
    assert row["q25"] == 1.5 and row["q75"] == 2.5
    assert row["end"] == pd.Timestamp("2024-01-03")


def test_statistics_separate_series_and_small_samples():
    frame = pd.DataFrame({"date": pd.to_datetime(["2024-01-01"] * 3),
                          "series": ["A", "B", "C"], "value": [1., None, np.inf]})
    rows = describe(frame).set_index("series")
    assert pd.isna(rows.loc["A", "std"])
    assert rows.loc["B", "count"] == rows.loc["C", "count"] == 0


def test_alignment_and_means_not_forward_fill():
    daily = pd.DataFrame({"date": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-03-01"]), "value": [1., 3., 8.]})
    monthly = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=3, freq="MS"), "value": [4., 5., 7.]})
    paired, frequency = align_pair(daily, monthly, "日度", "月度", changes=False)
    assert frequency == "月度"
    assert paired.x.tolist() == [2., 8.]
    assert paired.x_count.tolist() == [2, 1]
    changes, _ = align_pair(daily, monthly, "日度", "月度", changes=True)
    assert changes.empty  # Missing February must not create January-to-March differences.


def test_known_correlations_and_ties():
    paired = pd.DataFrame({"x": [1., 2., 2., 4.], "y": [9., 7., 7., 3.]})
    result = coefficients(paired)
    assert result["pearson"] == pytest.approx(-1)
    assert result["spearman"] == pytest.approx(-1)
    assert coefficients(paired.iloc[:2]) is None
    assert coefficients(paired.assign(y=1)) is None


def test_quarter_period_alignment():
    x = pd.DataFrame({"date": pd.date_range("2024-01-01", periods=6, freq="MS"), "value": [1., 2., 3., 4., 5., 6.]})
    y = pd.DataFrame({"date": pd.to_datetime(["2024-01-01", "2024-04-01"]), "value": [10., 20.]})
    paired, freq = align_pair(x, y, "月度", "季度", changes=False)
    assert freq == "季度"
    assert paired.x.tolist() == [2., 5.]
    assert paired.x_count.tolist() == [3, 3]


@pytest.mark.parametrize("language", ["zh", "en", "ja"])
def test_statistics_and_enabled_correlation_ui(language):
    fixture = pd.DataFrame({"date": pd.date_range("2021-01-01", periods=36, freq="MS"), "value": np.arange(36, dtype=float) ** 2})
    root = Path(__file__).resolve().parents[1]
    with patch("macroscope.ui.cached_world_bank", return_value=fixture), patch("macroscope.ui.cached_fred", return_value=fixture), patch("macroscope.ui.key", return_value="test-only"):
        app = AppTest.from_file(root / "app.py")
        app.session_state["language"] = language
        app.run()
        app.switch_page("pages/1_US_Economy.py").run()
        app.multiselect(key="us_indicators").set_value(["非农就业月度变动", "CPI 同比"]).run()
        assert len(app.dataframe) == 4
        app.switch_page("pages/2_Correlation.py").run()
        app.button(key="corr_run").click().run()
        assert not app.exception
        assert len(app.get("plotly_chart")) == 1
        assert any(metric.label == "Pearson r" and metric.value == "1.000" for metric in app.metric)
        assert len(app.dataframe) == 1  # independent paired observations
        if language == "en":
            import re
            assert not any(re.search(r"[\u4e00-\u9fff]", node.value) for node in [*app.caption, *app.info, *app.warning])
