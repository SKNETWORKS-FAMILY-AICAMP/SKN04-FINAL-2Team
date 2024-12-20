from .models import (
    Profile, Profile_Detail, Skill, Career, Activity, 
    AcademicBackground, ParticipatedProject, Certificate,
    EducationContent, URL, Language, LLM_Data
)
from django.db import transaction

@transaction.atomic
def create_profile_from_json(json_data):
    """
    JSON 데이터를 받아서 프로필 및 관련 정보를 생성하는 함수
    """
    # 기본 프로필 생성
    profile_data = json_data.get('profile', {})
    profile = Profile.objects.create(
        name=profile_data.get('name', ''),  # 이름
        job=profile_data.get('job', ''),  # 직업
        email=profile_data.get('email', ''),  # 이메일
        phone=profile_data.get('phone', ''),  # 전화번호
        address=profile_data.get('address', ''),  # 주소
        birth_date=profile_data.get('birth_date', None)  # 생년월일
    )

    # 프로필 상세 정보 생성
    detail_data = json_data.get('profile_detail', {})
    profile_detail = Profile_Detail.objects.create(
        profile=profile,  # 프로필 모델과 연결
        brief_introduction=detail_data.get('brief_introduction', ''),  # 간단한 소개
        introduction=detail_data.get('introduction', '')  # 자기소개
    )

    # 스킬 정보 생성
    for skill_data in json_data.get('skills', []):
        Skill.objects.create(
            profile=profile_detail,  # 프로필 상세 정보 모델과 연결
            name=skill_data.get('name', '')  # 스킬 이름
        )

    # 경력 정보 생성
    for career_data in json_data.get('careers', []):
        Career.objects.create(
            profile=profile_detail,  # 프로필 상세 정보 모델과 연결
            company_name=career_data.get('company_name', ''),  # 회사 이름
            position=career_data.get('position', ''),  # 직위
            start_date=career_data.get('start_date', None),  # 시작 날짜
            end_date=career_data.get('end_date', None),  # 종료 날짜
            employment_type=career_data.get('employment_type', ''),  # 고용 형태
            responsibilities=career_data.get('responsibilities', ''),  # 담당 업무
            description=career_data.get('description', '')  # 추가 설명
        )

    # 나머지 모델들도 같은 방식으로 생성
    for activity_data in json_data.get('activities', []):
        Activity.objects.create(
            profile=profile_detail,  # 프로필 상세 정보 모델과 연결
            activity_name=activity_data.get('activity_name', ''),  # 활동 이름
            organization_name=activity_data.get('organization_name', ''),  # 소속/기관 이름
            description=activity_data.get('description', ''),  # 활동 설명
            activity_year=activity_data.get('activity_year', None)  # 활동 연도
        )
    
    # 학력 정보 생성
    for academic_data in json_data.get('academic_backgrounds', []):
        AcademicBackground.objects.create(
            profile=profile_detail,
            school_name=academic_data.get('school_name', ''),
            major=academic_data.get('major', ''),
            status=academic_data.get('status', ''),
            start_date=academic_data.get('start_date', None),
            end_date=academic_data.get('end_date', None)
        )

    # 프로젝트 정보 생성
    for project_data in json_data.get('participated_projects', []):
        ParticipatedProject.objects.create(
            profile=profile_detail,
            project_name=project_data.get('project_name', ''),
            project_role=project_data.get('project_role', ''),
            organization_name=project_data.get('organization_name', ''),
            start_date=project_data.get('start_date', None),
            end_date=project_data.get('end_date', None)
        )

    # 자격증 정보 생성
    for cert_data in json_data.get('certificates', []):
        Certificate.objects.create(
            profile=profile_detail,
            name=cert_data.get('name', ''),
            acquisition_date=cert_data.get('acquisition_date', None),
            issuing_org=cert_data.get('issuing_org', '')
        )

    # 교육 이력 생성
    for edu_data in json_data.get('education_contents', []):
        EducationContent.objects.create(
            profile=profile_detail,
            education_name=edu_data.get('education_name', ''),
            description=edu_data.get('description', '')
        )

    # URL 정보 생성
    for url_data in json_data.get('urls', []):
        URL.objects.create(
            profile=profile_detail,
            link=url_data.get('link', '')
        )

    # 언어 능력 정보 생성
    for lang_data in json_data.get('languages', []):
        Language.objects.create(
            profile=profile_detail,
            description=lang_data.get('description', '')
        )

    return profile



@transaction.atomic
def save_llm_data(profile_detail, crawled_data, processed_json):
    """
    크롤링된 원본 데이터와 처리된 JSON 데이터를 저장하는 함수
    
    Args:
        profile_detail (Profile_Detail): 프로필 상세 정보 객체
        crawled_data (str): 크롤링된 원본 텍스트 데이터
        processed_json (str): JSON으로 변환/처리된 데이터
    
    Returns:
        LLM_Data: 생성된 LLM 데이터 객체
    """
    llm_data = LLM_Data.objects.create(
        profile=profile_detail,
        original_data=crawled_data,  # 크롤링된 원본 데이터
        processed_data=processed_json  # JSON으로 변환/처리된 데이터
    )
    
    return llm_data