from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import os
# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키를 환경 변수에서 가져옴
api_key = os.getenv("OPENAI_API_KEY")

class ResumePreprocessor:
    def __init__(self, batch_size=1):
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
                {"profile":{"name":,"job":,"email":,"phone":,"address":,"birth_date":},"profile_detail":{"brief_introduction":,"introduction":},"skills":[{"name":}],"careers":[{"company_name":,"position":,"start_date":,"end_date":,"employment_type":,"responsibilities":,"description":}],"activities":[{"activity_name":,"organization_name":,"description":,"activity_year":}],"academic_backgrounds":[{"school_name":,"major":,"status":,"start_date":,"end_date":}],"participated_projects":[{"project_name":,"project_role":,"organization_name":,"start_date":,"end_date":}],"certificates":[{"name":,"acquisition_date":,"issuing_org":}],"education_contents":[{"education_name":,"description":}],"urls":[{"link":}],"languages":[{"description":}]}
                사용자 입력 데이터를 json 형식에 맞춰서 바꿔줘 단 key 에 대응되는 값이 없을경우 key는 남겨두고 value에는 null값을 넣어줘
                날짜는 YYYY-MM-DD 형식으로 바꿔줘
                link는 링크주소가 아닌 한글형식이면 넣지 말아줘
                '''
            },
            {
                'role': 'user',
                'content': resume_data
            }   
        ],
        temperature=0.5
        )
        
        # API 응답에서 변환된 결과를 추출
        result = completion.choices[0].message.content
        return result