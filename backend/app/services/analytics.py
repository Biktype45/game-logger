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

def avg_metascore_by_platform(df: pd.DataFrame) -> dict[str, float]:
    """Average metascore per platform."""
    if "metascore" not in df.columns or "platform" not in df.columns:
        return {}
    tmp = df.dropna(subset=["metascore", "platform"])
    if tmp.empty:
        return {}
    avg = tmp.groupby(tmp["platform"].astype(str).str.title())["metascore"].mean().round(1)
    return avg.to_dict()


def must_play_pct_by_platform(df: pd.DataFrame, threshold: int = 90) -> dict[str, float]:
    """Percentage of games per platform with metascore ≥ threshold."""
    if "metascore" not in df.columns or "platform" not in df.columns:
        return {}
    tmp = df.dropna(subset=["metascore", "platform"])
    if tmp.empty:
        return {}
    tmp["is_must_play"] = tmp["metascore"].astype(int) >= threshold
    pct = tmp.groupby(tmp["platform"].astype(str).str.title())["is_must_play"].mean() * 100
    return pct.round(1).to_dict()


def metascore_histogram(df: pd.DataFrame) -> dict[str, int]:
    """Distribution of metascores into bins (50–100)."""
    if "metascore" not in df.columns:
        return {}
    scores = pd.to_numeric(df["metascore"], errors="coerce").dropna().astype(int)
    bins = [(50,59), (60,69), (70,79), (80,89), (90,100)]
    result = {}
    for lo, hi in bins:
        result[f"{lo}-{hi}"] = int(((scores >= lo) & (scores <= hi)).sum())
    return result


def top_devs_by_metascore(df: pd.DataFrame, min_games: int = 2, top_n: int = 5) -> list[dict]:
    """Top developers ranked by average metascore."""
    if "metascore" not in df.columns or "developer" not in df.columns:
        return []
    tmp = df.dropna(subset=["metascore", "developer"])
    if tmp.empty:
        return []
    grp = tmp.groupby(tmp["developer"].astype(str).str.title())["metascore"].agg(["mean", "count"])
    grp = grp[grp["count"] >= min_games].sort_values(by="mean", ascending=False).head(top_n)
    return [
        {"developer": dev, "avg_metascore": round(row["mean"],1), "count": int(row["count"])}
        for dev, row in grp.iterrows()
    ]