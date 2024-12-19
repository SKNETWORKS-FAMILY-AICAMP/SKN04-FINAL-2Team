from django.db import models

# 이름, 메일, 전번, 주소, 생년월일
# 기술스택, 경력, 대외활동, 학력, 자격증, 교육내용, URL, 외국어, 자기소개

class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)  # 프로필 ID, 기본 키로 설정
    name = models.CharField(max_length=100)  # 이름
    email = models.EmailField(max_length=255)  # 이메일
    phone = models.CharField(max_length=15)  # 전화번호
    address = models.CharField(max_length=255)  # 주소
    birth_date = models.DateField()  # 생년월일

    def __str__(self):
        return self.name  # 프로필 이름으로 문자열 반환
    
class Profile_Detail(models.Model):
    """
    사용자의 전문성과 경력 관련 상세 정보를 저장하는 모델
    """
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='detail')  # Profile 모델과 1:1 관계, related_name으로 'detail' 지정  
    # Profile과 1:1 관계로 변경하고 related_name 추가
    introduction = models.TextField(blank=True)  # 자기소개는 하나만 있으면 되므로 유지, 빈 문자열 허용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일, 자동으로 현재 시간으로 설정
    updated_at = models.DateTimeField(auto_now=True)      # 수정일, 자동으로 현재 시간으로 설정

    class Meta:
        db_table = 'profile_detail'  # 데이터베이스 테이블 이름

    def __str__(self):
        return f"Profile Detail for {self.profile.name}"  # 프로필 이름으로 문자열 반환

class Skill(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='skills')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'skills' 지정
    name = models.CharField(max_length=100)  # 기술명
    
    class Meta:
        db_table = 'skill'  # 데이터베이스 테이블 이름

class Career(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='careers')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'careers' 지정
    company_name = models.CharField(max_length=100)  # 회사명
    position = models.CharField(max_length=100)      # 직위
    start_date = models.DateField()                 # 시작일
    end_date = models.DateField(null=True, blank=True)  # 종료일 (현재 재직중일 수 있음), 빈 문자열 허용
    description = models.TextField(blank=True)       # 추가 설명, 빈 문자열 허용
    
    class Meta:
        db_table = 'career'  # 데이터베이스 테이블 이름
        ordering = ['-start_date']  # 최신 경력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.company_name} - {self.position}"  # 회사명과 직위로 문자열 반환

class Activity(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='activities')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'activities' 지정
    description = models.CharField(max_length=100)  # 활동 내용
    
    class Meta:
        db_table = 'activity'  # 데이터베이스 테이블 이름

class AcademicBackground(models.Model):
    GRADUATION_STATUS_CHOICES = [
        ('attending', '재학중'),
        ('graduated', '졸업'),
        ('leave', '휴학'),
        ('dropout', '중퇴'),
    ]
    
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='educations')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'educations' 지정
    school_name = models.CharField(max_length=100)   # 학교명
    major = models.CharField(max_length=100)         # 전공
    status = models.CharField(                       # 졸업상태
        max_length=20,
        choices=GRADUATION_STATUS_CHOICES,
        default='graduated'
    )
    start_date = models.DateField()                 # 입학일
    end_date = models.DateField(null=True, blank=True)  # 졸업일, 빈 문자열 허용
    
    class Meta:
        db_table = 'academic_background'  # 데이터베이스 테이블 이름
        ordering = ['-start_date']  # 최신 학력이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.school_name} - {self.major}"  # 학교명과 전공으로 문자열 반환

class Certificate(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='certificates')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'certificates' 지정
    name = models.CharField(max_length=100)          # 자격증명
    acquisition_date = models.DateField()           # 취득일
    issuing_org = models.CharField(max_length=100)   # 발급기관
    
    class Meta:
        db_table = 'certificate'  # 데이터베이스 테이블 이름
        ordering = ['-acquisition_date']  # 최신 자격증이 먼저 나오도록 정렬
    
    def __str__(self):
        return f"{self.name} ({self.issuing_org})"  # 자격증명과 발급기관으로 문자열 반환

class EducationContent(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='education_contents')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'education_contents' 지정
    description = models.CharField(max_length=100)  # 교육 이수 내용
    
    class Meta:
        db_table = 'education_content'  # 데이터베이스 테이블 이름

class URL(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='urls')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'urls' 지정
    link = models.CharField(max_length=100)  # URL 링크
    
    class Meta:
        db_table = 'url'  # 데이터베이스 테이블 이름

class Language(models.Model):
    profile = models.ForeignKey('Profile_Detail', on_delete=models.CASCADE, related_name='languages')  # Profile_Detail 모델과 외래 키 관계, related_name으로 'languages' 지정
    description = models.CharField(max_length=100)  # 언어 능력
    
    class Meta:
        db_table = 'language' 