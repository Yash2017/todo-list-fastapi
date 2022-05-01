import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from http.client import HTTPException

load_dotenv()

MONGODB_CONNECTION_URL = os.environ.get("MONGODB_CONNECTION_URL")
MONGODB_STRING = os.environ.get("MONGODB_STRING")
db_client: AsyncIOMotorClient = None
USER_COLLECTION_STRING = os.environ.get("USER_COLLECTION_STRING")
TODO_COLLECTION_STRING = os.environ.get("TODO_COLLECTION_STRING")

async def get_db_user_collection_client() -> AsyncIOMotorClient:
    global db_client
    return db_client[MONGODB_STRING][USER_COLLECTION_STRING]

async def get_db_todo_collection_client() -> AsyncIOMotorClient:
    global db_client
    return db_client[MONGODB_STRING][TODO_COLLECTION_STRING]

async def connect_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(MONGODB_CONNECTION_URL, serverSelectionTimeoutMS=5000)
    except:
        raise HTTPException(status_code=500, detail="Could Not Connect To MongoDB Server")

async def close_db():
    global db_client
    db_client.close()