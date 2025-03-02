from typing import List, Optional
import os
from app.core.config.base import BaseAppSettings

class ProductionSettings(BaseAppSettings):
    """배포 환경 설정
    
    프로덕션 환경에서 사용되는 설정 클래스입니다.
    """
    
    # 서버 설정
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = False
    DEBUG: bool = False
    
    # 배포용 데이터베이스 설정
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/app")
    
    # Supabase 설정
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # 배포용 Redis 설정
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "")
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))
    
    # Celery 설정
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL", 
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND", 
        f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    )
    
    # 배포용 CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://yourdomain.com",
        "https://api.yourdomain.com",
        "https://app.yourdomain.com",
    ]
    
    class Config:
        env_file = ".env.production" 