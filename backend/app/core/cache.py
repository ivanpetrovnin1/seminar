import redis
from app.core.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def delete_url_cache(short_code: str):
    key = f"link:{short_code}"
    redis_client.delete(key)