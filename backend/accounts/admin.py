# Django 관리자 기능과 사용자 관리를 위한 임포트
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# 커스텀 사용자 관리자 클래스 정의
class CustomUserAdmin(UserAdmin):
    model = CustomUser  # 사용할 모델 지정
    # 관리자 목록에 표시할 필드들
    list_display = ('email', 'is_staff', 'is_active', 'is_host', 'is_superuser')
    # 필터링 가능한 필드들
    list_filter = ('is_staff', 'is_active', 'is_host', 'is_superuser')
    # 사용자 수정 시 표시될 필드 그룹
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_host', 'is_superuser')}),
    )
    # 사용자 추가 시 표시될 필드 그룹
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_host', 'is_superuser')}
        ),
    )
    # 검색 가능한 필드
    search_fields = ('email',)
    # 정렬 기준 필드
    ordering = ('email',)

# 커스텀 사용자 모델을 관리자 사이트에 등록
admin.site.register(CustomUser, CustomUserAdmin)