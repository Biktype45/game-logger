from fastapi import APIRouter, HTTPException
from ..services import excel, analytics
from ..models import StatsResponse

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats", response_model=dict)
def stats():
    try:
        df = excel.read_excel()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "platform_counts": analytics.platform_counts(df),
        "year_counts": analytics.year_counts(df),
        "category_counts": analytics.category_counts(df),
        "monthly_completions": analytics.monthly_completions(df),
        "avg_hours_by_platform": analytics.avg_hours_by_platform(df),
    }
