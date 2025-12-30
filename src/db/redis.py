import redis
from src.config import settings
from redis.asyncio import Redis

JTI_EXPIRY = 3600

redis_client = Redis.from_url(
    settings.redis_url,
    decode_responses=True
)


async def add_jti_to_blocklist(jti: str) -> None:
    await redis_client.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti:str) -> bool:
   jti =  await redis_client.get(jti)
   return jti is not None