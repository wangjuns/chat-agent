"""Callback Handler that prints to std out."""
from typing import Any, Dict, List, Optional, Union

from langchain.callbacks.base import BaseCallbackHandler
from langchain.input import print_text
from langchain.schema import AgentAction, AgentFinish, LLMResult
from streamlit.delta_generator import DeltaGenerator


def _convert_newlines(text: str) -> str:
    return text.replace("\n", " \n")


class StreamingChatCallbackHandler(BaseCallbackHandler):
    """Callback Handler that prints to std out."""

    def __init__(self, generator: DeltaGenerator) -> None:
        """Initialize callback handler."""
        self.generator = generator
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.text += _convert_newlines(token)
        self.generator.markdown(self.text + "|")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.generator.markdown(self.text)
