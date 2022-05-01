import os
from dotenv import load_dotenv
import aioredis
from fastapi import HTTPException

load_dotenv()
REDIS_URL_WITH_PORT = os.environ.get("REDIS_URL_WITH_PORT")
redis = None
#Function to the get the redis client
async def get_redis_client():
    global redis
    return redis

#Function to close the redis client when the application shutsdown
async def close_redis_client():
    global redis
    await redis.close()

#Makes the redis client when the application starts
async def make_redis_client():
    try:
        global redis
        redis = await aioredis.from_url(REDIS_URL_WITH_PORT, decode_responses=True, max_connections=10)
    except:
        raise HTTPException(status_code=500, detail="Could Not Connect To Redis Server")
