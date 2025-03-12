from fastapi import APIRouter, status, HTTPException, Depends
from models.database import  db_dependency
from schemas.schemas import UserBase
from security.auth import get_current_active_user
from typing import Annotated
from pydantic import BaseModel, EmailStr
from models.database import get_db, Session
from sqlalchemy import Column, Integer, String
from models.database import Base
from models.models import User

router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.get("/me/", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[UserBase, Depends(get_current_active_user)]
):
    return current_user


class EmailOnly(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)

class UserCreate(BaseModel):
    email: EmailStr
    description: str

class EmailCreate(BaseModel):
    email: EmailStr


@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(email=user.email, description=user.description)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created successfully", "user": db_user}

@router.post("/emails/")
def create_email(email: EmailCreate, db: Session = Depends(get_db)):
    db_email = EmailOnly(email=email.email)
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return {"message": "Email saved successfully", "email": db_email}