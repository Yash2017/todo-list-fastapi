from http.client import HTTPException
import json
import aioredis

async def get_redis_client():
    try:
        redis = await aioredis.from_url("redis://localhost:6379", decode_responses=True, max_connections=10)
        return redis
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_redis_value(current_user):
    redis = await get_redis_client()
    redis_todo_value = await redis.get(current_user)
    if redis_todo_value:
        value = json.loads(redis_todo_value)
        return value
    else:
        return False

async def set_redis_value(current_user, todo_data):
    redis = await get_redis_client()
    await redis.set(current_user, json.dumps(todo_data))
    await redis.expire(current_user, 60)

async def find_todo_in_redis(current_user, todo_id):
    redis_todo_value = await get_redis_value(current_user)
    if redis_todo_value:
        for todo in redis_todo_value:
            if str(todo_id) == todo["_id"]:
                return True
        return False
    else:
        return False



