from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database.supabase import get_supabase
from app.users.dependencies import get_supabase_user_service
from app.users.schemas.token import Token
from app.users.schemas.user import UserCreate
from app.users.services.supabase_user_service import SupabaseUserService

router = APIRouter()


@router.post("/login", response_model=Token)
def login_access_token(
    service: SupabaseUserService = Depends(get_supabase_user_service),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 호환 토큰 로그인, 액세스 토큰 발급
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    user = service.authenticate(
        supabase, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    if not service.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    
    return service.create_access_token(user["id"])


@router.post("/register", response_model=Token)
def register_user(
    *,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    user_in: UserCreate,
) -> Any:
    """
    사용자 등록 및 액세스 토큰 발급
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    # 이메일 중복 확인
    user = service.get_by_email(supabase, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="이미 등록된 이메일입니다.",
        )
    
    # 사용자명 중복 확인
    user = service.get_by_username(supabase, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="이미 사용 중인 사용자명입니다.",
        )
    
    try:
        user = service.create(supabase, obj_in=user_in)
        return service.create_access_token(user["id"])
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) 