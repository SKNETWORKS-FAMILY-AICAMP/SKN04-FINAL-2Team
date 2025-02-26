from django.db import models
from django.conf import settings


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)  # 프로필 ID, 기본 키로 설정
    name = models.CharField(max_length=50)           # 이름
    job_category = models.CharField(max_length=50, blank=True, null=True)  # 직업
    career_year = models.IntegerField(blank=True, null=True)  # 경력 연수

    class Meta:
        db_table = 'profile'  # 데이터베이스 테이블 이름
    
    def __str__(self):
        return self.name  # 프로필 이름으로 문자열 반환

class ProfileData(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE, related_name='profile_data')
    original_data = models.FileField(upload_to='', blank=True, null=True)  # 원본 데이터 파일
    processed_data = models.FileField(upload_to='', blank=True, null=True)  # JSON 처리된 데이터 파일
    pdf_data = models.FileField(upload_to='', blank=True, null=True)  # PDF 파일
    ai_analysis = models.TextField(blank=True, null=True)  # AI 분석 결과

    def delete(self, *args, **kwargs):
        # 파일 삭제를 방지하기 위해 `FileField`의 `delete` 메서드를 호출하지 않음
        self.original_data.delete = lambda *args, **kwargs: None
        self.processed_data.delete = lambda *args, **kwargs: None
        self.pdf_data.delete = lambda *args, **kwargs: None
        super(ProfileData, self).delete(*args, **kwargs)

    class Meta:
        db_table = 'profile_data'  # 데이터베이스 테이블 이름

class TechStack(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='tech_stacks')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'skills' 지정
    tech_stack_name = models.CharField(max_length=100, blank=True, null=True)  # 기술명     
    
    class Meta:
        db_table = 'tech_stack'  # 데이터베이스 테이블 이름

class Career(models.Model): # 경력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='careers', )  # Profile_Detail 모델과 외래 키 관계, related_name으로 'careers' 지정
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='careers')  # Company 모델과 관계 추가
    company_name = models.CharField(max_length=100, blank=True, null=True, db_index=True)  # 회사명
    position = models.CharField(max_length=100, blank=True, null=True)      # 직위
    career_start_date = models.CharField(max_length=7, blank=True, null=True)      # 시작일(YYYY-MM 형식)
    career_end_date = models.CharField(max_length=7, null=True, blank=True)        # 종료일 (현재 재직중일 수 있음, YYYY-MM 형식)
    is_currently_employed = models.BooleanField(default=False, null=True)  # 현재 재직중인지 여부를 확인하는 변수
    career_description = models.TextField(blank=True, null=True)       # 추가 설명
    
    class Meta:
        db_table = 'career'  # 데이터베이스 테이블 이름
        ordering = ['-career_start_date']  # 최신 경력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.company_name} - {self.position}"  # 회사명과 직위로 문자열 반환

class AcademicRecord(models.Model): # 학력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='academic_records')
    school_name = models.CharField(max_length=100, blank=True, null=True)   # 학교명
    major = models.CharField(max_length=100, blank=True, null=True)         # 전공
    degree = models.IntegerField(blank=True, null=True)  # 학위 (0: 고졸, 1: 전문대졸, 2: 학사, 3: 석사, 4: 박사)
    enrollment_date = models.CharField(max_length=7, blank=True, null=True)  # 입학일 (YYYY-MM 형식)
    graduation_date = models.CharField(max_length=7, null=True, blank=True)  # 졸업일 (YYYY-MM 형식)
    
    class Meta:
        db_table = 'academic_record'  # 데이터베이스 테이블 이름
        ordering = ['-enrollment_date']  # 최신 학력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.school_name} - {self.major}"  # 학교명과 전공으로 문자열 반환


class Certificate(models.Model): # 자격증
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='certificates')
    certificate_name = models.CharField(max_length=100, blank=True, null=True)          # 자격증명
    
    class Meta:
        db_table = 'certificate'  # 데이터베이스 테이블 이름
    
    def __str__(self):
        return f"{self.certificate_name}"  # 자격증명으로 문자열 반환
    

class Language(models.Model):   # 외국어
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='languages')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'languages' 지정
    language_name = models.CharField(max_length=50, blank=True, null=True)  # 언어 명
    lank = models.CharField(max_length=10, blank=True, null=True)  # 언어 수준(예: 상, 중, 하)
    language_description = models.TextField(blank=True, null=True)     # 언어 능력
    
    class Meta:
        db_table = 'language'
    
    def __str__(self):
        return f"{self.language_name} ({self.language_description})"  # 언어명과 언어 능력으로 문자열 반환
    

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='bookmarked_by')
    ai_analysis = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmark'
        unique_together = ('user', 'profile')

    def __str__(self):
        return f"{self.user.username} - {self.profile.name}"
    
class Company(models.Model):
    company_name = models.CharField(max_length=100, db_index=True, unique=True)  # 회사이름
    is_major_company = models.BooleanField(default=False)  # 대기업 유무
    establishment_date = models.CharField(max_length=7)  # 설립일자 (YYYY-MM 형식)
    investment_scale = models.CharField(max_length=100, blank=True, null=True)  # 투자규모 (단위: 원)
    
    class Meta:
        db_table = 'company'  # 데이터베이스 테이블 이름
        
    def __str__(self):
        return self.company_name  # 회사이름으로 문자열 반환