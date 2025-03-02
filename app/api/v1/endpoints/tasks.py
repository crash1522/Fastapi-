from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel

from app.core.tasks import example_task, process_data, cleanup
from app.core.utils.security import get_current_active_user
from app.users.models.user import User

router = APIRouter()


class TaskRequest(BaseModel):
    """태스크 요청 모델"""
    word: str


class DataProcessRequest(BaseModel):
    """데이터 처리 요청 모델"""
    data: Dict[str, Any]


class TaskResponse(BaseModel):
    """태스크 응답 모델"""
    task_id: str
    message: str


@router.post("/example", response_model=TaskResponse)
def run_example_task(
    request: TaskRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    예제 태스크 실행
    """
    try:
        task = example_task.delay(request.word)
        return {
            "task_id": task.id,
            "message": f"태스크가 성공적으로 시작되었습니다. 태스크 ID: {task.id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"태스크 실행 중 오류 발생: {str(e)}"
        )


@router.post("/process-data", response_model=TaskResponse)
def run_process_data_task(
    request: DataProcessRequest,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    데이터 처리 태스크 실행
    """
    try:
        task = process_data.delay(request.data)
        return {
            "task_id": task.id,
            "message": f"데이터 처리 태스크가 성공적으로 시작되었습니다. 태스크 ID: {task.id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"태스크 실행 중 오류 발생: {str(e)}"
        )


@router.post("/cleanup", response_model=TaskResponse)
def run_cleanup_task(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    정리 작업 태스크 실행
    """
    try:
        task = cleanup.delay()
        return {
            "task_id": task.id,
            "message": f"정리 작업 태스크가 성공적으로 시작되었습니다. 태스크 ID: {task.id}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"태스크 실행 중 오류 발생: {str(e)}"
        )


@router.get("/status/{task_id}", response_model=Dict[str, Any])
def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    태스크 상태 확인
    """
    from app.core.celery_app import celery_app
    
    try:
        task = celery_app.AsyncResult(task_id)
        response = {
            "task_id": task_id,
            "status": task.status,
        }
        
        if task.status == "SUCCESS":
            response["result"] = task.result
        elif task.status == "FAILURE":
            response["error"] = str(task.result)
        
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"태스크 상태 확인 중 오류 발생: {str(e)}"
        ) 