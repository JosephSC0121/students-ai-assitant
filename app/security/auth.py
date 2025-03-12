from datetime import timedelta, datetime
from typing import Annotated
from fastapi import  Depends, HTTPException
from starlette import status
from models.models import User
from jose import jwt, JWTError
from settings import SECRET_KEY, ALGORITHM, bcrypt_context, oauth2_scheme

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token : Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate user.")
    
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.get('disabled'):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
    