import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1 import api_router
from app.core.config import settings
from app.core.middlewares.logging_middleware import LoggingMiddleware
from app.core.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    internal_server_error_exception_handler,
)
from app.core.exceptions import BaseAPIException
from app.core.database.session import Base, engine

# 로깅 설정
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """애플리케이션 생성 및 설정"""
    
    # FastAPI 앱 생성
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG,
    )
    
    # CORS 미들웨어 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 로깅 미들웨어 추가
    app.add_middleware(LoggingMiddleware)
    
    # 예외 핸들러 등록
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(BaseAPIException, http_exception_handler)
    
    # API 라우터 등록
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # 시작 및 종료 이벤트 등록
    @app.on_event("startup")
    async def startup_event():
        logger.info("애플리케이션 시작")
        # 데이터베이스 테이블 생성
        Base.metadata.create_all(bind=engine)
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("애플리케이션 종료")
    
    # 루트 엔드포인트
    @app.get("/")
    async def root():
        return {"message": f"Welcome to {settings.PROJECT_NAME}"}
    
    return app


app = create_app() 