from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from schemas.schemas import CreateUserRequest, Token
from starlette import status
from models.database import db_dependency
from models.models import User
from fastapi.security import  OAuth2PasswordRequestForm
from security.auth import authenticate_user, create_access_token
from settings import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = User(
        username=create_user_request.username,
        hashed_password = bcrypt_context.hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}