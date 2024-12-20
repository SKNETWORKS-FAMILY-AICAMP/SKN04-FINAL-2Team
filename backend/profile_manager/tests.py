# test_db_input_processor.py
from django.test import TestCase
from .db_profile_processor import ProfileCreator
from .models import (
    Profile, Profile_Detail, Skill, Career, Activity, 
    AcademicBackground, ParticipatedProject, Certificate,
    EducationContent, URL, Language
)

class ProfileCreatorTestCase(TestCase):
    def setUp(self):
        # 테스트에 사용할 JSON 데이터를 설정합니다.
        self.json_data = {
            "profile": {
                "name": "John Doe",
                "job": "Software Engineer",
                "email": "john.doe@example.com",
                "phone": "123-456-7890",
                "address": "123 Main St",
                "birth_date": "1990-01-01"
            },
            "profile_detail": {
                "brief_introduction": "A brief intro",
                "introduction": "A detailed introduction"
            },
            "skills": [
                {"name": "Python"}
            ],
            "careers": [
                {
                    "company_name": "Tech Corp",
                    "position": "Developer",
                    "start_date": "2015-01-01",
                    "end_date": "2020-01-01",
                    "employment_type": "Full-time",
                    "responsibilities": "Developing software",
                    "description": "Worked on various projects"
                }
            ],
            "activities": [
                {
                    "activity_name": "Hackathon",
                    "organization_name": "Tech Community",
                    "description": "Participated in a hackathon",
                    "activity_year": "2019"
                }
            ],
            "academic_backgrounds": [
                {
                    "school_name": "University of Example",
                    "major": "Computer Science",
                    "status": "Graduated",
                    "start_date": "2010-01-01",
                    "end_date": "2014-01-01"
                }
            ],
            "participated_projects": [
                {
                    "project_name": "Project X",
                    "project_role": "Lead Developer",
                    "organization_name": "Tech Corp",
                    "start_date": "2018-01-01",
                    "end_date": "2019-01-01"
                }
            ],
            "certificates": [
                {
                    "name": "Certified Developer",
                    "acquisition_date": "2016-01-01",
                    "issuing_org": "Certification Body"
                }
            ],
            "education_contents": [
                {
                    "education_name": "Online Course",
                    "description": "Completed an online course"
                }
            ],
            "urls": [
                {
                    "link": "http://example.com"
                }
            ],
            "languages": [
                {
                    "description": "English"
                }
            ]
        }

    def test_create_profile(self):
        # ProfileCreator를 사용하여 프로필을 생성합니다.
        creator = ProfileCreator(self.json_data)
        profile = creator.create_profile()

        # 생성된 프로필과 관련된 객체들이 올바르게 생성되었는지 확인합니다.
        self.assertIsNotNone(profile)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile_Detail.objects.count(), 1)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertEqual(Career.objects.count(), 1)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(AcademicBackground.objects.count(), 1)
        self.assertEqual(ParticipatedProject.objects.count(), 1)
        self.assertEqual(Certificate.objects.count(), 1)
        self.assertEqual(EducationContent.objects.count(), 1)
        self.assertEqual(URL.objects.count(), 1)
        self.assertEqual(Language.objects.count(), 1)

        # 프로필의 세부 정보가 올바른지 확인합니다.
        self.assertEqual(profile.name, "John Doe")
        self.assertEqual(profile.job, "Software Engineer")
        self.assertEqual(profile.email, "john.doe@example.com")