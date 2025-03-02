# Supabase 사용 가이드

이 가이드는 FastAPI 템플릿 프로젝트에서 Supabase를 설정하고 사용하는 방법을 설명합니다.

## Supabase란?

Supabase는 Firebase의 오픈 소스 대안으로, PostgreSQL 데이터베이스를 기반으로 한 백엔드 서비스입니다. 다음과 같은 기능을 제공합니다:

- 데이터베이스: PostgreSQL 데이터베이스
- 인증: 사용자 인증 및 권한 관리
- 스토리지: 파일 저장 및 관리
- 실시간 구독: 실시간 데이터 업데이트
- Edge Functions: 서버리스 함수

## 설정 방법

### 1. Supabase 계정 생성 및 프로젝트 설정

1. [Supabase 웹사이트](https://supabase.com/)에서 계정을 생성합니다.
2. 새 프로젝트를 생성합니다.
3. 프로젝트 설정에서 API URL과 API 키를 확인합니다.

### 2. 환경 변수 설정

`.env.development` 파일에 Supabase URL과 API 키를 설정합니다:

```
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your-supabase-key
```

### 3. 테이블 생성

Supabase 대시보드의 SQL 에디터에서 `scripts/create_supabase_tables.sql` 스크립트를 실행하여 필요한 테이블을 생성합니다.

## 사용 방법

### 1. Supabase 클라이언트 초기화

Supabase 클라이언트는 `app/core/database/supabase.py`에서 초기화됩니다. 환경 변수가 올바르게 설정되어 있으면 자동으로 초기화됩니다.

### 2. Supabase 기반 API 엔드포인트

다음 API 엔드포인트를 사용하여 Supabase 기반 기능을 사용할 수 있습니다:

- `/api/v1/supabase/auth/login` - 로그인
- `/api/v1/supabase/auth/register` - 회원가입
- `/api/v1/supabase/users/me` - 현재 사용자 정보
- `/api/v1/supabase/users/{user_id}` - 특정 사용자 정보

### 3. 의존성 주입

Supabase 기반 기능을 사용하려면 다음과 같은 의존성 주입 함수를 사용합니다:

```python
from app.users.dependencies import (
    get_current_supabase_user,
    get_current_active_supabase_user,
    get_current_active_supabase_superuser,
    get_supabase_user_service,
)
```

### 4. 사용자 인증

Supabase 기반 사용자 인증은 다음과 같이 사용합니다:

```python
@router.get("/protected-route")
def protected_route(
    current_user: dict = Depends(get_current_active_supabase_user),
) -> Any:
    """
    인증된 사용자만 접근 가능한 라우트
    """
    return {"message": "인증 성공", "user": current_user}
```

### 5. 관리자 권한

관리자 권한이 필요한 라우트는 다음과 같이 설정합니다:

```python
@router.get("/admin-route")
def admin_route(
    current_user: dict = Depends(get_current_active_supabase_superuser),
) -> Any:
    """
    관리자만 접근 가능한 라우트
    """
    return {"message": "관리자 인증 성공", "user": current_user}
```

## SQLAlchemy와 Supabase 함께 사용하기

이 프로젝트는 SQLAlchemy와 Supabase를 함께 사용할 수 있습니다. 필요에 따라 적절한 저장소와 서비스를 선택하여 사용하세요.

### SQLAlchemy 사용 예시

```python
from app.users.dependencies import get_current_active_user, get_user_service

@router.get("/sqlalchemy-route")
def sqlalchemy_route(
    current_user = Depends(get_current_active_user),
    service = Depends(get_user_service),
) -> Any:
    # SQLAlchemy 기반 코드
    return {"message": "SQLAlchemy 사용"}
```

### Supabase 사용 예시

```python
from app.users.dependencies import get_current_active_supabase_user, get_supabase_user_service
from app.core.database.supabase import get_supabase

@router.get("/supabase-route")
def supabase_route(
    current_user: dict = Depends(get_current_active_supabase_user),
    service = Depends(get_supabase_user_service),
) -> Any:
    supabase = get_supabase()
    # Supabase 기반 코드
    return {"message": "Supabase 사용"}
```

## 추가 리소스

- [Supabase 공식 문서](https://supabase.com/docs)
- [Supabase Python 클라이언트 문서](https://supabase.com/docs/reference/python/introduction)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/) 