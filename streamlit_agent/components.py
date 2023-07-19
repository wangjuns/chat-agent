from typing import Iterator

import streamlit as st

from streamlit_agent.hitstory import *
from streamlit_agent.tools import tool_map


system_chat = {"role": "assistant", "content": "How can I help you?"}


def save_current_chat(chat: List[dict[str, str]]):
    if "chat_key" not in st.session_state:
        st.session_state.chat_key = generate_chat_session_key()
        # save system setting first.
        append_message_to_file(system_chat, st.session_state.chat_key)

    append_message_to_file(chat, st.session_state.chat_key)

    current_messages = st.session_state["messages"]
    chat_session = ChatSession(key=st.session_state.chat_key, content=current_messages)
    # save to session state
    add_messsages_to_history_state(chat_session)
    return st.session_state.chat_key


def new_chat_button():
    if st.button("New Chat"):
        # save_current_message()

        del st.session_state.messages
        if "chat_key" in st.session_state:
            del st.session_state.chat_key


def plugin_selector():
    plugin = st.selectbox("Plugin", ["None"] + list(tool_map.keys()))
    st.session_state["select_plugin"] = plugin


def history_list():
    if "history" not in st.session_state:
        st.session_state.history = load_history()

    for h in st.session_state["history"]:
        col1, col2 = st.columns([8, 2])

        with col1:
            st.markdown(h.title)
        with col2:
            st.button(
                ":recycle:",
                key=f"y_{h.key}",
                on_click=use_history_messages,
                args=[h.key],
            )
            st.button(":x:", key=f"x_{h.key}", on_click=remove_history_item, args=[h.key])
        st.divider()
