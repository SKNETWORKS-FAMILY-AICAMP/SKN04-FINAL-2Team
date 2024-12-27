import os
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import transaction
from .models import (
    Profile, Career, AcademicRecord, Certificate, 
    Language, TechStack
)

class ProfileCreator:
    def __init__(self, origin_data, pdf_data, json_data):
        self.origin_data = origin_data
        self.pdf_data = pdf_data
        self.json_data = json_data
        self.profile = None

    @transaction.atomic
    def create_profile(self):
        """프로필 및 관련 정보를 생성하는 메인 메서드"""
        print("ProfileCreator 시작")
        self._create_base_profile()
        print("self._create_base_profile() 완료")
        self._create_tech_stacks()
        print("self._create_tech_stacks() 완료")
        self._create_careers()
        print("self._create_careers() 완료")
        self._create_academic_records()
        print("self._create_academic_records() 완료")
        self._create_certificates()
        print("self._create_certificates() 완료")
        self._create_languages()
        print("self._create_languages() 완료")
        return self.profile

    def _create_base_profile(self):
        """기본 프로필 생성"""
        profile_data = self.json_data.get('Profile', {})
        self.profile = Profile.objects.create(
            name=profile_data.get('name'),
            job_category=profile_data.get('job_category'),
            career_year=profile_data.get('career_year'),
            original_data=str(self.origin_data),  # 원본 데이터 저장
            processed_data=str(self.json_data)   # 처리된 데이터 저장
        )

    def _create_tech_stacks(self):
        """기술 스택 정보 생성"""
        for tech_data in self.json_data.get('TechStack', []):
            TechStack.objects.create(
                profile=self.profile,
                tech_stack_name=tech_data.get('tech_stack_name')
            )

    def _create_careers(self):
        """경력 정보 생성"""
        for career_data in self.json_data.get('Career', []):
            Career.objects.create(
                profile=self.profile,
                company_name=career_data.get('company_name'),
                position=career_data.get('position'),
                responsibilities=career_data.get('responsibilities'),
                start_date=career_data.get('start_date'),
                end_date=career_data.get('end_date'),
                is_currently_employed=career_data.get('is_currently_employed', False),
                description=career_data.get('description')
            )

    def _create_academic_records(self):
        """학력 정보 생성"""
        for academic_data in self.json_data.get('AcademicRecord', []):
            AcademicRecord.objects.create(
                profile=self.profile,
                school_name=academic_data.get('school_name'),
                major=academic_data.get('major'),
                status=academic_data.get('status'),
                enrollment_date=academic_data.get('enrollment_date'),
                graduation_date=academic_data.get('graduation_date')
            )

    def _create_certificates(self):
        """자격증 정보 생성"""
        for cert_data in self.json_data.get('Certificate', []):
            Certificate.objects.create(
                profile=self.profile,
                name=cert_data.get('name')
            )

    def _create_languages(self):
        """언어 능력 정보 생성"""
        for lang_data in self.json_data.get('Language', []):
            Language.objects.create(
                profile=self.profile,
                language_name=lang_data.get('language_name'),
                description=lang_data.get('description')
            )

def create_profile_from_json(json_data):
    """JSON 데이터를 받아서 프로필 및 관련 정보를 생성하는 함수"""
    creator = ProfileCreator(json_data)
    return creator.create_profile()