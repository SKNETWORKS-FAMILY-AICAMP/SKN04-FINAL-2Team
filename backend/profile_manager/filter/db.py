import os
from langchain_openai.embeddings import OpenAIEmbeddings
from backend.profile_manager.filter.utils import load_documents_from_folder, split_documents
import joblib
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_loaders import TextLoader
from data import data
import faiss
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()



folder_path = r"C:\Users\USER\Documents\백터db에 넣을 데이터"

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


keys = []
values = []
for i in data:
    a = i.split(':')
    keys.append(a[0])
    if a[1] == 'none' or a[1] == 'None':
        values.append('')
    else:
        values.append(a[1])


loader = TextLoader('asd.txt')

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
)
documents = loader.load_and_split(text_splitter)

db = FAISS.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings(model='text-embedding-3-small'),
)

db.delete([db.index_to_docstore_id[0]])

db.save_local(
    folder_path='save',
    index_name='faiss_etc_data_index',
)
