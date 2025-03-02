import logging
from sqlalchemy.orm import Session

from app.core.config import settings
from app.users.schemas.user import UserCreate
from app.users.services import user_service

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    데이터베이스 초기화 함수
    - 초기 관리자 사용자 생성
    """
    # 초기 관리자 사용자 생성
    create_first_superuser(db)


def create_first_superuser(db: Session) -> None:
    """
    초기 관리자 사용자 생성 함수
    """
    # 관리자 사용자 설정 확인
    if not settings.FIRST_SUPERUSER:
        logger.warning("초기 관리자 사용자 이메일이 설정되지 않았습니다. 관리자 사용자를 생성하지 않습니다.")
        return

    # 이미 존재하는지 확인
    user = user_service.get_user_by_email(db, email=settings.FIRST_SUPERUSER)
    if user:
        logger.info(f"관리자 사용자가 이미 존재합니다: {settings.FIRST_SUPERUSER}")
        return

    # 관리자 사용자 생성
    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER,
        username=settings.FIRST_SUPERUSER_USERNAME,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
        full_name="관리자",
    )

    try:
        user = user_service.create_user(db, user_in=user_in)
        logger.info(f"관리자 사용자가 생성되었습니다: {settings.FIRST_SUPERUSER}")
    except Exception as e:
        logger.error(f"관리자 사용자 생성 중 오류 발생: {e}") 