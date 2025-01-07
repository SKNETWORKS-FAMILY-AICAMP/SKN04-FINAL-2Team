import os
from langchain_openai.embeddings import OpenAIEmbeddings
from utils import load_documents_from_folder, split_documents
import joblib
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import TextLoader



load_dotenv()



folder_path = r"C:\Users\USER\Documents\직무종류"

documents = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(folder_path, filename), encoding='utf-8')
        documents.extend(loader.load())
splitted_documents = split_documents(documents)

chroma_db = Chroma.from_documents(
    splitted_documents,
    embedding = OpenAIEmbeddings(model='text-embedding-3-small'),
    collection_name="example_collection",
    persist_directory='./save'
)

retriever = BM25Retriever.from_documents(
    splitted_documents,
    embedding = OpenAIEmbeddings(model='text-embedding-3-small'),
    collection_name="example_collection",
    
)

joblib.dump(retriever, './save/bm25_retriever_model.pkl')