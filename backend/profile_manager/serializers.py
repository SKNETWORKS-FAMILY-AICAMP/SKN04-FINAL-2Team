from rest_framework import serializers
from .models import ( Profile, ProfileData, TechStack, Career, 
                    AcademicRecord, Certificate, Language, Bookmark )    
from django.conf import settings

class ProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileData
        fields = ['profile', 'original_data', 'processed_data', 'pdf_data']

class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ['profile', 'tech_stack_name']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['profile', 'company_name', 'position', 'responsibilities', 'start_date', 'end_date', 'is_currently_employed', 'description']

class AcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicRecord
        fields = ['profile', 'school_name', 'major', 'status', 'enrollment_date', 'graduation_date']

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['profile', 'name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['profile', 'language_name', 'description']

class ProfileSerializer(serializers.ModelSerializer):
    profile_data = ProfileDataSerializer()
    tech_stacks = TechStackSerializer(many=True)
    careers = CareerSerializer(many=True)
    academic_records = AcademicRecordSerializer(many=True)
    certificates = CertificateSerializer(many=True)
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Profile
        fields = [
            'profile_id', 
            'name', 'job_category', 
            'career_year', 
            'profile_data', 
            'tech_stacks', 
            'careers', 
            'academic_records', 
            'certificates', 
            'languages'
        ]

class SimpleProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    career_year = serializers.SerializerMethodField()
    ai_analysis = serializers.SerializerMethodField() # AI 분석 결과(임시)
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['profile_id', 'name', 'job_category', 'career_year', 'ai_analysis', 'pdf_url']
    
    def get_name(self, obj):
        # obj는 Profile 모델의 인스턴스
        return obj.name

    def get_job_category(self, obj):
        return obj.job_category

    def get_career_year(self, obj):
        return obj.career_year
    
    # AI 분석 결과(임시)
    def get_ai_analysis(self, obj):
        ai_analysis = f'{obj.name}의 AI 분석 결과입니다.'
        return ai_analysis
    
    def get_pdf_url(self, obj):
        profile_data = obj.profile_data
        if profile_data and profile_data.pdf_data:
            # STORAGES 설정에서 custom_domain 가져오기
            custom_domain = settings.STORAGES['default']['OPTIONS']['custom_domain']
            # PDF 파일의 전체 URL 생성
            return f"https://{custom_domain}/{profile_data.pdf_data.name}"
        return None


class BookmarkedProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    career_year = serializers.SerializerMethodField()
    ai_analysis = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Bookmark  # Bookmark 모델 사용
        fields = ['profile_id', 'name', 'job_category', 'career_year', 'ai_analysis', 'pdf_url']
    
    def get_name(self, obj):
        # obj는 Bookmark 인스턴스이므로 profile 속성을 통해 Profile에 접근
        return obj.profile.name
    
    def get_job_category(self, obj):
        return obj.profile.job_category
    
    def get_career_year(self, obj):
        return obj.profile.career_year
    
    def get_ai_analysis(self, obj):
        ai_analysis = obj.ai_analysis
        return ai_analysis
    
    def get_pdf_url(self, obj):
        profile_data = obj.profile.profile_data
        if profile_data and profile_data.pdf_data:
            custom_domain = settings.STORAGES['default']['OPTIONS']['custom_domain']
            return f"https://{custom_domain}/{profile_data.pdf_data.name}"
        return None