import os
from crawling_data_formatter import ResumePreprocessor
from profile_manager.db_input_processor import create_profile_from_json, save_llm_data
import json
from tqdm import tqdm

def process_all_resumes():
    # 1. 이력서 폴더 읽기
    resume_folder = "resume_data"
    resume_files = os.listdir(resume_folder)
    
    if not resume_files:
        print("이력서 파일이 없습니다.")
        return None
    
    # OpenAI API 키 설정
    api_key = "your-api-key-here"
    preprocessor = ResumePreprocessor(api_key)
    
    processed_profiles = []  # 처리된 프로필들을 저장할 리스트
    
    # 모든 이력서 파일 처리
    for resume_file in tqdm(resume_files, desc="이력서 처리 중"):
        resume_path = os.path.join(resume_folder, resume_file)
        
        try:
            # 파일에서 이력서 데이터 읽기
            with open(resume_path, 'r', encoding='utf-8') as file:
                resume_text = file.read()
            
            # GPT를 통한 데이터 구조화
            processed_resume = preprocessor.process_resume(resume_text)
            
            # DB에 저장
            profile = create_profile_from_json(processed_resume)
            processed_profiles.append(profile)  # 프로필 저장
            
            # 원본 데이터와 처리된 데이터 저장
            save_llm_data(
                profile.profile_detail,
                resume_text,
                json.dumps(processed_resume)
            )
            
            print(f"성공: {resume_file}")
            
        except Exception as e:
            print(f"실패 ({resume_file}): {str(e)}")
            continue
    
    print(f"\n처리 완료!")
    print(f"총 처리된 이력서: {len(processed_profiles)}개")
    
    return processed_profiles  # 모든 처리된 프로필 반환

if __name__ == "__main__":
    processed_profiles = process_all_resumes()