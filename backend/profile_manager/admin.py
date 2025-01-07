from django.contrib import admin
from .models import (
    Profile, TechStack, Career, AcademicRecord, Certificate, 
    Language, ProfileData, Bookmark, Company
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'name', 'job_category', 'career_year')
    search_fields = ('name', 'job_category', 'career_year')
    list_filter = ('job_category', 'career_year')

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
    list_display = ('profile', 'company_name', 'position', 'career_start_date', 'career_end_date', 'is_currently_employed')
    search_fields = ('company_name', 'position')
    list_filter = ('is_currently_employed',)

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('profile', 'school_name', 'major', 'degree', 'enrollment_date', 'graduation_date')
    search_fields = ('school_name', 'major', 'degree')
    list_filter = ('degree',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('profile', 'certificate_name')
    search_fields = ('certificate_name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'language_name', 'lank', 'language_description')
    search_fields = ('language_name', 'lank')
    list_filter = ('language_name', 'lank')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile', 'ai_analysis', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'profile__name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'is_major_company', 'establishment_date', 'investment_scale')
    list_filter = ('is_major_company', 'establishment_date', 'investment_scale')
    search_fields = ('company_name',)