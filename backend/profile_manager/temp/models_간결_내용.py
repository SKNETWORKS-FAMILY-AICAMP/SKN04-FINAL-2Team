from django.db import models

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    job_category = models.CharField(max_length=100, blank=True, null=True)
    career_year = models.IntegerField(blank=True, null=True)
class TechStack(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='tech_stacks') 
    tech_stack_name = models.CharField(max_length=100, blank=True, null=True)
class Career(models.Model): # 경력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='careers')
    company_name = models.CharField(max_length=100, blank=True, null=True)  # 회사명
    position = models.CharField(max_length=100, blank=True, null=True)      # 직위
    start_date = models.DateField(blank=True, null=True)                 # 시작일
    responsibilities = models.TextField(blank=True, null=True)  # 담당업무
    end_date = models.DateField(blank=True, null=True)  # 종료일 (현재 재직중일 수 있음)
    is_currently_employed = models.BooleanField(default=False)  # 현재 재직중인지 여부를 확인하는 변수
    description = models.TextField(blank=True, null=True)       # 추가 설명
class AcademicRecord(models.Model): # 학력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='academic_records')
    school_name = models.CharField(max_length=100, blank=True, null=True)   # 학교명
    major = models.CharField(max_length=100, blank=True, null=True)         # 전공
    status = models.CharField(max_length=20, default='graduated', blank=True, null=True)         # 졸업상태
    enrollment_date = models.CharField(max_length=7, blank=True, null=True)  # 입학일 (YYYY-MM 형식)
    graduation_date = models.CharField(max_length=7, null=True, blank=True)  # 졸업일 (YYYY-MM 형식)
class Certificate(models.Model): # 자격증
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='certificates')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'certificates' 지정
    name = models.CharField(max_length=100, blank=True, null=True)          # 자격증명
class Language(models.Model):   # 외국어
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='languages')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'languages' 지정
    language_name = models.CharField(max_length=100, blank=True, null=True)  # 언어 명
    description = models.CharField(max_length=100, blank=True, null=True)  # 언어 능력

