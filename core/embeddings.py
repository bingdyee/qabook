import os
import uuid
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


def ollama_embedding(docs, store_dir="vector-store/", restore_dir=None, model='deepseek-r1:8b'):
    embeddings = OllamaEmbeddings(model=model)
    if restore_dir:
        vectorstore = FAISS.load_local(restore_dir, embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(docs, embeddings)
        vstore_dir = os.path.join(store_dir, model, str(uuid.uuid4()))
        FAISS.save_local(vectorstore, vstore_dir)
    return vectorstore


def restore_vstore(restore_dir="vector-store/deepseek-r1", model='deepseek-r1:8b'):
    embeddings = OllamaEmbeddings(model=model)
    return FAISS.load_local(restore_dir, embeddings, allow_dangerous_deserialization=True)
