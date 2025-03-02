"""
기본 클래스 및 함수 모듈

이 모듈은 애플리케이션 전체에서 사용되는 기본 클래스와 함수를 정의합니다.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy.ext.declarative import DeclarativeMeta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database.session import get_db

# 모델 타입 변수
ModelType = TypeVar("ModelType")
# 생성 스키마 타입 변수
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 업데이트 스키마 타입 변수
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# 응답 스키마 타입 변수
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseResponse(BaseModel):
    """기본 응답 모델"""
    success: bool = True
    message: str = "성공적으로 처리되었습니다"
    data: Optional[Any] = None

class PaginatedResponse(BaseResponse):
    """페이지네이션 응답 모델"""
    total: int = 0
    page: int = 1
    size: int = 10
    items: List[Any] = []

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
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        항목 생성
        
        Args:
            db: 데이터베이스 세션
            obj_in: 생성할 항목 데이터
            
        Returns:
            생성된 항목
        """
        obj_in_data = obj_in.model_dump()
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
        obj_data = db_obj.__dict__
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
    
    def get(self, db: Session, id: Any) -> Optional[ResponseSchemaType]:
        """
        ID로 항목 조회
        
        Args:
            db: 데이터베이스 세션
            id: 항목 ID
            
        Returns:
            조회된 항목 또는 None
        """
        db_obj = self.repository.get(db=db, id=id)
        if not db_obj:
            return None
        return db_obj
    
    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ResponseSchemaType]:
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
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ResponseSchemaType:
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
        self, db: Session, *, id: Any, obj_in: UpdateSchemaType
    ) -> Optional[ResponseSchemaType]:
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
    
    def remove(self, db: Session, *, id: Any) -> Optional[ResponseSchemaType]:
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

class BaseRouter:
    """
    기본 라우터 클래스
    
    API 엔드포인트를 생성하는 기본 메서드를 제공합니다.
    """
    def __init__(
        self,
        service: BaseService,
        response_model: Type[ResponseSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        prefix: str,
        tags: List[str],
    ):
        """
        라우터 초기화
        
        Args:
            service: 서비스 인스턴스
            response_model: 응답 모델 클래스
            create_schema: 생성 스키마 클래스
            update_schema: 업데이트 스키마 클래스
            prefix: 라우터 접두사
            tags: 태그 목록
        """
        self.service = service
        self.response_model = response_model
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.router = APIRouter(prefix=prefix, tags=tags)
        self._setup_routes()
    
    def _setup_routes(self):
        """기본 라우트 설정"""
        
        @self.router.get("/", response_model=List[self.response_model])
        def read_items(
            skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
        ):
            """
            여러 항목 조회
            """
            items = self.service.get_multi(db=db, skip=skip, limit=limit)
            return items
        
        @self.router.get("/{id}", response_model=self.response_model)
        def read_item(id: int, db: Session = Depends(get_db)):
            """
            단일 항목 조회
            """
            item = self.service.get(db=db, id=id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return item
        
        @self.router.post("/", response_model=self.response_model)
        def create_item(item_in: self.create_schema, db: Session = Depends(get_db)):
            """
            항목 생성
            """
            item = self.service.create(db=db, obj_in=item_in)
            return item
        
        @self.router.put("/{id}", response_model=self.response_model)
        def update_item(id: int, item_in: self.update_schema, db: Session = Depends(get_db)):
            """
            항목 업데이트
            """
            item = self.service.update(db=db, id=id, obj_in=item_in)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return item
        
        @self.router.delete("/{id}", response_model=self.response_model)
        def delete_item(id: int, db: Session = Depends(get_db)):
            """
            항목 삭제
            """
            item = self.service.remove(db=db, id=id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return item 