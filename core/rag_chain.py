from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama

from core.retriever import retrieve_chunks

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


def get_rag_response(query, model='deepseek-r1:8b'):
  prompt = PromptTemplate.from_template(prompt_template)
  retrieved_chunks = retrieve_chunks(query, restore_dir="vector-store/deepseek-r1")
  # context = "\n".join([chunk.page_content for chunk in retrieved_chunks])
  chain = RetrievalQA.from_chain_type(
      llm=ChatOllama(model=model),
      retriever=retrieved_chunks.as_retriever(), 
      chain_type="stuff",
      return_source_documents=True,  
      chain_type_kwargs={'prompt': prompt} 
  )
  response = chain.invoke({'query': query})
  return response['result']

