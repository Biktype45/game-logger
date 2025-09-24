from fastapi import APIRouter, HTTPException
from ..services import excel
from ..models import StatsResponse

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats", response_model=StatsResponse)
def stats():
    try:
        df = excel.read_excel()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    platform_counts, year_counts = excel.compute_stats(df)
    return {"platform_counts": platform_counts, "year_counts": year_counts}
