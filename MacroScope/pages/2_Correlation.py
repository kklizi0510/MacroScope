import streamlit as st
from macroscope.i18n import t, sidebar
from macroscope.ui import dates, key, cached_fred, cached_world_bank
from macroscope.catalog import COUNTRIES, WORLD_BANK, FRED
from macroscope.data import DataError
from macroscope.analysis_ui import render_correlation

st.set_page_config(page_title=t("相关性分析") + " · MacroScope", layout="wide")
sidebar()
st.title(t("相关性分析"))
st.write(t("独立选择两组数据，无需在首页或美国专区预先勾选；支持跨国家、跨数据源比较。"))
start, end = dates()


def selection(side, default_label):
    st.subheader(t("横轴序列 X" if side == "x" else "纵轴序列 Y"))
    sources = {"FRED": t("FRED 美国指标"), "WB": t("世界银行年度指标")}
    source = st.selectbox(t("数据来源"), list(sources), format_func=sources.__getitem__, key=f"corr_{side}_source")
    if source == "WB":
        names = {name: t(name) for name in COUNTRIES}
        country = st.selectbox(t("国家"), list(COUNTRIES), format_func=names.__getitem__, key=f"corr_{side}_country")
        catalog = WORLD_BANK
        initial = "GDP 实际增速"
    else:
        country, catalog, initial = "美国", FRED, default_label
        st.caption(t("国家") + ": " + t(country))
    labels = {label: t(label) for label in catalog}
    label = st.selectbox(t("指标"), list(catalog), index=list(catalog).index(initial),
                         format_func=labels.__getitem__, key=f"corr_{side}_indicator")
    spec = catalog[label]
    st.caption(f"{t(spec.frequency)} · {t(spec.unit)} · {t(spec.note)}")
    if source == "FRED":
        url = f"https://fred.stlouisfed.org/series/{spec.code}"
        st.markdown(t("来源：") + f"[FRED / {spec.code}]({url})")
    else:
        codes = [spec.code] if spec.code != "balance" else ["NE.EXP.GNFS.CD", "NE.IMP.GNFS.CD"]
        url = " ; ".join("https://data.worldbank.org/indicator/" + code for code in codes)
        st.markdown(t("来源：") + " · ".join(f"[WDI / {code}](https://data.worldbank.org/indicator/{code})" for code in codes))
    return {"source_id": source, "country": country, "label": label, "spec": spec,
            "title": (country, label, source), "unit": spec.unit, "frequency": spec.frequency, "source": url}


a, b = st.columns(2)
with a:
    left = selection("x", "CPI 同比")
with b:
    right = selection("y", "联邦基金有效利率")
modes = {"changes": t("相邻期差值（默认）"), "levels": t("原始水平值")}
mode = st.radio(t("分析方式"), list(modes), format_func=modes.__getitem__, key="corr_mode")
if st.button(t("开始分析"), type="primary", key="corr_run"):
    identity = lambda item: (item["source_id"], item["country"], item["label"])
    if identity(left) == identity(right):
        st.warning(t("请选择两条不同的序列。"))
        st.stop()
    api_key = key()
    if any(item["source_id"] == "FRED" for item in (left, right)) and not api_key:
        st.warning(t("尚未配置 FRED_API_KEY。请按 README 设置自己的密钥。"))
        st.stop()
    try:
        with st.spinner(t("读取官方数据…")):
            for item in (left, right):
                spec = item["spec"]
                if item["source_id"] == "FRED":
                    frame = cached_fred(spec, item["label"], start, end, api_key)
                else:
                    frame = cached_world_bank(COUNTRIES[item["country"]], spec.code, start.year, end.year)
                item["frame"] = frame
                if frame.empty or not frame.value.notna().any():
                    st.warning(" · ".join(t(part) for part in item["title"]) + ": " + t("所选区间没有可用观测值。未填充或模拟数据。"))
                    st.stop()
        render_correlation(left, right, mode, "independent")
    except DataError as exc:
        st.warning(t(str(exc)))
else:
    st.info(t("选择两组数据和分析方式后，点击“开始分析”。修改选择后请重新分析。"))
