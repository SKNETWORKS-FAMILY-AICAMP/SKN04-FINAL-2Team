from pathlib import Path
from datetime import timedelta

# 프로젝트 기본 경로 설정: BASE_DIR / 'subdir' 형태로 경로 생성
BASE_DIR = Path(__file__).resolve().parent.parent

# 개발 단계 빠른 시작 설정 - 실제 운영에는 부적합
# 참고: https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = "django-insecure-^6kb6&sb)nm)tpxkgdasm(=1(4hc*miolkv_bbxh2n%-4k!fzh"

# 보안 경고: 프로덕션 환경에서는 디버그 모드를 비활성화해야 함
DEBUG = True

# 모든 호스트 허용 (개발 환경용)
ALLOWED_HOSTS = ['*']

# 설치된 앱 목록
INSTALLED_APPS = [
    # Django 기본 앱
    "django.contrib.admin",  # 관리자 인터페이스
    "django.contrib.auth",   # 인증 시스템
    "django.contrib.contenttypes",  # 컨텐츠 타입 프레임워크
    "django.contrib.sessions",      # 세션 프레임워크
    "django.contrib.messages",      # 메시징 프레임워크
    "django.contrib.staticfiles",   # 정적 파일 관리
    
    # REST 프레임워크 관련
    "rest_framework",              # DRF 기본
    "rest_framework.authtoken",    # 토큰 인증
    "rest_framework_simplejwt",    # JWT 인증
    
    # 인증 관련
    'django.contrib.sites',        # allauth에 필요한 사이트 프레임워크
    'allauth',                    # allauth 기본
    'allauth.account',            # allauth 계정 관리
    
    # 추가 기능
    "corsheaders",                # CORS 지원
    "django_extensions",          # Django 확장 기능
    
    # 커스텀 앱
    "accounts",                   # 계정 관리 앱
    "profile_manager",            # 프로필 관리 앱
]

# REST 프레임워크 설정
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT 인증 클래스 추가
    ]
}

# JWT 사용 설정
REST_USE_JWT = True

# Django sites 프레임워크 설정
SITE_ID = 1  # 사이트 ID 설정

# 미들웨어 설정
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 미들웨어
    "django.middleware.security.SecurityMiddleware",  # 보안 미들웨어
    "django.contrib.sessions.middleware.SessionMiddleware",  # 세션 미들웨어
    "django.middleware.common.CommonMiddleware",  # 공통 미들웨어
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF 보호 미들웨어
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # 인증 미들웨어
    "django.contrib.messages.middleware.MessageMiddleware",  # 메시지 미들웨어
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # 클릭재킹 보호 미들웨어
    "allauth.account.middleware.AccountMiddleware",  # allauth 계정 미들웨어
]

# JWT 설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15), # 15분
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3), # 3일
    'ROTATE_REFRESH_TOKENS': True, # 리프레시 토큰 재발급
    'BLACKLIST_AFTER_ROTATION': True, # 리프레시 토큰 블랙리스트
}

AUTH_USER_MODEL = 'accounts.CustomUser'  # 커스텀 유저 모델 지정

# URL 설정
ROOT_URLCONF = "backend.urls"

# 템플릿 설정
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Django 템플릿 엔진 사용
        "DIRS": [BASE_DIR/"templates"],  # 템플릿 디렉토리 목록
        "APP_DIRS": True,  # 앱 디렉토리에서 템플릿 검색 활성화
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # 디버그 관련 컨텍스트
                "django.template.context_processors.request",  # 요청 관련 컨텍스트
                "django.contrib.auth.context_processors.auth",  # 인증 관련 컨텍스트
                "django.contrib.messages.context_processors.messages",  # 메시지 관련 컨텍스트
            ],
        },
    },
]

# WSGI 애플리케이션 설정
WSGI_APPLICATION = "backend.wsgi.application"

# 데이터베이스 설정
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # SQLite3 사용
        "NAME": BASE_DIR / "db.sqlite3",        # 데이터베이스 파일 위치
    }
}

# 비밀번호 검증 설정
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # 사용자 속성 유사성 검사
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # 최소 길이 검사
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # 일반적인 비밀번호 검사
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # 숫자로만 이루어진 비밀번호 검사
    },
]

# 국제화 설정
LANGUAGE_CODE = "ko-kr"  # 기본 언어 설정

TIME_ZONE = "Asia/Seoul"        # 시간대 설정

USE_I18N = True         # 국제화 기능 사용

USE_TZ = True          # 시간대 기능 사용

# 정적 파일 설정 (CSS, JavaScript, Images)
STATIC_URL = "static/"

# 기본 프라이머리 키 필드 타입 설정
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True    # 모든 도메인에서의 CORS 요청 허용
CORS_ALLOW_CREDENTIALS = True   # 인증된 요청(쿠키, 인증 헤더 등) 허용
