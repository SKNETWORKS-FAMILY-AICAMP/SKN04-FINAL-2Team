import os
from .crawling_data_formatter import ResumePreprocessor

from tqdm import tqdm
import json
import boto3
from dotenv import load_dotenv

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')

# python -m profile_manager.json_processor_by_gpt 
# 위 명령어로 실행
def process_resumes(start_index=0):
    """
    이력서를 처리하는 함수입니다.
    start_index: 시작할 이력서 파일의 인덱스
    """
    crawling_data_formatter = ResumePreprocessor()
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    bucket_name = 'talentbucket01'
    prefix = 'txt/'

    resume_files = []
    continuation_token = None

    # 페이지네이션을 통해 모든 객체를 가져오기
    while True:
        if continuation_token:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, ContinuationToken=continuation_token)
        else:
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        resume_files.extend([obj['Key'] for obj in response.get('Contents', []) if not obj['Key'].endswith('/')])

        if response.get('IsTruncated'):  # 더 많은 객체가 있는지 확인
            continuation_token = response.get('NextContinuationToken')
        else:
            break

    if not resume_files:
        print("이력서 파일이 없습니다.")
        return

    success_count = 0
    fail_count = 0
    
    for idx, resume_file in enumerate(tqdm(resume_files), start=start_index):
        try:
            relative_path = resume_file.replace('txt/', '', 1)
            upload_key = f'processed_json/{os.path.splitext(relative_path)[0]}.json'
            # S3에 동일한 JSON 파일이 있는지 확인
            existing_objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=upload_key)
            if 'Contents' in existing_objects:
                print(f"이미 존재하는 파일: {upload_key}")
                continue

            obj = s3.get_object(Bucket=bucket_name, Key=resume_file)
            resume_text = obj['Body'].read().decode('utf-8')
            
            gpt_result = crawling_data_formatter.process_resume(resume_text)

            start_index = gpt_result.find('{')
            end_index = gpt_result.rfind('}')
            if start_index == -1 or end_index == -1:
                raise ValueError("JSON 데이터가 유효하지 않습니다.")

            json_part = gpt_result[start_index:end_index + 1]
            parsed_data = json.loads(json_part)
            json_data = json.dumps(parsed_data, ensure_ascii=False)

            s3.put_object(Bucket=bucket_name, Key=upload_key, Body=json_data.encode('utf-8'))

            print(f"S3에 업로드 완료: {upload_key}")

            success_count += 1
            print(f"성공: {resume_file}")

        except Exception as e:
            fail_count += 1
            print(f"실패 ({resume_file}): {str(e)}")
            continue
            
    # 처리 결과를 문자열로 리턴
    result_summary = (
        f"\n처리 완료!\n"
        f"성공: {success_count}개\n"
        f"실패: {fail_count}개\n"
        f"총 처리: {success_count + fail_count}개"
    )
    
    return result_summary
    
if __name__ == "__main__":
    result = process_resumes(start_index=0)
    print(result)
