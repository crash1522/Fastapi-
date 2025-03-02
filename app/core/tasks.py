import logging
from celery import shared_task
from typing import Any, Dict, List, Optional
import time

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    name="app.core.tasks.example_task"
)
def example_task(self, word: str) -> str:
    """
    예제 태스크
    
    Args:
        word: 처리할 단어
        
    Returns:
        처리 결과 메시지
    """
    try:
        logger.info(f"태스크 시작: {word}")
        # 태스크 처리 시간 시뮬레이션
        time.sleep(2)
        result = f"처리된 단어: {word.upper()}"
        logger.info(f"태스크 완료: {result}")
        return result
    except Exception as e:
        logger.error(f"태스크 실패: {str(e)}")
        raise

@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="app.core.tasks.process_data"
)
def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    데이터 처리 태스크
    
    Args:
        data: 처리할 데이터
        
    Returns:
        처리 결과
    """
    try:
        logger.info(f"데이터 처리 시작: {data}")
        # 데이터 처리 로직
        result = {
            "processed": True,
            "input": data,
            "timestamp": time.time()
        }
        logger.info(f"데이터 처리 완료: {result}")
        return result
    except Exception as e:
        logger.error(f"데이터 처리 실패: {str(e)}")
        raise

@shared_task(
    bind=True,
    name="app.core.tasks.cleanup"
)
def cleanup(self) -> str:
    """
    정기적인 정리 작업을 수행하는 태스크
    
    Returns:
        작업 결과 메시지
    """
    try:
        logger.info("정리 작업 시작")
        # 정리 작업 로직
        time.sleep(5)
        logger.info("정리 작업 완료")
        return "정리 작업이 성공적으로 완료되었습니다."
    except Exception as e:
        logger.error(f"정리 작업 실패: {str(e)}")
        raise 