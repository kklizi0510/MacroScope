import streamlit as st
from macroscope.ui import us_view
from macroscope.i18n import t

st.set_page_config(page_title=t("美国经济专区") + " · MacroScope", layout="wide")
us_view()
