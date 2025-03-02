from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.utils.security import create_access_token, verify_password, get_password_hash
from app.users.models.user import User
from app.users.repositories.user_repository import UserRepository
from app.users.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.core.services.base import BaseService


class UserService(BaseService[User, UserCreate, UserUpdate, UserSchema]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        return self.repository.get_by_email(db=db, email=email)
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        return self.repository.get_by_username(db=db, username=username)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """사용자 생성"""
        # 이메일 중복 확인
        user = self.repository.get_by_email(db, email=obj_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다."
            )
        
        # 사용자명 중복 확인
        username_exists = self.repository.get_by_username(db, username=obj_in.username)
        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자 이름입니다."
            )
        
        return self.repository.create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, id: int, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        """사용자 정보 업데이트"""
        user = self.repository.get(db=db, id=id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="사용자를 찾을 수 없습니다."
            )
        
        # 이메일 중복 확인
        if isinstance(obj_in, dict):
            email = obj_in.get("email")
        else:
            email = obj_in.email
        
        if email and email != user.email:
            existing_user = self.repository.get_by_email(db, email=email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 등록된 이메일입니다."
                )
        
        # 사용자명 중복 확인
        if isinstance(obj_in, dict):
            username = obj_in.get("username")
        else:
            username = obj_in.username
        
        if username and username != user.username:
            existing_username = self.repository.get_by_username(db, username=username)
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 사용 중인 사용자 이름입니다."
                )
        
        return self.repository.update(db=db, db_obj=user, obj_in=obj_in)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """사용자 인증"""
        user = self.repository.authenticate(db=db, email=email, password=password)
        return user

    def create_access_token(self, user_id: int) -> Dict[str, str]:
        """액세스 토큰 생성"""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                data={"sub": str(user_id)}, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

    def is_active(self, user: User) -> bool:
        """사용자 활성화 여부 확인"""
        return self.repository.is_active(user=user)

    def is_superuser(self, user: User) -> bool:
        """관리자 여부 확인"""
        return self.repository.is_superuser(user=user) 