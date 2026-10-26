from pathlib import Path
from unittest.mock import patch
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from macroscope.catalog import WORLD_BANK, FRED
from macroscope.explanations import WORLD_BANK_HELP, FRED_HELP
from macroscope.help_translations import WB, US, localized_help
from macroscope.i18n import TEXT

ROOT = Path(__file__).resolve().parents[1]


def test_translation_coverage():
    assert set(WB) == set(WORLD_BANK) == set(WORLD_BANK_HELP)
    assert set(US) == set(FRED) == set(FRED_HELP)
    for catalog in (WORLD_BANK, FRED):
        for label, spec in catalog.items():
            assert label in TEXT
            assert spec.note in TEXT
            assert spec.frequency in TEXT
            assert spec.unit == '%' or spec.unit in TEXT
    for group, catalog in (("WB", WORLD_BANK), ("US", FRED)):
        for label in catalog:
            for language in ("en", "ja"):
                help_text = localized_help(label, group, language)
                assert all((help_text.meaning, help_text.reading, help_text.market, help_text.caution))


@pytest.mark.parametrize("language,title", [("en", "US Economy"), ("ja", "米国経済"), ("zh", "美国经济专区")])
def test_language_switch_and_navigation(language, title):
    fixture = pd.DataFrame({"date": pd.to_datetime(["2023-01-01"]), "value": [1.0]})
    with patch("macroscope.ui.cached_world_bank", return_value=fixture), patch("macroscope.ui.key", return_value=""):
        app = AppTest.from_file(ROOT / "app.py").run()
        app.selectbox(key="_language_picker").select(language).run()
        assert not app.exception
        assert app.session_state["language"] == language
        assert len(app.get("plotly_chart")) == 1
        app.switch_page("pages/1_US_Economy.py").run()
        assert not app.exception
        assert app.title[0].value == title
        assert app.session_state["language"] == language
        assert app.expander


@pytest.mark.parametrize("language", ["en", "ja"])
def test_us_all_indicators_localized(language):
    fixture = pd.DataFrame({"date": pd.to_datetime(["2023-01-01"]), "value": [1.0]})
    with patch("macroscope.ui.key", return_value="test-only"), patch("macroscope.ui.cached_fred", return_value=fixture), patch("macroscope.ui.cached_world_bank", return_value=fixture):
        app = AppTest.from_file(ROOT / "app.py")
        app.session_state["language"] = language
        app.run()
        app.switch_page("pages/1_US_Economy.py").run()
        app.multiselect(key="us_indicators").set_value(list(FRED)).run()
        assert not app.exception
        assert len(app.expander) == len(FRED) * 2
        assert len(app.get("plotly_chart")) == len(FRED)
        if language == "en":
            import re
            for node in [*app.markdown, *app.caption, *app.subheader]:
                assert not re.search(r"[\u4e00-\u9fff]", node.value)
