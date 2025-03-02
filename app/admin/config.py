from sqladmin import Admin
from fastapi import FastAPI
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database.session import engine
from app.core.utils.security import get_current_active_superuser

class AdminConfig:
    """어드민 설정 클래스"""
    
    def __init__(self, app: FastAPI):
        self.app = app
        self.admin = Admin(
            app=app,
            engine=engine,
            title=f"{settings.PROJECT_NAME} 관리자",
            base_url="/admin",
            authentication_backend=self._get_auth_backend(),
        )
    
    def _get_auth_backend(self):
        """인증 백엔드 설정"""
        from sqladmin.authentication import AuthenticationBackend
        from fastapi import Request, Depends
        from fastapi.responses import RedirectResponse
        from app.core.utils.security import verify_password
        from app.users.services import user_service
        from app.core.database.session import get_db
        
        class AdminAuth(AuthenticationBackend):
            async def login(self, request: Request) -> bool:
                form = await request.form()
                username = form.get("username")
                password = form.get("password")
                
                # 세션 생성
                db = next(get_db())
                
                # 사용자 인증
                user = user_service.authenticate(db, email=username, password=password)
                
                # 관리자 권한 확인
                if user and user_service.is_superuser(user):
                    request.session.update({"user_id": user.id})
                    return True
                
                return False
            
            async def logout(self, request: Request) -> bool:
                request.session.clear()
                return True
            
            async def authenticate(self, request: Request) -> bool:
                user_id = request.session.get("user_id")
                if not user_id:
                    return False
                
                # 세션 생성
                db = next(get_db())
                
                # 사용자 조회
                user = user_service.get(db, id=user_id)
                
                # 관리자 권한 확인
                if user and user_service.is_superuser(user):
                    return True
                
                return False
        
        return AdminAuth(secret_key=settings.SECRET_KEY)
    
    def register_models(self, models: list[DeclarativeMeta]):
        """모델 등록"""
        for model in models:
            self.register_model(model)
    
    def register_model(self, model: DeclarativeMeta):
        """모델 등록"""
        from sqladmin import ModelView
        
        class ModelAdmin(ModelView):
            model = model
            name = model.__name__
            name_plural = f"{model.__name__}s"
            icon = "fa-solid fa-table"
            page_size = 25
            page_size_options = [25, 50, 100, 200]
        
        self.admin.add_view(ModelAdmin) 