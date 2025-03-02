from supabase import create_client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Supabase 클라이언트 생성
supabase = None
if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    try:
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("Supabase 클라이언트가 성공적으로 초기화되었습니다.")
    except Exception as e:
        logger.error(f"Supabase 클라이언트 초기화 중 오류 발생: {e}")
else:
    logger.warning("Supabase URL 또는 키가 설정되지 않았습니다. Supabase 기능이 비활성화됩니다.")

# 의존성 주입을 위한 Supabase 클라이언트 함수
def get_supabase():
    if supabase is None:
        logger.warning("Supabase 클라이언트가 초기화되지 않았습니다.")
    return supabase 