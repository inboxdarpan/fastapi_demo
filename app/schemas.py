from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: int
    created_at: datetime #note: default value provided
    owner_id: int
    owner: UserCreate
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None