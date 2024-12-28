from django.db import models


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)  # 프로필 ID, 기본 키로 설정
    name = models.CharField(max_length=50)           # 이름
    job_category = models.CharField(max_length=50, blank=True, null=True)  # 직업
    career_year = models.IntegerField(blank=True, null=True)  # 경력 연수
    
    original_data = models.TextField(blank=True, null=True)  # LLM 데이터
    processed_data = models.TextField(blank=True, null=True)  # LLM 데이터
    # pdf_data = models.FileField(upload_to='pdf_data/', blank=True, null=True)  # PDF 파일
    
    class Meta:
        db_table = 'profile'  # 데이터베이스 테이블 이름
    
    def __str__(self):
        return self.name  # 프로필 이름으로 문자열 반환


class TechStack(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='tech_stacks')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'skills' 지정
    tech_stack_name = models.CharField(max_length=100, blank=True, null=True)  # 기술명     
    
    class Meta:
        db_table = 'tech_stack'  # 데이터베이스 테이블 이름

class Career(models.Model): # 경력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='careers')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'careers' 지정
    company_name = models.CharField(max_length=100, blank=True, null=True)  # 회사명
    position = models.CharField(max_length=100, blank=True, null=True)      # 직위
    responsibilities = models.TextField(blank=True, null=True)  # 담당업무
    start_date = models.CharField(max_length=7, blank=True, null=True)      # 시작일(YYYY-MM 형식)
    end_date = models.CharField(max_length=7, null=True, blank=True)        # 종료일 (현재 재직중일 수 있음, YYYY-MM 형식)
    is_currently_employed = models.BooleanField(default=False)  # 현재 재직중인지 여부를 확인하는 변수
    description = models.TextField(blank=True, null=True)       # 추가 설명
    
    class Meta:
        db_table = 'career'  # 데이터베이스 테이블 이름
        ordering = ['-start_date']  # 최신 경력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.company_name} - {self.position}"  # 회사명과 직위로 문자열 반환

class AcademicRecord(models.Model): # 학력
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='academic_records')
    school_name = models.CharField(max_length=100, blank=True, null=True)   # 학교명
    major = models.CharField(max_length=100, blank=True, null=True)         # 전공
    status = models.CharField(max_length=20, default='graduated', blank=True, null=True)         # 졸업상태
    enrollment_date = models.CharField(max_length=7, blank=True, null=True)  # 입학일 (YYYY-MM 형식)
    graduation_date = models.CharField(max_length=7, null=True, blank=True)  # 졸업일 (YYYY-MM 형식)
    
    class Meta:
        db_table = 'academic_record'  # 데이터베이스 테이블 이름
        ordering = ['-enrollment_date']  # 최신 학력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.school_name} - {self.major}"  # 학교명과 전공으로 문자열 반환


class Certificate(models.Model): # 자격증
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=50, blank=True, null=True)          # 자격증명
    
    class Meta:
        db_table = 'certificate'  # 데이터베이스 테이블 이름
    
    def __str__(self):
        return f"{self.name}"  # 자격증명으로 문자열 반환
    

class Language(models.Model):   # 외국어
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='languages')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'languages' 지정
    language_name = models.CharField(max_length=50, blank=True, null=True)  # 언어 명
    description = models.CharField(max_length=100, blank=True, null=True)     # 언어 능력
    
    class Meta:
        db_table = 'language'
    
    def __str__(self):
        return f"{self.language_name} ({self.description})"  # 언어명과 언어 능력으로 문자열 반환