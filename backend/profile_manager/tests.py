from django.test import TestCase
from django.utils import timezone
from .models import *
from datetime import datetime, date

class ProfileModelTest(TestCase):
    def setUp(self):
        """
        테스트에 필요한 기본 데이터 생성
        """
        # 기본 프로필 생성
        self.profile = Profile.objects.create(
            name="김테스트",
            email="test@example.com",
            phone="010-1234-5678",
            address="서울시 강남구",
            birth_date="1990-01-01"
        )
        
        # 프로필 상세 정보 생성
        self.profile_detail = Profile_Detail.objects.create(
            profile=self.profile,
            introduction="테스트용 프로필입니다."
        )

    def test_profile_creation(self):
        """
        기본 프로필 생성 테스트
        """
        self.assertEqual(self.profile.name, "김테스트")
        self.assertEqual(self.profile.email, "test@example.com")
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertEqual(str(self.profile), "김테스트")

    def test_profile_detail_creation(self):
        """
        프로필 상세 정보 생성 및 관계 테스트
        """
        self.assertEqual(self.profile_detail.profile, self.profile)
        self.assertEqual(self.profile_detail.introduction, "테스트용 프로필입니다.")
        self.assertTrue(isinstance(self.profile_detail.created_at, datetime))

    def test_skill_creation(self):
        """
        기술 스택 추가 테스트
        """
        skill = Skill.objects.create(
            profile=self.profile_detail,
            name="Python"
        )
        self.assertEqual(skill.name, "Python")
        self.assertEqual(self.profile_detail.skills.count(), 1)

    def test_career_creation(self):
        """
        경력 정보 추가 테스트
        """
        career = Career.objects.create(
            profile=self.profile_detail,
            company_name="테스트 회사",
            position="개발자",
            start_date="2020-01-01",
            end_date="2023-01-01",
            description="테스트 업무"
        )
        self.assertEqual(career.company_name, "테스트 회사")
        self.assertEqual(self.profile_detail.careers.count(), 1)

    def test_academic_background_creation(self):
        """
        학력 정보 추가 테스트
        """
        education = AcademicBackground.objects.create(
            profile=self.profile_detail,
            school_name="테스트대학교",
            major="컴퓨터공학",
            status="graduated",
            start_date="2010-03-02",
            end_date="2014-02-28"
        )
        self.assertEqual(education.school_name, "테스트대학교")
        self.assertEqual(self.profile_detail.educations.count(), 1)

    def test_certificate_creation(self):
        """
        자격증 정보 추가 테스트
        """
        certificate = Certificate.objects.create(
            profile=self.profile_detail,
            name="정보처리기사",
            acquisition_date="2015-01-01",
            issuing_org="한국산업인력공단"
        )
        self.assertEqual(certificate.name, "정보처리기사")
        self.assertEqual(self.profile_detail.certificates.count(), 1)

    def test_related_data_deletion(self):
        """
        프로필 삭제 시 관련 데이터 삭제 테스트 (CASCADE 확인)
        """
        # 삭제할 프로필 ID 저장
        profile_id = self.profile.profile_id
        profile_detail_id = self.profile_detail.id
        # 관련 데이터 생성
        Skill.objects.create(profile=self.profile_detail, name="Python")
        Career.objects.create(
            profile=self.profile_detail,
            company_name="테스트 회사",
            position="개발자",
            start_date="2020-01-01"
        )

        # 프로필 삭제
        self.profile.delete()

        # 관련 데이터들이 모두 삭제되었는지 확인
        self.assertEqual(Profile_Detail.objects.filter(id=profile_detail_id).count(), 0)
        self.assertEqual(Profile.objects.filter(profile_id=profile_id).count(), 0)
        self.assertEqual(Skill.objects.filter(profile_id=profile_detail_id).count(), 0)
        self.assertEqual(Career.objects.filter(profile_id=profile_detail_id).count(), 0)
        
    def test_full_profile_data(self):
        """
        전체 프로필 데이터 생성 및 조회 테스트
        """
        # 기술 스택 추가
        Skill.objects.create(profile=self.profile_detail, name="Python")
        Skill.objects.create(profile=self.profile_detail, name="Django")

        # 경력 추가
        Career.objects.create(
            profile=self.profile_detail,
            company_name="테스트 회사",
            position="개발자",
            start_date="2020-01-01"
        )

        # URL 추가
        URL.objects.create(
            profile=self.profile_detail,
            link="https://github.com/test"
        )

        # 조회 테스트
        profile = Profile.objects.get(name="김테스트")
        self.assertEqual(profile.detail.skills.count(), 2)
        self.assertEqual(profile.detail.careers.count(), 1)
        self.assertEqual(profile.detail.urls.count(), 1)