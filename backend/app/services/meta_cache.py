import aiosqlite, time

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS meta_cache (
  key TEXT PRIMARY KEY,
  metascore INTEGER,
  url TEXT,
  rating_count INTEGER,
  fetched_at INTEGER
);
"""

def make_key(title: str, platform_id: int | None) -> str:
    return f"{title.strip().lower()}|{platform_id or 'none'}"

async def init_db(path="meta_cache.sqlite"):
    async with aiosqlite.connect(path) as db:
        await db.execute(CREATE_SQL)
        await db.commit()

async def get(key: str, max_age_days=30, path="meta_cache.sqlite"):
    async with aiosqlite.connect(path) as db:
        row = await (await db.execute(
            "SELECT metascore,url,rating_count,fetched_at FROM meta_cache WHERE key=?", (key,)
        )).fetchone()
        if not row:
            return None
        metascore, url, rating_count, fetched_at = row
        if time.time() - fetched_at > max_age_days * 86400:
            return None
        return {"metascore": metascore, "metacritic_url": url, "metacritic_count": rating_count}

async def put(key: str, data: dict, path="meta_cache.sqlite"):
    async with aiosqlite.connect(path) as db:
        await db.execute(
            "INSERT OR REPLACE INTO meta_cache(key, metascore, url, rating_count, fetched_at) VALUES (?,?,?,?,?)",
            (key, data.get("metascore"), data.get("metacritic_url"), data.get("metacritic_count"), int(time.time()))
        )
        await db.commit()
