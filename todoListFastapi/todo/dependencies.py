from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from db.db import get_user_from_db
from schema.token_schema.token_schema import TokenData
from redis.redis_helper import get_user_from_redis, set_user_value

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user(username: str):
    try:
        user_from_redis = await get_user_from_redis()
        if user_from_redis:
            for user in user_from_redis:
                if user["username"] == username:
                    return user
        else:
            db = await get_user_from_db()
            await set_user_value(db)
            for user in db:
                if user["username"] == username:
                    return user
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return token_data.username
