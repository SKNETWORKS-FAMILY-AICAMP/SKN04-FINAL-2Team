from dotenv import load_dotenv
import json
import re
from openai import OpenAI
import os
import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from .utils import reorder_documents
from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_chroma import Chroma
import numpy as np
import joblib
from langchain.retrievers import EnsembleRetriever

load_dotenv()

prompt_template = '''
# **역할(Role)**  
너는 사용자의 "tech_stack_name" 입력을 받아 벡터DB를 참조하여 유사한 값으로 변환해주는 AI assistant 봇이야.

# **목표(Objective)**  
- 사용자의 입력을 꼭 벡터DB를 참고하여 유사한 값으로 반환해야해. 
- 알맞은 값이 없을 경우 "None"으로 채워야 해.

# 답변 형식**  

tech_stack_name

# **주의사항(Constraints)**  
1. **정확성:** 답변은 주어진 형식과 일치해야 해.  
2. **언어:** 답변은 {language}로 작성해야 해.  
3. **유사도 참조:** 벡터DB를 활용해 가장 유사도가 높은 데이터를 찾아서 대체해서 값에 넣어야해  
4. **tech_stack_name:**  
   - tech_stack_name은 벡터DB의 값을 참고해 가장 유사한 항목으로 변환해야 해.  
   - 만약 유사한 항목이 없으면 "None"으로 넣어줘.  
# **예시(Example)**  

### 입력 예시:
"장고"

### 출력 예시:
    "django"

# **사용자 입력:**  
{question}
'''

db_chroma = Chroma(
    collection_name="example_collection",
    embedding_function = OpenAIEmbeddings(model='text-embedding-3-small'),
    persist_directory= os.path.join(os.getcwd(), 'save')
)

bm_retriever = joblib.load(os.path.join(os.getcwd(), 'save', 'bm25_retriever_model.pkl'))

retriever_chroma = db_chroma.as_retriever(search_type="mmr", search_kwargs={'k': 1, 'lambda_mult': 0.0})

ensemble_retriever = EnsembleRetriever(
        retrievers=[bm_retriever, retriever_chroma],
        weights=[0.5, 0.5]
    )
template = prompt_template

prompt = PromptTemplate.from_template(template)

model = ChatOpenAI(model_name='gpt-4o')

parser = StrOutputParser()

chain = (
    {
        'reference': itemgetter('question')
        | ensemble_retriever
        | RunnableLambda(reorder_documents),
        'question': itemgetter('question'),
        'language': itemgetter('language'),
    }
    | prompt
    | model
    | parser
)

def second_filter(answer):
    response = []
    data = json.loads(answer)
    for i in data.get('tech_stack_name'):
        response.append(chain.invoke({
                            'question': i,
                            'language': '한국어'
                        }))
        
    response = [item.strip('"').strip().replace('\\', '') for item in response]
    data['tech_stack_name'] = response
    answer = json.dumps(data, ensure_ascii=False)

    return answer

