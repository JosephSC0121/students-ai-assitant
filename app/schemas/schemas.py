from pydantic import BaseModel
from datetime import date


class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    id : int
    username : str

