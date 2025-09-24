from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    EXCEL_PATH: str = "../data/games.xlsx"
    PREFERRED_SHEET: str | None = "Raw Data"  # fallback to first sheet if missing
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    # Polling-based refresh on the frontend uses this version endpoint

settings = Settings()
