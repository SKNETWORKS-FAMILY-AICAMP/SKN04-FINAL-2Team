import os  # 운영체제와 상호작용하는 기능을 제공하는 모듈
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .crawling_data_formatter import ResumePreprocessor  # 이력서 데이터를 처리하는 클래스
from .db_profile_processor import ProfileCreator

from tqdm import tqdm  # 진행 상태를 표시하는 라이브러리

import json  # JSON 데이터를 처리하는 모듈
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')

def process_all_resumes(start_index=0):
    """
    모든 이력서를 처리하는 함수입니다.
    start_index: 시작할 이력서 파일의 인덱스
    """
    crawling_data_formatter = ResumePreprocessor()
 
    # S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    bucket_name = 'talentbucket01'  # S3 버킷 이름
    prefix = 'txt/'  # S3 버킷 내의 폴더 경로

    # S3에서 이력서 파일 목록 가져오기
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    resume_files = [obj['Key'] for obj in response.get('Contents', []) if not obj['Key'].endswith('/')]

    if not resume_files:
        print("이력서 파일이 없습니다.")
        return

    success_count = 0  # 성공한 이력서 처리 횟수
    fail_count = 0  # 실패한 이력서 처리 횟수
    
    for idx, resume_file in enumerate(tqdm(resume_files), start=start_index):
        
        try:
            # S3에서 파일 내용 직접 가져오기
            obj = s3.get_object(Bucket=bucket_name, Key=resume_file)
            resume_text = obj['Body'].read().decode('utf-8')  # 파일 내용을 문자열로 읽기
            
            gpt_result = crawling_data_formatter.process_resume(resume_text)  # 이력서 텍스트를 처리하여 GPT 결과를 얻습니다.

            # JSON 시작과 끝 부분만 추출
            start_index = gpt_result.find('{')  # 첫 번째 '{'의 위치
            end_index = gpt_result.rfind('}')  # 마지막 '}'의 위치
            if start_index == -1 or end_index == -1:
                raise ValueError("JSON 데이터가 유효하지 않습니다.")

            # JSON 부분만 가져오기
            json_part = gpt_result[start_index:end_index + 1]

            # JSON 파싱
            print("json 파싱 시작")
            parsed_data = json.loads(json_part)
            print("ProfileCreator 시작")
            profile_creator = ProfileCreator(parsed_data)
            profile =  profile_creator.create_profile()
            print("profile 완료")

            success_count += 1  # 성공한 이력서 처리 횟수를 증가시킵니다.
            print(f"성공: {resume_file}")  # 성공한 이력서 파일 이름을 출력합니다.
            break # 테스트를 위해 1개만 처리

        except Exception as e:  # 예외가 발생하면
            fail_count += 1  # 실패한 이력서 처리 횟수를 증가시킵니다.
            print(f"실패 ({resume_file}): {str(e)}")  # 실패한 이력서 파일 이름과 예외 메시지를 출력합니다.
            print(f"\n다음 실행 시 start_index={idx} 부터 시작하세요.")
            return None  # 실패 시 즉시 종료
        
    print(f"\n처리 완료!")  # 모든 이력서 처리가 완료되었습니다.
    print(f"성공: {success_count}개")  # 성공한 이력서 처리 횟수를 출력합니다.
    print(f"실패: {fail_count}개")  # 실패한 이력서 처리 횟수를 출력합니다.
    print(f"총 처리: {success_count + fail_count}개")  # 총 이력서 처리 횟수를 출력합니다.
    
    return profile  # 처리된 마지막 프로필을 반환합니다.
    
if __name__ == "__main__":
    result = process_all_resumes(start_index=0)  # 처음 1개만 처리
    print(result)
