from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_ollama import ChatOllama

from core.embeddings import restore_vstore

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


def rag_chain(model='deepseek-r1:8b'):
    prompt = PromptTemplate.from_template(prompt_template)
    vstore = restore_vstore(model=model, restore_dir="vector-store/deepseek-r1")
    return RetrievalQA.from_chain_type(
        llm=ChatOllama(model=model),
        retriever=vstore.as_retriever(),
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
