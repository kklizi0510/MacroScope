"""HTTP adapters. No Streamlit dependency, so parsing can be tested offline."""
import numpy as np
import pandas as pd
import requests


class DataError(Exception):
    """Safe user-facing message; never include URLs containing API keys."""


def get_json(url, params):
    try:
        response = requests.get(url, params=params, timeout=(10, 30))
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        raise DataError("数据请求失败。请检查网络、服务状态或 FRED 密钥，稍后重试。") from None


def parse_world_bank(payload):
    if not isinstance(payload, list) or len(payload) < 2:
        raise DataError("世界银行返回格式异常。")
    if payload[1] is None:
        return pd.DataFrame(columns=["date", "value"])
    try:
        rows = [{"date": f"{r['date']}-01-01", "value": r["value"]} for r in payload[1]]
        return clean_frame(pd.DataFrame(rows, columns=["date", "value"]))
    except (KeyError, TypeError, ValueError):
        raise DataError("世界银行数据字段异常。") from None


def clean_frame(frame):
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce").replace([np.inf, -np.inf], np.nan)
    return frame.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)


def world_bank(country, indicator, start, end):
    if indicator == "balance":
        exports = world_bank(country, "NE.EXP.GNFS.CD", start, end)
        imports = world_bank(country, "NE.IMP.GNFS.CD", start, end)
        merged = exports.merge(imports, on="date", how="outer", suffixes=("_exp", "_imp"))
        return clean_frame(merged.assign(value=merged.value_exp - merged.value_imp)[["date", "value"]])
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    payload = get_json(url, {"format": "json", "date": f"{start}:{end}", "per_page": 1000})
    return parse_world_bank(payload)


def transform_fred(frame, label):
    frame = clean_frame(frame)
    # Reindex monthly observations: absent months must not become adjacent months.
    if label in ("非农就业月度变动", "CPI 同比", "CPI 环比") and not frame.empty:
        frame = frame.set_index("date").asfreq("MS")
        if label == "非农就业月度变动":
            frame["value"] = frame.value.diff()
        else:
            lag = 12 if label == "CPI 同比" else 1
            frame["value"] = frame.value.pct_change(lag, fill_method=None) * 100
        frame = frame.reset_index()
    return clean_frame(frame)


def fred(spec, label, start, end, key):
    if not key:
        raise DataError("尚未配置 FRED_API_KEY。请按 README 设置自己的密钥。")
    # Fetch a warm-up period before filtering so growth/difference at the start is correct.
    warmup = (pd.Timestamp(start) - pd.DateOffset(months=13)).date().isoformat()
    payload = get_json("https://api.stlouisfed.org/fred/series/observations", {
        "series_id": spec.code, "api_key": key, "file_type": "json",
        "observation_start": warmup, "observation_end": str(end), "limit": 100000,
    })
    try:
        frame = pd.DataFrame(payload["observations"], columns=["date", "value"])
        frame = transform_fred(frame, label)
        return frame.loc[frame.date.between(pd.Timestamp(start), pd.Timestamp(end))].reset_index(drop=True)
    except (KeyError, TypeError, ValueError):
        raise DataError("FRED 返回格式异常，无法读取观测值。") from None

