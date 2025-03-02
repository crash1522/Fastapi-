from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.repositories.base import BaseRepository

# 모델 타입 변수
ModelType = TypeVar("ModelType")
# 생성 스키마 타입 변수
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 업데이트 스키마 타입 변수
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# 응답 스키마 타입 변수
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
    """
    기본 서비스 클래스
    
    비즈니스 로직을 처리하는 기본 메서드를 제공합니다.
    """
    def __init__(self, repository: BaseRepository):
        """
        서비스 초기화
        
        Args:
            repository: 저장소 인스턴스
        """
        self.repository = repository
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        ID로 항목 조회
        
        Args:
            db: 데이터베이스 세션
            id: 항목 ID
            
        Returns:
            조회된 항목 또는 None
        """
        return self.repository.get(db=db, id=id)
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        여러 항목 조회
        
        Args:
            db: 데이터베이스 세션
            skip: 건너뛸 항목 수
            limit: 최대 항목 수
            
        Returns:
            항목 목록
        """
        return self.repository.get_multi(db=db, skip=skip, limit=limit)
    
    def get_count(self, db: Session) -> int:
        """
        항목 수 조회
        
        Args:
            db: 데이터베이스 세션
            
        Returns:
            항목 수
        """
        return self.repository.get_count(db=db)
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        항목 생성
        
        Args:
            db: 데이터베이스 세션
            obj_in: 생성할 항목 데이터
            
        Returns:
            생성된 항목
        """
        return self.repository.create(db=db, obj_in=obj_in)
    
    def update(
        self, db: Session, *, id: Any, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> Optional[ModelType]:
        """
        항목 업데이트
        
        Args:
            db: 데이터베이스 세션
            id: 업데이트할 항목 ID
            obj_in: 업데이트 데이터
            
        Returns:
            업데이트된 항목 또는 None
        """
        db_obj = self.repository.get(db=db, id=id)
        if not db_obj:
            return None
        return self.repository.update(db=db, db_obj=db_obj, obj_in=obj_in)
    
    def remove(self, db: Session, *, id: Any) -> Optional[ModelType]:
        """
        항목 삭제
        
        Args:
            db: 데이터베이스 세션
            id: 삭제할 항목 ID
            
        Returns:
            삭제된 항목 또는 None
        """
        db_obj = self.repository.get(db=db, id=id)
        if not db_obj:
            return None
        return self.repository.remove(db=db, id=id)
    
    def get_by_field(self, db: Session, field_name: str, value: Any) -> Optional[ModelType]:
        """
        필드 값으로 항목 조회
        
        Args:
            db: 데이터베이스 세션
            field_name: 필드 이름
            value: 필드 값
            
        Returns:
            조회된 항목 또는 None
        """
        return self.repository.get_by_field(db=db, field_name=field_name, value=value)
    
    def get_multi_by_field(
        self, db: Session, field_name: str, value: Any, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        필드 값으로 여러 항목 조회
        
        Args:
            db: 데이터베이스 세션
            field_name: 필드 이름
            value: 필드 값
            skip: 건너뛸 항목 수
            limit: 최대 항목 수
            
        Returns:
            항목 목록
        """
        return self.repository.get_multi_by_field(
            db=db, field_name=field_name, value=value, skip=skip, limit=limit
        ) 