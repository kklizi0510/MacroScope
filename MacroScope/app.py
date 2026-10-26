import streamlit as st
from macroscope.catalog import COUNTRIES, WORLD_BANK
from macroscope.data import DataError
from macroscope.ui import cached_world_bank, dates, show, explain
import pandas as pd
from macroscope.i18n import t, sidebar, coverage

st.set_page_config(page_title="MacroScope", page_icon="🌏", layout="wide")
sidebar()
st.title("🌏 MacroScope")
st.write(t("中美日宏观经济数据看板"))
st.info(t("追踪中美日宏观经济指标并比较长期趋势。年度数据通常滞后；数据接入情况见页面底部，美国高频数据请查看美国经济专区。"))
start, end = dates()
countries = st.multiselect(t("国家"), list(COUNTRIES), default=list(COUNTRIES), format_func=t, key="countries")
labels = st.multiselect(t("指标（不同单位分别绘图）"), list(WORLD_BANK), default=["GDP 实际增速"], format_func=t, key="wb_indicators")
st.caption(t("年度序列按观测年份筛选，日期统一标为当年 1 月 1 日。跨国使用同一世界银行指标；不把年度数据扩展成月度数据。"))
for label in labels:
    spec = WORLD_BANK[label]
    st.subheader(t(label))
    explain(label, "WB")
    st.caption(f"{t(spec.frequency)} · {t(spec.unit)} · {t(spec.note)}")
    frames = []
    for country in countries:
        code = COUNTRIES[country]
        source = ("https://data.worldbank.org/indicator/" + spec.code if spec.code != "balance"
                  else "https://data.worldbank.org/indicator/NE.EXP.GNFS.CD ; https://data.worldbank.org/indicator/NE.IMP.GNFS.CD")
        try:
            with st.spinner(t("读取{country}数据…", country=t(country))):
                data = cached_world_bank(code, spec.code, start.year, end.year)
            if data.empty or data.value.notna().sum() == 0:
                st.warning(t(country) + ": " + t("所选年份没有可用数据。"))
            frames.append(data.assign(series=country, unit=spec.unit, frequency=spec.frequency,
                                      indicator=label, source=source))
        except DataError as exc:
            st.warning(t(country) + ": " + t(str(exc)))
    st.markdown(t("来源：[世界银行 WDI](https://data.worldbank.org/)；贸易差额由出口减进口计算。"))
    if frames:
        show(pd.concat(frames, ignore_index=True), spec.unit, f"WB_{spec.code}.csv")

with st.expander(t("MVP 数据接入清单与边界"), expanded=True):
    st.markdown(coverage())

if st.sidebar.button(t("清除缓存并重新读取")):
    st.cache_data.clear()
    st.rerun()
