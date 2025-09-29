from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .services import meta_cache

from .routers import games, stats, meta




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await meta_cache.init_db()
    yield
    # Shutdown (if you need cleanup later)
    # e.g., close DB connections, stop background tasks

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

