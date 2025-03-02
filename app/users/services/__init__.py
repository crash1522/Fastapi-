from app.users.services.user_service import UserService
from app.users.repositories import user_repository

# 사용자 서비스 인스턴스 생성
user_service = UserService(repository=user_repository)

__all__ = ["user_service"] 