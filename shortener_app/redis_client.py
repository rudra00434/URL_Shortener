import os

import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


def get_cached_url(shortened_url: str) -> str | None:
    return redis_client.get(f"url:{shortened_url}")


def cache_url(
    shortened_url: str,
    original_url: str,
    ttl: int = 3600
) -> None:
    redis_client.setex(
        f"url:{shortened_url}",
        ttl,
        original_url
    )


def delete_cached_url(shortened_url: str) -> None:
    redis_client.delete(f"url:{shortened_url}")
