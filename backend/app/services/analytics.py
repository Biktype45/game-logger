import pandas as pd
from collections import Counter

def platform_counts(df: pd.DataFrame) -> dict[str, int]:
    vals = (df["platform"].dropna().astype(str).str.strip().str.title()
            if "platform" in df.columns else pd.Series(dtype=str))
    return dict(Counter(vals))

def year_counts(df: pd.DataFrame) -> dict[str, int]:
    if "completed_on" not in df.columns:
        return {}
    years = pd.to_datetime(df["completed_on"], errors="coerce").dt.year.dropna().astype(int)
    c = Counter(years)
    # keys as strings for JSON
    return {str(k): int(v) for k, v in sorted(c.items())}


def category_counts(df: pd.DataFrame) -> dict[str, int]:
    if "rating" not in df.columns:  # we mapped CATEGORY → rating
        return {}
    vals = df["rating"].dropna().astype(str).str.strip().str.title()
    return dict(Counter(vals))

def monthly_completions(df: pd.DataFrame) -> dict[str, int]:
    if "completed_on" not in df.columns:
        return {}
    dts = pd.to_datetime(df["completed_on"], errors="coerce").dropna()
    months = dts.dt.to_period("M").astype(str)  # YYYY-MM
    return dict(Counter(months))

def avg_hours_by_platform(df: pd.DataFrame) -> dict[str, float]:
    if "hours" not in df.columns or "platform" not in df.columns:
        return {}
    tmp = df.dropna(subset=["hours", "platform"])
    if tmp.empty:
        return {}
    return tmp.groupby(tmp["platform"].astype(str).str.title())["hours"].mean().round(1).to_dict()
