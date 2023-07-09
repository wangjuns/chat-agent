import json
import os
from typing import List
import time
import streamlit as st
from pydantic import BaseModel


history_data_store_path = "data"
if not os.path.exists(history_data_store_path):
    os.mkdir(history_data_store_path)


class ChatSession(BaseModel):
    """
    single chat session content.
    contains multiple chat pair.
    """

    key: str
    content: List[dict[str, str]]

    @property
    def title(self):
        # use first user quesion as chat session title
        for message in self.content:
            if message["role"] == "user":
                return message["content"]
        return ""


def load_history_item(file_name: str) -> ChatSession:
    with open(f"{history_data_store_path}/{file_name}", "r") as f:
        content = f.read()
        messages = json.loads(content)
        return ChatSession(key=file_name.split(".")[0], content=messages)


def remove_history_item(key: str):
    print(f"remove key {key}")
    st.session_state["history"] = [h for h in st.session_state["history"] if h.key != key]
    os.remove(f"{history_data_store_path}/{key}.json")


@st.cache_data
def load_history():
    files = os.listdir("data")
    files = sorted(files, reverse=True)
    return [load_history_item(file) for file in files]


def use_history_messages(key: str):
    st.session_state["select_item"] = key
    history = st.session_state["history"]
    items = [h for h in history if h.key == key]
    if len(items) == 0:
        return
    assert len(items) == 1
    st.session_state["messages"] = items[0].content


def generate_chat_session_key() -> str:
    return str(int(time.time()))


def save_message_to_file(messages: List[dict[str, str]], key=None):
    if not key:
        key = generate_chat_session_key()
    with open(f"{history_data_store_path}/{key}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, ensure_ascii=False))
        f.flush()

    # clear cache when file changed
    st.cache_data.clear()
    return key


def add_messsages_to_history_state(chat_session: ChatSession):
    for h in st.session_state["history"]:
        if h.key == chat_session.key:
            # TODO should replace item
            return

    st.session_state["history"].insert(0, chat_session)
