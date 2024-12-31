# Django의 기본 사용자 모델과 관리자 모델을 상속
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# 커스텀 사용자 관리자 클래스
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not username:
            raise ValueError('사용자 이름은 필수 항목입니다.')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

# 커스텀 사용자 모델
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    
    # 필수 필드 추가
    is_active = models.BooleanField(default=True)  # 계정 활성화 여부
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()  # 커스텀 매니저 지정

    USERNAME_FIELD = 'username'  # 로그인 시 사용할 필드
    REQUIRED_FIELDS = ['email']  # 필수 입력 필드

    # 문자열 표현 메서드
    def __str__(self):
        return self.username