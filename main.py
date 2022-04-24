import uvicorn

from fastapi import FastAPI

todoListFastapi = FastAPI()

@todoListFastapi.get("/", tags=["test"])
def test():
    return {"hello", "world"}