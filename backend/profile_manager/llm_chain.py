from dotenv import load_dotenv
from utils import reorder_documents
from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
import numpy as np
import template_llm
import joblib
from langchain.retrievers import EnsembleRetriever
import os

load_dotenv()
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
template = template_llm.template

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