from fastapi import APIRouter, Query, HTTPException
from ..services import platforms, meta_cache
import httpx, time
from ..config import settings

router = APIRouter(prefix="/api/meta", tags=["meta"])

@router.get("/test")
async def test_enrich(title: str = Query(...), platform: str = Query(...)):
    """Test RAWG enrichment for a single title+platform."""
    pid = platforms.map_platform(platform)
    if not pid:
        raise HTTPException(status_code=400, detail=f"Unknown platform: {platform}")

    key = meta_cache.make_key(title, pid)

    # 1. Try cache
    cached = await meta_cache.get(key)
    if cached:
        return {"source": "cache", **cached}

    # 2. Query RAWG API
    params = {"search": title, "platforms": pid, "key": settings.RAWG_API_KEY, "page_size": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{settings.RAWG_BASE_URL}/games", params=params, timeout=20.0)
        if r.status_code != 200:
            raise HTTPException(status_code=r.status_code, detail=r.text)
        data = r.json()

    if not data.get("results"):
        return {"source": "api", "metascore": None, "metacritic_url": None}

    best = data["results"][0]

    # Try to extract platform-specific metascore
    platform_score = None
    if "metacritic_platforms" in best and best["metacritic_platforms"]:
        for mp in best["metacritic_platforms"]:
            if mp.get("platform", {}).get("id") == pid:
                platform_score = mp.get("metascore")
                break

    out = {
        "metascore": platform_score or best.get("metacritic"),
        "metascore_platform": platform_score,
        "metacritic_url": best.get("metacritic_url"),
        "metacritic_count": best.get("ratings_count"),
        "fetched_at": int(time.time()),
    }


    # 3. Save to cache
    await meta_cache.put(key, out)

    return {"source": "api", **out}
