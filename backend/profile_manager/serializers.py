from rest_framework import serializers
from .models import Profile, ProfileData, TechStack, Career, AcademicRecord, Certificate, Language

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

import random
# 프론트와의 통신을 위한 테스트용 데이터 생성
class SimpleProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    career_year = serializers.SerializerMethodField()
    ai_analysis = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['profile_id', 'name', 'job_category', 'career_year', 'ai_analysis']
        

    def get_name(self, obj):
        # 테스트용 임의 이름 반환
        test_names = ['김철수', '이영희', '박지민', '정민수']
        return random.choice(test_names)

    def get_job_category(self, obj):
        # 테스트용 직무 카테고리 반환
        test_categories = ['백엔드 개발자', '프론트엔드 개발자', '데이터 엔지니어', 'DevOps']
        return random.choice(test_categories)

    def get_career_year(self, obj):
        # 테스트용 경력 년수 반환
        return random.randint(0, 10)
    
    def get_ai_analysis(self, obj):
        # 테스트용 AI 분석 결과 반환
        test_analysis = ['AI 분석 결과 1', 'AI 분석 결과 2', 'AI 분석 결과 3', 'AI 분석 결과 4']
        return random.choice(test_analysis)
    

class BookmarkedProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    job_category = serializers.SerializerMethodField()
    career_year = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()    
    
    class Meta:
        model = Profile
        fields = ['profile_id', 'name', 'job_category', 'career_year', 'is_bookmarked']

    def get_bookmarked_profiles(self):
        # return Profile.objects.filter(is_bookmarked=True)
        return True
    
    def get_name(self, obj):
        # 테스트용 임의 이름 반환
        test_names = ['김철수', '이영희', '박지민', '정민수']
        return random.choice(test_names)

    def get_job_category(self, obj):
        # 테스트용 직무 카테고리 반환
        test_categories = ['백엔드 개발자', '프론트엔드 개발자', '데이터 엔지니어', 'DevOps']
        return random.choice(test_categories)

    def get_career_year(self, obj):
        # 테스트용 경력 년수 반환
        return random.randint(0, 10)
