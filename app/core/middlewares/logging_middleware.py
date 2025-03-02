import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# 로거 설정
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """요청 및 응답 로깅을 위한 미들웨어"""
    
    async def dispatch(self, request: Request, call_next):
        # 요청 시작 시간
        start_time = time.time()
        
        # 요청 정보 로깅
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # 다음 미들웨어 또는 엔드포인트 호출
        response = await call_next(request)
        
        # 처리 시간 계산
        process_time = time.time() - start_time
        
        # 응답 정보 로깅
        logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
        
        return response 