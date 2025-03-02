from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from app.core.database.supabase import get_supabase
from app.users.dependencies import (
    get_current_active_supabase_superuser,
    get_current_active_supabase_user,
    get_supabase_user_service,
)
from app.users.schemas.user import User, UserCreate, UserUpdate
from app.users.services.supabase_user_service import SupabaseUserService

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    *,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_active_supabase_superuser),
) -> Any:
    """
    모든 사용자 조회 (관리자 전용)
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    users = service.get_multi(supabase, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create_user(
    *,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    user_in: UserCreate,
) -> Any:
    """
    새 사용자 생성
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
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/me", response_model=User)
def read_user_me(
    current_user: dict = Depends(get_current_active_supabase_user),
) -> Any:
    """
    현재 사용자 정보 조회
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    password: Optional[str] = Body(None),
    full_name: Optional[str] = Body(None),
    email: Optional[EmailStr] = Body(None),
    username: Optional[str] = Body(None),
    current_user: dict = Depends(get_current_active_supabase_user),
) -> Any:
    """
    현재 사용자 정보 업데이트
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    if username is not None:
        user_in.username = username
    
    try:
        user = service.update(supabase, id=current_user["id"], obj_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/{user_id}", response_model=User)
def read_user_by_id(
    user_id: int,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    current_user: dict = Depends(get_current_active_supabase_user),
) -> Any:
    """
    특정 사용자 정보 조회
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    user = service.get(supabase, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # 관리자가 아니면서 다른 사용자 정보를 조회하려는 경우
    if not service.is_superuser(current_user) and user_id != current_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges",
        )
    
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    user_id: int,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    user_in: UserUpdate,
    current_user: dict = Depends(get_current_active_supabase_superuser),
) -> Any:
    """
    특정 사용자 정보 업데이트 (관리자 전용)
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    user = service.get(supabase, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    try:
        user = service.update(supabase, id=user_id, obj_in=user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    user_id: int,
    service: SupabaseUserService = Depends(get_supabase_user_service),
    current_user: dict = Depends(get_current_active_supabase_superuser),
) -> Any:
    """
    특정 사용자 삭제 (관리자 전용)
    """
    supabase = get_supabase()
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client not initialized",
        )
    
    user = service.get(supabase, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    
    # 자기 자신을 삭제하려는 경우
    if user_id == current_user["id"]:
        raise HTTPException(
            status_code=400,
            detail="Users cannot delete themselves",
        )
    
    user = service.remove(supabase, id=user_id)
    return user 