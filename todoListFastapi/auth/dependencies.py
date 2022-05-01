import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer 
from jose import jwt
from passlib.context import CryptContext
from db.db import get_user_from_db
from redis.redis_helper import get_user_from_redis, set_user_value

load_dotenv()
#Getting the environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#Function to verify the password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Function to get the password
def get_password_hash(password):
    return pwd_context.hash(password)

#Function which checks whether the username is present in the redis cache. If it isn't then it calls the db
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

'''
Authenticating the user by checking if the username is present in the db or not. Also verfying the password
'''
async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

'''
Creating an access token by using the current time and adding the expire time.
'''
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


