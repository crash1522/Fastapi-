from sqladmin import ModelView
from wtforms import PasswordField, BooleanField, StringField
from wtforms.validators import DataRequired, Email, Optional

from app.users.models.user import User
from app.core.utils.security import get_password_hash

class UserAdmin(ModelView, model=User):
    """사용자 어드민 뷰"""
    
    name = "사용자"
    name_plural = "사용자 관리"
    icon = "fa-solid fa-users"
    category = "사용자 관리"
    column_list = [User.id, User.email, User.username, User.full_name, User.is_active, User.is_superuser, User.created_at]
    column_details_list = [User.id, User.email, User.username, User.full_name, User.is_active, User.is_superuser, User.created_at, User.updated_at]
    column_searchable_list = [User.email, User.username, User.full_name]
    column_sortable_list = [User.id, User.email, User.username, User.created_at]
    column_formatters = {
        User.is_active: lambda m, a: "활성" if m.is_active else "비활성",
        User.is_superuser: lambda m, a: "관리자" if m.is_superuser else "일반 사용자",
    }
    column_labels = {
        User.id: "ID",
        User.email: "이메일",
        User.username: "사용자명",
        User.full_name: "이름",
        User.is_active: "활성 상태",
        User.is_superuser: "관리자 여부",
        User.created_at: "생성일",
        User.updated_at: "수정일",
    }
    
    form_columns = [User.email, User.username, User.full_name, User.is_active, User.is_superuser]
    form_overrides = {
        "email": StringField,
        "username": StringField,
        "full_name": StringField,
        "is_active": BooleanField,
        "is_superuser": BooleanField,
    }
    form_args = {
        "email": {
            "label": "이메일",
            "validators": [DataRequired(), Email()],
        },
        "username": {
            "label": "사용자명",
            "validators": [DataRequired()],
        },
        "full_name": {
            "label": "이름",
            "validators": [Optional()],
        },
        "is_active": {
            "label": "활성 상태",
        },
        "is_superuser": {
            "label": "관리자 여부",
        },
    }
    
    def on_model_change(self, form, model, is_created):
        """모델 변경 시 처리"""
        # 비밀번호 해싱
        if is_created:
            model.hashed_password = get_password_hash("password")  # 기본 비밀번호 설정 