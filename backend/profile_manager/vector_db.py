from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from .models import *

class ProfileVectorDB:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_stores = {}

    def vectorize_profile_detail(self, detail):
        """Profile_Detail 테이블의 각 행을 벡터화"""
        return {
            "content": f"""
            간단소개: {detail.brief_introduction}
            자기소개: {detail.introduction}
            """,
            "metadata": {
                "id": detail.id,
                "profile_id": detail.profile.profile_id,
                "type": "introduction"
            }
        }

    def vectorize_skill(self, skill):
        """Skill 테이블의 각 행을 벡터화"""
        return {
            "content": f"기술스택: {skill.name}",
            "metadata": {
                "profile_id": skill.profile.profile_id,
                "type": "skill"
            }
        }

    def vectorize_career(self, career):
        """Career 테이블의 각 행을 벡터화"""
        content = f"""
        회사명: {career.company_name or ''}
        직위: {career.position or ''}
        근무형태: {career.employment_type or ''}
        담당업무: {career.responsibilities or ''}
        설명: {career.description or ''}
        기간: {career.start_date or ''} ~ {career.end_date or '현재'}
        """
        # 비어있는 항목의 키와 항목을 제외
        content = " ".join([line for line in content.splitlines() if line.strip()])
        return {
            "content": content,
            "metadata": {
                "id": career.id,
                "profile_id": career.profile.profile_id,
                "type": "experience"
            }
        }

    def vectorize_activity(self, activity):
        """Activity 테이블의 각 행을 벡터화"""
        content = f"""
        활동명: {activity.activity_name or ''}
        기관명: {activity.organization_name or ''}
        활동내용: {activity.description or ''}
        활동연도: {activity.activity_year or ''}
        """
        # 비어있는 항목의 키와 항목을 제외
        content = " ".join([line for line in content.splitlines() if line.strip()])
        return {
            "content": content,
            "metadata": {
                "id": activity.id,
                "profile_id": activity.profile.profile_id,
                "type": "activity"
            }
        }

    def build_vector_stores(self):
        """각 테이블별로 벡터 저장소 구축"""
        # 각 테이블별 데이터와 벡터화 함수 매핑
        table_configs = {
            'profile_detail': (Profile_Detail.objects.all(), self.vectorize_profile_detail),
            'skill': (Skill.objects.all(), self.vectorize_skill),
            'career': (Career.objects.all(), self.vectorize_career),
            'activity': (Activity.objects.select_related('profile__profile').all(), self.vectorize_activity),
            'academic': (AcademicBackground.objects.select_related('profile__profile').all(), self.vectorize_academic),
            'project': (ParticipatedProject.objects.select_related('profile__profile').all(), self.vectorize_project),
            'certificate': (Certificate.objects.select_related('profile__profile').all(), self.vectorize_certificate),
            'education': (EducationContent.objects.select_related('profile__profile').all(), self.vectorize_education),
            'language': (Language.objects.select_related('profile__profile').all(), self.vectorize_language)
        }

        # 각 테이블별로 벡터 저장소 생성
        for table_name, (queryset, vectorize_func) in table_configs.items():
            documents = []
            for row in queryset:
                doc = vectorize_func(row)
                documents.append(doc)

            if documents:
                vector_store = FAISS.from_texts(
                    texts=[doc["content"] for doc in documents],
                    embedding=self.embeddings,
                    metadatas=[doc["metadata"] for doc in documents]
                )
                self.vector_stores[table_name] = vector_store
                vector_store.save_local(f"vector_store_{table_name}")

    def search(self, query: str, table_name: str = None, k: int = 5):
        """벡터 검색 수행"""
        if table_name and table_name in self.vector_stores:
            # 특정 테이블에서만 검색
            results = self.vector_stores[table_name].similarity_search_with_score(query, k=k)
            return [(doc, score, table_name) for doc, score in results]
        
        # 전체 테이블에서 검색
        all_results = []
        for table_name, store in self.vector_stores.items():
            results = store.similarity_search_with_score(query, k=k)
            all_results.extend([(doc, score, table_name) for doc, score in results])
        
        # 유사도 점수로 정렬하여 상위 k개 반환
        return sorted(all_results, key=lambda x: x[1])[:k]