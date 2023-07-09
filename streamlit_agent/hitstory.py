import json
import os
from typing import List
import time
import streamlit as st
from pydantic import BaseModel


class ChatSession(BaseModel):
    """
    single chat session content.
    contains multiple chat pair.
    """

    key: str
    title: str
    content: List[dict[str, str]]


def get_history_title(messages: List[dict[str, str]]):
    for message in messages:
        if message["role"] == "user":
            return message["content"]
    return ""


def load_history_item(file_name: str):
    with open(f"data/{file_name}", "r") as f:
        content = f.read()
        messages = json.loads(content)
        return [file_name.split(" .")[0], get_history_title(messages), messages]


def remove_history_item(key: str):
    print(f"remove key {key}")
    st.session_state["history"]: List[ChatSession] = [
        h for h in st.session_state["history"] if h.key != key
    ]
    os.remove(f"data/{key}.json")


@st.cache_data
def load_history():
    files = os.listdir("data")
    files = sorted(files, reverse=True)
    return [load_history_item(file) for file in files]


def use_history_messages(key: str):
    st.session_state["select_item"] = key
    history = st.session_state["history"]
    items = [h for h in history if h[0] == key]
    if len(items) == 0:
        return
    assert len(items) == 1
    st.session_state["messages"] = items[0][2]


def save_message_to_file(messages: List[dict[str, str]], key=None):
    if not key:
        key = int(time.time())
    with open(f"data/{key}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(messages, ensure_ascii=False))
        f.flush()

    # clear cache when file changed
    st.cache_data.clear()
    return key


def add_messsages_to_history_state(messages):
    for h in st.session_state["history"]:
        if h[0] == messages[0]:
            return

    st.session_state["history"].insert(0, messages)
