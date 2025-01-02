from django.contrib import admin
from .models import (
    Profile, TechStack, Career, AcademicRecord, Certificate, 
    Language, ProfileData, Bookmark
)
from django.core.management import call_command
from django.contrib import messages

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'name', 'job_category', 'career_year')
    search_fields = ('name', 'job_category')
    list_filter = ('job_category',)

@admin.register(ProfileData)
class ProfileDataAdmin(admin.ModelAdmin):
    list_display = ('profile', 'original_data', 'processed_data', 'pdf_data')
    search_fields = ('profile__name',)

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('profile', 'tech_stack_name')
    search_fields = ('tech_stack_name',)
    list_filter = ('tech_stack_name',)

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company_name', 'position', 'start_date', 'end_date', 'is_currently_employed')
    search_fields = ('company_name', 'position')
    list_filter = ('is_currently_employed', 'start_date', 'end_date')

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('profile', 'school_name', 'major', 'status', 'enrollment_date', 'graduation_date')
    search_fields = ('school_name', 'major')
    list_filter = ('status', 'enrollment_date', 'graduation_date')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name')
    search_fields = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'language_name', 'description')
    search_fields = ('language_name',)
    list_filter = ('language_name',)

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'created_at')  # 관리자 목록에서 표시할 필드
    list_filter = ('created_at',)  # 필터 옵션
    search_fields = ('user__username', 'profile__name')  # 검색 필드
    date_hierarchy = 'created_at'  # 날짜 기반 계층 구조
    ordering = ('-created_at',)  # 최신 북마크가 위에 오도록 정렬