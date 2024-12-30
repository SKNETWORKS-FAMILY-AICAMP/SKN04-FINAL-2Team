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
                {
                    "Profile": {
                        "name": "프로필 이름 (예: 김철수)",
                        "job_category": "직업 카테고리 (예: 소프트웨어 엔지니어, 데이터 사이언티스트 )",
                        "career_year": "경력 연수 (정수 값, 예: 5, 직업 카테고리로 쌓인 경력만을 활용해줘)"
                    },
                    "TechStack": [
                        {
                        "tech_stack_name": "기술 스택 이름 (예: Python, Django, React)"
                        }
                    ],
                    "Career": [
                        {
                        "company_name": "회사명 (예: 테크코퍼레이션)",
                        "position": "직위 (예: Senior Software Engineer, Software Developer, 하나의 직위만 표현해줘)",
                        "start_date": "시작일 (YYYY-MM 형식, 예: 2018-01)",
                        "end_date": "종료일 또는 null (YYYY-MM 형식, 예: 2022-12)",
                        "is_currently_employed": "현재 재직 여부 (Boolean 값, 예: true 또는 false)",
                        "responsibilities": "담당 업무 (예: 웹 애플리케이션 개발 및 유지보수)",
                        "description": "추가 설명 (예: 글로벌 팀 프로젝트를 진행)"
                        }
                    ],
                    "AcademicRecord": [
                        {
                        "school_name": "학교명 (예: 서울대학교)",
                        "major": "전공 (예: 컴퓨터공학)",
                        "status": "졸업 상태 (예: 졸업, 재학, 중퇴)",
                        "enrollment_date": "입학일 (YYYY-MM 형식, 예: 2014-09)",
                        "graduation_date": "졸업일 또는 null (YYYY-MM 형식, 예: 2018-06)"
                        }
                    ],
                    "Certificate": [
                        {
                        "name": "자격증 이름 (예: 정보처리기사, ADsP, 빅데이터 분석기사, 외국어 관련 자격증은 제외해줘)"
                        }
                    ],
                    "Language": [
                        {
                        "language_name": "언어 이름 (예: 영어, 스페인어)",
                        "description": "이력서의 내용으로 해당 언어 능력을 판단해서 꼭 판단 근거와 함께 길게 작성해줘"
                        }
                    ]
                }
                key 에 대응되는 값이 없을경우 key는 남겨두고 value에는 null값을 넣어줘
                '''
            },
            {
                'role': 'user',
                'content': resume_data
            }   
        ],
        temperature=0.4
        )
        
        # API 응답에서 변환된 결과를 추출
        result = completion.choices[0].message.content
        return result