from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# 기본 사용자 스키마
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False


# 사용자 생성 요청 스키마
class UserCreate(UserBase):
    password: str


# 사용자 업데이트 요청 스키마
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


# 데이터베이스에서 반환된 사용자 스키마
class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# API 응답용 사용자 스키마
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 토큰 스키마
class Token(BaseModel):
    access_token: str
    token_type: str


# 토큰 데이터 스키마
class TokenPayload(BaseModel):
    sub: int
    exp: datetime 