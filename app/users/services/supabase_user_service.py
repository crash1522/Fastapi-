from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import logging

from supabase import Client
from pydantic import EmailStr

from app.core.config import settings
from app.core.utils.security import create_access_token
from app.users.schemas.user import UserCreate, UserUpdate, User as UserSchema
from app.users.repositories.supabase_user_repository import SupabaseUserRepository

logger = logging.getLogger(__name__)

class SupabaseUserService:
    """
    Supabase 기반 사용자 서비스
    
    사용자 관련 비즈니스 로직을 처리합니다.
    """
    def __init__(self, repository: SupabaseUserRepository):
        """
        서비스 초기화
        
        Args:
            repository: Supabase 사용자 저장소
        """
        self.repository = repository
    
    def get(self, supabase: Client, id: Any) -> Optional[Dict[str, Any]]:
        """
        ID로 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            id: 사용자 ID
            
        Returns:
            사용자 정보 또는 None
        """
        return self.repository.get(supabase, id)
    
    def get_by_email(self, supabase: Client, email: str) -> Optional[Dict[str, Any]]:
        """
        이메일로 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            email: 사용자 이메일
            
        Returns:
            사용자 정보 또는 None
        """
        return self.repository.get_by_email(supabase, email)
    
    def get_by_username(self, supabase: Client, username: str) -> Optional[Dict[str, Any]]:
        """
        사용자명으로 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            username: 사용자명
            
        Returns:
            사용자 정보 또는 None
        """
        return self.repository.get_by_username(supabase, username)
    
    def get_multi(self, supabase: Client, *, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        여러 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            skip: 건너뛸 항목 수
            limit: 최대 항목 수
            
        Returns:
            사용자 목록
        """
        return self.repository.get_multi(supabase, skip=skip, limit=limit)
    
    def create(self, supabase: Client, *, obj_in: UserCreate) -> Dict[str, Any]:
        """
        사용자 생성
        
        Args:
            supabase: Supabase 클라이언트
            obj_in: 생성할 사용자 데이터
            
        Returns:
            생성된 사용자 정보
        """
        # 이메일 중복 확인
        user = self.repository.get_by_email(supabase, email=obj_in.email)
        if user:
            raise ValueError(f"이미 등록된 이메일입니다: {obj_in.email}")
        
        # 사용자명 중복 확인
        user = self.repository.get_by_username(supabase, username=obj_in.username)
        if user:
            raise ValueError(f"이미 사용 중인 사용자명입니다: {obj_in.username}")
        
        # 사용자 생성
        return self.repository.create(supabase, obj_in=obj_in)
    
    def update(self, supabase: Client, *, id: Any, obj_in: Union[UserUpdate, Dict[str, Any]]) -> Dict[str, Any]:
        """
        사용자 업데이트
        
        Args:
            supabase: Supabase 클라이언트
            id: 업데이트할 사용자 ID
            obj_in: 업데이트 데이터
            
        Returns:
            업데이트된 사용자 정보
        """
        # 사용자 존재 확인
        user = self.repository.get(supabase, id)
        if not user:
            raise ValueError(f"사용자를 찾을 수 없습니다: {id}")
        
        # 이메일 중복 확인
        if isinstance(obj_in, dict):
            email = obj_in.get("email")
        else:
            email = obj_in.email if obj_in.email else None
        
        if email and email != user["email"]:
            existing_user = self.repository.get_by_email(supabase, email=email)
            if existing_user:
                raise ValueError(f"이미 등록된 이메일입니다: {email}")
        
        # 사용자명 중복 확인
        if isinstance(obj_in, dict):
            username = obj_in.get("username")
        else:
            username = obj_in.username if obj_in.username else None
        
        if username and username != user["username"]:
            existing_user = self.repository.get_by_username(supabase, username=username)
            if existing_user:
                raise ValueError(f"이미 사용 중인 사용자명입니다: {username}")
        
        # 사용자 업데이트
        return self.repository.update(supabase, id=id, obj_in=obj_in)
    
    def remove(self, supabase: Client, *, id: Any) -> Dict[str, Any]:
        """
        사용자 삭제
        
        Args:
            supabase: Supabase 클라이언트
            id: 삭제할 사용자 ID
            
        Returns:
            삭제된 사용자 정보
        """
        # 사용자 존재 확인
        user = self.repository.get(supabase, id)
        if not user:
            raise ValueError(f"사용자를 찾을 수 없습니다: {id}")
        
        # 사용자 삭제
        return self.repository.remove(supabase, id=id)
    
    def authenticate(self, supabase: Client, *, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        사용자 인증
        
        Args:
            supabase: Supabase 클라이언트
            email: 사용자 이메일
            password: 비밀번호
            
        Returns:
            인증된 사용자 정보 또는 None
        """
        return self.repository.authenticate(supabase, email=email, password=password)
    
    def create_access_token(self, user_id: int) -> Dict[str, str]:
        """
        액세스 토큰 생성
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            액세스 토큰 정보
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": create_access_token(
                data={"sub": str(user_id)}, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    
    def is_active(self, user: Dict[str, Any]) -> bool:
        """
        사용자 활성화 여부 확인
        
        Args:
            user: 사용자 정보
            
        Returns:
            활성화 여부
        """
        return self.repository.is_active(user)
    
    def is_superuser(self, user: Dict[str, Any]) -> bool:
        """
        관리자 여부 확인
        
        Args:
            user: 사용자 정보
            
        Returns:
            관리자 여부
        """
        return self.repository.is_superuser(user) 