from __future__ import annotations
from typing import Optional
from . import meta_cache
from .metacritic import fetch_best_item, extract_scores

def _key(title: str) -> str:
    return meta_cache.make_key(title, None)

async def enrich_one(title: str, platform: Optional[str] = None) -> Optional[dict]:
    """Return dict with metascore fields or None (cache-first, title-only lookup)."""
    k = _key(title)
    cached = await meta_cache.get(k)
    if cached:
        return cached

    item = await fetch_best_item(title)
    if not item:
        return None

    data = extract_scores(item)
    await meta_cache.put(k, data)
    return data
