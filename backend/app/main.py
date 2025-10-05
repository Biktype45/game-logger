from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .services import meta_cache, auto_enrich

from .routers import games, stats, meta
from .utils.banner import print_banner




@asynccontextmanager
async def lifespan(app):
    print_banner()
    await meta_cache.init_db()
    try:
        await auto_enrich.auto_enrich_missing()
    except Exception as e:
        print(f"[AutoEnrich] Skipped due to error: {e}")
    yield

app = FastAPI(title="Game Logger API", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router)
app.include_router(stats.router)
app.include_router(meta.router)

@app.get("/", tags=["health"])
async def root():
    return {
        "status": "ok",
        "message": "Game Logger Backend is live!",
        "docs": "/docs"
    }

