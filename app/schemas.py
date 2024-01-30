
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserGet(BaseModel):
    email: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    owner: UserGet


class PostCreate(PostBase):
    pass


class Post(PostBase):
    created_at: datetime
    owner_id: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
