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
        data = []
        for line in f:
            data.append(json.loads(line))

        return ChatSession(key=file_name.split(".")[0], content=data)


def remove_history_item(key: str):
    print(f"remove key {key}")
    st.session_state["history"] = [h for h in st.session_state["history"] if h.key != key]
    os.remove(f"{history_data_store_path}/{key}.jsonl")


@st.cache_data
def load_history():
    files = os.listdir(history_data_store_path)
    files = [file for file in files if file.endswith(".jsonl")]
    files = sorted(files, reverse=True)
    return [load_history_item(file) for file in files]


def use_history_messages(key: str):
    st.session_state["chat_key"] = key
    history = st.session_state["history"]
    items = [h for h in history if h.key == key]
    if len(items) == 0:
        return
    assert len(items) == 1
    st.session_state["messages"] = items[0].content


def generate_chat_session_key() -> str:
    return str(int(time.time()))


def append_message_to_file(message: dict[str, str], key):
    assert key is not None, "key is None"

    with open(f"{history_data_store_path}/{key}.jsonl", "a", encoding="utf-8") as f:
        line = json.dumps(message, ensure_ascii=False)
        f.write(line + "\n")
        f.flush()

    # clear cache when file changed
    st.cache_data.clear()
    return key


def add_messsages_to_history_state(chat_session: ChatSession):
    if "history" not in st.session_state:
        st.session_state["history"] = [chat_session]
        return

    current_idx = next(
        (
            idx
            for idx, value in enumerate(st.session_state["history"])
            if value.key == chat_session.key
        ),
        None,
    )
    print(f"current key: {current_idx}")

    if current_idx is not None:
        st.session_state["history"][current_idx] = chat_session
        return

    st.session_state["history"].insert(0, chat_session)
