import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from helper_functions.empty_checker.empty_checker import empty_checker
from log.json_request_dependency.json_request_dependency import json_request_dependency
from .dependencies import *
from db.db import create_user
from schema.profile_schema.profile_schema import profile_schema
from schema.token_schema.token_schema import Token
load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
#API router to route the requests coming at /auth endpoint
auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

#Login endpoint. Please send requests to this as form.
@auth.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        #Checking for authencating the user. This checks whether the user is present in the database
        user = await authenticate_user(form_data.username, form_data.password)

        #Making timedelta for making the authorizatin token
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

        #Making the token
        access_token = create_access_token(
            data={"sub": user["username"]}, expires_delta=access_token_expires
        )

        #Returning the token back
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")


#Signup page which asks the user information
@auth.post("/signup")
async def read_user_me(userInfo:profile_schema, json_request=Depends(json_request_dependency)):
    #Checking whether the requests fields are empty
    empty_checker(userInfo.username, "Username")
    empty_checker(userInfo.password, "Password")

    #Checking if username is already present in the db
    users = await get_user(userInfo.username)
    if users:
        raise HTTPException(status_code=400, detail="Username already exists. Please login using that username")

    #Getting the password has
    userInfo.password = get_password_hash(userInfo.password)

    #Encoding it back to json
    userInfo = jsonable_encoder(userInfo)

    #Creating the useer
    result = await create_user(userInfo)
    if not result:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"Message": "User Account Created"}

    

