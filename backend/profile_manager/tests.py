from django.test import TestCase
from django.utils import timezone
from .models import *
from .db_input_processor import create_profile_from_json, save_llm_data
import json
from datetime import datetime, date

class DBInputProcessorTest(TestCase):
    def setUp(self):
        """
        테스트에 필요한 실제 데이터 설정
        """
        self.test_json_data = {
            "profile": {
                "name": "박수빈",
                "job": "프론트엔드 개발자",
                "email": None,
                "phone": None,
                "address": None,
                "birth_date": None
            },
            "profile_detail": {
                "brief_introduction": "친구들에게 일본어를 알려주기 위해 일본어 단어장 앱인 당고당고를 개발하고 운영하고 있습니다.",
                "introduction": "현재 누적 다운로드 3만, MAU 4천을 달성했습니다. 앱 서비스는 사용자와 함께 만들어 나가는 것이라고 생각해 여러 피드백을 적극 수용하면서 업데이트하고 있습니다."
            },
            "skills": [
                {"name": "JavaScript"},
                {"name": "TypeScript"},
                {"name": "React"},
                {"name": "Next.js"},
                {"name": "React Native"},
                {"name": "Firebase"}
            ],
            "careers": [
                {
                    "company_name": "goondori",
                    "position": "리액트네이티브 개발자",
                    "start_date": "2023.11.",
                    "end_date": "재직 중",
                    "employment_type": "정규직",
                    "responsibilities": "누적 200만 다운로드 국민 전역일 계산기 군돌이 서비스 스타트업",
                    "description": "초기 스타트업에 적응하여 여러 페이지와 기능 개발, 맛있는 메뉴 추가 로직 1.6s -> 0.6s로 성능 개선, 공통 컴포넌트 코치마크, Toast 개발"
                }
            ],
            "activities": [
                {
                    "activity_name": "DND 8기",
                    "organization_name": "DND",
                    "description": "개발자와 디자이너가 모여 사이드 프로젝트를 진행하는 동아리",
                    "activity_year": "2023"
                }
            ],
            "academic_backgrounds": [
                {
                    "school_name": "동양미래대학교",
                    "major": "소프트웨어공학",
                    "status": "졸업",
                    "start_date": "2018.03.",
                    "end_date": "2024.02."
                }
            ],
            "participated_projects": [
                {
                    "project_name": "당고당고",
                    "project_role": "개발자",
                    "organization_name": "사이드 프로젝트 (개발자1, 디자이너1)",
                    "start_date": "2023.01.",
                    "end_date": "진행 중"
                },
                {
                    "project_name": "슬편생",
                    "project_role": "서기",
                    "organization_name": "DND 8기 10조 (프론트2, 백엔드2, 디자이너2)",
                    "start_date": "2023.01.",
                    "end_date": "2023.03."
                }
            ],
            "certificates": [],
            "education_contents": [],
            "urls": [
                {"link": "깃허브 링크"},
                {"link": "개발 블로그 링크"},
                {"link": "프론트엔드 개발자 박수빈 이력서"}
            ],
            "languages": [
                {"description": "일본어: 일상 회화 가능"}
            ]
        }

    def test_create_profile_from_json_with_real_data(self):
        """
        실제 데이터로 프로필 생성 테스트
        """
        profile = create_profile_from_json(self.test_json_data)

        # 기본 프로필 정보 검증
        self.assertEqual(profile.name, "박수빈")
        self.assertEqual(profile.job, "프론트엔드 개발자")
        self.assertIsNone(profile.email)
        self.assertIsNone(profile.phone)

        # 프로필 상세 정보 검증
        profile_detail = profile.detail
        self.assertTrue("당고당고를 개발" in profile_detail.brief_introduction)
        self.assertTrue("MAU 4천을 달성" in profile_detail.introduction)

        # 스킬 정보 검증
        skills = profile_detail.skills.all()
        self.assertEqual(len(skills), 6)
        skill_names = [skill.name for skill in skills]
        self.assertIn("JavaScript", skill_names)
        self.assertIn("React Native", skill_names)

        # 경력 정보 검증
        careers = profile_detail.careers.all()
        self.assertEqual(len(careers), 1)
        self.assertEqual(careers[0].company_name, "goondori")
        self.assertEqual(careers[0].position, "리액트네이티브 개발자")

        # 활동 정보 검증
        activities = profile_detail.activities.all()
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0].activity_name, "DND 8기")
        self.assertEqual(activities[0].activity_year, 2023)

    def test_create_profile_with_special_date_formats(self):
        """
        특수한 날짜 형식 처리 테스트 (YYYY.MM. 형식)
        """
        career = self.test_json_data['careers'][0]
        self.assertEqual(career['start_date'], "2023.11.")
        self.assertEqual(career['end_date'], "재직 중")
        
        profile = create_profile_from_json(self.test_json_data)
        career_obj = profile.detail.careers.first()
        
        # 날짜 형식이 올바르게 처리되었는지 확인
        self.assertIsNotNone(career_obj)
        # 여기서는 날짜 처리 로직에 따라 적절한 검증을 추가해야 합니다

    def test_create_profile_with_empty_collections(self):
        """
        빈 배열 데이터 처리 테스트
        """
        self.assertEqual(len(self.test_json_data['certificates']), 0)
        self.assertEqual(len(self.test_json_data['education_contents']), 0)
        
        profile = create_profile_from_json(self.test_json_data)
        
        # 빈 컬렉션이 올바르게 처리되었는지 확인
        self.assertEqual(profile.detail.certificates.count(), 0)
        self.assertEqual(profile.detail.education_contents.count(), 0)

    def test_urls_and_languages(self):
        """
        URL과 언어 정보 저장 테스트
        """
        profile = create_profile_from_json(self.test_json_data)
        
        # URL 검증
        urls = profile.detail.urls.all()
        self.assertEqual(len(urls), 3)
        self.assertTrue(any(url.link == "깃허브 링크" for url in urls))
        
        # 언어 정보 검증
        languages = profile.detail.languages.all()
        self.assertEqual(len(languages), 1)
        self.assertEqual(languages[0].description, "일본어: 일상 회화 가능")