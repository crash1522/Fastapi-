# FastAPI 템플릿 프로젝트

이 프로젝트는 FastAPI를 사용한 웹 애플리케이션 개발을 위한 템플릿입니다. SQLAlchemy ORM과 Supabase를 모두 지원하여 다양한 백엔드 옵션을 제공합니다.

## 기능

- FastAPI 기반 RESTful API
- SQLAlchemy ORM을 통한 데이터베이스 연동
- Supabase 통합 지원
- Celery를 이용한 비동기 작업 처리
- Redis를 이용한 캐싱 및 메시지 큐
- Docker 및 Docker Compose를 통한 컨테이너화
- 사용자 인증 및 권한 관리
- 관리자 기능

## 시작하기

### 필수 조건

- Docker 및 Docker Compose
- Python 3.9 이상 (로컬 개발 시)
- Poetry (의존성 관리)

### 설치 및 실행

1. 저장소 클론

```bash
git clone <repository-url>
cd fastapi_template_ver1
```

2. 환경 변수 설정

`.env.development` 파일을 수정하여 필요한 환경 변수를 설정합니다.

```
# Supabase 설정 (Supabase 사용 시)
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your-supabase-key
```

3. Docker Compose로 실행

```bash
docker compose up -d
```

4. API 문서 접속

브라우저에서 `http://localhost:8000/docs`로 접속하여 API 문서를 확인할 수 있습니다.

## 프로젝트 구조

```
app/
├── api/                  # API 엔드포인트
│   └── v1/               # API 버전 1
├── core/                 # 핵심 기능 및 설정
│   ├── config/           # 설정
│   ├── database/         # 데이터베이스 연결 및 모델
│   ├── repositories/     # 저장소 패턴 구현
│   └── utils/            # 유틸리티 함수
├── users/                # 사용자 관련 기능
│   ├── models/           # 사용자 모델
│   ├── repositories/     # 사용자 저장소
│   ├── routers/          # 사용자 라우터
│   ├── schemas/          # 사용자 스키마
│   └── services/         # 사용자 서비스
└── admin/                # 관리자 기능
```

## Supabase 통합

이 프로젝트는 Supabase를 통한 데이터 관리를 지원합니다. Supabase를 사용하려면:

1. Supabase 계정 생성 및 프로젝트 설정
2. `.env.development` 파일에 Supabase URL과 API 키 설정
3. Supabase 기반 API 엔드포인트 사용:
   - `/api/v1/supabase/auth/login` - 로그인
   - `/api/v1/supabase/auth/register` - 회원가입
   - `/api/v1/supabase/users/me` - 현재 사용자 정보

## SQLAlchemy vs Supabase

이 프로젝트는 두 가지 데이터 액세스 방식을 지원합니다:

1. **SQLAlchemy ORM**: 로컬 또는 자체 호스팅 데이터베이스를 사용할 때 적합
2. **Supabase**: 클라우드 기반 PostgreSQL 데이터베이스와 추가 기능(인증, 스토리지 등)을 활용하고 싶을 때 적합

필요에 따라 두 방식을 선택하거나 혼합하여 사용할 수 있습니다.

## 라이선스

MIT
