from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from supabase import Client

# 모델 타입 변수
ModelType = TypeVar("ModelType")
# 생성 스키마 타입 변수
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 업데이트 스키마 타입 변수
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class SupabaseBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Supabase 기반 기본 저장소 클래스
    
    Supabase를 사용한 CRUD 작업을 위한 기본 메서드를 제공합니다.
    """
    def __init__(self, table_name: str):
        """
        저장소 초기화
        
        Args:
            table_name: Supabase 테이블 이름
        """
        self.table_name = table_name
    
    def get(self, supabase: Client, id: Any) -> Optional[Dict[str, Any]]:
        """
        ID로 항목 조회
        
        Args:
            supabase: Supabase 클라이언트
            id: 항목 ID
            
        Returns:
            조회된 항목 또는 None
        """
        response = supabase.table(self.table_name).select("*").eq("id", id).execute()
        data = response.data
        return data[0] if data else None
    
    def get_multi(
        self, supabase: Client, *, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        여러 항목 조회
        
        Args:
            supabase: Supabase 클라이언트
            skip: 건너뛸 항목 수
            limit: 최대 항목 수
            
        Returns:
            항목 목록
        """
        response = supabase.table(self.table_name).select("*").range(skip, skip + limit - 1).execute()
        return response.data
    
    def get_count(self, supabase: Client) -> int:
        """
        항목 수 조회
        
        Args:
            supabase: Supabase 클라이언트
            
        Returns:
            항목 수
        """
        response = supabase.table(self.table_name).select("id", count="exact").execute()
        return response.count
    
    def create(self, supabase: Client, *, obj_in: CreateSchemaType) -> Dict[str, Any]:
        """
        항목 생성
        
        Args:
            supabase: Supabase 클라이언트
            obj_in: 생성할 항목 데이터
            
        Returns:
            생성된 항목
        """
        obj_in_data = jsonable_encoder(obj_in)
        response = supabase.table(self.table_name).insert(obj_in_data).execute()
        return response.data[0] if response.data else None
    
    def update(
        self, supabase: Client, *, id: Any, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        항목 업데이트
        
        Args:
            supabase: Supabase 클라이언트
            id: 업데이트할 항목 ID
            obj_in: 업데이트 데이터
            
        Returns:
            업데이트된 항목
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        response = supabase.table(self.table_name).update(update_data).eq("id", id).execute()
        return response.data[0] if response.data else None
    
    def remove(self, supabase: Client, *, id: Any) -> Dict[str, Any]:
        """
        항목 삭제
        
        Args:
            supabase: Supabase 클라이언트
            id: 삭제할 항목 ID
            
        Returns:
            삭제된 항목
        """
        response = supabase.table(self.table_name).delete().eq("id", id).execute()
        return response.data[0] if response.data else None
    
    def get_by_field(self, supabase: Client, field_name: str, value: Any) -> Optional[Dict[str, Any]]:
        """
        필드 값으로 항목 조회
        
        Args:
            supabase: Supabase 클라이언트
            field_name: 필드 이름
            value: 필드 값
            
        Returns:
            조회된 항목 또는 None
        """
        response = supabase.table(self.table_name).select("*").eq(field_name, value).execute()
        data = response.data
        return data[0] if data else None
    
    def get_multi_by_field(
        self, supabase: Client, field_name: str, value: Any, *, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        필드 값으로 여러 항목 조회
        
        Args:
            supabase: Supabase 클라이언트
            field_name: 필드 이름
            value: 필드 값
            skip: 건너뛸 항목 수
            limit: 최대 항목 수
            
        Returns:
            항목 목록
        """
        response = (
            supabase.table(self.table_name)
            .select("*")
            .eq(field_name, value)
            .range(skip, skip + limit - 1)
            .execute()
        )
        return response.data 