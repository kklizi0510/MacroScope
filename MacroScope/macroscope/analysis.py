"""Pure statistical functions; missing periods are never forward-filled."""
import numpy as np
import pandas as pd

FREQUENCIES = {"日度": "D", "周度": "W-SAT", "月度": "M", "季度": "Q", "年度": "Y"}


def describe(frame):
    rows = []
    for name, group in frame.groupby("series", sort=False):
        values = pd.to_numeric(group.value, errors="coerce").replace([np.inf, -np.inf], np.nan)
        valid = values.dropna()
        dates = group.loc[values.notna(), "date"]
        rows.append({"series": name, "count": len(valid), "missing": int(values.isna().sum()),
                     "mean": valid.mean(), "median": valid.median(), "std": valid.std(ddof=1),
                     "min": valid.min(), "q25": valid.quantile(.25), "q75": valid.quantile(.75),
                     "max": valid.max(), "start": dates.min(), "end": dates.max()})
    return pd.DataFrame(rows)


def common_frequency(x_frequency, y_frequency):
    order = list(FREQUENCIES)
    return max((x_frequency, y_frequency), key=order.index)


def align_pair(x, y, x_frequency, y_frequency, changes=True):
    """Coarsen to period means; difference on a full calendar BEFORE dropping gaps."""
    frequency = common_frequency(x_frequency, y_frequency)
    rule = FREQUENCIES[frequency]

    def aggregate(frame):
        values = pd.to_numeric(frame.value, errors="coerce").replace([np.inf, -np.inf], np.nan)
        periods = pd.to_datetime(frame.date).dt.to_period(rule)
        grouped = values.groupby(periods)
        return grouped.mean(), grouped.count()

    xs, xc = aggregate(x)
    ys, yc = aggregate(y)
    if xs.empty or ys.empty:
        return pd.DataFrame(columns=["date", "x", "y", "x_count", "y_count"]), frequency
    calendar = pd.period_range(min(xs.index.min(), ys.index.min()), max(xs.index.max(), ys.index.max()), freq=rule)
    xs, ys = xs.reindex(calendar), ys.reindex(calendar)
    if changes:
        xs, ys = xs.diff(), ys.diff()
    paired = pd.DataFrame({"date": calendar.to_timestamp(), "x": xs.to_numpy(), "y": ys.to_numpy(),
                           "x_count": xc.reindex(calendar, fill_value=0).to_numpy(),
                           "y_count": yc.reindex(calendar, fill_value=0).to_numpy()})
    return paired.dropna(subset=["x", "y"]).reset_index(drop=True), frequency


def coefficients(paired):
    if len(paired) < 3 or paired.x.nunique() < 2 or paired.y.nunique() < 2:
        return None
    return {"pearson": float(paired.x.corr(paired.y)),
            "spearman": float(paired.x.rank(method="average").corr(paired.y.rank(method="average")))}
