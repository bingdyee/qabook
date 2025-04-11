from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


def retrieve_chunks(query, restore_dir, model='deepseek-r1:8b'):
  embeddings = OllamaEmbeddings(model=model)
  vectorstore = FAISS.load_local(restore_dir, embeddings, allow_dangerous_deserialization=True)
  docs = vectorstore.similarity_search(query, k=3)
  return FAISS.from_documents(docs, embeddings)