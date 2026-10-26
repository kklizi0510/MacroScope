"""Shared rendering keeps page scripts small."""
import os
from datetime import date
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from macroscope.data import world_bank, fred
from macroscope.i18n import t, lang, sidebar, column_name

load_dotenv()
cached_world_bank = st.cache_data(ttl=86400, max_entries=128, show_spinner=False)(world_bank)
cached_fred = st.cache_data(ttl=3600, max_entries=128, show_spinner=False)(fred)


def key():
    value = os.getenv("FRED_API_KEY", "").strip()
    if value:
        return value
    try:
        return str(st.secrets.get("FRED_API_KEY", "")).strip()
    except st.errors.StreamlitSecretNotFoundError:
        return ""


def dates():
    options = {"latest5": t("最近5年（截至最新数据）"), "custom": t("自定义日期")}
    mode = st.sidebar.radio(t("时间范围"), list(options),
                            format_func=options.__getitem__,
                            key="period_mode")
    if mode == "latest5":
        st.sidebar.caption(t("每张图以所选序列的最新有效观测为终点，展示最近5年；年度指标展示最近5个观测年份。"))
        # Read available history first; show() filters relative to the actual latest observation.
        return date(1960, 1, 1), date.today()
    start = st.sidebar.date_input(t("开始日期"), (pd.Timestamp(date.today()) - pd.DateOffset(years=5)).date(), key="custom_start")
    end = st.sidebar.date_input(t("结束日期"), date.today(), key="custom_end")
    if start > end:
        st.error(t("开始日期不能晚于结束日期。"))
        st.stop()
    return start, end


def show(frame, unit, filename):
    if st.session_state.get("period_mode", "latest5") == "latest5":
        from macroscope.periods import latest_five_years
        frame = latest_five_years(frame)
    if frame.empty or frame.value.notna().sum() == 0:
        st.warning(t("所选区间没有可用观测值。未填充或模拟数据。"))
        return
    missing = int(frame.value.isna().sum())
    if missing:
        st.warning(t("有 {missing} 条观测缺失；图中保留缺口，未前向填充。", missing=missing))
    valid = frame.loc[frame.value.notna(), "date"]
    st.caption(t("有效观测范围：{start} — {end}。观测日期不是发布日期；可能存在发布滞后和修订。", start=valid.min().strftime("%Y-%m-%d"), end=valid.max().strftime("%Y-%m-%d")))
    display = frame.copy()
    for field in ("series", "unit", "frequency", "indicator"):
        if field in display:
            display[field] = display[field].map(t)
    fig = px.line(display, x="date", y="value", color="series", markers=True,
                  labels={"date": t("观测期"), "value": t(unit), "series": t("序列")})
    fig.update_traces(connectgaps=False)
    st.plotly_chart(fig, use_container_width=True)
    display = display.rename(columns=column_name)
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button(t("下载当前数据 CSV"), display.to_csv(index=False).encode("utf-8-sig"),
                       filename, "text/csv", key=filename)
    from macroscope.analysis_ui import describe_panel
    describe_panel(frame, unit, filename)


def explain(label, country_group):
    from macroscope.explanations import EXPECTATIONS
    from macroscope.help_translations import localized_help
    help_text = localized_help(label, country_group, lang())
    st.markdown(f"**{t('是什么')}：** " + help_text.meaning)
    with st.expander(t("如何阅读 · 对投资市场的可能影响")):
        st.markdown(f"**{t('如何阅读')}：** " + help_text.reading)
        st.markdown(f"**{t('可能影响市场的路径（机制解读）')}：** " + help_text.market)
        st.markdown(f"**{t('容易误解的地方')}：** " + help_text.caution)
        st.caption(t(EXPECTATIONS))
        links = []
        for index, (title, url) in enumerate(help_text.references, 1):
            title = title if lang() == "zh" else (f"Reference {index}" if lang() == "en" else f"参考資料 {index}")
            links.append(f"[{title}]({url})")
        st.markdown(t("参考资料：") + " · ".join(links))


def us_view():
    from macroscope.catalog import FRED
    from macroscope.data import DataError
    sidebar()
    st.title(t("美国经济专区"))
    st.write(t("月度、周度、季度和日度序列分别展示，保留各自频率与定义。"))
    start, end = dates()
    selected = st.multiselect(t("选择美国指标"), list(FRED), default=["非农就业月度变动"], format_func=t, key="us_indicators")
    api_key = key()
    if not api_key:
        st.info(t("配置 FRED_API_KEY 后可读取美国专区数据；无密钥时仍可使用首页世界银行数据。"))
    for label in selected:
        spec = FRED[label]
        st.subheader(t(label))
        explain(label, "US")
        st.caption(f"{t(spec.frequency)} · {t(spec.unit)} · {t(spec.note)}")
        st.markdown(t("来源：") + f"[FRED / {spec.code}](https://fred.stlouisfed.org/series/{spec.code})")
        if not api_key:
            continue
        try:
            with st.spinner(t("读取官方数据…")):
                frame = cached_fred(spec, label, start, end, api_key)
            frame = frame.assign(series=label, unit=spec.unit, frequency=spec.frequency,
                                 source=f"https://fred.stlouisfed.org/series/{spec.code}")
            show(frame, spec.unit, f"US_{spec.code}_{list(FRED).index(label)}.csv")
        except DataError as exc:
            st.warning(t(str(exc)))

