import os
import re
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_transformers import LongContextReorder
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


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