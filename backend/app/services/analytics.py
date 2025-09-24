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
