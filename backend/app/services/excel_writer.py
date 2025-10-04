import pandas as pd
from .meta_cache import get as cache_get

async def write_metascores_to_excel(path: str, sheet_name: str):
    """Read the Excel, inject cached metascores, and overwrite the file."""
    df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")

    # make sure there is a 'metascore' column
    if "metascore" not in df.columns:
        df["metascore"] = None

    # fill from cache (async safe)
    for i, row in df.iterrows():
        title = str(row.get("NAME OF THE GAME") or "").strip().lower()
        if not title:
            continue
        cached = await cache_get(title)
        if cached and cached.get("metascore") is not None:
            df.at[i, "metascore"] = cached["metascore"]

    # overwrite Excel in-place
    with pd.ExcelWriter(path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
