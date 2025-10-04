from __future__ import annotations
import os, time
import pandas as pd
from typing import List, Tuple
from . import analytics
from ..config import settings
from ..models import GameRow

def _snake(s: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in s).strip("_")

# Map your actual headers → normalized keys the app expects.
COLUMN_CANDIDATES = {
    # include your column: NAME OF THE GAME → name_of_the_game
    "title": ["name_of_the_game", "title", "name", "game", "game_title"],
    "platform": ["platform", "console", "system"],
    "completed_on": ["completed_on", "completed", "date_completed", "finished", "beaten_on"],
    "hours": ["hours", "playtime", "time_spent"],
    # include your column: CATEGORY → category
    "rating": ["category", "rating", "tier", "my_rating"],
    "developer": ["developer", "dev", "studio"],
    "metascore": ["metascore", "meta_score", "meta"]
}


def read_excel() -> pd.DataFrame:
    path = settings.EXCEL_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Excel not found at {path}")
    # Try preferred sheet, else first
    try:
        df = pd.read_excel(path, sheet_name=settings.PREFERRED_SHEET, engine="openpyxl")
    except Exception:
        df = pd.read_excel(path, engine="openpyxl")  # defaults to first sheet

    # Normalize column names
    df.columns = [_snake(c) for c in df.columns]

    # Build a mapping from our keys → actual df columns, if present
    resolved = {}
    for key, candidates in COLUMN_CANDIDATES.items():
        for cand in candidates:
            sc = _snake(cand)
            if sc in df.columns:
                resolved[key] = sc
                break

    # Ensure required fields exist
    if "title" not in resolved:
        raise ValueError("Could not find a column for 'title' (candidates: name, game, title ...)")

    # Coerce types
    if "completed_on" in resolved:
        df[resolved["completed_on"]] = pd.to_datetime(df[resolved["completed_on"]], errors="coerce").dt.date
    if "hours" in resolved:
        df[resolved["hours"]] = pd.to_numeric(df[resolved["hours"]], errors="coerce")
    if "metascore" in resolved:
        df[resolved["metascore"]] = pd.to_numeric(
            df[resolved["metascore"]], errors="coerce"
        )

    # Project to a consistent view
    out = pd.DataFrame({
        "title": df[resolved["title"]],
        "platform": df.get(resolved.get("platform"), pd.Series([None]*len(df))),
        "completed_on": df.get(resolved.get("completed_on"), pd.Series([None]*len(df))),
        "hours": df.get(resolved.get("hours"), pd.Series([None]*len(df))),
        "rating": df.get(resolved.get("rating"), pd.Series([None]*len(df))),
        "developer": df.get(resolved.get("developer"), pd.Series([None]*len(df))),
        "metascore": df.get(resolved.get("metascore"), pd.Series([None]*len(df)))
    })
    out = out.reset_index(drop=True)
    return out

def as_game_rows(df: pd.DataFrame) -> List[GameRow]:
    rows: List[GameRow] = []
    for i, r in df.iterrows():
        rows.append(GameRow(
            idx=i,
            title=str(r["title"]).strip() if pd.notna(r["title"]) else "Unknown",
            platform=str(r["platform"]).strip() if pd.notna(r["platform"]) else None,
            completed_on=r["completed_on"] if pd.notna(r["completed_on"]) else None,
            hours=float(r["hours"]) if pd.notna(r["hours"]) else None,
            rating=str(r["rating"]).strip() if pd.notna(r["rating"]) else None,
            developer=str(r["developer"]).strip() if pd.notna(r["developer"]) else None,
            metascore=int(r["metascore"]) if ("metascore" in df.columns and pd.notna(r["metascore"])) else None
        ))
    return rows

def file_version() -> str:
    """A cheap hash so the frontend knows when to refresh (mtime+size)."""
    p = settings.EXCEL_PATH
    try:
        stat = os.stat(p)
        return f"{int(stat.st_mtime)}-{stat.st_size}"
    except FileNotFoundError:
        return f"missing-{int(time.time())}"

def compute_stats(df: pd.DataFrame) -> Tuple[dict, dict]:
    return analytics.platform_counts(df), analytics.year_counts(df)
