from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database.session import SessionLocal
from app.core.database.supabase import get_supabase
from app.core.utils.security import ALGORITHM
from app.users.models.user import User
from app.users.repositories.user_repository import UserRepository
from app.users.repositories.supabase_user_repository import SupabaseUserRepository
from app.users.schemas.token import TokenPayload
from app.users.services.user_service import UserService
from app.users.services.supabase_user_service import SupabaseUserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db=db, model=User)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(repository=repository)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_service = get_user_service(repository=get_user_repository(db))
    user = user_service.get(id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    user_service = get_user_service(
        repository=get_user_repository(SessionLocal())
    )
    if not user_service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    user_service = get_user_service(
        repository=get_user_repository(SessionLocal())
    )
    if not user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


# Supabase 의존성 주입 함수
def get_supabase_user_repository() -> SupabaseUserRepository:
    """
    Supabase 사용자 저장소 의존성 주입
    
    Returns:
        SupabaseUserRepository: Supabase 사용자 저장소
    """
    return SupabaseUserRepository()


def get_supabase_user_service(
    repository: SupabaseUserRepository = Depends(get_supabase_user_repository),
) -> SupabaseUserService:
    """
    Supabase 사용자 서비스 의존성 주입
    
    Args:
        repository: Supabase 사용자 저장소
        
    Returns:
        SupabaseUserService: Supabase 사용자 서비스
    """
    return SupabaseUserService(repository=repository)


def get_current_supabase_user(
    token: str = Depends(reusable_oauth2)
) -> dict:
    """
    현재 Supabase 사용자 조회
    
    Args:
        token: 액세스 토큰
        
    Returns:
        dict: 사용자 정보
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    user_service = get_supabase_user_service()
    user = user_service.get(supabase, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_supabase_user(
    current_user: dict = Depends(get_current_supabase_user),
) -> dict:
    """
    현재 활성화된 Supabase 사용자 조회
    
    Args:
        current_user: 현재 사용자 정보
        
    Returns:
        dict: 활성화된 사용자 정보
    """
    user_service = get_supabase_user_service()
    if not user_service.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_supabase_superuser(
    current_user: dict = Depends(get_current_supabase_user),
) -> dict:
    """
    현재 활성화된 Supabase 관리자 조회
    
    Args:
        current_user: 현재 사용자 정보
        
    Returns:
        dict: 활성화된 관리자 정보
    """
    user_service = get_supabase_user_service()
    if not user_service.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user 