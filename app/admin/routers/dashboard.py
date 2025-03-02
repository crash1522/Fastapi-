from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database.deps import get_db
from app.core.utils.security import get_current_active_superuser
from app.users.models.user import User
from app.users.services import user_service

router = APIRouter()


@router.get("/dashboard", response_model=Dict[str, Any])
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    관리자 대시보드 데이터 조회
    """
    # 사용자 통계
    total_users = len(user_service.get_multi(db))
    active_users = len([u for u in user_service.get_multi(db) if u.is_active])
    superusers = len([u for u in user_service.get_multi(db) if u.is_superuser])
    
    return {
        "user_stats": {
            "total_users": total_users,
            "active_users": active_users,
            "superusers": superusers,
        },
        "system_info": {
            "app_name": "FastAPI 템플릿",
            "version": "0.1.0",
        }
    }


@router.get("/users", response_model=List[Dict[str, Any]])
def get_admin_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    관리자용 사용자 목록 조회 (상세 정보 포함)
    """
    users = user_service.get_multi(db, skip=skip, limit=limit)
    
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "last_login": None,  # 추후 로그인 기록 기능 구현 시 추가
        })
    
    return result


@router.post("/users/{user_id}/activate", response_model=Dict[str, Any])
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    사용자 활성화
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    
    if user.is_active:
        return {"message": "이미 활성화된 사용자입니다.", "user_id": user_id}
    
    user_service.update(db, id=user_id, obj_in={"is_active": True})
    return {"message": "사용자가 활성화되었습니다.", "user_id": user_id}


@router.post("/users/{user_id}/deactivate", response_model=Dict[str, Any])
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    사용자 비활성화
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 계정은 비활성화할 수 없습니다.",
        )
    
    if not user.is_active:
        return {"message": "이미 비활성화된 사용자입니다.", "user_id": user_id}
    
    user_service.update(db, id=user_id, obj_in={"is_active": False})
    return {"message": "사용자가 비활성화되었습니다.", "user_id": user_id}


@router.post("/users/{user_id}/make-admin", response_model=Dict[str, Any])
def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    사용자를 관리자로 승격
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    
    if user.is_superuser:
        return {"message": "이미 관리자 권한을 가진 사용자입니다.", "user_id": user_id}
    
    user_service.update(db, id=user_id, obj_in={"is_superuser": True})
    return {"message": "사용자가 관리자로 승격되었습니다.", "user_id": user_id}


@router.post("/users/{user_id}/remove-admin", response_model=Dict[str, Any])
def remove_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """
    사용자의 관리자 권한 제거
    """
    user = user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자신의 관리자 권한은 제거할 수 없습니다.",
        )
    
    if not user.is_superuser:
        return {"message": "관리자 권한이 없는 사용자입니다.", "user_id": user_id}
    
    user_service.update(db, id=user_id, obj_in={"is_superuser": False})
    return {"message": "사용자의 관리자 권한이 제거되었습니다.", "user_id": user_id} 