"""Select a trailing window using observation dates, never the current calendar year."""
import pandas as pd


def latest_five_years(frame):
    valid = frame.loc[frame.value.notna(), "date"]
    if valid.empty:
        return frame.copy()
    latest = pd.Timestamp(valid.max())
    annual = "frequency" in frame and frame.frequency.eq("年度").all()
    # Five annual observations (e.g. 2021–2025), or a rolling five-year interval.
    start = (pd.Timestamp(latest.year - 4, 1, 1) if annual
             else latest - pd.DateOffset(years=5) + pd.Timedelta(days=1))
    return frame.loc[frame.date.between(start, latest)].copy()
