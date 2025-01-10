import llm
from dotenv import load_dotenv
import json
import re
from openai import OpenAI
import os
from first import First_filter
import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings

load_dotenv()


def Second_filter(query):
    answer = First_filter(query)
    data = json.loads(answer)
    b = ', '.join(data.get('tech_stack_name'))
    question = b
    response = llm.chain.invoke({
                        'question': question,
                        'language': '한국어'
                    })
    

    db = FAISS.load_local(
    folder_path='save',
    index_name='faiss_etc_data_index',
    embeddings=OpenAIEmbeddings(model='text-embedding-3-small'),
    allow_dangerous_deserialization=True,
    )

    a = db.similarity_search(data.get('etc'), k=5)
    b = []
    for page_contents in a:
        b.append(page_contents.metadata['key'])

    return response, b
