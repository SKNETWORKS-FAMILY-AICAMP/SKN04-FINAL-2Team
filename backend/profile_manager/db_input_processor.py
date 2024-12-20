from django.db import transaction
from .models import (
    Profile, Profile_Detail, Skill, Career, Activity, 
    AcademicBackground, ParticipatedProject, Certificate,
    EducationContent, URL, Language, LLM_Data
)

class ProfileCreator:
    def __init__(self, json_data):
        self.json_data = json_data
        self.profile = None
        self.profile_detail = None

    @transaction.atomic
    def create_profile(self):
        """프로필 및 관련 정보를 생성하는 메인 메서드"""
        self._create_base_profile()
        self._create_profile_detail()
        self._create_skills()
        self._create_careers()
        self._create_activities()
        self._create_academic_backgrounds()
        self._create_projects()
        self._create_certificates()
        self._create_education_contents()
        self._create_urls()
        self._create_languages()
        return self.profile

    def _create_base_profile(self):
        """기본 프로필 생성"""
        profile_data = self.json_data.get('profile', {})
        self.profile = Profile.objects.create(
            name=profile_data.get('name', ''),
            job=profile_data.get('job', ''),
            email=profile_data.get('email', ''),
            phone=profile_data.get('phone', ''),
            address=profile_data.get('address', ''),
            birth_date=profile_data.get('birth_date', None)
        )

    def _create_profile_detail(self):
        """프로필 상세 정보 생성"""
        detail_data = self.json_data.get('profile_detail', {})
        self.profile_detail = Profile_Detail.objects.create(
            profile=self.profile,
            brief_introduction=detail_data.get('brief_introduction', ''),
            introduction=detail_data.get('introduction', '')
        )

    def _create_skills(self):
        """스킬 정보 생성"""
        for skill_data in self.json_data.get('skills', []):
            Skill.objects.create(
                profile=self.profile_detail,
                name=skill_data.get('name', '')
            )

    def _create_careers(self):
        """경력 정보 생성"""
        for career_data in self.json_data.get('careers', []):
            Career.objects.create(
                profile=self.profile_detail,
                company_name=career_data.get('company_name', ''),
                position=career_data.get('position', ''),
                start_date=career_data.get('start_date', None),
                end_date=career_data.get('end_date', None),
                employment_type=career_data.get('employment_type', ''),
                responsibilities=career_data.get('responsibilities', ''),
                description=career_data.get('description', '')
            )

    def _create_activities(self):
        """활동 정보 생성"""
        for activity_data in self.json_data.get('activities', []):
            Activity.objects.create(
                profile=self.profile_detail,
                activity_name=activity_data.get('activity_name', ''),
                organization_name=activity_data.get('organization_name', ''),
                description=activity_data.get('description', ''),
                activity_year=activity_data.get('activity_year', None)
            )

    def _create_academic_backgrounds(self):
        """학력 정보 생성"""
        for academic_data in self.json_data.get('academic_backgrounds', []):
            AcademicBackground.objects.create(
                profile=self.profile_detail,
                school_name=academic_data.get('school_name', ''),
                major=academic_data.get('major', ''),
                status=academic_data.get('status', ''),
                start_date=academic_data.get('start_date', None),
                end_date=academic_data.get('end_date', None)
            )

    def _create_projects(self):
        """프로젝트 정보 생성"""
        for project_data in self.json_data.get('participated_projects', []):
            ParticipatedProject.objects.create(
                profile=self.profile_detail,
                project_name=project_data.get('project_name', ''),
                project_role=project_data.get('project_role', ''),
                organization_name=project_data.get('organization_name', ''),
                start_date=project_data.get('start_date', None),
                end_date=project_data.get('end_date', None)
            )

    def _create_certificates(self):
        """자격증 정보 생성"""
        for cert_data in self.json_data.get('certificates', []):
            Certificate.objects.create(
                profile=self.profile_detail,
                name=cert_data.get('name', ''),
                acquisition_date=cert_data.get('acquisition_date', None),
                issuing_org=cert_data.get('issuing_org', '')
            )

    def _create_education_contents(self):
        """교육 이력 생성"""
        for edu_data in self.json_data.get('education_contents', []):
            EducationContent.objects.create(
                profile=self.profile_detail,
                education_name=edu_data.get('education_name', ''),
                description=edu_data.get('description', '')
            )

    def _create_urls(self):
        """URL 정보 생성"""
        for url_data in self.json_data.get('urls', []):
            URL.objects.create(
                profile=self.profile_detail,
                link=url_data.get('link', '')
            )

    def _create_languages(self):
        """언어 능력 정보 생성"""
        for lang_data in self.json_data.get('languages', []):
            Language.objects.create(
                profile=self.profile_detail,
                description=lang_data.get('description', '')
            )

# 기존 함수를 대체하는 헬퍼 함수
def create_profile_from_json(json_data):
    """JSON 데이터를 받아서 프로필 및 관련 정보를 생성하는 함수"""
    creator = ProfileCreator(json_data)
    return creator.create_profile()