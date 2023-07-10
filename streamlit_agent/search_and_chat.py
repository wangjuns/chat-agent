from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import AzureChatOpenAI
import streamlit as st
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

from streamlit_agent.utils import to_langchain_messages
from streamlit_agent.streaming_message import StreamingChatCallbackHandler
from streamlit_agent.hitstory import *
from streamlit_agent.components import *
from streamlit_agent.tools import tool_map


st.set_page_config(page_title="Chat & Agent", page_icon="🦜")
# st.title("Chat")


with st.sidebar:
    # openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    col1, col2 = st.columns([1, 1])
    with col1:
        new_chat_button()
    with col2:
        save_chat_button()

    plugin_selector()
    st.divider()
    history_list()


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    llm = AzureChatOpenAI(
        deployment_name="GPT4-8k",
        openai_api_version="2023-03-15-preview",
        streaming=True,
    )

    if st.session_state["select_plugin"] != "None":
        search_agent = initialize_agent(
            tools=[tool_map[st.session_state["select_plugin"]]],
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            verbose=True,
        )
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
    else:
        with st.chat_message("assistant"):
            chat_box = st.empty()
            st_cb = StreamingChatCallbackHandler(chat_box)

            response = llm(
                messages=to_langchain_messages(st.session_state.messages),
                callbacks=[st_cb],
            )

            st.session_state.messages.append({"role": "assistant", "content": response.content})
