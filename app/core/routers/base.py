from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database.session import get_db
from app.core.services.base import BaseService
from app.core.schemas.base import BaseResponseSchema, PaginatedResponseSchema

# 모델 타입 변수
ModelType = TypeVar("ModelType")
# 생성 스키마 타입 변수
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# 업데이트 스키마 타입 변수
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
# 응답 스키마 타입 변수
ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseModel)

class BaseRouter(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ResponseSchemaType]):
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
        
        @self.router.get(
            "/",
            response_model=PaginatedResponseSchema[self.response_model],
            summary="항목 목록 조회",
            description="페이지네이션을 적용하여 항목 목록을 조회합니다.",
        )
        async def read_items(
            skip: int = Query(0, ge=0, description="건너뛸 항목 수"),
            limit: int = Query(100, ge=1, le=100, description="최대 항목 수"),
            db: Session = Depends(get_db),
        ):
            """
            여러 항목 조회
            """
            items = self.service.get_multi(db=db, skip=skip, limit=limit)
            total = self.service.get_count(db=db)
            return {
                "success": True,
                "message": "항목 목록을 성공적으로 조회했습니다",
                "total": total,
                "page": skip // limit + 1 if limit > 0 else 1,
                "size": limit,
                "items": items,
            }
        
        @self.router.get(
            "/{id}",
            response_model=BaseResponseSchema[self.response_model],
            summary="항목 상세 조회",
            description="ID를 기준으로 항목을 상세 조회합니다.",
        )
        async def read_item(
            id: int = Path(..., ge=1, description="항목 ID"),
            db: Session = Depends(get_db),
        ):
            """
            단일 항목 조회
            """
            item = self.service.get(db=db, id=id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return {
                "success": True,
                "message": "항목을 성공적으로 조회했습니다",
                "data": item,
            }
        
        @self.router.post(
            "/",
            response_model=BaseResponseSchema[self.response_model],
            status_code=status.HTTP_201_CREATED,
            summary="항목 생성",
            description="새로운 항목을 생성합니다.",
        )
        async def create_item(
            item_in: self.create_schema,
            db: Session = Depends(get_db),
        ):
            """
            항목 생성
            """
            item = self.service.create(db=db, obj_in=item_in)
            return {
                "success": True,
                "message": "항목을 성공적으로 생성했습니다",
                "data": item,
            }
        
        @self.router.put(
            "/{id}",
            response_model=BaseResponseSchema[self.response_model],
            summary="항목 수정",
            description="ID를 기준으로 항목을 수정합니다.",
        )
        async def update_item(
            id: int = Path(..., ge=1, description="항목 ID"),
            item_in: self.update_schema = None,
            db: Session = Depends(get_db),
        ):
            """
            항목 업데이트
            """
            item = self.service.update(db=db, id=id, obj_in=item_in)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return {
                "success": True,
                "message": "항목을 성공적으로 수정했습니다",
                "data": item,
            }
        
        @self.router.delete(
            "/{id}",
            response_model=BaseResponseSchema[self.response_model],
            summary="항목 삭제",
            description="ID를 기준으로 항목을 삭제합니다.",
        )
        async def delete_item(
            id: int = Path(..., ge=1, description="항목 ID"),
            db: Session = Depends(get_db),
        ):
            """
            항목 삭제
            """
            item = self.service.remove(db=db, id=id)
            if not item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="항목을 찾을 수 없습니다",
                )
            return {
                "success": True,
                "message": "항목을 성공적으로 삭제했습니다",
                "data": item,
            } 