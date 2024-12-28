import os  # 운영체제와 상호작용하는 기능을 제공하는 모듈
import django
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from .crawling_data_formatter import ResumePreprocessor  # 이력서 데이터를 처리하는 클래스
from .db_profile_processor import ProfileCreator

from tqdm import tqdm  # 진행 상태를 표시하는 라이브러리
import json  # JSON 데이터를 처리하는 모듈


def process_all_resumes(start_index=0):
    """
    모든 이력서를 처리하는 함수입니다.
    start_index: 시작할 이력서 파일의 인덱스
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
    
    # resume_files = resume_files[start_index:]  # start_index부터 모든 이력서 파일을 선택합니다.

    success_count = 0  # 성공한 이력서 처리 횟수
    fail_count = 0  # 실패한 이력서 처리 횟수
    
    for idx, resume_file in enumerate(tqdm(resume_files), start=start_index):
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
