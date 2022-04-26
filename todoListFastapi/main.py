from fastapi import FastAPI
from auth.authorization import *
# to get a string like this run:
# openssl rand -hex 32

todoListFastapi = FastAPI()

todoListFastapi.include_router(auth)

@todoListFastapi.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
