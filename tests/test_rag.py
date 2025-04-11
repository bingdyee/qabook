import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.text_splitter import extract_docs
from core.embeddings import ollama_embedding
from core.rag_chain import get_rag_response 


def embed():
  docs = extract_docs('example/9787115592316.epub')
  ollama_embedding(docs)


rs = get_rag_response("如何快速成稿？")
print(rs)