# Django의 기본 사용자 모델과 관리자 모델을 상속
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# 커스텀 사용자 관리자 클래스
class CustomUserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)  # 이메일 정규화
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해시화
        user.save(using=self._db)
        return user

    # 관리자 사용자 생성 메서드
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # 스태프 권한 부여
        extra_fields.setdefault('is_superuser', True)  # 슈퍼유저 권한 부여

        return self.create_user(username, email, password, **extra_fields)

# 커스텀 사용자 모델
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)  # 고유한 사용자 이름 필드
    email = models.EmailField(unique=True)  # 고유한 이메일 필드
    is_active = models.BooleanField(default=True)  # 계정 활성화 상태
    is_staff = models.BooleanField(default=False)  # 관리자 사이트 접근 권한
    is_host = models.BooleanField(default=False)  # 호스트 권한
    is_superuser = models.BooleanField(default=False)  # 최고 관리자 권한

    objects = CustomUserManager()  # 커스텀 매니저 지정

    USERNAME_FIELD = 'username'  # 로그인 시 사용할 필드
    REQUIRED_FIELDS = ['email']  # 필수 입력 필드

    # 문자열 표현 메서드
    def __str__(self):
        return self.username