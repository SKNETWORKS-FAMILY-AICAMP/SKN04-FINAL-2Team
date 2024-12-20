import os  # 운영체제와 상호작용하는 기능을 제공하는 모듈
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .crawling_data_formatter import ResumePreprocessor  # 이력서 데이터를 처리하는 클래스
from .db_profile_processor import ProfileCreator

from tqdm import tqdm  # 진행 상태를 표시하는 라이브러리
import json  # JSON 데이터를 처리하는 모듈


def process_all_resumes(start_index=0, batch_size=10):
    """
    모든 이력서를 처리하는 함수입니다.
    start_index: 시작할 이력서 파일의 인덱스
    batch_size: 한 번에 처리할 이력서 파일의 수
    """
    crawling_data_formatter = ResumePreprocessor()
 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    resume_folder = os.path.join(BASE_DIR, 'resume_data')

    if not os.path.exists(resume_folder):
        os.makedirs(resume_folder)
    # resume_folder = "./resume_data"  # 이력서 데이터가 저장된 폴더 경로
    resume_files = sorted(os.listdir(resume_folder))  # 이력서 폴더 내부의 모든 파일을 정렬된 리스트로 가져옵니다.
    
    if not resume_files:
        print("이력서 파일이 없습니다.")  # 이력서 파일이 없으면 메시지를 출력합니다.
        return
    
    # 처리할 파일 범위를 지정합니다.
    if batch_size:
        resume_files = resume_files[start_index:start_index + batch_size]  # batch_size만큼의 이력서 파일을 선택합니다.
    else:
        resume_files = resume_files[start_index:]  # batch_size가 지정되지 않으면 모든 이력서 파일을 선택합니다.

    success_count = 0  # 성공한 이력서 처리 횟수
    fail_count = 0  # 실패한 이력서 처리 횟수
    
    for resume_file in tqdm(resume_files, desc="이력서 처리 중"):  # 이력서 파일을 tqdm으로 처리합니다.
        resume_path = os.path.join(resume_folder, resume_file)  # 이력서 파일의 전체 경로를 생성합니다.
        
        try:
            with open(resume_path, 'r', encoding='utf-8') as file:  # 이력서 파일을 읽기 모드로 열고, 내용을 읽습니다.
                resume_text = file.read()
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
            
            # profile = create_profile_from_json(gpt_result)  # GPT 결과를 JSON으로 변환하여 프로필을 생성합니다.
            
            # save_llm_data(
            #     profile.profile_detail,
            #     resume_text,
            #     json.dumps(processed_resume)
            # )  # LLM 데이터를 저장하는 코드입니다. (현재 주석 처리)
            
            success_count += 1  # 성공한 이력서 처리 횟수를 증가시킵니다.
            print(f"성공: {resume_file}")  # 성공한 이력서 파일 이름을 출력합니다.

        except Exception as e:  # 예외가 발생하면
            fail_count += 1  # 실패한 이력서 처리 횟수를 증가시킵니다.
            print(f"실패 ({resume_file}): {str(e)}")  # 실패한 이력서 파일 이름과 예외 메시지를 출력합니다.
            continue  # 다음 이력서 파일로 넘어갑니다.
        
    
    print(f"\n처리 완료!")  # 모든 이력서 처리가 완료되었습니다.
    print(f"성공: {success_count}개")  # 성공한 이력서 처리 횟수를 출력합니다.
    print(f"실패: {fail_count}개")  # 실패한 이력서 처리 횟수를 출력합니다.
    print(f"총 처리: {success_count + fail_count}개")  # 총 이력서 처리 횟수를 출력합니다.
    
    return profile  # 처리된 마지막 프로필을 반환합니다.
    
if __name__ == "__main__":
    # 전체 처리
    # process_all_resumes()
    
    # 또는 특정 범위만 처리
    result = process_all_resumes(start_index=2, batch_size=10)  # 처음 1개만 처리
    print(result)
