import os
import django
import json
from django.conf import settings
from .models import ProfileData

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .db_profile_processor import create_profile_from_json
from tqdm import tqdm
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

# python manage.py run_db_input_processor
# 이력서 파일을 읽어서 db에 프로필 정보를 생성하는 함수입니다.
def db_input_processor(start_index=0):
    # S3 클라이언트 생성
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)

    prefix = 'processed_json/'  # S3 버킷 내의 폴더 경로

    json_files = []
    continuation_token = None

    # 페이지네이션을 통해 모든 객체 가져오기
    while True:
        if continuation_token:
            response = s3.list_objects_v2(
                Bucket=AWS_STORAGE_BUCKET_NAME, 
                Prefix=prefix, 
                ContinuationToken=continuation_token
            )
        else:
            response = s3.list_objects_v2(
                Bucket=AWS_STORAGE_BUCKET_NAME, 
                Prefix=prefix
            )

        # JSON 파일 추가
        json_files.extend([obj['Key'] for obj in response.get('Contents', []) if not obj['Key'].endswith('/')])

        # 다음 페이지 확인
        if response.get('IsTruncated'):  # 추가 페이지가 있는 경우
            continuation_token = response.get('NextContinuationToken')
        else:
            break

    if not json_files:
        print("이력서 파일이 없습니다.")
        return

    success_count = 0  # 성공한 이력서 처리 횟수
    fail_count = 0  # 실패한 이력서 처리 횟수

    for idx, json_file in enumerate(tqdm(json_files), start=start_index):
        try:
            filename = json_file.split('/')[-1]  # 'resume_001_01.json' 부분만 추출
            parts = filename.replace('.json', '').split('_')  # ['resume', '001', '01']
            
            # 각 부분을 변수로 저장
            page_id = parts[1]  # '001'
            resume_id = parts[2]  # '01'
            processed_data_path = 'processed_json/resume_{:03}_{:02}.json'.format(int(page_id), int(resume_id))
            
            # 이미 존재하는 데이터 확인
            matching_profile_data = ProfileData.objects.filter(processed_data=processed_data_path)
            if matching_profile_data.exists():
                print(f"이미 존재하는 프로필: {processed_data_path}")
                continue

            # S3에서 파일 내용 직접 가져오기
            obj = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=json_file)
            json_data = obj['Body'].read().decode('utf-8')  # 파일 내용을 문자열로 읽기
            dict_data = json.loads(json_data)  # JSON 문자열을 파이썬 딕셔너리로 변환
            
            # 프로필 생성
            create_profile_from_json(page_id, resume_id, dict_data)

            success_count += 1  # 성공한 이력서 처리 횟수를 증가
            print(f"성공: {json_file}")  # 성공한 이력서 파일 이름 출력

        except Exception as e:  # 예외가 발생하면
            fail_count += 1  # 실패한 이력서 처리 횟수를 증가
            print(f"실패 ({json_file}): {str(e)}")  # 실패한 이력서 파일 이름과 예외 메시지를 출력
        
    # 처리 결과를 문자열로 리턴
    result_summary = (
        f"\n처리 완료!\n"
        f"성공: {success_count}개\n"
        f"실패: {fail_count}개\n"
        f"총 처리: {success_count + fail_count}개"
    )
    
    return result_summary


# if __name__ == "__main__":
#     result = db_input_processor(start_index=0)
#     print(result)
