from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

# 모델 타입 변수
T = TypeVar("T")

class BaseSchema(BaseModel):
    """기본 스키마 클래스"""
    class Config:
        from_attributes = True
        populate_by_name = True

class IDSchema(BaseSchema):
    """ID 스키마 클래스"""
    id: int = Field(..., description="고유 식별자")

class TimestampSchema(BaseSchema):
    """타임스탬프 스키마 클래스"""
    created_at: Optional[datetime] = Field(None, description="생성 시간")
    updated_at: Optional[datetime] = Field(None, description="수정 시간")

class BaseResponseSchema(BaseSchema, Generic[T]):
    """기본 응답 스키마 클래스"""
    success: bool = Field(True, description="성공 여부")
    message: str = Field("성공적으로 처리되었습니다", description="응답 메시지")
    data: Optional[T] = Field(None, description="응답 데이터")

class PaginatedResponseSchema(BaseResponseSchema[List[T]]):
    """페이지네이션 응답 스키마 클래스"""
    total: int = Field(0, description="전체 항목 수")
    page: int = Field(1, description="현재 페이지")
    size: int = Field(10, description="페이지 크기")
    items: List[T] = Field([], description="항목 목록") 