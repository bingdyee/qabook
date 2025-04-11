import os
import uuid
from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

from core.utils import log_time


prompt_template = """
### System:
You are an honest reading assistant.
You will accept content of a book and you will answer the question asked by the user appropriately.
If you don't know the answer, just say you don't know. Don't try to make up an answer.

### Context:
{context}

### User:
{question}

### Response:
"""


class BookReader:

    def __init__(self, model, chunk_size=1000, store_dir="langchain-store/vectorstore/"):
        self.chunk_size = chunk_size
        self._model = model
        self._store_dir = store_dir
        self.chain = None

    @log_time
    def _extract_docs(self, file_path):
        if not file_path.endswith('.epub') and not file_path.endswith('.pdf'):
            return
        loader = loader = UnstructuredEPubLoader(file_path) if file_path.endswith('.epub') else PyMuPDFLoader(file_path)  
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=0) 
        return text_splitter.split_documents(documents)[:3]
    
    @log_time
    def learn(self, file_path=None, restore_dir=None):
        """
        Embed the content of the book and store it in a vectorstore.
        """
        embeddings = OllamaEmbeddings(model=self._model)
        if restore_dir:
            restore_dir = os.path.join(self._store_dir, self._model, restore_dir)
            vectorstore = FAISS.load_local(restore_dir, embeddings, allow_dangerous_deserialization=True)
        else:
            documents = self._extract_docs(file_path)
            vectorstore = FAISS.from_documents(documents, embeddings) 
            vstore_dir = os.path.join(self._store_dir, self._model, str(uuid.uuid4()))
            FAISS.save_local(vectorstore, vstore_dir)
        prompt = PromptTemplate.from_template(prompt_template)
        self.chain = RetrievalQA.from_chain_type(
            llm=ChatOllama(model=self._model),
            retriever=vectorstore.as_retriever(), 
            chain_type="stuff",
            return_source_documents=True,  
            chain_type_kwargs={'prompt': prompt} 
        )

    def query(self, text):
        if not self.chain:
            return
        response = self.chain.invoke({'query': text})
        return response['result']
