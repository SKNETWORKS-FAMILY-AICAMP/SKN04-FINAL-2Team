from .db_search_process import search_profiles
from typing import Dict, Any, List
from .models import Profile

def search_process(search_criteria : Dict[str, Any]) -> List[Profile]: 
    try:
        # db_search_process의 search_profiles 함수 호출
        search_results = search_profiles(search_criteria)
        return search_results
        
    except Exception as e:
        # 에러 처리
        print(f"검색 중 오류 발생: {str(e)}")
        return []