PLATFORM_MAP = {
    "ps5": 187,
    "playstation 5": 187,
    "ps4": 18,
    "playstation 4": 18,
    "pc": 4,
    "switch": 7,
    "nintendo switch": 7,
    "xbox one": 1,
    "xbox series": 186,
    "xbox series x": 186,
    "xbox series s": 186,
}

def map_platform(name: str | None) -> int | None:
    if not name:
        return None
    key = name.strip().lower()
    for k, v in PLATFORM_MAP.items():
        if k in key:
            return v
    return None
