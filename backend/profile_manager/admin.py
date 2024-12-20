from django.contrib import admin
from .models import (Profile, Profile_Detail, Skill, Career, Activity, 
                    AcademicBackground, ParticipatedProject, Certificate, 
                    EducationContent, URL, Language, LLM_Data)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('profile_id', 'name', 'job', 'email', 'phone')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('job',)

@admin.register(Profile_Detail)
class ProfileDetailAdmin(admin.ModelAdmin):
    list_display = ('profile', 'brief_introduction', 'created_at', 'updated_at')
    search_fields = ('profile__name', 'brief_introduction')
    list_filter = ('created_at', 'updated_at')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name')
    search_fields = ('name',)

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company_name', 'position', 'start_date', 'end_date')
    search_fields = ('company_name', 'position')
    list_filter = ('employment_type', 'start_date', 'end_date')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('profile', 'activity_name', 'organization_name', 'activity_year')
    search_fields = ('activity_name', 'organization_name')
    list_filter = ('activity_year',)

@admin.register(AcademicBackground)
class AcademicBackgroundAdmin(admin.ModelAdmin):
    list_display = ('profile', 'school_name', 'major', 'status', 'start_date', 'end_date')
    search_fields = ('school_name', 'major')
    list_filter = ('status', 'start_date', 'end_date')

@admin.register(ParticipatedProject)
class ParticipatedProjectAdmin(admin.ModelAdmin):
    list_display = ('profile', 'project_name', 'project_role', 'organization_name', 'start_date', 'end_date')
    search_fields = ('project_name', 'organization_name')
    list_filter = ('start_date', 'end_date')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('profile', 'name', 'acquisition_date', 'issuing_org')
    search_fields = ('name', 'issuing_org')
    list_filter = ('acquisition_date',)

@admin.register(EducationContent)
class EducationContentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'education_name', 'description')
    search_fields = ('education_name',)

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('profile', 'link')
    search_fields = ('link',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'description')
    search_fields = ('description',)

@admin.register(LLM_Data)
class LLM_DataAdmin(admin.ModelAdmin):
    list_display = ('profile', 'original_data', 'processed_data')
    search_fields = ('original_data', 'processed_data')