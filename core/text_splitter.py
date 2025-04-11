from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_docs(file_path, chunk_size=500, chunk_overlap=20):
    if not file_path.endswith('.epub') and not file_path.endswith('.pdf'):
        return
    loader = loader = UnstructuredEPubLoader(file_path) if file_path.endswith('.epub') else PyMuPDFLoader(file_path)  
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)
