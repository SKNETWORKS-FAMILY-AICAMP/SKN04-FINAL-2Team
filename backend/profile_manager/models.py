from django.db import models


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)  # 프로필 ID, 기본 키로 설정
    name = models.CharField(max_length=100)  # 이름
    job = models.CharField(max_length=100, blank=True, null=True)  # 직업
    email = models.EmailField(max_length=255, blank=True, null=True)  # 이메일
    phone = models.CharField(max_length=15, blank=True, null=True)  # 전화번호
    address = models.CharField(max_length=255, blank=True, null=True)  # 주소
    birth_date = models.DateField(blank=True, null=True)  # 생년월일

    def __str__(self):
        return self.name  # 프로필 이름으로 문자열 반환
    
class Profile_Detail(models.Model):
    """
    사용자의 전문성과 경력 관련 상세 정보를 저장하는 모델
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='detail')  # Profile 모델과 1:1 관계, related_name으로 'detail' 지정  
    # Profile과 1:1 관계로 변경하고 related_name 추가
    brief_introduction = models.TextField(blank=True, null=True)  # 간단소개, 빈 문자열 허용
    introduction = models.TextField(blank=True, null=True)  # 자기소개는 하나만 있으면 되므로 유지, 빈 문자열 허용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일, 자동으로 현재 시간으로 설정
    updated_at = models.DateTimeField(auto_now=True)      # 수정일, 자동으로 현재 시간으로 설정

    class Meta:
        db_table = 'profile_detail'  # 데이터베이스 테이블 이름

    def __str__(self):
        return f"Profile Detail for {self.profile.name}"  # 프로필 이름으로 문자열 반환

class Skill(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='skills')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'skills' 지정
    name = models.CharField(max_length=100, blank=True, null=True)  # 기술명
    
    class Meta:
        db_table = 'skill'  # 데이터베이스 테이블 이름

class Career(models.Model): # 경력
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='careers')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'careers' 지정
    company_name = models.CharField(max_length=100, blank=True, null=True)  # 회사명
    position = models.CharField(max_length=100, blank=True, null=True)      # 직위
    start_date = models.DateField(blank=True, null=True)                 # 시작일
    employment_type = models.CharField(max_length=100, blank=True, null=True)  # 근무 형태
    responsibilities = models.TextField(blank=True, null=True)  # 담당업무
    end_date = models.DateField(blank=True, null=True)  # 종료일 (현재 재직중일 수 있음)
    description = models.TextField(blank=True, null=True)       # 추가 설명
    
    class Meta:
        db_table = 'career'  # 데이터베이스 테이블 이름
        ordering = ['-start_date']  # 최신 경력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.company_name} - {self.position}"  # 회사명과 직위로 문자열 반환

class Activity(models.Model): # 대외활동
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='activities')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'activities' 지정
    activity_name = models.CharField(max_length=100, blank=True, null=True)  # 활동 명
    organization_name = models.CharField(max_length=100, blank=True, null=True)  # 소속/기관명
    description = models.CharField(max_length=100, blank=True, null=True)  # 활동 내용
    activity_year = models.IntegerField(blank=True, null=True)  # 활동 연도 
    
    
    class Meta:
        db_table = 'activity'  # 데이터베이스 테이블 이름

class AcademicBackground(models.Model): # 학력
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='educations')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'educations' 지정
    school_name = models.CharField(max_length=100, blank=True, null=True)   # 학교명
    major = models.CharField(max_length=100, blank=True, null=True)         # 전공
    status = models.CharField(                                   # 졸업상태
        max_length=20,
        default='graduated',
        blank=True,
        null=True
    )
    start_date = models.DateField(blank=True, null=True)                 # 입학일
    end_date = models.DateField(null=True, blank=True)  # 졸업일, 빈 문자열 허용
    
    class Meta:
        db_table = 'academic_background'  # 데이터베이스 테이블 이름
        ordering = ['-start_date']  # 최신 학력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.school_name} - {self.major}"  # 학교명과 전공으로 문자열 반환

class ParticipatedProject(models.Model): # 참여 프로젝트 정보
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='participated_projects')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'participated_projects' 지정
    project_name = models.CharField(max_length=100, blank=True, null=True)  # 프로젝트 명
    project_role = models.CharField(max_length=100, blank=True, null=True)  # 프로젝트 역할
    organization_name = models.CharField(max_length=100, blank=True, null=True)  # 소속/기관명
    start_date = models.DateField(blank=True, null=True)  # 시작일
    end_date = models.DateField(blank=True, null=True)  # 종료일
    
    class Meta:
        db_table = 'participated_project'  # 데이터베이스 테이블 이름

class Certificate(models.Model): # 자격증
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='certificates')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'certificates' 지정
    name = models.CharField(max_length=100, blank=True, null=True)          # 자격증명
    acquisition_date = models.DateField(blank=True, null=True)           # 취득일
    issuing_org = models.CharField(max_length=100, blank=True, null=True)   # 발급기관
    
    class Meta:
        db_table = 'certificate'  # 데이터베이스 테이블 이름
        ordering = ['-acquisition_date']  # 최신 자격증이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.name} ({self.issuing_org})"  # 자격증명과 발급기관으로 문자열 반환

class EducationContent(models.Model): # 교육이수
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='education_contents')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'education_contents' 지정
    education_name = models.CharField(max_length=100, blank=True, null=True)  # 이수 교육명
    description = models.CharField(max_length=100, blank=True, null=True)      # 교육 내용
    
    class Meta:
        db_table = 'education_content'  # 데이터베이스 테이블 이름

class URL(models.Model): # URL
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='urls')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'urls' 지정
    link = models.CharField(max_length=100, blank=True, null=True)  # URL 링크
    
    class Meta:
        db_table = 'url'  # 데이터베이스 테이블 이름

class Language(models.Model):   # 외국어
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='languages')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'languages' 지정
    description = models.CharField(max_length=100, blank=True, null=True)  # 언어 능력
    
    class Meta:
        db_table = 'language' 

class LLM_Data(models.Model): # LLM 데이터
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='llm_data')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'llm_data' 지정
    original_data = models.TextField(blank=True, null=True)  # LLM 데이터
    processed_data = models.TextField(blank=True, null=True)  # LLM 데이터
    
    class Meta:
        db_table = 'llm_data'  # 데이터베이스 테이블 이름
