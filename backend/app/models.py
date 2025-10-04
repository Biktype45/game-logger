from pydantic import BaseModel
from typing import Optional
from datetime import date

class GameRow(BaseModel):
    idx: int
    title: str
    platform: Optional[str] = None
    completed_on: Optional[date] = None
    hours: Optional[float] = None
    rating: Optional[str] = None
    developer: Optional[str] = None
    # NEW: enrichment fields (stay None until filled)
    metascore: Optional[int] = None
    metascore_platform: Optional[int] = None
    metacritic_url: Optional[str] = None
    metacritic_count: Optional[int] = None


class StatsResponse(BaseModel):
    platform_counts: dict[str, int]
    year_counts: dict[str, int]

class VersionResponse(BaseModel):
    version: str
