from chromadb import ChromaClient
from langchain.embeddings import OpenAIEmbeddings
from .models import Profile, TechStack, Career, AcademicRecord, Certificate, Language

class ProfileVectorDB:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.chroma_client = ChromaClient()
        self.vector_stores = {}

    def vectorize_profile(self, profile):
        """Profile 테이블의 각 행을 벡터화"""
        return {
            "content": f"이름: {profile.name}, 직업: {profile.job_category}, 경력 연수: {profile.career_year}",
            "metadata": {
                "profile_id": profile.profile_id,
                "type": "profile"
            }
        }

    def vectorize_tech_stack(self, tech_stack):
        """TechStack 테이블의 각 행을 벡터화"""
        return {
            "content": f"기술스택: {tech_stack.tech_stack_name}",
            "metadata": {
                "profile_id": tech_stack.profile.profile_id,
                "type": "tech_stack"
            }
        }

    def vectorize_career(self, career):
        """Career 테이블의 각 행을 벡터화"""
        content = f"""
        회사명: {career.company_name or ''}
        직위: {career.position or ''}
        담당업무: {career.responsibilities or ''}
        설명: {career.description or ''}
        기간: {career.start_date or ''} ~ {career.end_date or '현재'}
        """
        content = " ".join([line for line in content.splitlines() if line.strip()])
        return {
            "content": content,
            "metadata": {
                "profile_id": career.profile.profile_id,
                "type": "career"
            }
        }

    def build_vector_stores(self):
        """각 테이블별로 벡터 저장소 구축"""
        table_configs = {
            'profile': (Profile.objects.all(), self.vectorize_profile),
            'tech_stack': (TechStack.objects.all(), self.vectorize_tech_stack),
            'career': (Career.objects.all(), self.vectorize_career),
            # Add other models as needed
        }

        for table_name, (queryset, vectorize_func) in table_configs.items():
            documents = []
            for row in queryset:
                doc = vectorize_func(row)
                documents.append(doc)

            if documents:
                self.chroma_client.insert(
                    collection_name=table_name,
                    documents=[doc["content"] for doc in documents],
                    metadatas=[doc["metadata"] for doc in documents]
                )
                self.vector_stores[table_name] = table_name

    def search(self, query: str, table_name: str = None, k: int = 5):
        """벡터 검색 수행"""
        if table_name and table_name in self.vector_stores:
            results = self.chroma_client.search(
                collection_name=table_name,
                query=query,
                top_k=k
            )
            return [(doc, score, table_name) for doc, score in results]
        
        all_results = []
        for table_name in self.vector_stores:
            results = self.chroma_client.search(
                collection_name=table_name,
                query=query,
                top_k=k
            )
            all_results.extend([(doc, score, table_name) for doc, score in results])
        
        return sorted(all_results, key=lambda x: x[1])[:k]