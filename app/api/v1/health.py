from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.supabase import get_supabase

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """
    서버 상태 확인 엔드포인트
    """
    return {"status": "ok", "message": "서버가 정상적으로 동작 중입니다"}

@router.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    """
    데이터베이스 연결 상태 확인 엔드포인트
    """
    try:
        # 간단한 쿼리 실행
        db.execute("SELECT 1")
        return {"status": "ok", "message": "데이터베이스 연결이 정상입니다"}
    except Exception as e:
        return {"status": "error", "message": f"데이터베이스 연결 오류: {str(e)}"}

@router.get("/health/supabase")
async def supabase_health_check():
    """
    Supabase 연결 상태 확인 엔드포인트
    """
    try:
        supabase = get_supabase()
        # 간단한 쿼리 실행
        response = supabase.table("health").select("*").limit(1).execute()
        return {"status": "ok", "message": "Supabase 연결이 정상입니다"}
    except Exception as e:
        return {"status": "error", "message": f"Supabase 연결 오류: {str(e)}"} 