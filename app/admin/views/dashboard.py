from sqladmin import BaseView, expose
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database.session import get_db
from app.users.models.user import User

class DashboardView(BaseView):
    """대시보드 뷰"""
    
    name = "대시보드"
    icon = "fa-solid fa-gauge"
    
    @expose("/", methods=["GET"])
    def dashboard(self, request: Request):
        """대시보드 페이지"""
        db = next(get_db())
        
        # 사용자 통계
        total_users = db.query(func.count(User.id)).scalar()
        active_users = db.query(func.count(User.id)).filter(User.is_active == True).scalar()
        superusers = db.query(func.count(User.id)).filter(User.is_superuser == True).scalar()
        
        # 최근 가입한 사용자
        recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()
        
        return self.templates.TemplateResponse(
            "admin/dashboard.html",
            {
                "request": request,
                "stats": {
                    "total_users": total_users,
                    "active_users": active_users,
                    "superusers": superusers,
                },
                "recent_users": recent_users,
            },
        ) 