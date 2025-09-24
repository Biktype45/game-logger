from fastapi import APIRouter, HTTPException
from ..services import excel
from ..models import GameRow, VersionResponse

router = APIRouter(prefix="/api", tags=["games"])

@router.get("/health")
def health():
    return {"ok": True}

@router.get("/games", response_model=list[GameRow])
def get_games():
    try:
        df = excel.read_excel()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return excel.as_game_rows(df)

@router.get("/version", response_model=VersionResponse)
def get_version():
    return {"version": excel.file_version()}
