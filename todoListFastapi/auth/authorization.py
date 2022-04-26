from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from .dependencies import *
from db.db import *
from schema.profile_schema.profile_schema import profile_schema

auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2a$12$sZKW5DqvQzPDpR0IOhQNNu.gVdnnMdlZ3EhIv4FmHAfmDuam6EPyy",
        "disabled": False,
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str


@auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth.post("/signup")
async def read_user_me(userInfo:profile_schema):
    users = await get_user()
    if users:
        raise HTTPException(status_code=400, detail="Username already exists. Please login using that username")
    userInfo.password = get_password_hash(userInfo.password)
    userInfo = jsonable_encoder(userInfo)
    await do_insert(userInfo)
    return {"Message": "User Account Created"}
    

