from typing import Optional
import os
from app.core.config.base import BaseAppSettings

class TestSettings(BaseAppSettings):
    """테스트 환경 설정
    
    테스트 환경에서 사용되는 설정 클래스입니다.
    """
    
    # 서버 설정
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = True
    DEBUG: bool = True
    TESTING: bool = True
    
    # 테스트용 데이터베이스 설정
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Supabase 설정
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    # 테스트용 Redis 설정
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 1
    
    # Celery 설정
    CELERY_BROKER_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    CELERY_RESULT_BACKEND: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    
    class Config:
        env_file = ".env.test"