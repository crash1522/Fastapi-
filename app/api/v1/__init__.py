from fastapi import APIRouter
from app.api.v1.endpoints import auth, tasks
from app.users.routers.user_router import router as user_router
from app.users.routers.supabase_users import router as supabase_user_router
from app.users.routers.supabase_auth import router as supabase_auth_router
from app.admin.routers import admin_router

# API v1 라우터
api_router = APIRouter()

# 라우터 등록
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Supabase 라우터 등록
api_router.include_router(supabase_auth_router, prefix="/supabase/auth", tags=["supabase-auth"])
api_router.include_router(supabase_user_router, prefix="/supabase/users", tags=["supabase-users"])

# 추가 라우터는 여기에 등록
# api_router.include_router(items_router, prefix="/items", tags=["items"]) 