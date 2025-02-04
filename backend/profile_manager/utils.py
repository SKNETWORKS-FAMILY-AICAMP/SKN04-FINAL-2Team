import os
import re
import boto3
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
    client = OpenAI(api_key=api_key)
    
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


def process_company_information(data_path):
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    # S3에서 파일 내용 가져오기
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
    data_path_ = f'{data_path}'
    obj = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=data_path_)
    file_content = obj['Body'].read().decode('utf-8')  # 파일 내용을 문자열로 읽기  
    return file_content
    # 파일 내용을 줄 단위로 분리


def candidate_validation(query, candidate_data):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                'role': 'system',
                'content': '''
                너는 헤드헌터 맞춤형 데이터 검색엔진에서 candidate 선정 이유를 알려주는 AI 봇이야.
                사용자가 입력한 쿼리와 candidate의 정보를 담은 JSON 데이터를 분석하고, 후보자가 선택된 이유를 한 줄로 설명해야 해.
                
                **출력 형식 예시 (반드시 따를 것!)**
                "후보자 (이름)는 ~~같은 이유들로 인하여 선정"
                
                반드시 위와 같은 포맷으로 응답하되, (이름) 부분에는 후보자의 실제 이름을, ~~에는 주요 선정 이유를 포함해야 해.
                '''
            },
            {
                'role': 'user',
                'content': f"사용자 쿼리: {query}, candidate_json 데이터: {candidate_data}"
            }
        ],
        temperature=0.2
    )
    
    # API 응답에서 변환된 결과를 추출
    result = completion.choices[0].message.content.strip()

    return result