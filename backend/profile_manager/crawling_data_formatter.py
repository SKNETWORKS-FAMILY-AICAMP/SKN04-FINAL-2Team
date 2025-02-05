from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import os
import numpy as np
from langchain_community.vectorstores import FAISS
import json
from langchain_openai.embeddings import OpenAIEmbeddings
from utils import get_best_match
# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키를 환경 변수에서 가져옴
api_key = os.getenv("OPENAI_API_KEY")

tech_stack_db = FAISS.load_local(
    folder_path="save",
    index_name='faiss_tech_stack_name_data_index',
    embeddings=OpenAIEmbeddings(model='text-embedding-ada-002'),
    allow_dangerous_deserialization=True,
    )

class ResumePreprocessor:
    def __init__(self, batch_size=1):
        self.client = OpenAI(api_key=api_key)
        self.batch_size = batch_size
        
    def process_resume(self, resume_data):
        # 단일 이력서 처리
        completion = self.client.chat.completions.create(
            model='gpt-4',
            messages=[
            {
                'role': 'system',
                'content': '''너는 사용자의 입력을 분석하고, 아래 JSON 형식에 맞춰 정확하게 값을 채워주는 AI 어시스턴트야.
                {
                    "Profile": {
                        "name": "프로필 이름 (예: 김철수)",
                        "total_career_year": "총 경력 연수 (정수 값, 없을경우 0, 모든 경력 기간을 더해줘.)"
                    },
                    "TechStack": [
                        {
                        "tech_stack_name": "기술 스택 이름 (카테고리 분류에 사용할 것이기 때문에 보편적인 기술스택으로 변환해서서 반환해줘, 예: Python, Django, React )"
                        }
                    ],
                    "Career": [
                        {
                        "company_name": "회사명 (한글 회사명으로 작성해줘, 주식회사 및 (주) 등은 생략해줘, *팀 또는 *동아리 *아카데미 등은 company_name으로 넣지 말아줘.",
                        "job_category": "직업 카테고리 (다음 카테고리 중 하나에 해당하면 해당 단어를 사용해줘 [AI 엔지니어, IT 기획자, QA, UIUX 디자이너, 강사, 게임 개발자, 기술 영업, 데이터 분석가, 데이터 사이언티스트, 데이터 엔지니어, 머신러닝 엔지니어, 백엔드 개발자, 보안 담당자, 서버 개발자, 앱 개발자, 풀스택 개발자, 프로젝트 매니저, 프론트엔드 개발자])",
                        "career_year": "경력 연차 (정수 값, 없을경우 0, 이 회사에서 다닌 경력 연차차를 기재해줘.)",
                        "tech_stack_name": "기술 스택 이름들 나열 단 영어로 변환환",
                        "position": "직위 (해당 직무의 업무로 추정되는 하나의 직위만 표현해줘)",
                        "career_start_date": "시작일 (YYYY-MM 형식, 예: 2018-01)",
                        "career_end_date": "종료일 또는 null (YYYY-MM 형식, 예: 2022-12)",
                        "is_currently_employed": "현재 재직 여부 (Boolean 값, 예: True 또는 False)",
                        "career_description": "수행 업무에 대해서 정리해서 작성해줘"
                        }
                    ],
                    "AcademicRecord": [
                        {
                        "school_name": "학교명 (예: 서울대학교)",
                        "major": "전공 (예: 컴퓨터공학)",
                        "degree": "학위 (정수 값 ,고졸: 0, 전문대졸: 1, 학사: 2, 석사: 3, 박사: 4)",
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
                - 각 career_description에 내용 중 경험을 요약해서 "~~했던 경험이 있음" 형식으로 작성해줘.
                - 각 position은 직위를 파악해서 ['엔트리 개발자', '중급 개발자', '상급 개발자', '매니저', '임원'] 이 리스트에 포함된 값으로 작성해줘
                - 모든 value는 key와 매칭하여 **resume**에서 명확하게 명시 되지 않았으면 None 또는 []으로 넣어줘
                - tech_stack_name 값은 영어로 변환해서 작성해줘
                - Career에는 회사에서 일해본 경력을 근거로 작성해줘
                - Career에 career_year = career_end_date - career_start_data + 1년 'career_end_date'가 None일 경우 career_end_date를 오늘 날짜로 가정하고 계산해줘.
                - career_year 구하기 위해 계산 제대로해. (예시 : career_start_date: 2023-11, career_end_date: None -> (오늘 날짜) - (2023.11) + 1년 -> (2025.01) - (2023.11) + 1년 = 2년 2개월 -> 연차만 남기면 정답은 2)
                '''
            },
            {
                'role': 'user',
                'content': resume_data
            }   
        ],
        temperature=0.1
        )

        # API 응답에서 변환된 결과를 추출
        result = completion.choices[0].message.content
        try:
            result = json.loads(result.replace('\n', ' ').replace('```json', '').replace('```','').replace('\\', '/').strip())

            if result['Career']:
                for i in range(len(result['Career'])):
                    if result['Career'][i]['job_category']:
                        input_jobs = result['Career'][i]['job_category']
                        standardized_job = get_best_match(input_jobs)
                        result['Career'][i]['job_category'] = standardized_job
                
            if result['TechStack']:
                for i in range(len(result['TechStack'])):
                    if tech_stack_db.similarity_search_with_relevance_scores(result['TechStack'][i]['tech_stack_name'], k=1)[0][1] > 0.8:
                        result['TechStack'][i]['tech_stack_name'] = tech_stack_db.similarity_search_with_relevance_scores(result['TechStack'][i]['tech_stack_name'], k=1)[0][0].page_content
                        
            if result['Career']:
                for i in range(len(result['Career'])):
                    if result['Career'][i]['tech_stack_name']:
                        tech = []
                        k = result['Career'][i]['tech_stack_name'].split(', ')
                        for j in k:
                            if tech_stack_db.similarity_search_with_relevance_scores(j, k=1)[0][1] > 0.8:
                                tech.append(tech_stack_db.similarity_search_with_relevance_scores(j, k=1)[0][0].page_content)
                            else:
                                tech.append(j)
                        result['Career'][i]['tech_stack_name'] = ', '.join(tech)
                        
        except (json.JSONDecodeError, TypeError) as e:
            print(f"JSON 디코딩 오류: {e}")
        except Exception as e:
            print(f"예상치 못한 오류 발생: {e}")
        return result