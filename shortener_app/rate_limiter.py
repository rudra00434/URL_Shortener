import time

from fastapi import HTTPException, Request

from .redis_client import redis_client


RATE_LIMIT = 10
WINDOW_SECONDS = 60


def check_rate_limit(request: Request) -> None:
    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.setex(
            key,
            WINDOW_SECONDS,
            1
        )
        return

    current_count = int(current_count)

    if current_count >= RATE_LIMIT:
        ttl = redis_client.ttl(key)

        raise HTTPException(
            status_code=429,
            detail={
                "message": "Rate limit exceeded",
                "retry_after": ttl
            }
        )

    redis_client.incr(key)
