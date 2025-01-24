import os
import re

from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_transformers import LongContextReorder
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
import numpy as np

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def reorder_documents(documents):
    context_reorder = LongContextReorder()
    
    documents_reordered = context_reorder.transform_documents(documents)
    
    documents_joined = '\n'.join([document.page_content for document in documents_reordered])

    return documents_joined


def modify_file_name(file_name: str):
    modified_name = re.sub(r"\(.*?\)", "", file_name)
    return modified_name.strip()

def load_documents_from_folder(folder_path: str):
    documents = []
    docx_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    for file_name in docx_files:
        file_path = os.path.join(folder_path, file_name)
        loader = UnstructuredWordDocumentLoader(file_path)
        try:
            modified_file_name = modify_file_name(os.path.splitext(file_name)[0])
            document = loader.load()
            for doc in document:
                if "source" in doc.metadata:
                    del doc.metadata["source"]
                doc.metadata["file_name"] = modified_file_name
                documents.append(doc)
        except Exception as e:  
            print(f"Error occurred while loading {file_name}: {e}")

    return documents

def split_documents(documents: list, chunk_size=100, chunk_overlap=50):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    splitted_documents = []
    for document in documents:
        splitted_texts = text_splitter.split_text(document.page_content)
        
        splitted_documents.extend(
            Document(page_content=text, metadata=document.metadata)
            for text in splitted_texts
        )
    
    return splitted_documents


VALID_JOB_CATEGORIES = [
    "AI 엔지니어", "IT 기획자", "큐에이", "UIUX 디자이너", "강사", "게임 개발자",
    "기술 영업", "데이터 분석가", "데이터 사이언티스트", "데이터 엔지니어", "머신러닝 엔지니어",
    "백엔드 개발자", "보안 담당자", "서버 개발자", "앱 개발자", "풀스택 개발자",
    "프로젝트 매니저", "프론트엔드 개발자"
]


def get_embedding(text: str) -> np.ndarray:
    client = OpenAI.Client(api_key=api_key)
    
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    
    # 최신 API에서는 리스트에서 'embedding' 값 추출이 필요
    return np.array(response.data[0].embedding)

# 표준 직업 카테고리 임베딩 미리 생성
category_embeddings = {category: get_embedding(category) for category in VALID_JOB_CATEGORIES}

# 유사도 계산 함수 (코사인 유사도)
def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 유사 직업 카테고리 찾기 함수
def get_best_match(input_category: str) -> str:
    if input_category == 'None':
        return 'None'
    input_embedding = get_embedding(input_category)
    similarities = {category: cosine_similarity(input_embedding, emb) for category, emb in category_embeddings.items()}
    
    # 가장 높은 유사도를 가진 직업 카테고리 선택
    best_match = max(similarities, key=similarities.get)
    return best_match if similarities[best_match] > 0.75 else 'None'