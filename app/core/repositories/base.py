from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func

# 모델 타입 변수
ModelType = TypeVar("ModelType")
# 생성 스키마 타입 변수
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 업데이트 스키마 타입 변수
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    기본 저장소 클래스
    
    CRUD 작업을 위한 기본 메서드를 제공합니다.
    """
    def __init__(self, model: Type[ModelType]):
        """
        저장소 초기화
        
        Args:
            model: SQLAlchemy 모델 클래스
        """
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        ID로 항목 조회
        
        Args:
            db: 데이터베이스 세션
            id: 항목 ID
            
        Returns:
            조회된 항목 또는 None
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
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
        return db.query(self.model).offset(skip).limit(limit).all()
    
    def get_count(self, db: Session) -> int:
        """
        항목 수 조회
        
        Args:
            db: 데이터베이스 세션
            
        Returns:
            항목 수
        """
        return db.query(func.count(self.model.id)).scalar()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        항목 생성
        
        Args:
            db: 데이터베이스 세션
            obj_in: 생성할 항목 데이터
            
        Returns:
            생성된 항목
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        항목 업데이트
        
        Args:
            db: 데이터베이스 세션
            db_obj: 업데이트할 기존 항목
            obj_in: 업데이트 데이터
            
        Returns:
            업데이트된 항목
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: Any) -> ModelType:
        """
        항목 삭제
        
        Args:
            db: 데이터베이스 세션
            id: 삭제할 항목 ID
            
        Returns:
            삭제된 항목
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
    
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
        return db.query(self.model).filter(getattr(self.model, field_name) == value).first()
    
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
        return (
            db.query(self.model)
            .filter(getattr(self.model, field_name) == value)
            .offset(skip)
            .limit(limit)
            .all()
        ) 