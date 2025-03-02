import os
import logging
from dotenv import load_dotenv

# 환경 변수 로드
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Redis 연결 정보 로깅
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_db = os.getenv("REDIS_DB", "0")
broker_url = os.getenv("CELERY_BROKER_URL", f"redis://{redis_host}:{redis_port}/{redis_db}")
result_backend = os.getenv("CELERY_RESULT_BACKEND", f"redis://{redis_host}:{redis_port}/{redis_db}")

logger.info(f"Redis 연결 정보: 호스트={redis_host}, 포트={redis_port}, DB={redis_db}")
logger.info(f"Celery 브로커 URL: {broker_url}")
logger.info(f"Celery 결과 백엔드: {result_backend}")

# 환경 변수 설정
os.environ["CELERY_BROKER_URL"] = broker_url
os.environ["CELERY_RESULT_BACKEND"] = result_backend

# Celery 앱 가져오기
from app.core.celery_app import celery_app

if __name__ == "__main__":
    logger.info("Celery 워커 시작")
    # 워커 실행 (기본 풀 사용)
    celery_app.worker_main(["worker", "--loglevel=info"]) 