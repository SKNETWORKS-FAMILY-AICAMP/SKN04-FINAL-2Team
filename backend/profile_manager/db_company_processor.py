from .models import Company, Career
from tqdm import tqdm
import boto3
from dotenv import load_dotenv
import os
from .models import Company
from datetime import datetime

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# python manage.py run_db_company_processor
def process_company_information():
    # S3에서 파일 내용 가져오기
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    
    for i in range(0, 2500):
        company_data_path = 'company_txt/company_information{:}.txt'.format(i)
        try:
            obj = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=company_data_path)
            file_content = obj['Body'].read().decode('utf-8')  # 파일 내용을 문자열로 읽기  
            # 파일 내용을 줄 단위로 분리
            lines_data = [line.strip() for line in file_content.strip().split('\n')]
        
            # 데이터 파싱
            company_name = lines_data[0].strip()
            is_major_company_str = lines_data[1].strip().lower()
            is_major_company = True if is_major_company_str == 'yes' else False
            establishment_date_str = lines_data[2].strip()
            # '2017년 11월' 형식을 '2017-11'로 변환
            try:
                establishment_date = datetime.strptime(establishment_date_str, "%Y년 %m월").strftime("%Y-%m")
            except ValueError:
                print(f"날짜 형식 오류: {establishment_date_str}")
                continue
            investment_scale = lines_data[3].strip()
            
            matching_companies = Career.objects.filter(company_name__icontains=company_name)
            
            # Career 모델에서 company_name 확인
            if not matching_companies.exists():
                # 일치하는 회사 이름이 없으면 로그에 기록
                with open('missing_company_names.log', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"{company_name}\n")
                    continue
            else:
                # 포함된 회사 이름이 있으면 로그에 기록
                with open('found_company_names.log', 'a', encoding='utf-8') as log_file:
                    for matching_company in matching_companies:
                        log_file.write(f"career_company_name:{matching_company.company_name}, company_name:{company_name}\n")
                
            # Company 모델에 데이터 저장
            company, created = Company.objects.get_or_create(
                company_name=company_name,
                defaults={
                    'is_major_company': is_major_company,
                    'establishment_date': establishment_date,
                    'investment_scale': investment_scale
                }
            )
            if created:
                print(f"새로운 회사 정보가 저장되었습니다: {company_name}")
                with open('saved_company_info.log', 'a', encoding='utf-8') as log_file:
                    log_file.write(f"{company_name}\n")
            else:
                print(f"이미 존재하는 회사 정보입니다: {company_name}")
                
        except s3.exceptions.NoSuchKey:
            # 파일이 불규칙하게 존재해 예외로 반복유지
            continue
        
# ... 기존 코드 ...
# if __name__ == "__main__":
#     process_company_information('company_information2070.txt')