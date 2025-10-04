from fastapi import APIRouter, HTTPException, Query
from ..services import excel
from ..models import GameRow, VersionResponse
from ..services.enricher import enrich_one
from ..services.excel_writer import write_metascores_to_excel
from ..config import settings

router = APIRouter(prefix="/api", tags=["games"])

@router.get("/health")
def health():
    return {"ok": True}

@router.get("/games", response_model=list[GameRow])
async def get_games(enrich: bool = Query(False)):
    try:
        df = excel.read_excel()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    rows = excel.as_game_rows(df)

    if not enrich:
        return rows  # fast path

    # Enrich missing metascores (title-only)
    for r in rows:
        if r.metascore is None:
            data = await enrich_one(r.title)
            if data:
                r.metascore = data.get("metascore")
                r.metacritic_url = data.get("metacritic_url")
                r.metacritic_count = data.get("metacritic_count")

    # ✅ write metascores back into Excel so /api/stats can read them
    await write_metascores_to_excel(settings.EXCEL_PATH, settings.PREFERRED_SHEET)

    return rows

@router.get("/version", response_model=VersionResponse)
def get_version():
    return {"version": excel.file_version()}
