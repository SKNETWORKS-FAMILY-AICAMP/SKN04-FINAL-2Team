from django.contrib import admin
from .models import Profile, TechStack, Career, AcademicRecord, Certificate, Language

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'name', 'job_category', 'career_year')
    search_fields = ('name', 'job_category')
    list_filter = ('job_category',)
    # 리스트 페이지에서 선택한 항목들을 삭제할 수 있는 액션 활성화
    actions = ['delete_selected']

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