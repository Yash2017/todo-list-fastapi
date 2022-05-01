from motor.motor_asyncio import AsyncIOMotorClient
from http.client import HTTPException
conn_str = "mongodb+srv://yashkakade:yashkakade@bug-tracker.np7pj.mongodb.net/todo-list-fastapi?retryWrites=true&w=majority"
db_str = "todo-list-fastapi"
db_client: AsyncIOMotorClient = None
user_collection_str = "profile"
todo_collection_str = "todo_information"

async def get_db_user_collection_client() -> AsyncIOMotorClient:
    global db_client
    return db_client[db_str][user_collection_str]

async def get_db_todo_collection_client() -> AsyncIOMotorClient:
    global db_client
    return db_client[db_str][todo_collection_str]

async def connect_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
    except:
        raise HTTPException(status_code=500, detail="Could Not Connect To MongoDB Server")

async def close_db():
    global db_client
    db_client.close()