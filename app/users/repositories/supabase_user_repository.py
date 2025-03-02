from typing import List, Optional, Dict, Any, Union
import logging
from supabase import Client

from app.core.utils.security import get_password_hash, verify_password
from app.users.schemas.user import UserCreate, UserUpdate
from app.core.repositories.supabase_base import SupabaseBaseRepository

logger = logging.getLogger(__name__)

class SupabaseUserRepository(SupabaseBaseRepository[Dict[str, Any], UserCreate, UserUpdate]):
    """
    Supabase 기반 사용자 저장소
    
    사용자 관련 CRUD 작업을 Supabase를 통해 처리합니다.
    """
    def __init__(self):
        """저장소 초기화"""
        super().__init__("users")
    
    def get_by_email(self, supabase: Client, email: str) -> Optional[Dict[str, Any]]:
        """
        이메일로 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            email: 사용자 이메일
            
        Returns:
            사용자 정보 또는 None
        """
        return self.get_by_field(supabase, "email", email)
    
    def get_by_username(self, supabase: Client, username: str) -> Optional[Dict[str, Any]]:
        """
        사용자명으로 사용자 조회
        
        Args:
            supabase: Supabase 클라이언트
            username: 사용자명
            
        Returns:
            사용자 정보 또는 None
        """
        return self.get_by_field(supabase, "username", username)
    
    def create(self, supabase: Client, *, obj_in: UserCreate) -> Dict[str, Any]:
        """
        사용자 생성
        
        Args:
            supabase: Supabase 클라이언트
            obj_in: 생성할 사용자 데이터
            
        Returns:
            생성된 사용자 정보
        """
        db_obj = {
            "email": obj_in.email,
            "username": obj_in.username,
            "hashed_password": get_password_hash(obj_in.password),
            "full_name": obj_in.full_name,
            "is_active": obj_in.is_active,
            "is_superuser": obj_in.is_superuser,
        }
        
        try:
            response = supabase.table(self.table_name).insert(db_obj).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"사용자 생성 중 오류 발생: {e}")
            raise
    
    def update(
        self, supabase: Client, *, id: Any, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        사용자 업데이트
        
        Args:
            supabase: Supabase 클라이언트
            id: 업데이트할 사용자 ID
            obj_in: 업데이트 데이터
            
        Returns:
            업데이트된 사용자 정보
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # 비밀번호가 있으면 해시 처리
        if "password" in update_data:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        try:
            response = supabase.table(self.table_name).update(update_data).eq("id", id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"사용자 업데이트 중 오류 발생: {e}")
            raise
    
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
        user = self.get_by_email(supabase, email)
        if not user:
            return None
        if not verify_password(password, user["hashed_password"]):
            return None
        return user
    
    def is_active(self, user: Dict[str, Any]) -> bool:
        """
        사용자 활성화 여부 확인
        
        Args:
            user: 사용자 정보
            
        Returns:
            활성화 여부
        """
        return user["is_active"]
    
    def is_superuser(self, user: Dict[str, Any]) -> bool:
        """
        관리자 여부 확인
        
        Args:
            user: 사용자 정보
            
        Returns:
            관리자 여부
        """
        return user["is_superuser"] 