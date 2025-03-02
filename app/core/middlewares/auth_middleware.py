from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from app.core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    """인증 미들웨어"""
    
    async def dispatch(self, request: Request, call_next):
        # 인증이 필요 없는 경로 목록
        public_paths = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/health",
            "/api/v1/health/db",
            "/api/v1/health/supabase",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
        ]
        
        # 현재 경로가 인증이 필요 없는 경로인지 확인
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Authorization 헤더 확인
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증 정보가 없습니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Bearer 토큰 확인
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="유효하지 않은 인증 방식입니다",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # 토큰 검증
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            
            # 요청 상태에 사용자 정보 저장
            request.state.user_id = payload.get("sub")
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 다음 미들웨어 또는 엔드포인트 호출
        return await call_next(request) 