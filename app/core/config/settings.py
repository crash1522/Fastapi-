import os
from dotenv import load_dotenv
from app.core.config.base import BaseAppSettings
from app.core.config.development import DevelopmentSettings
from app.core.config.production import ProductionSettings
from app.core.config.test import TestSettings

# 환경 변수 로드
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file)

def get_settings():
    """환경에 따른 설정 반환
    
    현재 환경에 맞는 설정 클래스의 인스턴스를 반환합니다.
    
    Returns:
        BaseAppSettings: 환경에 맞는 설정 클래스의 인스턴스
    """
    env = os.getenv("ENV", "development")
    
    if env == "production":
        return ProductionSettings()
    elif env == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()

# 설정 인스턴스 생성
settings = get_settings() 