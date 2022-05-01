import aioredis
from fastapi import HTTPException

redis = None

async def get_redis_client():
    global redis
    return redis

async def close_redis_client():
    global redis
    await redis.close()

async def make_redis_client():
    try:
        global redis
        redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True, max_connections=10)
    except:
        raise HTTPException(status_code=500, detail="Could Not Connect To Redis Server")
