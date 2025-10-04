from fastapi import APIRouter, Query, HTTPException
from ..services import meta_cache
from ..services.metacritic import fetch_best_item, extract_scores
from ..config import settings
import time

router = APIRouter(prefix="/api/meta", tags=["meta"])

@router.get("/test")
async def test_enrich(title: str = Query(...)):
    """Test RAWG enrichment for a single title."""
    key = meta_cache.make_key(title)
    cached = await meta_cache.get(key)
    if cached:
        return {"source": "cache", **cached}

    item = await fetch_best_item(title)
    if not item:
        raise HTTPException(status_code=404, detail="Game not found on RAWG")

    out = extract_scores(item)
    out["fetched_at"] = int(time.time())
    await meta_cache.put(key, out)
    return {"source": "api", **out}
