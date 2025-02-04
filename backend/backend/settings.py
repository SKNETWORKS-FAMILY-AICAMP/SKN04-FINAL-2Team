from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
import boto3

load_dotenv()
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
    "storages",
    
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
    # Access Token의 유효 시간 (5분 동안 유효)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Refresh Token의 유효 시간 (1일 동안 유효)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    
    # Refresh Token 재발급 시 새로운 토큰으로 교체 여부 (False: 교체하지 않음)
    "ROTATE_REFRESH_TOKENS": False,
    
    # Refresh Token이 교체될 때 이전 토큰을 블랙리스트에 추가할지 여부 (False: 추가하지 않음)
    "BLACKLIST_AFTER_ROTATION": False,
    
    # 마지막 로그인 시간을 업데이트할지 여부 (False: 업데이트하지 않음)
    "UPDATE_LAST_LOGIN": False,

    # 토큰 서명에 사용할 알고리즘 (HS256: 대칭키 알고리즘)
    "ALGORITHM": "HS256",
    
    # 토큰 서명에 사용할 비밀 키 (Django의 SECRET_KEY 사용)
    "SIGNING_KEY": SECRET_KEY,
        
    # 토큰 수신자(Audience) 검증 (None: 검증하지 않음)
    "AUDIENCE": None,
    
    # 토큰 발급자(Issuer) 검증 (None: 검증하지 않음)
    "ISSUER": None,
    
    # JSON 인코더 클래스 (None: 기본 인코더 사용)
    "JSON_ENCODER": None,
    
    # JSON Web Key Set URL (None: 사용하지 않음)
    "JWK_URL": None,
    
    # 토큰 만료 시간에 대한 허용 오차 (초 단위, 기본값: 0)
    "LEEWAY": 0,

    # HTTP Authorization 헤더에서 사용할 타입 (Bearer)
    "AUTH_HEADER_TYPES": ("Bearer",),
    
    # HTTP 요청에서 인증 정보를 가져올 헤더 키
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    
    # 사용자 모델의 ID 필드 (id 사용)
    "USER_ID_FIELD": "id",
    
    # JWT Payload에서 사용자 ID를 나타내는 클레임
    "USER_ID_CLAIM": "user_id",
    
    # 사용자 인증 규칙을 정의하는 함수
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    # 사용할 토큰 클래스 (기본 AccessToken 사용)
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
        
    # 토큰을 통해 사용자 객체를 나타낼 때 사용할 클래스
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # JWT 토큰의 고유 식별자 (jti: 토큰의 고유 ID)
    "JTI_CLAIM": "jti",

    # Sliding Token에서 Refresh 만료 시간을 나타내는 클레임
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    
    # Sliding Access Token의 유효 시간 (5분)
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=60),
    
    # Sliding Refresh Token의 유효 시간 (1일)
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    # Access & Refresh Token을 발급하는 Serializer
    "TOKEN_OBTAIN_SERIALIZER": "accounts.serializers.CustomTokenObtainPairSerializer",
    
    # Refresh Token으로 Access Token을 재발급하는 Serializer
    "TOKEN_REFRESH_SERIALIZER": "accounts.serializers.CustomTokenRefreshSerializer",
    
    # JWT 토큰의 유효성을 검증하는 Serializer
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    
    # 블랙리스트에 토큰을 등록하는 Serializer
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    
    # Sliding Token을 발급하는 Serializer
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    
    # Sliding Refresh Token으로 새로운 Sliding Token을 발급하는 Serializer
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
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
        "ENGINE": os.getenv('DB_ENGINE'),  # PostgreSQL 사용
        "NAME": os.getenv('DB_NAME'),               # 데이터베이스 이름
        "USER": os.getenv('DB_USER'),               # 데이터베이스 사용자
        "PASSWORD": os.getenv('DB_PASSWORD'),       # 데이터베이스 비밀번호
        "HOST": os.getenv('DB_HOST'),               # 데이터베이스 호스트 (로컬일 경우 'localhost')
        "PORT": os.getenv('DB_PORT'),               # 데이터베이스 포트 (기본값: 5432)
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv('AWS_ACCESS_KEY_ID'),
            "secret_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
            "bucket_name": os.getenv('AWS_STORAGE_BUCKET_NAME'),
            "region_name": os.getenv('AWS_S3_REGION_NAME'),
            "custom_domain": f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
            "file_overwrite": True,
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
# 미디어 파일 URL
MEDIA_URL = f'https://{os.getenv("AWS_STORAGE_BUCKET_NAME")}.s3.amazonaws.com/'

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
# 쿠키 옵션
# SESSION_COOKIE_SAMESITE = 'Lax'  # Lax로 설정 (Strict는 제한적)
# SESSION_COOKIE_SECURE = False  # 개발 환경에서는 False
# CSRF_COOKIE_SAMESITE = 'Lax'
# CSRF_COOKIE_SECURE = False

