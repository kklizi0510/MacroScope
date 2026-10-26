"""Statistics panels share the same observations and time window as the main charts."""
import plotly.express as px
import streamlit as st
from macroscope.analysis import describe, align_pair, coefficients
from macroscope.i18n import t
from macroscope.periods import latest_five_years


def describe_panel(frame, unit, filename):
    with st.expander(t("描述统计")):
        st.caption(t("按当前图表区间、各序列原始频率分别计算。缺失值不当作零；标准差为样本标准差（ddof=1），不足2条时留空。"))
        st.caption(t("单位：") + t(unit))
        result = describe(frame)
        result["series"] = result.series.map(t)
        names = {"series": t("序列"), "count": t("有效样本数"), "missing": t("缺失观测数"),
                 "mean": t("均值"), "median": t("中位数"), "std": t("样本标准差"),
                 "min": t("最小值"), "q25": t("25%分位数"), "q75": t("75%分位数"), "max": t("最大值"),
                 "start": t("首个有效观测"), "end": t("末个有效观测")}
        result = result.rename(columns=names)
        st.dataframe(result, hide_index=True, use_container_width=True)
        st.caption(t("缺失观测数只统计数据源返回的空值，不包含未返回的交易日或观测期。历史描述统计不是未来预测。"))
        st.download_button(t("下载描述统计 CSV"), result.to_csv(index=False).encode("utf-8-sig"),
                           "stats_" + filename, "text/csv", key="stats_" + filename)


def render_correlation(left, right, mode, panel_key):
    modes = {"changes": t("相邻期差值（默认）"), "levels": t("原始水平值")}
    paired, frequency = align_pair(left["frame"], right["frame"], left["frequency"], right["frequency"], mode == "changes")
    if st.session_state.get("period_mode", "latest5") == "latest5" and not paired.empty:
        paired = latest_five_years(paired.assign(value=paired.x, frequency=frequency)).drop(columns=["value", "frequency"])
    st.caption(t("对齐频率：") + t(frequency))
    st.caption(t("按较低频率的日历期对齐；有多条观测时取有效值算术平均。先计算相邻期差值，再仅保留双方有效的共同观测；不插值、不前向填充。周度按周六结束。"))
    st.caption(t("聚合值表示期内观测的平均，不代表季度GDP增速或复合通胀率。边界时期及缺测时期可能不完整；下载配对数据可查看每期有效观测数。差值不是百分比变化。"))
    if mode == "levels":
        st.warning(t("共同趋势可能产生虚假相关，尤其是GDP总量等水平序列。建议同时查看差值结果。"))
    st.info(t("相关性不代表因果或预测能力。本功能只提供描述性系数，不提供显著性检验；序列自相关、趋势和样本区间都会影响结果。"))
    n = len(paired)
    st.metric(t("共同有效样本数"), n)
    if n:
        st.caption(t("共同区间：{start} — {end}", start=paired.date.min().strftime("%Y-%m-%d"), end=paired.date.max().strftime("%Y-%m-%d")))
    result = coefficients(paired)
    if result is None:
        st.warning(t("至少需要3组配对观测，且双方都不能为常数；当前无法计算相关系数。"))
        return
    if n < 12:
        st.warning(t("共同样本少于12组，结果对个别观测非常敏感；不要据此作强推断。"))
    a, b = st.columns(2)
    a.metric("Pearson r", f"{result['pearson']:.3f}")
    b.metric("Spearman ρ", f"{result['spearman']:.3f}")
    st.caption(t("Pearson 描述线性关系，Spearman 描述秩次的单调关系。系数范围为−1到1，接近0不等于不存在任何关系。"))
    def axis_unit(item):
        return t("百分点") if mode == "changes" and "%" in item["unit"] else t(item["unit"])
    x_label = " · ".join(t(part) for part in left["title"]) + " (" + axis_unit(left) + ")"
    y_label = " · ".join(t(part) for part in right["title"]) + " (" + axis_unit(right) + ")"
    fig = px.scatter(paired, x="x", y="y", hover_data=["date", "x_count", "y_count"],
                     labels={"x": x_label, "y": y_label, "date": t("观测期"),
                             "x_count": t("X期内有效观测数"), "y_count": t("Y期内有效观测数")})
    st.plotly_chart(fig, use_container_width=True)
    download = paired.rename(columns={"date": t("观测期"), "x": "X", "y": "Y",
                                       "x_count": t("X期内有效观测数"), "y_count": t("Y期内有效观测数")})
    # Include definitions in the export so the numerical columns are interpretable.
    download[t("横轴序列 X")] = x_label
    download[t("纵轴序列 Y")] = y_label
    download["X " + t("来源")] = left.get("source", "")
    download["Y " + t("来源")] = right.get("source", "")
    download[t("分析方式")] = modes[mode]
    download[t("对齐频率：")] = t(frequency)
    st.dataframe(download, hide_index=True, use_container_width=True)
    st.download_button(t("下载配对数据 CSV"), download.to_csv(index=False).encode("utf-8-sig"),
                       "correlation_" + panel_key + ".csv", "text/csv", key=panel_key + "_download")
