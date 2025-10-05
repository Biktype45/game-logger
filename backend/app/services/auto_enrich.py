import asyncio
import pandas as pd
from . import excel, enricher, excel_writer
from ..config import settings

async def auto_enrich_missing():
    """Scan Excel for missing metascores and fill them automatically."""
    print("[AutoEnrich] Checking for missing metascores...")
    df = excel.read_excel()

    # Identify missing metascores
    if "metascore" not in df.columns:
        print("[AutoEnrich] No 'metascore' column found.")
        return

    missing = df[df["metascore"].isna()]
    if missing.empty:
        print("[AutoEnrich] All games already have metascores.")
        return

    total = len(missing)
    updated = 0

    for _, row in missing.iterrows():
        title = str(row["title"]).strip()
        if not title:
            continue
        data = await enricher.enrich_one(title)
        if data and data.get("metascore") is not None:
            df.loc[df["title"] == row["title"], "metascore"] = data["metascore"]
            updated += 1
            print(f"[AutoEnrich] ✓ {title} → {data['metascore']}")
        await asyncio.sleep(0.3)  # polite throttle

    if updated:
        await excel_writer.write_metascores_to_excel(settings.EXCEL_PATH, settings.PREFERRED_SHEET)
        print(f"[AutoEnrich] Updated {updated}/{total} missing metascores and saved to Excel.")
    else:
        print("[AutoEnrich] No new metascores found.")
