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
            model='gpt-4o',
            messages=[
            {
                'role': 'system',
                'content': '''너는 사용자의 입력을 분석하고, 아래 JSON 형식에 맞춰 정확하게 값을 채워주는 AI 어시스턴트야.
                {
                    "Profile": {
                        "name": "프로필 이름 (예: 김철수)",
                        "job_category": "직업 카테고리 (다음 카테고리 중 하나에 해당하면 해당 단어를 사용해줘 [AI 엔지니어, IT 기획자, QA, UIUX 디자이너, 강사, 게임 개발자, 기술 영업, 데이터 분석가, 데이터 사이언티스트, 데이터 엔지니어, 머신러닝 엔지니어, 백엔드 개발자, 보안 담당자, 서버 개발자, 앱 개발자, 풀스택 개발자, 프로젝트 매니저, 프론트엔드 개발자])",
                        "career_year": "경력 연수 (정수 값, 없을경우 0, 직업 카테고리로 쌓인 경력만을 활용해줘)"
                    },
                    "TechStack": [
                        {
                        "tech_stack_name": "기술 스택 이름 (카테고리 분류에 사용할 것이기 때문에 보편적인 기술스택으로 변환해 반환해줘, 예: Python, Django, React )"
                        }
                    ],
                    "Career": [
                        {
                        "company_name": "회사명 (한글 회사명으로 작성해줘, 주식회사 및 (주) 등은 생략해줘, *팀 또는 *동아리 등은 회사로 표현하지 말아줘",
                        "position": "직위 (해당 직무의 업무로 추정되는 하나의 직위만 표현해줘)",
                        "career_start_date": "시작일 (YYYY-MM 형식, 예: 2018-01)",
                        "career_end_date": "종료일 또는 null (YYYY-MM 형식, 예: 2022-12)",
                        "is_currently_employed": "현재 재직 여부 (Boolean 값, 예: True 또는 False)",
                        "career_description": "추가 설명 (예: 해당 직무에서 경험한 내용이 적혀있다면 작성해줘)"
                        }
                    ],
                    "AcademicRecord": [
                        {
                        "school_name": "학교명 (예: 서울대학교)",
                        "major": "전공 (예: 컴퓨터공학)",
                        "degree": "학위 (정수 값 ,0: 고졸, 1: 전문대졸, 2: 학사, 3: 석사, 4: 박사)",
                        "enrollment_date": "입학일 (YYYY-MM 형식, 예: 2014-09)",
                        "graduation_date": "졸업일 또는 null (YYYY-MM 형식, 예: 2018-06)"
                        }
                    ],
                    "Certificate": [
                        {
                        "certificate_name": "자격증 이름 (외국어 관련 자격증은 제외해줘, 예: 정보처리기사, ADsP, 빅데이터 분석기사)"
                        }
                    ],
                    "Language": [
                        {
                        "language_name": "언어 이름 (예: 영어, 스페인어)",
                        "lank" : "언어 수준(예: 상, 중, 하 로만 작성해줘, 상:원어민 중:비즈니스 하:기본대화 정도를 이력서 내용으로 판단해줘)",
                        "language_description": "이력서 내용을 바탕으로 언어 수준에 해당하는 이유 또는 근거 설명을 작성해줘"
                        }
                    ]
                }
                key 에 대응되는 값이 없을경우:
                - 단일 값의 경우 null을 넣어주고,
                - 배열의 경우 빈 배열 []을 넣어줘
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