from typing import Iterator

import streamlit as st

from streamlit_agent.hitstory import *


def save_current_message():
    current_messages = st.session_state["messages"]
    # save to file
    key = save_message_to_file(
        current_messages,
        key=None if "select_item" not in st.session_state else st.session_state["select_item"],
    )

    chat_session = ChatSession(key=key, content=current_messages)
    # save to session state
    add_messsages_to_history_state(chat_session)
    return key


def new_chat_button():
    if st.button("New Chat"):
        save_current_message()

        del st.session_state.messages
        if "select_item" in st.session_state:
            del st.session_state.select_item


def save_chat_button():
    if st.button("Save Chat"):
        key = save_current_message()
        st.session_state.select_item = key


def plugin_selector():
    plugin = st.selectbox("Plugin", ["None", "Search"])
    st.session_state["select_plugin"] = plugin


def history_list():
    if "history" not in st.session_state:
        st.session_state.history = load_history()

    for h in st.session_state["history"]:
        col1, col2 = st.columns([8, 2])

        with col1:
            st.markdown(h.title)
        with col2:
            st.button(":recycle:", key=f"y_{h.key}", on_click=use_history_messages, args=[h.key])
            st.button(":x:", key=f"x_{h.key}", on_click=remove_history_item, args=[h.key])
        st.divider()
