from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

class ResumePreprocessor:
    def __init__(self, batch_size=10):
        self.client = OpenAI(api_key=api_key)
        self.batch_size = batch_size
        
    def process_resume(self, resume_data):
        # 단일 이력서 처리
        completion = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
            {
                'role': 'system',
                'content': '''너는 관련된 내용을 아래 json 형식에 맞춰 바꿔주는 봇이야
                {
                    "profile": {
                        "name": "",
                        "job": "",
                        "email": "",
                        "phone": "",
                        "address": "",
                        "birth_date": ""
                    },
                    "profile_detail": {
                        "brief_introduction": "",
                        "introduction": ""
                    },
                    "skills": [
                        {"name": ""}
                    ],
                    "careers": [
                        {
                            "company_name": "",
                            "position": "",
                            "start_date": "",
                            "end_date": "",
                            "employment_type": "",
                            "responsibilities": "",
                            "description": ""
                        }
                    ],
                    "activities": [
                        {
                            "activity_name": "",
                            "organization_name": "",
                            "description": "",
                            "activity_year": ""
                        }
                    ],
                    "academic_backgrounds": [
                        {
                            "school_name": "",
                            "major": "",
                            "status": "",
                            "start_date": "",
                            "end_date": ""
                        }
                    ],
                    "participated_projects": [
                        {
                            "project_name": "",
                            "project_role": "",
                            "organization_name": "",
                            "start_date": "",
                            "end_date": ""
                        }
                    ],
                    "certificates": [
                        {
                            "name": "",
                            "acquisition_date": "",
                            "issuing_org": ""
                        }
                    ],
                    "education_contents": [
                        {
                            "education_name": "",
                            "description": ""
                        }
                    ],
                    "urls": [
                        {
                            "link": ""
                        }
                    ],
                    "languages": [
                        {
                            "description": ""
                        }
                    ]
                }
                사용자 입력 데이터를 위 틀에 맞춰서 바꿔줘 단 key 에 대응되는 값이 없을경우 key는 남겨두고 value에는 None값을 넣어줘
                '''
            },
            {
                'role': 'user',
                'content': resume_data
            }   
        ],
        response_format={ "type": "json_object" },
        temperature=0.0
        )
        return completion
    
    def process_multiple_resumes(self, resume_list):
        # 여러 이력서 일괄 처리
        processed_resumes = []
        
        for i in tqdm(range(0, len(resume_list), self.batch_size), desc="이력서 처리 중"):
            batch = resume_list[i:i + self.batch_size]
            for resume_data in batch:
                try:
                    processed = self.process_resume(resume_data)
                    processed_resumes.append(processed)
                except Exception as e:
                    print(f"처리 중 오류 발생: {e}")
                    continue
                    
        return processed_resumes