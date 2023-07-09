from langchain.schema import AIMessage, HumanMessage
from typing import List


def to_langchain_message(message: dict[str, str]):
    assert message["role"] in ["assistant", "user"]
    if message["role"] == "assistant":
        return AIMessage(content=message["content"])
    if message["role"] == "user":
        return HumanMessage(content=message["content"])


def to_langchain_messages(messages: List[dict[str, str]]):
    return [to_langchain_message(message) for message in messages]
