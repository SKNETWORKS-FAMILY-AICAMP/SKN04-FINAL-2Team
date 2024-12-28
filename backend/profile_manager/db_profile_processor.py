import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.exceptions import ValidationError

from django.db import transaction
from .models import (
    Profile, Career, AcademicRecord, Certificate, 
    Language, TechStack, ProfileData
)


class ProfileCreator:
    def __init__(self, page_id, resume_id, json_data:dict):
        self.page_id = page_id
        self.resume_id = resume_id
        self.json_data = json_data
        self.profile = None

    # 예외 처리 데코레이터
    def exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"{func.__name__} 오류: {str(e)}")
        return wrapper
    
    # 트랜잭션 처리
    @transaction.atomic
    def create_profile(self):
        """프로필 및 관련 정보를 생성하는 메인 메서드"""
        self._create_base_profile()
        self._create_profile_data()
        self._create_tech_stacks()
        self._create_careers()
        self._create_academic_records()
        self._create_certificates()
        self._create_languages()
        return self.profile

    def _create_base_profile(self):
        """기본 프로필 생성"""
        profile_data = self.json_data.get('Profile', {})
        self.profile = Profile.objects.create(
            name=profile_data.get('name'),
            job_category=profile_data.get('job_category'),
            career_year=profile_data.get('career_year')
        )

    def _create_profile_data(self):
        """프로필 데이터 생성"""
        # S3 경로 설정
        original_data_path = 'txt/resume_{:03}_{:02}.txt'.format(self.page_id, self.resume_id)
        processed_data_path = 'processed_json/resume_{:03}_{:02}.json'.format(self.page_id, self.resume_id)
        pdf_data_path = 'pdf/pdf_resume_{:03}_{:02}.pdf'.format(self.page_id, self.resume_id)

        # 파일 경로를 직접 할당
        ProfileData.objects.create(
            profile=self.profile,
            original_data=original_data_path,
            processed_data=processed_data_path,
            pdf_data=pdf_data_path
        )

    def _create_tech_stacks(self):
        """기술 스택 정보 생성"""
        tech_datas = self.json_data.get('TechStack') or []
        for tech_data in tech_datas:
            TechStack.objects.create(
                profile=self.profile,
                tech_stack_name=tech_data.get('tech_stack_name')
            )

    def _create_careers(self):
        """경력 정보 생성"""
        career_datas = self.json_data.get('Career') or []
        for career_data in career_datas:
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
        academic_datas = self.json_data.get('AcademicRecord') or []
        for academic_data in academic_datas:
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
        certificate_datas = self.json_data.get('Certificate') or []
        for cert_data in certificate_datas:
            Certificate.objects.create(
                profile=self.profile,
                name=cert_data.get('name')
            )

    def _create_languages(self):
        """언어 능력 정보 생성"""
        language_datas = self.json_data.get('Language') or []
        for lang_data in language_datas:
            Language.objects.create(
                profile=self.profile,
                language_name=lang_data.get('language_name'),
                description=lang_data.get('description')
            )

def create_profile_from_json(page_id, resume_id, json_data):
    """JSON 데이터를 받아서 프로필 및 관련 정보를 생성하는 함수"""
    creator = ProfileCreator(page_id, resume_id, json_data)
    return creator.create_profile()