import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler

from core.rag_chain import rag_chain


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


@st.cache_resource
def get_rag_chain():
    print("Getting rag_chain...")
    return rag_chain(), ChatMessageHistory()


def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "针对本书提出你的问题"}]


st.title("QABook")
st.caption("🚀 A streamlit chatbot powered by Ollama LLM")

chain, chat_history = get_rag_chain()
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "针对本书提出你的问题"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner(text='思考中...'):
            placeholder = st.empty()
            chat_history.clear()
            for message in st.session_state.messages:
                if 'assistant' == message['role']:
                    chat_history.add_ai_message(message['content'])
                if 'user' == message['role']:
                    chat_history.add_user_message(message['content'])
            response = chain.invoke(prompt, config={"callbacks": [StreamHandler(placeholder)]})
        message = {"role": "assistant", "content": response['result']}
        st.session_state.messages.append(message)
