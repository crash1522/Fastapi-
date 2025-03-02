from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    """기본 API 예외 클래스"""
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundException(BaseAPIException):
    """리소스를 찾을 수 없을 때 발생하는 예외"""
    def __init__(
        self,
        detail: Any = "요청한 리소스를 찾을 수 없습니다",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, headers=headers)

class BadRequestException(BaseAPIException):
    """잘못된 요청일 때 발생하는 예외"""
    def __init__(
        self,
        detail: Any = "잘못된 요청입니다",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, headers=headers)

class UnauthorizedException(BaseAPIException):
    """인증되지 않은 요청일 때 발생하는 예외"""
    def __init__(
        self,
        detail: Any = "인증이 필요합니다",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, headers=headers)

class ForbiddenException(BaseAPIException):
    """권한이 없을 때 발생하는 예외"""
    def __init__(
        self,
        detail: Any = "접근 권한이 없습니다",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, headers=headers)

class InternalServerErrorException(BaseAPIException):
    """서버 내부 오류일 때 발생하는 예외"""
    def __init__(
        self,
        detail: Any = "서버 내부 오류가 발생했습니다",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, headers=headers) 