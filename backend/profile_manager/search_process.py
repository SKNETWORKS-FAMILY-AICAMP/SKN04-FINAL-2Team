from .db_search_process import search_profiles
from typing import Dict, Any, List
from .models import Profile
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def search_process(search_criteria : Dict[str, Any]) -> List[Profile]: 
    try:
        # db_search_process의 search_profiles 함수 호출
        search_results = search_profiles(search_criteria)
        return search_results
        
    except Exception as e:
        # 에러 처리
        print(f"검색 중 오류 발생: {str(e)}")
        return []
    

def get_openai_response(user_input) -> Dict[str, Any]:
    # 환경 변수에서 API 키 가져오기
    api_key = os.getenv("OPENAI_API_KEY")
    
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=api_key)
    
    # 사용자 입력을 메시지로 설정
    PROMPT = [{
                'role': 'system',
                'content': '''
                너는 사용자의 입력을 받아 키워드를 추출하여 아래 JSON 형식에 key에 맞춰 알맞은 value를 넣어주는 AI Assistant 봇이야.

                # **목표(Objective)**  
                - 사용자의 입력을 꼭 아래 틀에 맞게 JSON 형식으로 정리해.  

                # **JSON 형식**  
                {
                    "job_category": "직업 카테고리",
                    "career_year": "경력 연수",
                    "tech_stack_name": "기술 스택 이름, 가능하면 영문 표현으로 보편적으로 표현해야 해(예: python, django)",
                    "language_name": "외국어 능력 이름",
                    "language_lank": "외국어 능력 수준",
                    "initial_company_experience": "회사 설립 초기 경험 유무",
                    "top_tier_startup": "탑 티어 스타트업 경험 유무",
                    "conglomerate": "대기업 경력 유무",
                    "major": "전공",
                    "degree": "학위",
                    "etc": "위 항목에 포함되지 않은 중요 내용을 간결하게 넣어줘, 예를 들어 검색 시스템 구축 경험이 있는 사람이라면 검색 시스템 구축 경험이라고 넣어줘"
                }

                # **주의사항(Constraints)**  
                1. **정확성:** 답변은 주어진 JSON 형식과 일치해야 해.  
                2. **언어:** 답변은 {language}로 작성해야 해.  
                3. **유사도 참조:** 벡터DB를 활용해 가장 유사도가 높은 데이터를 찾아서 대체해서 value값에 넣어야 해  
                4. **숫자 표현:** 이상, 이하, 초과, 미만과 같은 범위는 **숫자**로만 표현해야 해.  
                5. **job_category:**  
                - 아래 카테고리 중 하나에 해당하면 사용하고, 없으면 "None"을 넣어야 해.  
                - **'DevOps 엔지니어', 'QA', '보안 담당자', '프론트엔드 개발자', '게임 개발자', 'UIUX 디자이너', '데브옵스 엔지니어', '풀스택 개발자', '데이터 사이언티스트', '앱 개발자', '데이터 엔지니어', '데이터 분석가', '머신러닝 엔지니어', '기술 영업', 'IT 기획자', '백엔드 개발자', '프로젝트 매니저', 'AI 엔지니어', '서버 개발자', '강사'**  
                6. **career_year:**  
                - 정수로만 표현해야 해 (예: 5)  
                7. **tech_stack_name:**  
                - 만약 유사한 항목이 없으면 "None"으로 넣어줘.  
                8. **language_name:**  
                - 외국어 능력 이름만 적어줘 (예: 영어, 중국어, 일어)  
                9. **language_lank:**  
                - `상`: 원어민 수준  
                - `중`: 비즈니스 수준  
                - `하`: 기본 대화 수준  
                10. **initial_company_experience:**  
                    - 경험이 있으면 True, 없으면 False  
                11. **top_tier_startup:**  
                    - 경험이 있으면 True, 없으면 False
                12. **conglomerate:**  
                    - 경험이 있으면 True, 없으면 False  
                13. **AcademicRecord - major:**  
                    - 사용자 입력 데이터에서 전공으로 해당되는 항목을 넣어주면 돼  
                14. **AcademicRecord - degree:**  
                    - 고졸: 0, 전문학사: 1, 학사: 2, 석사: 3, 박사: 4  
                15. **etc:**  
                    - 특이사항이 없을경우 None을 넣어줘

                # **예시(Example)**  
                ### 입력 예시:  
                "백엔드 엔지니어 경험이 5년 이상이고, python과 django 경험이 있으며, 비즈니스 회화를 하고, 탑 티어 스타트업 경험이 있으며 컴퓨터 관련 전공자이고, 석사 이상이고, 검색 시스템 구축 경험이 있는 사람"

                ### 출력 예시:
                {"job_category":"백엔드 엔지니어","career_year":"5","tech_stack_name":["python","django"],"language_name":"영어","language_rank":"중","initial_company_experience":"False","top_tier_startup":"True","conglomerate":"False","major":"컴퓨터공학과","degree":"3","etc":"검색 시스템 구축 경험이 있는 사람"}  
                '''
            },
            {
                'role': 'assistant',
                'content': '''{"job_category":"프론트 엔지니어","career_year":"5","tech_stack_name":["react","vue"],"language_name":"영어","language_rank":"중","initial_company_experience":"False","top_tier_startup":"True","conglomerate":"False","major":"컴퓨터공학과","degree":"3","etc":"서버 구축 경험이 있는 사람"}
                '''
            },
            {
                'role': 'user',
                'content': '''
                {user_input}
                '''.format(user_input=user_input)
            }]
    
    # OpenAI API 호출
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=PROMPT,
        temperature=0.2
    )
    
    # API 응답에서 변환된 결과를 추출
    result = completion.choices[0].message.content
    return result