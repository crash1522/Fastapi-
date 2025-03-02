from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import (
    BaseAPIException,
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    InternalServerErrorException,
)

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """요청 검증 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "message": "입력 데이터 검증에 실패했습니다"},
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """SQLAlchemy 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc), "message": "데이터베이스 오류가 발생했습니다"},
    )

async def http_exception_handler(request: Request, exc: BaseAPIException):
    """HTTP 예외 핸들러"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """404 Not Found 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail, "message": "요청한 리소스를 찾을 수 없습니다"},
    )

async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    """400 Bad Request 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.detail, "message": "잘못된 요청입니다"},
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    """401 Unauthorized 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.detail, "message": "인증이 필요합니다"},
    )

async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    """403 Forbidden 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail, "message": "접근 권한이 없습니다"},
    )

async def internal_server_error_exception_handler(request: Request, exc: InternalServerErrorException):
    """500 Internal Server Error 예외 핸들러"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.detail, "message": "서버 내부 오류가 발생했습니다"},
    ) 