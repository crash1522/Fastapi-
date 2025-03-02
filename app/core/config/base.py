from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import secrets

class BaseAppSettings(BaseSettings):
    """기본 애플리케이션 설정 클래스
    
    모든 환경 설정의 기본이 되는 공통 설정 클래스입니다.
    """
    
    # 환경 설정
    ENV: str = os.getenv("ENV", "development")
    
    # 기본 API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Template"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",  # React 프론트엔드
    ]
    
    # 보안 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "11520"))  # 8일
    
    # 사용자 설정
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin@example.com")
    FIRST_SUPERUSER_USERNAME: str = os.getenv("FIRST_SUPERUSER_USERNAME", "admin")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "admin")
    USERS_OPEN_REGISTRATION: bool = os.getenv("USERS_OPEN_REGISTRATION", "True").lower() == "true"
    
    class Config:
        case_sensitive = True
        extra = "ignore"  # 추가 필드 무시 