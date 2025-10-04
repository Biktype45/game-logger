from fastapi import APIRouter, HTTPException
from ..services import excel, analytics

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/stats")
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

        # 🆕 Metacritic analytics
        "avg_metascore_by_platform": analytics.avg_metascore_by_platform(df),
        "must_play_pct_by_platform": analytics.must_play_pct_by_platform(df, threshold=90),
        "metascore_histogram": analytics.metascore_histogram(df),
        "top_devs_by_metascore": analytics.top_devs_by_metascore(df),
    }
