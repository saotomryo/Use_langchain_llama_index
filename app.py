# 以下を「app.py」に書き込み
import streamlit as st
import openai
from dotenv import load_dotenv
load_dotenv()

import os


from langchain import OpenAI
from llama_index import GPTVectorStoreIndex,StorageContext,load_index_from_storage
from langchain.agents import initialize_agent, Tool
from langchain.tools.python.tool import PythonREPLTool
from langchain.chains.conversation.memory import ConversationBufferMemory
import secret_keys  # 外部ファイルにAPI keyを保存

os.environ["OPENAI_API_KEY"] = secret_keys.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ]
    # インデックスの呼び出し
    faq_index = StorageContext.from_defaults(persist_dir="index")
    faq_index = load_index_from_storage(faq_index)
    faq_query_engine = faq_index.as_query_engine()
    
    st.session_state["index_tool"] = Tool(
        name="Index"
        , description="質問に対して回答します。"
        , func=faq_query_engine.query
    )

    st.session_state["agent_executor"]  = initialize_agent(
        tools=[
            PythonREPLTool()
            , st.session_state["index_tool"]
        ]
        , llm=OpenAI(temperature=0)
        , agent="zero-shot-react-description", verbose=True
        , memory=ConversationBufferMemory(memory_key="chat_history")
    )
    

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    answer = {"role": "assistant","content": st.session_state["agent_executor"].run(st.session_state["user_input"])}

    messages.append(answer)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("langchain_llama-indexを利用した内部情報を利用したチャット")

user_input = st.text_input("質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages):  # 直近のメッセージを上に
        speaker = "あなた"
        if message["role"]=="assistant":
            speaker="AI"

        st.write(speaker + ": " + message["content"])
