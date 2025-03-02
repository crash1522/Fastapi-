from celery import Celery
from app.core.config import settings
import os

# 환경 변수에서 직접 가져오기
broker_url = os.getenv("CELERY_BROKER_URL", f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/{os.getenv('REDIS_DB', '0')}")
result_backend = os.getenv("CELERY_RESULT_BACKEND", f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/{os.getenv('REDIS_DB', '0')}")

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=result_backend,
    include=["app.core.tasks"],
)

# Celery 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=False,
    worker_concurrency=4,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
)

# 태스크 라우팅 설정
celery_app.conf.task_routes = {
    "app.core.tasks.*": {"queue": "default"},
}

# 태스크 기본 큐 설정
celery_app.conf.task_default_queue = "default"

# 주기적 태스크 설정 (선택 사항)
celery_app.conf.beat_schedule = {
    # 예: 매일 자정에 실행되는 태스크
    # "cleanup-every-midnight": {
    #     "task": "app.core.tasks.cleanup",
    #     "schedule": 86400.0,  # 24시간마다
    # },
}

# Celery 시작 시 실행할 함수
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # 여기에 주기적 태스크 설정 코드 추가
    pass 