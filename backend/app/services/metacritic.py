from __future__ import annotations
import asyncio, time
import httpx
from typing import Optional
from ..config import settings

# polite throttle
_sem = asyncio.Semaphore(settings.RAWG_RPS)

async def _sleep_for_rps():
    await asyncio.sleep(1 / max(settings.RAWG_RPS, 1))

async def fetch_best_item(title: str) -> Optional[dict]:
    """Fetch top RAWG search result for given game title (no platform-specific queries)."""
    if not title or not settings.RAWG_API_KEY:
        return None

    params = {
        "search": title,
        "page_size": 1,
        "key": settings.RAWG_API_KEY,
    }

    retries = settings.RAWG_MAX_RETRIES
    async with _sem:
        for attempt in range(retries + 1):
            try:
                async with httpx.AsyncClient(timeout=settings.RAWG_TIMEOUT) as client:
                    r = await client.get(f"{settings.RAWG_BASE_URL}/games", params=params)
                if r.status_code == 429:
                    # Rate limit: backoff and retry
                    await asyncio.sleep(2 ** attempt)
                    if attempt == retries:
                        return None
                    continue
                if r.status_code != 200:
                    return None
                js = r.json()
                results = js.get("results") or []
                return results[0] if results else None
            except Exception:
                # network error, safe-fail
                return None
            finally:
                await _sleep_for_rps()


def extract_scores(item: dict) -> dict:
    """Extract Metacritic-related data from RAWG item."""
    return {
        "metascore": item.get("metacritic"),
        "metacritic_url": item.get("metacritic_url"),
        "metacritic_count": item.get("ratings_count"),
    }
